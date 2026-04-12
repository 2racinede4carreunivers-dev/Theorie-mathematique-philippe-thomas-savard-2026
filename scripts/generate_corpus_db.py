#!/usr/bin/env python3
"""
Generateur du corpus SQLite complet (Option C)
Extraction textuelle PDF, TEX, THY + arborescences HOL, LaTeX, PDF, globale

Execute par le job generate_corpus_db dans build.yml
"""

import os
import sys
import re
import sqlite3
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone


def sha256_file(filepath):
    """Calcule le SHA-256 d'un fichier."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def extract_text_tex(filepath):
    """Extrait le texte brut d'un fichier .tex en retirant les commandes LaTeX."""
    try:
        content = Path(filepath).read_text(encoding='utf-8', errors='ignore')
        # Retirer les commentaires
        content = re.sub(r'%.*$', '', content, flags=re.MULTILINE)
        # Retirer les commandes LaTeX communes
        content = re.sub(r'\\(begin|end)\{[^}]*\}', '', content)
        content = re.sub(r'\\[a-zA-Z]+\*?\{([^}]*)\}', r'\1', content)
        content = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?', '', content)
        content = re.sub(r'[{}$]', '', content)
        # Nettoyer les espaces multiples
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r' {2,}', ' ', content)
        return content.strip()
    except Exception as e:
        return f"[Erreur extraction TEX: {e}]"


def extract_text_thy(filepath):
    """Extrait le texte et la structure d'un fichier .thy Isabelle/HOL."""
    try:
        content = Path(filepath).read_text(encoding='utf-8', errors='ignore')
        return content.strip()
    except Exception as e:
        return f"[Erreur extraction THY: {e}]"


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


def extract_tex_sections(filepath):
    """Extrait la structure des sections d'un fichier .tex."""
    sections = []
    try:
        content = Path(filepath).read_text(encoding='utf-8', errors='ignore')
        patterns = [
            (r'\\chapter\*?\{([^}]*)\}', 'chapter'),
            (r'\\section\*?\{([^}]*)\}', 'section'),
            (r'\\subsection\*?\{([^}]*)\}', 'subsection'),
            (r'\\subsubsection\*?\{([^}]*)\}', 'subsubsection'),
        ]
        for pattern, level in patterns:
            for match in re.finditer(pattern, content):
                sections.append({
                    'level': level,
                    'title': match.group(1).strip(),
                    'position': match.start()
                })
        sections.sort(key=lambda x: x['position'])
    except Exception:
        pass
    return sections


def extract_thy_structure(filepath):
    """Extrait la structure logique d'un fichier .thy (theoremes, lemmes, imports)."""
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

        # Nom de la theorie
        m = re.search(r'theory\s+(\w+)', content)
        if m:
            structure['theory_name'] = m.group(1)

        # Imports
        imports_match = re.search(r'imports\s+(.*?)begin', content, re.DOTALL)
        if imports_match:
            imports_text = imports_match.group(1)
            structure['imports'] = [i.strip().strip('"') for i in re.findall(r'(?:"([^"]+)"|(\S+))', imports_text) if any(x for x in i)]
            structure['imports'] = [x for pair in re.findall(r'(?:"([^"]+)"|(\S+))', imports_text) for x in pair if x and x not in ('', 'begin')]

        # Theoremes
        for m in re.finditer(r'theorem\s+(\w+)', content):
            structure['theorems'].append(m.group(1))

        # Lemmes
        for m in re.finditer(r'lemma\s+(\w+)', content):
            structure['lemmas'].append(m.group(1))

        # Definitions
        for m in re.finditer(r'definition\s+(\w+)', content):
            structure['definitions'].append(m.group(1))

        # Datatypes
        for m in re.finditer(r'datatype\s+(\w+)', content):
            structure['datatypes'].append(m.group(1))

        # Fonctions
        for m in re.finditer(r'fun\s+(\w+)', content):
            structure['functions'].append(m.group(1))

        # Locales
        for m in re.finditer(r'locale\s+(\w+)', content):
            structure['locales'].append(m.group(1))

    except Exception:
        pass
    return structure


def build_arborescence_hol(thy_files):
    """Construit l'arborescence logique HOL a partir des fichiers .thy."""
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
    # Construire les liens de dependances
    theory_names = {t['theory_name']: t['file'] for t in arbo['theories']}
    for t in arbo['theories']:
        t['depends_on'] = [imp for imp in t['imports'] if imp in theory_names]
    return arbo


