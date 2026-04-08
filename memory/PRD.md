# PRD - Banque Q&R Evolutive Intelligente
## Theorie Mathematique Philippe Thomas Savard 2026

### Enonce du Probleme
Concevoir une banque de questions/reponses evolutive et intelligente pour un depot GitHub de documentation mathematique. Le systeme genere automatiquement des Q&R a partir des fichiers .tex, .thy et .pdf via une API LLM, integre dans les workflows CI/CD GitHub Actions.

### Architecture
```
/repo_savard/
├── .github/workflows/
│   ├── build.yml                      (CI principal: Isabelle + LaTeX + Q&R)
│   ├── auto-daily-qa.yml             (Cron 3x/jour: 6h, 12h, 18h UTC)
│   ├── auto-weekly-proposals.yml     (Cron vendredi 14h UTC)
│   └── auto-monthly-maintenance.yml  (Cron 1er du mois 9h UTC)
├── scripts/
│   ├── qa_database.py, qa_generator.py, qa_validator.py, qa_config.py, qa_wolfram.py
│   ├── auto_generate_qa.py           (Script quotidien v2 - sections aleatoires, 10 angles)
│   ├── auto_weekly_proposals.py      (Script hebdomadaire)
│   ├── auto_monthly_maintenance.py   (Script mensuel)
│   └── generate_script_narratif.py   (Generateur script video)
├── qa_bank/
│   ├── qa_bank.db                    (Base SQLite)
│   └── CATALOGUE.md                  (Catalogue lisible des Q&R)
├── SCRIPT_NARRATIF.md                (Script narratif video - 5 chapitres)
└── src/ (tex/, hol/, pdf/)
```

### Ce qui est implemente
- [x] Base de donnees SQLite avec schema complet
- [x] Generateur Q&R avec LLM (qa_generator.py)
- [x] Validateur CLI interactif (qa_validator.py)
- [x] Integration dans build.yml (job generate_qa)
- [x] Workflow quotidien (3x/jour, rotation 12 fichiers) - FONCTIONNE
- [x] Workflow hebdomadaire (propositions .tex/.thy) - YAML corrige
- [x] Workflow mensuel (rapport maintenance) - YAML corrige
- [x] Scripts Python autonomes pour tous les workflows cron
- [x] Correction SSL pour telechargement Isabelle
- [x] Correction heredoc YAML dans build.yml (printf)
- [x] Correction espace secrets._CLE dans build.yml
- [x] Push direct vers GitHub via token
- [x] Q&R variees v2 (sections aleatoires, 10 angles, toutes questions existantes)
- [x] Catalogue CATALOGUE.md auto-genere et consultable sur GitHub
- [x] Correction sous-module orphelin repo_savard (warning Actions)
- [x] Attestation SLSA limitee aux 19 fichiers de la theorie (plus de PDF Isabelle)
- [x] Script narratif complet (intro + 5 chapitres, ~3500 mots, ~23 min)

### Backlog
- [ ] P1: Surveiller les cron jobs automatiques
- [ ] P2: Ameliorations futures selon retours utilisateur
- [ ] P3: Potentiel diaporama/video automatise dans Actions
