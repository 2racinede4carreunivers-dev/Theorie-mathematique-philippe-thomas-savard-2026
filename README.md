# Theorie Mathematique de l'Univers est au Carre

![Build Isabelle + LaTeX](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026/actions/workflows/build.yml/badge.svg)
![Auto QR Quotidien](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026/actions/workflows/auto-daily-qa.yml/badge.svg)
![Propositions Hebdomadaires](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026/actions/workflows/auto-weekly-proposals.yml/badge.svg)
![Maintenance Mensuelle](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026/actions/workflows/auto-monthly-maintenance.yml/badge.svg)

---

## Introduction

Ce depot est le depot officiel de la **theorie mathematique de Philippe Thomas Savard : L'Univers est au Carre**. Il reunit l'ensemble de la documentation, des preuves formelles et des outils associes a cette theorie originale.

La theorie est presentee a travers plusieurs chapitres :

1. **La geometrie du spectre des nombres premiers** -- Etude de la distribution des nombres premiers a travers des methodes geometriques originales, aboutissant a une axiomatisation du rapport spectral.
2. **La mecanique harmonique du chaos discret** -- Demonstration de l'invariance geometrique a travers des configurations de figures emboitees et des unites admissibles.
3. **Le postulat unique de l'univers est au carre** -- La methode du squaring, acte fondamental de la theorie qui eleve le perimetre d'un rectangle au rang de nouveau perimetre.
4. **L'espace de Philippot** -- Construction d'un espace geometrique pyramidal fonde sur la spirale de Theodore de Cyrene, unifiant disques, nombres hypercomplexes et volumes.

D'autres chapitres seront ajoutes au fil du temps a mesure que la theorie evolue.

---

## Contenu du depot

### Documents source et compiles

| Type | Nombre | Description |
|------|--------|-------------|
| `.tex` | 7 fichiers | Source LaTeX des chapitres de la theorie |
| `.thy` | 5 fichiers | Preuves formelles Isabelle/HOL validant les propositions mathematiques |
| `.pdf` | 7 fichiers | Documents compiles par le build du workflow |

### Guides d'utilisation

Plusieurs guides sont fournis dans `docs/guides/` pour permettre a tout utilisateur de reproduire les resultats presentes dans les chapitres :

- **Guide de compilation** (`guide_compilation.md`) -- Instructions pour compiler les fichiers LaTeX et Isabelle
- **Guide HOL** (`guide_HOL.md`) -- Utilisation des preuves formelles Isabelle/HOL
- **Guide IA** (`guide_IA.md`) -- Fonctionnement du systeme de questions/reponses intelligent
- **Guide de contribution** (`guide_contribution.md`) -- Comment contribuer au depot
- **Guide Python Q&R** (`guide_python_qa`) -- Fonctionnement des scripts de la banque evolutive
- **Guide de securite** (`guide_securite.md`) -- Politique de securite du depot

### Arborescences et coherence

L'arborescence de tous les fichiers `.pdf` et `.thy` est incluse dans `src/` (12 fichiers `arborescence_*.md`), demontrant :

- La coherence du corpus Isabelle genere par le build du workflow
- La coherence de chacun des chapitres attestes par le build de la session HOL d'Isabelle
- La base de donnees de ce corpus est disponible dans l'explorateur du depot (`archive/`)

### Illustrations

Le depot contient pres d'une centaine d'illustrations variees sur la theorie de l'univers est au carre, presentes dans les PDF, les fichiers `.tex` et le dossier `assets/` (81 images).

### Script narratif

Un script narratif decrivant la theorie et son contenu est disponible (`SCRIPT_NARRATIF.md`). Il a ete genere pour un projet en cours de creation : une animation presentant la theorie de A a Z.

### Application web -- 3 IA collaboratives

Le dossier `Ia_geo_spec_prem_app_deplo/` contient une application logiciel web integrant trois intelligences artificielles :

1. **IA Collaborative** -- Repond aux questions des utilisateurs en s'appuyant sur la documentation du depot
2. **IA Socratique** -- Guide l'utilisateur par le questionnement pour approfondir sa comprehension de la theorie
3. **IA Evolutive** -- Dotee d'une banque de Q&R evolutive qui s'ameliore par l'entrainement a chaque question posee par les utilisateurs

