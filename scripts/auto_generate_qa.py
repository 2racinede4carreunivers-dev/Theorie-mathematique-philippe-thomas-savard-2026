#!/usr/bin/env python3
"""
Script de generation automatique d'une Q&R quotidienne (v3 - corpus.db)
Exploite corpus.db pour des Q&R riches en equations, demonstrations et contenu mathematique.

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
import sqlite3
import re
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from qa_database import QADatabase
from qa_config import DATABASE_CONFIG

FILES_ROTATION = [
    "postulat_de_univers_carre.tex",
    "teleosemantique_philosophie_esprit_analogiste.tex",
    "pilosophy_geometry_of_prime_number.tex",
    "mecanique_harmonique_du_chaos_discret.tex",
    "geometry_prime_spectrum.tex",
    "geometrie_du_spectre_premier.tex",
    "espace_de_philippot.tex",
    "postulat_carre.thy",
    "methode_spectral.thy",
    "methode_de_philippot.thy",
    "mecanique_discret.thy",
    "espace_philippot.thy",
]

QUESTION_ANGLES = [
    {"angle": "equation", "instruction": "Pose une question sur une EQUATION ou FORMULE MATHEMATIQUE precise present dans le contenu. La reponse doit expliquer chaque terme de l'equation et son role dans la demonstration.", "difficulty": "expert"},
    {"angle": "demonstration", "instruction": "Pose une question sur une DEMONSTRATION ou PREUVE. La reponse doit detailler les etapes logiques qui menent au resultat.", "difficulty": "avance"},
    {"angle": "theoreme", "instruction": "Pose une question sur un THEOREME, LEMME ou AXIOME formel. La reponse doit inclure l'enonce precis et ses implications dans la theorie.", "difficulty": "avance"},
    {"angle": "methode", "instruction": "Pose une question sur une METHODE (squaring, produit alternatif, analyse metrique, Philippot). La reponse doit decrire la methode, son but et son resultat.", "difficulty": "intermediaire"},
    {"angle": "relation", "instruction": "Pose une question sur les RELATIONS entre concepts mathematiques differents presentes dans le contenu.", "difficulty": "avance"},
    {"angle": "calcul", "instruction": "Pose une question de CALCUL ou VERIFICATION numerique basee sur les formules du contenu. La reponse doit montrer les etapes du calcul.", "difficulty": "expert"},
    {"angle": "structure_hol", "instruction": "Pose une question sur la FORMALISATION Isabelle/HOL: les locales, les definitions, les axiomes formels. La reponse doit expliquer comment la formalisation valide la proposition mathematique.", "difficulty": "expert"},
    {"angle": "geometrie", "instruction": "Pose une question sur les PROPRIETES GEOMETRIQUES (aires, perimetres, volumes, rapports) decrites dans le contenu.", "difficulty": "avance"},
    {"angle": "comparaison", "instruction": "Pose une question qui COMPARE deux approches, deux resultats ou deux methodes presentes dans le contenu.", "difficulty": "intermediaire"},
    {"angle": "philosophique", "instruction": "Pose une question sur les IMPLICATIONS PHILOSOPHIQUES (isossophie, teleosemantique, analogisme) en lien avec le contenu mathematique.", "difficulty": "avance"},
]


def get_file_for_hour():
    """Retourne le fichier du jour/heure selon la rotation."""
    day_of_year = datetime.utcnow().timetuple().tm_yday
    bloc_index = (day_of_year - 1) % 4
    start_index = bloc_index * 3
    todays_files = FILES_ROTATION[start_index:start_index + 3]

    hour = datetime.utcnow().hour
    if hour < 10:
        file_index = 0
    elif hour < 16:
        file_index = 1
    else:
        file_index = 2

    selected = todays_files[file_index]
    print(f"  Jour {day_of_year}, Bloc {bloc_index+1}/4, Heure {hour}h -> {selected}")
    return selected


def load_from_corpus(target_filename, root_path):
    """Charge le contenu enrichi depuis corpus.db."""
    corpus_path = root_path / 'qa_bank' / 'corpus.db'
    if not corpus_path.exists():
        print(f"  corpus.db non trouve a {corpus_path}")
        return None

    conn = sqlite3.connect(str(corpus_path))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Chercher le fichier par nom exact ou par base
    base_name = os.path.splitext(target_filename)[0]
    c.execute("SELECT * FROM files WHERE filename = ? OR filename LIKE ?",
              (target_filename, f"%{base_name}%"))
    rows = c.fetchall()

    if not rows:
        conn.close()
        print(f"  Fichier {target_filename} non trouve dans corpus.db")
        return None

    result = {
        'target_file': target_filename,
        'extracted_texts': [],
        'hol_structure': None,
        'tex_sections': None,
        'pdf_pages': 0,
        'related_files': [],
    }

    for row in rows:
        row_dict = dict(row)
        text = row_dict.get('extracted_text', '')
        if text:
            result['extracted_texts'].append({
                'filename': row_dict['filename'],
                'filetype': row_dict['filetype'],
                'text': text,
                'size': row_dict['filesize'],
            })
        result['related_files'].append(row_dict['filename'])

        file_id = row_dict['id']

        # Structure HOL si disponible
        c.execute("SELECT * FROM hol_structure WHERE file_id = ?", (file_id,))
        hol = c.fetchone()
        if hol:
            hol_dict = dict(hol)
            result['hol_structure'] = {
                'theory_name': hol_dict.get('theory_name', ''),
                'imports': json.loads(hol_dict.get('imports', '[]')),
                'theorems': json.loads(hol_dict.get('theorems', '[]')),
                'lemmas': json.loads(hol_dict.get('lemmas', '[]')),
                'definitions': json.loads(hol_dict.get('definitions', '[]')),
                'locales': json.loads(hol_dict.get('locales', '[]')),
                'functions': json.loads(hol_dict.get('functions', '[]')),
                'total_propositions': hol_dict.get('total_propositions', 0),
            }

        # Structure TEX si disponible
        c.execute("SELECT * FROM tex_structure WHERE file_id = ?", (file_id,))
        tex = c.fetchone()
        if tex:
            tex_dict = dict(tex)
            result['tex_sections'] = json.loads(tex_dict.get('sections', '[]'))

        # Structure PDF si disponible
        c.execute("SELECT * FROM pdf_structure WHERE file_id = ?", (file_id,))
        pdf = c.fetchone()
        if pdf:
            result['pdf_pages'] = dict(pdf).get('page_count', 0)

    # Charger aussi le PDF correspondant pour avoir les equations rendues
    c.execute("SELECT f.extracted_text, f.filename FROM files f WHERE f.filetype = 'pdf' AND f.filename LIKE ?",
              (f"%{base_name}%",))
    pdf_row = c.fetchone()
    if pdf_row and pdf_row['extracted_text']:
        already_has = any(t['filetype'] == 'pdf' for t in result['extracted_texts'])
        if not already_has:
            result['extracted_texts'].append({
                'filename': pdf_row['filename'],
                'filetype': 'pdf',
                'text': pdf_row['extracted_text'],
                'size': 0,
            })
            result['related_files'].append(pdf_row['filename'])

    conn.close()

    total_text = sum(len(t['text']) for t in result['extracted_texts'])
    print(f"  Corpus charge: {len(result['extracted_texts'])} sources, {total_text} car. total")
    if result['hol_structure']:
        hs = result['hol_structure']
        print(f"  Structure HOL: {hs['theory_name']}, {hs['total_propositions']} propositions, {len(hs['locales'])} locales")
    if result['tex_sections']:
        print(f"  Sections LaTeX: {len(result['tex_sections'])}")
    if result['pdf_pages']:
        print(f"  Pages PDF: {result['pdf_pages']}")

    return result


def build_rich_context(corpus_data, max_chars=12000):
    """Construit un contexte riche a partir des donnees du corpus."""
    parts = []

    # 1. Structure HOL (priorite haute pour les .thy)
    if corpus_data['hol_structure']:
        hs = corpus_data['hol_structure']
        parts.append(f"STRUCTURE FORMELLE ISABELLE/HOL (theorie: {hs['theory_name']}):")
        if hs['locales']:
            parts.append(f"  Locales: {', '.join(hs['locales'])}")
        if hs['definitions']:
            parts.append(f"  Definitions: {', '.join(hs['definitions'])}")
        if hs['functions']:
            parts.append(f"  Fonctions: {', '.join(hs['functions'])}")
        if hs['theorems']:
            parts.append(f"  Theoremes: {', '.join(hs['theorems'])}")
        if hs['lemmas']:
            parts.append(f"  Lemmes: {', '.join(hs['lemmas'])}")
        parts.append("")

    # 2. Sections LaTeX (plan du document)
    if corpus_data['tex_sections']:
        parts.append("PLAN DU DOCUMENT:")
        for s in corpus_data['tex_sections']:
            indent = {'chapter': '', 'section': '  ', 'subsection': '    '}.get(s.get('level', ''), '  ')
            parts.append(f"{indent}[{s.get('level', '?')}] {s.get('title', '?')}")
        parts.append("")

    # 3. Texte extrait — prendre une section aleatoire
    all_texts = []
    for source in corpus_data['extracted_texts']:
        all_texts.append((source['filetype'], source['filename'], source['text']))

    if all_texts:
        # Choisir aleatoirement entre les sources (TEX, THY, PDF)
        chosen_type, chosen_name, chosen_text = random.choice(all_texts)
        parts.append(f"EXTRAIT DU FICHIER ({chosen_type.upper()}: {chosen_name}):")

        # Prendre une section aleatoire du texte
        lines = chosen_text.split('\n')
        if len(lines) > 100:
            max_start = max(0, len(lines) - 100)
            start = random.randint(0, max_start)
            section = '\n'.join(lines[start:start + 100])
            parts.append(f"[lignes {start}-{start+100}/{len(lines)}]")
        else:
            section = chosen_text

        remaining = max_chars - sum(len(p) for p in parts)
        parts.append(section[:remaining])

    return '\n'.join(parts)


def get_all_existing_questions(db):
    """Recupere TOUTES les questions existantes pour eviter les doublons."""
    questions = []
    try:
        for qa in db.get_validated_qa(limit=500):
            questions.append(qa.get('question', ''))
        for qa in db.get_pending_qa():
            questions.append(qa.get('question', ''))
    except Exception:
        pass
    return questions


def export_catalogue(db, root_path):
    """Exporte toutes les Q&R validees en Markdown."""
    qa_list = db.get_validated_qa(limit=10000)
    if not qa_list:
        return

    catalogue_path = root_path / 'qa_bank' / 'CATALOGUE.md'
    lines = []
    lines.append("# Catalogue des Questions/Reponses")
    lines.append("## Theorie Mathematique - L'Univers est au Carre")
    lines.append("")
    lines.append(f"**Derniere mise a jour:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Total Q&R:** {len(qa_list)}")
    lines.append("")
    lines.append("---")
    lines.append("")

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
        by_source.setdefault(source, []).append(qa)

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
    print(f"  Catalogue exporte: {catalogue_path} ({len(qa_list)} Q&R)")


async def generate_single_qa():
    """Genere une Q&R en exploitant corpus.db."""

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

    print(f"Generation Q&R v3 (corpus.db) - {run_id}")
    print("=" * 50)

    target_filename = get_file_for_hour()
    root_path = Path(__file__).parent.parent

    # Charger depuis corpus.db
    corpus_data = load_from_corpus(target_filename, root_path)

    # Fallback: lecture directe si corpus.db absent
    if not corpus_data:
        print("  Fallback: lecture directe du fichier...")
        for f in root_path.rglob(f'*{target_filename}'):
            if '.git' not in str(f):
                content = f.read_text(encoding='utf-8', errors='ignore')
                corpus_data = {
                    'target_file': target_filename,
                    'extracted_texts': [{'filename': target_filename, 'filetype': 'tex', 'text': content, 'size': len(content)}],
                    'hol_structure': None,
                    'tex_sections': None,
                    'pdf_pages': 0,
                    'related_files': [target_filename],
                }
                break

    if not corpus_data or not corpus_data['extracted_texts']:
        print("Aucun contenu trouve")
        return False

    # Construire le contexte riche
    rich_context = build_rich_context(corpus_data)

    # Banque Q&R
    db_path = root_path / DATABASE_CONFIG["db_path"]
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = QADatabase(str(db_path))

    existing_questions = get_all_existing_questions(db)
    print(f"  Questions existantes: {len(existing_questions)}")

    existing_block = ""
    if existing_questions:
        existing_block = "\n\nQUESTIONS DEJA POSEES (tu DOIS poser une question COMPLETEMENT DIFFERENTE):\n"
        for q in existing_questions:
            existing_block += f"- {q[:120]}\n"

    angle = random.choice(QUESTION_ANGLES)
    print(f"  Angle: {angle['angle']} ({angle['difficulty']})")

    category = "philosophique" if angle['angle'] == 'philosophique' else "mathematique"

    # Enrichir les instructions avec le contexte HOL
    hol_bonus = ""
    if corpus_data['hol_structure']:
        hs = corpus_data['hol_structure']
        hol_bonus = f"""
