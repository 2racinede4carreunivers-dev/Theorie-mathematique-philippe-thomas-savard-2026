# Arborescence logique HOL

## Session Isabelle : Univers_Au_Carre

**Generee depuis :** `Univers_Au_Carre.db` (session HOL compilee)
**Session :** `Univers_Au_Carre`
**Return code :** 0 (compilation reussie)
**Heap d'entree :** `Pure` → `HOL`

---

## Schema de dependances des theories

```mermaid
graph TD
    subgraph Isabelle Standard Library
        Pure["Pure"]
        HOL["HOL"]
        Main["Main"]
        Complex_Main["Complex_Main"]
        HOL_Rat["HOL.Rat"]
    end

    Pure --> HOL
    HOL --> Main
    Main --> Complex_Main
    HOL --> HOL_Rat

    subgraph Session Univers_Au_Carre
        postulat["postulat_carre.thy"]
        spectral["methode_spectral.thy"]
        mecanique["mecanique_discret.thy"]
        philippot["methode_de_philippot.thy"]
        espace["espace_philippot.thy"]
    end

    Complex_Main --> postulat
    Complex_Main --> spectral
    Complex_Main --> mecanique
    Complex_Main --> espace
    Main --> philippot
    HOL_Rat --> philippot

    style Pure fill:#4a4a4a,color:#fff
    style HOL fill:#4a4a4a,color:#fff
    style Main fill:#555,color:#fff
    style Complex_Main fill:#1a6b3c,color:#fff
    style HOL_Rat fill:#1a6b3c,color:#fff
    style postulat fill:#2563eb,color:#fff
    style spectral fill:#2563eb,color:#fff
    style mecanique fill:#2563eb,color:#fff
    style philippot fill:#7c3aed,color:#fff
    style espace fill:#2563eb,color:#fff
```

**Legende :**
- **Vert** : Bibliotheques Isabelle standard (`Complex_Main`, `HOL.Rat`)
- **Bleu** : Theories importees depuis `Complex_Main` (analyse complexe)
- **Violet** : `methode_de_philippot.thy` utilise `Main` + `HOL.Rat` (nombres rationnels) au lieu de `Complex_Main`

---

## Architecture conceptuelle de la session

```mermaid
graph LR
    subgraph Fondations geometriques
        postulat["postulat_carre"]
    end

    subgraph Analyse spectrale
        spectral["methode_spectral"]
    end

    subgraph Methode iterative
        philippot["methode_de_philippot"]
    end

    subgraph Mecanique discrete
        mecanique["mecanique_discret"]
    end

    subgraph Geometrie 3D
        espace["espace_philippot"]
    end

    postulat -- "squaring du rectangle" --> spectral
    spectral -- "rapport spectral 1/k" --> philippot
    philippot -- "substitution spectrale" --> mecanique
    postulat -- "unite sqrt(p)+1" --> mecanique
    mecanique -- "spirale de Theodore" --> espace

    style postulat fill:#2563eb,color:#fff
    style spectral fill:#2563eb,color:#fff
    style philippot fill:#7c3aed,color:#fff
    style mecanique fill:#2563eb,color:#fff
    style espace fill:#2563eb,color:#fff
```

---

## Detail par theorie

### postulat_carre.thy

| Propriete | Valeur |
|-----------|--------|
| Import | `Complex_Main` |
| Locales | 6 |
| Definitions | 19 |
| Axiomes | Oui (multiples axiomatisations) |

```mermaid
graph TD
    subgraph Locales de postulat_carre.thy
        L1["postulat_carre<br/><i>w, h : real ; prime p</i>"]
        L2["rectangle_carre<br/><i>Extension : squaring</i>"]
        L3["polygone_carre_axiomes<br/><i>Polygones reguliers inscrits</i>"]
        L4["exemple_p3<br/><i>Exemple numerique p = 3</i>"]
        L5["octogone_carre_equations<br/><i>3 equations de l'octogone</i>"]
        L6["hexagone_carre_equations<br/><i>Equations de l'hexagone</i>"]
    end

    L1 --> L2
    L1 --> L3
    L3 --> L4
    L3 --> L5
    L3 --> L6

    style L1 fill:#2563eb,color:#fff
    style L2 fill:#3b82f6,color:#fff
    style L3 fill:#3b82f6,color:#fff
    style L4 fill:#60a5fa,color:#fff
    style L5 fill:#60a5fa,color:#fff
    style L6 fill:#60a5fa,color:#fff
```

**Definitions principales :**

