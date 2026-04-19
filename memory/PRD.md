# PRD - Theorie mathematique Philippe Thomas Savard

## Probleme original
Creer une banque de Q&R evolutive et intelligente (SQLite + LLM GPT-4o) pour un corpus de theorie mathematique (LaTeX, Isabelle/HOL, PDF). CI/CD 100% autonome via GitHub Actions.

## Architecture
- Depot : `Theorie-mathematique-philippe-thomas-savard-2026`
- Sources : `src/tex/` (10), `src/hol/` (7 .thy), `src/pdf/` (11)
- DBs : `qa_bank/qa_bank.db`, `qa_bank/corpus.db`
- CI/CD : 5 workflows dans `.github/workflows/`
- Evaluation : `scripts/evaluation/academic_evaluation.py`

## Implemente

### Phase 1-3 (sessions precedentes)
- Infrastructure CI/CD complete
- corpus.db extraction, Q&R automatiques, nettoyage depot
- Arborescences Mermaid.js, README, Release v1.0.0

### Phase 4 (2026-04-13)
- Arborescences Mermaid.js (4 fichiers)

### Phase 5 (2026-04-13 - 2026-04-18)
- Philippot_Method.thy : generalisation complete (n termes, n etapes, 1/k)
- Versions v3-v6 : nettoyage Unicode complet, 100% ASCII

### Phase 6 (2026-04-19) - Systeme d'evaluation academique
- `scripts/evaluation/academic_evaluation.py` : 7 axes, score /100
- `.github/workflows/academic-evaluation.yml` : declenchement manuel
- `evaluation/RAPPORT_EVALUATION.md` : score preliminaire 85.5/100 (Grade A)
- `evaluation/RAPPORT_PREPARATOIRE.md` : liste complete des criteres
- `evaluation/grille_evaluation.json` : donnees brutes
- Cadre : K-State + HOL + MAV 2025 + CRM + Epistemologie
- Option LLM (GPT-4o) pour evaluation qualitative

## Backlog
- P0 : Completer les 8 sorry dans Philippot_Method.thy (gain +3-5 pts)
- P1 : Generer plus de Q&R pour qa_bank (gain +1.5 pts)
- P2 : Ajouter tactiques variees dans les .thy (gain +2 pts)
- P3 : Score potentiel apres corrections : 93-95/100 (Grade A+)
