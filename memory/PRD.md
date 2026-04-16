# PRD - Theorie mathematique Philippe Thomas Savard

## Probleme original
Creer une banque de questions et reponses (Q&R) evolutive et intelligente stockee dans une base de donnees SQLite, utilisant une API LLM (Emergent LLM Key / GPT-4o) pour generer du contenu base sur des documents de theorie mathematique (LaTeX, Isabelle/HOL, PDF). Integrer la generation et la validation dans les workflows GitHub Actions (CI/CD) de maniere 100% autonome avec des taches planifiees (cron).

## Architecture
- Depot GitHub : `Theorie-mathematique-philippe-thomas-savard-2026`
- Sources : `src/tex/` (10 LaTeX), `src/hol/` (5+1 Isabelle/HOL), `src/pdf/` (14 PDF)
- Bases de donnees : `qa_bank/qa_bank.db` (Q&R), `qa_bank/corpus.db` (extraction)
- Scripts : `scripts/auto_generate_qa.py`, `scripts/generate_corpus_db.py`
- CI/CD : `.github/workflows/build.yml`, `auto-daily-qa.yml`
- Application : `Ia_geo_spec_prem_app_deplo/` (3 IAs collaboratives)

## Ce qui a ete implemente

### Phase 1 - Infrastructure CI/CD
- Workflows GitHub Actions (build, cron quotidien Q&R, propositions hebdomadaires, maintenance mensuelle)
- Scripts Python autonomes dans `scripts/`
- Correction syntaxe YAML

### Phase 2 - Qualite du contenu
- Script narratif V2 pragmatique
- Nettoyage massif du depot (254 Mo -> 56 Mo)
- README complet + Release v1.0.0

### Phase 3 - Intelligence documentaire
- Job `generate_corpus_db` dans `build.yml`
- `corpus.db` avec extraction complete
- `auto_generate_qa.py` V3 exploitant `corpus.db`

### Phase 4 - Arborescences avec schemas (2026-04-13)
- 4 fichiers Mermaid.js dans `src/arborescences_corpus/`
- Commit : `43a7a63`

### Phase 5 - Generalisation Philippot_Method.thy (2026-04-13)
- Nouvelle theorie `Philippot_Method.thy` ajoutee au depot
- ROOT mis a jour pour inclure la theorie
- Contenu :
  - Conservation de toutes les locales existantes (3-7 termes, len>=8)
  - Formule unifiee : explicit_sum(p, s) = Rs - accumulated(p, s)
  - Position de substitution : p = n-2 (3-7 termes), p = 6 (8+ termes)
  - Identites algebriques : factorisation, paire de queue simplifiee
  - Lemme telescopique par induction
  - Invariance du rapport spectral 1/k
  - Theoremes de validation pour toutes longueurs et etapes
  - Forme fermee de l'accumulation
  - Certaines preuves algebriques marquees `sorry` (necessitent sledgehammer)
- Commit : `702e49b`

## Backlog
- P1 : Completer les preuves `sorry` dans Philippot_Method.thy via sledgehammer
- P1 : Surveiller qualite generation quotidienne Q&R avec corpus.db
- P2 : Ameliorer l'application web des 3 IAs collaboratives
