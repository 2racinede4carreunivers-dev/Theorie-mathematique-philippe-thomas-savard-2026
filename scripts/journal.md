#!/usr/bin/env bash
set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
JOURNAL="$REPO_ROOT/JOURNAL.md"
TEMP_FILE="$(mktemp)"

echo "=== Création d'une entrée pour JOURNAL.md ==="
echo ""

# Questions professionnelles
read -p "1. Quelle modification ai-je apportée dans ce commit ? " Q1
read -p "2. Quelle est la raison ou l’intention derrière ce changement ? " Q2
read -p "3. Quelle est la prochaine étape prévue en lien avec cette évolution ? " Q3

# Date du jour
DATE="$(date +%Y-%m-%d)"

# Titre automatique basé sur Q1
TITLE="$DATE — $Q1"

# Génération du bloc Markdown
ENTRY="## $TITLE
**Modification apportée :** $Q1  
**Raison du changement :** $Q2  
**Prochaine étape :** $Q3  

---
"

# Si JOURNAL.md n'existe pas, créer l'en-tête
if [ ! -f "$JOURNAL" ]; then
    echo "# Journal d’évolution du dépôt" > "$JOURNAL"
    echo "" >> "$JOURNAL"
    echo "## Table des matières" >> "$JOURNAL"
    echo "" >> "$JOURNAL"
    echo "---" >> "$JOURNAL"
    echo "" >> "$JOURNAL"
fi

# Extraire les anciennes entrées (tout après la ligne ---)
awk 'NR==1,/^---$/' "$JOURNAL" > "$TEMP_FILE"
echo "" >> "$TEMP_FILE"

# Ajouter la nouvelle entrée
echo "$ENTRY" >> "$TEMP_FILE"

# Ajouter les anciennes entrées (tout après la première occurrence de ---)
awk 'f{print} /^---$/{f=1}' "$JOURNAL" >> "$TEMP_FILE"

# Mise à jour de la table des matières
sed -i '/## Table des matières/,$d' "$TEMP_FILE"

echo "## Table des matières" >> "$TEMP_FILE"
grep "^## " "$TEMP_FILE" | sed 's/^## \(.*\)$/- [\1](#\1)/' >> "$TEMP_FILE"

echo "---" >> "$TEMP_FILE"
echo "" >> "$TEMP_FILE"

# Ajouter les entrées complètes
grep -v "^# Journal" "$JOURNAL" | grep -v "^## Table des matières" | grep -v "^---$" >> "$TEMP_FILE"

# Remplacer le fichier original
mv "$TEMP_FILE" "$JOURNAL"

echo ""
echo "Votre entrée a été ajoutée à JOURNAL.md."
