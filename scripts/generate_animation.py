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
# (FALLBACK SUPPRIME : seules les illustrations presentes dans le .md
# sont utilisees dans l'animation, conformement aux instructions)
# ================================================================


def embed_image_path(rel_or_abs_path):
    """Embed une image au format data: en cherchant dans plusieurs dossiers.

    Recherche insensible a la casse car les noms dans le .md ne correspondent
    pas toujours exactement aux fichiers reels (ex: animation_A-5.png vs
    Animation_A-5.png).
    """
    target_basename = os.path.basename(rel_or_abs_path)
    # Candidats directs (rapides, sensibles a la casse)
    candidates = [
        rel_or_abs_path,
        os.path.join(REPO_ROOT, rel_or_abs_path.lstrip("./")),
        os.path.join(ASSETS_DIR, target_basename),
        os.path.join(ASSETS_IMG_DIR, target_basename),
    ]
    for path in candidates:
        if os.path.exists(path):
            return _read_image_as_data_url(path)

    # Recherche insensible a la casse dans les dossiers d'assets
    target_lower = target_basename.lower()
    for assets_dir in (ASSETS_DIR, ASSETS_IMG_DIR,
                       os.path.join(REPO_ROOT, "assets", "animation"),
                       os.path.join(REPO_ROOT, "assets", "images"),
                       os.path.join(REPO_ROOT, "assets")):
        if not os.path.isdir(assets_dir):
            continue
        try:
            for fname in os.listdir(assets_dir):
                if fname.lower() == target_lower:
                    return _read_image_as_data_url(
                        os.path.join(assets_dir, fname)
                    )
        except OSError:
            continue
    return None, target_basename


def _read_image_as_data_url(path):
    """Lit une image et retourne (data_url, basename)."""
    ext = os.path.splitext(path)[1].lstrip(".").lower() or "png"
    if ext == "jpg":
        ext = "jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/{ext};base64,{data}", os.path.basename(path)


# ================================================================
# PARSEUR DU SCRIPT ETIQUETE
# ================================================================

# Regex pour les etiquettes au debut de ligne (apres espaces eventuels)
TAG_RE = re.compile(r'^\s*@(NARRATION|MINI_SCRIPT|EXEMPLE_CALCUL|NOTE|ILLUSTRATION)\s*:\s*(.*)$')

# Reconnaitre les illustrations dans le markdown :
# 1. <img src="..."> direct
# 2. <a href="...png|jpg|jpeg|webp">...</a> (hyperlien vers une image asset)
# 3. ![alt](path) markdown
IMG_TAG_RE = re.compile(r'<img\b[^>]*?src=["\']([^"\']+)["\'][^>]*?>', re.IGNORECASE | re.DOTALL)
A_HREF_IMG_RE = re.compile(
    r'<a\b[^>]*?href=["\']([^"\']+\.(?:png|jpg|jpeg|webp|gif))["\'][^>]*?>',
    re.IGNORECASE | re.DOTALL,
)
MD_IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)]+\.(?:png|jpg|jpeg|webp|gif))\)', re.IGNORECASE)
SEPARATOR_RE = re.compile(r'^\s*-{3,}\s*$')
DECOR_RE = re.compile(r'^\s*={3,}\s*$')


def extract_all_image_refs(raw):
    """Extrait toutes les references aux illustrations dans l'ordre d'apparition.

    Retourne une liste de dicts {pos: int, src: str} ou pos est l'offset
    en caracteres dans `raw`.
    """
    refs = []
    for regex in (IMG_TAG_RE, A_HREF_IMG_RE, MD_IMG_RE):
        for m in regex.finditer(raw):
            refs.append({"pos": m.start(), "src": m.group(1)})
    refs.sort(key=lambda r: r["pos"])
    # Deduplication consecutive (meme image referencee 2x sans texte entre)
    out = []
    for r in refs:
        if not out or out[-1]["src"] != r["src"]:
            out.append(r)
    return out


def clean_md_text(text):
    """Nettoie le markdown pour la narration TTS."""
    # Retirer les blocs HTML img + hyperliens vers images
    text = IMG_TAG_RE.sub("", text)
    text = A_HREF_IMG_RE.sub("", text)
    text = re.sub(r'</a>', "", text, flags=re.IGNORECASE)
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
    # Filtrer "Voir l'animation / application web" et autres indications similaires
    text = re.sub(r'^.*Voir l[\u2019\']animation.*$', "", text, flags=re.MULTILINE)
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
        # Extraire toutes les illustrations dans l'ordre (img + a href + md ![])
        s["image_refs"] = extract_all_image_refs(raw)
        s["images"] = [r["src"] for r in s["image_refs"]]

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