def build_arborescence_tex(tex_files):
    """Construit l'arborescence documentaire LaTeX."""
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
    """Construit l'arborescence narrative PDF."""
    arbo = {'type': 'pdf', 'documents': []}
    for f in pdf_files:
        page_count = 0
        try:
            from pypdf import PdfReader
            reader = PdfReader(f)
            page_count = len(reader.pages)
        except Exception:
            pass
        arbo['documents'].append({
            'file': os.path.basename(f),
            'path': str(f),
            'pages': page_count,
        })
    return arbo


def build_arborescence_globale(arbo_hol, arbo_tex, arbo_pdf):
    """Construit l'arborescence globale unifiant HOL, LaTeX et PDF."""
    # Creer les liens entre documents par nom de base
    links = []
    tex_bases = {os.path.splitext(d['file'])[0]: d for d in arbo_tex['documents']}
    pdf_bases = {os.path.splitext(d['file'])[0]: d for d in arbo_pdf['documents']}
    thy_bases = {os.path.splitext(d['file'])[0]: d for d in arbo_hol['theories']}

    all_bases = set(list(tex_bases.keys()) + list(pdf_bases.keys()) + list(thy_bases.keys()))
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


def create_corpus_db(db_path, tex_files, thy_files, pdf_files):
    """Cree la base de donnees SQLite corpus.db complete."""
    print(f"Creation de {db_path}...")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Schema
    c.executescript('''
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
    ''')

    now = datetime.now(timezone.utc).isoformat()

    # Metadata
    commit_sha = os.environ.get('GITHUB_SHA', 'local')
    c.execute("INSERT OR REPLACE INTO metadata VALUES (?, ?)", ('generated_at', now))
    c.execute("INSERT OR REPLACE INTO metadata VALUES (?, ?)", ('commit_sha', commit_sha))
    c.execute("INSERT OR REPLACE INTO metadata VALUES (?, ?)", ('version', '1.0.0'))

    # Inserer les fichiers TEX
    print("  Extraction des fichiers .tex...")
    for f in tex_files:
        sha = sha256_file(f)
        size = os.path.getsize(f)
        text = extract_text_tex(f)
        sections = extract_tex_sections(f)

        c.execute('''INSERT INTO files (filename, filepath, filetype, sha256, filesize, extracted_text, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (os.path.basename(f), str(f), 'tex', sha, size, text, now))
        file_id = c.lastrowid
        c.execute('''INSERT INTO tex_structure (file_id, sections, total_sections)
                     VALUES (?, ?, ?)''',
                  (file_id, json.dumps(sections, ensure_ascii=False), len(sections)))
        print(f"    {os.path.basename(f)}: {len(text)} car., {len(sections)} sections")

    # Inserer les fichiers THY
    print("  Extraction des fichiers .thy...")
    for f in thy_files:
        sha = sha256_file(f)
        size = os.path.getsize(f)
        text = extract_text_thy(f)
        struct = extract_thy_structure(f)

        c.execute('''INSERT INTO files (filename, filepath, filetype, sha256, filesize, extracted_text, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (os.path.basename(f), str(f), 'thy', sha, size, text, now))
        file_id = c.lastrowid
        c.execute('''INSERT INTO hol_structure (file_id, theory_name, imports, theorems, lemmas, definitions, datatypes, functions, locales, total_propositions)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (file_id, struct['theory_name'],
                   json.dumps(struct['imports']),
                   json.dumps(struct['theorems']),
                   json.dumps(struct['lemmas']),
                   json.dumps(struct['definitions']),
                   json.dumps(struct['datatypes']),
                   json.dumps(struct['functions']),
                   json.dumps(struct['locales']),
                   len(struct['theorems']) + len(struct['lemmas'])))
        total_p = len(struct['theorems']) + len(struct['lemmas'])
        print(f"    {os.path.basename(f)}: theorie={struct['theory_name']}, {total_p} propositions")

    # Inserer les fichiers PDF
    print("  Extraction des fichiers .pdf...")
    for f in pdf_files:
        sha = sha256_file(f)
        size = os.path.getsize(f)
        text = extract_text_pdf(f)
        page_count = 0
        try:
            from pypdf import PdfReader
            page_count = len(PdfReader(f).pages)
        except Exception:
            pass

        c.execute('''INSERT INTO files (filename, filepath, filetype, sha256, filesize, extracted_text, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (os.path.basename(f), str(f), 'pdf', sha, size, text, now))
        file_id = c.lastrowid
        c.execute('''INSERT INTO pdf_structure (file_id, page_count) VALUES (?, ?)''',
                  (file_id, page_count))
        print(f"    {os.path.basename(f)}: {page_count} pages, {len(text)} car.")

    # Generer les arborescences
    print("  Generation des arborescences...")
    arbo_hol = build_arborescence_hol(thy_files)
    arbo_tex = build_arborescence_tex(tex_files)
    arbo_pdf = build_arborescence_pdf(pdf_files)
    arbo_globale = build_arborescence_globale(arbo_hol, arbo_tex, arbo_pdf)

    c.execute("INSERT INTO arborescences (arbo_type, arbo_data, created_at) VALUES (?, ?, ?)",
              ('hol', json.dumps(arbo_hol, ensure_ascii=False, indent=2), now))
    c.execute("INSERT INTO arborescences (arbo_type, arbo_data, created_at) VALUES (?, ?, ?)",
              ('latex', json.dumps(arbo_tex, ensure_ascii=False, indent=2), now))
    c.execute("INSERT INTO arborescences (arbo_type, arbo_data, created_at) VALUES (?, ?, ?)",
              ('pdf', json.dumps(arbo_pdf, ensure_ascii=False, indent=2), now))
    c.execute("INSERT INTO arborescences (arbo_type, arbo_data, created_at) VALUES (?, ?, ?)",
              ('global', json.dumps(arbo_globale, ensure_ascii=False, indent=2), now))
    print("    4 arborescences generees (HOL, LaTeX, PDF, globale)")

    # Extraire les concepts depuis les theoremes et sections
    print("  Extraction des concepts...")
    for t in arbo_hol['theories']:
        for thm in t['theorems']:
            c.execute("INSERT INTO concepts (concept_name, source_files, concept_type) VALUES (?, ?, ?)",
                      (thm, json.dumps([t['file']]), 'theorem'))
        for lem in t['lemmas']:
            c.execute("INSERT INTO concepts (concept_name, source_files, concept_type) VALUES (?, ?, ?)",
                      (lem, json.dumps([t['file']]), 'lemma'))
        for defn in t['definitions']:
            c.execute("INSERT INTO concepts (concept_name, source_files, concept_type) VALUES (?, ?, ?)",
                      (defn, json.dumps([t['file']]), 'definition'))
        for loc in t['locales']:
            c.execute("INSERT INTO concepts (concept_name, source_files, concept_type) VALUES (?, ?, ?)",
                      (loc, json.dumps([t['file']]), 'locale'))

    conn.commit()

    # Statistiques finales
    c.execute("SELECT COUNT(*) FROM files")
    total_files = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM concepts")
    total_concepts = c.fetchone()[0]
    c.execute("SELECT SUM(LENGTH(extracted_text)) FROM files")
    total_text = c.fetchone()[0] or 0

    conn.close()

    print(f"\nCorpus genere: {db_path}")
    print(f"  Fichiers: {total_files}")
    print(f"  Concepts: {total_concepts}")
    print(f"  Texte extrait: {total_text} caracteres")
    print(f"  Arborescences: 4 (HOL, LaTeX, PDF, globale)")
    print(f"  Taille DB: {os.path.getsize(db_path)} octets")


def main():
    print("=" * 60)
    print("GENERATION DU CORPUS SQLite (Option C - Extraction complete)")
    print("=" * 60)

    # Trouver les fichiers
    root = Path('.')
    tex_files = sorted([str(f) for f in root.rglob('src/tex/*.tex')])
    thy_files = sorted([str(f) for f in root.rglob('src/hol/*.thy')])
    pdf_files = sorted([str(f) for f in root.rglob('src/pdf/*.pdf')])

    print(f"\nFichiers trouves:")
    print(f"  .tex: {len(tex_files)}")
    print(f"  .thy: {len(thy_files)}")
    print(f"  .pdf: {len(pdf_files)}")

    if not tex_files and not thy_files:
        print("ERREUR: Aucun fichier source trouve")
        sys.exit(1)

    # Creer le dossier de sortie
    Path('corpus_output').mkdir(exist_ok=True)
    db_path = 'corpus_output/corpus.db'

    # Supprimer l'ancienne DB si elle existe
    if os.path.exists(db_path):
        os.remove(db_path)

    create_corpus_db(db_path, tex_files, thy_files, pdf_files)

    print("\n" + "=" * 60)
    print("CORPUS GENERE AVEC SUCCES")
    print("=" * 60)


if __name__ == "__main__":
    main()
