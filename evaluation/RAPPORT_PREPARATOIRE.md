# Rapport preparatoire : Points d'evaluation

## L'Univers est au Carre -- Philippe Thomas Savard
## Preparation avant lancement de l'evaluation finale

Ce document liste **tous les points** sur lesquels le systeme d'evaluation portera.
Utilisez-le pour preparer votre depot avant de lancer le workflow `Academic Evaluation`.

---

## Score preliminaire actuel : 85.5 / 100 (Grade A)

| Axe | Score actuel | Max | Points a gagner |
|-----|-------------|-----|-----------------|
| A - Rigueur mathematique | 20.0 | 20 | 0 (maximum atteint) |
| B - Verification HOL | 13.0 | 20 | **7 points** |
| C - Qualite redactionnelle | 14.0 | 15 | 1 point |
| D - Coherence et originalite | 13.0 | 15 | 2 points |
| E - Philosophie | 9.0 | 10 | 1 point |
| F - Infrastructure CI/CD | 10.0 | 10 | 0 (maximum atteint) |
| G - Couverture corpus | 6.5 | 10 | **3.5 points** |

---

## AXE A : Rigueur mathematique (20/20) -- MAXIMUM ATTEINT

Fichiers evalues : 6 `.thy` + 10 `.tex`

| Critere | Ce qui est mesure | Votre score | Seuil max |
|---------|-------------------|-------------|-----------|
| A1. Definitions formelles | Nombre de `definition` dans les .thy | 258 defs | >= 50 -> 5/5 |
| A2. Axiomatisations | Nombre de `axiom`, `assumes` | 73 | >= 20 -> 4/4 |
| A3. Structure logique | Nombre de `locale` | 20 | >= 8 -> 4/4 |
| A4. Notation LaTeX | Equations inline + align + equation | 1212 | >= 200 -> 4/4 |
| A5. Exemples numeriques | Mentions "exemple", "validation", etc. | 330 | >= 30 -> 3/3 |

**Rien a ameliorer ici.**

---

## AXE B : Verification formelle HOL (13/20) -- PRIORITE HAUTE

| Critere | Ce qui est mesure | Votre score | Comment gagner des points |
|---------|-------------------|-------------|---------------------------|
| B1. Compilation | return_code = 0 dans Univers_Au_Carre.db | 5/5 | OK |
| B2. Sorry restants | Nombre de `sorry` dans les .thy | 2/5 (8 sorry) | **Reduire les sorry** : 0 sorry = 5/5, <= 3 = 4/5 |
| B3. Ratio preuves/propositions | proof / (lemma + theorem) | 3/5 | Ajouter des blocs `proof ... qed` |
| B4. Tactiques | simp, auto, sledgehammer, etc. | 1/3 | Utiliser davantage de tactiques Isabelle |
| B5. Theories compilees | Theories dans isabelle_exports | 2/2 | OK (7 theories) |

