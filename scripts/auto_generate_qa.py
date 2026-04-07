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
import random
import hashlib
from datetime import datetime
from pathlib import Path

# Ajouter scripts au path
sys.path.insert(0, str(Path(__file__).parent))

from qa_database import QADatabase
from qa_config import DATABASE_CONFIG

# Liste des 12 fichiers dans l'ordre de rotation
FILES_ROTATION = [
    # Bloc 1
    "postulat_de_univers_carre.tex",
    "teleosemantique_philosophie_esprit_analogiste.tex",
    "pilosophy_geometry_of_prime_number.tex",
    # Bloc 2
    "mecanique_harmonique_du_chaos_discret.tex",
    "geometry_prime_spectrum.tex",
    "geometrie_du_spectre_premier.tex",
    # Bloc 3
    "espace_de_philippot.tex",
    "postulat_carre.thy",
    "methode_spectral.thy",
    # Bloc 4
    "methode_de_philippot.thy",
    "mecanique_discret.thy",
    "espace_philippot.thy",
]

# Angles varies pour les questions
QUESTION_ANGLES = [
    {
        "angle": "definition",
        "instruction": "Pose une question sur une DEFINITION ou un CONCEPT specifique present dans le fichier. La reponse doit expliquer le concept en detail.",
        "difficulty": "intermediaire"
    },
    {
        "angle": "demonstration",
        "instruction": "Pose une question sur une DEMONSTRATION ou une PREUVE presente dans le fichier. La reponse doit detailler les etapes logiques.",
        "difficulty": "avance"
    },
    {
        "angle": "theoreme",
        "instruction": "Pose une question sur un THEOREME ou un RESULTAT PRINCIPAL du fichier. La reponse doit inclure l'enonce et ses implications.",
        "difficulty": "avance"
    },
    {
        "angle": "application",
        "instruction": "Pose une question sur les APPLICATIONS ou CONSEQUENCES pratiques d'un concept du fichier.",
        "difficulty": "intermediaire"
    },
    {
        "angle": "relation",
        "instruction": "Pose une question sur les RELATIONS ou CONNEXIONS entre differents concepts presentes dans le fichier.",
        "difficulty": "avance"
    },
    {
        "angle": "formule",
        "instruction": "Pose une question centree sur une FORMULE ou une EQUATION specifique du fichier. La reponse doit expliquer chaque terme.",
        "difficulty": "expert"
    },
    {
        "angle": "comparaison",
        "instruction": "Pose une question qui COMPARE ou DISTINGUE deux concepts, methodes ou approches presentes dans le fichier.",
        "difficulty": "intermediaire"
    },
    {
        "angle": "fondement",
        "instruction": "Pose une question sur les FONDEMENTS AXIOMATIQUES ou les HYPOTHESES de base utilisees dans le fichier.",
        "difficulty": "debutant"
    },
    {
        "angle": "philosophique",
        "instruction": "Pose une question sur les IMPLICATIONS PHILOSOPHIQUES ou ONTOLOGIQUES des idees presentees dans le fichier.",
        "difficulty": "expert"
    },
    {
        "angle": "structure",
        "instruction": "Pose une question sur la STRUCTURE MATHEMATIQUE ou la LOGIQUE d'organisation des preuves dans le fichier.",
        "difficulty": "avance"
    },
]


def get_todays_files():
    """Retourne les 3 fichiers du jour selon la rotation."""
    day_of_year = datetime.utcnow().timetuple().tm_yday
    bloc_index = (day_of_year - 1) % 4
    start_index = bloc_index * 3
    todays_files = FILES_ROTATION[start_index:start_index + 3]
    print(f"  - Jour de l'annee: {day_of_year}")
    print(f"  - Bloc du jour: {bloc_index + 1}/4")
    print(f"  - Fichiers du jour: {todays_files}")
    return todays_files


def get_file_for_hour():
    """Retourne le fichier specifique selon l'heure (6h, 12h, 18h)."""
    todays_files = get_todays_files()
    hour = datetime.utcnow().hour
    if hour < 10:
        file_index = 0
    elif hour < 16:
        file_index = 1
    else:
        file_index = 2
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