def split_narration_by_image_positions(narrative_raw, image_refs):
    """Decoupe une section narration en sous-segments basees sur les positions
    des images.

    Chaque sous-segment correspond au texte qui SUIT une illustration (jusqu'a
    la prochaine, ou jusqu'a la fin). Le texte AVANT la premiere image est
    rattache a celui de la premiere image.

    Retourne une liste de tuples (image_src_or_None, text_raw).
    Si aucune image n'est trouvee, retourne [(None, narrative_raw)].
    """
    if not image_refs:
        return [(None, narrative_raw)]

    # On doit retrouver la position des images dans `narrative_raw`.
    # `image_refs` a ete extrait de `raw` (qui contient peut-etre aussi le
    # calc), donc on re-extrait sur narrative_raw pour avoir des positions
    # coherentes.
    refs = extract_all_image_refs(narrative_raw)
    if not refs:
        return [(None, narrative_raw)]

    segments = []
    n = len(refs)
    for i, r in enumerate(refs):
        # Texte du segment : depuis la position de l'image courante jusqu'a la
        # prochaine image (ou la fin)
        if i == 0:
            # Inclut le texte AVANT la premiere image dans le 1er segment
            start = 0
        else:
            start = refs[i]["pos"]
        end = refs[i + 1]["pos"] if i + 1 < n else len(narrative_raw)
        seg_text = narrative_raw[start:end]
        segments.append((r["src"], seg_text))
    return segments


def build_scenes_from_blocks(blocks):
    """Convertit la liste de sections en scenes.

    Regle stricte : SEULES les illustrations referencees dans le .md sont
    utilisees (aucun fallback). Si une section narration n'a pas
    d'illustration, on conserve la derniere illustration affichee.

    - NARRATION : decoupee en sous-scenes selon les positions d'images.
                  Chaque sous-scene affiche son image pendant son texte.
    - EXEMPLE_CALCUL : stocke le calcul comme candidat
    - MINI_SCRIPT : scene 'calculation' avec page de calcul fixe + voix
                    explicative (le calcul reste affiche pendant tout le
                    mini-script)
    - NOTE : ignore (jamais narre ni affiche)
    """
    scenes = []
    pending_calc_raw = None
    last_image = None  # Image courante a conserver si pas de nouvelle

    def resolve_image(src):
        data, name = embed_image_path(src)
        if data:
            return {"data": data, "name": name, "src": src}
        return None

    for s in blocks:
        tag = s["tag"]

        if tag == "NARRATION":
            # Si la section contient un calc_raw, il devient pending pour le
            # prochain mini-script
            if s["calc_raw"].strip():
                pending_calc_raw = s["calc_raw"]

            # Decoupage de la section narration en sous-segments selon les
            # positions d'images dans la partie narrative (sans le calc)
            segments = split_narration_by_image_positions(
                s["narrative_raw"], s["image_refs"]
            )

            for img_src, seg_raw in segments:
                seg_text = clean_md_text(seg_raw)

                # Resolution image : nouvelle image si presente, sinon on
                # conserve la derniere. On memorise l'image MEME si le
                # segment de texte est vide (utile quand une image est
                # placee entre deux narrations sans texte autour).
                if img_src:
                    resolved = resolve_image(img_src)
                    if resolved:
                        last_image = resolved

                if not seg_text.strip():
                    # Segment sans texte : on saute la creation d'une
                    # scene mais on a deja memorise l'image pour la suite.
                    continue

                scenes.append({
                    "type": "narration",
                    "id": s["id"],
                    "title": f"Narration {s['id']}" if s["id"] else "Narration",
                    "text": seg_text,
                    "image": last_image,
                    "calc_html": None,
                })
            continue

        if tag == "EXEMPLE_CALCUL":
            # Pour un tag EXPLICITE @EXEMPLE_CALCUL, on prend TOUT le raw
            # (pas de filtre looks_like_calc : l'utilisateur a explicitement
            # declare que ce bloc est un calcul a afficher en entier).
            content = s["raw"]
            if content.strip():
                pending_calc_raw = content
            continue

        if tag == "MINI_SCRIPT":
            calc_raw = pending_calc_raw if pending_calc_raw else s["calc_raw"]
            if not calc_raw.strip():
                calc_raw = "(Exemple de calcul non identifie)"

            mini_text = s["text"]
            if not mini_text.strip():
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

    # Prepend la scene d'introduction (page de presentation)
    intro = build_intro_scene()
    if intro:
        scenes.insert(0, intro)

    for i, sc in enumerate(scenes):
        sc["num"] = i + 1
    return scenes


