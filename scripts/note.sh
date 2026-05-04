#!/usr/bin/env bash
set -e

# Aller à la racine du dépôt, peu importe d'où le script est lancé
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

NOTE_FILE="$REPO_ROOT/.pending_note"

echo "=== Création d'une note pour le CHANGELOG ==="
echo ""

# --- Détection automatique ---
BUILD_HASH="$(git rev-parse --short HEAD 2>/dev/null || echo 'local')"
TODAY_HUMAN="$(date '+%d %B %Y %H:%M')"

# --- Questions posées à l'utilisateur ---
read -p "1. Titre de la mise à jour : " TITLE
read -p "2. Résumé des modifications : " SUMMARY
read -p "3. Date (texte libre) [$TODAY_HUMAN] : " DATE

# Valeurs par défaut si vide
TITLE="${TITLE:-Mise à jour $BUILD_HASH}"
SUMMARY="${SUMMARY:-Modifications au dépôt.}"
DATE="${DATE:-$TODAY_HUMAN}"

# --- Écriture du fichier .pending_note ---
cat > "$NOTE_FILE" <<EOF
TITLE=$TITLE
SUMMARY=$SUMMARY
DATE=$DATE
EOF

echo ""
echo "Note enregistrée dans : .pending_note"
echo "  Titre   : $TITLE"
echo "  Résumé  : $SUMMARY"
echo "  Date    : $DATE"
echo ""
echo "La note sera intégrée automatiquement au CHANGELOG lors du prochain push."
echo ""
echo "Exécute maintenant :"
echo "  git add .pending_note"
echo "  git commit -m \"$TITLE\""
echo "  git push"
