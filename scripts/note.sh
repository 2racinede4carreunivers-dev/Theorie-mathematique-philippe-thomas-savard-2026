#!/usr/bin/env bash
set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
NOTE_FILE="$REPO_ROOT/.git/.note"

echo "=== Création d'une note pour le CHANGELOG ==="
echo ""

# Trois questions essentielles
read -p "1. Quels changements avez-vous apportés ? " Q1
read -p "2. Quel est l'effet immédiat sur le dépôt ? " Q2
read -p "3. Quelle mise à jour prévoyez-vous ensuite ? " Q3

# Enregistrement de la note dans .git/.note
echo "type=\"manual\"" > "$NOTE_FILE"
echo "q1=\"$Q1\"" >> "$NOTE_FILE"
echo "q2=\"$Q2\"" >> "$NOTE_FILE"
echo "q3=\"$Q3\"" >> "$NOTE_FILE"

echo ""
echo "Votre note a été enregistrée."
echo "Elle sera intégrée automatiquement au CHANGELOG lors du prochain push."
