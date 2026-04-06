#!/usr/bin/env python3
"""
Script de generation automatique d'une Q&R quotidienne
Execute par le workflow GitHub Actions auto-daily-qa.yml

Rotation des fichiers en blocs de 3:
- Bloc 1 (Jour 1, 5, 9...): postulat_de_univers_carre.tex, teleosemantique_philosophie_esprit_analogiste.tex, pilosophy_geometry_of_prime_number.tex
- Bloc 2 (Jour 2, 6, 10...): mecanique_harmonique_du_chaos_discret.tex, geometry_prime_spectrum.tex, geometrie_du_spectre_premier.tex
- Bloc 3 (Jour 3, 7, 11...): espace_de_philippot.tex, postulat_carre.thy, methode_spectral.thy
- Bloc 4 (Jour 4, 8, 12...): methode_de_philippot.thy, mecanique_discret.thy, espace_philippot.thy
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

# Liste des 12 fichiers dans l'ordre de rotation
FILES_ROTATION = [
    # Bloc 1 (indices 0, 1, 2)
    "postulat_de_univers_carre.tex",
    "teleosemantique_philosophie_esprit_analogiste.tex",
    "pilosophy_geometry_of_prime_number.tex",
    # Bloc 2 (indices 3, 4, 5)
    "mecanique_harmonique_du_chaos_discret.tex",
    "geometry_prime_spectrum.tex",
    "geometrie_du_spectre_premier.tex",
    # Bloc 3 (indices 6, 7, 8)
    "espace_de_philippot.tex",
    "postulat_carre.thy",
    "methode_spectral.thy",
    # Bloc 4 (indices 9, 10, 11)
    "methode_de_philippot.thy",
    "mecanique_discret.thy",
    "espace_philippot.thy",
]

def get_todays_files():
    """
    Retourne les 3 fichiers du jour selon la rotation.
    Bloc change chaque jour en cycle de 4 jours.
    """
    day_of_year = datetime.utcnow().timetuple().tm_yday
    bloc_index = (day_of_year - 1) % 4  # 0, 1, 2, ou 3
    
    start_index = bloc_index * 3
    todays_files = FILES_ROTATION[start_index:start_index + 3]
    
    print(f"  - Jour de l'annee: {day_of_year}")
    print(f"  - Bloc du jour: {bloc_index + 1}/4")
    print(f"  - Fichiers du jour: {todays_files}")
    
    return todays_files

def get_file_for_hour():
    """
    Retourne le fichier specifique selon l'heure (6h, 12h, 18h).
    - 6h UTC: 1er fichier du bloc
    - 12h UTC: 2eme fichier du bloc
    - 18h UTC: 3eme fichier du bloc
    """
    todays_files = get_todays_files()
    hour = datetime.utcnow().hour
    
    if hour < 10:
        file_index = 0  # 6h -> 1er fichier
    elif hour < 16:
        file_index = 1  # 12h -> 2eme fichier
    else:
        file_index = 2  # 18h -> 3eme fichier
    
    selected_file = todays_files[file_index]
    print(f"  - Heure UTC: {hour}h -> Fichier selectionne: {selected_file}")
    
    return selected_file

def find_file_content(filename, root_path):
    """Trouve et lit le contenu d'un fichier specifique."""
    for f in root_path.rglob(f'*{filename}'):
        if '.git' not in str(f):
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                print(f"  - Fichier trouve: {f} ({len(content)} caracteres)")
                return content, str(f)
            except Exception as e:
                print(f"  - Erreur lecture {f}: {e}")
    return None, None

async def generate_single_qa():
    """Genere une seule Q&R a partir du fichier du jour/heure."""
    
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
    print("=" * 50)
    
    # Determiner le fichier a utiliser
    target_filename = get_file_for_hour()
    
    # Trouver et lire le fichier
    root_path = Path(__file__).parent.parent
    content, file_path = find_file_content(target_filename, root_path)
    
    if not content:
        print(f"ERREUR: Fichier {target_filename} non trouve!")
        # Fallback: lire tous les fichiers
        print("Fallback: lecture de tous les fichiers...")
        content_parts = []
        for ext in ['.tex', '.thy']:
            for f in root_path.rglob(f'*{ext}'):
                if '.git' not in str(f):
                    try:
                        text = f.read_text(encoding='utf-8', errors='ignore')[:2000]
                        content_parts.append(f"=== {f.name} ===\n{text}\n")
                    except:
                        pass
        content = '\n'.join(content_parts)[:10000]
        file_path = "multiple_files"
    
    if not content:
        print("Aucun contenu trouve")
        return False
    
    # Limiter le contenu
    content = content[:12000]
    
    # Initialiser la banque
    db_path = root_path / DATABASE_CONFIG["db_path"]
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = QADatabase(str(db_path))
    
    # Obtenir le contexte des Q&R validees
    context = db.get_context_for_generation()
    validated_count = len(context.get('validated_examples', []))
    print(f"  - Q&R validees existantes: {validated_count}")
    
    # Construire le contexte des questions existantes pour eviter les doublons
    existing_questions = ""
    if validated_count > 0:
        existing_questions = "\n\nQUESTIONS DEJA POSEES (NE PAS REPETER):\n"
        for ex in context['validated_examples'][:10]:
            q = str(ex.get('question', ''))[:100]
            existing_questions += f"- {q}...\n"
    
    # Determiner le type de question selon l'extension du fichier
    if target_filename.endswith('.thy'):
        question_type = "sur les PREUVES FORMELLES et la LOGIQUE ISABELLE/HOL"
        category = "mathematique"
        subcategory = "demonstration"
    else:
        question_type = "sur les CONCEPTS MATHEMATIQUES et THEOREMES"
        category = "mathematique"
        subcategory = "theoreme"
    
    # Generer la Q&R
    chat = LlmChat(
        api_key=api_key,
        session_id=run_id,
        system_message=f"""Tu es un expert en mathematiques specialise dans la theorie "L'Univers est au Carre" de Philippe Thomas Savard.

Tu dois generer UNE SEULE question {question_type} basee UNIQUEMENT sur le fichier "{target_filename}" fourni.

REGLES IMPORTANTES:
1. La question doit etre SPECIFIQUE au contenu du fichier fourni
2. La question doit etre ORIGINALE et DIFFERENTE des questions deja posees
3. La reponse doit etre detaillee et pedagogique
4. Mentionne le fichier source dans ta reponse

Reponds UNIQUEMENT en JSON valide:
{{"question": "...", "answer": "...", "category": "{category}", "subcategory": "{subcategory}", "difficulty": "intermediaire", "source_file": "{target_filename}"}}"""
    ).with_model("openai", "gpt-4o")
    
    prompt = f"""Analyse ce fichier et genere UNE question originale avec sa reponse detaillee.

FICHIER SOURCE: {target_filename}
{existing_questions}

CONTENU DU FICHIER:
{content}

IMPORTANT: 
- Base ta question UNIQUEMENT sur ce fichier specifique
- Ne repete pas les questions deja posees ci-dessus
- Reponds en JSON uniquement"""

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
                run_id=run_id,
                source_files=[target_filename]
            )
            
            if qa_id:
                # Auto-validation
                db.validate_qa(qa_id, quality_score=0.8)
                print("=" * 50)
                print(f"Q&R generee et validee (ID: {qa_id})")
                print(f"  Source: {target_filename}")
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
    print("=" * 60)
    print("GENERATION Q&R - ROTATION DES FICHIERS")
    print("=" * 60)
    success = asyncio.run(generate_single_qa())
    print("=" * 60)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
