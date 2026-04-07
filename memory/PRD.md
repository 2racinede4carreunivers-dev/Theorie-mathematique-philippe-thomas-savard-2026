# PRD - Banque Q&R Evolutive Intelligente
## Theorie Mathematique Philippe Thomas Savard 2026

### Enonce du Probleme
Concevoir une banque de questions/reponses evolutive et intelligente pour un depot GitHub de documentation mathematique. Le systeme doit generer automatiquement des Q&R a partir des fichiers .tex, .thy et .pdf du depot en utilisant une API LLM, et s'integrer dans les workflows CI/CD GitHub Actions.

### Architecture
```
/repo_savard/
├── .github/workflows/
│   ├── build.yml                      (CI principal: Isabelle + LaTeX + Q&R)
│   ├── auto-daily-qa.yml             (Cron 3x/jour: 6h, 12h, 18h UTC)
│   ├── auto-weekly-proposals.yml     (Cron vendredi 14h UTC)
│   └── auto-monthly-maintenance.yml  (Cron 1er du mois 9h UTC)
├── scripts/
│   ├── qa_database.py                (Gestionnaire SQLite)
│   ├── qa_generator.py               (Generateur LLM)
│   ├── qa_validator.py               (Validateur CLI interactif)
│   ├── qa_config.py                  (Configuration)
│   ├── qa_wolfram.py                 (Integration Wolfram)
│   ├── auto_generate_qa.py           (Script quotidien, rotation 12 fichiers)
│   ├── auto_weekly_proposals.py      (Script hebdomadaire)
│   └── auto_monthly_maintenance.py   (Script mensuel)
├── qa_bank/
│   └── qa_bank.db                    (Base SQLite)
└── src/ (tex/, hol/, pdf/)
```

### Schema DB (SQLite)
- `qa_validated`: Q&R validees (question, answer, category, subcategory, difficulty, language, tags, source_files, source_commit, created_at, quality_score, hash_signature, metadata)
- `qa_pending`: Q&R en attente de validation
- `learned_patterns`: Patterns appris (pattern_type, pattern_value UNIQUE, success_rate, usage_count)
- `key_concepts`: Concepts cles extraits

### Integrations
- **Emergent Universal Key** (OpenAI GPT-4o) via `emergentintegrations` SDK
- Secret GitHub: `${{ secrets._CLE }}`

### Ce qui est implemente
- [x] Base de donnees SQLite avec schema complet
- [x] Generateur Q&R avec LLM (qa_generator.py)
- [x] Validateur CLI interactif (qa_validator.py)
- [x] Integration dans build.yml (job generate_qa)
- [x] Workflow quotidien auto-daily-qa.yml (3x/jour, rotation 12 fichiers)
- [x] Workflow hebdomadaire auto-weekly-proposals.yml (propositions .tex/.thy)
- [x] Workflow mensuel auto-monthly-maintenance.yml (rapport maintenance)
- [x] Scripts autonomes Python pour tous les workflows cron
- [x] Correction SSL pour telechargement Isabelle
- [x] Contrainte UNIQUE sur learned_patterns
- [x] Fallback created_at dans auto_weekly_proposals.py
- [x] Correction heredoc YAML dans build.yml (printf au lieu de cat << EOF)
- [x] Correction espace secrets._CLE dans build.yml
- [x] Validation YAML: 4/4 workflows passent le parseur

### Backlog
- [ ] P0: Pousser les fichiers modifies vers GitHub (Save to GitHub)
- [ ] P1: Tester les workflows via workflow_dispatch sur GitHub Actions
- [ ] P2: Surveiller les cron jobs automatiques une fois actifs
- [ ] P3: Ameliorations futures selon retours utilisateur
