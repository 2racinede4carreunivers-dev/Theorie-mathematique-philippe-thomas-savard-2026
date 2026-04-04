#!/usr/bin/env python3
"""
Générateur de Questions/Réponses pour la Théorie Mathématique Philippe Thomas Savard
Utilise OpenAI GPT-4o via la clé Emergent pour analyser les documents et générer des Q&R

Ce script est conçu pour être exécuté dans GitHub Actions après la compilation des documents.
"""

import os
import sys
import json
import glob
import asyncio
import hashlib
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from pathlib import Path

# Ajouter le dossier scripts au path pour les imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# Configuration
from qa_config import (
    LANGUAGES, QUESTION_RATIO, QUESTIONS_PER_RUN, MATH_CATEGORIES,
    PHILO_CATEGORIES, FILE_EXTENSIONS, OPENAI_CONFIG, REPO_PATHS,
    DATABASE_CONFIG, DIFFICULTY_LEVELS, ANSWER_QUALITY, TAGS
)
from qa_database import QADatabase

# Import de la bibliothèque Emergent pour l'intégration LLM
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
except ImportError:
    print("Installation de emergentintegrations...")
    os.system("pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/")
    from emergentintegrations.llm.chat import LlmChat, UserMessage


class DocumentAnalyzer:
    """Analyse les documents .tex, .thy et extrait le contenu pertinent."""
    
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
    
    def find_documents(self) -> Dict[str, List[Path]]:
        """Trouve tous les documents à analyser."""
        documents = {ext: [] for ext in FILE_EXTENSIONS.keys()}
        
        for ext in FILE_EXTENSIONS.keys():
            pattern = f"**/*{ext}"
            files = list(self.repo_root.glob(pattern))
            documents[ext] = [f for f in files if not any(x in str(f) for x in ['.git', 'node_modules', '__pycache__'])]
        
        return documents
    
    def extract_content(self, file_path: Path) -> Dict:
        """Extrait le contenu d'un fichier."""
        content = {
            "path": str(file_path),
            "type": file_path.suffix,
            "name": file_path.name,
            "content": "",
            "sections": [],
            "key_terms": []
        }
        
        try:
            if file_path.suffix in ['.tex', '.thy']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content["content"] = f.read()
                    
                # Extraction des sections pour .tex
                if file_path.suffix == '.tex':
                    content["sections"] = self._extract_tex_sections(content["content"])
                    content["key_terms"] = self._extract_tex_terms(content["content"])
                
                # Extraction pour .thy (Isabelle)
                elif file_path.suffix == '.thy':
                    content["sections"] = self._extract_thy_sections(content["content"])
                    content["key_terms"] = self._extract_thy_terms(content["content"])
                    
        except Exception as e:
            print(f"Erreur lors de la lecture de {file_path}: {e}")
        
        return content
    
    def _extract_tex_sections(self, content: str) -> List[Dict]:
        """Extrait les sections d'un fichier LaTeX."""
        sections = []
        import re
        
        # Pattern pour les sections LaTeX
        section_patterns = [
            (r'\\section\{([^}]+)\}', 'section'),
            (r'\\subsection\{([^}]+)\}', 'subsection'),
            (r'\\chapter\{([^}]+)\}', 'chapter'),
            (r'\\theorem\{([^}]+)\}', 'theorem'),
            (r'\\definition\{([^}]+)\}', 'definition'),
            (r'\\lemma\{([^}]+)\}', 'lemma'),
            (r'\\proof', 'proof'),
        ]
        
        for pattern, sec_type in section_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                title = match.group(1) if match.lastindex else sec_type
                sections.append({
                    "type": sec_type,
                    "title": title,
                    "position": match.start()
                })
        
        return sorted(sections, key=lambda x: x['position'])
    
    def _extract_tex_terms(self, content: str) -> List[str]:
        """Extrait les termes mathématiques clés d'un fichier LaTeX."""
        import re
        terms = set()
        
        # Termes définis
        defined = re.findall(r'\\(?:newcommand|def|let)\{?\\([a-zA-Z]+)', content)
        terms.update(defined)
        
        # Environnements mathématiques
        envs = re.findall(r'\\begin\{(equation|align|theorem|definition|lemma|proof)\*?\}', content)
        terms.update(envs)
        
        # Symboles mathématiques importants
        math_symbols = re.findall(r'\$([^$]+)\$', content)
        for sym in math_symbols[:50]:  # Limiter
            if len(sym) < 50:
                terms.add(sym.strip())
        
        return list(terms)[:100]
    
    def _extract_thy_sections(self, content: str) -> List[Dict]:
        """Extrait les sections d'un fichier Isabelle/HOL."""
        sections = []
        import re
        
        thy_patterns = [
            (r'theory\s+(\w+)', 'theory'),
            (r'theorem\s+(\w+):', 'theorem'),
            (r'lemma\s+(\w+):', 'lemma'),
            (r'definition\s+(\w+):', 'definition'),
            (r'fun\s+(\w+)\s+::', 'function'),
            (r'datatype\s+(\w+)\s+=', 'datatype'),
            (r'proof\s*-', 'proof'),
        ]
        
        for pattern, sec_type in thy_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                title = match.group(1) if match.lastindex else sec_type
                sections.append({
                    "type": sec_type,
                    "title": title,
                    "position": match.start()
                })
        
        return sorted(sections, key=lambda x: x['position'])
    
    def _extract_thy_terms(self, content: str) -> List[str]:
        """Extrait les termes d'un fichier Isabelle."""
        import re
        terms = set()
        
        # Théorèmes et lemmes
        theorems = re.findall(r'(?:theorem|lemma)\s+(\w+)', content)
        terms.update(theorems)
        
        # Définitions
        defs = re.findall(r'definition\s+(\w+)', content)
        terms.update(defs)
        
        # Types de données
        datatypes = re.findall(r'datatype\s+(\w+)', content)
        terms.update(datatypes)
        
        return list(terms)