def build_intro_scene():
    """Construit la scene d'introduction basee sur les meta-donnees du projet.

    Retourne une scene de type 'intro' avec titre, photo de l'auteur,
    date et lieu. Lue par le TTS au demarrage de l'animation.
    """
    # Chercher la photo de l'auteur dans les dossiers d'assets
    author_photo = None
    for candidate in ("philippe_thomas_savard.jpg", "philippe_thomas_savard.png",
                      "auteur.jpg", "author.jpg"):
        data, name = embed_image_path(candidate)
        if data:
            author_photo = {"data": data, "name": name, "src": candidate}
            break

    # Illustration principale de presentation (animation_G-1 souvent)
    title_illustration = None
    for candidate in ("animation_G-1.png", "animation_G1.png"):
        data, name = embed_image_path(candidate)
        if data:
            title_illustration = {"data": data, "name": name, "src": candidate}
            break

    narration_text = (
        "Bienvenue dans L'Univers est au Carre, une theorie mathematique "
        "originale de Philippe Thomas Savard. Auteur autodidacte etabli a "
        "Levis, au Canada, il propose ici une exploration audacieuse de la "
        "geometrie des nombres premiers, du postulat du squaring et de ses "
        "implications philosophiques. Une invitation a penser les "
        "mathematiques autrement : rigoureuses, visuelles, et profondement "
        "humaines."
    )

    return {
        "type": "intro",
        "id": "0.0",
        "title": "L'Univers est au Carre",
        "subtitle": "Theorie mathematique de Philippe Thomas Savard",
        "author_photo": author_photo,
        "title_illustration": title_illustration,
        "meta": {
            "author": "Philippe Thomas Savard",
            "date": "30 avril 2026",
            "place": "Levis, Chaudiere-Appalaches, Canada",
            "license": "Apache 2.0",
        },
        "text": narration_text,
        "image": author_photo,  # utilise pour fallback rendu
        "calc_html": None,
    }


