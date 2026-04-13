# Arborescence globale de la theorie

## L'Univers est au Carre -- Philippe Thomas Savard

**Generee le :** 2026-04-13

---

## Vue d'ensemble

| Categorie | Nombre |
|-----------|--------|
| Fichiers .tex | 10 |
| Fichiers .thy | 5 |
| Fichiers .pdf | 14 |
| Total fichiers | 29 |
| Total pages PDF | 499 |

---

## Architecture globale du depot

```mermaid
graph TD
    ROOT["repo_savard/"]

    ROOT --> SRC["src/"]
    ROOT --> QA["qa_bank/"]
    ROOT --> SCRIPTS["scripts/"]
    ROOT --> GH[".github/workflows/"]
    ROOT --> IA["Ia_geo_spec_prem_app_deplo/"]
    ROOT --> DOCS["docs/"]

    SRC --> TEX["tex/<br/><i>10 fichiers .tex</i>"]
    SRC --> HOL["hol/<br/><i>5 fichiers .thy + ROOT</i>"]
    SRC --> PDF["pdf/<br/><i>14 fichiers .pdf</i>"]
    SRC --> ARB["arborescences_corpus/<br/><i>4 fichiers .md</i>"]

    QA --> QADB["qa_bank.db"]
    QA --> CORPUS["corpus.db"]
    QA --> QCAT["CATALOGUE.md"]

    SCRIPTS --> QAGEN["auto_generate_qa.py"]
    SCRIPTS --> CORPGEN["generate_corpus_db.py"]

    GH --> BUILD["build.yml"]
    GH --> CRON["auto-daily-qa.yml"]

    style ROOT fill:#4a4a4a,color:#fff
    style SRC fill:#2563eb,color:#fff
    style QA fill:#16a34a,color:#fff
    style SCRIPTS fill:#ea580c,color:#fff
    style GH fill:#7c3aed,color:#fff
    style IA fill:#dc2626,color:#fff
    style DOCS fill:#555,color:#fff
    style TEX fill:#3b82f6,color:#fff
    style HOL fill:#3b82f6,color:#fff
    style PDF fill:#3b82f6,color:#fff
    style ARB fill:#3b82f6,color:#fff
    style QADB fill:#16a34a,color:#fff
    style CORPUS fill:#16a34a,color:#fff
    style QCAT fill:#16a34a,color:#fff
    style QAGEN fill:#ea580c,color:#fff
    style CORPGEN fill:#ea580c,color:#fff
    style BUILD fill:#7c3aed,color:#fff
    style CRON fill:#7c3aed,color:#fff
```

---

## Schema de flux complet : du source a la Q&R

```mermaid
graph TD
    subgraph 1. Sources
        TEX[".tex<br/><i>Documents LaTeX</i>"]
        THY[".thy<br/><i>Theories Isabelle/HOL</i>"]
        IMG[".png<br/><i>Figures geometriques</i>"]
    end

    subgraph 2. Build CI/CD
        BUILD["build.yml<br/><i>GitHub Actions</i>"]
        PDFLATEX["pdflatex"]
        ISABELLE["isabelle build"]
        CORPUSGEN["generate_corpus_db.py"]
    end

    subgraph 3. Artefacts
        PDF[".pdf<br/><i>14 documents</i>"]
        HOLDB["Univers_Au_Carre.db<br/><i>Session compilee</i>"]
        CORPUSDB["corpus.db<br/><i>Extraction complete</i>"]
    end

    subgraph 4. Generation Q&R
        CRON["auto-daily-qa.yml<br/><i>Cron quotidien</i>"]
        QAGEN["auto_generate_qa.py"]
        LLM["GPT-4o<br/><i>Emergent LLM Key</i>"]
    end

    subgraph 5. Banque de Q&R
        QADB["qa_bank.db"]
        QAMD[".md + .json<br/><i>Fichiers generes</i>"]
    end

    TEX --> BUILD
    THY --> BUILD
    IMG --> BUILD
    BUILD --> PDFLATEX
    BUILD --> ISABELLE
    BUILD --> CORPUSGEN
    PDFLATEX --> PDF
    ISABELLE --> HOLDB
    CORPUSGEN --> CORPUSDB

    CRON --> QAGEN
    CORPUSDB --> QAGEN
    QAGEN --> LLM
    LLM --> QADB
    LLM --> QAMD

    style TEX fill:#2563eb,color:#fff
    style THY fill:#2563eb,color:#fff
    style IMG fill:#7c3aed,color:#fff
    style BUILD fill:#ea580c,color:#fff
    style PDFLATEX fill:#ea580c,color:#fff
    style ISABELLE fill:#ea580c,color:#fff
    style CORPUSGEN fill:#ea580c,color:#fff
    style PDF fill:#16a34a,color:#fff
    style HOLDB fill:#16a34a,color:#fff
    style CORPUSDB fill:#16a34a,color:#fff
    style CRON fill:#7c3aed,color:#fff
    style QAGEN fill:#7c3aed,color:#fff
    style LLM fill:#dc2626,color:#fff
    style QADB fill:#16a34a,color:#fff
    style QAMD fill:#16a34a,color:#fff
```

---

## Interdependances entre les 3 couches

