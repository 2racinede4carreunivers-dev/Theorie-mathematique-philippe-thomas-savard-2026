#!/usr/bin/env python3
"""
Générateur du corpus SQLite complet (corpus_actions)
Extraction avancée :
- TEX, THY, PDF, MD, TXT
- Arborescences HOL / LaTeX / PDF
- Structure Markdown
- Concepts
- Exemples de calculs (détection avancée, option B)
"""

import os
import re
import sys
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timezone


# ------------------------------------------------------------
# UTILITAIRES
# ------------------------------------------------------------

def iso_now():
    return datetime.now(timezone.utc).isoformat()


def sha256_file(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return f"[Erreur lecture fichier texte: {e}]"


# ------------------------------------------------------------
# EXTRACTION TEX
# ------------------------------------------------------------

def extract_text_tex(filepath: Path) -> str:
    """Extrait le texte brut d'un fichier .tex en retirant les commandes LaTeX."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")

        # Retirer les commentaires
        content = re.sub(r"%.*$", "", content, flags=re.MULTILINE)

        # Retirer environnements begin/end
        content = re.sub(r"\\(begin|end)\{[^}]*\}", "", content)

        # Commandes \commande{...}
        content = re.sub(r"\\[a-zA-Z]+\*?\{([^}]*)\}", r"\1", content)

        # Commandes \commande[options]
        content = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", content)

        # Nettoyage symboles
        content = re.sub(r"[{}$^]", "", content)

        # Espaces
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r" {2,}", " ", content)

        return content.strip()
    except Exception as e:
        return f"[Erreur extraction TEX: {e}]"


def extract_tex_sections(filepath: Path):
    """Extraction simple des sections LaTeX."""
    sections = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        patterns = [
            (r"\\chapter\*?\{([^}]*)\}", "chapter"),
            (r"\\section\*?\{([^}]*)\}", "section"),
            (r"\\subsection\*?\{([^}]*)\}", "subsection"),
            (r"\\subsubsection\*?\{([^}]*)\}", "subsubsection"),
        ]
        for pattern, level in patterns:
            for m in re.finditer(pattern, content):
                sections.append(
                    {
                        "level": level,
                        "title": m.group(1).strip(),
                        "position": m.start(),
                    }
                )
        sections.sort(key=lambda x: x["position"])
    except Exception:
        pass
    return sections


# ------------------------------------------------------------
# EXTRACTION HOL
# ------------------------------------------------------------

def extract_text_thy(filepath: Path) -> str:
    try:
        return filepath.read_text(encoding="utf-8", errors="ignore").strip()
    except Exception as e:
        return f"[Erreur extraction THY: {e}]"


def extract_thy_structure(filepath: Path):
    structure = {
        "theory_name": "",
        "imports": [],
        "theorems": [],
        "lemmas": [],
        "definitions": [],
        "datatypes": [],
        "functions": [],
        "locales": [],
    }
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")

        m = re.search(r"theory\s+(\w+)", content)
        if m:
            structure["theory_name"] = m.group(1)

        imports_match = re.search(r"imports\s+(.*?)begin", content, re.DOTALL)
        if imports_match:
            imports_text = imports_match.group(1)
            structure["imports"] = [
                x
                for pair in re.findall(r'(?:"([^"]+)"|(\S+))', imports_text)
                for x in pair
                if x and x not in ("", "begin")
            ]

        structure["theorems"] = re.findall(r"theorem\s+(\w+)", content)
        structure["lemmas"] = re.findall(r"lemma\s+(\w+)", content)
        structure["definitions"] = re.findall(r"definition\s+(\w+)", content)
        structure["datatypes"] = re.findall(r"datatype\s+(\w+)", content)
        structure["functions"] = re.findall(r"fun\s+(\w+)", content)
        structure["locales"] = re.findall(r"locale\s+(\w+)", content)

    except Exception:
        pass

    return structure


# ------------------------------------------------------------
# EXTRACTION PDF
# ------------------------------------------------------------

def extract_text_pdf(filepath: Path) -> str:
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(filepath))
        parts = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                parts.append(t)
        return "\n\n".join(parts).strip()
    except Exception as e:
        return f"[Erreur extraction PDF: {e}]"


def count_pdf_pages(filepath: Path) -> int:
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(filepath))
        return len(reader.pages)
    except Exception:
        return 0


# ------------------------------------------------------------
# EXTRACTION MARKDOWN / TXT
# ------------------------------------------------------------

def extract_md_structure(text: str):
    """
    Extraction avancée pour .md / .txt :
    - titres
    - listes
    - blocs de code
    - résumé simple
    - nombre de mots
    """
    lines = text.splitlines()
    headings = []
    lists = []
    code_blocks = []
    current_code = []
    in_code = False

    for i, line in enumerate(lines):
        # Titres Markdown
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            headings.append(
                {"level": level, "title": title, "line": i + 1}
            )

        # Listes
        if re.match(r"^\s*[-*+]\s+.+", line):
            lists.append({"line": i + 1, "text": line.strip()})

        # Blocs de code ```...```
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                current_code = [line]
            else:
                current_code.append(line)
                code_blocks.append(
                    {"start_line": i + 1 - len(current_code) + 1, "code": "\n".join(current_code)}
                )
                current_code = []
                in_code = False
        elif in_code:
            current_code.append(line)

    # Résumé simple : premières lignes non vides
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    summary = " ".join(paragraphs[:3]) if paragraphs else ""

    word_count = len(re.findall(r"\w+", text, flags=re.UNICODE))

    return {
        "headings": headings,
        "lists": lists,
        "code_blocks": code_blocks,
        "summary": summary,
        "word_count": word_count,
    }


# ------------------------------------------------------------
# DETECTION AVANCÉE DES CALCULS (Option B)
# ------------------------------------------------------------

CALC_PATTERNS = [
    r"\b\d+\s*/\s*\d+\b",
    r"√\s*\d+",
    r"sqrt\(\s*[^)]+\)",
    r"\\sqrt\{[^}]+\}",
    r"\b[a-zA-Z0-9]+\s*\^\s*[a-zA-Z0-9]+\b",
    r"[a-zA-Z0-9]+\s*\^\s*\{[^}]+\}",
    r"\\sum_{[^}]+}\^{[^}]+}",
    r"\\prod_{[^}]+}\^{[^}]+}",
    r"[a-zA-Z]_{n\+1}\s*=\s*[a-zA-Z]_n[^,\n]*",
    r"\b[a-zA-Z]\s*=\s*[^=\n]+",
]


def detect_calculs(text: str):
    calculs = []
    for pattern in CALC_PATTERNS:
        for m in re.finditer(pattern, text):
            expr = m.group(0).strip()
            start = max(0, m.start() - 60)
            end = min(len(text), m.end() + 60)
            context = text[start:end].replace("\n", " ")
            calculs.append({"expression": expr, "context": context})
    return calculs


def classify_calcul(expr: str) -> str:
    expr = expr.strip()
    if "sqrt" in expr or "√" in expr or "\\sqrt" in expr:
        return "racine"
    if "/" in expr and re.search(r"\d+\s*/\s*\d+", expr):
        return "fraction"
    if "^" in expr:
        return "puissance"
    if "\\sum" in expr:
        return "somme"
    if "\\prod" in expr:
        return "produit"
    if re.search(r"_{n\+1}\s*=", expr):
        return "suite"
    if "=" in expr:
        return "equation"
    return "expression"


# ------------------------------------------------------------
# ARBORESCENCES
# ------------------------------------------------------------

def build_arborescence_hol(thy_files):
    arbo = {"type": "hol", "theories": []}
    for f in thy_files:
        p = Path(f)
        struct = extract_thy_structure(p)
        arbo["theories"].append(
            {
                "file": p.name,
                "path": str(p),
                "theory_name": struct["theory_name"],
                "imports": struct["imports"],
                "theorems": struct["theorems"],
                "lemmas": struct["lemmas"],
                "definitions": struct["definitions"],
                "datatypes": struct["datatypes"],
                "functions": struct["functions"],
                "locales": struct["locales"],
                "total_propositions": len(struct["theorems"]) + len(struct["lemmas"]),
            }
        )

    theory_names = {t["theory_name"]: t["file"] for t in arbo["theories"] if t["theory_name"]}
    for t in arbo["theories"]:
        t["depends_on"] = [imp for imp in t["imports"] if imp in theory_names]

    return arbo


def build_arborescence_tex(tex_files):
    arbo = {"type": "latex", "documents": []}
    for f in tex_files:
        p = Path(f)
        sections = extract_tex_sections(p)
        arbo["documents"].append(
            {
                "file": p.name,
                "path": str(p),
                "sections": sections,
                "total_sections": len(sections),
            }
        )
    return arbo


def build_arborescence_pdf(pdf_files):
    arbo = {"type": "pdf", "documents": []}
    for f in pdf_files:
        p = Path(f)
        pages = count_pdf_pages(p)
        arbo["documents"].append(
            {
                "file": p.name,
                "path": str(p),
                "pages": pages,
            }
        )
    return arbo


def build_arborescence_globale(arbo_hol, arbo_tex, arbo_pdf):
    tex_bases = {os.path.splitext(d["file"])[0]: d for d in arbo_tex["documents"]}
    pdf_bases = {os.path.splitext(d["file"])[0]: d for d in arbo_pdf["documents"]}
    thy_bases = {os.path.splitext(d["file"])[0]: d for d in arbo_hol["theories"]}

    all_bases = set(list(tex_bases.keys()) + list(pdf_bases.keys()) + list(thy_bases.keys()))
    links = []

    for base in all_bases:
        link = {"concept": base, "files": {}}
        if base in tex_bases:
            link["files"]["tex"] = tex_bases[base]["file"]
        if base in pdf_bases:
            link["files"]["pdf"] = pdf_bases[base]["file"]
        if base in thy_bases:
            link["files"]["thy"] = thy_bases[base]["file"]
        links.append(link)

    return {
        "type": "global",
        "total_tex": len(arbo_tex["documents"]),
        "total_thy": len(arbo_hol["theories"]),
        "total_pdf": len(arbo_pdf["documents"]),
        "total_theorems": sum(t["total_propositions"] for t in arbo_hol["theories"]),
        "links": links,
        "hol": arbo_hol,
        "latex": arbo_tex,
        "pdf": arbo_pdf,
    }


# ------------------------------------------------------------
# CREATION SCHEMA
# ------------------------------------------------------------

def create_schema(conn: sqlite3.Connection):
    c = conn.cursor()
    c.executescript(
        """
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

        CREATE TABLE IF NOT EXISTS md_structure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            headings TEXT,
            lists TEXT,
            code_blocks TEXT,
            summary TEXT,
            word_count INTEGER DEFAULT 0,
            FOREIGN KEY (file_id) REFERENCES files(id)
        );

        CREATE TABLE IF NOT EXISTS calculs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            expression TEXT NOT NULL,
            context TEXT,
            calc_type TEXT,
            created_at TEXT NOT NULL,
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
    )
    conn.commit()