def render_calc_block(raw_text):
    """Convertit le texte brut d'un exemple de calcul en HTML stylise.

    - Conserve les retours a la ligne (formule monospace)
    - Detecte les blocs LaTeX \\[ ... \\] et les laisse tels quels (rendu via MathJax)
    - Met les titres ### en valeur
    - Retire les balises HTML image (<img>, <a href>, 👉 Voir l'illustration)
      qui ne doivent pas apparaitre dans le slide de calcul.
    """
    # Nettoyer balises HTML img/divers
    text = IMG_TAG_RE.sub("", raw_text)
    text = A_HREF_IMG_RE.sub("", text)
    text = re.sub(r'</a>', "", text, flags=re.IGNORECASE)
    # Retirer les lignes "👉 Voir l'illustration ..." residuelles
    text = re.sub(
        r'^\s*(?:👉\s*)?Voir l[\u2019\']illustration.*$',
        "",
        text,
        flags=re.MULTILINE,
    )
    # Retirer aussi les balises paragraphe/div/span et lignes vides multiples
    text = re.sub(r'</?(p|div|span|br)[^>]*>', "", text, flags=re.IGNORECASE)
    text = re.sub(r'</?h[1-6][^>]*>', "", text, flags=re.IGNORECASE)
    # Retirer les retours a la ligne intempestifs (lignes vides multiples)
    text = re.sub(r'\n{3,}', "\n\n", text)

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
    """Charge / genere les MP3 TTS et retourne un mapping num -> filename MP3.

    Les MP3 sont stockes dans AUDIO_DIR (animation_output/audio/) et le
    HTML les reference par URL relative `audio/<filename>.mp3` au lieu
    de les embarquer en base64 (sinon fichier HTML de 130 MB et crashes
    navigateur sur Chrome/Firefox apres la 8eme scene).
    """
    # Toujours creer le dossier audio (meme vide) pour eviter les warnings
    # de upload-artifact sur GitHub Actions
    os.makedirs(AUDIO_DIR, exist_ok=True)
    audio_map = {}  # num -> filename (ex: "scene_001_32933d60.mp3")

    # Dossier de cache persistant commit dans le repo (pour GitHub Actions
    # quand l'appel TTS externe n'est pas possible : 403 free-tier Emergent,
    # budget epuise, etc.). On le charge EN PREMIER.
    AUDIO_CACHE_DIR = os.path.join(REPO_ROOT, "assets", "audio_cache")
    cache_hits = 0
    if os.path.isdir(AUDIO_CACHE_DIR):
        for scene in scenes:
            num = scene["num"]
            text = scene["text"][:4000]
            if not text.strip():
                continue
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            filename = f"scene_{num:03d}_{text_hash}.mp3"
            cache_path = os.path.join(AUDIO_CACHE_DIR, filename)
            if os.path.exists(cache_path):
                audio_map[num] = filename
                cache_hits += 1
                # Copie dans le dossier runtime pour que le HTML
                # puisse pointer dessus via URL relative
                runtime_path = os.path.join(AUDIO_DIR, filename)
                if not os.path.exists(runtime_path):
                    import shutil as _sh
                    _sh.copy2(cache_path, runtime_path)
        if cache_hits:
            print(f"  {cache_hits} audios charges depuis assets/audio_cache/")

    # Charger aussi les MP3 deja dans AUDIO_DIR (runtime)
    for scene in scenes:
        num = scene["num"]
        text = scene["text"][:4000]
        if not text.strip():
            continue
        if num in audio_map:
            continue
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        filename = f"scene_{num:03d}_{text_hash}.mp3"
        mp3_path = os.path.join(AUDIO_DIR, filename)
        if os.path.exists(mp3_path):
            audio_map[num] = filename
    if audio_map:
        print(f"  {len(audio_map)} audios disponibles (cache + runtime)")

    if not LLM_KEY:
        if audio_map:
            print("  Cle LLM absente : utilisation du cache uniquement.")
        else:
            print("  [ATTENTION] Cle LLM (EMERGENT_LLM_KEY) manquante ou vide.")
            print("  [ATTENTION] Sur GitHub Actions, verifiez que le secret '_CLE'")
            print("  [ATTENTION] est configure dans Settings > Secrets > Actions.")
        return audio_map
    print(f"  Cle LLM detectee (longueur: {len(LLM_KEY)} chars)")

    try:
        from emergentintegrations.llm.openai import OpenAITextToSpeech
    except ImportError:
        print("  [ERREUR] emergentintegrations non installe.")
        print("  [INFO]   Installer avec : pip install emergentintegrations \\")
        print("                            --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/")
        return audio_map

    tts = OpenAITextToSpeech(api_key=LLM_KEY)
    errors = 0

    for scene in scenes:
        num = scene["num"]
        text = scene["text"][:4000]
        if not text.strip():
            continue
        # Deja en cache (charge ci-dessus), on saute
        if num in audio_map:
            continue

        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        filename = f"scene_{num:03d}_{text_hash}.mp3"
        mp3_path = os.path.join(AUDIO_DIR, filename)

        # Retry avec backoff exponentiel sur erreurs reseau / rate limit
        success = False
        for attempt in range(3):
            try:
                print(f"  Scene {num}/{len(scenes)} ({scene['type']}): TTS..."
                      f"{' (retry ' + str(attempt) + ')' if attempt else ''}")
                audio_bytes = await tts.generate_speech(
                    text=text,
                    model="tts-1-hd",
                    voice="shimmer",
                    speed=0.95,
                    response_format="mp3"
                )
                with open(mp3_path, "wb") as f:
                    f.write(audio_bytes)
                audio_map[num] = filename
                success = True
                break
            except Exception as e:
                err_msg = str(e)[:200]
                print(f"  Scene {num}: erreur tentative {attempt + 1}/3 - {err_msg}")
                # Si budget depasse, pas la peine de retry
                if "budget" in err_msg.lower() or "quota" in err_msg.lower():
                    print("  [ARRET] Budget LLM depasse - arret des appels TTS")
                    return audio_map
                import asyncio as _aio
                await _aio.sleep(3 * (attempt + 1))
        if not success:
            errors += 1

    print(f"  TTS termine : {len(audio_map)} audios generes/charges, {errors} echecs sur {len(scenes)} scenes")
    return audio_map


# ================================================================
# HTML GENERATION - VIDEO PLAYER STYLE
# ================================================================