INFORMATION SUPPLEMENTAIRE - STRUCTURE FORMELLE:
Ce fichier fait partie de la theorie Isabelle/HOL "{hs['theory_name']}".
Locales definies: {', '.join(hs['locales']) if hs['locales'] else 'aucune'}
Definitions: {', '.join(hs['definitions']) if hs['definitions'] else 'aucune'}
Fonctions: {', '.join(hs['functions']) if hs['functions'] else 'aucune'}
Tu peux poser des questions sur ces elements formels specifiques."""

    chat = LlmChat(
        api_key=api_key,
        session_id=run_id,
        system_message=f"""Tu es un expert en mathematiques specialise dans la theorie "L'Univers est au Carre" de Philippe Thomas Savard.

Tu as acces au TEXTE EXTRAIT DIRECTEMENT des fichiers PDF, TEX et THY de la theorie, incluant:
- Les equations mathematiques exactes
- Les demonstrations formelles
- Les structures de preuves Isabelle/HOL
- Les sections et sous-sections de chaque chapitre

CONSIGNE: {angle['instruction']}
Difficulte: {angle['difficulty']}
{hol_bonus}

REGLES:
1. La question doit etre UNIQUE et porter sur un element MATHEMATIQUE PRECIS du contenu
2. Si le contenu contient des equations, CITE-LES dans ta question ou ta reponse
3. La reponse doit etre DETAILLEE (minimum 4 phrases), montrer les ETAPES mathematiques
4. Reference les fichiers source exacts et les sections/theoremes concernes
5. Pour les .thy: reference les noms de locales, definitions et axiomes Isabelle exacts
6. Les Q&R doivent etre utiles a quelqu'un qui etudie serieusement la theorie

