#!/bin/bash

# ================================
# Script note.sh — Version corrigée
# Compatible avec le workflow GitHub
# ================================

echo "----------------------------------------"
echo " Génération d'une note pour CHANGELOG.md"
echo "----------------------------------------"
echo ""

# Question 1 — Titre
read -p "Titre de la mise à jour : " TITLE

# Question 2 — Résumé
read -p "Résumé court : " SUMMARY

# Question 3 — Date (auto ou manuelle)
read -p "Date (laisser vide pour aujourd'hui) : " DATE
if [ -z "$DATE" ]; then
    DATE=$(date +%Y-%m-%d)
fi

# Écriture dans le fichier attendu par GitHub Actions
{
    echo "TITLE=$TITLE"
    echo "SUMMARY=$SUMMARY"
    echo "DATE=$DATE"
} > .pending_note

echo ""
echo "----------------------------------------"
echo " Note enregistrée dans .pending_note"
echo "----------------------------------------"
echo "Contenu écrit :"
cat .pending_note
echo ""
echo "Vous pouvez maintenant faire :"
echo "  git add ."
echo "  git commit -m \"Mise à jour note\""
echo "  git push"
echo ""