def generate_html(scenes, audio_map):
    total = len(scenes)
    scenes_data = []
    for s in scenes:
        entry = {
            "num": s["num"],
            "title": s["title"],
            "type": s["type"],
            "image": s["image"]["data"] if s.get("image") else None,
            "calc_html": s.get("calc_html"),
            "audio": audio_map.get(s["num"]),
        }
        # Donnees specifiques a la scene d'intro
        if s["type"] == "intro":
            entry["subtitle"] = s.get("subtitle", "")
            entry["meta"] = s.get("meta", {})
            entry["author_photo"] = (
                s["author_photo"]["data"] if s.get("author_photo") else None
            )
            entry["title_illustration"] = (
                s["title_illustration"]["data"]
                if s.get("title_illustration") else None
            )
        scenes_data.append(entry)

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
/* ===== Scene d'intro / page de presentation ===== */
.intro-page {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(ellipse at center, #141218 0%, #050507 70%);
  position: relative;
  overflow: hidden;
}
.intro-page::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 30%, rgba(201, 168, 76, 0.15), transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(180, 120, 60, 0.12), transparent 40%);
  pointer-events: none;
}
.intro-content {
  position: relative;
  z-index: 2;
  display: flex;
  gap: 64px;
  align-items: center;
  max-width: 92%;
  padding: 40px;
}
.intro-photo {
  width: 280px;
  height: 380px;
  object-fit: cover;
  border-radius: 14px;
  border: 3px solid rgba(201, 168, 76, 0.85);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6),
              0 0 0 1px rgba(201, 168, 76, 0.2);
  flex-shrink: 0;
}
.intro-text {
  color: #f0e8d0;
  font-family: 'Georgia', 'Cambria', serif;
}
.intro-title {
  font-size: 3.4rem;
  color: #ffd866;
  font-weight: 700;
  letter-spacing: 1px;
  line-height: 1.1;
  margin-bottom: 14px;
  text-shadow: 0 2px 20px rgba(201, 168, 76, 0.3);
}
.intro-subtitle {
  font-size: 1.3rem;
  color: #c9a84c;
  margin-bottom: 38px;
  font-style: italic;
  letter-spacing: 0.5px;
}
.intro-meta {
  font-size: 1rem;
  line-height: 1.9;
  color: #d8c890;
  border-left: 2px solid rgba(201, 168, 76, 0.5);
  padding-left: 22px;
}
.intro-meta strong {
  color: #c9a84c;
  display: inline-block;
  min-width: 90px;
  letter-spacing: 0.5px;
}
</style>
</head>
<body>
<div class="player" id="player">
  <div class="title-overlay" id="title-overlay" data-testid="title-overlay"></div>
  <div class="type-badge" id="type-badge" data-testid="type-badge"></div>
  <img id="scene-image" src="" alt="" data-testid="scene-image" style="display:none;">
  <div class="calc-page" id="calc-page" data-testid="calc-page" style="display:none;"></div>
  <div class="intro-page" id="intro-page" data-testid="intro-page" style="display:none;">
    <div class="intro-content">
      <img class="intro-photo" id="intro-photo" alt="Philippe Thomas Savard">
      <div class="intro-text">
        <div class="intro-title" id="intro-title"></div>
        <div class="intro-subtitle" id="intro-subtitle"></div>
        <div class="intro-meta" id="intro-meta"></div>
      </div>
    </div>
  </div>
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

// UN SEUL element Audio reutilise (evite saturation memoire navigateur
// apres ~18 elements crees, qui causait le bug "scenes 19-29 defilent
// sans son" : audio.play() etait rejete par manque de ressources).
const audio = new Audio();
audio.preload = 'auto';
let scenePlayingIdx = -1;  // pour eviter races sur changements rapides

audio.addEventListener('ended', () => {
  if (playing && current < total - 1) {
    current++;
    showScene(current);
    playAudio();
  } else {
    playing = false;
    btnPlay.innerHTML = '&#9654;';
    btnPlay.classList.remove('active');
  }
});

audio.addEventListener('error', (e) => {
  console.error('Audio error scene ' + (current + 1), e, audio.error);
  if (playing && current < total - 1) {
    setTimeout(() => {
      if (playing) { current++; showScene(current); playAudio(); }
    }, 1500);
  }
});

