espace_philippot.thy
│
├── I. Côtes de la pyramide selon la spirale de Théodore
│     │
│     ├── Description générale
│     │     └── L(n) = sqrt(n * Lref²)
│     │
│     ├── Longueurs de référence
│     │     ├── L1_ref
│     │     ├── L2_ref
│     │     ├── L3_ref
│     │     └── L4_ref
│     │
│     └── Définition générale d’un côté
│           ├── cote Lref n
│           ├── cote1
│           ├── cote2
│           ├── cote3
│           └── cote4
│
├── II. Propriétés générales des côtés
│     ├── cote_formule_exacte
│     ├── cote_carre_exact
│     ├── cote1_carre_exact
│     └── cote2_carre_exact
│
├── III. Hauteurs, rayons et spirale de Théodore
│     │
│     ├── Hauteur de la pyramide
│     │     ├── hauteur n = sqrt(n)
│     │     ├── hauteur_carre_exact
│     │
│     ├── Rayon associé
│     │     ├── rayon n = sqrt(hauteur n / 10)
│     │     ├── rayon_def_simplifie
│     │     └── rayon_carre_exact
│     │
│     └── Axiome géométrique fondamental
│           ├── diag_base (constante)
│           ├── aire_disque (constante)
│           └── relation_diag_hauteur_rayon :
│                 (diag_base * hauteur n + rayon n)/2
│                 = (hauteur n)² + aire_disque
│
├── IV. Nombres hypercomplexes géométriques
│     │
│     ├── Type hypercomplexe
│     │     └── hypercomplexe = real * real * real
│     │
│     ├── Trois formes hypercomplexes
│     │     ├── hyper1 A r
│     │     ├── hyper2 A r
│     │     └── hyper3 A r
│     │
│     └── Interprétation :
│           nombres géométriques liés aux disques et rayons
│
├── V. Axiomatisation de la pyramide hypercomplexe
│     │
│     ├── Types abstraits
│     │     ├── event
│     │     └── index
│     │
│     ├── Constantes géométriques
│     │     ├── r(n)      : rayon du disque
│     │     ├── a(n), b(n), c(n), d(n) : composantes hypercomplexes
│     │     ├── V_pyr(n)  : volume pyramide
│     │     ├── V_ell(n)  : volume ellipsoïde
│     │     ├── val_geom(n)
│     │     └── spiral_pos(n, e)
│     │
│     └── Axiomes globaux
│           ├── spiral_Theodore :
│           │     ∃f. r(f n) = sqrt(n)
│           │
│           ├── val_geom_form :
│           │     val_geom n = sqrt(u n) + v n
│           │
│           ├── hypercomplex_norm :
│           │     N(a,b,c,d) = sqrt(a² + b² + c² + d²)
│           │
│           ├── volume_ratio :
│           │     V_ell n = 10 * V_pyr n
│           │
│           └── events_on_spiral :
│                 spiral_pos n e = F(a n, b n, c n, d n) e
│
└── VI. Interprétation globale
      ├── Spirale de Théodore comme structure d’échelle
      ├── Pyramide géométrique comme espace interne
      ├── Hypercomplexes comme coordonnées généralisées
      ├── Volumes ellipsoïdaux ↔ volumes pyramidaux
      └── Événements sur la spirale = espace-temps géométrique
