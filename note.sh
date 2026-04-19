#!/usr/bin/env bash
set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
NOTE_FILE="$REPO_ROOT/.git/.note"

echo "=== Création d'une note pour le CHANGELOG ==="
echo ""

# --- Détection automatique du build ---
BUILD_HASH="$(git rev-parse --short HEAD)"
BUILD_LINK="# build $BUILD_HASH"

# --- Détection automatique du tag existant ---
CURRENT_TAG="$(git describe --tags --abbrev=0 2>/dev/null || true)"

# --- Génération automatique du tag intelligent ---
TODAY="$(date '+%Y.%m.%d')"
TAG_PREFIX="v$TODAY"

# Trouver le prochain numéro disponible
N=1
while git rev-parse "$TAG_PREFIX.$N" >/dev/null 2>&1; do
    N=$((N+1))
done

AUTO_TAG="$TAG_PREFIX.$N"

# --- Questions posées à l'utilisateur ---
read -p "1. Titre de la note (titre du commit) : " TITLE
read -p "2. Résumé de la mise à jour : " SUMMARY
read -p "3. Date de la mise à jour (YYYY-MM-DD) [$(date '+%Y-%m-%d')] : " DATE

# Valeurs par défaut si vide
TITLE="${TITLE:-Commit $BUILD_HASH du $(date '+%Y-%m-%d') ($AUTO_TAG)}"
SUMMARY="${SUMMARY:-Mise à jour automatique du commit $BUILD_HASH.}"
DATE="${DATE:-$(date '+%Y-%m-%d')}"

# --- Enregistrement structuré ---
{
    echo "type=\"manual\""
    echo "title=\"$TITLE $BUILD_LINK\""
    echo "summary=\"$SUMMARY\""
    echo "date=\"$DATE\""
    echo "tag=\"$AUTO_TAG\""
    echo "previous_tag=\"$CURRENT_TAG\""
} > "$NOTE_FILE"

echo ""
echo "Votre note a été enregistrée dans : $NOTE_FILE"
echo "Tag généré automatiquement : $AUTO_TAG"
echo "Ancien tag détecté : ${CURRENT_TAG:-aucun}"
echo "Elle sera intégrée automatiquement au CHANGELOG lors du prochain push."
