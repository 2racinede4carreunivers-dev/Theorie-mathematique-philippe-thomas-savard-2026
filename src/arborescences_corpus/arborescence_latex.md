# Arborescence documentaire LaTeX

## Documents source -- Theorie de l'Univers est au Carre

**Generee le :** 2026-04-13
**Documents :** 10 fichiers `.tex`

---

## Schema des relations entre documents

```mermaid
graph TD
    subgraph Documents mathematiques - Francais
        GNP["geometrie_nombre_premier.tex<br/><i>57 sections, 108 Ko</i>"]
        AHR["analyse_hypothese_riemann_savard.tex<br/><i>52 sections, 122 Ko</i>"]
        PUC["postulat_de_univers_carre.tex<br/><i>18 sections, 22 Ko</i>"]
        MHC["mecanique_harmonique_du_chaos_discret.tex<br/><i>15 sections, 52 Ko</i>"]
        EDP["espace_de_philippot.tex<br/><i>8 sections, 6 Ko</i>"]
    end

    subgraph Documents mathematiques - Anglais
        GPS["geometry_prime_spectrum.tex<br/><i>50 sections, 108 Ko</i>"]
        PNG["prime_number_geometry.tex<br/><i>49 sections, 104 Ko</i>"]
    end

    subgraph Documents philosophiques - Francais
        TEL_FR["teleosemantique_philosophie_<br/>esprit_analogiste.tex<br/><i>44 sections, 78 Ko</i>"]
    end

    subgraph Documents philosophiques - Anglais
        PIL_EN["pilosophy_geometry_of_<br/>prime_number.tex<br/><i>44 sections, 70 Ko</i>"]
        TEL_EN["teleosemantics_mind_<br/>analogist_philosophy.tex<br/><i>44 sections, 70 Ko</i>"]
    end

    GNP -. "traduction EN" .-> GPS
    GNP -. "traduction EN" .-> PNG
    TEL_FR -. "traduction EN" .-> TEL_EN
    TEL_FR -. "traduction EN" .-> PIL_EN

    AHR -- "extension de" --> GNP
    PUC -- "fondation" --> GNP
    MHC -- "mecanique de" --> GNP
    EDP -- "geometrie 3D de" --> MHC

    style GNP fill:#2563eb,color:#fff
    style AHR fill:#2563eb,color:#fff
    style PUC fill:#2563eb,color:#fff
    style MHC fill:#2563eb,color:#fff
    style EDP fill:#2563eb,color:#fff
    style GPS fill:#3b82f6,color:#fff
    style PNG fill:#3b82f6,color:#fff
    style TEL_FR fill:#7c3aed,color:#fff
    style PIL_EN fill:#a855f7,color:#fff
    style TEL_EN fill:#a855f7,color:#fff
```

**Legende :**
- **Bleu fonce** : Documents mathematiques en francais (sources principales)
- **Bleu clair** : Traductions anglaises des documents mathematiques
- **Violet fonce** : Document philosophique en francais
- **Violet clair** : Traductions anglaises du document philosophique
- Fleche pleine : relation conceptuelle
- Fleche pointillee : relation de traduction

---

## References croisees LaTeX ↔ HOL

```mermaid
graph LR
    subgraph Fichiers LaTeX
        AHR["analyse_hypothese_<br/>riemann_savard.tex"]
        GNP["geometrie_nombre_<br/>premier.tex"]
        PUC["postulat_de_<br/>univers_carre.tex"]
        MHC["mecanique_harmonique_<br/>du_chaos_discret.tex"]
        EDP["espace_de_<br/>philippot.tex"]
    end

    subgraph Theories HOL
        ms["methode_spectral.thy"]
        mp["methode_de_philippot.thy"]
        pc["postulat_carre.thy"]
        md["mecanique_discret.thy"]
        ep["espace_philippot.thy"]
    end

    AHR --> ms
    AHR --> mp
    GNP --> ms
    GNP --> mp
    PUC --> pc
    MHC --> md
    EDP --> ep

    style AHR fill:#2563eb,color:#fff
    style GNP fill:#2563eb,color:#fff
    style PUC fill:#2563eb,color:#fff
    style MHC fill:#2563eb,color:#fff
    style EDP fill:#2563eb,color:#fff
    style ms fill:#16a34a,color:#fff
    style mp fill:#16a34a,color:#fff
    style pc fill:#16a34a,color:#fff
    style md fill:#16a34a,color:#fff
    style ep fill:#16a34a,color:#fff
```

