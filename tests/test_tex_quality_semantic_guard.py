import importlib.util
from pathlib import Path


MODULE_PATH = Path("scripts/tex_quality/quality_pipeline.py")
spec = importlib.util.spec_from_file_location("quality_pipeline", MODULE_PATH)
qp = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(qp)


def test_semantic_score_perfect_when_unchanged():
    text = "La hauteur suit la spirale de Theodore."
    assert qp.semantic_score_out_of_10(text, text) == 10.0


def test_semantic_score_penalizes_number_change():
    a = "Le rayon vaut sqrt(2) / 10."
    b = "Le rayon vaut sqrt(3) / 10."
    assert qp.semantic_score_out_of_10(a, b) < 9.6


def test_prose_filter_skips_math_and_commands():
    editable, in_math = qp.is_prose_line("\\section*{Titre}", False)
    assert editable is False
    editable, in_math = qp.is_prose_line("$x^2 + y^2 = z^2$", False)
    assert editable is False
    editable, in_math = qp.is_prose_line("Texte normal sans formule", False)
    assert editable is True
