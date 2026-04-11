Mécanique harmonique du chaos discret
│
├── Préambule
│     ├── Contexte de création
│     ├── Liberté intellectuelle
│     └── Absence de formation académique (positionnement épistémologique)
│
├── I. Figure de la mécanique harmonique du chaos discret
│     ├── 1.1 Produit alternatif pour l’unité √2 + 1
│     │     ├── Relations géométriques (AL, JK, BE, LF)
│     │     ├── Égalités structurelles
│     │     └── Détermination de l’unité via arcsin
│     ├── 1.2 Produit alternatif pour l’unité √3 + 1
│     │     ├── Nouvelle configuration
│     │     ├── Relations analogues
│     │     └── Unité déterminée par l’angle 22.844°
│     ├── 1.3 Produit alternatif pour l’unité √5 + 1
│     │     ├── Structure plus complexe
│     │     └── Angle 19.132° et unité √5 + 1
│     ├── 1.4 Lecture des trois exemples d’unités p + 1
│     │     ├── √2 + 1 : cohérence structurelle
│     │     ├── √3 + 1 : invariance relationnelle
│     │     └── √5 + 1 : persistance de la loi universelle
│     └── 1.5 Invariance géométrique et lien avec Isabelle/HOL
│           ├── base_length(n,p)
│           ├── height_length(n,p)
│           ├── ratio_halfbase_height(n,p)
│           ├── Axiome ratio_axiom
│           ├── Segment AL_nat(p)
│           └── Invariance : geometric_unit(p) = √p + 1
│
├── II. Exemple complet : Construction des trois matrices
│     ├── 2.1 Matrice M1 — mesures du plan
│     │     ├── Coefficients C1…C9
│     │     ├── Lignes R1, R2, R3
│     │     └── Relations pondérées (diam_eq, u1.5, u3.375)
│     ├── 2.2 Matrice M2 — matrice de transition
│     │     ├── Version symbolique de M1
│     │     ├── Relations structurelles
│     │     └── Indépendance des valeurs numériques
│     ├── 2.3 Matrice M3 — matrice à dérivée première simplifiée
│     │     ├── Coefficients premiers (37, 31, 29…)
│     │     ├── Ponderations 7/k
│     │     └── Inconnue unique u = √3.375
│     ├── 2.4 Comment construire les trois matrices
│     │     ├── M1 : géométrie brute
│     │     ├── M2 : abstraction relationnelle
│     │     └── M3 : normalisation arithmétique
│     └── 2.5 Facteur trigonométrique alternatif
│           ├── Définition F(p)
│           ├── Domaine de définition
│           ├── Forme fermée
│           ├── Monotonie décroissante
│           ├── Comportement asymptotique
│           └── Produit alternatif sur les nombres premiers
│
├── III. Script Isabelle/HOL (référence)
│     └── Structure complète du fichier mecanique_discret.thy
│
├── IV. Conclusion
│     ├── Synthèse de la mécanique harmonique
│     ├── Rôle des unités √p + 1
│     ├── Invariance géométrique
│     └── Structure matricielle profonde
│
└── V. Licence Apache 2.0
