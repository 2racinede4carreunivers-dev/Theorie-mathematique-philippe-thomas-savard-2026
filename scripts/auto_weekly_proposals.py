#!/usr/bin/env python3
"""
Script de generation des propositions hebdomadaires
Execute par le workflow GitHub Actions auto-weekly-proposals.yml
"""

import os
import sys
import json
import asyncio
import sqlite3
from datetime import datetime
from pathlib import Path


async def generate_weekly_proposal():
    """Genere une proposition d'amelioration basee sur les Q&R recentes."""

    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
    except ImportError:
        os.system("pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/")
        from emergentintegrations.llm.chat import LlmChat, UserMessage

    api_key = os.environ.get("EMERGENT_LLM_KEY")
    if not api_key:
        print("Cle API non trouvee")
        return False

    date_str = datetime.now().strftime('%Y-%m-%d')
    print(f"Generation des propositions hebdomadaires - {date_str}")

    # Lire les Q&R validees recentes
    qa_content = ""
    rows = []
    db_path = Path('qa_bank/qa_bank.db')

    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Verifier si created_at existe
        cursor.execute('PRAGMA table_info(qa_validated)')
        columns = [col[1] for col in cursor.fetchall()]

        if 'created_at' in columns:
            cursor.execute('''
                SELECT question, answer, category, subcategory
                FROM qa_validated
                ORDER BY created_at DESC
                LIMIT 21
            ''')
        else:
            cursor.execute('''
                SELECT question, answer, category, subcategory
                FROM qa_validated
                ORDER BY id DESC
                LIMIT 21
            ''')

        rows = cursor.fetchall()
        conn.close()

        if rows:
            qa_content = "\n\n".join([
                f"Q: {r[0]}\nR: {r[1]}\nCategorie: {r[2]}/{r[3]}"
                for r in rows
            ])
            print(f"  - {len(rows)} Q&R recentes trouvees")

    if not qa_content:
        print("Pas assez de Q&R pour generer des propositions")
        return False

    # Lister les fichiers .tex et .thy
    files_info = []
    for ext in ['.tex', '.thy']:
        for f in Path('.').rglob(f'*{ext}'):
            if '.git' not in str(f):
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    files_info.append({
                        'path': str(f),
                        'name': f.name,
                        'type': ext,
                        'preview': content[:2000]
                    })
                except Exception:
                    pass

    if not files_info:
        print("Aucun fichier .tex ou .thy trouve")
        return False

    print(f"  - {len(files_info)} fichiers .tex/.thy trouves")

    # Choisir un fichier (rotation basee sur la semaine)
    week_num = datetime.now().isocalendar()[1]
    file_index = week_num % len(files_info)
    target_file = files_info[file_index]

    print(f"  - Fichier selectionne: {target_file['name']}")

    # Generer la proposition
    chat = LlmChat(
        api_key=api_key,
        session_id=f"proposal-{date_str}",
        system_message="""Tu es un expert en mathematiques et en redaction scientifique.
Ta tache est d'analyser les Q&R recentes et de proposer des ameliorations pour un fichier .tex ou .thy.
Tes propositions doivent etre:
- Precises et applicables
- Basees sur les nouvelles informations des Q&R
- Respectueuses du style et de la structure existante du fichier"""
    ).with_model("openai", "gpt-4o")

    prompt = f"""Analyse les Q&R recentes de la banque et propose des ameliorations pour le fichier "{target_file['name']}".

## Q&R RECENTES (nouvelles connaissances):
{qa_content[:6000]}

## FICHIER A AMELIORER ({target_file['type']}):
{target_file['preview']}

## TA TACHE:
1. Identifie les concepts des Q&R qui pourraient enrichir ce fichier
2. Propose 2-3 ameliorations concretes (nouvelles sections, clarifications, preuves)
3. Pour chaque proposition, donne le code {target_file['type']} exact a ajouter ou modifier

Reponds en Markdown structure."""

    try:
        print("  - Appel API en cours...")
        response = await chat.send_message(UserMessage(text=prompt))

        # Sauvegarder la proposition
        proposals_dir = Path('proposals')
        proposals_dir.mkdir(exist_ok=True)

        proposal_file = proposals_dir / f"proposal_{date_str}_{target_file['name']}.md"

        proposal_content = f"""# Proposition d'amelioration - {date_str}

## Fichier cible: `{target_file['path']}`

## Base sur: {len(rows)} Q&R recentes de la banque

---

{response}

---

*Genere automatiquement par le workflow hebdomadaire*
"""

        proposal_file.write_text(proposal_content, encoding='utf-8')
        print(f"Proposition sauvegardee: {proposal_file}")

        return True

    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    success = asyncio.run(generate_weekly_proposal())
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
