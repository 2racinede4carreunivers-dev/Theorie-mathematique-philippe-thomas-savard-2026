#!/usr/bin/env python3
"""
generate_video.py
=================
Assemble un MP4 16:9 1920x1080 (YouTube / Facebook / LinkedIn) a partir des
scenes generees par generate_animation.py, en utilisant les MP3 TTS deja caches
dans animation_output/audio/.

Produit aussi :
- Sous-titres multilingues (.srt) : FR (source), EN, ES, DE
- Variante MP4 avec sous-titres FR incrustes (pour partage standalone)

Prerequis : ffmpeg, PIL, mutagen
Optionnel  : emergentintegrations (traduction via Emergent LLM Key)

Lance apres generate_animation.py avec ENABLE_TTS=true.
"""

import os
import re
import sys
import json
import hashlib
import subprocess
import asyncio
from pathlib import Path

# Reutilise le parser de generate_animation.py
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)
from generate_animation import (  # noqa: E402
    parse_tagged_script,
    build_scenes_from_blocks,
    embed_image_path,
    SCRIPT_PATH,
    OUTPUT_DIR,
    AUDIO_DIR,
    LLM_KEY,
)

VIDEO_DIR = os.path.join(OUTPUT_DIR, "video")
FRAMES_DIR = os.path.join(VIDEO_DIR, "frames")
SUBS_DIR = os.path.join(VIDEO_DIR, "subtitles")
TARGET_W = 1920
TARGET_H = 1080
FPS = 30

# Mode TEST : limite le nombre de scenes et utilise un preset rapide
TEST_MODE = os.environ.get("VIDEO_TEST_MODE", "false").lower() == "true"
MAX_SCENES = int(os.environ.get("MAX_SCENES", "0"))  # 0 = toutes
FFMPEG_PRESET = os.environ.get("FFMPEG_PRESET", "ultrafast" if TEST_MODE else "medium")

# Langues cibles pour sous-titres (FR est la source)
TARGET_LANGS = os.environ.get("SUBTITLE_LANGS", "en,es,de").split(",")
TARGET_LANGS = [lang.strip() for lang in TARGET_LANGS if lang.strip()]

LANG_LABELS = {
    "en": "English",
    "es": "Espanol",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Portugues",
    "ja": "Japanese",
    "zh": "Chinese",
}

# Skip translation si pas de cle ou desactive explicitement
ENABLE_TRANSLATION = (
    os.environ.get("ENABLE_TRANSLATION", "true").lower() == "true"
    and bool(LLM_KEY)
)


# ================================================================
# RENDU DES IMAGES DES SCENES (1920x1080)
# ================================================================

from PIL import Image, ImageDraw, ImageFont  # noqa: E402


def find_font(prefer_mono=False):
    """Trouve une police disponible dans le systeme."""
    candidates_mono = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]
    candidates_serif = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ]
    pool = candidates_mono if prefer_mono else candidates_serif
    for p in pool:
        if os.path.exists(p):
            return p
    return None


