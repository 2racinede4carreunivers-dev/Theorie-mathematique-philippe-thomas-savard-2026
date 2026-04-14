postulat_carre.thy
│
├── I. Introduction philosophique
│     └── A priori et raison pure : le produit carré d’un rectangle
│
├── II. Unified Squared Rectangle and Prime Postulate
│     │
│     ├── Locale : postulat_carre
│     │     ├── Hypothèses géométriques (w, h, s, t > 0)
│     │     ├── Hypothèse arithmétique : prime p
│     │     │
│     │     ├── Définitions fondamentales
│     │     │     ├── S_S  : aire du rectangle
│     │     │     ├── S_F  : aire du carré interne
│     │     │     ├── S_C  : aire complémentaire
│     │     │     ├── d_S  : diagonale rectangle
│     │     │     ├── d_F  : diagonale carré
│     │     │     ├── d_C  : diagonale complémentaire
│     │     │     ├── unit_p
│     │     │     ├── upto_from_2
│     │     │     ├── k
│     │     │     ├── postulat_eq
│     │     │     ├── ratio_height_square
│     │     │     └── ratio_trunc_square
│     │
│     └── Interprétation : carré unifié et postulat premier
│
├── III. Rectangle carré : équivalence avec un carré
│     │
│     ├── Locale : rectangle_carre
│     │     ├── area_rect
│     │     ├── area_square
│     │     └── rect_equiv_square
│     │
│     └── Condition d’équivalence aire(rectangle) = aire(carré)
│
├── IV. Axiomatisation du polygone au carré
│     │
│     ├── Locale : polygone_carre_axiomes
│     │     ├── Hypothèses : prime p, h>0, s>0, t>0
│     │     │
│     │     ├── Équations fondamentales
│     │     │     ├── eq_ratio_height
│     │     │     ├── eq_ratio_trunc
│     │     │     ├── eq_postulat
│     │     │     └── polygone_defini
│     │
│     └── Structure générale du polygone carré
│
├── V. Exemple numérique pour p = 3
│     │
│     ├── Locale : exemple_p3
│     │     ├── Hypothèses : s3>0, ratios exacts, diagonale exacte
│     │     │
│     │     ├── Lemmata
│     │     │     ├── hauteur_sur_cote
│     │     │     ├── tronque_sur_cote
│     │     │     ├── diagonale_tronquee_exacte
│     │     │     ├── aire_rectangle
│     │     │     ├── hauteur_exacte
│     │     │     ├── troncature_exacte
│     │     │     ├── diagonale_tronquee_carree
│     │     │     └── aire_exacte
│     │
│     └── Interprétation : cas p = 3 comme modèle canonique
│
├── VI. Système des trois équations : Octogone carré
│     │
│     ├── Locale : octogone_carre_equations
│     │     ├── Aires exactes
│     │     │     ├── area_carre_def
│     │     │     ├── area_rect_def
│     │     │     └── area_rect_c_def
│     │     │
│     │     ├── Diagonales exactes
│     │     │     ├── d_carre_def
│     │     │     ├── d_rect_comp_def
│     │     │     └── d_rect_def
│     │     │
│     │     ├── Valeurs numériques
│     │     │     ├── area_carre_num
│     │     │     └── area_rect_c_num
│     │     │
│     │     └── Système des trois équations
│     │           ├── eq1_octogone_carre
│     │           ├── eq2_octogone_carre
│     │           └── eq3_octogone_carre
│     │
│     └── Interprétation : structure carrée de l’octogone
│
├── VII. Système des trois équations : Hexagone carré
│     │
│     ├── Locale : hexagone_carre_equations
│     │     ├── Aires exactes
│     │     ├── Diagonales exactes
│     │     ├── Valeurs numériques
│     │     └── Système des trois équations
│     │           ├── eq1_hexagone_carre
│     │           ├── eq2_hexagone_carre
│     │           └── eq3_hexagone_carre
│     │
│     └── Interprétation : structure carrée de l’hexagone
│
└── VIII. Annexes et Licence
      ├── Code source complet
      └── Licence Apache 2.0
