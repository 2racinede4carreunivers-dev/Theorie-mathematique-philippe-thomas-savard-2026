#!/usr/bin/env python3
"""
Générateur du corpus SQLite complet
Extraction textuelle PDF, TEX, THY + arborescences HOL, LaTeX, PDF, globale
Version complète et fonctionnelle
"""

import os
import sys
import re
import sqlite3
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone


# ------------------------------------------------------------
# UTILITAIRES
# ------------------------------------------------------------

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def iso_now():
    return datetime.now(timezone.utc).isoformat()


# ------------------------------------------------------------
# EXTRACTION TEX
# ------------------------------------------------------------

def extract_text_tex(filepath):
    """Extrait le texte brut d'un fichier .tex en retirant les commandes LaTeX."""
    try:
        content = Path(filepath).read_text(encoding='utf-8', errors='ignore')

        # Retirer les commentaires
        content = re.sub(r'%.*$', '', content, flags=re.MULTILINE)

        # Retirer les environnements begin/end
        content = re.sub(r'\\(begin|end)\{[^}]*\}', '', content)

        # Retirer les commandes LaTeX du type \commande{...}
        content = re.sub(r'\\[a-zA-Z]+\*?\{([^}]*)\}', r'\1', content)

        # Retirer les commandes du type \commande[options]
        content = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?', '', content)

        # Nettoyage final pour enlever les accolades, les signes $, etc.
        content = re.sub(r'[{}$^]', '', content)

        return content.strip()

    except Exception as e:
        return f"[Erreur extraction TEX: {e}]"


def extract_tex_sections(filepath):
    """
    Extraction très simple des sections LaTeX.
    On repère les commandes \section, \subsection, \subsubsection.
    """
    sections = []
    try:
        content = Path(filepath).read_text(encoding='utf-8', errors='ignore')
        pattern = r'\\(section|subsection|subsubsection)\*?\{([^}]*)\}'
        for kind, title in re.findall(pattern, content):
            sections.append({
                'level': kind,
                'title': title.strip()
            })
    except Exception:
        pass
    return sections


# ------------------------------------------------------------
# EXTRACTION HOL
# ------------------------------------------------------------

def extract_text_thy(filepath):
    """Extrait le texte brut d'un fichier .thy Isabelle/HOL."""
    try:
        return Path(filepath).read_text(encoding='utf-8', errors='ignore').strip()
    except Exception as e:
        return f"[Erreur extraction THY: {e}]"


def extract_thy_structure(filepath):
    """Extrait la structure logique d'un fichier .thy."""
    structure = {
        'theory_name': '',
        'imports': [],
        'theorems': [],
        'lemmas': [],
        'definitions': [],
        'datatypes': [],
        'functions': [],
        'locales': [],
    }
    try:
        content = Path(filepath).read_text(encoding='utf-8', errors='ignore')

        # Nom de la théorie
        m = re.search(r'theory\s+(\w+)', content)
        if m:
            structure['theory_name'] = m.group(1)

        # Imports
        imports_match = re.search(r'imports\s+(.*?)begin', content, re.DOTALL)
        if imports_match:
            imports_text = imports_match.group(1)
            structure['imports'] = [
                x for pair in re.findall(r'(?:"([^"]+)"|(\S+))', imports_text)
                for x in pair if x and x not in ('', 'begin')
            ]

        # Théorèmes
        structure['theorems'] = re.findall(r'theorem\s+(\w+)', content)

        # Lemmes
        structure['lemmas'] = re.findall(r'lemma\s+(\w+)', content)

        # Définitions
        structure['definitions'] = re.findall(r'definition\s+(\w+)', content)

        # Datatypes
        structure['datatypes'] = re.findall(r'datatype\s+(\w+)', content)

        # Fonctions
        structure['functions'] = re.findall(r'fun\s+(\w+)', content)

        # Locales
        structure['locales'] = re.findall(r'locale\s+(\w+)', content)

    except Exception:
        pass

    return structure


# ------------------------------------------------------------
# EXTRACTION PDF
# ------------------------------------------------------------