class QAGenerator:
    """Générateur de Questions/Réponses utilisant l'IA."""
    
    def __init__(self, api_key: str, language: str = "fr"):
        self.api_key = api_key
        self.language = language
        self.chat = None
        self._init_chat()
    
    def _init_chat(self):
        """Initialise le client LLM."""
        session_id = f"qa-gen-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        system_message = self._get_system_prompt()
        
        self.chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=system_message
        ).with_model("openai", OPENAI_CONFIG["model"])
    
    def _get_system_prompt(self) -> str:
        """Retourne le prompt système pour la génération de Q&R."""
        if self.language == "fr":
            return """Tu es un expert en mathématiques et en pédagogie, spécialisé dans la théorie complète "L'Univers est au Carré" de Philippe Thomas Savard (2026).

CONTEXTE DE LA THÉORIE:
La théorie "L'Univers est au Carré" est une œuvre mathématique complète qui comprend PLUSIEURS chapitres et sections:
- Le postulat unique du "squaring" (postulat_carre, postulat_univers_carre) - UN des chapitres
- Les fondements géométriques et algébriques
- Les démonstrations formelles en Isabelle/HOL
- Les applications et corollaires
- Les implications philosophiques et ontologiques

IMPORTANT: Tu dois générer des questions sur L'ENSEMBLE de la théorie, pas seulement sur le postulat unique. Couvre tous les chapitres, sections et concepts présents dans les documents fournis.

Ta mission est de générer des questions et réponses de haute qualité basées sur TOUT le contenu mathématique fourni, en variant les sujets pour couvrir l'ensemble de l'œuvre.

RÈGLES IMPORTANTES:
1. Génère des questions variées couvrant TOUS les chapitres et aspects de la théorie
2. Ne te limite PAS au postulat unique - explore TOUTE la documentation
3. Les réponses doivent être précises, complètes et pédagogiques
4. Inclus des références aux formules et théorèmes quand pertinent
5. Adapte le niveau de difficulté selon les instructions
6. Pour les questions philosophiques, explore les implications profondes de la théorie
7. Mentionne explicitement de quel chapitre/section provient chaque question

FORMAT DE SORTIE (JSON):
{
    "questions": [
        {
            "question": "La question complète",
            "answer": "La réponse détaillée",
            "category": "mathematique|philosophique",
            "subcategory": "definition|demonstration|theoreme|...",
            "difficulty": "debutant|intermediaire|avance|expert",
            "tags": ["tag1", "tag2"],
            "source_reference": "Fichier ou section source"
        }
    ]
}"""
        else:
            return """You are an expert in mathematics and pedagogy, specialized in the "Universe is Squared" theory by Philippe Thomas Savard.

Your mission is to generate high-quality questions and answers based on the mathematical content provided.

OUTPUT FORMAT (JSON):
{
    "questions": [
        {
            "question": "The complete question",
            "answer": "The detailed answer",
            "category": "mathematique|philosophique",
            "subcategory": "definition|demonstration|theorem|...",
            "difficulty": "beginner|intermediate|advanced|expert",
            "tags": ["tag1", "tag2"],
            "source_reference": "Source file or section"
        }
    ]
}"""
    
    async def generate_questions(self, 
                                 documents: List[Dict], 
                                 context: Dict = None,
                                 num_math: int = 10,
                                 num_philo: int = 1) -> List[Dict]:
        """Génère des questions basées sur les documents fournis."""
        
        # Préparer le contenu pour l'analyse
        content_summary = self._prepare_content_summary(documents)
        
        # Préparer le contexte intelligent (si disponible)
        context_prompt = ""
        if context and context.get("validated_examples"):
            context_prompt = self._prepare_context_prompt(context)
        
        # Prompt pour les questions mathématiques
        math_prompt = f"""Analyse le contenu mathématique suivant et génère exactement {num_math} questions mathématiques/techniques variées.

IMPORTANT: Les questions doivent couvrir L'ENSEMBLE de la théorie "L'Univers est au Carré", pas seulement le postulat unique. 
Assure-toi de varier les sources et de poser des questions sur DIFFÉRENTS fichiers et chapitres.

CONTENU À ANALYSER (provenant de plusieurs fichiers/chapitres):
{content_summary}

{context_prompt}

CATÉGORIES À COUVRIR (répartis les questions sur TOUS les chapitres):
- Définitions et concepts fondamentaux (de différents chapitres)
- Démonstrations et preuves formelles (Isabelle/HOL)
- Théorèmes et leurs applications  
- Formules et équations clés
- Relations entre concepts de différentes parties de la théorie
- Applications pratiques

CONSIGNE: Chaque question doit mentionner explicitement de quel fichier/chapitre elle provient dans "source_reference".

Génère les questions en JSON selon le format spécifié."""

        # Prompt pour la question philosophique
        philo_prompt = f"""Basé sur l'ENSEMBLE de la théorie "L'Univers est au Carré" (pas seulement le postulat), génère exactement {num_philo} question(s) philosophique(s)/ontologique(s) sur:
- La signification profonde de la théorie COMPLÈTE pour la compréhension de l'univers
- L'impact sur notre vision du monde
- Les implications épistémologiques de l'ensemble de l'œuvre

CONTENU:
{content_summary[:2000]}

Génère en JSON selon le format spécifié."""

        questions = []
        
        # Générer les questions mathématiques (avec retry si pas assez)
        max_retries = 2
        for attempt in range(max_retries):
            try:
                print(f"   Génération des questions mathématiques (tentative {attempt + 1})...")
                math_response = await self.chat.send_message(UserMessage(text=math_prompt))
                math_questions = self._parse_response(math_response)
                questions.extend(math_questions)
                
                if len(math_questions) >= num_math:
                    break
                elif attempt < max_retries - 1:
                    print(f"   ⚠️ Seulement {len(math_questions)} questions générées, nouvelle tentative...")
                    
            except Exception as e:
                print(f"Erreur génération math: {e}")
        
        # Générer la question philosophique
        try:
            print(f"   Génération de la question philosophique...")
            philo_response = await self.chat.send_message(UserMessage(text=philo_prompt))
            philo_questions = self._parse_response(philo_response)
            questions.extend(philo_questions)
        except Exception as e:
            print(f"Erreur génération philo: {e}")
        
        print(f"   ✅ Total: {len(questions)} questions générées")
        return questions
    
    def _prepare_content_summary(self, documents: List[Dict]) -> str:
        """Prépare un résumé du contenu pour l'analyse."""
        summary_parts = []
        
        for doc in documents:
            if doc.get("content"):
                # Limiter la taille par document
                content = doc["content"][:5000]
                summary_parts.append(f"""
=== {doc['name']} ({doc['type']}) ===
Sections: {', '.join([s['title'] for s in doc.get('sections', [])[:10]])}
Termes clés: {', '.join(doc.get('key_terms', [])[:20])}

Contenu:
{content}
""")
        
        return '\n'.join(summary_parts)[:15000]  # Limite globale
    
    def _prepare_context_prompt(self, context: Dict) -> str:
        """Prépare le contexte intelligent pour améliorer la génération."""
        prompt = "\nCONTEXTE POUR AMÉLIORER LA QUALITÉ:\n"
        
        if context.get("validated_examples"):
            prompt += "\nExemples de Q&R validées précédemment (inspire-toi du style):\n"
            for ex in context["validated_examples"][:3]:
                prompt += f"Q: {ex['question'][:100]}...\n"
        
        if context.get("successful_patterns"):
            prompt += f"\nPatterns qui fonctionnent bien: {[p['pattern_value'] for p in context['successful_patterns'][:5]]}\n"
        
        if context.get("key_concepts"):
            concepts = [c['concept'] for c in context["key_concepts"][:10]]
            prompt += f"\nConcepts clés à inclure: {concepts}\n"
        
        return prompt
    
    def _parse_response(self, response: str) -> List[Dict]:
        """Parse la réponse JSON du LLM."""
        try:
            # Nettoyer la réponse
            response = response.strip()
            
            # Supprimer les balises markdown de code si présentes
            import re
            response = re.sub(r'```json\s*', '', response)
            response = re.sub(r'```\s*', '', response)
            
            # Chercher le JSON dans la réponse (objet avec "questions")
            json_match = re.search(r'\{[\s\S]*"questions"[\s\S]*\}', response)
            if json_match:
                json_str = json_match.group()
                # S'assurer que le JSON est complet
                data = json.loads(json_str)
                questions = data.get("questions", [])
                print(f"   → {len(questions)} questions parsées")
                return questions
            
            # Essayer de parser directement comme tableau
            array_match = re.search(r'\[[\s\S]*\]', response)
            if array_match:
                questions = json.loads(array_match.group())
                if isinstance(questions, list):
                    print(f"   → {len(questions)} questions parsées (tableau)")
                    return questions
                    
        except json.JSONDecodeError as e:
            print(f"Erreur parsing JSON: {e}")
            print(f"Réponse brute (500 premiers caractères): {response[:500]}")
        
        return []