---

## Detail par document

### analyse_hypothese_riemann_savard.tex

| Propriete | Valeur |
|-----------|--------|
| Taille | 122 456 octets |
| Sections | 52 |
| Langue | Francais |
| HOL references | `methode_spectral.thy`, `methode_de_philippot.thy` |

```mermaid
graph TD
    A["Introduction et<br/>Declaration de l'Auteur"] --> B["Geometrie du Spectre<br/>des Nombres Premiers"]
    B --> C["Analyse Numerique<br/>Metrique"]
    C --> D["Methode de Philippot<br/>Validation HOL"]
    D --> E["Nombres Premiers et<br/>Emploi du Digamma"]
    E --> F["Methodes Spectrales :<br/>Rapport 1/2"]
    F --> G["Comparaison asymetrique<br/>chaotique"]
    G --> H["Suites pour nombres<br/>premiers negatifs"]
    H --> I["Quantite de nombres entre<br/>deux nombres premiers"]
    I --> J["Forme Generale --<br/>Script HOL Complet"]
    J --> K["Tableaux Complets<br/>des Deux Suites"]

    style A fill:#2563eb,color:#fff
    style B fill:#2563eb,color:#fff
    style C fill:#3b82f6,color:#fff
    style D fill:#3b82f6,color:#fff
    style E fill:#7c3aed,color:#fff
    style F fill:#7c3aed,color:#fff
    style G fill:#dc2626,color:#fff
    style H fill:#dc2626,color:#fff
    style I fill:#ea580c,color:#fff
    style J fill:#16a34a,color:#fff
    style K fill:#16a34a,color:#fff
```

---

### postulat_de_univers_carre.tex

| Propriete | Valeur |
|-----------|--------|
| Taille | 22 774 octets |
| Sections | 18 |
| Langue | Francais |
| HOL references | `postulat_carre.thy` |

```mermaid
graph TD
    A["Note de l'auteur"] --> B["Explication mathematique<br/>du postulat du squaring"]
    B --> B1["Rectangle initial ABCD"]
    B --> B2["Elevation au carre : A'B'C'D'"]
    B --> B3["Carre maximal inscrit"]
    B --> B4["Decomposition interne"]
    B --> B5["Trois diagonales fondamentales"]
    B --> B6["Trois equations de<br/>l'octogone carre"]
    B2 --> C["Appendix :<br/>Script HOL Isabelle"]
    B6 --> D["Unite symbolique sqrt(3)"]
    D --> D1["Developpement en calculs"]
    D --> D2["Rectangle transforme"]
    D --> D3["Validation formelle p=3"]
    D3 --> E["Resume de la methode"]
    E --> E1["Theoreme de Gabriel<br/>Triangle rectangle"]
    E --> E2["Theoreme de Gabriel<br/>Triangle scalene"]

    style A fill:#2563eb,color:#fff
    style B fill:#2563eb,color:#fff
    style B1 fill:#3b82f6,color:#fff
    style B2 fill:#3b82f6,color:#fff
    style B3 fill:#3b82f6,color:#fff
    style B4 fill:#3b82f6,color:#fff
    style B5 fill:#3b82f6,color:#fff
    style B6 fill:#3b82f6,color:#fff
    style C fill:#16a34a,color:#fff
    style D fill:#7c3aed,color:#fff
    style D1 fill:#a855f7,color:#fff
    style D2 fill:#a855f7,color:#fff
    style D3 fill:#a855f7,color:#fff
    style E fill:#ea580c,color:#fff
    style E1 fill:#ea580c,color:#fff
    style E2 fill:#ea580c,color:#fff
```

