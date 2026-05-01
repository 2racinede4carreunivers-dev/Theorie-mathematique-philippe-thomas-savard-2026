#!/usr/bin/env python3
"""
generate_animation.py v4
========================
Genere une animation narrative complete de la theorie
"L'Univers est au Carre" a partir du SCRIPT_NARRATIF_VP.md
qui utilise un systeme d'etiquettes :

  @NARRATION: x.y       -> narration principale (scene image + voix)
  @MINI_SCRIPT: x.y     -> narration de l'exemple de calcul precedent
                           (page fixe affichant le calcul)
  @EXEMPLE_CALCUL: x.y  -> marqueur explicite d'un bloc de calcul
  @NOTE: ...            -> consignes pour l'agent E1 (NON narrees)
  <img src="...">       -> illustrations a afficher
  ---                   -> separateurs de blocs

Produit :
  - HTML autonome avec lecteur video-like
  - PDF formate
  - Audio TTS optionnel (voix shimmer FR)
"""

import os
import re
import sys
import json
import base64
import asyncio
import hashlib
from pathlib import Path

REPO_ROOT = os.environ.get("REPO_ROOT", ".")
SCRIPT_PATH = os.path.join(REPO_ROOT, "src", "SCRIPT_NARRATIF_VP.md")
ASSETS_DIR = os.path.join(REPO_ROOT, "assets", "animation")
ASSETS_IMG_DIR = os.path.join(REPO_ROOT, "assets", "images")
OUTPUT_DIR = os.path.join(REPO_ROOT, "animation_output")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
LLM_KEY = os.environ.get("EMERGENT_LLM_KEY", "")
ENABLE_TTS = os.environ.get("ENABLE_TTS", "false").lower() == "true"
ENABLE_PDF = os.environ.get("ENABLE_PDF", "true").lower() == "true"

# ================================================================
# IMAGE FALLBACK (utilise si aucune <img> dans la section MD)
# ================================================================

FALLBACK_IMAGES = [
    "animation_A-2.png", "animation_A-3.png", "animation-A-4.png",
    "Animation_A-5.png", "animation_A-6.png",
    "animation_T-1.png", "animation_T-2.png", "animation_T-3.png",
    "animation-T-4.png", "aniamtion-T-5.png", "animation_T-6.png",
    "animation_B-1.png", "animation_B-2.png", "animation_B-3.png",
    "animation_C-1.png", "animation_C-3.png", "animation_C-5.png",
    "animation_D-1.png", "animation_D-2.png",
    "animation_E-1.png", "animation_E-2.png", "animation_E-3.png", "animation_E-4.png",
    "animation_F-1.png", "animation_G-1.png",
    "animation_H-1.png", "animation_H-2.png", "animation_H-3.png",
]


def embed_image_path(rel_or_abs_path):
    """Embed une image au format data: en cherchant dans plusieurs dossiers."""
    # Essai chemin direct (si absolu ou existant)
    candidates = [
        rel_or_abs_path,
        os.path.join(REPO_ROOT, rel_or_abs_path.lstrip("./")),
        os.path.join(ASSETS_DIR, os.path.basename(rel_or_abs_path)),
        os.path.join(ASSETS_IMG_DIR, os.path.basename(rel_or_abs_path)),
    ]
    for path in candidates:
        if os.path.exists(path):
            ext = os.path.splitext(path)[1].lstrip(".").lower() or "png"
            if ext == "jpg":
                ext = "jpeg"
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            return f"data:image/{ext};base64,{data}", os.path.basename(path)
    return None, os.path.basename(rel_or_abs_path)


def get_fallback_images():
    """Retourne une liste d'images fallback en data:url."""
    out = []
    for fname in FALLBACK_IMAGES:
        data, name = embed_image_path(fname)
        if data:
            out.append({"data": data, "name": name})
    return out


# ================================================================
# PARSEUR DU SCRIPT ETIQUETE
# ================================================================