def select_random_section(content, target_filename):
    """Selectionne une section aleatoire du fichier pour varier le contenu analyse."""
    lines = content.split('\n')
    total_lines = len(lines)

    if total_lines <= 200:
        return content

    # Trouver les points de decoupe naturels (sections, theoremes, etc.)
    import re
    if target_filename.endswith('.tex'):
        section_markers = [i for i, line in enumerate(lines)
                          if re.match(r'\\(section|subsection|chapter|theorem|definition|lemma|begin\{)', line)]
    else:
        section_markers = [i for i, line in enumerate(lines)
                          if re.match(r'(theorem|lemma|definition|fun |datatype |proof)', line.strip())]

    if section_markers and len(section_markers) > 1:
        # Choisir un point de depart aleatoire parmi les sections
        start_marker = random.choice(section_markers)
        # Prendre ~200 lignes depuis cette section
        start = max(0, start_marker - 5)
        end = min(total_lines, start + 250)
        selected = '\n'.join(lines[start:end])
        print(f"  - Section aleatoire selectionnee: lignes {start}-{end}/{total_lines}")
        return selected
    else:
        # Pas de marqueurs: choisir un bloc aleatoire
        max_start = max(0, total_lines - 250)
        start = random.randint(0, max_start)
        end = min(total_lines, start + 250)
        selected = '\n'.join(lines[start:end])
        print(f"  - Bloc aleatoire selectionne: lignes {start}-{end}/{total_lines}")
        return selected


def get_all_existing_questions(db):
    """Recupere TOUTES les questions existantes pour eviter les doublons."""
    questions = []
    try:
        validated = db.get_validated_qa(limit=500)
        for qa in validated:
            questions.append(qa.get('question', ''))
        pending = db.get_pending_qa()
        for qa in pending:
            questions.append(qa.get('question', ''))
    except Exception:
        pass
    return questions