| Definition | Description |
|-----------|-------------|
| `unit_p` | Unite symbolique de la theorie |
| `ratio_height_square` | Rapport hauteur au carre |
| `ratio_trunc_square` | Rapport troncature au carre |
| `area_rect` | Aire du rectangle |
| `area_square` | Aire du carre maximal inscrit |
| `rect_equiv_square` | Equivalence rectangle-carre |
| `eq_postulat` | Equation du postulat |
| `polygone_defini` | Definition du polygone regulier |
| `postulat_eq` | Equation principale du postulat |

---

### methode_spectral.thy

| Propriete | Valeur |
|-----------|--------|
| Import | `Complex_Main` |
| Locales | 0 |
| Definitions | 90+ |
| Axiomes | 15+ axiomatisations |

**Theorie la plus dense du corpus.**

```mermaid
graph TD
    subgraph I. Rapport spectral 1/2
        SA["SA, SB<br/><i>Suites de base</i>"]
        RsP["RsP, RsP_nn<br/><i>Rapport spectral</i>"]
        DG["digamma_calc<br/><i>Calcul du Digamma</i>"]
    end

    subgraph II. Extensions 1/3 et 1/4
        M3["A_1_3, B_1_3, RsP_1_3<br/><i>Modele k=3</i>"]
        M4["A_1_4, B_1_4, RsP_1_4<br/><i>Modele k=4</i>"]
    end

    subgraph III. Nombres negatifs
        NEG["SA_neg_eq, SB_neg_eq<br/><i>Extension n &lt; 0</i>"]
    end

    subgraph IV. Asymetrie et blocs
        ASYM["asymetrique_ordonnee<br/>asymetrique_chaotique"]
        BLOC["somme_SA_bloc<br/>somme_SB_bloc<br/>RsP_bloc_1_2"]
    end

    subgraph V. Equations de l'ecart
        GAP["gap_equation_1_3<br/>gap_equation_1_4"]
    end

    SA --> RsP
    SA --> DG
    RsP --> M3
    RsP --> M4
    RsP --> NEG
    NEG --> ASYM
    ASYM --> BLOC
    M3 --> GAP
    M4 --> GAP

    style SA fill:#2563eb,color:#fff
    style RsP fill:#2563eb,color:#fff
    style DG fill:#3b82f6,color:#fff
    style M3 fill:#7c3aed,color:#fff
    style M4 fill:#7c3aed,color:#fff
    style NEG fill:#dc2626,color:#fff
    style ASYM fill:#ea580c,color:#fff
    style BLOC fill:#ea580c,color:#fff
    style GAP fill:#16a34a,color:#fff
```

**Axiomes fondamentaux :**

| Axiome | Enonce |
|--------|--------|
| Equation premiere | Pour tout n >= 1 et p premier : `prime_equation(n, p) = p` |
| Rapport negatif 1/2 | Pour n1, n2 <= -1, n1 != n2 : `RsP_neg(n1, n2) = 1/2` |
| Rapport negatif 1/3 | Pour n1, n2 <= -1, n1 != n2 : `RsP_neg_1_3(n1, n2) = 1/3` |
| Rapport negatif 1/4 | Pour n1, n2 <= -1, n1 != n2 : `RsP_neg_1_4(n1, n2) = 1/4` |
| Gap 1/3 | Validation : 227 / 173 |
| Gap 1/4 | Validation : 947 / 881 |
| Spectral final | Il existe P tel que `P_spectral(n) = P` et `A(n) + B(n) >= 1` |
| Zeros de Riemann | Pour tout rho (zero de zeta) : `Re(rho) = 1/2` |

---

### mecanique_discret.thy

| Propriete | Valeur |
|-----------|--------|
| Import | `Complex_Main` |
| Locales | 0 |
| Definitions | 60+ |
| Axiomes | 3 axiomatisations |

```mermaid
graph TD
    subgraph A. Geometrie de base
        GEO["base_length, height_length<br/>side, A, B, C, D"]
        UNIT["admissible_unit<br/>unit = sqrt(p) + 1"]
        RATIO["ratio_halfbase_height<br/>= sqrt(p)"]
    end

    subgraph B. Segments et angles
        SEG["BD, DE, BC, EF,<br/>FG, CG, AB, AC"]
        ANG["angle_rect, ang_BDE,<br/>ang_CGF, ang_BAC"]
        CARD["card_D, card_G,<br/>card_A ... card_F"]
    end

    subgraph C. Matrices de transition
        M1["M1_matrix<br/><i>3 lignes</i>"]
        M2["M2_structure<br/><i>Transition</i>"]
        DER["L1_weighted, L2_weighted<br/>L3_weighted<br/><i>Coefficients premiers</i>"]
    end

    subgraph D. Invariance
        INV["inv_ratio_height_halfbase<br/>alt_factor<br/>diam_equiv_sq"]
    end

    GEO --> UNIT
    UNIT --> RATIO
    RATIO --> SEG
    SEG --> ANG
    ANG --> CARD
    SEG --> M1
    M1 --> M2
    M2 --> DER
    RATIO --> INV

    style GEO fill:#2563eb,color:#fff
    style UNIT fill:#2563eb,color:#fff
    style RATIO fill:#3b82f6,color:#fff
    style SEG fill:#7c3aed,color:#fff
    style ANG fill:#7c3aed,color:#fff
    style CARD fill:#7c3aed,color:#fff
    style M1 fill:#ea580c,color:#fff
    style M2 fill:#ea580c,color:#fff
    style DER fill:#ea580c,color:#fff
    style INV fill:#16a34a,color:#fff
```