# Regex pour les etiquettes au debut de ligne (apres espaces eventuels)
TAG_RE = re.compile(r'^\s*@(NARRATION|MINI_SCRIPT|EXEMPLE_CALCUL|NOTE|ILLUSTRATION)\s*:\s*(.*)$')
IMG_TAG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
MD_IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
SEPARATOR_RE = re.compile(r'^\s*-{3,}\s*$')
DECOR_RE = re.compile(r'^\s*={3,}\s*$')


def clean_md_text(text):
    """Nettoie le markdown pour la narration TTS."""
    # Retirer les blocs HTML img
    text = IMG_TAG_RE.sub("", text)
    text = MD_IMG_RE.sub("", text)
    # Retirer balises HTML simples
    text = re.sub(r'</?(p|div|a|span|br|h[1-6])[^>]*>', "", text, flags=re.IGNORECASE)
    # Retirer les liens markdown [texte](url) -> texte
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Bold/italic
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Headers ###
    text = re.sub(r'^#{1,6}\s+', "", text, flags=re.MULTILINE)
    # Citations >
    text = re.sub(r'^\s*>\s?', "", text, flags=re.MULTILINE)
    # Les blocs LaTeX \[ ... \] : on les remplace par une mention
    text = re.sub(r'\\\[(.+?)\\\]', "", text, flags=re.DOTALL)
    # Filtrer lignes "Voir l'illustration..." (indications visuelles, non narrees)
    text = re.sub(r'^.*Voir l[\u2019\']illustration.*$', "", text, flags=re.MULTILINE)
    # Filtrer lignes-titre des mini-scripts ("script narratif de l'exemple...")
    text = re.sub(
        r'^.*script narratif de l[\u2019\']exemple.*$',
        "",
        text,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    # Filtrer emojis decoratifs isoles
    text = re.sub(r'[\U0001F300-\U0001FAFF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u27BF]', "", text)
    # Lignes vides multiples
    text = re.sub(r'\n{3,}', "\n\n", text)
    return text.strip()


def parse_tagged_script(md_content):
    """Parse le markdown en sections etiquetees.

    Logique : chaque etiquette @TAG ouvre une section. Le contenu de la section
    s'etend jusqu'a la prochaine etiquette. Les separateurs `---` et `===` sont
    consideres comme du decor et ignores. Les @NOTE n'interrompent pas la section
    en cours -- elles sont juste extraites pour reference (et exclues du contenu
    narre).

    Retourne :
    [{"tag": "NARRATION"|"MINI_SCRIPT"|"EXEMPLE_CALCUL"|"PROSE",
      "id": "x.y" ou None,
      "raw": str,
      "text": str (texte narratif nettoye, NOTES exclues),
      "calc_raw": str (parties qui ressemblent a un calcul, raw),
      "narrative_raw": str (parties qui ne sont PAS du calcul, raw),
      "notes": [str],
      "images": [str src]}]
    """
    lines = md_content.split("\n")
    sections = []
    current = {"tag": "PROSE", "id": None, "lines": [], "notes": []}

    stop_markers = ("FIN DU SCRIPT", "NOTE POUR L", "Consigne pour employer")

    def push():
        if current["lines"] or current["tag"] != "PROSE" or current["notes"]:
            sections.append({
                "tag": current["tag"],
                "id": current["id"],
                "lines": current["lines"][:],
                "notes": current["notes"][:],
            })

    in_note = False
    note_buf = []
    for line in lines:
        if any(m in line for m in stop_markers):
            break

        if DECOR_RE.match(line):
            continue
        if SEPARATOR_RE.match(line):
            # fin eventuelle d'une note multi-ligne
            if in_note:
                current["notes"].append(" ".join(note_buf).strip())
                note_buf = []
                in_note = False
            continue

        m = TAG_RE.match(line)
        if m:
            tag = m.group(1)
            if in_note:
                current["notes"].append(" ".join(note_buf).strip())
                note_buf = []
                in_note = False

            if tag == "NOTE":
                # Demarrer la capture d'une note (potentiellement multi-ligne)
                in_note = True
                note_buf = [m.group(2).strip()]
                continue

            if tag == "ILLUSTRATION":
                # On la traite comme un marqueur, le contenu (image markdown) suit
                continue

            # Tag majeur : NARRATION, MINI_SCRIPT, EXEMPLE_CALCUL
            push()
            current = {
                "tag": tag,
                "id": m.group(2).strip() or None,
                "lines": [],
                "notes": [],
            }
            continue

        if in_note:
            # Ligne de continuation de la note (jusqu'a la prochaine ligne vide ou tag)
            if line.strip() == "":
                current["notes"].append(" ".join(note_buf).strip())
                note_buf = []
                in_note = False
            else:
                note_buf.append(line.strip())
            continue

        current["lines"].append(line)

    if in_note and note_buf:
        current["notes"].append(" ".join(note_buf).strip())
    push()

    # Post-traitement
    for s in sections:
        raw = "\n".join(s["lines"])
        s["raw"] = raw
        s["images"] = IMG_TAG_RE.findall(raw)

        # Separer la partie "calcul" de la partie "narrative" dans les sections NARRATION
        calc_raw, narrative_raw = split_calc_from_narrative(raw)
        s["calc_raw"] = calc_raw
        s["narrative_raw"] = narrative_raw
        s["text"] = clean_md_text(narrative_raw)

    # Filtrer les sections completement vides
    sections = [s for s in sections if (
        s["text"] or s["images"] or s["calc_raw"].strip() or s["tag"] in ("MINI_SCRIPT", "EXEMPLE_CALCUL")
    )]
    return sections


def split_calc_from_narrative(raw):
    """Separe le contenu raw en (calc_raw, narrative_raw).

    Heuristique : un paragraphe est considere comme 'calcul' s'il contient
    plusieurs lignes avec '=' et des chiffres, ou des formules LaTeX, ou des
    tableaux markdown, ou des indices d'exemples (Suite A:, Digamma...).
    """
    paragraphs = re.split(r'\n\s*\n', raw)
    calc_parts = []
    narr_parts = []
    for p in paragraphs:
        if not p.strip():
            continue
        if looks_like_calc(p):
            calc_parts.append(p)
        else:
            narr_parts.append(p)
    return ("\n\n".join(calc_parts), "\n\n".join(narr_parts))


def looks_like_calc(text):
    """Detecte si un paragraphe est un bloc de calcul/exemple."""
    if not text.strip():
        return False
    # Indices forts : LaTeX bloc
    if re.search(r'\\\[|\\text\{|\\frac|\\left|\\sqrt', text):
        return True
    # Tableau markdown
    if re.search(r'^\s*\|.+\|', text, re.MULTILINE):
        return True
    # Mots-cles d'exemple (mais pas pris isolement)
    keywords = ["Suite A", "Suite B", "Digamma", "Nombre premier", "ième position",
                "Matrice", "matrice", "Pour (", "pour (", "1ière équation",
                "2ième équation", "3ième équation"]
    has_kw = any(k in text for k in keywords)
    # Plusieurs lignes avec '=' et des chiffres
    eq_lines = sum(1 for ln in text.split("\n")
                   if "=" in ln and re.search(r'\d', ln))
    if has_kw and eq_lines >= 1:
        return True
    if eq_lines >= 2:
        return True
    return False


def build_scenes_from_blocks(blocks):
    """Convertit la liste de sections en scenes TTS.

    - NARRATION  -> scene 'narration' (image + texte narratif)
                    Si la section contient aussi un bloc de calcul,
                    celui-ci est conserve comme calc candidat pour le mini-script
                    suivant.
    - EXEMPLE_CALCUL -> stocke le calcul comme candidat
    - MINI_SCRIPT -> scene 'calculation' (texte du mini-script lu en voix off,
                    page = calcul candidat affiche en plein ecran)
    - NOTE -> ignore (ces consignes restent dans s['notes'] pour log mais
              jamais narrees ni affichees a l'ecran)
    """
    scenes = []
    pending_calc_raw = None
    fallback_imgs = get_fallback_images()
    fallback_idx = 0
    used_imgs = set()

    def next_fallback():
        nonlocal fallback_idx
        for _ in range(len(fallback_imgs)):
            if fallback_idx < len(fallback_imgs):
                img = fallback_imgs[fallback_idx]
                fallback_idx += 1
                if img["name"] not in used_imgs:
                    used_imgs.add(img["name"])
                    return img
            else:
                break
        return None

    def resolve_image(img_srcs):
        for src in img_srcs:
            data, name = embed_image_path(src)
            if data:
                used_imgs.add(name)
                return {"data": data, "name": name}
        return None

    for s in blocks:
        tag = s["tag"]

        if tag == "NARRATION":
            # Si la section contient un calc_raw, il devient pending pour le prochain mini-script
            if s["calc_raw"].strip():
                pending_calc_raw = s["calc_raw"]

            text = s["text"]
            if not text.strip() and not s["images"]:
                # Narration sans texte ni image : skip
                continue

            img = resolve_image(s["images"]) if s["images"] else None
            if img is None:
                img = next_fallback()

            scenes.append({
                "type": "narration",
                "id": s["id"],
                "title": f"Narration {s['id']}" if s["id"] else "Narration",
                "text": text or s["title"] if False else (text or ""),
                "image": img,
                "calc_html": None,
            })
            continue

        if tag == "EXEMPLE_CALCUL":
            # Le contenu (raw) est le calcul a afficher
            content = s["calc_raw"] if s["calc_raw"].strip() else s["raw"]
            if content.strip():
                pending_calc_raw = content
            continue

        if tag == "MINI_SCRIPT":
            calc_raw = pending_calc_raw if pending_calc_raw else s["calc_raw"]
            if not calc_raw.strip():
                # Pas de calcul candidat : on cree quand meme la scene avec
                # un placeholder textuel
                calc_raw = "(Exemple de calcul non identifie)"

            mini_text = s["text"]
            if not mini_text.strip():
                # Mini-script sans contenu narratif : on saute
                pending_calc_raw = None
                continue

            scenes.append({
                "type": "calculation",
                "id": s["id"],
                "title": f"Exemple de calcul {s['id']}" if s["id"] else "Exemple de calcul",
                "text": mini_text,
                "image": None,
                "calc_html": render_calc_block(calc_raw),
                "calc_raw": calc_raw,
            })
            pending_calc_raw = None
            continue

        # PROSE residuel : ignore
        continue

    for i, sc in enumerate(scenes):
        sc["num"] = i + 1
    return scenes


def render_calc_block(raw_text):
    """Convertit le texte brut d'un exemple de calcul en HTML stylise.

    - Conserve les retours a la ligne (formule monospace)
    - Detecte les blocs LaTeX \\[ ... \\] et les laisse tels quels (rendu via MathJax)
    - Met les titres ### en valeur
    """
    # Nettoyer balises HTML img/divers
    text = IMG_TAG_RE.sub("", raw_text)
    text = re.sub(r'</?(p|div|a|span|br|h[1-6])[^>]*>', "", text, flags=re.IGNORECASE)

    # Headers markdown -> <h4>
    def h_repl(m):
        return f'<h4 class="calc-h">{m.group(2).strip()}</h4>'
    text = re.sub(r'^(#{2,4})\s+(.+)$', h_repl, text, flags=re.MULTILINE)

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # Lignes de formules \[ ... \] : conservees pour MathJax
    # Le reste : enrobe dans <pre> pour preserver l'alignement
    parts = re.split(r'(\\\[.+?\\\])', text, flags=re.DOTALL)
    out = []
    for p in parts:
        if not p.strip():
            continue
        if p.startswith(r'\['):
            # Formule LaTeX : MathJax la rendra
            out.append(f'<div class="calc-formula">{p}</div>')
        else:
            # Echapper HTML basique tout en preservant les <h4>, <strong>, <em> ajoutes
            # On prend une approche simple : on detecte les balises generees
            # et on les laisse, le reste est dans un <pre>
            sub_parts = re.split(r'(<h4 class="calc-h">[^<]+</h4>|<strong>[^<]+</strong>|<em>[^<]+</em>)', p)
            for sp in sub_parts:
                if not sp.strip():
                    continue
                if sp.startswith('<'):
                    out.append(sp)
                else:
                    # Echapper < > & dans le code brut
                    safe = sp.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    # Restaurer les blocs LaTeX inline \(...\)
                    safe = re.sub(r'\\\\\\\((.+?)\\\\\\\)', r'\\(\1\\)', safe)
                    out.append(f'<pre class="calc-pre">{safe}</pre>')
    return "\n".join(out)


# ================================================================
# TTS GENERATION
# ================================================================

async def generate_tts(scenes):
    if not LLM_KEY:
        print("  Pas de cle LLM (EMERGENT_LLM_KEY).")
        return {}
    try:
        from emergentintegrations.llm.openai import OpenAITextToSpeech
    except ImportError:
        print("  emergentintegrations non installe.")
        return {}

    tts = OpenAITextToSpeech(api_key=LLM_KEY)
    audio_map = {}
    os.makedirs(AUDIO_DIR, exist_ok=True)

    for scene in scenes:
        num = scene["num"]
        text = scene["text"][:4000]
        if not text.strip():
            continue

        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        mp3_path = os.path.join(AUDIO_DIR, f"scene_{num:03d}_{text_hash}.mp3")

        if os.path.exists(mp3_path):
            print(f"  Scene {num}: cache")
            with open(mp3_path, "rb") as f:
                audio_map[num] = base64.b64encode(f.read()).decode()
            continue

        try:
            print(f"  Scene {num}/{len(scenes)} ({scene['type']}): TTS...")
            audio_bytes = await tts.generate_speech(
                text=text,
                model="tts-1-hd",
                voice="shimmer",
                speed=0.95,
                response_format="mp3"
            )
            with open(mp3_path, "wb") as f:
                f.write(audio_bytes)
            audio_map[num] = base64.b64encode(audio_bytes).decode()
        except Exception as e:
            print(f"  Scene {num}: erreur - {str(e)[:80]}")
            import time
            time.sleep(3)

    return audio_map


# ================================================================
# HTML GENERATION - VIDEO PLAYER STYLE
# ================================================================

def generate_html(scenes, audio_map):
    total = len(scenes)
    scenes_data = []
    for s in scenes:
        scenes_data.append({
            "num": s["num"],
            "title": s["title"],
            "type": s["type"],
            "image": s["image"]["data"] if s.get("image") else None,
            "calc_html": s.get("calc_html"),
            "audio": audio_map.get(s["num"]),
        })

    scenes_json = json.dumps(scenes_data, ensure_ascii=False)

    html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>L'Univers est au Carre - Animation</title>
<script>
window.MathJax = {
  tex: { inlineMath: [['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']] },
  svg: { fontCache: 'global' }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0a0a0a;
  color: #f5f5f5;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.player {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  overflow: hidden;
}
.player img {
  max-width: 95%;
  max-height: 90vh;
  object-fit: contain;
  transition: opacity 0.6s ease;
}
.calc-page {
  width: 92%;
  max-width: 1100px;
  max-height: 90vh;
  overflow-y: auto;
  background: #1a1a1a;
  border: 2px solid #c9a84c;
  border-radius: 12px;
  padding: 32px 40px;
  color: #f0e8d0;
  font-family: 'Georgia', 'Cambria', serif;
  font-size: 1.05rem;
  line-height: 1.55;
  box-shadow: 0 10px 40px rgba(201, 168, 76, 0.18);
}
.calc-page h4 {
  color: #c9a84c;
  font-family: 'Helvetica Neue', sans-serif;
  font-size: 1.05rem;
  letter-spacing: 0.5px;
  margin: 14px 0 8px;
  border-bottom: 1px solid #3a3324;
  padding-bottom: 4px;
}
.calc-page .calc-pre {
  font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
  font-size: 0.95rem;
  color: #e8e0c0;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 6px 0;
  background: transparent;
}
.calc-page .calc-formula {
  text-align: center;
  margin: 12px 0;
  color: #ffd866;
  font-size: 1.15rem;
}
.calc-page strong { color: #ffd866; }
.calc-page em { color: #d8c890; font-style: italic; }
.no-image {
  color: #555;
  font-size: 1.2rem;
  text-align: center;
}
.title-overlay {
  position: absolute;
  top: 20px;
  left: 30px;
  background: rgba(0,0,0,0.75);
  padding: 8px 18px;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #c9a84c;
  letter-spacing: 1px;
  pointer-events: none;
  transition: opacity 0.5s;
  z-index: 10;
}
.type-badge {
  position: absolute;
  top: 20px;
  right: 30px;
  background: rgba(201, 168, 76, 0.85);
  color: #000;
  padding: 6px 14px;
  border-radius: 4px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  font-weight: bold;
  pointer-events: none;
  z-index: 10;
}
.controls {
  background: #111;
  border-top: 1px solid #2a2a2a;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.controls button {
  background: none;
  border: 1px solid #555;
  color: #fff;
  padding: 8px 16px;
  font-size: 1.05rem;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.2s, border-color 0.2s, color 0.2s;
  min-width: 48px;
}
.controls button:hover {
  background: #c9a84c;
  color: #000;
  border-color: #c9a84c;
}
.controls button.active {
  background: #c9a84c;
  color: #000;
  border-color: #c9a84c;
}
.progress-bar {
  flex: 1;
  height: 6px;
  background: #333;
  border-radius: 3px;
  cursor: pointer;
  position: relative;
}
.progress-fill {
  height: 100%;
  background: #c9a84c;
  border-radius: 3px;
  transition: width 0.3s;
}
.time-display {
  color: #888;
  font-size: 0.85rem;
  min-width: 90px;
  text-align: center;
  font-variant-numeric: tabular-nums;
}
</style>
</head>
<body>
<div class="player" id="player">
  <div class="title-overlay" id="title-overlay" data-testid="title-overlay"></div>
  <div class="type-badge" id="type-badge" data-testid="type-badge"></div>
  <img id="scene-image" src="" alt="" data-testid="scene-image" style="display:none;">
  <div class="calc-page" id="calc-page" data-testid="calc-page" style="display:none;"></div>
  <div class="no-image" id="no-image" style="display:none;">Chargement...</div>
</div>
<div class="controls">
  <button id="btn-prev" data-testid="prev-btn" title="Section precedente">&#9664;&#9664;</button>
  <button id="btn-play" data-testid="play-btn" title="Lecture / Pause">&#9654;</button>
  <button id="btn-next" data-testid="next-btn" title="Section suivante">&#9654;&#9654;</button>
  <div class="progress-bar" id="progress-bar" data-testid="progress-bar">
    <div class="progress-fill" id="progress-fill"></div>
  </div>
  <span class="time-display" id="time-display" data-testid="time-display">1 / __TOTAL__</span>
</div>
<script>
const scenes = __SCENES_JSON__;
const total = scenes.length;
let current = 0;
let playing = false;
let audio = null;

const img = document.getElementById('scene-image');
const calcPage = document.getElementById('calc-page');
const noImg = document.getElementById('no-image');
const titleOv = document.getElementById('title-overlay');
const typeBadge = document.getElementById('type-badge');
const btnPlay = document.getElementById('btn-play');
const btnPrev = document.getElementById('btn-prev');
const btnNext = document.getElementById('btn-next');
const progressFill = document.getElementById('progress-fill');
const timeDisplay = document.getElementById('time-display');
const progressBar = document.getElementById('progress-bar');

function showScene(idx) {
  if (idx < 0 || idx >= total) return;
  current = idx;
  const scene = scenes[current];

  // Reset displays
  img.style.display = 'none';
  calcPage.style.display = 'none';
  noImg.style.display = 'none';

  if (scene.type === 'calculation' && scene.calc_html) {
    calcPage.innerHTML = scene.calc_html;
    calcPage.style.display = 'block';
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([calcPage]).catch(() => {});
    }
    typeBadge.textContent = 'Exemple de calcul';
    typeBadge.style.display = 'block';
  } else if (scene.image) {
    img.src = scene.image;
    img.style.display = 'block';
    typeBadge.textContent = 'Narration';
    typeBadge.style.display = 'block';
  } else {
    noImg.style.display = 'block';
    noImg.textContent = scene.title;
    typeBadge.style.display = 'none';
  }

  titleOv.textContent = scene.title;
  titleOv.style.opacity = 1;
  setTimeout(() => { titleOv.style.opacity = 0.4; }, 4000);

  progressFill.style.width = ((current + 1) / total * 100) + '%';
  timeDisplay.textContent = (current + 1) + ' / ' + total;
}

function playAudio() {
  if (audio) { audio.pause(); audio = null; }
  const scene = scenes[current];
  if (scene.audio) {
    audio = new Audio('data:audio/mp3;base64,' + scene.audio);
    audio.play().catch(err => console.error('Audio err', err));
    audio.onended = function() {
      if (playing && current < total - 1) {
        current++;
        showScene(current);
        setTimeout(playAudio, 600);
      } else {
        playing = false;
        btnPlay.innerHTML = '&#9654;';
        btnPlay.classList.remove('active');
      }
    };
  } else {
    if (playing && current < total - 1) {
      setTimeout(() => {
        if (playing) {
          current++;
          showScene(current);
          playAudio();
        }
      }, 6000);
    }
  }
}

function togglePlay() {
  playing = !playing;
  if (playing) {
    btnPlay.innerHTML = '&#9646;&#9646;';
    btnPlay.classList.add('active');
    showScene(current);
    playAudio();
  } else {
    btnPlay.innerHTML = '&#9654;';
    btnPlay.classList.remove('active');
    if (audio) audio.pause();
  }
}

btnPlay.addEventListener('click', togglePlay);
btnPrev.addEventListener('click', () => {
  if (audio) { audio.pause(); audio = null; }
  if (current > 0) { current--; showScene(current); if (playing) playAudio(); }
});
btnNext.addEventListener('click', () => {
  if (audio) { audio.pause(); audio = null; }
  if (current < total - 1) { current++; showScene(current); if (playing) playAudio(); }
});

progressBar.addEventListener('click', (e) => {
  const rect = progressBar.getBoundingClientRect();
  const pct = (e.clientX - rect.left) / rect.width;
  const idx = Math.floor(pct * total);
  if (audio) { audio.pause(); audio = null; }
  showScene(idx);
  if (playing) playAudio();
});

document.addEventListener('keydown', (e) => {
  if (e.key === ' ') { e.preventDefault(); togglePlay(); }
  if (e.key === 'ArrowRight') { btnNext.click(); }
  if (e.key === 'ArrowLeft') { btnPrev.click(); }
});

showScene(0);
</script>
</body>
</html>'''

    html = html.replace('__SCENES_JSON__', scenes_json)
    html = html.replace('__TOTAL__', str(total))
    return html


# ================================================================
# PDF GENERATION
# ================================================================

def generate_pdf(scenes, pdf_path):
    try:
        from weasyprint import HTML
        print("  Generation PDF...")

        pages_html = ""
        total = len(scenes)
        for s in scenes:
            num = s["num"]
            type_label = "Exemple de calcul" if s["type"] == "calculation" else "Narration"
            content_html = ""
            if s["type"] == "calculation" and s.get("calc_html"):
                content_html = f'<div class="calc-box">{s["calc_html"]}</div>'
            elif s.get("image"):
                content_html = f'<div class="img-box"><img src="{s["image"]["data"]}"></div>'

            text = s["text"]
            text_html = "".join(
                f"<p>{p.strip()}</p>" for p in text.split("\n\n") if p.strip()
            )

            pages_html += f'''
<div class="page">
  <div class="hdr">
    <span>Page {num} / {total} - {type_label}</span>
    <h2>{s["title"]}</h2>
  </div>
  {content_html}
  <div class="txt">{text_html}</div>
</div>'''

        pdf_html = f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<style>
@page {{ size: A4; margin: 2cm; }}
body {{ font-family: Georgia, serif; font-size: 10pt; line-height: 1.5; color: #1a1a1a; }}
.page {{ page-break-after: always; }}
.page:last-child {{ page-break-after: avoid; }}
.hdr {{ border-bottom: 2px solid #8b7332; padding-bottom: 8px; margin-bottom: 15px; }}
.hdr span {{ font-size: 8pt; color: #8b7332; }}
.hdr h2 {{ font-size: 14pt; margin: 4px 0 0; }}
.img-box {{ text-align: center; margin: 10px 0; }}
.img-box img {{ max-width: 75%; max-height: 250px; }}
.calc-box {{
  border: 1px solid #8b7332;
  background: #fdfaf0;
  padding: 12px 16px;
  margin: 10px 0;
  font-family: 'Courier New', monospace;
  font-size: 9pt;
  white-space: pre-wrap;
}}
.calc-box .calc-pre {{ white-space: pre-wrap; font-family: inherit; margin: 0; }}
.calc-box h4 {{ font-family: Georgia, serif; color: #8b7332; font-size: 10pt; margin: 8px 0 4px; }}
.calc-box .calc-formula {{ text-align: center; margin: 8px 0; font-style: italic; }}
.txt p {{ margin-bottom: 6px; text-align: justify; }}
</style></head><body>{pages_html}</body></html>'''

        HTML(string=pdf_html).write_pdf(pdf_path)
        print(f"  PDF : {pdf_path}")
        return True
    except Exception as e:
        print(f"  Erreur PDF : {e}")
        return False


# ================================================================
# MAIN
# ================================================================

async def async_main():
    print("=" * 60)
    print("ANIMATION v4 - L'Univers est au Carre (etiquettes)")
    print("=" * 60)

    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        md = f.read()
    print(f"Script : {len(md)} chars, {md.count(chr(10))} lignes")

    # Parse en blocs etiquetes
    blocks = parse_tagged_script(md)
    by_tag = {}
    for b in blocks:
        by_tag[b["tag"]] = by_tag.get(b["tag"], 0) + 1
    print("Blocs detectes :", by_tag)

    # Construire les scenes
    scenes = build_scenes_from_blocks(blocks)
    n_narr = sum(1 for s in scenes if s["type"] == "narration")
    n_calc = sum(1 for s in scenes if s["type"] == "calculation")
    print(f"Scenes : {len(scenes)} total ({n_narr} narration, {n_calc} calcul)")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # TTS
    audio_map = {}
    if ENABLE_TTS:
        print("\n--- TTS (shimmer, FR) ---")
        audio_map = await generate_tts(scenes)
        print(f"Audio : {len(audio_map)} fichiers")

    # HTML
    print("\n--- HTML ---")
    html = generate_html(scenes, audio_map)
    html_path = os.path.join(OUTPUT_DIR, "animation.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML : {html_path}")

    # PDF
    if ENABLE_PDF:
        print("\n--- PDF ---")
        generate_pdf(scenes, os.path.join(OUTPUT_DIR, "animation.pdf"))

    # Index
    index = [{
        "num": s["num"], "title": s["title"], "type": s["type"], "id": s.get("id"),
        "has_audio": s["num"] in audio_map,
        "has_image": bool(s.get("image")),
        "has_calc": bool(s.get("calc_html")),
    } for s in scenes]
    with open(os.path.join(OUTPUT_DIR, "scenes_index.json"), "w") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"ANIMATION : {len(scenes)} scenes ({n_narr} narration, {n_calc} calcul), {len(audio_map)} audio")
    print(f"{'=' * 60}")
    return 0


def main():
    return asyncio.run(async_main())


if __name__ == "__main__":
    sys.exit(main())
