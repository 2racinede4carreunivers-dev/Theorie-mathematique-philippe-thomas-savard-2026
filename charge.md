/
├── .github/
│   ├── workflows/
│   │   ├── compile_tex.yml
│   │   ├── compile_thy.yml
│   │   ├── attestations.yml
│   │   └── release.yml
│   └── SECURITY.md
│
├── docs/
│   ├── guides/
│   │   ├── guide_compilation.md
│   │   ├── guide_IA.md
│   │   ├── guide_HOL.md
│   │   ├── guide_securite.md
│   │   └── guide_contribution.md
│   ├── architecture/
│   │   ├── charge.md
│   │   └── blueprint.md
│   └── index.md
│
├── src/
│   ├── tex/
│   │   ├── postulat_univers_carre.tex
│   │   ├── geometrie_du_spectre_premier.tex
│   │   ├── mecanique_chaos_discret.tex
│   │   ├── pilosophy_geometry_of_prime_number.tex
│   │   ├── prime_specrtrum_geometry.tex
│   │   ├── telosemantique_analogiste_spectre_premier.tex
│   │   └── autres_documents.tex
│   │
│   ├── hol/
│   │   ├── postulat_carre.thy
│   │   ├── methode_spectral.thy
│   │   ├── methode_de_philippot.thy
│   │   ├── mecanique_discret.thy
│   │   ├── espace_philippot.thy
│   │   └── autres_theories.thy
│   │
│   └── pdf/
│       ├── postulat_univers_carre.pdf
│       ├── geometrie_du_spectre_premier.pdf
│       └── autres_documents.pdf
│
├── app/   # sous-module IA
│
├── scripts/
│   ├── note.sh
│   ├── build_all.sh
│   ├── clean.sh
│   └── versioning.sh
│
├── assets/
│   ├── images/
│   │   ├── espace_philippot.png
│   │   ├── quadrature_parabole_zero_critique.png
│   │   └── autres_images.png
│   └── illustrations/
│
├── archive/
│
├── .gitignore
├── .gitmodules
├── CHANGELOG.md
├── README.md
└── LICENSE
# Cahier des charges — Dépôt « Univers au carré » (v2)

## 1. Vision et objectifs

### 1.1. Vision générale

Le dépôt a pour but de rendre accessible au public intéressé par les mathématiques, la géométrie et la connaissance, la théorie de « L’univers est au carré ».  
Il sert à :

- partager un travail personnel sérieux, même hors cadre académique ;
- offrir des documents lisibles (PDF, LaTeX, images) ;
- fournir des validations formelles (Isabelle/HOL) ;
- permettre la **reproduction** des résultats par d’autres.

### 1.2. Objectifs principaux

- **O1 — Accessibilité :** permettre à toute personne curieuse de consulter les documents, les images et les guides.
- **O2 — Reproductibilité :** fournir des instructions et des workflows permettant de reproduire les compilations LaTeX et Isabelle/HOL.
- **O3 — Attestation :** garantir que les artefacts (PDF, .thy) ont été compilés et certifiés par GitHub Actions, via des rapports SLSA.
- **O4 — Traçabilité :** documenter les changements via un CHANGELOG et un script `note.sh`.
- **O5 — Clarté méthodologique :** centraliser la méthode dans un fichier de méthodologie (type « livre de recettes »).
- **O6 — Sécurité et licence :** préciser clairement les droits, limites et responsabilités (Apache 2.0 + SECURITY).

---

## 2. Périmètre documentaire

### 2.1. Documents scientifiques

Le dépôt contiendra entre **16 et 19 documents**, répartis en :

- **6–7 fichiers LaTeX (.tex)**  
  - ex. : `postulat_univers_carre.tex`, `geometrie_du_spectre_premier.tex`, etc.
- **6–7 fichiers PDF (.pdf)**  
  - versions compilées des .tex.
- **4–5 fichiers Isabelle/HOL (.thy)**  
  - ex. : `postulat_carre.thy`, `methode_spectral.thy`, `methode_de_philippot.thy`, `mecanique_discret.thy`, `espace_philippot.thy` (optionnel selon inclusion immédiate ou ultérieure).

### 2.2. Illustrations

- Plusieurs fichiers `.png` (schémas, figures, illustrations) seront inclus dans `assets/images/`.
- Ces images sont utilisées dans les PDF et servent aussi de support explicatif dans les guides.

### 2.3. Guides et documentation

Le dépôt contiendra :

- **5 à 7 guides d’utilisation** (Markdown), un par document ou groupe de documents, expliquant :
  - comment reproduire les résultats ;
  - comment lancer les compilations ;
  - comment interpréter les sorties.
- Un **fichier de méthodologie** (Markdown) décrivant, de manière formalisée, la méthode utilisée pour chaque PDF :
  - objectifs ;
  - étapes ;
  - outils ;
  - structure des preuves et calculs.

---

## 3. Architecture du dépôt

### 3.1. Structure générale

```text
/
├── .github/workflows/      # Workflows GitHub Actions (build, attestations, release)
├── app/                    # Sous-module IA (application web, 3 IA)
├── archive/                # Archives, versions anciennes
├── assets/images/          # Illustrations (.png)
├── docs/
│   ├── architecture/       # charge.md, éventuellement blueprint.md
│   └── guides/             # Guides d’utilisation (Markdown)
├── scripts/                # Scripts utilitaires (note.sh, build_all.sh, etc.)
├── src/
│   ├── tex/                # Sources LaTeX (.tex)
│   ├── pdf/                # PDF générés
│   └── hol/                # Théories Isabelle/HOL (.thy)
├── CHANGELOG.md
├── README.md
├── SECURITY.md
├── LICENSE                 # Apache 2.0
├── .gitignore
└── .gitmodules
