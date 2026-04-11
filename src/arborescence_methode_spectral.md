Méthode Spectrale (methode_spectral.thy)
│
├── I. Rapport Spectral 1/2 — Fondations
│   │
│   ├── 1. Suites SA et SB
│   │     ├── SA_def
│   │     └── SB_def
│   │
│   ├── 2. Validité pour n > 0
│   │     ├── SA_forme_generale
│   │     └── SB_forme_generale
│   │
│   ├── 3. Rapport spectral RsP
│   │     ├── RsP_def
│   │     └── RsP_un_demi_general
│   │
│   ├── 4. Généralisation n×n
│   │     ├── RsP_nn
│   │     └── rapport_spectral_un_demi_nn
│   │
│   └── 5. Exemples numériques (29, 31, 37, 41)
│         ├── SA_10 / SB_10
│         ├── SA_11 / SB_11
│         ├── SA_12 / SB_12
│         ├── SA_13 / SB_13
│         └── digamma_calc_XX + relations
│
├── II. Modèles Spectraux 1/3 et 1/4
│   │
│   ├── A. Modèle 1/3
│   │     ├── A_1_3_def / B_1_3_def
│   │     ├── prime_equation_1_3
│   │     ├── spectral_postulate_1_3
│   │     ├── RsP_un_tiers_constant
│   │     └── Exemple : premier 227
│   │
│   └── B. Modèle 1/4
│         ├── A_1_4_def / B_1_4_def
│         ├── prime_equation_1_4
│         ├── spectral_postulate_1_4
│         ├── RsP_un_quart_constant
│         └── Exemple : premier 947
│
├── III. Méthode Savard — Unification générale
│   │
│   ├── Équations spectrales négatives
│   │     ├── SA_neg_eq
│   │     ├── SB_neg_eq
│   │     └── digamma_neg_calc
│   │
│   ├── Identités affines
│   │     ├── SB_affine_en_SA
│   │     ├── digamma_affine_en_SA
│   │     └── ecart_spectral_constant
│   │
│   └── Incréments
│         ├── difference_SA_succ
│         ├── difference_SB_succ
│         └── ratio_incremental_un_demi
│
├── IV. Écart entre deux nombres premiers
│   │
│   ├── digamma_calc
│   ├── prime_equation
│   ├── prime_equation_identity
│   └── Exemples d’écarts (positifs et négatifs)
│
├── V. Géométrie Spectrale — Asymétries
│   │
│   ├── Asymétrie ordonnée (int)
│   │     ├── indice_valide
│   │     ├── liste_strictement_croissante
│   │     └── asymetrique_ordonnee
│   │
│   ├── Asymétrie chaotique (int)
│   │     └── asymetrique_chaotique
│   │
│   └── Version naturelle (nat)
│         ├── indice_valide_nat
│         ├── asymetrique_ordonnee_nat
│         └── asymetrique_chaotique_nat
│
├── VI. Méthode de comparaison asymétrique
│   │
│   ├── Sommes de blocs
│   │     ├── somme_SA_bloc
│   │     └── somme_SB_bloc
│   │
│   ├── Rapport spectral de blocs
│   │     └── RsP_bloc_1_2
│   │
│   └── Comparaison ordonnée / chaotique
│         ├── comparaison_asym_ordonnee_1_2
│         └── comparaison_asym_chaotique_1_2
│
└── VII. SECTION FINALE — AXIOMATISATIONS DE LA MÉTHODE SPECTRALE
    │
    ├── 1. Axiomatisation du rapport spectral négatif
    │     ├── spectral_ratio_neg_un_demi
    │     └── RsP_neg_un_demi_general
    │
    ├── 2. Axiomatisation des indices valides
    │     ├── indice_valide
    │     └── indice_valide_nat
    │
    ├── 3. Axiomatisation des asymétries
    │     ├── asymetrique_ordonnee
    │     ├── asymetrique_chaotique
    │     ├── asymetrique_ordonnee_nat
    │     └── asymetrique_chaotique_nat
    │
    ├── 4. Axiomatisation de la comparaison asymétrique
    │     ├── comparaison_asym_ordonnee_1_2
    │     └── comparaison_asym_chaotique_1_2
    │
    └── 5. Bloc conceptuel d’unification Zêta / Spectre
          (intention mathématique : relier structure spectrale ↔ zéros de ζ(s))
