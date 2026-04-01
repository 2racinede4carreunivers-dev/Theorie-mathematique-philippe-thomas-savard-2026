# Guide de compilation GitHub Actions
## Compilation, certification et attestation des documents

Ce dépôt utilise un pipeline GitHub Actions entièrement automatisé pour compiler, certifier et attester les **19 documents scientifiques** du projet :

- 7 fichiers LaTeX (`.tex`)
- 5 fichiers Isabelle/HOL (`.thy`)
- 7 fichiers PDF générés (`.pdf`)

L’ensemble du processus est reproductible, traçable et cryptographiquement attesté.

---

## 1. Vue d’ensemble du workflow

Le workflow suit une chaîne de compilation en trois étapes :

1. **Compilation scientifique**
   - Vérification formelle des théories HOL (`.thy`)
   - Compilation LaTeX → PDF (`.pdf`)

2. **Production des métadonnées**
   - SHA‑256 des PDF
   - Rapport d’attestation
   - Métadonnées du build (commit, date, branche)

3. **Attestation SLSA v1**
   - Certification de provenance
   - Signature cryptographique
   - Vérification que tous les fichiers proviennent de `main`

---

## 2. Installation des outils

### 2.1. TeX Live minimal

Le workflow installe :
- `texlive-latex-base`
- `texlive-latex-recommended`
- `texlive-latex-extra`
- `texlive-fonts-recommended`
- `texlive-lang-french`
- `python3-pygments` (pour `minted`)

**Garanties :**
- Compilation reproductible
- Support complet des packages requis
- Typographie française correcte
- Coloration syntaxique stable

---

### 2.2. Isabelle 2024

Le workflow :
- télécharge Isabelle 2024,
- l’extrait,
- ajoute `isabelle/bin` au PATH.

**Garanties :**
- Version fixe et stable
- Certification formelle des `.thy`
- Reproductibilité totale

---

## 3. Compilation des documents

### 3.1. Théories Isabelle/HOL (`.thy`)

Les fichiers suivants sont certifiés :

- `espace_philippot.thy`
- `methode_spectral.thy`
- `methode_de_philippot.thy`
- `mecanique_discret.thy`
- `postulat_carre.thy`

**Garanties :**
- Vérification formelle complète
- Cohérence logique assurée
- Aucune théorie invalide ne peut être publiée

---

### 3.2. Documents LaTeX (`.tex`)

Les 7 fichiers `.tex` sont compilés **trois fois** pour stabiliser :
- la table des matières,
- les références internes,
- les environnements `minted`.

Les PDF générés sont déplacés dans `src/pdf/`.

---

## 4. Attestation cryptographique

Le workflow génère :

### `attestation_report.txt`
Contient :
- la liste des PDF,
- leurs empreintes SHA‑256,
- un message si aucun PDF n’a été généré.

### `build_metadata.txt`
Contient :
- SHA du commit
- Branche
- Date UTC
- Liste des PDF
- SHA‑256 des PDF
- Informations de provenance

**Garanties :**
- Intégrité vérifiable
- Traçabilité complète
- Archivage scientifique fiable

---

## 5. Attestation SLSA v1

Le workflow utilise :


pour certifier :
- `.tex`
- `.thy`
- `.pdf`

**Garanties :**
- Provenance certifiée
- Authenticité du build
- Intégrité cryptographique
- Documents natifs du dépôt

---

## 6. Artifacts publiés

| Artifact | Contenu | Utilité |
|---------|---------|---------|
| `pdf-documents` | Tous les PDF générés | Téléchargement |
| `attestation-report` | SHA‑256 des PDF | Vérification |
| `build-metadata` | Métadonnées du build | Audit & archivage |

---

## 7. Chaîne complète du workflow

1. Checkout du dépôt  
2. Installation TeX Live minimal  
3. Installation Isabelle 2024  
4. Certification des 5 théories HOL  
5. Compilation des 7 documents LaTeX  
6. Déplacement des PDF  
7. Génération des SHA‑256  
8. Rapport d’attestation  
9. Métadonnées du build  
10. Attestation SLSA v1  
11. Publication des artifacts  
12. Mise à jour automatique du CHANGELOG (si `.git/.note` existe)

---

## 8. Résultat final

Le pipeline garantit :

- une **reproductibilité scientifique totale**,  
- une **certification formelle** des théories HOL,  
- une **attestation cryptographique** des PDF,  
- une **provenance certifiée SLSA**,  
- une **traçabilité complète** de chaque document.

Ce dépôt constitue ainsi une chaîne de production scientifique robuste, transparente et vérifiable.
