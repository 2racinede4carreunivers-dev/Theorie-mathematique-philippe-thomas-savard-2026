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
│   ├── auto_generate_qa.py           (Script quotidien, rotation 12 fichiers)
│   ├── auto_weekly_proposals.py      (Script hebdomadaire)
│   └── auto_monthly_maintenance.py   (Script mensuel)
├── qa_bank/qa_bank.db                (Base SQLite)
└── src/ (tex/, hol/, pdf/)
```

### Ce qui est implemente
- [x] Base de donnees SQLite avec schema complet
- [x] Generateur Q&R avec LLM (qa_generator.py)
- [x] Validateur CLI interactif (qa_validator.py)
- [x] Integration dans build.yml (job generate_qa)
- [x] Workflow quotidien (3x/jour, rotation 12 fichiers) - FONCTIONNE (verif 07/04)
- [x] Workflow hebdomadaire (propositions .tex/.thy) - YAML corrige
- [x] Workflow mensuel (rapport maintenance) - YAML corrige
- [x] Scripts Python autonomes pour tous les workflows cron
- [x] Correction SSL pour telechargement Isabelle
- [x] Correction heredoc YAML dans build.yml (printf)
- [x] Correction espace secrets._CLE dans build.yml
- [x] Push direct vers GitHub via token (commit 8445be4) - 07/04/2026
- [x] Build declenche avec succes sur GitHub Actions

### Historique des corrections YAML (recurrent)
- Probleme: heredoc `python3 << 'EOF'` et `cat << 'EOF'` cassent le parseur YAML GitHub Actions
- Solution: scripts Python autonomes dans scripts/ + printf pour fichiers texte
- Applique 3 fois (les merges ecrasaient les corrections)
- Correction finale poussee directement via token GitHub le 07/04/2026

### Backlog
- [ ] P1: Verifier resultat final du build 8445be4 (en cours)
- [ ] P2: Surveiller les cron jobs automatiques
- [ ] P3: Ameliorations futures selon retours utilisateur