const img = document.getElementById('scene-image');
const calcPage = document.getElementById('calc-page');
const noImg = document.getElementById('no-image');
const introPage = document.getElementById('intro-page');
const introPhoto = document.getElementById('intro-photo');
const introTitle = document.getElementById('intro-title');
const introSubtitle = document.getElementById('intro-subtitle');
const introMeta = document.getElementById('intro-meta');
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
  introPage.style.display = 'none';
  noImg.style.display = 'none';

  if (scene.type === 'intro') {
    if (scene.author_photo) introPhoto.src = scene.author_photo;
    introTitle.textContent = scene.title;
    introSubtitle.textContent = scene.subtitle || '';
    const meta = scene.meta || {};
    introMeta.innerHTML =
      '<strong>Auteur :</strong> ' + (meta.author || '') + '<br>' +
      '<strong>Date :</strong> ' + (meta.date || '') + '<br>' +
      '<strong>Lieu :</strong> ' + (meta.place || '') + '<br>' +
      '<strong>Licence :</strong> ' + (meta.license || '');
    introPage.style.display = 'flex';
    typeBadge.textContent = 'Presentation';
    typeBadge.style.display = 'block';
  } else if (scene.type === 'calculation' && scene.calc_html) {
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
  const scene = scenes[current];
  scenePlayingIdx = current;
  // Pause l'audio en cours et reset, sans recreer l'element
  audio.pause();
  try { audio.currentTime = 0; } catch (e) { /* ignore */ }

  if (scene.audio) {
    // Charge le nouvel MP3 via URL relative
    audio.src = 'audio/' + scene.audio;
    audio.load();
    const startedFor = current;
    audio.play().catch(err => {
      console.error('audio.play() rejected scene ' + (startedFor + 1) + ':', err);
      // Fallback : avance apres un delai court (pas 8s sinon "saute" trop vite)
      setTimeout(() => {
        if (playing && current === startedFor && current < total - 1) {
          current++; showScene(current); playAudio();
        }
      }, 3000);
    });
  } else {
    // Pas d'audio pour cette scene : avance apres un delai par defaut
    if (playing && current < total - 1) {
      const startedFor = current;
      setTimeout(() => {
        if (playing && current === startedFor) {
          current++; showScene(current); playAudio();
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
    audio.pause();
  }
}

btnPlay.addEventListener('click', togglePlay);
btnPrev.addEventListener('click', () => {
  audio.pause();
  if (current > 0) { current--; showScene(current); if (playing) playAudio(); }
});
btnNext.addEventListener('click', () => {
  audio.pause();
  if (current < total - 1) { current++; showScene(current); if (playing) playAudio(); }
});

progressBar.addEventListener('click', (e) => {
  const rect = progressBar.getBoundingClientRect();
  const pct = (e.clientX - rect.left) / rect.width;
  const idx = Math.floor(pct * total);
  audio.pause();
  showScene(idx);
  current = idx;
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
            if s["type"] == "intro":
                type_label = "Presentation"
            elif s["type"] == "calculation":
                type_label = "Exemple de calcul"
            else:
                type_label = "Narration"

            content_html = ""
            if s["type"] == "intro":
                meta = s.get("meta", {})
                photo_src = s["author_photo"]["data"] if s.get("author_photo") else ""
                content_html = f'''
<div class="intro-pdf">
  <img class="intro-pdf-photo" src="{photo_src}" alt="Auteur">
  <div class="intro-pdf-text">
    <h1 class="intro-pdf-title">{s["title"]}</h1>
    <p class="intro-pdf-sub">{s.get("subtitle", "")}</p>
    <ul class="intro-pdf-meta">
      <li><strong>Auteur :</strong> {meta.get("author", "")}</li>
      <li><strong>Date :</strong> {meta.get("date", "")}</li>
      <li><strong>Lieu :</strong> {meta.get("place", "")}</li>
      <li><strong>Licence :</strong> {meta.get("license", "")}</li>
    </ul>
  </div>
</div>'''
            elif s["type"] == "calculation" and s.get("calc_html"):
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
.intro-pdf {{ display: flex; gap: 20px; align-items: center; padding: 20px 0; }}
.intro-pdf-photo {{ width: 140px; height: 190px; object-fit: cover;
                    border: 2px solid #8b7332; border-radius: 6px; flex-shrink: 0; }}
.intro-pdf-title {{ font-size: 22pt; color: #8b7332; margin: 0 0 6px; }}
.intro-pdf-sub {{ font-size: 11pt; color: #5a4a22; font-style: italic; margin: 0 0 14px; }}
.intro-pdf-meta {{ list-style: none; padding: 0; margin: 0; font-size: 9.5pt; }}
.intro-pdf-meta li {{ padding: 3px 0; border-bottom: 1px dotted #d4c08a; }}
.intro-pdf-meta strong {{ color: #8b7332; display: inline-block; min-width: 70px; }}
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
