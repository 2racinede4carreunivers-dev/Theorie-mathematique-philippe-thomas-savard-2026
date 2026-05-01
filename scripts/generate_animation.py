#!/usr/bin/env python3
"""
generate_animation.py v3
========================
Genere une animation narrative complete de la theorie
"L'Univers est au Carre".

Produit un HTML autonome avec :
- Lecteur video-like (play/pause/skip)
- Images plein ecran qui defilent chronologiquement
- Narration audio TTS (voix feminine francaise)
- Pas de texte visible : uniquement images + voix
- Mini-scripts narratifs pour les calculs et tableaux
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
OUTPUT_DIR = os.path.join(REPO_ROOT, "animation_output")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
LLM_KEY = os.environ.get("EMERGENT_LLM_KEY", "")
ENABLE_TTS = os.environ.get("ENABLE_TTS", "false").lower() == "true"
ENABLE_PDF = os.environ.get("ENABLE_PDF", "true").lower() == "true"

# ================================================================
# IMAGE MAPPING: associate images to chapters chronologically
# ================================================================

IMAGE_MAP = {
    "intro": ["animation_A-2.png"],
    "ch1_suites": ["animation_A-3.png", "animation-A-4.png", "Animation_A-5.png", "animation_A-6.png"],
    "ch1_tableaux": [
        "animation_T-1.png", "animation_T-2.png", "animation_T-3.png",
        "animation-T-4.png", "aniamtion-T-5.png", "animation_T-6.png",
        "animation_T-7.png", "animation_T8.png", "animation_T-9.png",
        "animation_T-10.png", "animation_T-11.png", "animation_T-12.png",
        "animation_T-13.png", "animation_T-14.png", "animation_T-15.png",
        "animation_T-16.png", "animation_T17.png", "animation_T-18.png",
    ],
    "ch1_ecarts": ["analyse_geo_corde.png", "quadrature_parabole_zero_critique.png"],
    "ch2_mecanique": [
        "animation_B-1.png", "animation_B-2.png", "animation_B-3.png",
        "animation_B-4.png", "animation_B-5.png", "animation_B-6.png",
        "animation_B-7.png", "animation_B-8.png", "animation_B9.png",
        "animation_B-10.png", "animation_B-11.png", "animation_B-12.png",
        "animation_B-13.png", "animation_B-14.png", "animation_B-15.png",
        "animation_B-16.png", "animation_B-17.png",
    ],
    "ch3_postulat": [
        "animation_C-1.png", "animation`_C-2.png", "animation_C-3.png",
        "animation_C--4.png", "animation_C-5.png", "animation_C-6.png",
        "animation_C-7.png", "animation_C-8.png", "animation_C-9.png",
        "animation_C-10.png", "animation_C-11.png", "animation_C-12.png",
        "animation_C-13.png", "animation_C14.png", "animation_C-15.png",
        "animation_C-16.png", "animation_C-17.png", "animation-C-19.png",
        "animation_C-20.png",
    ],
    "ch4_espace": ["animation_D-1.png", "animation_D-2.png"],
    "ch5_philo": [
        "animation_E-1.png", "animation_E-2.png",
        "animation_E-3.png", "animation_E-4.png",
    ],
    "annexes": [
        "animation_F-1.png", "animation_G-1.png",
        "animation_H-1.png", "animation_H-2.png", "animation_H-3.png",
    ],
}


def embed_image(filename):
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"


def get_all_images_ordered():
    """Return flat list of all images in chronological order."""
    order = ["intro", "ch1_suites", "ch1_tableaux", "ch1_ecarts",
             "ch2_mecanique", "ch3_postulat", "ch4_espace", "ch5_philo", "annexes"]
    images = []
    for key in order:
        for fname in IMAGE_MAP.get(key, []):
            b64 = embed_image(fname)
            if b64:
                images.append({"filename": fname, "data": b64, "section": key})
    return images


# ================================================================
# SCENE PARSER - extract narrative + calculations
# ================================================================

def parse_narrative(md_content):
    """Parse markdown into narrative scenes with calculations identified."""
    scenes = []
    lines = md_content.split("\n")
    current_title = "Introduction"
    current_narration = []
    current_calculations = []
    in_calc = False
    calc_block = []

    for line in lines:
        stripped = line.strip()

        # Skip decoration lines
        if stripped.startswith("===") or stripped.startswith("---"):
            continue

        # Chapter headers
        if re.match(r'^(CHAPITRE \d|INTRODUCTION|FIN DU SCRIPT)', stripped):
            if current_narration or current_calculations:
                scenes.append({
                    "title": current_title,
                    "narration": "\n".join(current_narration).strip(),
                    "calculations": current_calculations[:],
                })
            current_title = stripped
            current_narration = []
            current_calculations = []
            continue

        if re.match(r'^#{1,3}\s+', stripped):
            header = re.sub(r'^#+\s*', '', stripped)
            if current_narration:
                scenes.append({
                    "title": current_title,
                    "narration": "\n".join(current_narration).strip(),
                    "calculations": current_calculations[:],
                })
                current_narration = []
                current_calculations = []
            current_title = header
            continue

        # Skip images and HTML
        if stripped.startswith("<img") or stripped.startswith("</"):
            continue

        # Detect calculation blocks (indented lines with math operators)
        is_calc_line = (line.startswith("    ") or line.startswith("\t")) and re.search(r'[=+\-*/^]', stripped)
        is_table_line = stripped.startswith("|") and "|" in stripped[1:]

        if is_calc_line or is_table_line:
            if not in_calc:
                in_calc = True
                calc_block = []
            calc_block.append(stripped)
        else:
            if in_calc and calc_block:
                current_calculations.append("\n".join(calc_block))
                calc_block = []
                in_calc = False
            if stripped:
                # Clean markdown
                clean = re.sub(r'\*\*(.+?)\*\*', r'\1', stripped)
                clean = re.sub(r'\*(.+?)\*', r'\1', clean)
                clean = re.sub(r'`(.+?)`', r'\1', clean)
                clean = re.sub(r'^>\s*', '', clean)
                current_narration.append(clean)

    if current_narration:
        scenes.append({
            "title": current_title,
            "narration": "\n".join(current_narration).strip(),
            "calculations": current_calculations[:],
        })

    return scenes


# ================================================================
# GENERATE ENRICHED NARRATION FOR TTS
# ================================================================

def generate_calc_narration(calc_text, context_title):
    """Generate spoken explanation for a calculation block."""
    lines = calc_text.strip().split("\n")

    # Table?
    if lines[0].startswith("|"):
        cells_header = [c.strip() for c in lines[0].split("|") if c.strip()]
        data_lines = [l for l in lines[1:] if l.strip() and not re.match(r'^\|[-:]+', l)]
        narration = f"Un tableau est presente avec les colonnes : {', '.join(cells_header)}. "
        for dl in data_lines[:3]:
            cells = [c.strip() for c in dl.split("|") if c.strip()]
            if cells:
                narration += f"On y lit : {', '.join(cells)}. "
        return narration

    # Calculation
    narration = "Observons maintenant le calcul suivant. "
    for line in lines:
        spoken = line.strip()
        if "=" in spoken:
            parts = spoken.split("=", 1)
            left = parts[0].strip()
            right = parts[1].strip() if len(parts) > 1 else ""
            # Convert math symbols to speech
            for old, new in [("sqrt", "racine carree de "), ("^", " exposant "),
                             ("*", " fois "), ("/", " divise par "),
                             ("+", " plus "), ("- ", " moins ")]:
                left = left.replace(old, new)
                right = right.replace(old, new)
            narration += f"{left} est egal a {right}. "
        elif spoken:
            for old, new in [("sqrt", "racine carree de "), ("^", " exposant "),
                             ("*", " fois "), ("/", " divise par ")]:
                spoken = spoken.replace(old, new)
            narration += f"{spoken}. "

    return narration


def build_tts_scenes(scenes, images):
    """Build final TTS scenes: narration + calc explanations, matched with images."""
    tts_scenes = []
    img_idx = 0
    total_images = len(images)

    for scene in scenes:
        narration = scene["narration"]
        if not narration.strip():
            continue

        # Split narration into chunks (~3500 chars max for TTS)
        paragraphs = narration.split("\n\n") if "\n\n" in narration else narration.split("\n")
        chunk = ""
        for para in paragraphs:
            if len(chunk) + len(para) > 3000 and chunk:
                # Assign images proportionally
                scene_images = []
                if img_idx < total_images:
                    scene_images.append(images[img_idx])
                    img_idx += 1

                tts_scenes.append({
                    "title": scene["title"],
                    "text": chunk.strip(),
                    "images": scene_images,
                    "type": "narration",
                })
                chunk = ""
            chunk += para + "\n\n"

        if chunk.strip():
            scene_images = []
            if img_idx < total_images:
                scene_images.append(images[img_idx])
                img_idx += 1
            tts_scenes.append({
                "title": scene["title"],
                "text": chunk.strip(),
                "images": scene_images,
                "type": "narration",
            })

        # Add calculation explanations as separate scenes
        for calc in scene.get("calculations", []):
            calc_narration = generate_calc_narration(calc, scene["title"])
            if calc_narration and len(calc_narration) > 20:
                scene_images = []
                if img_idx < total_images:
                    scene_images.append(images[img_idx])
                    img_idx += 1
                tts_scenes.append({
                    "title": scene["title"] + " - Calcul",
                    "text": calc_narration,
                    "images": scene_images,
                    "type": "calculation",
                })

    # Number them
    for i, s in enumerate(tts_scenes):
        s["num"] = i + 1

    return tts_scenes


# ================================================================
# TTS GENERATION
# ================================================================

async def generate_tts(tts_scenes):
    if not LLM_KEY:
        print("  Pas de cle LLM.")
        return {}
    try:
        from emergentintegrations.llm.openai import OpenAITextToSpeech
    except ImportError:
        print("  emergentintegrations non installe.")
        return {}

    tts = OpenAITextToSpeech(api_key=LLM_KEY)
    audio_map = {}
    os.makedirs(AUDIO_DIR, exist_ok=True)

    for scene in tts_scenes:
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
            print(f"  Scene {num}/{len(tts_scenes)}: TTS ({scene['type']})...")
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
            print(f"  Scene {num}: erreur - {str(e)[:60]}")
            import time
            time.sleep(3)

    return audio_map


# ================================================================
# HTML GENERATION - VIDEO PLAYER STYLE
# ================================================================

def generate_html(tts_scenes, audio_map):
    total = len(tts_scenes)

    scenes_data = []
    for scene in tts_scenes:
        num = scene["num"]
        img_data = scene["images"][0]["data"] if scene.get("images") else None
        audio_data = audio_map.get(num)
        scenes_data.append({
            "num": num,
            "title": scene["title"],
            "image": img_data,
            "audio": audio_data,
        })

    scenes_json = json.dumps(scenes_data, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>L'Univers est au Carre - Animation</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: #000;
  color: #fff;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}}
.player {{
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
  overflow: hidden;
}}
.player img {{
  max-width: 95%;
  max-height: 90vh;
  object-fit: contain;
  transition: opacity 0.8s ease;
}}
.player .no-image {{
  color: #555;
  font-size: 1.2rem;
  text-align: center;
}}
.title-overlay {{
  position: absolute;
  top: 20px;
  left: 30px;
  background: rgba(0,0,0,0.7);
  padding: 8px 18px;
  border-radius: 6px;
  font-size: 0.95rem;
  color: #c9a84c;
  letter-spacing: 1px;
  pointer-events: none;
  transition: opacity 0.5s;
}}
.controls {{
  background: #111;
  border-top: 1px solid #333;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.controls button {{
  background: none;
  border: 1px solid #555;
  color: #fff;
  padding: 8px 16px;
  font-size: 1.1rem;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
  min-width: 44px;
}}
.controls button:hover {{
  background: #c9a84c;
  color: #000;
  border-color: #c9a84c;
}}
.controls button.active {{
  background: #c9a84c;
  color: #000;
  border-color: #c9a84c;
}}
.progress-bar {{
  flex: 1;
  height: 6px;
  background: #333;
  border-radius: 3px;
  cursor: pointer;
  position: relative;
}}
.progress-fill {{
  height: 100%;
  background: #c9a84c;
  border-radius: 3px;
  transition: width 0.3s;
}}
.time-display {{
  color: #888;
  font-size: 0.85rem;
  min-width: 80px;
  text-align: center;
}}
</style>
</head>
<body>
<div class="player" id="player">
  <div class="title-overlay" id="title-overlay"></div>
  <img id="scene-image" src="" alt="">
  <div class="no-image" id="no-image" style="display:none;">Chargement...</div>
</div>
<div class="controls">
  <button id="btn-prev" title="Section precedente">&#9664;&#9664;</button>
  <button id="btn-play" title="Lecture / Pause">&#9654;</button>
  <button id="btn-next" title="Section suivante">&#9654;&#9654;</button>
  <div class="progress-bar" id="progress-bar">
    <div class="progress-fill" id="progress-fill"></div>
  </div>
  <span class="time-display" id="time-display">1 / {total}</span>
</div>
<script>
const scenes = {scenes_json};
const total = scenes.length;
let current = 0;
let playing = false;
let audio = null;

const img = document.getElementById('scene-image');
const noImg = document.getElementById('no-image');
const titleOv = document.getElementById('title-overlay');
const btnPlay = document.getElementById('btn-play');
const btnPrev = document.getElementById('btn-prev');
const btnNext = document.getElementById('btn-next');
const progressFill = document.getElementById('progress-fill');
const timeDisplay = document.getElementById('time-display');
const progressBar = document.getElementById('progress-bar');

function showScene(idx) {{
  if (idx < 0 || idx >= total) return;
  current = idx;
  const scene = scenes[current];

  // Image
  if (scene.image) {{
    img.src = scene.image;
    img.style.display = 'block';
    noImg.style.display = 'none';
  }} else {{
    img.style.display = 'none';
    noImg.style.display = 'block';
    noImg.textContent = scene.title;
  }}

  // Title
  titleOv.textContent = scene.title;
  titleOv.style.opacity = 1;
  setTimeout(() => {{ titleOv.style.opacity = 0; }}, 3000);

  // Progress
  progressFill.style.width = ((current + 1) / total * 100) + '%';
  timeDisplay.textContent = (current + 1) + ' / ' + total;
}}

function playAudio() {{
  if (audio) {{ audio.pause(); audio = null; }}
  const scene = scenes[current];
  if (scene.audio) {{
    audio = new Audio('data:audio/mp3;base64,' + scene.audio);
    audio.play();
    audio.onended = function() {{
      if (playing && current < total - 1) {{
        current++;
        showScene(current);
        setTimeout(playAudio, 500);
      }} else {{
        playing = false;
        btnPlay.innerHTML = '&#9654;';
        btnPlay.classList.remove('active');
      }}
    }};
  }} else {{
    // No audio: show image for 5 seconds then advance
    if (playing && current < total - 1) {{
      setTimeout(() => {{
        if (playing) {{
          current++;
          showScene(current);
          playAudio();
        }}
      }}, 5000);
    }}
  }}
}}

function togglePlay() {{
  playing = !playing;
  if (playing) {{
    btnPlay.innerHTML = '&#9646;&#9646;';
    btnPlay.classList.add('active');
    showScene(current);
    playAudio();
  }} else {{
    btnPlay.innerHTML = '&#9654;';
    btnPlay.classList.remove('active');
    if (audio) audio.pause();
  }}
}}

btnPlay.addEventListener('click', togglePlay);
btnPrev.addEventListener('click', () => {{
  if (audio) {{ audio.pause(); audio = null; }}
  if (current > 0) {{ current--; showScene(current); if (playing) playAudio(); }}
}});
btnNext.addEventListener('click', () => {{
  if (audio) {{ audio.pause(); audio = null; }}
  if (current < total - 1) {{ current++; showScene(current); if (playing) playAudio(); }}
}});

progressBar.addEventListener('click', (e) => {{
  const rect = progressBar.getBoundingClientRect();
  const pct = (e.clientX - rect.left) / rect.width;
  const idx = Math.floor(pct * total);
  if (audio) {{ audio.pause(); audio = null; }}
  showScene(idx);
  if (playing) playAudio();
}});

document.addEventListener('keydown', (e) => {{
  if (e.key === ' ') {{ e.preventDefault(); togglePlay(); }}
  if (e.key === 'ArrowRight') {{ btnNext.click(); }}
  if (e.key === 'ArrowLeft') {{ btnPrev.click(); }}
}});

showScene(0);
</script>
</body>
</html>'''
    return html


# ================================================================
# PDF GENERATION
# ================================================================

def generate_pdf(tts_scenes, pdf_path):
    try:
        from weasyprint import HTML
        print("  Generation PDF...")

        pages_html = ""
        total = len(tts_scenes)
        for scene in tts_scenes:
            num = scene["num"]
            img_html = ""
            if scene.get("images"):
                img_data = scene["images"][0]["data"]
                img_html = f'<div class="img-box"><img src="{img_data}"></div>'

            text = scene["text"]
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text_html = "".join(f"<p>{p.strip()}</p>" for p in text.split("\n") if p.strip())

            pages_html += f'''
<div class="page">
  <div class="hdr">
    <span>Page {num} / {total}</span>
    <h2>{scene["title"]}</h2>
  </div>
  {img_html}
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
    print("ANIMATION v3 - L'Univers est au Carre")
    print("=" * 60)

    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        md = f.read()
    print(f"Script : {len(md)} chars, {md.count(chr(10))} lignes")

    # Parse
    scenes = parse_narrative(md)
    print(f"Scenes narratives : {len(scenes)}")
    print(f"Calculs detectes : {sum(len(s['calculations']) for s in scenes)}")

    # Images
    images = get_all_images_ordered()
    print(f"Images chargees : {len(images)}")

    # Build TTS scenes
    tts_scenes = build_tts_scenes(scenes, images)
    print(f"Scenes TTS : {len(tts_scenes)}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # TTS
    audio_map = {}
    if ENABLE_TTS:
        print("\n--- TTS (shimmer, FR) ---")
        audio_map = await generate_tts(tts_scenes)
        print(f"Audio : {len(audio_map)} fichiers")

    # HTML
    print("\n--- HTML ---")
    html = generate_html(tts_scenes, audio_map)
    html_path = os.path.join(OUTPUT_DIR, "animation.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML : {html_path}")

    # PDF
    if ENABLE_PDF:
        print("\n--- PDF ---")
        generate_pdf(tts_scenes, os.path.join(OUTPUT_DIR, "animation.pdf"))

    # Index
    index = [{"num": s["num"], "title": s["title"], "type": s["type"],
              "has_audio": s["num"] in audio_map, "has_image": bool(s.get("images"))}
             for s in tts_scenes]
    with open(os.path.join(OUTPUT_DIR, "scenes_index.json"), "w") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"ANIMATION : {len(tts_scenes)} scenes, {len(images)} images, {len(audio_map)} audio")
    print(f"{'=' * 60}")
    return 0


def main():
    return asyncio.run(async_main())

if __name__ == "__main__":
    sys.exit(main())
