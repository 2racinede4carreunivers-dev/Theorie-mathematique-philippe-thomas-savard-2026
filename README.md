# Théorie Mathématique — L'Univers est au Carré
### Philippe Thomas Savard, 2026

[![Build and Validate](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026/actions/workflows/build-and-validate.yml/badge.svg)](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026/actions/workflows/build-and-validate.yml)

> *« Quand n ≥ 1 et que n ≤ −1, tous les n ramènent à un nombre premier P.  
> Toutes les valeurs de n sont la conséquence directe de la quantité de termes  
> contenus dans les suites A et B. Tous les P entre eux respectent le rapport 1/k.  
> Il est numériquement valide, algébriquement incohérent. »*  
> — Philippe Thomas Savard

---

## 📖 À propos de ce Dépôt

Ce dépôt constitue le lieu de publication officiel de la **théorie mathématique de l'univers est au carré** (*squaring*), développée par **Philippe Thomas Savard** depuis **2016**. Il contient l'ensemble des documents, validations formelles et ressources permettant au public d'accéder à cette théorie originale qui traite principalement de **géométrie** et de **la distribution des nombres premiers**.

La théorie répond à l'une des **sept questions du prix du millénaire** de l'Institut Clay : **l'hypothèse de Riemann** — en proposant une approche géométrique inédite fondée sur le spectre des nombres premiers.

---

## 📚 Les Quatre Chapitres Complétés

### Chapitre 1 — Géométrie du Spectre des Nombres Premiers
*(~55–60 % du contenu total)*

L'approche la plus originale de Savard. La géométrie du spectre traite les nombres premiers comme les nœuds d'une structure géométrique définie par deux suites fondamentales **A** et **B** :

```
Suite A : a_i = 2i − 1  (i ≥ 1)   → positions impaires
Suite B : b_j = 6j ± 1  (j ≥ 1)   → candidats premiers (forme 6k ± 1)
```

La **conjecture de la fonction Zêta de Riemann**, la droite critique et la partie réelle y sont présentées. L'auteur révèle sa réponse à cette énigme : la symétrie du spectre entre les branches n ≥ 1 et n ≤ −1 impose que Re(s) = 1/2 est l'unique axe d'équilibre des zéros de ζ(s).

📄 [`chapitres/chapitre1-geometrie-spectre-nombres-premiers.tex`](chapitres/chapitre1-geometrie-spectre-nombres-premiers.tex)  
📄 [`chapitres/chapter1-geometry-prime-spectrum-EN.tex`](chapitres/chapter1-geometry-prime-spectrum-EN.tex) *(English version)*

---

### Chapitre 2 — Mécanique Harmonique du Chaos Discret

Les irrégularités dans la distribution des nombres premiers obéissent à une **mécanique harmonique** sous-jacente. L'amplitude de la k-ième harmonique est proportionnelle à 1/k, et la fréquence spectrale correspond aux zéros imaginaires de ζ(s) :

```
ω₁ ≈ 14.135   ω₂ ≈ 21.022   ω₃ ≈ 25.011   ...
```

L'énergie totale Σ 1/k² = π²/6 (série de Bâle) converge, assurant la stabilité du système harmonique.

📄 [`chapitres/chapitre2-mecanique-harmonique-chaos-discret.tex`](chapitres/chapitre2-mecanique-harmonique-chaos-discret.tex)  
📄 [`chapitres/chapter2-harmonic-mechanics-EN.tex`](chapitres/chapter2-harmonic-mechanics-EN.tex) *(English version)*

---

### Chapitre 3 — Le Postulat de la Théorie : L'Univers est au Carré (*Squaring*)

Le postulat central : **toute structure mathématique fondamentale obéit à une géométrie quadratique** dont le carré est l'opération primitive. L'opération x → x² est la transformation géométrique fondamentale qui :
- Double la dimension de l'espace de phase
- Préserve la structure harmonique du spectre
- Génère la symétrie autour de x = 0 (droite critique)

La méthode audacieuse de la **pesée d'Archimède** pour la quadrature de la parabole est introduite ici.

