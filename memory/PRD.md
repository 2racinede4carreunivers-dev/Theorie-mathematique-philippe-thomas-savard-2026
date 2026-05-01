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

- **Export Video MP4 pour reseaux sociaux** (`scripts/generate_video.py`) :
  - Format 16:9 1920x1080 30fps H.264 + AAC 192k (YouTube / Facebook / LinkedIn)
  - Rendu PNG des scenes via Pillow (narration = image centree ; calculation =
    bloc stylise or/noir avec texte monospace)
  - Duree audio detectee automatiquement via mutagen
  - Concatenation audio (TTS ou silences) et video via ffmpeg concat demuxer
  - **Sous-titres multilingues SRT** : FR source + EN + ES + DE
    (traduction via Emergent LLM gpt-4o-mini par lots de 20)
  - **Variante MP4 avec sous-titres FR incrustes** (burned-in) pour partage
    standalone
  - Workflow GitHub Actions dedie (`generate-video.yml`) avec choix des
    langues, mode test, limitation scenes
  - Options env : `VIDEO_TEST_MODE`, `MAX_SCENES`, `FFMPEG_PRESET`,
    `SUBTITLE_LANGS`, `ENABLE_TRANSLATION`

- **Tests pytest** (`tests/test_animation_parser.py`) :
  - 7 tests passent : parser d'etiquettes, exclusion des @NOTE, association
    mini-script <-> calcul precedent, format SRT, decoupage chunks SRT,
    robustesse fichier vide, marqueurs de fin

### Sessions precedentes
- Replacement Unicode -> ASCII pour `Philippot_Method.thy` (Isabelle compliant)
- `academic_evaluation.py` : evaluation multi-critere (note 92.5/100, A+)
- Retry/Exit 0 sur erreurs 502 OpenAI dans `auto_generate_qa.py`
- Flux `CHANGELOG.md` via `.pending_note`
- Secrets `secrets._CLE` (au lieu de `EMERGENT_LLM_KEY`)
- `SCRIPT_NARRATIF_VP.md` consolide (~1921 lignes)
- `src/mini_script.md` : extraction initiale des 17 mini-scripts (legacy)

## Tests realises
- Generation animation locale `ENABLE_TTS=false ENABLE_PDF=true REPO_ROOT=. python3 scripts/generate_animation.py`
  -> produit `animation.html` (2.6 MB) et `animation.pdf` (1.8 MB) avec 27 scenes
- Generation video locale `VIDEO_TEST_MODE=true MAX_SCENES=2 python3 scripts/generate_video.py`
  -> produit `animation_16x9_youtube.mp4` (3.1 MB, 2 min) + variante avec
  sous-titres FR incrustes (4.1 MB) en environ 2 min sur preset ultrafast
- Traduction LLM (EN/ES) validee sur 3 phrases -- traductions precises y
  compris des termes mathematiques ("Digamma", "nombre premier")
- Smoke test screenshot : scene 1 (narration image) et scene 4 (calcul 2.0
  plein ecran) OK ; MP4 frame : illustration + badge NARRATION + titre
  + sous-titres FR lisibles
- Lint Python : passes (animation.py + video.py)
- Tests pytest : **7/7 passent** (`tests/test_animation_parser.py`)

## Backlog (P1/P2)
- **P1 (NOUVEAU)** : Verifier sur GitHub Actions que le workflow
  `generate-animation.yml` consomme bien `assets/audio_cache/*.mp3`
  sans avoir besoin de la cle LLM (compte Free Tier bloque)
- **P1** : Tester `generate-video.yml` (workflow_dispatch) avec
  `enable_translation=true`, langues FR/EN/ES/DE par defaut
  -> la traduction peut encore consommer du budget LLM, a surveiller
- **P1** : Verifier que la video generee est bien lisible sur YouTube/
  Facebook/LinkedIn et que les SRT s'activent bien en CC multilingue
- **P2** : Ajouter les formats portrait 9:16 (TikTok/Reels/Shorts) et
  carre 1:1 (Instagram feed) via le meme pipeline
- **P2** : Affiner les seuils de detection `looks_like_calc()` si certains
  blocs sont mal classes
- **P2** : Support optionnel `@ILLUSTRATION: ID` explicite
- **P2** : Refactoring : decouper `generate_animation.py` en modules
  (`parser.py`, `renderer_html.py`, `renderer_pdf.py`, `tts.py`)
- **P2** : Envisager Git LFS pour `assets/audio_cache/` si le repo devient
  trop lourd (actuellement +94 MB, repo total ~176 MB)

## Session 2026-05-01 (finalisation audio cache)
- Genere les **29/29 MP3** (voix shimmer FR) en local depuis l'Emergent Pod
  (user a recharge le Universal Key : budget +10 credits)
- Commit dans `assets/audio_cache/` (94 MB, 29 fichiers + README)
- `scripts/generate_animation.py` : prioritise le cache du repo avant tout
  appel API (robuste au 403 Free Tier sur GitHub Actions)
- `scripts/generate_video.py` : `find_audio_for_scene()` cherche aussi dans
  le cache du repo
- Workflow `generate-animation.yml` : retire le fail-hard sur `_CLE`
  manquant, active TTS par defaut, step diagnostique 'Check audio cache'
- Tests pytest : **11/11 passent**
- Test en conditions GitHub Actions simulees (cle LLM vide) :
  -> 29 audios charges depuis cache, HTML genere, 0 appel API
- Commit final : `55aaf3d` (a pusher via 'Save to Github')

## Integrations 3rd party
- OpenAI GPT-4o-mini (traductions sous-titres) -- via Emergent LLM Key
- OpenAI GPT (textes Q&A) -- via Emergent LLM Key
- OpenAI TTS `tts-1-hd` voix `shimmer` -- via Emergent LLM Key
- ffmpeg 5.1.x (video encoding H.264 + AAC, burn-in subtitles)
- Pillow (rendu PNG des scenes)
- mutagen (lecture duree MP3)
- WeasyPrint (PDF)
- MathJax 3 (rendu LaTeX dans HTML)

## Credentials
- `EMERGENT_LLM_KEY` cote local / `_CLE` cote secrets GitHub Actions
