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
    scenes = build_scenes_from_blocks(blocks)
    assert scenes == []


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