---

### mecanique_harmonique_du_chaos_discret.tex

| Propriete | Valeur |
|-----------|--------|
| Taille | 52 339 octets |
| Sections | 15 |
| Langue | Francais |
| HOL references | `mecanique_discret.thy` |

```mermaid
graph TD
    A["Figure de la mecanique<br/>harmonique du chaos discret"] --> A1["Produit alternatif sqrt(2)"]
    A --> A2["Produit alternatif sqrt(3)"]
    A --> A3["Produit alternatif sqrt(5)"]
    A --> A4["Lecture des 3 exemples"]
    A --> A5["Invariance geometrique<br/>et lien HOL"]
    A5 --> B["Construction des 3 matrices"]
    B --> B1["M1 : mesures du plan"]
    B --> B2["M2 : matrice de transition"]
    B --> B3["M3 : derivee premiere"]
    B --> B4["Comment construire<br/>les trois matrices"]
    B --> B5["Facteur trigonometrique<br/>alternatif"]
    B5 --> C["Script HOL :<br/>mecanique_discret.thy"]
    C --> D["Conclusion"]

    style A fill:#2563eb,color:#fff
    style A1 fill:#3b82f6,color:#fff
    style A2 fill:#3b82f6,color:#fff
    style A3 fill:#3b82f6,color:#fff
    style A4 fill:#3b82f6,color:#fff
    style A5 fill:#3b82f6,color:#fff
    style B fill:#7c3aed,color:#fff
    style B1 fill:#a855f7,color:#fff
    style B2 fill:#a855f7,color:#fff
    style B3 fill:#a855f7,color:#fff
    style B4 fill:#a855f7,color:#fff
    style B5 fill:#a855f7,color:#fff
    style C fill:#16a34a,color:#fff
    style D fill:#4a4a4a,color:#fff
```

---

### espace_de_philippot.tex

| Propriete | Valeur |
|-----------|--------|
| Taille | 6 346 octets |
| Sections | 8 |
| Langue | Francais |
| HOL references | `espace_philippot.thy` |

**Structure :**

| # | Section |
|---|---------|
| 1 | Introduction |
| 2 | Structure geometrique de l'Espace de Philippot |
| 3 | Nombres hypercomplexes geometriques |
| 4 | Aires des quatre faces a la hauteur sqrt(2) |
| 5 | Volume de la pyramide et correspondance ellipsoidale |
| 6 | Relations exactes validees dans HOL |
| 7 | Conclusion |

---

### geometrie_nombre_premier.tex

| Propriete | Valeur |
|-----------|--------|
| Taille | 108 709 octets |
| Sections | 50 |
| Langue | Francais |
| HOL references | `methode_spectral.thy`, `methode_de_philippot.thy` |
| Traductions | `geometry_prime_spectrum.tex`, `prime_number_geometry.tex` |

---

### teleosemantique_philosophie_esprit_analogiste.tex

| Propriete | Valeur |
|-----------|--------|
| Taille | 78 410 octets |
| Sections | 44 |
| Langue | Francais |
| HOL references | Aucune (document philosophique) |
| Traductions | `teleosemantics_mind_analogist_philosophy.tex`, `pilosophy_geometry_of_prime_number.tex` |

**Themes couverts :**
- Autobiographie et parcours scolaire
- Esprit geometrique et pulsion de vie
- Definition de l'idioschizophrenie
- Phenomenologie et lois du savoir
- L'esprit analogiste et l'isossophie

---

*Generee depuis le corpus source -- 10 documents LaTeX*