**Actions recommandees :**
1. Completer les 8 `sorry` dans `Philippot_Method.thy` avec `sledgehammer` (--> jusqu'a +3 points)
2. Ajouter des tactiques variees (auto, blast, force, arith) --> +1-2 points
3. Le ratio preuves/propositions augmentera naturellement en completant les sorry

**Fichier concerne :** `src/hol/Philippot_Method.thy` (8 sorry sur 8 total)

---

## AXE C : Qualite redactionnelle (14/15)

| Critere | Votre score | Comment gagner le point restant |
|---------|-------------|--------------------------------|
| C1. Structure | 4/4 | OK (374 sections + sous-sections) |
| C2. Figures | 2/3 | **Ajouter des figures** (includegraphics) : >= 15 = 3/3 |
| C3. References | 3/3 | OK |
| C4. Bilinguisme | 3/3 | OK (FR + EN) |
| C5. Volume | 2/2 | OK (744 Ko total) |

**Action recommandee :**
- Ajouter quelques `\includegraphics` dans les .tex (figures geometriques, diagrammes)

---

## AXE D : Coherence et originalite (13/15)

| Critere | Votre score | Comment gagner des points |
|---------|-------------|---------------------------|
| D1. Liens HOL <-> LaTeX | 4/5 | Mentionner davantage les noms des .thy dans les .tex |
| D2. Originalite | 4/4 | OK (9/11 concepts originaux trouves) |
| D3. Progression logique | 3/3 | OK (6/6 etapes presentes) |
| D4. Consistance notations | 2/3 | Uniformiser les notations Rs, 1/k entre fichiers |

**Actions recommandees :**
- Dans les .tex, mentionner explicitement les noms de theories : `methode_spectral.thy`, `postulat_carre.thy`, etc.
- S'assurer que `Rs = 1/(k-1)` est defini de maniere consistante partout

---

## AXE E : Philosophie et epistemologie (9/10)

| Critere | Votre score | Comment gagner le point restant |
|---------|-------------|--------------------------------|
| E1. Presence | 2.5/3 | Ajouter un 4e document philosophique (>= 3 = 3/3) |
| E2. Profondeur | 3/3 | OK (9/12 concepts trouves) |
| E3. Lien philo-math | 2/2 | OK |
| E4. Originalite | 1.5/2 | Mentionner davantage "isossophie" ou "idioschizophrenie" |

**Actions recommandees :**
- Verifier que les termes "isossophie" et "idioschizophrenie" sont bien presents dans au moins 3 des documents philosophiques

---

## AXE F : Infrastructure CI/CD (10/10) -- MAXIMUM ATTEINT

| Critere | Votre score |
|---------|-------------|
| F1. Workflows | 3/3 (4 workflows) |
| F2. Scripts | 3/3 (9 scripts Python) |
| F3. Attestation | 2/2 (metadata + SHA-256) |
| F4. Bases SQLite | 2/2 (corpus.db + qa_bank.db) |

**Rien a ameliorer ici.**

---

## AXE G : Couverture et completude (6.5/10) -- PRIORITE MOYENNE

| Critere | Votre score | Comment gagner des points |
|---------|-------------|---------------------------|
| G1. Correspondances | 2/3 | Aligner les noms .tex/.thy/.pdf |
| G2. Banque Q&R | 0.5/2 | **Generer plus de Q&R** (>= 20 = 1.5/2, >= 50 = 2/2) |
| G3. Arborescences | 2/2 | OK (4 arborescences + README) |
| G4. Volume total | 2/3 | Atteindre >= 400 pages PDF ET >= 3000 lignes HOL |

**Actions recommandees :**
1. Lancer le workflow `auto-daily-qa` plusieurs fois pour generer plus de Q&R dans qa_bank.db
2. Augmenter le volume HOL (actuellement ~4466 lignes, bien, mais les pages PDF comptent aussi)
3. S'assurer que `pdf_structure` dans corpus.db contient >= 400 pages

---

## Resume des actions prioritaires

| Priorite | Action | Gain potentiel |
|----------|--------|----------------|
| 1 (HAUTE) | Completer les 8 sorry dans Philippot_Method.thy | +3 a +5 pts (Axe B) |
| 2 (HAUTE) | Generer plus de Q&R (lancer auto-daily-qa) | +1 a +1.5 pts (Axe G) |
| 3 (MOYENNE) | Ajouter des tactiques Isabelle variees | +1 a +2 pts (Axe B) |
| 4 (MOYENNE) | Mentionner les .thy dans les .tex | +1 pt (Axe D) |
| 5 (BASSE) | Ajouter des figures dans les .tex | +1 pt (Axe C) |
| 6 (BASSE) | Uniformiser les notations Rs/1/k | +1 pt (Axe D) |

**Score potentiel apres corrections : ~93-95/100 (Grade A+)**

---

## Comment lancer l'evaluation

1. Allez dans l'onglet **Actions** de votre depot GitHub
2. Cliquez sur **Academic Evaluation** dans la liste des workflows
3. Cliquez **Run workflow**
4. Choisissez `use_llm: true` pour ajouter un commentaire qualitatif GPT-4o (optionnel)
5. Le rapport sera genere dans `evaluation/RAPPORT_EVALUATION.md`

*Ce rapport preparatoire a ete genere le 2026-04-19.*