def extract_text_pdf(filepath):
    """Extrait le texte d'un fichier PDF via pypdf."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return '\n\n'.join(text_parts).strip()
    except Exception as e:
        return f"[Erreur extraction PDF: {e}]"


# ------------------------------------------------------------
# ARBORESCENCES
# ------------------------------------------------------------

def build_arborescence_hol(thy_files):
    arbo = {'type': 'hol', 'theories': []}
    for f in thy_files:
        struct = extract_thy_structure(f)
        arbo['theories'].append({
            'file': os.path.basename(f),
            'path': str(f),
            'theory_name': struct['theory_name'],
            'imports': struct['imports'],
            'theorems': struct['theorems'],
            'lemmas': struct['lemmas'],
            'definitions': struct['definitions'],
            'datatypes': struct['datatypes'],
            'functions': struct['functions'],
            'locales': struct['locales'],
            'total_propositions': len(struct['theorems']) + len(struct['lemmas']),
        })
    return arbo


def build_arborescence_tex(tex_files):
    arbo = {'type': 'latex', 'documents': []}
    for f in tex_files:
        sections = extract_tex_sections(f)
        arbo['documents'].append({
            'file': os.path.basename(f),
            'path': str(f),
            'sections': sections,
            'total_sections': len(sections),
        })
    return arbo


def build_arborescence_pdf(pdf_files):
    arbo = {'type': 'pdf', 'documents': []}
    for f in pdf_files:
        page_count = 0
        try:
            from pypdf import PdfReader
            page_count = len(PdfReader(f).pages)
        except Exception:
            pass
        arbo['documents'].append({
            'file': os.path.basename(f),
            'path': str(f),
            'pages': page_count,
        })
    return arbo


def build_arborescence_globale(arbo_hol, arbo_tex, arbo_pdf):
    tex_bases = {os.path.splitext(d['file'])[0]: d for d in arbo_tex['documents']}
    pdf_bases = {os.path.splitext(d['file'])[0]: d for d in arbo_pdf['documents']}
    thy_bases = {os.path.splitext(d['file'])[0]: d for d in arbo_hol['theories']}

    all_bases = set(list(tex_bases.keys()) + list(pdf_bases.keys()) + list(thy_bases.keys()))
    links = []

    for base in all_bases:
        link = {'concept': base, 'files': {}}
        if base in tex_bases:
            link['files']['tex'] = tex_bases[base]['file']
        if base in pdf_bases:
            link['files']['pdf'] = pdf_bases[base]['file']
        if base in thy_bases:
            link['files']['thy'] = thy_bases[base]['file']
        links.append(link)

    return {
        'type': 'global',
        'total_tex': len(arbo_tex['documents']),
        'total_thy': len(arbo_hol['theories']),
        'total_pdf': len(arbo_pdf['documents']),
        'total_theorems': sum(t['total_propositions'] for t in arbo_hol['theories']),
        'links': links,
        'hol': arbo_hol,
        'latex': arbo_tex,
        'pdf': arbo_pdf,
    }


# ------------------------------------------------------------
# CREATION DE LA BASE
# ------------------------------------------------------------

def create_schema(conn):
    c = conn.cursor()
    schema_sql = """
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        filetype TEXT NOT NULL,
        sha256 TEXT NOT NULL,
        filesize INTEGER NOT NULL,
        extracted_text TEXT,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS arborescences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arbo_type TEXT NOT NULL,
        arbo_data TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS hol_structure (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER NOT NULL,
        theory_name TEXT,
        imports TEXT,
        theorems TEXT,
        lemmas TEXT,
        definitions TEXT,
        datatypes TEXT,
        functions TEXT,
        locales TEXT,
        total_propositions INTEGER DEFAULT 0,
        FOREIGN KEY (file_id) REFERENCES files(id)
    );

    CREATE TABLE IF NOT EXISTS tex_structure (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER NOT NULL,
        sections TEXT,
        total_sections INTEGER DEFAULT 0,
        FOREIGN KEY (file_id) REFERENCES files(id)
    );

    CREATE TABLE IF NOT EXISTS pdf_structure (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id INTEGER NOT NULL,
        page_count INTEGER DEFAULT 0,
        FOREIGN KEY (file_id) REFERENCES files(id)
    );

    CREATE TABLE IF NOT EXISTS concepts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        concept_name TEXT NOT NULL,
        source_files TEXT,
        concept_type TEXT,
        description TEXT
    );

    CREATE TABLE IF NOT EXISTS metadata (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """
    c.executescript(schema_sql)
    conn.commit()


def insert_file(conn, filename, filepath, filetype, sha256, filesize, extracted_text):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO files (filename, filepath, filetype, sha256, filesize, extracted_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (filename, filepath, filetype, sha256, filesize, extracted_text, iso_now())
    )
    conn.commit()
    return c.lastrowid


def insert_hol_structure(conn, file_id, struct):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO hol_structure (
            file_id, theory_name, imports, theorems, lemmas,
            definitions, datatypes, functions, locales, total_propositions
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            file_id,
            struct.get('theory_name', ''),
            json.dumps(struct.get('imports', []), ensure_ascii=False),
            json.dumps(struct.get('theorems', []), ensure_ascii=False),
            json.dumps(struct.get('lemmas', []), ensure_ascii=False),
            json.dumps(struct.get('definitions', []), ensure_ascii=False),
            json.dumps(struct.get('datatypes', []), ensure_ascii=False),
            json.dumps(struct.get('functions', []), ensure_ascii=False),
            json.dumps(struct.get('locales', []), ensure_ascii=False),
            len(struct.get('theorems', [])) + len(struct.get('lemmas', [])),
        )
    )
    conn.commit()


def insert_tex_structure(conn, file_id, sections):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO tex_structure (file_id, sections, total_sections)
        VALUES (?, ?, ?)
        """,
        (file_id, json.dumps(sections, ensure_ascii=False), len(sections))
    )
    conn.commit()


