#!/usr/bin/env python3
"""
generate_youtube_chapters.py
=============================
Genere un chapitrage YouTube + un kit reseaux sociaux pour l'animation
"L'Univers est au Carre" a partir des durees reelles des MP3 et des
titres semantiques extraits de SCRIPT_NARRATIF_VP.md.

Produit :
- animation_output/youtube_description.txt   : description YouTube complete
                                               avec chapitres timestampes
- animation_output/youtube_chapters_only.txt : juste la liste des chapitres
- animation_output/social_media_kit.txt      : posts Twitter/X, LinkedIn,
                                               Facebook, TikTok/Reels/Shorts
- animation_output/chapters.json             : structure JSON exploitable

YouTube exige :
  - 1er chapitre debutant a 0:00
  - Au moins 3 chapitres
  - Chaque chapitre >= 10 secondes

Aucun appel API. Fonctionne sur le cache audio du repo.
"""

import os
import re
import sys
import json
import hashlib

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

from generate_animation import (  # noqa: E402
    parse_tagged_script,
    build_scenes_from_blocks,
    SCRIPT_PATH,
    OUTPUT_DIR,
    AUDIO_DIR,
    REPO_ROOT,
)

REPO_URL = "https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026"
AUTHOR = "Philippe Thomas Savard"
LOCATION = "Levis, Chaudiere-Appalaches, Canada"
LICENSE = "Apache 2.0"


def get_mp3_duration(path):
    """Retourne la duree d'un MP3 en secondes (via mutagen)."""
    try:
        from mutagen.mp3 import MP3
        return float(MP3(path).info.length)
    except Exception as e:
        print(f"  [WARN] duree inconnue pour {path}: {e}")
        return 60.0  # fallback raisonnable


def find_audio(scene_num, scene_text):
    """Localise le MP3 d'une scene (cache repo prioritaire)."""
    text_hash = hashlib.md5(scene_text[:4000].encode()).hexdigest()[:8]
    name = f"scene_{scene_num:03d}_{text_hash}.mp3"
    for d in (AUDIO_DIR, os.path.join(REPO_ROOT, "assets", "audio_cache")):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    # fallback : n'importe quel scene_NNN_*.mp3
    for d in (AUDIO_DIR, os.path.join(REPO_ROOT, "assets", "audio_cache")):
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.startswith(f"scene_{scene_num:03d}_") and f.endswith(".mp3"):
                    return os.path.join(d, f)
    return None


def extract_section_titles(md_content):
    """Extrait un titre semantique pour chaque bloc etiquete.

    Retourne un dict { (tag, sid) : titre_court } ou tag est NARRATION,
    MINI_SCRIPT ou EXEMPLE_CALCUL et sid est l'identifiant '1.0', '2.0', etc.
    """
    pattern = re.compile(
        r'^@(NARRATION|MINI_SCRIPT|EXEMPLE_CALCUL):\s*([\d.]+)\s*$',
        re.MULTILINE,
    )
    matches = list(pattern.finditer(md_content))
    titles = {}
    for i, m in enumerate(matches):
        tag, sid = m.group(1), m.group(2)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_content)
        block = md_content[start:end]
        for line in block.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('@'):
                continue
            if line.startswith('<'):
                continue
            if line.startswith('---'):
                continue
            if line.startswith('!['):
                continue
            if line.startswith(('\\[', '\\(')):
                continue
            if 'Voir l' in line and 'illustration' in line:
                continue
            line = re.sub(r'^#+\s*', '', line)
            line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
            line = re.sub(r'\*(.+?)\*', r'\1', line)
            line = re.sub(r'^>\s*', '', line)
            line = re.sub(r':\s*$', '', line)
            if len(line) > 5:
                titles[(tag, sid)] = line[:90]
                break
    return titles