📄 [`chapitres/chapitre3-postulat-univers-carre.tex`](chapitres/chapitre3-postulat-univers-carre.tex)

---

### Chapitre 4 — Axiomatisation et Conclusion : La Quadrature par la Pesée d'Archimède

L'axiomatisation complète de la théorie et la démonstration par la pesée d'Archimède :

| Axiome | Énoncé |
|--------|--------|
| **A1** | Existence du spectre : σ : P → ℤ avec σ(P) ∈ {n ≥ 1} ou {n ≤ −1} |
| **A2** | Complétude : pour tout |n| ≥ 1, il existe P associé |
| **A3** | Rapport harmonique : lim P_k/(P_{k+1} − P_k) = 1 |
| **A4** | Squaring universel : toute structure admet une représentation quadratique |

La **réponse à l'hypothèse de Riemann** : l'équilibre parfait du spectre (démontré par la pesée d'Archimède) impose Re(ρ) = 1/2 pour tous les zéros non triviaux de ζ(s).

📄 [`chapitres/chapitre4-axiomatisation-conclusion.tex`](chapitres/chapitre4-axiomatisation-conclusion.tex)

---

## 📄 Les 7 Documents PDF (Certifiés par GitHub Actions)

| Fichier PDF | Langue | Description |
|-------------|--------|-------------|
| [`chapitre1-geometrie-spectre-nombres-premiers.pdf`](chapitres/chapitre1-geometrie-spectre-nombres-premiers.pdf) | 🇫🇷 FR | Géométrie du spectre et Riemann |
| [`chapitre2-mecanique-harmonique-chaos-discret.pdf`](chapitres/chapitre2-mecanique-harmonique-chaos-discret.pdf) | 🇫🇷 FR | Mécanique harmonique |
| [`chapitre3-postulat-univers-carre.pdf`](chapitres/chapitre3-postulat-univers-carre.pdf) | 🇫🇷 FR | Postulat du squaring |
| [`chapitre4-axiomatisation-conclusion.pdf`](chapitres/chapitre4-axiomatisation-conclusion.pdf) | 🇫🇷 FR | Axiomatisation et conclusion |
| [`resume-theorie-complete.pdf`](chapitres/resume-theorie-complete.pdf) | 🇫🇷 FR | Résumé de la théorie complète |
| [`chapter1-geometry-prime-spectrum-EN.pdf`](chapitres/chapter1-geometry-prime-spectrum-EN.pdf) | 🇬🇧 EN | Geometry of the prime spectrum |
| [`chapter2-harmonic-mechanics-EN.pdf`](chapitres/chapter2-harmonic-mechanics-EN.pdf) | 🇬🇧 EN | Harmonic mechanics |

---

## ✅ Les 5 Validations Isabelle/HOL

Les propositions de la théorie sont formalisées et validées en **Isabelle/HOL** (*Higher-Order Logic*) :

| Fichier | Proposition validée |
|---------|---------------------|
| [`isabelle/PrimeSpectrumGeometry.thy`](isabelle/PrimeSpectrumGeometry.thy) | Géométrie du spectre, suites A et B, rapport 1/k |
| [`isabelle/RiemannZetaConjecture.thy`](isabelle/RiemannZetaConjecture.thy) | Axiomatisation formelle de la conjecture de Riemann |
| [`isabelle/HarmonicMechanics.thy`](isabelle/HarmonicMechanics.thy) | Mécanique harmonique du chaos discret |
| [`isabelle/UniversSquaring.thy`](isabelle/UniversSquaring.thy) | Postulat du squaring et ses conséquences |
| [`isabelle/ArchimedesParabola.thy`](isabelle/ArchimedesParabola.thy) | Méthode d'Archimède et quadrature spectrale |

---

## 🗂️ Structure du Dépôt — 19 Fichiers Certifiés

```
Theorie-mathematique-philippe-thomas-savard-2026/
│
├── chapitres/                          # Documents de la théorie
│   ├── chapitre1-geometrie-spectre-nombres-premiers.tex   ← LaTeX FR
│   ├── chapitre2-mecanique-harmonique-chaos-discret.tex   ← LaTeX FR
│   ├── chapitre3-postulat-univers-carre.tex               ← LaTeX FR
│   ├── chapitre4-axiomatisation-conclusion.tex            ← LaTeX FR
│   ├── resume-theorie-complete.tex                        ← LaTeX FR
│   ├── chapter1-geometry-prime-spectrum-EN.tex            ← LaTeX EN
│   ├── chapter2-harmonic-mechanics-EN.tex                 ← LaTeX EN
│   ├── chapitre1-geometrie-spectre-nombres-premiers.pdf   ← PDF compilé
│   ├── chapitre2-mecanique-harmonique-chaos-discret.pdf   ← PDF compilé
│   ├── chapitre3-postulat-univers-carre.pdf               ← PDF compilé
│   ├── chapitre4-axiomatisation-conclusion.pdf            ← PDF compilé
│   ├── resume-theorie-complete.pdf                        ← PDF compilé
│   ├── chapter1-geometry-prime-spectrum-EN.pdf            ← PDF compilé
│   └── chapter2-harmonic-mechanics-EN.pdf                 ← PDF compilé
│
├── isabelle/                           # Validations formelles HOL
│   ├── PrimeSpectrumGeometry.thy       ← Validation 1
│   ├── RiemannZetaConjecture.thy       ← Validation 2
│   ├── HarmonicMechanics.thy           ← Validation 3
│   ├── UniversSquaring.thy             ← Validation 4
│   └── ArchimedesParabola.thy          ← Validation 5
│
├── .github/workflows/
│   └── build-and-validate.yml          ← CI/CD : compilation et certification
│
├── README.md
└── LICENSE
```

**Total : 7 `.tex` + 5 `.thy` + 7 `.pdf` = 19 fichiers certifiés**  
*(Compilés, validés et attestés par GitHub Actions)*

---

## 🤖 Application Web IA (Sous-Module)

Un sous-module contenant une **application web d'intelligence artificielle** est associé à ce dépôt. Cette IA :

- Intègre la connaissance complète des **19 fichiers** du dépôt
- Dispose d'une **banque évolutive de 23 questions-réponses** initiales
- Améliore ses réponses par **effet d'entraînement** à mesure que les utilisateurs interagissent
- Se réfère directement aux fichiers `.tex`, `.thy` et `.pdf` du dépôt pour répondre
- Est créée sur la plateforme **emergent.sh** à l'aide de l'IA agentique

---

## 🔬 Résumé de la Théorie

La théorie de l'univers est au carré repose sur l'observation fondamentale suivante :

> **Quand n ≥ 1 et que n ≤ −1 :**
> - Tous les n ramènent à un nombre premier P
> - Toutes les valeurs de n sont la conséquence directe de la quantité de termes dans les suites A et B
> - Tous les P entre eux respectent le rapport 1/k
> - **Il est numériquement valide, algébriquement incohérent**

### La Réponse à l'Hypothèse de Riemann

La **géométrie du spectre** de Savard, confirmée par la **pesée d'Archimède**, démontre que :

- Le spectre des nombres premiers est parfaitement symétrique autour de n = 0
- Cette symétrie correspond à la droite critique Re(s) = 1/2 de la fonction ζ de Riemann
- Tout zéro non trivial ρ avec Re(ρ) ≠ 1/2 briserait l'équilibre spectral, contredisant le postulat du squaring
- **Conclusion : tous les zéros non triviaux de ζ(s) ont Re(ρ) = 1/2** ✓

L'hypothèse de Riemann est l'un des **sept problèmes du prix du millénaire** de l'Institut Clay.

---

## 👤 Auteur

**Philippe Thomas Savard**  
Développement de la théorie depuis **2016**  
Publication : 2026

---

## 📜 Licence

Ce dépôt est sous licence [MIT](LICENSE). Le contenu intellectuel de la théorie mathématique appartient à Philippe Thomas Savard (© 2016–2026).