def render_intro_frame(scene, out_path):
    """Cree un PNG 1920x1080 pour la page de presentation (intro).

    Layout : photo de l'auteur a gauche, titre + meta a droite, sur fond
    noir avec touches dorees.
    """
    import base64
    from io import BytesIO

    canvas = Image.new("RGB", (TARGET_W, TARGET_H), color=(10, 8, 12))
    draw = ImageDraw.Draw(canvas)

    # Gradient radial douce simule par plusieurs cercles degrades
    # (simple : un halo dore centre)
    for r, alpha in [(900, 20), (700, 35), (500, 45), (300, 55)]:
        overlay = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([0, 0, r * 2, r * 2], fill=(201, 168, 76, alpha))
        canvas.paste(
            Image.alpha_composite(
                Image.new("RGBA", overlay.size, (0, 0, 0, 0)), overlay
            ).convert("RGB"),
            (TARGET_W // 2 - r, TARGET_H // 2 - r),
            overlay.split()[3],
        )

    # Recadre l'image auteur (portrait) a gauche
    photo_data_url = scene.get("author_photo")
    photo_x_center = 520  # centre de la photo
    photo_y_center = TARGET_H // 2
    photo_w, photo_h = 380, 520

    if photo_data_url:
        m = re.match(r'data:image/[^;]+;base64,(.+)', photo_data_url)
        if m:
            try:
                img_bytes = base64.b64decode(m.group(1))
                img = Image.open(BytesIO(img_bytes)).convert("RGB")
                # Redimensionner pour remplir photo_w x photo_h (crop centre)
                ratio = max(photo_w / img.width, photo_h / img.height)
                new_w = int(img.width * ratio)
                new_h = int(img.height * ratio)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                left = (new_w - photo_w) // 2
                top = (new_h - photo_h) // 2
                img = img.crop((left, top, left + photo_w, top + photo_h))

                # Cadre dore
                px = photo_x_center - photo_w // 2
                py = photo_y_center - photo_h // 2
                draw.rectangle(
                    [px - 6, py - 6, px + photo_w + 6, py + photo_h + 6],
                    outline=(201, 168, 76), width=4,
                )
                canvas.paste(img, (px, py))
            except Exception as e:
                print(f"  Erreur chargement photo intro : {e}")

    # Texte a droite
    text_x = 900
    font_path = find_font()

    # Titre
    if font_path:
        try:
            f_title = ImageFont.truetype(font_path, 78)
        except Exception:
            f_title = ImageFont.load_default()
        try:
            f_sub = ImageFont.truetype(font_path, 30)
            f_meta = ImageFont.truetype(font_path, 24)
            f_meta_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
            f_meta_bold = (
                ImageFont.truetype(f_meta_bold_path, 24)
                if os.path.exists(f_meta_bold_path) else f_meta
            )
        except Exception:
            f_sub = f_meta = f_meta_bold = f_title

        title = scene.get("title", "L'Univers est au Carre")
        subtitle = scene.get("subtitle", "")
        meta = scene.get("meta", {})

        # Titre en dore
        draw.text((text_x, 220), title, fill=(255, 216, 102), font=f_title)
        # Subtitle en or patine
        draw.text((text_x, 320), subtitle, fill=(201, 168, 76), font=f_sub)

        # Ligne de separation
        draw.line([(text_x, 395), (text_x + 600, 395)],
                  fill=(201, 168, 76), width=2)

        # Meta
        meta_y = 440
        line_h = 52
        rows = [
            ("Auteur :", meta.get("author", "")),
            ("Date :", meta.get("date", "")),
            ("Lieu :", meta.get("place", "")),
            ("Licence :", meta.get("license", "")),
        ]
        for label, val in rows:
            draw.text((text_x, meta_y), label, fill=(201, 168, 76),
                      font=f_meta_bold)
            draw.text((text_x + 140, meta_y), val, fill=(232, 224, 192),
                      font=f_meta)
            meta_y += line_h

    canvas.save(out_path, "PNG", optimize=True)


def render_narration_frame(image_data_url, title, out_path):
    """Cree un PNG 1920x1080 avec l'illustration centree sur fond noir.

    image_data_url: 'data:image/png;base64,...' ou None
    """
    canvas = Image.new("RGB", (TARGET_W, TARGET_H), color=(8, 8, 12))

    if image_data_url:
        import base64
        from io import BytesIO
        # Extraire les donnees base64
        m = re.match(r'data:image/[^;]+;base64,(.+)', image_data_url)
        if m:
            img_bytes = base64.b64decode(m.group(1))
            try:
                img = Image.open(BytesIO(img_bytes)).convert("RGB")
                # Redimensionner en preservant le ratio, pour entrer dans 95% de l'espace
                max_w = int(TARGET_W * 0.90)
                max_h = int(TARGET_H * 0.85)
                ratio = min(max_w / img.width, max_h / img.height)
                new_w = int(img.width * ratio)
                new_h = int(img.height * ratio)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                # Coller centre
                x = (TARGET_W - new_w) // 2
                y = (TARGET_H - new_h) // 2
                canvas.paste(img, (x, y))
            except Exception as e:
                print(f"  Erreur chargement image : {e}")

    # Overlay titre haut gauche
    draw = ImageDraw.Draw(canvas)
    font_path = find_font()
    if font_path:
        font = ImageFont.truetype(font_path, 28)
        # Fond semi-transparent pour le titre : on dessine un rect opaque
        draw.rectangle([20, 20, 20 + 14 + len(title) * 14, 66],
                       fill=(0, 0, 0))
        draw.text((34, 28), title, fill=(201, 168, 76), font=font)

    canvas.save(out_path, "PNG", optimize=True)


def render_calc_frame(calc_raw, title, out_path):
    """Cree un PNG 1920x1080 affichant le texte du calcul en bloc stylise."""
    canvas = Image.new("RGB", (TARGET_W, TARGET_H), color=(8, 8, 12))
    draw = ImageDraw.Draw(canvas)

    # Zone centrale stylisee
    box_margin_x = 120
    box_margin_y = 90
    box = (box_margin_x, box_margin_y,
           TARGET_W - box_margin_x, TARGET_H - box_margin_y)
    # Fond fonce + bordure or
    draw.rectangle(box, fill=(26, 26, 26), outline=(201, 168, 76), width=3)

    # Nettoyer le texte : retirer balises HTML/img, LaTeX markers, markdown bold
    text = re.sub(r'<[^>]+>', '', calc_raw)
    text = re.sub(r'\\\[|\\\]', '', text)
    text = re.sub(r'\\text\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'(\1)/(\2)', text)
    text = re.sub(r'\\left|\\right', '', text)
    text = re.sub(r'\\times', 'x', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = text.strip()

    # Decomposer en lignes
    lines = [ln for ln in text.split("\n")]
    # Supprimer lignes vides multiples
    cleaned = []
    prev_empty = False
    for ln in lines:
        if ln.strip() == "":
            if not prev_empty:
                cleaned.append("")
            prev_empty = True
        else:
            cleaned.append(ln)
            prev_empty = False
    lines = cleaned

    # Choix taille police selon volume de texte
    total_chars = sum(len(ln) for ln in lines)
    if len(lines) > 30 or total_chars > 1500:
        font_size = 20
    elif len(lines) > 20 or total_chars > 900:
        font_size = 24
    else:
        font_size = 28

    mono_path = find_font(prefer_mono=True)
    if mono_path:
        font = ImageFont.truetype(mono_path, font_size)
    else:
        font = ImageFont.load_default()

    # Rendre le texte a l'interieur de la box, centre verticalement
    line_height = int(font_size * 1.4)
    inner_x = box[0] + 40
    inner_y = box[1] + 30
    inner_w = box[2] - box[0] - 80
    inner_h = box[3] - box[1] - 60

    # Wrapping approximatif (si ligne trop longue)
    wrapped_lines = []
    # Approx : on mesure 1 char avec la police pour estimer le max char width
    sample = font.getbbox("M")
    char_w = (sample[2] - sample[0]) or font_size
    max_chars = max(10, inner_w // char_w)
    for ln in lines:
        if len(ln) <= max_chars:
            wrapped_lines.append(ln)
        else:
            # wrap simple
            cur = ""
            for word in ln.split(" "):
                if len(cur) + len(word) + 1 <= max_chars:
                    cur = (cur + " " + word).strip()
                else:
                    if cur:
                        wrapped_lines.append(cur)
                    cur = word
            if cur:
                wrapped_lines.append(cur)

    # Centrage vertical si possible
    total_h = len(wrapped_lines) * line_height
    if total_h < inner_h:
        inner_y = box[1] + (box[3] - box[1] - total_h) // 2

    # Titre en haut (badge)
    font_title_path = find_font()
    if font_title_path:
        f_title = ImageFont.truetype(font_title_path, 26)
        draw.text((40, 30), title, fill=(201, 168, 76), font=f_title)

    # Texte du calcul
    for i, ln in enumerate(wrapped_lines):
        y = inner_y + i * line_height
        if y + line_height > box[3] - 20:
            # overflow : arret
            draw.text((inner_x, y), "...", fill=(201, 168, 76), font=font)
            break
        # Headers (lignes commencant par # ou ##) : les mettre en or
        color = (232, 224, 192)
        if re.match(r'^\s*(Suite [AB]|Digamma|Pour \(|\d+\.\d+\.)', ln):
            color = (255, 216, 102)
        elif re.match(r'^\s*(ex |Observons|Voici un exemple)', ln):
            color = (255, 216, 102)
        draw.text((inner_x, y), ln, fill=color, font=font)

    canvas.save(out_path, "PNG", optimize=True)


# ================================================================
# AUDIO : duree via mutagen
# ================================================================

def get_audio_duration(mp3_path):
    """Retourne la duree du MP3 en secondes."""
    try:
        from mutagen.mp3 import MP3
        audio = MP3(mp3_path)
        return float(audio.info.length)
    except Exception as e:
        print(f"  Erreur duree {mp3_path}: {e}")
        # Fallback : duree par defaut 5s
        return 5.0


def find_audio_for_scene(scene_num, scene_text):
    """Trouve le fichier MP3 pour une scene (meme logique que generate_tts).

    Cherche dans l'ordre :
      1. animation_output/audio/ (runtime)
      2. assets/audio_cache/ (cache commit dans le repo)
    """
    text_hash = hashlib.md5(scene_text[:4000].encode()).hexdigest()[:8]
    expected_name = f"scene_{scene_num:03d}_{text_hash}.mp3"

    # Candidats : dossiers dans l'ordre de priorite
    from generate_animation import REPO_ROOT as _REPO_ROOT
    cache_dir = os.path.join(_REPO_ROOT, "assets", "audio_cache")
    candidates_dirs = [AUDIO_DIR, cache_dir]

    # 1. Match exact (scene_NNN_<hash>.mp3)
    for d in candidates_dirs:
        path = os.path.join(d, expected_name)
        if os.path.exists(path):
            return path
    # 2. Fallback : n'importe quel fichier scene_NNN_*.mp3
    for d in candidates_dirs:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.startswith(f"scene_{scene_num:03d}_") and f.endswith(".mp3"):
                    return os.path.join(d, f)
    return None


# ================================================================
# SOUS-TITRES SRT
# ================================================================

def srt_timestamp(seconds):
    """Convertit un nombre de secondes en format SRT : HH:MM:SS,mmm"""
    ms = int(round(seconds * 1000))
    h = ms // 3600000
    ms -= h * 3600000
    m = ms // 60000
    ms -= m * 60000
    s = ms // 1000
    ms = ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_text_into_srt_chunks(text, audio_duration, start_time):
    """Decoupe le texte d'une scene en entrees SRT synchronisees.

    On decoupe par phrases et on repartit la duree proportionnellement
    au nombre de caracteres.
    """
    # Decouper par phrases
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÉÀÈÊÇ])', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return []

    total_chars = sum(len(s) for s in sentences) or 1
    entries = []
    t = start_time
    for s in sentences:
        duration = audio_duration * len(s) / total_chars
        # wrap les phrases longues en 2 lignes pour lisibilite
        if len(s) > 80:
            # couper a l'espace le plus proche du milieu
            mid = len(s) // 2
            left_break = s.rfind(" ", 0, mid + 20)
            if left_break > 30:
                s = s[:left_break] + "\n" + s[left_break + 1:]
        entries.append({
            "start": t,
            "end": t + duration,
            "text": s,
        })
        t += duration
    return entries


def write_srt(entries, path):
    """Ecrit les entrees au format .srt."""
    lines = []
    for i, e in enumerate(entries, 1):
        lines.append(str(i))
        lines.append(f"{srt_timestamp(e['start'])} --> {srt_timestamp(e['end'])}")
        lines.append(e["text"])
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


async def translate_entries(fr_entries, target_lang):
    """Traduit les textes des entries de FR vers target_lang via Emergent LLM.

    Ne modifie PAS les timings.
    """
    if not LLM_KEY or not ENABLE_TRANSLATION:
        print(f"  Pas de traduction {target_lang} : cle ou option desactivee.")
        return None
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
    except ImportError:
        print(f"  emergentintegrations non installe, skip {target_lang}.")
        return None

    lang_name = LANG_LABELS.get(target_lang, target_lang)
    session_id = f"subtitle_translate_{target_lang}"
    chat = (
        LlmChat(
            api_key=LLM_KEY,
            session_id=session_id,
            system_message=(
                f"You are a professional subtitle translator. Translate the "
                f"French sentences below into {lang_name}. Keep the same order, "
                f"one translation per line, prefixed by its number. Preserve "
                f"line breaks marked with \\n inside a sentence. Do NOT add "
                f"commentary. Mathematical terms must stay accurate."
            ),
        )
        .with_model("openai", "gpt-4o-mini")
    )

    # Traduire en lots (ex: 20 entrees par appel pour rester rapide)
    translated = []
    batch_size = 20
    NL_MARKER = " [NL] "
    for i in range(0, len(fr_entries), batch_size):
        batch = fr_entries[i:i + batch_size]
        numbered = "\n".join(
            f"{j + 1}. " + e['text'].replace("\n", NL_MARKER)
            for j, e in enumerate(batch)
        )
        prompt = (
            f"Translate these {len(batch)} French sentences into {lang_name}. "
            f"Output format : one line per sentence, starting with the number "
            f"and a dot, then the translation. Nothing else.\n\n{numbered}"
        )
        try:
            print(f"  Traduction {target_lang} lot {i // batch_size + 1}...")
            response = await chat.send_message(UserMessage(text=prompt))
            out = response.strip()
            # Parser les lignes numerotees
            parsed = {}
            for line in out.split("\n"):
                m = re.match(r'^\s*(\d+)\.\s*(.+)$', line)
                if m:
                    idx = int(m.group(1)) - 1
                    parsed[idx] = m.group(2).strip().replace(NL_MARKER, "\n")
            for j, e in enumerate(batch):
                new_text = parsed.get(j, e["text"])  # fallback = original
                translated.append({
                    "start": e["start"],
                    "end": e["end"],
                    "text": new_text,
                })
        except Exception as exc:
            print(f"  Erreur traduction {target_lang}: {str(exc)[:80]}")
            # Fallback : garder l'original pour ne pas casser la video
            translated.extend(batch)

    return translated


# ================================================================
# PIPELINE VIDEO : images -> concat ffmpeg -> mp4
# ================================================================

def build_concat_file(scene_entries, concat_path):
    """Ecrit le fichier ffconcat decrivant la sequence frames + durees."""
    with open(concat_path, "w", encoding="utf-8") as f:
        f.write("ffconcat version 1.0\n")
        for e in scene_entries:
            f.write(f"file '{os.path.abspath(e['frame'])}'\n")
            f.write(f"duration {e['duration']:.3f}\n")
        # Repeter la derniere frame (exigence ffconcat)
        if scene_entries:
            f.write(f"file '{os.path.abspath(scene_entries[-1]['frame'])}'\n")


def concat_audio(scene_entries, out_path):
    """Concatene tous les mp3 en un seul fichier audio.

    Les scenes sans audio TTS recoivent un silence de la meme duree.
    """
    list_path = out_path + ".list"
    silent_tmps = []
    with open(list_path, "w") as f:
        for e in scene_entries:
            if e.get("audio"):
                f.write(f"file '{os.path.abspath(e['audio'])}'\n")
            else:
                tmp = os.path.join(VIDEO_DIR, f".silent_{e['num']}.mp3")
                silent_tmps.append(tmp)
                subprocess.run([
                    "ffmpeg", "-y", "-f", "lavfi", "-i",
                    "anullsrc=channel_layout=stereo:sample_rate=44100",
                    "-t", str(e["duration"]), "-q:a", "9",
                    "-acodec", "libmp3lame", tmp,
                ], check=True, capture_output=True)
                f.write(f"file '{os.path.abspath(tmp)}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_path,
        "-c", "copy", out_path,
    ], check=True, capture_output=True)

    # Nettoyage des fichiers temporaires
    try:
        os.remove(list_path)
    except OSError:
        pass
    for t in silent_tmps:
        try:
            os.remove(t)
        except OSError:
            pass


def render_mp4(concat_path, audio_path, out_path):
    """Assemble le MP4 final 1920x1080 H.264 + AAC."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-preset", FFMPEG_PRESET,
        "-crf", "23",
        "-vf", f"scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=decrease,pad={TARGET_W}:{TARGET_H}:(ow-iw)/2:(oh-ih)/2:black,fps={FPS}",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        out_path,
    ]
    print("  Encodage MP4...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("  Erreur ffmpeg (video) :")
        print(r.stderr[-600:])
        return False
    return True


def render_mp4_with_subs(input_mp4, srt_path, out_path):
    """Genere une variante MP4 avec sous-titres FR incrustes (burned-in)."""
    # Echapper chemin SRT pour ffmpeg
    srt_escaped = srt_path.replace(":", r"\:").replace(",", r"\,")
    cmd = [
        "ffmpeg", "-y", "-i", input_mp4,
        "-vf", f"subtitles={srt_escaped}:force_style='Fontsize=22,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BackColour=&H80000000&,BorderStyle=4,Outline=1,Shadow=0,MarginV=40'",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        out_path,
    ]
    print("  Encodage MP4 (sous-titres FR incrustes)...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("  Erreur ffmpeg (burn-in) :")
        print(r.stderr[-600:])
        return False
    return True


# ================================================================
# MAIN
# ================================================================

async def async_main():
    print("=" * 60)
    print("VIDEO MP4 (16:9) - L'Univers est au Carre")
    print("=" * 60)

    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        md = f.read()

    blocks = parse_tagged_script(md)
    scenes = build_scenes_from_blocks(blocks)
    if MAX_SCENES > 0:
        scenes = scenes[:MAX_SCENES]
        print(f"Mode limite : {MAX_SCENES} premieres scenes uniquement")
    print(f"Scenes : {len(scenes)}")
    if TEST_MODE:
        print(f"Mode TEST actif (preset={FFMPEG_PRESET})")

    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(FRAMES_DIR, exist_ok=True)
    os.makedirs(SUBS_DIR, exist_ok=True)

    # 1. Rendu des frames PNG 1920x1080
    print("\n--- Rendu des frames ---")
    scene_entries = []
    for sc in scenes:
        num = sc["num"]
        frame_path = os.path.join(FRAMES_DIR, f"scene_{num:03d}.png")
        if sc["type"] == "intro":
            # Scene de presentation : passer la scene brute pour acceder
            # aux meta, subtitle, author_photo, etc.
            intro_data = {
                "title": sc.get("title", ""),
                "subtitle": sc.get("subtitle", ""),
                "meta": sc.get("meta", {}),
                "author_photo": (
                    sc["author_photo"]["data"]
                    if sc.get("author_photo") else None
                ),
            }
            render_intro_frame(intro_data, frame_path)
        elif sc["type"] == "calculation":
            render_calc_frame(sc.get("calc_raw", ""), sc["title"], frame_path)
        else:
            img_url = sc["image"]["data"] if sc.get("image") else None
            render_narration_frame(img_url, sc["title"], frame_path)

        # 2. Duree = duree audio si dispo sinon estimation
        audio_path = find_audio_for_scene(num, sc["text"])
        if audio_path:
            duration = get_audio_duration(audio_path)
        else:
            # Estimation : ~150 mots/min ~= 2.5 mots/sec
            words = len(sc["text"].split())
            duration = max(3.0, min(words / 2.3, 60.0))

        scene_entries.append({
            "num": num,
            "frame": frame_path,
            "audio": audio_path,
            "duration": duration,
            "text": sc["text"],
            "type": sc["type"],
            "title": sc["title"],
        })
        print(f"  Scene {num:02d} [{sc['type'][:4]}] {duration:5.2f}s  {'[AUDIO]' if audio_path else '[SILENT]'}")

    total_duration = sum(e["duration"] for e in scene_entries)
    print(f"Duree totale : {total_duration:.1f}s ({total_duration / 60:.1f} min)")

    # 3. Concat audio + concat file
    print("\n--- Concatenation audio ---")
    audio_concat = os.path.join(VIDEO_DIR, "audio_full.mp3")
    try:
        concat_audio(scene_entries, audio_concat)
        print(f"  Audio concatene : {audio_concat}")
    except Exception as e:
        print(f"  Erreur concat audio : {e}")
        return 1

    concat_file = os.path.join(VIDEO_DIR, "scenes.ffconcat")
    build_concat_file(scene_entries, concat_file)

    # 4. Assemble MP4
    print("\n--- Encodage MP4 ---")
    mp4_path = os.path.join(VIDEO_DIR, "animation_16x9_youtube.mp4")
    if not render_mp4(concat_file, audio_concat, mp4_path):
        return 1
    size_mb = os.path.getsize(mp4_path) / (1024 * 1024)
    print(f"  MP4 produit : {mp4_path} ({size_mb:.1f} MB)")

    # 5. Sous-titres SRT
    print("\n--- Generation sous-titres FR ---")
    fr_entries = []
    current_t = 0.0
    for e in scene_entries:
        chunks = split_text_into_srt_chunks(e["text"], e["duration"], current_t)
        fr_entries.extend(chunks)
        current_t += e["duration"]

    fr_srt = os.path.join(SUBS_DIR, "animation_fr.srt")
    write_srt(fr_entries, fr_srt)
    print(f"  {fr_srt} : {len(fr_entries)} entrees")

    # 6. Traductions
    for lang in TARGET_LANGS:
        print(f"\n--- Sous-titres {lang.upper()} ---")
        translated = await translate_entries(fr_entries, lang)
        if translated:
            path = os.path.join(SUBS_DIR, f"animation_{lang}.srt")
            write_srt(translated, path)
            print(f"  {path} : {len(translated)} entrees")

    # 7. Variante MP4 avec sous-titres FR incrustes
    print("\n--- MP4 variante avec sous-titres FR incrustes ---")
    mp4_burned = os.path.join(VIDEO_DIR, "animation_16x9_youtube_FR_subtitles.mp4")
    render_mp4_with_subs(mp4_path, fr_srt, mp4_burned)
    if os.path.exists(mp4_burned):
        size_mb = os.path.getsize(mp4_burned) / (1024 * 1024)
        print(f"  MP4 FR-sub produit : {mp4_burned} ({size_mb:.1f} MB)")

    # 8. Manifest
    manifest = {
        "total_duration_seconds": total_duration,
        "scene_count": len(scene_entries),
        "resolution": f"{TARGET_W}x{TARGET_H}",
        "fps": FPS,
        "files": {
            "video_clean": os.path.basename(mp4_path),
            "video_fr_subtitles": (os.path.basename(mp4_burned)
                                   if os.path.exists(mp4_burned) else None),
            "subtitles": {
                "fr": os.path.relpath(fr_srt, VIDEO_DIR),
                **{
                    lang: f"subtitles/animation_{lang}.srt"
                    for lang in TARGET_LANGS
                    if os.path.exists(os.path.join(SUBS_DIR, f"animation_{lang}.srt"))
                },
            },
        },
    }
    with open(os.path.join(VIDEO_DIR, "video_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print("VIDEO PRODUITE :")
    print(f"  - {mp4_path}")
    if os.path.exists(mp4_burned):
        print(f"  - {mp4_burned} (avec sous-titres FR incrustes)")
    print(f"  - {len(os.listdir(SUBS_DIR))} fichiers SRT dans {SUBS_DIR}")
    print(f"  Duree : {total_duration / 60:.1f} min")
    print(f"{'=' * 60}")
    return 0


def main():
    return asyncio.run(async_main())


if __name__ == "__main__":
    sys.exit(main())