def _is_clean_title(s):
    """True si le titre semble lisible pour YouTube (pas du LaTeX/separateur)."""
    if not s or len(s) < 10:
        return False
    if s.startswith(('---', '\\[', '\\(', '\\text', 'S_', 'B =', 'C^', '$')):
        return False
    if 'script narratif' in s.lower():
        return False
    if '---' in s:  # contient des separateurs markdown
        return False
    # trop de caracteres LaTeX = pas un titre lisible
    bad = sum(1 for c in s[:60] if c in '\\{}_^=')
    return bad <= 3


def make_chapter_title(scene, semantic_titles):
    """Construit un titre court pour un chapitre YouTube (max 80 chars)."""
    if scene["type"] == "intro":
        return "Presentation - L'Univers est au Carre"
    sid = scene.get("id", "")
    if scene["type"] == "calculation":
        # On essaie EXEMPLE_CALCUL puis MINI_SCRIPT, on garde le plus lisible
        candidates = [
            semantic_titles.get(("EXEMPLE_CALCUL", sid)),
            semantic_titles.get(("MINI_SCRIPT", sid)),
        ]
        sem = next((c for c in candidates if c and _is_clean_title(c)), None)
        # Si aucun candidat propre, on n'ajoute pas de sous-titre douteux
        # (on garde juste 'Exemple de calcul X.Y')
        prefix = f"Exemple de calcul {sid}"
    else:  # narration
        sem = semantic_titles.get(("NARRATION", sid))
        prefix = f"Section {sid}" if sid else "Section"

    # Si le contenu commence deja par 'CHAPITRE X', evite la redondance
    if sem and re.match(r'^CHAPITRE\s+\d', sem, re.IGNORECASE):
        return sem.strip().rstrip('.').rstrip(':')[:90]
    if sem and re.match(r'^INTRODUCTION', sem, re.IGNORECASE):
        return f"Introduction - {prefix}"[:90] if "Section" not in sem else "Introduction"

    if sem:
        sem = sem.strip().rstrip('.').rstrip(':')
        title = f"{prefix} - {sem}"
    else:
        title = prefix
    return title[:90]


def deduplicate_chapter_titles(chapters):
    """Marque les titres dupliques avec '(suite)', '(suite 2)', etc.

    Cas typique : une narration 13.0 decoupee en 2 sous-scenes a cause
    de plusieurs images = 2 chapitres avec le meme titre.
    """
    seen_count = {}
    for ch in chapters:
        base = ch["title"]
        n = seen_count.get(base, 0)
        if n > 0:
            ch["title"] = f"{base} (suite {n})" if n > 1 else f"{base} (suite)"
        seen_count[base] = n + 1
    return chapters


def fmt_timestamp(seconds):
    """Formate des secondes en MM:SS ou H:MM:SS pour YouTube.

    YouTube exige que le 1er chapitre soit '0:00'.
    """
    s = int(round(seconds))
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    if h > 0:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m}:{sec:02d}"


