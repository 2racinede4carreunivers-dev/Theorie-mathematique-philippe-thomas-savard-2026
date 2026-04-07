"""
Configuration pour le système de génération de Questions/Réponses
Théorie Mathématique Philippe Thomas Savard 2026
"""

# Configuration des langues
LANGUAGES = {
    "fr": {
        "enabled": True,  # Français activé par défaut
        "name": "Français"
    },
    "en": {
        "enabled": False,  # Anglais désactivé (prêt pour activation future)
        "name": "English"
    }
}

# Ratio des types de questions (sur 11 questions générées)
# 10 questions mathématiques/théoriques + 1 question philosophique/ontologique
QUESTION_RATIO = {
    "mathematique": 10,      # 90% - Structure mathématique, technique
    "philosophique": 1       # 10% - Aspect humain, philosophique, ontologique
}

# Nombre total de questions par génération
QUESTIONS_PER_RUN = 11

# Configuration des catégories de questions mathématiques
MATH_CATEGORIES = [
    "definition",           # Définitions des concepts
    "demonstration",        # Preuves et démonstrations
    "theoreme",            # Théorèmes et leurs applications
    "formule",             # Formules mathématiques
    "propriete",           # Propriétés et caractéristiques
    "application",         # Applications pratiques
    "relation",            # Relations entre concepts
    "axiome",              # Axiomes fondamentaux
    "corollaire",          # Corollaires et implications
    "notation"             # Notations et symboles
]

# Catégories philosophiques/ontologiques
PHILO_CATEGORIES = [
    "signification",       # Signification profonde de la théorie
    "impact_humain",       # Impact sur la compréhension humaine
    "vision_monde",        # Vision du monde et de l'univers
    "epistemologie",       # Aspects épistémologiques
    "ontologie"            # Nature de l'être et de l'existence
]

# Extensions de fichiers à analyser
FILE_EXTENSIONS = {
    ".tex": "LaTeX - Documentation mathématique",
    ".thy": "Isabelle/HOL - Preuves formelles",
    ".pdf": "PDF - Documents compilés (texte extrait)"
}

# Configuration du modèle OpenAI
OPENAI_CONFIG = {
    "model": "gpt-4o",
    "temperature": 0.7,
    "max_tokens": 4000
}

# Chemins par défaut dans le dépôt
REPO_PATHS = {
    "tex_dir": "src/tex",
    "hol_dir": "src/hol", 
    "pdf_dir": "src/pdf",
    "docs_dir": "docs"
}

# Configuration de la base de données SQLite
DATABASE_CONFIG = {
    "db_path": "qa_bank/qa_bank.db",
    "backup_enabled": True,
    "backup_path": "qa_bank/backups"
}

# Niveaux de difficulté des questions
DIFFICULTY_LEVELS = [
    "debutant",        # Concepts de base
    "intermediaire",   # Compréhension approfondie
    "avance",          # Maîtrise complète
    "expert"           # Questions de recherche
]

# Configuration de la qualité des réponses
ANSWER_QUALITY = {
    "include_references": True,     # Inclure les références aux fichiers source
    "include_equations": True,      # Inclure les équations LaTeX
    "include_context": True,        # Inclure le contexte théorique
    "max_answer_length": 2000       # Longueur maximale des réponses (caractères)
}

# Tags pour la classification des Q&R
TAGS = [
    "univers_carre",
    "geometrie",
    "algebre", 
    "analyse",
    "topologie",
    "isabelle_hol",
    "demonstration_formelle",
    "theoreme_principal",
    "corollaire",
    "application",
    "philosophie",
    "ontologie"
]