**Axiomes :**

| Axiome | Enonce |
|--------|--------|
| Ratio fondamental | Si `admissible_unit(p)` et n >= 1 : `ratio_halfbase_height(n, p) = sqrt(p)` |
| Invariance | `AL_nat(p) != 0` et l'unite geometrique coincide avec `sqrt(p) + 1` |
| Alt factor | `alt_factor(p) = 1 / sqrt(p)` |

---

### methode_de_philippot.thy

| Propriete | Valeur |
|-----------|--------|
| Import | `Main`, `HOL.Rat` |
| Locales | 0 |
| Definitions | 32 |
| Fonctions | 1 (`etape1_general`) |

```mermaid
graph TD
    subgraph Etape 1 - 11 termes
        E1["etape1_3 = [1/2, 1/3, 1/6]<br/>etape1_4 = [1/2, 1/4, 1/6, 1/12]<br/>... jusqu'a etape1_11"]
        EG["etape1_general<br/><i>Fonction recursive</i>"]
        POS["pos_substitution"]
    end

    subgraph Etape 2 - 7 termes
        E2P["suite_reglementaire_etape2_petit"]
        E2G["suite_reglementaire_etape2_grand"]
    end

    subgraph Etape 3 - 11 termes
        E3["suite_reglementaire_etape3"]
        VAL["valeur_substituee_etape3"]
    end

    subgraph Resultat spectral
        TS["terme_spectral"]
        SS["suite_spectrale"]
    end

    E1 --> EG
    EG --> POS
    POS --> E2P
    POS --> E2G
    E2P --> E3
    E2G --> E3
    E3 --> VAL
    VAL --> TS
    TS --> SS

    style E1 fill:#7c3aed,color:#fff
    style EG fill:#7c3aed,color:#fff
    style POS fill:#7c3aed,color:#fff
    style E2P fill:#a855f7,color:#fff
    style E2G fill:#a855f7,color:#fff
    style E3 fill:#c084fc,color:#fff
    style VAL fill:#c084fc,color:#fff
    style TS fill:#16a34a,color:#fff
    style SS fill:#16a34a,color:#fff
```

---

### espace_philippot.thy

| Propriete | Valeur |
|-----------|--------|
| Import | `Complex_Main` |
| Locales | 0 |
| Definitions | 13 |
| Axiomes | 5 axiomatisations |

```mermaid
graph TD
    subgraph Longueurs de reference
        L["L1_ref = 1.653<br/>L2_ref = 1.728<br/>L3_ref = 1.653<br/>L4_ref = 0.938"]
    end

    subgraph Pyramide
        COTE["cote1(n), cote2(n),<br/>cote3(n), cote4(n)"]
        HAUT["hauteur"]
        RAY["rayon"]
    end

    subgraph Hypercomplexes
        HYP["hyper1, hyper2, hyper3"]
    end

    L --> COTE
    COTE --> HAUT
    COTE --> RAY
    HAUT --> HYP
    RAY --> HYP

    style L fill:#2563eb,color:#fff
    style COTE fill:#3b82f6,color:#fff
    style HAUT fill:#7c3aed,color:#fff
    style RAY fill:#7c3aed,color:#fff
    style HYP fill:#dc2626,color:#fff
```

**Axiomes :**

| Axiome | Enonce |
|--------|--------|
| Spirale de Theodore | Il existe f tel que pour tout n : `r(f(n)) = sqrt(n)` |
| Valeur geometrique | Il existe u, v tel que `val_geom(n) = sqrt(u(n)) + v(n)` |
| Norme hypercomplexe | `N(a, b, c, d) = sqrt(a^2 + b^2 + c^2 + d^2)` |
| Pyramide-ellipsoide | Pour tout n : `V_ell(n) = 10 * V_pyr(n)` |
| Position spirale | `spiral_pos(n, e) = F(a(n), b(n), c(n), d(n), e)` |

---

*Generee depuis Univers_Au_Carre.db -- Session Isabelle 2024 -- Compilation reussie (return code 0)*
