# PRD - Theorie mathematique Philippe Thomas Savard

## Probleme original
Banque Q&R evolutive (SQLite + LLM GPT-4o) pour corpus mathematique (LaTeX, HOL, PDF). CI/CD GitHub Actions.

## Architecture
- Depot : `Theorie-mathematique-philippe-thomas-savard-2026`
- Sources : `src/tex/` (10), `src/hol/` (7 .thy), `src/pdf/` (10+)
- Evaluation : `scripts/evaluation/academic_evaluation.py` v2.0
- CI/CD : 5 workflows dont `academic-evaluation.yml` (manuel)

## Implemente
- Phase 1-3 : CI/CD, corpus.db, Q&R, nettoyage
- Phase 4 : Arborescences Mermaid.js
- Phase 5 : Philippot_Method.thy (remplace par infini_parti.thy)
- Phase 6 : Evaluation academique v2.0 - rapport peer-review detaille
  - 550+ lignes, fichier par fichier, 5 axes (K-State/Calgary/Greiffenhagen)
  - Justifications explicites pour chaque score
  - Methodologie, comparaison CRM, forces/faiblesses
  - Score : 74.3/100 (7 fichiers .thy, 0 sorry)
  - Option GPT-4o pour analyse qualitative

## Backlog
- P0 : Completer sorry dans Philippot_Method.thy pour le reintegrer
- P1 : Reduire axiomatisations pour augmenter le score
- P2 : Eliminer constantes flottantes
