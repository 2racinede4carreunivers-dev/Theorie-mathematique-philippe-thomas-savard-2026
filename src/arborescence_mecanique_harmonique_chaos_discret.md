mecanique_discret.thy
│
├── CHAPITRE A — Axiomatisation de la mécanique harmonique du chaos discret
│     │
│     ├── A1.0 Fondements géométriques
│     │     ├── A1.1 Unités admissibles : u(p) = sqrt(p) + 1
│     │     │     ├── prime_nat
│     │     │     ├── admissible_unit
│     │     │     └── unit
│     │     │
│     │     ├── A1.2 Carrés emboîtés et structure d’échelle 1.5^n
│     │     │     ├── type_synonym point
│     │     │     ├── side
│     │     │     ├── A, B(n), C(n), D(n)
│     │     │
│     │     ├── A1.3 Triangles inscrits et base paramétrique b(n,p)
│     │     │     ├── base_param
│     │     │     ├── P1(n,p)
│     │     │     └── P2(n,p)
│     │     │
│     │     ├── A1.4 Rapport fondamental demi-base / hauteur = sqrt(p)
│     │     │     ├── dist2
│     │     │     ├── base_length
│     │     │     ├── height_length
│     │     │     ├── ratio_halfbase_height
│     │     │     └── ratio_axiom  (axiome central)
│     │     │
│     │     ├── A1.5 Angle associé θ(p) = arctan(sqrt(p))
│     │     │     └── angle_rect
│     │     │
│     │     ├── A1.6 Unité géométrique via AL_nat
│     │     │     ├── AL_nat
│     │     │     ├── geometric_unit
│     │     │     ├── geometric_unit_eq_unit
│     │     │     ├── AL_nat_domain (axiome)
│     │     │     └── invariance_geometric_unit
│     │     │
│     │     └── A1.7 Axiome d’invariance géométrique
│     │
│     └── A2.0 Invariance et dynamique interne
│           ├── A2.1 Dépendance des longueurs à l’unité
│           ├── A2.2 Déplacement des segments
│           ├── A2.3 Invariance du produit alternatif
│           ├── A2.4 Diamètre équivalent LM
│           └── A2.5 Interprétation relationnelle (analogie relativiste)
│
├── CHAPITRE B — Cardan sans blocage et matrice à dérivée première
│     │
│     ├── B1.0 Cardan sans blocage
│     │     ├── pol (coordonnées polaires)
│     │     ├── Angles fondamentaux :
│     │     │     ├── ang_BDE (60°)
│     │     │     ├── ang_CGF (75°)
│     │     │     └── ang_BAC (45°)
│     │     ├── Longueurs fondamentales :
│     │     │     ├── BD_len, DE_len, BC_len, EF_len
│     │     │     ├── FG_len, CG_len, AB_len
│     │     │     ├── AC_len, DG_len, AG_len
│     │     └── Points du cardan :
│     │           ├── card_D, card_G, card_A, card_B
│     │           ├── card_E, card_C, card_F
│     │           └── card_G2
│     │
│     ├── B2.0 Matrice à dérivée première
│     │     ├── Record cardan_lengths
│     │     ├── Coefficients C1…C9
│     │     ├── Sommes R1, R2, R3
│     │     ├── M1_L1, M1_L2, M1_L3
│     │     └── M1_matrix
│     │
│     ├── B2.1 Matrice de transition
│     │     ├── Record drift_transition
│     │     └── M2_structure
│     │
│     └── B2.2 Matrice simplifiée (nombres premiers)
│           ├── u = sqrt(3.375)
│           ├── L1_simplified
│           ├── L2_simplified
│           ├── L3_simplified
│           ├── L1_weighted
│           ├── L2_weighted
│           └── L3_weighted
│
├── CHAPITRE C — Prisme matriciel à dérivée première
│     │
│     ├── C1.0 Définition du prisme matriciel
│     │     ├── Structure tridimensionnelle
│     │     ├── Relations entre plans
│     │     └── Interprétation géométrique
│     │
│     └── C2.0 Propriétés du prisme
│           ├── Équilibre matriciel
│           ├── Invariance par changement d’unité
│           └── Rôle de l’inconnue unique u = sqrt(3.375)
│
├── CHAPITRE D — Facteur trigonométrique alternatif
│     │
│     ├── D1.0 Inversion du rapport hauteur/demi-base
│     │     ├── inv_ratio_height_halfbase
│     │     ├── inv_ratio_height_halfbase_simpl
│     │
│     ├── D1.1 alt_factor (facteur trigonométrique)
│     │     ├── alt_factor
│     │     ├── alt_factor_axiom
│     │     ├── alt_factor_for_primes
│     │     ├── diam_equiv_sq
│     │     ├── diam_equiv_sq_for_primes
│     │     └── alt_factor_explicit_for_primes
│     │
│     └── Interprétation : lien trigonométrique ↔ invariant géométrique
│
└── ANNEXE — Crédits et Licence Apache 2.0
