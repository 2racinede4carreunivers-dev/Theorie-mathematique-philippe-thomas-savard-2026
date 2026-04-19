# Rapport preparatoire v2 : Points d'evaluation detailles

## Score actuel : 74.3 / 100 (Revisions majeures requises)

| Fichier | Score | Points a gagner |
|---------|-------|-----------------|
| methode_spectral.thy | 19/20 | 1 |
| espace_philippot.thy | 16/20 | 4 |
| mecanique_discret.thy | 15/20 | 5 |
| methode_de_philippot.thy | 14/20 | 6 |
| postulat_carre.thy | 14/20 | 6 |
| geometrie_spectre_premier.thy | 13/20 | 7 |
| infini_parti.thy | 13/20 | 7 |

## Actions prioritaires pour augmenter le score

| Priorite | Action | Fichier(s) | Gain |
|----------|--------|------------|------|
| 1 | Reduire les axiomatisations dans methode_spectral (15 blocs) | methode_spectral.thy | +1-2 pts |
| 2 | Eliminer les constantes flottantes | espace_philippot, mecanique_discret, postulat_carre | +1-3 pts |
| 3 | Ajouter des lemmes prouves dans geometrie_spectre_premier | geometrie_spectre_premier.thy | +2-4 pts |
| 4 | Ajouter des lemmes dans les locales de infini_parti | infini_parti.thy | +2-4 pts |
| 5 | Generer plus de Q&R (>= 20) | qa_bank.db | +1 pt (Axe G) |

## Comment lancer l'evaluation

1. Onglet **Actions** > **Academic Evaluation** > **Run workflow**
2. Choisir `use_llm: true` pour evaluation GPT-4o (optionnel)
3. Le rapport sera commite dans `evaluation/RAPPORT_EVALUATION.md`
