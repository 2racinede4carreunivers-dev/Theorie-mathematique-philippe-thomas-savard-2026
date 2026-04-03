# Système de Génération de Questions/Réponses Intelligent

## Théorie Mathématique Philippe Thomas Savard 2026

Ce système génère automatiquement des questions et réponses basées sur le contenu de votre documentation mathématique. Il apprend de vos validations pour améliorer la qualité des futures générations.

---

## 📁 Structure des fichiers

```
votre-depot/
├── .github/
│   └── workflows/
│       └── qa-generation.yml    # Workflow GitHub Actions
├── scripts/
│   ├── qa_config.py             # Configuration du système
│   ├── qa_database.py           # Gestion de la banque SQLite
│   ├── qa_generator.py          # Générateur principal
│   ├── qa_validator.py          # Outil de validation manuelle
│   └── requirements.txt         # Dépendances Python
├── qa_bank/
│   └── qa_bank.db               # Base de données SQLite
└── qa_output/                   # Dossier des Q&R générées
```

---

## 🚀 Installation

### 1. Ajouter les fichiers à votre dépôt

Copiez tous les fichiers dans votre dépôt en respectant la structure ci-dessus.

### 2. Configurer le secret GitHub

1. Allez dans **Settings** → **Secrets and variables** → **Actions**
2. Créez un nouveau secret nommé `EMERGENT_LLM_KEY`
3. Collez votre clé Emergent: `sk-emergent-c20D27d2bDa5755870`

### 3. Adapter le workflow

Dans `.github/workflows/qa-generation.yml`, modifiez la ligne:
```yaml
workflows: ["Build"]  # Remplacez par le nom exact de votre workflow de build
```

---

## 🔄 Flux de travail

### Génération automatique

1. **Vous faites un commit** avec du nouveau contenu (.tex, .thy, .pdf)
2. **Le build existant s'exécute** (compilation LaTeX, Isabelle/HOL)
3. **Le workflow Q&R se déclenche** automatiquement après le build
4. **L'IA analyse** tous les documents et génère 11 questions:
   - 10 questions mathématiques/techniques
   - 1 question philosophique/ontologique
5. **Un artifact est créé** avec les Q&R générées

### Validation manuelle

```bash
# Téléchargez l'artifact depuis GitHub Actions
# Puis utilisez le validateur:

# Lister les Q&R en attente
python scripts/qa_validator.py --list

# Voir une Q&R en détail
python scripts/qa_validator.py --show 1

# Valider des Q&R
python scripts/qa_validator.py --validate 1 2 3

# Rejeter des Q&R
python scripts/qa_validator.py --reject 4 5

# Mode interactif
python scripts/qa_validator.py --interactive

# Exporter la banque validée
python scripts/qa_validator.py --export
```

### Amélioration continue

Plus vous validez de Q&R, plus le système apprend:
- Les patterns de questions qui fonctionnent bien
- Les concepts clés de votre théorie
- Le style de réponses que vous préférez

Ces informations sont utilisées pour améliorer les futures générations.

---

## ⚙️ Configuration

### Modifier le ratio de questions (`scripts/qa_config.py`)

```python
QUESTION_RATIO = {
    "mathematique": 10,    # 90% - Questions techniques
    "philosophique": 1     # 10% - Questions ontologiques
}

QUESTIONS_PER_RUN = 11  # Total par génération
```

### Activer l'anglais

```python
LANGUAGES = {
    "fr": {"enabled": True, "name": "Français"},
    "en": {"enabled": True, "name": "English"}  # Changer False → True
}
```

### Personnaliser les catégories

```python
MATH_CATEGORIES = [
    "definition",
    "demonstration",
    "theoreme",
    # Ajoutez vos propres catégories
]
```

---

## 📊 Base de données

La banque SQLite (`qa_bank/qa_bank.db`) contient:

| Table | Description |
|-------|-------------|
| `qa_validated` | Q&R validées et utilisables |
| `qa_pending` | Q&R en attente de validation |
| `learned_patterns` | Patterns appris pour améliorer la génération |
| `generation_history` | Historique des générations |
| `key_concepts` | Concepts clés extraits des documents |

---

## 🔑 Clé API

Le système utilise la **clé Emergent** qui donne accès à OpenAI GPT-4o.

- **Variable d'environnement**: `EMERGENT_LLM_KEY`
- **Dans GitHub**: Secret `EMERGENT_LLM_KEY`

Pour vérifier votre solde ou recharger:
- Accédez à **Profile** → **Universal Key** → **Add Balance**

---

## 📝 Exemple de Q&R générée

### Question (Mathématique)
> Expliquez le théorème principal de la théorie "L'Univers est au Carré" et démontrez comment il relie les concepts géométriques aux structures algébriques.

### Réponse
> Le théorème principal établit que toute structure géométrique peut être représentée par une transformation quadratique...
> 
> [Démonstration formelle avec équations LaTeX]

---

## 🆘 Dépannage

### Le workflow ne se déclenche pas
- Vérifiez que le nom du workflow dans `workflow_run.workflows` correspond exactement
- Assurez-vous que le build précédent a réussi

### Erreur de clé API
```
ERREUR: Aucune clé API trouvée
```
→ Ajoutez le secret `EMERGENT_LLM_KEY` dans GitHub

### Aucun document trouvé
→ Vérifiez que vos fichiers .tex et .thy sont dans les dossiers `src/tex` et `src/hol`

---

## 📜 Licence

Ce système fait partie de la documentation de la Théorie Mathématique Philippe Thomas Savard 2026.
Licence: Apache-2.0 (comme le dépôt principal)

---

## 🙏 Crédits

- **Auteur de la théorie**: Philippe Thomas Savard
- **Système Q&R**: Généré avec l'aide d'Emergent AI
- **LLM**: OpenAI GPT-4o via Emergent Universal Key
