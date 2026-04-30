# PRD — Theorie mathematique de Philippe Thomas Savard

## Probleme original
Construire et maintenir un depot GitHub regroupant la theorie "L'Univers est au Carre"
(Philippe Thomas Savard) avec :

1. Une banque de questions/reponses generee par LLM, stockee dans SQLite.
2. Des preuves Isabelle/HOL (`src/hol/`).
3. Une evaluation academique automatisee (`scripts/evaluation/academic_evaluation.py`).
4. Une **animation audiovisuelle automatisee** (HTML + PDF + TTS) basee sur
   `src/SCRIPT_NARRATIF_VP.md`, lancee depuis GitHub Actions.

L'animation finale doit afficher chronologiquement les illustrations en plein ecran
avec un lecteur video, narration audio TTS (voix feminine francaise `shimmer`).
Les equations mathematiques doivent etre presentees comme des **diapositives visuelles
plein ecran** pendant que la narration explique de maniere semantique (mini-scripts)
plutot que de lire les symboles bruts.

## Architecture
```
/app/repo_savard/
├── .github/workflows/
│   ├── build.yml
│   ├── academic-evaluation.yml
│   └── generate-animation.yml
├── scripts/
│   ├── auto_generate_qa.py
│   ├── evaluation/academic_evaluation.py
│   ├── generate_animation.py    (v4 - parser etiquettes)
│   └── note.sh
├── src/
│   ├── hol/                     (preuves Isabelle)
│   ├── SCRIPT_NARRATIF_VP.md    (script narratif etiquete v2)
│   └── mini_script.md           (legacy : explications semantiques)
└── assets/animation/            (illustrations PNG)
```

## Format du script narratif (v2 - etiquettes)
Le fichier `src/SCRIPT_NARRATIF_VP.md` utilise les etiquettes :
- `@NARRATION: x.y`     -> narration principale
- `@MINI_SCRIPT: x.y`   -> narration explicative d'un calcul (page calcul fixe)
- `@EXEMPLE_CALCUL: x.y`-> marqueur explicite de bloc de calcul
- `@NOTE: ...`          -> consignes pour l'agent E1 (jamais narrees)
- `<img src="...">`     -> illustrations
- `---`                 -> separateurs (ignores par le parser)

## Implementations realisees
### Avril 2026 (cette session)
- **Animation v4** (`scripts/generate_animation.py`) :
  - Parser `parse_tagged_script()` qui reconnait les etiquettes `@TAG`
  - Decoupage automatique narration / calcul via `split_calc_from_narrative()`
  - Heuristique `looks_like_calc()` (LaTeX, tableaux MD, mots-cles)
  - 2 types de scenes : `narration` (image plein ecran) et `calculation`
    (page de calcul stylee or/noir, MathJax pour LaTeX)
  - HTML autonome avec lecteur video (Play/Pause/Skip, progress bar, raccourcis clavier)
  - PDF formate (WeasyPrint) avec page par scene
  - TTS optionnel (voix `shimmer` FR via `OpenAITextToSpeech`)
  - 27 scenes generees (18 narration + 9 calcul) a partir du script source
  - `@NOTE` jamais lues ni affichees ; "Voir l'illustration" et titres
    "script narratif de l'exemple..." nettoyes du texte TTS

### Sessions precedentes
- Replacement Unicode -> ASCII pour `Philippot_Method.thy` (Isabelle compliant)
- `academic_evaluation.py` : evaluation multi-critere (note 92.5/100, A+)
- Retry/Exit 0 sur erreurs 502 OpenAI dans `auto_generate_qa.py`
- Flux `CHANGELOG.md` via `.pending_note`
- Secrets `secrets._CLE` (au lieu de `EMERGENT_LLM_KEY`)
- `SCRIPT_NARRATIF_VP.md` consolide (~1921 lignes)
- `src/mini_script.md` : extraction initiale des 17 mini-scripts (legacy)

## Tests realises
- Generation locale `ENABLE_TTS=false ENABLE_PDF=true REPO_ROOT=. python3 scripts/generate_animation.py`
  -> produit `animation.html` (2.6 MB) et `animation.pdf` (1.8 MB) avec 27 scenes
- Smoke test screenshot : scene 1 (narration image) et scene 4 (calcul 2.0 plein ecran) OK
- Lint Python : passes

## Backlog (P1/P2)
- **P1** : Tester le pipeline complet en production via GitHub Actions
  (`workflow_dispatch` -> `generate-animation.yml`) avec `ENABLE_TTS=true`
  et le secret `_CLE` configure
- **P1** : Verifier la synchronisation audio/visuel sur navigateur cible
- **P2** : Affiner les seuils de detection `looks_like_calc()` si certains
  blocs sont mal classes
- **P2** : Permettre l'ajout d'etiquettes `@ILLUSTRATION: ID` explicites pour
  controler precisement quelle image affiche pour quelle narration
- **P2** : Refactoring : decouper `generate_animation.py` (722 lignes) en modules
  (`parser.py`, `renderer_html.py`, `renderer_pdf.py`, `tts.py`)

## Integrations 3rd party
- OpenAI GPT (textes Q&A) -- via Emergent LLM Key
- OpenAI TTS `tts-1-hd` voix `shimmer` -- via Emergent LLM Key
- WeasyPrint (PDF)
- MathJax 3 (rendu LaTeX dans HTML)

## Credentials
- `EMERGENT_LLM_KEY` cote local / `_CLE` cote secrets GitHub Actions