def insert_pdf_structure(conn, file_id, page_count):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO pdf_structure (file_id, page_count)
        VALUES (?, ?)
        """,
        (file_id, page_count)
    )
    conn.commit()


def insert_arborescence(conn, arbo_type, arbo_data):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO arborescences (arbo_type, arbo_data, created_at)
        VALUES (?, ?, ?)
        """,
        (arbo_type, json.dumps(arbo_data, ensure_ascii=False), iso_now())
    )
    conn.commit()


def insert_metadata(conn, key, value):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO metadata (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """,
        (key, value)
    )
    conn.commit()


# ------------------------------------------------------------
# PIPELINE PRINCIPAL
# ------------------------------------------------------------

def create_corpus_db(db_path, root_dir):
    print(f"Création de {db_path}…")

    conn = sqlite3.connect(db_path)
    create_schema(conn)

    root = Path(root_dir)

    tex_files = list(root.rglob("*.tex"))
    thy_files = list(root.rglob("*.thy"))
    pdf_files = list(root.rglob("*.pdf"))

    print(f"Trouvé {len(tex_files)} .tex, {len(thy_files)} .thy, {len(pdf_files)} .pdf")

    # --- Fichiers TEX ---
    for f in tex_files:
        f = Path(f)
        try:
            text = extract_text_tex(f)
            sha = sha256_file(f)
            size = f.stat().st_size
            file_id = insert_file(
                conn,
                f.name,
                str(f),
                "tex",
                sha,
                size,
                text
            )
            sections = extract_tex_sections(f)
            insert_tex_structure(conn, file_id, sections)
        except Exception as e:
            print(f"[TEX] Erreur sur {f}: {e}")

    # --- Fichiers THY ---
    for f in thy_files:
        f = Path(f)
        try:
            text = extract_text_thy(f)
            sha = sha256_file(f)
            size = f.stat().st_size
            file_id = insert_file(
                conn,
                f.name,
                str(f),
                "thy",
                sha,
                size,
                text
            )
            struct = extract_thy_structure(f)
            insert_hol_structure(conn, file_id, struct)
        except Exception as e:
            print(f"[THY] Erreur sur {f}: {e}")

    # --- Fichiers PDF ---
    for f in pdf_files:
        f = Path(f)
        try:
            text = extract_text_pdf(f)
            sha = sha256_file(f)
            size = f.stat().st_size
            file_id = insert_file(
                conn,
                f.name,
                str(f),
                "pdf",
                sha,
                size,
                text
            )
            # Nombre de pages
            try:
                from pypdf import PdfReader
                page_count = len(PdfReader(f).pages)
            except Exception:
                page_count = 0
            insert_pdf_structure(conn, file_id, page_count)
        except Exception as e:
            print(f"[PDF] Erreur sur {f}: {e}")

    # --- Arborescences ---
    arbo_hol = build_arborescence_hol(thy_files)
    arbo_tex = build_arborescence_tex(tex_files)
    arbo_pdf = build_arborescence_pdf(pdf_files)
    arbo_global = build_arborescence_globale(arbo_hol, arbo_tex, arbo_pdf)

    insert_arborescence(conn, "hol", arbo_hol)
    insert_arborescence(conn, "latex", arbo_tex)
    insert_arborescence(conn, "pdf", arbo_pdf)
    insert_arborescence(conn, "global", arbo_global)

    # --- Métadonnées ---
    insert_metadata(conn, "created_at", iso_now())
    insert_metadata(conn, "root_dir", str(root.resolve()))
    insert_metadata(conn, "total_tex", str(len(tex_files)))
    insert_metadata(conn, "total_thy", str(len(thy_files)))
    insert_metadata(conn, "total_pdf", str(len(pdf_files)))

    conn.close()
    print("Corpus SQLite généré avec succès.")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage : python3 generate_corpus_db.py <dossier_racine> <fichier_db.sqlite>")
        sys.exit(1)

    root_dir = sys.argv[1]
    db_path = sys.argv[2]

    create_corpus_db(db_path, root_dir)
