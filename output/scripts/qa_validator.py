#!/usr/bin/env python3
"""
Script de validation manuelle des Questions/Réponses générées.
À utiliser localement pour sélectionner les Q&R à ajouter à la banque validée.

Usage:
    python qa_validator.py                    # Mode interactif
    python qa_validator.py --list             # Liste les Q&R en attente
    python qa_validator.py --validate 1 2 3   # Valide les IDs spécifiés
    python qa_validator.py --reject 4 5       # Rejette les IDs spécifiés
    python qa_validator.py --export           # Exporte la banque validée
"""

import argparse
import json
import sys
from typing import List
from qa_database import QADatabase
from qa_config import DATABASE_CONFIG


def print_qa(qa: dict, show_full: bool = False):
    """Affiche une Q&R de manière formatée."""
    print(f"\n{'='*60}")
    print(f"ID: {qa.get('id')} | Catégorie: {qa.get('category')} / {qa.get('subcategory')}")
    print(f"Difficulté: {qa.get('difficulty')} | Langue: {qa.get('language')}")
    print(f"Tags: {qa.get('tags')}")
    print(f"{'='*60}")
    print(f"\n📝 QUESTION:\n{qa.get('question')}")
    
    if show_full:
        print(f"\n✅ RÉPONSE:\n{qa.get('answer')}")
    else:
        answer = qa.get('answer', '')
        print(f"\n✅ RÉPONSE (aperçu):\n{answer[:300]}..." if len(answer) > 300 else f"\n✅ RÉPONSE:\n{answer}")
    
    print(f"\n📁 Source: {qa.get('source_files')}")
    print(f"🔗 Commit: {qa.get('source_commit')}")


def list_pending(db: QADatabase):
    """Liste toutes les Q&R en attente."""
    pending = db.get_pending_qa()
    
    if not pending:
        print("\n✨ Aucune Q&R en attente de validation!")
        return
    
    print(f"\n📋 {len(pending)} Q&R en attente de validation:\n")
    
    for qa in pending:
        print(f"  [{qa['id']}] {qa['category']}/{qa['subcategory']} - {qa['question'][:60]}...")
    
    print(f"\nUtilisez 'python qa_validator.py --show <ID>' pour voir les détails")


def show_qa(db: QADatabase, qa_id: int):
    """Affiche les détails d'une Q&R."""
    pending = db.get_pending_qa()
    qa = next((q for q in pending if q['id'] == qa_id), None)
    
    if not qa:
        # Chercher dans les validées
        validated = db.get_validated_qa(limit=1000)
        qa = next((q for q in validated if q['id'] == qa_id), None)
        if qa:
            print("\n⚠️  Cette Q&R est déjà validée:")
    
    if qa:
        print_qa(qa, show_full=True)
    else:
        print(f"\n❌ Q&R avec ID {qa_id} non trouvée")


def validate_qas(db: QADatabase, ids: List[int], quality_score: float = 0.8):
    """Valide les Q&R spécifiées."""
    validated = 0
    for qa_id in ids:
        if db.validate_qa(qa_id, quality_score):
            print(f"✅ Q&R {qa_id} validée avec succès")
            validated += 1
        else:
            print(f"❌ Impossible de valider Q&R {qa_id}")
    
    print(f"\n📊 {validated}/{len(ids)} Q&R validées")


def reject_qas(db: QADatabase, ids: List[int]):
    """Rejette les Q&R spécifiées."""
    rejected = 0
    for qa_id in ids:
        if db.reject_qa(qa_id):
            print(f"🗑️  Q&R {qa_id} rejetée")
            rejected += 1
        else:
            print(f"❌ Impossible de rejeter Q&R {qa_id}")
    
    print(f"\n📊 {rejected}/{len(ids)} Q&R rejetées")


