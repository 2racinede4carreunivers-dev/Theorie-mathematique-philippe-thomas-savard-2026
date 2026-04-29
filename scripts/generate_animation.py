#!/usr/bin/env python3
"""
generate_animation.py
=====================
Genere une presentation animee a partir du SCRIPT_NARRATIF_VP.md.

Produit :
  - animation.html  : Presentation HTML interactive avec navigation
  - animation.pdf   : Version PDF paginee
  - audio/           : Fichiers MP3 par scene (TTS voix feminine francaise)

Usage :
  python scripts/generate_animation.py [--tts] [--pdf]
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
# LATEX TO SPEECH CONVERSION
# ================================================================

def latex_to_speech(formula):
    """Convert LaTeX formula to spoken French text."""
    f = formula.strip()
    # Remove \[ \] wrappers
    f = re.sub(r'^\\\[|\\\]$', '', f).strip()
    # Remove \text{...} -> just the content
    f = re.sub(r'\\text\{([^}]+)\}', r'\1', f)
    # \frac{a}{b} -> a divise par b
    f = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1 divise par \2', f)
    # \left( \right) -> parentheses
    f = re.sub(r'\\left[(\[]', '(', f)
    f = re.sub(r'\\right[)\]]', ')', f)
    # \times -> fois
    f = f.replace('\\times', ' fois ')
    # ^{n} or ^n -> exposant n
    f = re.sub(r'\^\{([^}]+)\}', r' exposant \1', f)
    f = re.sub(r'\^(\d+)', r' exposant \1', f)
    # \sqrt -> racine carree de
    f = re.sub(r'\\sqrt\{([^}]+)\}', r'racine carree de \1', f)
    # Cleanup
    f = re.sub(r'\s+', ' ', f).strip()
    return f


def enrich_text_for_tts(scene):
    """Enrich scene text with spoken explanations of formulas, tables and images."""
    parts = []

    # Title
    parts.append(f"Page {scene['num']}. {scene['title']}.")
    parts.append("")

    # Main text - process line by line
    text = scene["text"]
    # Clean markdown
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'#{1,3}\s*', '', text)

    lines = text.split("\n")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Detect computation lines (indented, with = or + or -)
        is_calc = (line.startswith("    ") or line.startswith("\t")) and re.search(r'[=+\-*/^]', stripped)
        if is_calc:
            # Convert formula to speech
            spoken = stripped
            # Replace math symbols
            spoken = spoken.replace("^", " exposant ")
            spoken = spoken.replace("*", " fois ")
            spoken = spoken.replace("/", " divise par ")
            spoken = spoken.replace("sqrt", "racine carree de ")
            spoken = re.sub(r'\s+', ' ', spoken)
            parts.append(f"Le calcul suivant est affiche : {spoken}.")
        elif stripped.startswith("\\[") or stripped.startswith("$"):
            spoken = latex_to_speech(stripped)
            if spoken and len(spoken) > 5:
                parts.append(f"La formule indique : {spoken}.")
        else:
            parts.append(stripped)

    # Tables - narrate content
    if scene.get("tables"):
        parts.append("")
        parts.append("Un tableau recapitulatif est presente a l'ecran. Voici son contenu.")
        for table in scene["tables"]:
            rows = [r for r in table.split("\n") if r.strip() and not re.match(r'^\|[-:]+', r)]
            if len(rows) >= 1:
                header_cells = [c.strip() for c in rows[0].split("|") if c.strip()]
                if header_cells:
                    parts.append(f"Les colonnes sont : {', '.join(header_cells)}.")
                for row in rows[1:5]:
                    cells = [c.strip() for c in row.split("|") if c.strip()]
                    if cells:
                        parts.append(f"Ligne de donnees : {', '.join(cells)}.")

    # Images - describe
    if scene.get("images"):
        parts.append("")
        for img in scene["images"]:
            fname = os.path.basename(img).replace(".png", "").replace("_", " ").replace("-", " ")
            parts.append(f"Une illustration est presentee a l'ecran : {fname}.")
            parts.append("Prenez un instant pour observer cette figure qui illustre le propos.")

    full_text = "\n".join(parts)
    if len(full_text) > 3900:
        full_text = full_text[:3900]
    return full_text


# ================================================================
# SCENE PARSER
# ================================================================

def parse_scenes(md_content):
    """Parse le markdown en scenes structurees."""
    scenes = []
    current_scene = None

    # Split by major section delimiters
    lines = md_content.split("\n")
    scene_num = 0
    current_title = "Page de titre"
    current_text = []
    current_images = []
    current_formulas = []
    current_tables = []

    in_table = False
    table_lines = []

    for line in lines:
        stripped = line.strip()

        # Detect chapter/section headers
        is_header = False
        header_title = ""

        if stripped.startswith("----") and len(stripped) > 10:
            # Separator line before chapter title
            continue

        if re.match(r'^(CHAPITRE \d|INTRODUCTION|FIN DU SCRIPT)', stripped):
            is_header = True
            header_title = stripped

        if re.match(r'^#{1,3}\s+', stripped):
            is_header = True
            header_title = re.sub(r'^#+\s*', '', stripped)

        if stripped.startswith("===") and len(stripped) > 10:
            continue

        # Detect images
        img_match = re.search(r'<img\s+src="([^"]+)"', line)
        if img_match:
            img_path = img_match.group(1)
            # Normalize path
            if img_path.startswith("./"):
                img_path = img_path[2:]
            current_images.append(img_path)
            continue

        # Detect LaTeX formulas
        if stripped.startswith("\\[") or stripped.startswith("$"):
            current_formulas.append(stripped)
            current_text.append(line)  # Keep in text too for HTML display
            continue
        if stripped.startswith("\\]"):
            current_text.append(line)
            continue

        # Detect tables
        if "|" in stripped and stripped.startswith("|"):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(stripped)
            continue
        elif in_table:
            in_table = False
            current_tables.append("\n".join(table_lines))
            table_lines = []

        # New scene on major header
        if is_header and header_title:
            # Save previous scene
            if current_text or current_images:
                scene_num += 1
                text_content = "\n".join(current_text).strip()
                if text_content or current_images:
                    scenes.append({
                        "num": scene_num,
                        "title": current_title,
                        "text": text_content,
                        "images": current_images[:],
                        "formulas": current_formulas[:],
                        "tables": current_tables[:],
                    })

            current_title = header_title
            current_text = []
            current_images = []
            current_formulas = []
            current_tables = []
            continue

        # Regular text
        if stripped:
            current_text.append(line)

    # Last scene
    if current_text or current_images:
        scene_num += 1
        scenes.append({
            "num": scene_num,
            "title": current_title,
            "text": "\n".join(current_text).strip(),
            "images": current_images[:],
            "formulas": current_formulas[:],
            "tables": current_tables[:],
        })

    # Split long scenes into sub-scenes (max ~800 chars per slide for readability)
    final_scenes = []
    global_num = 0
    for scene in scenes:
        text = scene["text"]
        if len(text) > 1200 and not scene["tables"]:
            # Split by paragraphs
            paragraphs = text.split("\n\n")
            chunk = ""
            img_idx = 0
            for para in paragraphs:
                if len(chunk) + len(para) > 1000 and chunk:
                    global_num += 1
                    imgs = []
                    if img_idx < len(scene["images"]):
                        imgs = [scene["images"][img_idx]]
                        img_idx += 1
                    final_scenes.append({
                        "num": global_num,
                        "title": scene["title"],
                        "text": chunk.strip(),
                        "images": imgs,
                        "formulas": [],
                        "tables": [],
                    })
                    chunk = ""
                chunk += para + "\n\n"
            if chunk.strip():
                global_num += 1
                remaining_imgs = scene["images"][img_idx:]
                final_scenes.append({
                    "num": global_num,
                    "title": scene["title"],
                    "text": chunk.strip(),
                    "images": remaining_imgs,
                    "formulas": scene["formulas"],
                    "tables": scene["tables"],
                })
        else:
            global_num += 1
            scene["num"] = global_num
            final_scenes.append(scene)

    return final_scenes


# ================================================================
# IMAGE EMBEDDING
# ================================================================

def embed_image_base64(img_path):
    """Convert image to base64 for HTML embedding."""
    full_path = os.path.join(REPO_ROOT, img_path)
    if not os.path.exists(full_path):
        # Try assets/animation/ directly
        fname = os.path.basename(img_path)
        full_path = os.path.join(ASSETS_DIR, fname)
    if not os.path.exists(full_path):
        return None
    with open(full_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{data}"


# ================================================================
# HTML GENERATION
# ================================================================

def generate_html(scenes, audio_files=None):
    """Generate interactive HTML presentation."""
    total = len(scenes)

    slides_html = ""
    for scene in scenes:
        num = scene["num"]
        title = scene["title"]
        text = scene["text"]

        # Clean text for HTML
        text_html = ""
        in_latex = False
        latex_block = []
        for para in text.split("\n"):
            para_s = para.strip()
            if not para_s:
                if not in_latex:
                    text_html += "\n"
                continue
            # LaTeX block detection
            if para_s.startswith("\\["):
                in_latex = True
                latex_block = [para_s]
                continue
            if para_s.startswith("\\]"):
                in_latex = False
                latex_content = "\n".join(latex_block)
                text_html += f'<div class="formula">\\[{latex_content}\\]</div>\n'
                latex_block = []
                continue
            if in_latex:
                latex_block.append(para_s)
                continue
            # Handle blockquotes
            if para_s.startswith(">"):
                para_s = para_s.lstrip("> ")
                text_html += f'<blockquote>{para_s}</blockquote>\n'
            elif para_s.startswith("- ") or para_s.startswith("* "):
                item_text = re.sub(r'^[-*]\s*', '', para_s)
                text_html += f"<li>{item_text}</li>\n"
            else:
                # Bold
                para_s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para_s)
                # Italic
                para_s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', para_s)
                # Code
                para_s = re.sub(r'`(.+?)`', r'<code>\1</code>', para_s)
                text_html += f"<p>{para_s}</p>\n"
                text_html += f"<p>{para}</p>\n"

        # Tables
        tables_html = ""
        for table in scene.get("tables", []):
            rows = table.strip().split("\n")
            tables_html += '<table class="scene-table">\n'
            for i, row in enumerate(rows):
                cells = [c.strip() for c in row.split("|") if c.strip()]
                if not cells:
                    continue
                if all(re.match(r'^[-:]+$', c) for c in cells):
                    continue
                tag = "th" if i == 0 else "td"
                tables_html += "  <tr>"
                for cell in cells:
                    tables_html += f"<{tag}>{cell}</{tag}>"
                tables_html += "</tr>\n"
            tables_html += "</table>\n"

        # Images
        images_html = ""
        for img in scene.get("images", []):
            b64 = embed_image_base64(img)
            if b64:
                images_html += f'<div class="scene-image"><img src="{b64}" alt="{os.path.basename(img)}"></div>\n'

        # Audio
        audio_html = ""
        if audio_files and num in audio_files:
            audio_b64 = audio_files[num]
            audio_html = f'<audio class="scene-audio" data-scene="{num}" src="data:audio/mp3;base64,{audio_b64}"></audio>'

        # Formulas
        formulas_html = ""
        for formula in scene.get("formulas", []):
            formulas_html += f'<div class="formula">{formula}</div>\n'

        slides_html += f'''
<div class="slide" id="slide-{num}" data-num="{num}" style="display:none;">
  <div class="slide-header">
    <span class="slide-number">Page {num} / {total}</span>
    <h2 class="slide-title">{title}</h2>
  </div>
  <div class="slide-body">
    <div class="slide-content">
      {text_html}
      {formulas_html}
      {tables_html}
    </div>
    {images_html}
  </div>
  {audio_html}
</div>
'''

    html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>L'Univers est au Carre - Animation narrative</title>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: 'Georgia', 'Times New Roman', serif;
  background: #0a0a0f;
  color: #e8e8e8;
  min-height: 100vh;
}}
.presentation {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}}
.slide {{
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  padding: 40px;
  animation: fadeIn 0.6s ease-in;
}}
@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(20px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.slide-header {{
  border-bottom: 2px solid #c9a84c;
  padding-bottom: 15px;
  margin-bottom: 30px;
}}
.slide-number {{
  font-size: 0.85rem;
  color: #c9a84c;
  letter-spacing: 2px;
  text-transform: uppercase;
}}
.slide-title {{
  font-size: 1.8rem;
  color: #ffffff;
  margin-top: 8px;
  font-weight: normal;
  letter-spacing: 1px;
}}
.slide-body {{
  flex: 1;
  display: flex;
  gap: 30px;
}}
.slide-content {{
  flex: 1;
  font-size: 1.05rem;
  line-height: 1.75;
}}
.slide-content p {{
  margin-bottom: 12px;
  text-align: justify;
}}
.slide-content blockquote {{
  border-left: 3px solid #c9a84c;
  padding: 10px 20px;
  margin: 15px 0;
  font-style: italic;
  color: #d4c9a8;
  background: rgba(201,168,76,0.05);
}}
.slide-content strong {{ color: #ffffff; }}
.slide-content code {{
  background: rgba(201,168,76,0.15);
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.95em;
}}
.scene-image {{
  max-width: 450px;
  flex-shrink: 0;
}}
.scene-image img {{
  width: 100%;
  border-radius: 8px;
  border: 1px solid #333;
}}
.scene-table {{
  width: 100%;
  border-collapse: collapse;
  margin: 15px 0;
  font-size: 0.9rem;
}}
.scene-table th, .scene-table td {{
  border: 1px solid #444;
  padding: 8px 12px;
  text-align: left;
}}
.scene-table th {{
  background: rgba(201,168,76,0.15);
  color: #c9a84c;
}}
.formula {{
  background: rgba(255,255,255,0.05);
  padding: 10px 20px;
  margin: 10px 0;
  border-radius: 5px;
  font-family: 'Courier New', monospace;
  overflow-x: auto;
}}
.nav {{
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(10,10,15,0.95);
  border-top: 1px solid #333;
  padding: 12px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 100;
}}
.nav button {{
  background: #c9a84c;
  color: #0a0a0f;
  border: none;
  padding: 10px 25px;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold;
  transition: background 0.2s;
}}
.nav button:hover {{ background: #e0c060; }}
.nav button:disabled {{ opacity: 0.3; cursor: default; }}
.nav .progress {{
  color: #888;
  font-size: 0.9rem;
}}
.audio-btn {{
  background: none;
  border: 1px solid #c9a84c;
  color: #c9a84c;
  padding: 8px 15px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 0.85rem;
}}
.audio-btn:hover {{ background: rgba(201,168,76,0.1); }}
ul {{ margin: 10px 0 10px 25px; }}
li {{ margin-bottom: 5px; }}
</style>
</head>
<body>
<div class="presentation">
{slides_html}
</div>
<div class="nav">
  <button id="prev" onclick="navigate(-1)">Precedent</button>
  <span class="progress" id="progress">Page 1 / {total}</span>
  <button class="audio-btn" id="audio-btn" onclick="toggleAudio()">Ecouter</button>
  <button class="audio-btn" id="autoplay-btn" onclick="toggleAutoPlay()">Lecture auto</button>
  <button id="next" onclick="navigate(1)">Suivant</button>
</div>
<script>
let current = 1;
const total = {total};
let currentAudio = null;

let autoPlay = false;

function showSlide(n) {{
  document.querySelectorAll('.slide').forEach(s => s.style.display = 'none');
  const slide = document.getElementById('slide-' + n);
  if (slide) {{
    slide.style.display = 'flex';
    slide.style.animation = 'none';
    slide.offsetHeight;
    slide.style.animation = 'fadeIn 0.6s ease-in';
    // Re-render MathJax for this slide
    if (window.MathJax) MathJax.typeset([slide]);
  }}
  document.getElementById('progress').textContent = 'Page ' + n + ' / ' + total;
  document.getElementById('prev').disabled = (n <= 1);
  document.getElementById('next').disabled = (n >= total);
  if (currentAudio) {{ currentAudio.pause(); currentAudio = null; }}
  // Auto-play audio if enabled
  if (autoPlay && slide) {{
    const audio = slide.querySelector('.scene-audio');
    if (audio) {{
      currentAudio = audio;
      audio.play();
      audio.onended = function() {{ navigate(1); }};
    }}
  }}
}}

function navigate(dir) {{
  current += dir;
  if (current < 1) current = 1;
  if (current > total) current = total;
  showSlide(current);
}}

function toggleAudio() {{
  if (currentAudio && !currentAudio.paused) {{
    currentAudio.pause();
    return;
  }}
  const slide = document.getElementById('slide-' + current);
  const audio = slide ? slide.querySelector('.scene-audio') : null;
  if (audio) {{
    currentAudio = audio;
    audio.play();
  }}
}}

function toggleAutoPlay() {{
  autoPlay = !autoPlay;
  const btn = document.getElementById('autoplay-btn');
  btn.textContent = autoPlay ? 'Arreter auto' : 'Lecture auto';
  btn.style.background = autoPlay ? 'rgba(201,168,76,0.3)' : 'none';
  if (autoPlay) {{
    const slide = document.getElementById('slide-' + current);
    const audio = slide ? slide.querySelector('.scene-audio') : null;
    if (audio) {{
      currentAudio = audio;
      audio.play();
      audio.onended = function() {{ navigate(1); }};
    }}
  }}
}}

document.addEventListener('keydown', function(e) {{
  if (e.key === 'ArrowRight' || e.key === ' ') navigate(1);
  if (e.key === 'ArrowLeft') navigate(-1);
}});

showSlide(1);
</script>
</body>
</html>'''
    return html


# ================================================================
# PDF GENERATION
# ================================================================

def generate_pdf(html_path, pdf_path):
    """Generate PDF from HTML using weasyprint."""
    try:
        from weasyprint import HTML
        print("  Generation PDF...")
        HTML(filename=html_path).write_pdf(pdf_path)
        print(f"  PDF genere : {pdf_path}")
        return True
    except Exception as e:
        print(f"  Erreur PDF : {e}")
        return False


# ================================================================
# TTS GENERATION
# ================================================================

async def generate_tts(scenes):
    """Generate TTS audio for each scene."""
    if not LLM_KEY:
        print("  Pas de cle LLM, TTS desactive.")
        return {}

    try:
        from emergentintegrations.llm.openai import OpenAITextToSpeech
    except ImportError:
        print("  emergentintegrations non installe, TTS desactive.")
        return {}

    tts = OpenAITextToSpeech(api_key=LLM_KEY)
    audio_files = {}
    os.makedirs(AUDIO_DIR, exist_ok=True)

    for scene in scenes:
        num = scene["num"]
        text = enrich_text_for_tts(scene)
        if not text.strip():
            continue

        # Cache: check if audio already exists
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        mp3_path = os.path.join(AUDIO_DIR, f"scene_{num:03d}_{text_hash}.mp3")

        if os.path.exists(mp3_path):
            print(f"  Scene {num}: cache (existant)")
            with open(mp3_path, "rb") as f:
                audio_files[num] = base64.b64encode(f.read()).decode()
            continue

        try:
            print(f"  Scene {num}/{len(scenes)}: TTS...")
            audio_bytes = await tts.generate_speech(
                text=text,
                model="tts-1-hd",
                voice="shimmer",
                speed=0.95,
                response_format="mp3"
            )
            with open(mp3_path, "wb") as f:
                f.write(audio_bytes)
            audio_files[num] = base64.b64encode(audio_bytes).decode()
            print(f"  Scene {num}: OK ({len(audio_bytes)} bytes)")
        except Exception as e:
            print(f"  Scene {num}: erreur TTS - {str(e)[:80]}")
            import time
            time.sleep(2)

    return audio_files


# ================================================================
# MAIN
# ================================================================

async def async_main():
    print("=" * 60)
    print("GENERATION ANIMATION - L'Univers est au Carre")
    print("=" * 60)

    # Read markdown
    if not os.path.exists(SCRIPT_PATH):
        print(f"ERREUR: {SCRIPT_PATH} introuvable.")
        return 1

    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()

    print(f"Script lu : {len(md_content)} caracteres, {md_content.count(chr(10))} lignes")

    # Parse scenes
    scenes = parse_scenes(md_content)
    print(f"Scenes extraites : {len(scenes)}")

    # Filter Minkowski scenes
    scenes = [s for s in scenes if "minkowski" not in s["title"].lower()
              and "minkowski" not in s["text"].lower()[:200]]
    # Renumber
    for i, s in enumerate(scenes):
        s["num"] = i + 1
    print(f"Scenes apres filtrage Minkowski : {len(scenes)}")

    # List images
    all_images = set()
    for s in scenes:
        for img in s.get("images", []):
            all_images.add(img)
    print(f"Images referencees : {len(all_images)}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # TTS
    audio_files = {}
    if ENABLE_TTS:
        print("\n--- Generation TTS (voix feminine, shimmer, FR) ---")
        audio_files = await generate_tts(scenes)
        print(f"Audio genere pour {len(audio_files)} scenes")

    # HTML
    print("\n--- Generation HTML ---")
    html = generate_html(scenes, audio_files)
    html_path = os.path.join(OUTPUT_DIR, "animation.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML genere : {html_path} ({len(html)} chars)")

    # PDF
    if ENABLE_PDF:
        print("\n--- Generation PDF ---")
        pdf_path = os.path.join(OUTPUT_DIR, "animation.pdf")
        generate_pdf(html_path, pdf_path)

    # Scene index
    index = []
    for s in scenes:
        index.append({
            "num": s["num"],
            "title": s["title"],
            "text_length": len(s["text"]),
            "images": len(s.get("images", [])),
            "tables": len(s.get("tables", [])),
            "has_audio": s["num"] in audio_files,
        })
    index_path = os.path.join(OUTPUT_DIR, "scenes_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"\nIndex des scenes : {index_path}")

    print(f"\n{'=' * 60}")
    print(f"ANIMATION GENEREE : {len(scenes)} scenes")
    print(f"HTML : {html_path}")
    if ENABLE_PDF:
        print(f"PDF  : {os.path.join(OUTPUT_DIR, 'animation.pdf')}")
    if ENABLE_TTS:
        print(f"Audio: {len(audio_files)} fichiers MP3")
    print(f"{'=' * 60}")
    return 0


def main():
    return asyncio.run(async_main())


if __name__ == "__main__":
    sys.exit(main())