Reponds UNIQUEMENT en JSON valide:
{{"question": "...", "answer": "...", "category": "{category}", "subcategory": "{angle['angle']}", "difficulty": "{angle['difficulty']}", "source_file": "{target_filename}"}}"""
    ).with_model("openai", "gpt-4o")

    prompt = f"""Genere UNE question mathematique originale et sa reponse detaillee a partir du contenu enrichi suivant.

ANGLE: {angle['angle'].upper()} - {angle['instruction']}

FICHIERS SOURCE: {', '.join(corpus_data['related_files'])}
{existing_block}

{rich_context}

IMPORTANT:
- Ta question doit porter sur un element MATHEMATIQUE PRECIS de cet extrait
- Inclus des equations, des valeurs, des references aux demonstrations
- Reponds UNIQUEMENT en JSON valide"""

    try:
        print("  Appel API...")
        response = None
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                response = await chat.send_message(UserMessage(text=prompt))
                break
            except Exception as api_err:
                err_str = str(api_err)
                if ("502" in err_str or "503" in err_str or "429" in err_str
                        or "BadGateway" in err_str or "timeout" in err_str.lower()):
                    wait = 15 * attempt
                    print(f"  Erreur API temporaire (tentative {attempt}/{max_retries}): {err_str[:80]}")
                    print(f"  Nouvel essai dans {wait}s...")
                    import time
                    time.sleep(wait)
                else:
                    raise
        if response is None:
            print(f"  Echec apres {max_retries} tentatives.")
            return False

        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*', '', response)

        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            qa = json.loads(json_match.group())

            qa_id = db.add_pending_qa(
                question=qa.get("question", ""),
                answer=qa.get("answer", ""),
                category=qa.get("category", category),
                subcategory=qa.get("subcategory", angle['angle']),
                difficulty=qa.get("difficulty", angle['difficulty']),
                language="fr",
                source_commit=commit_sha,
                run_id=run_id,
                source_files=corpus_data['related_files']
            )

            if qa_id:
                db.validate_qa(qa_id, quality_score=0.85)
                print("=" * 50)
                print(f"Q&R generee (ID: {qa_id})")
                print(f"  Sources: {corpus_data['related_files']}")
                print(f"  Angle: {angle['angle']} | Diff: {angle['difficulty']}")
                print(f"  Q: {qa.get('question', '')[:150]}...")
            else:
                print("Q&R similaire existante, ignoree")

            export_catalogue(db, root_path)
            return True
        else:
            print(f"Pas de JSON: {response[:200]}")
            return False

    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("GENERATION Q&R v3 - CORPUS.DB (equations + demonstrations)")
    print("=" * 60)
    random.seed(datetime.utcnow().strftime('%Y%m%d%H%M'))
    success = asyncio.run(generate_single_qa())
    print("=" * 60)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
