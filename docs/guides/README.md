# Théorie Mathématique Philippe Thomas Savard — 2026
*Formalisation, démonstrations, documentation et génération IA.*

Bienvenue sur le site officiel du projet **Théorie Mathématique Philippe Thomas Savard — 2026**.  
Ce dépôt rassemble l’ensemble des travaux mathématiques, logiques, computationnels et documentaires liés à la théorie, ainsi que les outils permettant leur compilation, leur vérification et leur diffusion.

---

##  Présentation du projet

Ce projet vise à :

- formaliser la théorie mathématique dans **Isabelle/HOL**  
- produire automatiquement les documents scientifiques en **LaTeX**  
- générer un système intelligent de **Questions/Réponses** basé sur IA  
- fournir un pipeline complet, reproductible et attesté  
- documenter chaque aspect de la théorie et de son architecture  

Le dépôt est conçu pour être **transparent**, **traçable**, **scientifique**, et **pédagogique**.

---

##  Structure du dépôt

###  1. Théories Isabelle/HOL
Dossier : `src/hol/`

Contient les fichiers `.thy` définissant :

- les axiomes  
- les structures mathématiques  
- les méthodes de démonstration  
- les théorèmes formalisés  

La compilation est automatisée via GitHub Actions.

---

###  2. Documents LaTeX
Dossier : `src/tex/`

Contient les documents scientifiques principaux :

- *Espace de Philippot*  
- *Géométrie du spectre premier*  
- *Philosophy geometry of prime number*  
- *Postulat de l’univers carré*  
- etc.

Les PDF générés sont déposés dans `src/pdf/`.

---

###  3. Système IA de Questions/Réponses
Dossiers : `scripts/`, `qa_output/`, `qa_bank/`

Fonctionnalités :

- extraction automatique des contenus  
- génération IA des Q&R  
- base de données SQLite  
- validation interactive  
- configuration modulaire  

Le script principal est : `scripts/qa_generator.py`.

---

###  4. Documentation
Dossier : `docs/`

Inclut :

- guides de compilation  
- architecture du projet  
- documentation du système IA  
- guide HOL  
- guide sécurité  

Ce dossier sert également de **racine GitHub Pages**.

---

###  5. Pipelines GitHub Actions
Dossier : `.github/workflows/`

- `build.yml` → pipeline principal  
- compilation Isabelle  
- compilation LaTeX  
- génération des PDF  
- génération des Q&R  
- attestations SLSA  
- mise à jour automatique du CHANGELOG  

---

###  6. Archives
Dossier : `archive/`

Contient :

- rapports d’attestation  
- métadonnées de build  
- versions compressées  
- anciennes bases de données  

---

###  7. Illustrations
Dossier : `assets/images/`

Images scientifiques utilisées dans les documents et la documentation.

---

##  Pipeline de compilation

### Compilation Isabelle
```bash
isabelle build -v -d src/hol Univers_Au_Carre

Compilation LaTeX
Automatique via GitHub Actions.

Génération IA des Q&R
bash
cd scripts
python qa_generator.py
 Sécurité

# Système de Génération de Questions/Réponses Intelligent
 
## Théorie Mathématique Philippe Thomas Savard 2026

Ce système génère automatiquement des questions et réponses basées sur le contenu de la documentation mathématique contenue dans le dépôt du GitHub. Il apprend des validations et documents explicatifs pour améliorer la qualité des chapitres de la théorie déjà existants et de ceux qui sont a venirs. Facilitant les contributeurs qui souhaitent contribuer a l'information du dépôt et de sa théorie qui a l'aide du système peuvent simplement contribuer en mettant en route le build du workflow dans Actions du GitHub et ainsi contribué. Ils ont un impacte de cette manière sur le contenu de la banque de questions et de réponses et par conséquent sur la théorie en ajoutant celles-ci a la banque évolutive. Bienvenu aux contributeurs !

---

##  Structure des fichiers

```
votre-depot/
├── .github/
│   └── workflows/
│       └── build.yml            # Workflow unifié (Build + Q&R)
├── scripts/
│   ├── qa_config.py             # Configuration du système
│   ├── qa_database.py           # Gestion de la banque SQLite
│   ├── qa_generator.py          # Générateur principal
│   ├── qa_validator.py          # Outil de validation manuelle
│   ├── qa_wolfram.py            # Intégration Wolfram (optionnel)
│   └── requirements.txt         # Dépendances Python
├── qa_bank/
│   └── qa_bank.db               # Base de données SQLite
└── qa_output/                   # Dossier des Q&R générées
```

---

##  Installation

### 1. Ajouter les fichiers à votre dépôt

Copiez tous les fichiers dans votre dépôt en respectant la structure ci-dessus.

### 2. Configurer le secret GitHub

1. Allez dans **Settings** → **Secrets and variables** → **Actions**
2. Créez un nouveau secret nommé `EMERGENT_LLM_KEY`
3. Collez votre clé Emergent: '...'

### 3. Le workflow est déjà intégré

Le fichier `build.yml` contient maintenant votre workflow existant PLUS la génération Q&R.
Il suffit de remplacer votre `build.yml` actuel par celui fourni.

---

##  Flux de travail

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

Plus l'utilisateur valide de Q&R, plus le système apprend:
- Les patterns de questions qui fonctionnent bien.
- Les concepts clés de la théorie.
- Le style de réponses recherché.

Ces informations sont utilisées pour améliorer les futures générations.

---

##  Configuration

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

##  Base de données

La banque SQLite (`qa_bank/qa_bank.db`) contient:

| Table | Description |
|-------|-------------|
| `qa_validated` | Q&R validées et utilisables |
| `qa_pending` | Q&R en attente de validation |
| `learned_patterns` | Patterns appris pour améliorer la génération |
| `generation_history` | Historique des générations |
| `key_concepts` | Concepts clés extraits des documents |

---

##  Clé API

Le système utilise la **clé Emergent** qui donne accès à OpenAI GPT-4o.

- **Variable d'environnement**: `EMERGENT_LLM_KEY`
- **Dans GitHub**: Secret `EMERGENT_LLM_KEY`

Pour vérifier votre solde ou recharger:
- Accédez à **Profile** → **Universal Key** → **Add Balance**

---

##  Exemple de Q&R générée

### Question (Mathématique)
> Expliquez le théorème principal de la théorie "L'Univers est au Carré" et démontrez comment il relie les concepts géométriques aux structures algébriques.

### Réponse
> Le théorème principal établit que toute structure géométrique peut être représentée par une transformation quadratique...
> 
> [Démonstration formelle avec équations LaTeX]

---

##  Dépannage

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

##  Licence

Ce système fait partie de la documentation de la Théorie Mathématique Philippe Thomas Savard 2026.
Licence: Apache-2.0 (comme le dépôt principal)

---

##  Crédits

- **Auteur de la théorie**: Philippe Thomas Savard
- **Système Q&R**: Généré avec l'aide d'Emergent AI
- **LLM**: OpenAI GPT-4o via Emergent Universal Key



📄 Licence
Le projet est distribué sous licence Apach 2.0.

🧭 Objectif global
Ce dépôt constitue un environnement complet pour :

formaliser la théorie

produire les documents

vérifier les démonstrations

générer des contenus pédagogiques

assurer la reproductibilité scientifique

🎉 Bienvenue dans la théorie 2026

Les workflows automatisés
Les 3 workflows automatisés sont toujours en place et fonctionnent:

Quotidien (10h UTC): 3 Q&R auto-générées et auto-validées
Hebdomadaire (vendredi 14h UTC): Propositions .tex/.thy

Mensuel (1er du mois 9h UTC): Rapport de maintenance