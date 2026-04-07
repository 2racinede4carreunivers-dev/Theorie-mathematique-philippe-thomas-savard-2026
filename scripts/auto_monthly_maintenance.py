#!/usr/bin/env python3
"""
Script de maintenance mensuelle du depot
Execute par le workflow GitHub Actions auto-monthly-maintenance.yml
"""

import os
import sys
import json
import asyncio
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path


async def monthly_maintenance():
    """Execute la maintenance mensuelle et genere un rapport."""

    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
    except ImportError:
        os.system("pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/")
        from emergentintegrations.llm.chat import LlmChat, UserMessage

    api_key = os.environ.get("EMERGENT_LLM_KEY")
    if not api_key:
        print("Cle API non trouvee")
        return False

    date_str = datetime.now().strftime('%Y-%m')
    print(f"Maintenance mensuelle - {date_str}")

    # 1. Analyse de la structure du depot
    print("\n1. Analyse de la structure du depot...")

    structure = {
        'tex_files': [],
        'thy_files': [],
        'pdf_files': [],
        'md_files': [],
        'py_files': [],
    }

    for f in Path('.').rglob('*.tex'):
        if '.git' not in str(f):
            structure['tex_files'].append(str(f))
    for f in Path('.').rglob('*.thy'):
        if '.git' not in str(f):
            structure['thy_files'].append(str(f))
    for f in Path('.').rglob('*.pdf'):
        if '.git' not in str(f):
            structure['pdf_files'].append(str(f))
    for f in Path('.').rglob('*.md'):
        if '.git' not in str(f):
            structure['md_files'].append(str(f))
    if Path('scripts').exists():
        for f in Path('scripts').rglob('*.py'):
            structure['py_files'].append(str(f))

    print(f"  - Fichiers .tex: {len(structure['tex_files'])}")
    print(f"  - Fichiers .thy: {len(structure['thy_files'])}")
    print(f"  - Fichiers .pdf: {len(structure['pdf_files'])}")
    print(f"  - Fichiers .md: {len(structure['md_files'])}")
    print(f"  - Scripts Python: {len(structure['py_files'])}")

    # 2. Statistiques de la banque Q&R
    print("\n2. Statistiques de la banque Q&R...")
    qa_stats = {'validated': 0, 'pending': 0, 'concepts': 0}

    if Path('qa_bank/qa_bank.db').exists():
        conn = sqlite3.connect('qa_bank/qa_bank.db')
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT COUNT(*) FROM qa_validated')
            qa_stats['validated'] = cursor.fetchone()[0]
        except Exception:
            pass

        try:
            cursor.execute('SELECT COUNT(*) FROM qa_pending')
            qa_stats['pending'] = cursor.fetchone()[0]
        except Exception:
            pass

        try:
            cursor.execute('SELECT COUNT(*) FROM key_concepts')
            qa_stats['concepts'] = cursor.fetchone()[0]
        except Exception:
            pass

        conn.close()

    print(f"  - Q&R validees: {qa_stats['validated']}")
    print(f"  - Q&R en attente: {qa_stats['pending']}")
    print(f"  - Concepts cles: {qa_stats['concepts']}")

    # 3. Commits du mois dernier
    print("\n3. Activite du mois...")
    commits = []
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', '--since=1 month ago'],
            capture_output=True, text=True
        )
        commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        print(f"  - Commits ce mois: {len(commits)}")
    except Exception:
        pass

    # 4. Fichiers modifies recemment
    print("\n4. Fichiers modifies recemment...")
    modified_files = []
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~10'],
            capture_output=True, text=True
        )
        modified_files = [f for f in result.stdout.strip().split('\n') if f]
        print(f"  - Fichiers modifies: {len(modified_files)}")
    except Exception:
        pass

    # 5. Generer le rapport avec l'IA
    print("\n5. Generation du rapport de maintenance...")

    chat = LlmChat(
        api_key=api_key,
        session_id=f"maintenance-{date_str}",
        system_message="""Tu es un assistant de maintenance pour un depot de documentation mathematique.
Ta tache est de:
1. Analyser la structure du depot
2. Identifier les problemes potentiels
3. Proposer des corrections SIMPLES (typos, formatage, liens casses)
4. NE PAS modifier le contenu mathematique
Sois concis et pratique."""
    ).with_model("openai", "gpt-4o")

    prompt = f"""Genere un rapport de maintenance mensuelle pour ce depot mathematique.

## STRUCTURE DU DEPOT:
- Fichiers .tex: {structure['tex_files']}
- Fichiers .thy: {structure['thy_files']}
- Fichiers .pdf: {structure['pdf_files']}

## STATISTIQUES BANQUE Q&R:
- Q&R validees: {qa_stats['validated']}
- Q&R en attente: {qa_stats['pending']}

## ACTIVITE:
- Commits ce mois: {len(commits)}
- Fichiers modifies recemment: {modified_files[:10]}

## TA TACHE:
1. Resume de l'etat du depot (2-3 lignes)
2. Points positifs (2-3 points)
3. Points d'attention (2-3 points)
4. Recommandations pour le mois prochain (2-3 actions)

Reponds en Markdown structure, format rapport professionnel."""

    try:
        print("  - Appel API en cours...")
        response = await chat.send_message(UserMessage(text=prompt))

        # Sauvegarder le rapport
        reports_dir = Path('maintenance_reports')
        reports_dir.mkdir(exist_ok=True)

        report_file = reports_dir / f"rapport_maintenance_{date_str}.md"

        report_content = f"""# Rapport de Maintenance Mensuelle

**Periode:** {date_str}
**Date de generation:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

---

## Statistiques du depot

| Categorie | Nombre |
|-----------|--------|
| Fichiers .tex | {len(structure['tex_files'])} |
| Fichiers .thy | {len(structure['thy_files'])} |
| Fichiers .pdf | {len(structure['pdf_files'])} |
| Q&R validees | {qa_stats['validated']} |
| Commits ce mois | {len(commits)} |

---

{response}

---

*Rapport genere automatiquement par le workflow de maintenance mensuelle*
"""

        report_file.write_text(report_content, encoding='utf-8')
        print(f"Rapport sauvegarde: {report_file}")

        return True

    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    success = asyncio.run(monthly_maintenance())
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