async def main():
    """Point d'entrée principal pour GitHub Actions."""
    
    print("=" * 60)
    print("Génération de Questions/Réponses - Théorie Savard")
    print("=" * 60)
    
    # Configuration
    api_key = os.environ.get("EMERGENT_LLM_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERREUR: Aucune clé API trouvée (EMERGENT_LLM_KEY ou OPENAI_API_KEY)")
        sys.exit(1)
    
    commit_sha = os.environ.get("GITHUB_SHA", "local")[:8]
    run_id = f"gen-{commit_sha}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Déterminer les langues actives
    active_languages = [lang for lang, config in LANGUAGES.items() if config["enabled"]]
    
    print(f"\nConfiguration:")
    print(f"  - Run ID: {run_id}")
    print(f"  - Commit: {commit_sha}")
    print(f"  - Langues: {active_languages}")
    print(f"  - Questions par run: {QUESTIONS_PER_RUN}")
    
    # Analyser les documents
    print("\n1. Analyse des documents...")
    analyzer = DocumentAnalyzer(".")
    documents_by_type = analyzer.find_documents()
    
    all_documents = []
    for doc_type, files in documents_by_type.items():
        print(f"   - {doc_type}: {len(files)} fichiers")
        for f in files:
            doc_content = analyzer.extract_content(f)
            if doc_content["content"]:
                all_documents.append(doc_content)
    
    if not all_documents:
        print("ERREUR: Aucun document trouvé à analyser")
        sys.exit(1)
    
    print(f"   Total: {len(all_documents)} documents avec contenu")
    
    # Initialiser la base de données
    print("\n2. Initialisation de la banque de données...")
    db = QADatabase(DATABASE_CONFIG["db_path"])
    db.start_generation_run(run_id, commit_sha, [d["path"] for d in all_documents])
    
    # Obtenir le contexte intelligent
    context = db.get_context_for_generation()
    print(f"   - Q&R validées existantes: {len(context['validated_examples'])}")
    print(f"   - Concepts clés: {len(context['key_concepts'])}")
    
    # Générer les questions pour chaque langue active
    all_generated = []
    
    for lang in active_languages:
        print(f"\n3. Génération des Q&R en {LANGUAGES[lang]['name']}...")
        
        generator = QAGenerator(api_key, lang)
        
        questions = await generator.generate_questions(
            all_documents,
            context=context,
            num_math=QUESTION_RATIO["mathematique"],
            num_philo=QUESTION_RATIO["philosophique"]
        )
        
        print(f"   - Générées: {len(questions)} questions")
        
        # Ajouter à la base de données (en attente)
        for q in questions:
            qa_id = db.add_pending_qa(
                question=q.get("question", ""),
                answer=q.get("answer", ""),
                category=q.get("category", "mathematique"),
                subcategory=q.get("subcategory"),
                difficulty=q.get("difficulty", "intermediaire"),
                language=lang,
                tags=q.get("tags", []),
                source_files=[d["path"] for d in all_documents[:5]],
                source_commit=commit_sha,
                run_id=run_id
            )
            if qa_id:
                q["db_id"] = qa_id
                all_generated.append(q)
    
    # Compléter la génération
    db.complete_generation_run(run_id, len(all_generated))
    
    # Sauvegarder le résultat pour l'artifact
    output_dir = "qa_output"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/generated_qa_{run_id}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "run_id": run_id,
            "commit": commit_sha,
            "generated_at": datetime.now().isoformat(),
            "total_questions": len(all_generated),
            "questions": all_generated
        }, f, ensure_ascii=False, indent=2)
    
    # Créer aussi un fichier Markdown pour review facile
    md_file = f"{output_dir}/generated_qa_{run_id}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# Questions/Réponses Générées\n\n")
        f.write(f"**Run ID:** {run_id}\n")
        f.write(f"**Commit:** {commit_sha}\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")
        
        for i, q in enumerate(all_generated, 1):
            f.write(f"## {i}. {q.get('question', 'N/A')}\n\n")
            f.write(f"**Catégorie:** {q.get('category', 'N/A')} / {q.get('subcategory', 'N/A')}\n")
            f.write(f"**Difficulté:** {q.get('difficulty', 'N/A')}\n")
            f.write(f"**Tags:** {', '.join(q.get('tags', []))}\n\n")
            f.write(f"### Réponse\n\n{q.get('answer', 'N/A')}\n\n")
            f.write("---\n\n")
    
    print(f"\n4. Résultats sauvegardés:")
    print(f"   - JSON: {output_file}")
    print(f"   - Markdown: {md_file}")
    
    # Statistiques finales
    stats = db.get_statistics()
    print(f"\n5. Statistiques de la banque:")
    print(f"   - Total Q&R validées: {stats['total_validated']}")
    print(f"   - Q&R en attente: {stats['total_pending']}")
    print(f"   - Score qualité moyen: {stats['avg_quality_score']:.2f}")
    
    print("\n" + "=" * 60)
    print("Génération terminée avec succès!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
