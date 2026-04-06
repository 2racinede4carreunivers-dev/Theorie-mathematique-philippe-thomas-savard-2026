#!/usr/bin/env python3
"""
Script de generation automatique d'une Q&R quotidienne
Execute par le workflow GitHub Actions auto-daily-qa.yml
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path

# Ajouter scripts au path
sys.path.insert(0, str(Path(__file__).parent))

from qa_database import QADatabase
from qa_config import DATABASE_CONFIG

async def generate_single_qa():
    """Genere une seule Q&R et l'ajoute a la banque."""
    
    # Import Emergent
    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
    except ImportError:
        print("Installation de emergentintegrations...")
        os.system("pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/")
        from emergentintegrations.llm.chat import LlmChat, UserMessage
    
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    if not api_key:
        print("Cle API non trouvee")
        return False
    
    commit_sha = os.environ.get("GITHUB_SHA", "auto")[:8]
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')
    run_id = f"auto-{commit_sha}-{timestamp}"
    
    print(f"Generation automatique de 1 Q&R - {run_id}")
    
    # Lire le contenu des fichiers .tex et .thy
    content_parts = []
    root_path = Path(__file__).parent.parent  # Remonter de scripts/ vers racine
    
    for ext in ['.tex', '.thy']:
        for f in root_path.rglob(f'*{ext}'):
            if '.git' not in str(f):
                try:
                    text = f.read_text(encoding='utf-8', errors='ignore')[:3000]
                    content_parts.append(f"=== {f.name} ===\n{text}\n")
                except:
                    pass
    
    content = '\n'.join(content_parts)[:10000]
    
    if not content:
        print("Aucun contenu trouve")
        return False
    
    print(f"  - Contenu charge: {len(content)} caracteres")
    
    # Initialiser la banque
    db_path = root_path / DATABASE_CONFIG["db_path"]
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = QADatabase(str(db_path))
    
    # Obtenir le contexte des Q&R validees
    context = db.get_context_for_generation()
    validated_count = len(context.get('validated_examples', []))
    print(f"  - Q&R validees existantes: {validated_count}")
    
    context_prompt = ""
    if validated_count > 0:
        context_prompt = "\nExemples de Q&R validees (inspire-toi du style mais pose une question DIFFERENTE):\n"
        for ex in context['validated_examples'][:3]:
            context_prompt += f"Q: {str(ex.get('question', ''))[:80]}...\n"
    
    # Determiner le type de question base sur l'heure
    hour = datetime.utcnow().hour
    if hour < 10:
        question_type = "mathematique sur les DEFINITIONS ou AXIOMES"
        category = "mathematique"
        subcategory = "definition"
    elif hour < 16:
        question_type = "mathematique sur les THEOREMES ou DEMONSTRATIONS"
        category = "mathematique"
        subcategory = "theoreme"
    else:
        question_type = "philosophique ou ontologique sur la SIGNIFICATION de la theorie"
        category = "philosophique"
        subcategory = "ontologie"
    
    print(f"  - Type de question: {question_type}")
    
    # Generer 1 Q&R
    chat = LlmChat(
        api_key=api_key,
        session_id=run_id,
        system_message=f"""Tu es un expert en mathematiques specialise dans la theorie "L'Univers est au Carre" de Philippe Thomas Savard.
Genere UNE SEULE question {question_type} et sa reponse detaillee basee sur le contenu fourni.
La question doit etre ORIGINALE et DIFFERENTE des exemples fournis.
Reponds UNIQUEMENT en JSON valide avec ce format:
{{"question": "...", "answer": "...", "category": "{category}", "subcategory": "{subcategory}", "difficulty": "intermediaire"}}"""
    ).with_model("openai", "gpt-4o")
    
    prompt = f"""Analyse ce contenu mathematique et genere UNE question {question_type} originale avec sa reponse detaillee.
{context_prompt}

CONTENU DE LA THEORIE:
{content}

IMPORTANT: La question doit etre NOUVELLE et ne pas repeter les exemples ci-dessus.
Reponds en JSON uniquement."""

    try:
        print("  - Appel API en cours...")
        response = await chat.send_message(UserMessage(text=prompt))
        
        # Parser la reponse
        import re
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*', '', response)
        
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            qa = json.loads(json_match.group())
            
            # Ajouter a la banque ET auto-valider
            qa_id = db.add_pending_qa(
                question=qa.get("question", ""),
                answer=qa.get("answer", ""),
                category=qa.get("category", category),
                subcategory=qa.get("subcategory", subcategory),
                difficulty=qa.get("difficulty", "intermediaire"),
                language="fr",
                source_commit=commit_sha,
                run_id=run_id
            )
            
            if qa_id:
                # Auto-validation
                db.validate_qa(qa_id, quality_score=0.8)
                print(f"Q&R generee et validee (ID: {qa_id})")
                print(f"  Q: {qa.get('question', '')[:100]}...")
                return True
            else:
                print("Q&R similaire deja existante, ignoree")
                return True
        else:
            print(f"Pas de JSON trouve dans la reponse: {response[:200]}")
            return False
                
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Point d'entree principal."""
    success = asyncio.run(generate_single_qa())
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
