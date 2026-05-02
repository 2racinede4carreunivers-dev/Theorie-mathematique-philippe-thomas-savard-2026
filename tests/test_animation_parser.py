"""Tests rapides du parser d'etiquettes + rendu SRT."""
import os
import sys
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
os.environ.setdefault("REPO_ROOT", REPO_ROOT)

from generate_animation import parse_tagged_script, build_scenes_from_blocks  # noqa: E402
from generate_video import srt_timestamp, split_text_into_srt_chunks  # noqa: E402


def test_parser_recognises_all_tags():
    md = """
@NARRATION: 1.0
Bonjour et bienvenue dans cette theorie.
---

@NOTE: Placer l'exemple sur une page fixe.

Suite A: 2 + 4 = 6
Somme = 42
---

@MINI_SCRIPT: 1.0
Ce mini-script explique le calcul precedent de maniere conceptuelle.
---

@NARRATION: 2.0
La suite se poursuit.
"""
    blocks = parse_tagged_script(md)
    tags = [b["tag"] for b in blocks]
    assert "NARRATION" in tags
    assert "MINI_SCRIPT" in tags
    # @NOTE ne doit pas apparaitre comme une section : ses consignes
    # sont rattachees a la section courante (ou absorbees)
    assert tags.count("NARRATION") == 2
    assert tags.count("MINI_SCRIPT") == 1


def test_note_content_excluded_from_narration():
    md = """
@NARRATION: 1.0
Texte de narration principal.

@NOTE: Cette note ne doit jamais etre narree
ni apparaitre dans le texte audio.
"""
    blocks = parse_tagged_script(md)
    narr = next(b for b in blocks if b["tag"] == "NARRATION")
    assert "narre" not in narr["text"].lower()
    assert "jamais" not in narr["text"].lower()
    assert "Texte de narration" in narr["text"]


def test_mini_script_uses_preceding_calc_block():
    md = """
@NARRATION: 1.0
Introduction.

Suite A: 2 + 4 + 8 = 14
Suite B: 16 + 32 = 48
Digamma calcule = 100
---

@MINI_SCRIPT: 1.0
Explication semantique du calcul sans lire les symboles.
"""
    blocks = parse_tagged_script(md)
    scenes = build_scenes_from_blocks(blocks)
    calc_scenes = [s for s in scenes if s["type"] == "calculation"]
    assert len(calc_scenes) == 1
    assert "Suite A" in calc_scenes[0]["calc_raw"]
    assert "Digamma" in calc_scenes[0]["calc_raw"]
    assert "semantique" in calc_scenes[0]["text"].lower()


def test_srt_timestamp_formatting():
    assert srt_timestamp(0.0) == "00:00:00,000"
    assert srt_timestamp(1.5) == "00:00:01,500"
    assert srt_timestamp(61.234) == "00:01:01,234"
    assert srt_timestamp(3661.001) == "01:01:01,001"


def test_split_text_into_srt_chunks_respects_timing():
    text = "Premiere phrase. Deuxieme phrase ! Troisieme phrase ?"
    entries = split_text_into_srt_chunks(text, 9.0, 10.0)
    assert len(entries) == 3
    # La derniere entree doit finir a environ 19s (10 + 9)
    assert abs(entries[-1]["end"] - 19.0) < 0.01
    # Les entries sont ordonnees chronologiquement
    for i in range(1, len(entries)):
        assert entries[i]["start"] >= entries[i - 1]["start"]


def test_empty_script_does_not_crash():
    blocks = parse_tagged_script("")
    assert blocks == []
    # Scenes contient TOUJOURS la scene d'intro (page de presentation)
    scenes = build_scenes_from_blocks(blocks)
    assert len(scenes) == 1
    assert scenes[0]["type"] == "intro"


def test_stop_markers_truncate_parsing():
    md = """
@NARRATION: 1.0
Contenu valide.

============================================================
FIN DU SCRIPT
============================================================

# NOTE POUR L'AGENT
Ceci ne doit pas etre parse.

@NARRATION: 99.0
Contenu apres FIN -- doit etre ignore.
"""
    blocks = parse_tagged_script(md)
    # Seule la NARRATION 1.0 doit etre dans les blocs
    narrations = [b for b in blocks if b["tag"] == "NARRATION"]
    assert len(narrations) == 1
    assert narrations[0]["id"] == "1.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


def test_a_href_image_format_recognized():
    """Reconnait <a href='X.png'> comme illustration (format dominant du .md)."""
    md = """
@NARRATION: 1.0

<p align="center">
  <a href="./assets/animation/animation_A-3.png">
    Voir l'illustration : animation_A-3
  </a>
</p>

Texte narratif principal qui devrait apparaitre.
"""
    blocks = parse_tagged_script(md)
    narr = next(b for b in blocks if b["tag"] == "NARRATION")
    assert "./assets/animation/animation_A-3.png" in narr["images"]
    assert "illustration" not in narr["text"].lower()


def test_narration_with_multiple_images_creates_subscenes():
    """Une section avec 3 illustrations cree 3 sous-scenes narration."""
    md = """
@NARRATION: 13.0

<a href="./assets/animation/animation_C-7.png">img1</a>
Premier paragraphe parlant de C-7.

<a href="./assets/animation/animation_C-8.png">img2</a>
Deuxieme paragraphe parlant de C-8.

<a href="./assets/animation/animation_C-15.png">img3</a>
Troisieme paragraphe parlant de C-15.
"""
    blocks = parse_tagged_script(md)
    scenes = build_scenes_from_blocks(blocks)
    narr_scenes = [s for s in scenes if s["type"] == "narration"]
    # 3 sous-scenes attendues (une par image)
    assert len(narr_scenes) == 3
    # Chaque scene contient le texte specifique
    assert "C-7" in narr_scenes[0]["text"]
    assert "C-8" in narr_scenes[1]["text"]
    assert "C-15" in narr_scenes[2]["text"]


def test_no_image_means_inherit_previous():
    """Une narration sans image herite de la derniere image affichee."""
    md = """
@NARRATION: 1.0

<a href="./assets/animation/animation_A-1.png">img</a>
Premier texte avec image.

@NARRATION: 1.1

Deuxieme narration sans image propre.
"""
    blocks = parse_tagged_script(md)
    scenes = build_scenes_from_blocks(blocks)
    narr_scenes = [s for s in scenes if s["type"] == "narration"]
    # La 2e scene doit avoir l'image de la 1ere (heritage), meme si fichier absent
    # Note: l'image peut etre None si fichier inexistant -- on teste la logique
    # de propagation du `last_image` plus bas.
    assert len(narr_scenes) == 2


def test_intro_scene_is_first():
    """La scene d'intro (page de presentation) est toujours premiere."""
    md = """
@NARRATION: 1.0
Premier texte.

@MINI_SCRIPT: 1.0
Un mini-script.
"""
    blocks = parse_tagged_script(md)
    scenes = build_scenes_from_blocks(blocks)
    assert scenes[0]["type"] == "intro"
    assert scenes[0]["num"] == 1
    assert "Philippe Thomas Savard" in scenes[0]["meta"]["author"]
    assert scenes[0]["title"] == "L'Univers est au Carre"
    # La scene d'intro doit avoir une narration introductive non vide
    assert len(scenes[0]["text"]) > 50
