#!/usr/bin/env bash
set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
NOTE_FILE="$REPO_ROOT/.pending_note"

echo "=== Note pour le CHANGELOG ==="
echo ""

BUILD_HASH="$(git rev-parse --short HEAD 2>/dev/null || echo 'local')"
TODAY="$(date '+%Y-%m-%d')"

read -p "1. Titre de la mise a jour : " TITLE
read -p "2. Resume des modifications : " SUMMARY
read -p "3. Date (YYYY-MM-DD) [$TODAY] : " DATE

TITLE="${TITLE:-Mise a jour $BUILD_HASH}"
SUMMARY="${SUMMARY:-Modifications au depot.}"
DATE="${DATE:-$TODAY}"

cat > "$NOTE_FILE" <<EOF
TITLE=$TITLE
SUMMARY=$SUMMARY
DATE=$DATE
HASH=$BUILD_HASH
EOF

echo ""
echo "Note enregistree dans : .pending_note"
echo "  Titre   : $TITLE"
echo "  Resume  : $SUMMARY"
echo "  Date    : $DATE"
echo ""
echo "La note sera integree au CHANGELOG lors du prochain push."
echo "N'oubliez pas de commiter .pending_note avec vos modifications :"
echo "  git add .pending_note && git commit -m \"$TITLE\" && git push"
