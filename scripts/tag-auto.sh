#!/usr/bin/env bash
set -e

# Génération du tag intelligent basé sur la date
TODAY="$(date '+%Y.%m.%d')"
TAG_PREFIX="v$TODAY"

# Trouver le prochain numéro disponible
N=1
while git rev-parse "$TAG_PREFIX.$N" >/dev/null 2>&1; do
    N=$((N+1))
done

TAG="$TAG_PREFIX.$N"

echo "Création du tag : $TAG"

git tag "$TAG"
git push origin "$TAG"

echo "Tag créé et poussé avec succès."