def main():
    print("=" * 60)
    print("GENERATION CHAPITRAGE YOUTUBE - L'Univers est au Carre")
    print("=" * 60)

    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        md = f.read()

    blocks = parse_tagged_script(md)
    scenes = build_scenes_from_blocks(blocks)
    semantic_titles = extract_section_titles(md)
    print(f"Scenes : {len(scenes)} | titres semantiques extraits : {len(semantic_titles)}")

    # Calcul des durees + timestamps
    chapters = []
    cumul = 0.0
    for sc in scenes:
        audio_path = find_audio(sc["num"], sc["text"]) if sc.get("text") else None
        duration = get_mp3_duration(audio_path) if audio_path else 6.0
        title = make_chapter_title(sc, semantic_titles)
        chapters.append({
            "num": sc["num"],
            "type": sc["type"],
            "id": sc.get("id"),
            "title": title,
            "start_seconds": round(cumul, 2),
            "duration": round(duration, 2),
            "timestamp": fmt_timestamp(cumul),
            "audio_file": os.path.basename(audio_path) if audio_path else None,
        })
        cumul += duration

    total_duration = cumul
    total_str = fmt_timestamp(total_duration)
    print(f"Duree totale : {total_str} ({total_duration:.0f}s)")
    print(f"Chapitres : {len(chapters)}")

    # YouTube exige le 1er chapitre a exactement 0:00
    chapters[0]["timestamp"] = "0:00"
    chapters[0]["start_seconds"] = 0

    # Post-traitement : fusionner les chapitres trop courts (<10s) avec le suivant
    # pour respecter l'exigence YouTube
    cleaned = []
    i = 0
    while i < len(chapters):
        ch = chapters[i]
        if ch["duration"] < 10 and i + 1 < len(chapters):
            # On fusionne le titre dans le suivant et on le saute
            print(f"  [merge] chapitre court ({ch['duration']:.1f}s) : {ch['title']}")
            i += 1
            continue
        cleaned.append(ch)
        i += 1
    chapters = cleaned

    # Dedupliquer les titres identiques (sous-scenes d'une meme narration)
    chapters = deduplicate_chapter_titles(chapters)

    # ----------------------------------------------------------------
    # SORTIES
    # ----------------------------------------------------------------
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Description YouTube complete
    desc_lines = [
        "L'Univers est au Carre - Theorie mathematique de Philippe Thomas Savard",
        "",
        "Une exploration audacieuse de la geometrie des nombres premiers,",
        "du postulat du squaring et de ses implications philosophiques.",
        "Une theorie originale qui propose de penser les mathematiques",
        "autrement : rigoureuses, visuelles, et profondement humaines.",
        "",
        f"Auteur : {AUTHOR}",
        f"Lieu   : {LOCATION}",
        f"Licence : {LICENSE}",
        "",
        f"Depot complet (code, preuves, illustrations, documentation) :",
        f"   {REPO_URL}",
        "",
        "Sous licence Apache 2.0 vous etes autorise a :",
        "  - consulter, cloner, modifier, partager, contribuer",
        "  - commenter et engager une discussion sur la theorie",
        "  - reutiliser les contenus dans le respect de la licence",
        "",
        "Je reste disponible pour repondre aux commentaires et critiques",
        "constructives. La theorie est offerte au public dans un esprit",
        "d'ouverture intellectuelle et de partage de la connaissance.",
        "",
        "═══════════════════════════════════════════════════════════",
        "CHAPITRES",
        "═══════════════════════════════════════════════════════════",
        "",
    ]
    for ch in chapters:
        desc_lines.append(f"{ch['timestamp']} {ch['title']}")
    desc_lines.extend([
        "",
        "═══════════════════════════════════════════════════════════",
        "MOTS-CLES",
        "═══════════════════════════════════════════════════════════",
        "#mathematiques #theoriedesnombres #nombrespremiers #geometrie",
        "#philippethomassavard #universaucarre #squaring #recherchemath",
        "#mathopensource #apache2 #rechercheindependante #autodidacte",
    ])
    with open(os.path.join(OUTPUT_DIR, "youtube_description.txt"), "w") as f:
        f.write("\n".join(desc_lines))

    # 2. Chapitres seuls (a coller dans une description existante)
    with open(os.path.join(OUTPUT_DIR, "youtube_chapters_only.txt"), "w") as f:
        for ch in chapters:
            f.write(f"{ch['timestamp']} {ch['title']}\n")

    # 3. Kit reseaux sociaux
    short_pitch = (
        "L'Univers est au Carre : une theorie mathematique originale sur "
        "la geometrie des nombres premiers et le postulat du squaring."
    )
    twitter = (
        f"{short_pitch}\n\n"
        f"Animation video complete (29 chapitres, narration FR) sur YouTube.\n"
        f"Code et preuves : {REPO_URL}\n\n"
        f"#mathematiques #nombrespremiers #recherchemath #opensource"
    )
    linkedin_lines = [
        f"Apres plusieurs annees de recherche autodidacte, je suis fier de partager",
        f"L'Univers est au Carre - une theorie mathematique originale qui explore",
        f"la geometrie des nombres premiers et propose le postulat du squaring.",
        "",
        f"L'animation video (~{int(total_duration//60)} minutes, {len(chapters)} chapitres) presente :",
        "  - Le questionnement initial et le postulat fondamental",
        "  - La geometrie du spectre des nombres premiers",
        "  - La mecanique harmonique du chaos discret",
        "  - Le postulat de l'univers est au carre",
        "  - L'espace de Philippot et l'axiomatisation finale",
        "",
        f"Sous licence Apache 2.0, le depot accueille les contributions, critiques",
        f"et discussions ouvertes :",
        f"   {REPO_URL}",
        "",
        f"#Mathematiques #TheorieDesNombres #RechercheIndependante #OpenSource",
    ]
    facebook = (
        f"{short_pitch}\n\n"
        f"L'animation video complete (~{int(total_duration//60)} min, narration "
        f"francaise) est decoupee en {len(chapters)} chapitres clairs pour "
        f"faciliter la decouverte progressive de la theorie.\n\n"
        f"Tout le travail (code, preuves Isabelle/HOL, illustrations, "
        f"documentation) est disponible en libre acces sur GitHub sous "
        f"licence Apache 2.0 - vous pouvez consulter, cloner, modifier, "
        f"partager, contribuer ou simplement engager la discussion.\n\n"
        f"Depot : {REPO_URL}\n\n"
        f"Auteur : {AUTHOR} ({LOCATION})"
    )
    tiktok_reels = (
        f"L'Univers est au Carre - extrait de la theorie mathematique\n"
        f"de {AUTHOR}\n\n"
        f"Animation complete (~{int(total_duration//60)} min) sur YouTube.\n\n"
        f"Lien complet en bio : depot GitHub libre (Apache 2.0)\n\n"
        f"#mathstok #mathematiques #nombrespremiers #recherche "
        f"#geometrie #autodidacte #opensource #fyp #pourtoi"
    )

    social_lines = [
        "═══════════════════════════════════════════════════════════",
        "KIT RESEAUX SOCIAUX - L'Univers est au Carre",
        "═══════════════════════════════════════════════════════════",
        "",
        "▶ TWITTER / X (limite 280 chars)",
        "─" * 60,
        twitter,
        "",
        "▶ LINKEDIN",
        "─" * 60,
        "\n".join(linkedin_lines),
        "",
        "▶ FACEBOOK",
        "─" * 60,
        facebook,
        "",
        "▶ TIKTOK / INSTAGRAM REELS / YOUTUBE SHORTS",
        "─" * 60,
        tiktok_reels,
        "",
        "═══════════════════════════════════════════════════════════",
        f"Duree totale animation : {total_str}",
        f"Nombre de chapitres   : {len(chapters)}",
        f"Auteur                : {AUTHOR}",
        f"Licence               : {LICENSE}",
        f"Depot                 : {REPO_URL}",
        "═══════════════════════════════════════════════════════════",
    ]
    with open(os.path.join(OUTPUT_DIR, "social_media_kit.txt"), "w") as f:
        f.write("\n".join(social_lines))

    # 4. JSON structure
    with open(os.path.join(OUTPUT_DIR, "chapters.json"), "w") as f:
        json.dump({
            "title": "L'Univers est au Carre",
            "author": AUTHOR,
            "license": LICENSE,
            "repo_url": REPO_URL,
            "total_duration_seconds": round(total_duration, 2),
            "total_duration_human": total_str,
            "chapters": chapters,
        }, f, ensure_ascii=False, indent=2)

    # ----------------------------------------------------------------
    # SUMMARY
    # ----------------------------------------------------------------
    print("\n--- APERCU CHAPITRAGE YOUTUBE ---")
    for ch in chapters[:10]:
        print(f"  {ch['timestamp']:>8s}  {ch['title']}")
    if len(chapters) > 10:
        print(f"  ... ({len(chapters) - 10} chapitres supplementaires)")
    print(f"\nFichiers generes dans {OUTPUT_DIR} :")
    for fn in ("youtube_description.txt", "youtube_chapters_only.txt",
               "social_media_kit.txt", "chapters.json"):
        p = os.path.join(OUTPUT_DIR, fn)
        if os.path.exists(p):
            print(f"  - {fn} ({os.path.getsize(p)} bytes)")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
