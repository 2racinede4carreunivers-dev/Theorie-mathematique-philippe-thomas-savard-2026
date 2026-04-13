# PRD - Theorie mathematique Philippe Thomas Savard

## Probleme original
Creer une banque de questions et reponses (Q&R) evolutive et intelligente stockee dans une base de donnees SQLite, utilisant une API LLM (Emergent LLM Key / GPT-4o) pour generer du contenu base sur des documents de theorie mathematique (LaTeX, Isabelle/HOL, PDF). Integrer la generation et la validation dans les workflows GitHub Actions (CI/CD) de maniere 100% autonome avec des taches planifiees (cron).

## Architecture
- Depot GitHub : `Theorie-mathematique-philippe-thomas-savard-2026`
- Sources : `src/tex/` (10 LaTeX), `src/hol/` (5 Isabelle/HOL), `src/pdf/` (14 PDF)
- Bases de donnees : `qa_bank/qa_bank.db` (Q&R), `qa_bank/corpus.db` (extraction)
- Scripts : `scripts/auto_generate_qa.py`, `scripts/generate_corpus_db.py`
- CI/CD : `.github/workflows/build.yml`, `auto-daily-qa.yml`
- Application : `Ia_geo_spec_prem_app_deplo/` (3 IAs collaboratives)

## Ce qui a ete implemente

### Phase 1 - Infrastructure CI/CD
- Workflows GitHub Actions (build, cron quotidien Q&R, propositions hebdomadaires, maintenance mensuelle)
- Scripts Python autonomes dans `scripts/`
- Correction syntaxe YAML (inline Python → scripts autonomes)
- Attestation SLSA ciblee sur les 19 fichiers theoriques

### Phase 2 - Qualite du contenu
- Script narratif V2 pragmatique (`SCRIPT_NARRATIF.md`)
- Nettoyage massif du depot (254 Mo → 56 Mo)
- README complet + Release v1.0.0

### Phase 3 - Intelligence documentaire
- Job `generate_corpus_db` dans `build.yml` pour extraction automatique texte/structures
- `corpus.db` avec tables : files, hol_structure, tex_structure, pdf_structure, concepts
- `auto_generate_qa.py` V3 exploitant `corpus.db` pour Q&R riches en equations/preuves

### Phase 4 - Arborescences avec schemas (2026-04-13)
- 4 fichiers Mermaid.js dans `src/arborescences_corpus/` :
  - `arborescence_hol.md` : dependances HOL, locales, axiomes
  - `arborescence_latex.md` : relations documents, references croisees HOL
  - `arborescence_pdf.md` : pipeline compilation, correspondances source/PDF
  - `arborescence_globale.md` : flux CI/CD complet, interdependances 3 couches
- Commit : `43a7a63` pousse sur `main`

## Backlog
- P1 : Surveiller qualite generation quotidienne Q&R avec corpus.db
- P2 : Ameliorer l'application web des 3 IAs collaboratives