```mermaid
graph LR
    subgraph LaTeX - Documents
        AHR["analyse_hypothese_<br/>riemann_savard"]
        GNP["geometrie_nombre_<br/>premier"]
        PUC["postulat_de_<br/>univers_carre"]
        MHC["mecanique_harmonique_<br/>du_chaos_discret"]
        EDP["espace_de_<br/>philippot"]
        TEL["teleosemantique_<br/>esprit_analogiste"]
    end

    subgraph HOL - Preuves formelles
        ms["methode_spectral"]
        mp["methode_de_philippot"]
        pc["postulat_carre"]
        md["mecanique_discret"]
        ep["espace_philippot"]
    end

    subgraph PDF - Documents compiles
        P_AHR["analyse_hypothese_<br/>riemann_savard.pdf"]
        P_GNP["geometrie_nombre_<br/>premier.pdf"]
        P_PUC["postulat_de_<br/>univers_carre.pdf"]
        P_MHC["mecanique_harmonique_<br/>chaos_discret.pdf"]
        P_EDP["espace_de_<br/>philippot.pdf"]
        P_TEL["teleosemantique_<br/>esprit_analogiste.pdf"]
    end

    AHR --- ms
    AHR --- mp
    GNP --- ms
    GNP --- mp
    PUC --- pc
    MHC --- md
    EDP --- ep

    AHR --> P_AHR
    GNP --> P_GNP
    PUC --> P_PUC
    MHC --> P_MHC
    EDP --> P_EDP
    TEL --> P_TEL

    style AHR fill:#2563eb,color:#fff
    style GNP fill:#2563eb,color:#fff
    style PUC fill:#2563eb,color:#fff
    style MHC fill:#2563eb,color:#fff
    style EDP fill:#2563eb,color:#fff
    style TEL fill:#7c3aed,color:#fff
    style ms fill:#16a34a,color:#fff
    style mp fill:#16a34a,color:#fff
    style pc fill:#16a34a,color:#fff
    style md fill:#16a34a,color:#fff
    style ep fill:#16a34a,color:#fff
    style P_AHR fill:#ea580c,color:#fff
    style P_GNP fill:#ea580c,color:#fff
    style P_PUC fill:#ea580c,color:#fff
    style P_MHC fill:#ea580c,color:#fff
    style P_EDP fill:#ea580c,color:#fff
    style P_TEL fill:#ea580c,color:#fff
```

---

## Correspondances completes

| Concept | .tex | .thy | .pdf |
|---------|------|------|------|
| Analyse hypothese Riemann | `analyse_hypothese_riemann_savard.tex` | -- | `analyse_hypothese_riemann_savard.pdf` |
| Espace de Philippot | `espace_de_philippot.tex` | `espace_philippot.thy` | `espace_de_philippot.pdf` |
| Geometrie nombre premier | `geometrie_nombre_premier.tex` | -- | `geometrie_nombre_premier.pdf` |
| Geometry prime spectrum (EN) | `geometry_prime_spectrum.tex` | -- | `geometry_prime_spectrum.pdf`, `geometrie_du_spectre_premier.pdf` |
| Mecanique harmonique chaos | `mecanique_harmonique_du_chaos_discret.tex` | `mecanique_discret.thy` | `mecanique_harmonique_du_chaos_discret.pdf`, `mecanique_chaos_discret.pdf` |
| Methode de Philippot | -- | `methode_de_philippot.thy` | -- |
| Methode spectrale | -- | `methode_spectral.thy` | -- |
| Philosophy prime number (EN) | `pilosophy_geometry_of_prime_number.tex` | -- | `pilosophy_geometry_of_prime_number.pdf` |
| Postulat univers carre | `postulat_de_univers_carre.tex` | `postulat_carre.thy` | `postulat_de_univers_carre.pdf`, `postulat_univers_carre.pdf` |
| Prime number geometry (EN) | `prime_number_geometry.tex` | -- | `prime_number_geometry.pdf` |
| Teleosemantics (EN) | `teleosemantics_mind_analogist_philosophy.tex` | -- | `teleosemantics_mind_analogist_philosophy.pdf` |
| Teleosemantique (FR) | `teleosemantique_philosophie_esprit_analogiste.tex` | -- | `teleosemantique_philosophie_esprit_analogiste.pdf`, `telosemantique_analogiste_spectre_premier.pdf` |

---

## Hierarchie du depot

```
repo_savard/
|
|-- .github/workflows/
|   |-- build.yml                  (CI : compilation PDF + HOL + corpus.db)
|   |-- auto-daily-qa.yml         (Cron : generation quotidienne Q&R)
|
|-- src/
|   |-- tex/                       (10 documents LaTeX source)
|   |-- hol/                       (5 theories Isabelle/HOL + ROOT)
|   |-- pdf/                       (14 documents PDF compiles)
|   |-- arborescences_corpus/      (4 schemas Mermaid.js)
|
|-- qa_bank/
|   |-- qa_bank.db                 (Base de donnees Q&R)
|   |-- corpus.db                  (Extraction complete du corpus)
|   |-- CATALOGUE.md               (Index des Q&R generees)
|
|-- scripts/
|   |-- auto_generate_qa.py        (Generateur Q&R avec LLM)
|   |-- generate_corpus_db.py      (Extracteur de corpus vers SQLite)
|
|-- Ia_geo_spec_prem_app_deplo/    (Application web des 3 IAs collaboratives)
|-- docs/                          (Documentation supplementaire)
|-- SCRIPT_NARRATIF.md             (Script narratif V2 de la theorie)
|-- README.md                      (Presentation du depot)
```

---

*Generee depuis le depot complet -- 29 fichiers source, 5 theories, 14 PDF, 499 pages*
