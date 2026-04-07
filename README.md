# Theorie Mathematique Philippe Thomas Savard 2026

![Build Isabelle + LaTeX](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026/actions/workflows/build.yml/badge.svg)
![Auto QR Quotidien](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026/actions/workflows/auto-daily-qa.yml/badge.svg)
![Propositions Hebdomadaires](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026/actions/workflows/auto-weekly-proposals.yml/badge.svg)
![Maintenance Mensuelle](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026/actions/workflows/auto-monthly-maintenance.yml/badge.svg)

---

Depot officiel de la documentation de la theorie mathematique de Philippe Thomas Savard. Ce depot contient les fichiers source LaTeX (`.tex`), les preuves formelles Isabelle/HOL (`.thy`) et les PDF compiles.

## Structure du depot

```
src/tex/        Fichiers source LaTeX
src/hol/        Preuves formelles Isabelle/HOL
src/pdf/        PDF compiles (generes par le build)
scripts/        Scripts Python (generation Q&R, maintenance)
qa_bank/        Banque de questions/reponses (SQLite)
proposals/      Propositions d'amelioration hebdomadaires
```

## Workflows automatiques

| Workflow | Frequence | Description |
|----------|-----------|-------------|
| **Build** | A chaque push sur `main` | Compile Isabelle + LaTeX, genere les PDF, attestation SLSA |
| **Q&R Quotidien** | 3x/jour (6h, 12h, 18h UTC) | Genere 1 question/reponse par execution (rotation de 12 fichiers) |
| **Propositions** | Vendredi 14h UTC | Propose des ameliorations pour 1 fichier .tex/.thy |
| **Maintenance** | 1er du mois 9h UTC | Rapport de coherence et maintenance du depot |

## Banque Q&R evolutive

Le systeme genere automatiquement des questions et reponses a partir du contenu mathematique du depot. La banque est stockee dans `qa_bank/qa_bank.db` (SQLite) et s'enrichit a chaque execution des workflows.

## Licence

Voir [LICENSE](LICENSE)