def interactive_mode(db: QADatabase):
    """Mode interactif pour valider les Q&R une par une."""
    pending = db.get_pending_qa()
    
    if not pending:
        print("\n✨ Aucune Q&R en attente de validation!")
        return
    
    print(f"\n🎯 Mode interactif - {len(pending)} Q&R à traiter")
    print("Commandes: [v]alider, [r]ejeter, [s]auter, [q]uitter\n")
    
    for qa in pending:
        print_qa(qa, show_full=True)
        
        while True:
            choice = input("\n> Action [v/r/s/q]: ").strip().lower()
            
            if choice == 'v':
                score = input("Score de qualité (0.0-1.0, défaut 0.8): ").strip()
                score = float(score) if score else 0.8
                db.validate_qa(qa['id'], score)
                print("✅ Validée!")
                break
            elif choice == 'r':
                db.reject_qa(qa['id'])
                print("🗑️  Rejetée!")
                break
            elif choice == 's':
                print("⏭️  Sautée")
                break
            elif choice == 'q':
                print("\n👋 Au revoir!")
                return
            else:
                print("❓ Commande non reconnue. Utilisez v, r, s ou q")
    
    print("\n✨ Toutes les Q&R ont été traitées!")


def export_bank(db: QADatabase, output_format: str = "both"):
    """Exporte la banque de Q&R validées."""
    import os
    os.makedirs("qa_export", exist_ok=True)
    
    if output_format in ["json", "both"]:
        json_path = db.export_validated_qa("qa_export/qa_bank_validated.json", "json")
        print(f"📄 Exporté en JSON: {json_path}")
    
    if output_format in ["markdown", "both"]:
        md_path = db.export_validated_qa("qa_export/qa_bank_validated.md", "markdown")
        print(f"📄 Exporté en Markdown: {md_path}")


def show_stats(db: QADatabase):
    """Affiche les statistiques de la banque."""
    stats = db.get_statistics()
    
    print("\n📊 STATISTIQUES DE LA BANQUE")
    print("=" * 40)
    print(f"Q&R validées:        {stats['total_validated']}")
    print(f"Q&R en attente:      {stats['total_pending']}")
    print(f"Score qualité moyen: {stats['avg_quality_score']:.2f}")
    print(f"Concepts clés:       {stats['total_concepts']}")
    print(f"Générations:         {stats['total_generations']}")
    
    if stats.get('categories'):
        print(f"\nRépartition par catégorie:")
        for cat, count in stats['categories'].items():
            print(f"  - {cat}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Gestionnaire de validation des Questions/Réponses"
    )
    
    parser.add_argument('--list', '-l', action='store_true',
                        help='Liste les Q&R en attente')
    parser.add_argument('--show', '-s', type=int,
                        help='Affiche les détails d\'une Q&R par ID')
    parser.add_argument('--validate', '-v', nargs='+', type=int,
                        help='Valide les Q&R par leurs IDs')
    parser.add_argument('--reject', '-r', nargs='+', type=int,
                        help='Rejette les Q&R par leurs IDs')
    parser.add_argument('--export', '-e', action='store_true',
                        help='Exporte la banque validée')
    parser.add_argument('--stats', action='store_true',
                        help='Affiche les statistiques')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Mode interactif')
    parser.add_argument('--quality', '-q', type=float, default=0.8,
                        help='Score de qualité pour la validation (défaut: 0.8)')
    parser.add_argument('--db', type=str, default=DATABASE_CONFIG["db_path"],
                        help='Chemin de la base de données')
    
    args = parser.parse_args()
    
    # Initialiser la base de données
    db = QADatabase(args.db)
    
    # Exécuter l'action demandée
    if args.list:
        list_pending(db)
    elif args.show:
        show_qa(db, args.show)
    elif args.validate:
        validate_qas(db, args.validate, args.quality)
    elif args.reject:
        reject_qas(db, args.reject)
    elif args.export:
        export_bank(db)
    elif args.stats:
        show_stats(db)
    elif args.interactive:
        interactive_mode(db)
    else:
        # Par défaut, afficher l'aide et les stats
        parser.print_help()
        print("\n")
        show_stats(db)


if __name__ == "__main__":
    main()