# ------------------------------------------------------------
# INSERT HELPERS
# ------------------------------------------------------------

def insert_file(conn, filename, filepath, filetype, sha256, filesize, extracted_text):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO files (filename, filepath, filetype, sha256, filesize, extracted_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (filename, filepath, filetype, sha256, filesize, extracted_text, iso_now()),
    )
    conn.commit()
    return c.lastrowid


def insert_tex_structure(conn, file_id, sections):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO tex_structure (file_id, sections, total_sections)
        VALUES (?, ?, ?)
        """,
        (file_id, json.dumps(sections, ensure_ascii=False), len(sections)),
    )
    conn.commit()


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
            struct.get("theory_name", ""),
            json.dumps(struct.get("imports", []), ensure_ascii=False),
            json.dumps(struct.get("theorems", []), ensure_ascii=False),
            json.dumps(struct.get("lemmas", []), ensure_ascii=False),
            json.dumps(struct.get("definitions", []), ensure_ascii=False),
            json.dumps(struct.get("datatypes", []), ensure_ascii=False),
            json.dumps(struct.get("functions", []), ensure_ascii=False),
            json.dumps(struct.get("locales", []), ensure_ascii=False),
            len(struct.get("theorems", [])) + len(struct.get("lemmas", [])),
        ),
    )
    conn.commit()


def insert_pdf_structure(conn, file_id, page_count):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO pdf_structure (file_id, page_count)
        VALUES (?, ?)
        """,
        (file_id, page_count),
    )
    conn.commit()

def insert_markdown_examples(conn, corpus_root):
    """
    Lecture et insertion du fichier exemple_calculs.md dans la base corpus.db
    """
    md_path = corpus_root / "exemple_calculs.md"
    if not md_path.exists():
        print("[INFO] Aucun fichier exemple_calculs.md trouvé, étape ignorée.")
        return

    text = md_path.read_text(encoding="utf-8", errors="ignore")
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    filesize = len(text.encode("utf-8"))

    file_id = insert_file(
        conn,
        filename=md_path.name,
        filepath=str(md_path),
        filetype="markdown",
        sha256=sha,
        filesize=filesize,
        extracted_text=text,
    )

    md_struct = extract_md_structure(text)
    insert_md_structure(conn, file_id, md_struct)
    print(f"[OK] Fichier Markdown {md_path.name} ajouté au corpus.")