Les trois IA puisent l'information directement a la source du depot et sont mises a jour regulierement. La banque de Q&R de l'application evolue en meme temps que celle du depot puisque le logiciel web se met a jour avec le depot en temps reel.

Par souci de transparence, une mise a niveau est fournie a chaque question entre ce que dit la theorie et les spheres mathematiques et scientifiques dans le monde.

### Banque de questions/reponses evolutive

La banque est consultable dans `qa_bank/CATALOGUE.md`. Elle contient actuellement **56 Q&R validees** et continue de croitre automatiquement.

---

## Fonctionnement du Workflow

### Build principal (a chaque push sur `main`)

A chaque poussee d'un commit manuel, le workflow execute une compilation complete :

1. **Compilation LaTeX** -- Les fichiers `.tex` sont compiles par TexLive pour generer les `.pdf`
2. **Compilation Isabelle** -- Les fichiers `.thy` sont compiles par Isabelle 2024. Une attestation pour le corpus Isabelle est generee, produisant une base de donnees certifiant la coherence logique et que les propositions mathematiques avancees dans les theoremes sont soutenues (voir les arborescences des 5 fichiers `.thy`)
3. **Attestation SLSA** -- Chacun des 19 fichiers (`.pdf`, `.thy`, `.tex`) est certifie et une attestation cryptographique SLSA est generee, garantissant la provenance et l'integrite
4. **Generation de Q&R** -- A chaque commit, une question et sa reponse sont generees et ajoutees a la banque evolutive intelligente du depot

La banque de Q&R est evolutive et devient toujours plus complexe dans son questionnement et ses reponses a mesure que les mises a jour du depot s'effectuent.

### Workflows automatises

| Workflow | Frequence | Description |
|----------|-----------|-------------|
| **Q&R Quotidien** | 3 fois par jour (6h, 12h, 18h UTC) | Generation automatique de Q&R avec rotation sur les 12 fichiers source |
| **Propositions Hebdomadaires** | Vendredi 14h UTC | Analyse de la banque Q&R et proposition d'ameliorations pour un fichier `.tex` ou `.thy` |
| **Maintenance Mensuelle** | 1er du mois 9h UTC | Rapport de coherence, statistiques du depot et recommandations |

---

## Utilisation du depot

### Licence Apache 2.0

Ce depot est distribue sous la licence **Apache 2.0**. Les utilisateurs peuvent :

- **Consulter** et **cloner** le depot
- **Contribuer** via des pull requests (1 approbation requise, revue par proprietaire du code)
- **Partager** et **redistribuer** le depot ou ses versions modifiees
- **Modifier** le code source et les documents a des fins personnelles

Les conditions completes sont definies dans le fichier [LICENSE](LICENSE).

### Securite et integrite

- Chaque build genere une empreinte cryptographique **SHA-256** pour tous les documents
- Les attestations **SLSA** garantissent que les fichiers proviennent exclusivement de la branche `main`
- L'historique lineaire est obligatoire, le force-push est interdit
- Seule la branche `main` est supportee et authentifiee

Pour signaler une vulnerabilite, ne pas creer d'issue publique. Contacter : **philippethomassavard@gmail.com**

La politique de securite complete est disponible dans [SECURITY.md](.github/SECURITY.md).

### Cloner le depot

```bash
git clone https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git
```

---

## Structure du depot

```
.github/workflows/          4 workflows (build + 3 automatises)
.github/SECURITY.md         Politique de securite
src/tex/                    7 fichiers source LaTeX
src/hol/                    5 preuves formelles Isabelle/HOL
src/pdf/                    7 PDF compiles + references
src/arborescence_*.md       12 arborescences de coherence
assets/                     ~81 illustrations de la theorie
scripts/                    Scripts Python (generation Q&R, maintenance)
qa_bank/                    Banque Q&R evolutive (SQLite + catalogue)
docs/guides/                6 guides d'utilisation
proposals/                  Propositions d'amelioration hebdomadaires
archive/                    Base de donnees du corpus Isabelle
Ia_geo_spec_prem_app_deplo/ Application web 3 IA collaboratives
SCRIPT_NARRATIF.md          Script narratif pour animation video
CHANGELOG.md                Journal des modifications
LICENSE                     Licence Apache 2.0
```

---

*Theorie mathematique de Philippe Thomas Savard -- L'Univers est au Carre -- 2026*
