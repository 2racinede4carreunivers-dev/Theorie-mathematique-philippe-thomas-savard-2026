# PRD - Système de Q&R Intelligent pour Théorie Mathématique Savard

## Date: 2026-04-03

## Problème Original
Création d'un système de génération automatique de questions/réponses évolutif et intelligent pour le dépôt GitHub de la Théorie Mathématique Philippe Thomas Savard 2026, intégré au workflow GitHub Actions existant.

## Architecture
- **Scripts Python**: Génération via OpenAI GPT-4o (clé Emergent)
- **Base de données**: SQLite pour la banque de Q&R
- **Workflow**: GitHub Actions déclenché après le build existant
- **Enrichissement optionnel**: Wolfram Alpha API

## Choix Utilisateur
- Clé API: Emergent Universal Key
- Format banque: SQLite
- Ratio Q&R: 90% mathématique / 10% philosophique (11 questions par run)
- Langue: Français par défaut (anglais préparé mais désactivé)
- Wolfram: Optionnel (gratuit limité)

## Fichiers Générés
1. `scripts/qa_config.py` - Configuration
2. `scripts/qa_database.py` - Gestion SQLite intelligente
3. `scripts/qa_generator.py` - Générateur principal avec OpenAI
4. `scripts/qa_validator.py` - Outil CLI de validation
5. `scripts/qa_wolfram.py` - Intégration Wolfram (optionnel)
6. `scripts/requirements.txt` - Dépendances
7. `.github/workflows/qa-generation.yml` - Workflow GitHub Actions
8. `README_QA_SYSTEM.md` - Documentation complète

## Ce qui est implémenté
- Génération automatique de Q&R via GPT-4o
- Banque SQLite avec apprentissage des patterns
- Détection des doublons
- Validation manuelle interactive
- Export JSON/Markdown
- Workflow GitHub Actions complet
- Support multilingue (FR actif, EN préparé)

## Backlog / Améliorations Futures
- P1: Activer l'intégration Wolfram Alpha complète
- P2: Interface web pour la validation
- P3: Génération de flashcards Anki
- P4: API REST pour accès externe à la banque