def export_catalogue(db, root_path):
    """Exporte toutes les Q&R validees dans un fichier Markdown lisible."""
    qa_list = db.get_validated_qa(limit=10000)
    if not qa_list:
        return

    catalogue_path = root_path / 'qa_bank' / 'CATALOGUE.md'

    lines = []
    lines.append("# Catalogue des Questions/Reponses")
    lines.append(f"## Theorie Mathematique - L'Univers est au Carre")
    lines.append(f"")
    lines.append(f"**Derniere mise a jour:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Total Q&R:** {len(qa_list)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Grouper par source_files/categorie
    by_source = {}
    for qa in qa_list:
        source = "Divers"
        if qa.get('source_files'):
            try:
                sf = json.loads(qa['source_files'])
                if sf:
                    source = sf[0] if isinstance(sf, list) else str(sf)
            except Exception:
                pass
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(qa)

    for source, qas in sorted(by_source.items()):
        lines.append(f"### Source: `{source}`")
        lines.append("")
        for i, qa in enumerate(qas, 1):
            diff = qa.get('difficulty', '?')
            cat = qa.get('category', '?')
            subcat = qa.get('subcategory', '')
            lines.append(f"**{i}. [{diff}] {qa.get('question', 'N/A')}**")
            lines.append("")
            lines.append(f"*Categorie: {cat}/{subcat} | Score: {qa.get('quality_score', 0):.1f}*")
            lines.append("")
            lines.append(f"> {qa.get('answer', 'N/A')}")
            lines.append("")
            lines.append("---")
            lines.append("")

    catalogue_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  - Catalogue exporte: {catalogue_path} ({len(qa_list)} Q&R)")


async def generate_single_qa():
    """Genere une seule Q&R a partir du fichier du jour/heure."""

    try:
        from emergentintegrations.llm.chat import LlmChat, UserMessage
    except ImportError:
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
        print("Fallback: lecture de tous les fichiers...")
        content_parts = []
        for ext in ['.tex', '.thy']:
            for f in root_path.rglob(f'*{ext}'):
                if '.git' not in str(f):
                    try:
                        text = f.read_text(encoding='utf-8', errors='ignore')[:2000]
                        content_parts.append(f"=== {f.name} ===\n{text}\n")
                    except Exception:
                        pass
        content = '\n'.join(content_parts)[:10000]
        file_path = "multiple_files"

    if not content:
        print("Aucun contenu trouve")
        return False

    # Selectionner une section ALEATOIRE du fichier (pas toujours le debut)
    section_content = select_random_section(content, target_filename)

    # Initialiser la banque
    db_path = root_path / DATABASE_CONFIG["db_path"]
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = QADatabase(str(db_path))

    # Recuperer TOUTES les questions existantes
    existing_questions = get_all_existing_questions(db)
    print(f"  - Questions existantes dans la banque: {len(existing_questions)}")

    existing_block = ""
    if existing_questions:
        existing_block = "\n\nQUESTIONS DEJA POSEES (tu DOIS poser une question COMPLETEMENT DIFFERENTE):\n"
        for q in existing_questions:
            existing_block += f"- {q[:120]}\n"

    # Choisir un angle ALEATOIRE pour varier les questions
    angle = random.choice(QUESTION_ANGLES)
    print(f"  - Angle choisi: {angle['angle']} (difficulte: {angle['difficulty']})")

    # Determiner la categorie selon le type de fichier et l'angle
    if target_filename.endswith('.thy'):
        file_type_desc = "preuves formelles Isabelle/HOL"
        category = "mathematique"
    else:
        file_type_desc = "documentation mathematique LaTeX"
        category = "mathematique"

    if angle['angle'] == 'philosophique':
        category = "philosophique"

    # Generer la Q&R avec angle varie
    chat = LlmChat(
        api_key=api_key,
        session_id=run_id,
        system_message=f"""Tu es un expert en mathematiques specialise dans la theorie "L'Univers est au Carre" de Philippe Thomas Savard.

Cette theorie comprend 4 chapitres de documentation LaTeX et 5 fichiers de validation formelle Isabelle/HOL.
Les sujets couverts incluent: geometrie du spectre premier, mecanique harmonique du chaos discret, espace de Philippot, postulat de l'univers au carre, teleosemantique, methode spectrale, et plus.

CONSIGNE SPECIFIQUE POUR CETTE GENERATION:
{angle['instruction']}
Niveau de difficulte cible: {angle['difficulty']}

REGLES:
1. La question doit etre UNIQUE et JAMAIS vue auparavant
2. La question doit porter sur un aspect SPECIFIQUE et PRECIS du contenu fourni
3. La reponse doit etre DETAILLEE (minimum 3 phrases), PEDAGOGIQUE et citer les elements du fichier
4. Mentionne le fichier source et la section/concept exact dans la reponse
5. Si c'est un fichier .thy, reference les noms de theoremes/lemmes Isabelle exacts

Reponds UNIQUEMENT en JSON valide:
{{"question": "...", "answer": "...", "category": "{category}", "subcategory": "{angle['angle']}", "difficulty": "{angle['difficulty']}", "source_file": "{target_filename}"}}"""
    ).with_model("openai", "gpt-4o")

    prompt = f"""Analyse cet EXTRAIT du fichier "{target_filename}" ({file_type_desc}) et genere UNE question originale avec sa reponse detaillee.

ANGLE DE LA QUESTION: {angle['angle'].upper()} - {angle['instruction']}
{existing_block}

EXTRAIT DU FICHIER "{target_filename}":
{section_content}

IMPORTANT:
- Ta question doit porter sur un element PRECIS de cet extrait
- Elle doit etre COMPLETEMENT DIFFERENTE de toutes les questions listees ci-dessus
- Reponds UNIQUEMENT en JSON valide"""

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
                subcategory=qa.get("subcategory", angle['angle']),
                difficulty=qa.get("difficulty", angle['difficulty']),
                language="fr",
                source_commit=commit_sha,
                run_id=run_id,
                source_files=[target_filename]
            )

            if qa_id:
                db.validate_qa(qa_id, quality_score=0.8)
                print("=" * 50)
                print(f"Q&R generee et validee (ID: {qa_id})")
                print(f"  Source: {target_filename}")
                print(f"  Angle: {angle['angle']}")
                print(f"  Difficulte: {angle['difficulty']}")
                print(f"  Q: {qa.get('question', '')[:150]}...")
            else:
                print("Q&R similaire deja existante, ignoree")

            # Exporter le catalogue Markdown
            export_catalogue(db, root_path)
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
    print("GENERATION Q&R - ROTATION DES FICHIERS (v2 - variee)")
    print("=" * 60)
    # Seed aleatoire base sur le timestamp pour varier les resultats
    random.seed(datetime.utcnow().strftime('%Y%m%d%H%M'))
    success = asyncio.run(generate_single_qa())
    print("=" * 60)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
