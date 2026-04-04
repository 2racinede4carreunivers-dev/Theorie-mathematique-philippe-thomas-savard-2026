"""
Gestion de la banque de données SQLite pour les Questions/Réponses
Théorie Mathématique Philippe Thomas Savard 2026

Cette banque est "intelligente" : elle apprend des Q&R validées pour améliorer
les futures générations de questions.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import hashlib

class QADatabase:
    """
    Gestionnaire de la banque de Questions/Réponses SQLite.
    
    Fonctionnalités intelligentes:
    - Apprentissage des patterns de questions validées
    - Détection des doublons sémantiques
    - Statistiques d'utilisation pour améliorer la génération
    - Historique des versions et évolution de la banque
    """
    
    def __init__(self, db_path: str = "qa_bank/qa_bank.db"):
        self.db_path = db_path
        self._ensure_directory()
        self._init_database()
        self._migrate_database()
    
    def _ensure_directory(self):
        """Crée le répertoire de la base de données si nécessaire."""
        if os.path.dirname(self.db_path):
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _migrate_database(self):
        """Migration pour corriger les tables existantes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Vérifier si learned_patterns a besoin de migration
            cursor.execute("PRAGMA table_info(learned_patterns)")
            columns = cursor.fetchall()
            
            # Recréer la table avec UNIQUE si elle existe mais sans contrainte
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='learned_patterns'")
            if cursor.fetchone():
                # Créer une nouvelle table avec la contrainte UNIQUE
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS learned_patterns_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pattern_type TEXT NOT NULL,
                        pattern_value TEXT NOT NULL UNIQUE,
                        frequency INTEGER DEFAULT 1,
                        success_rate REAL DEFAULT 0.0,
                        last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT
                    )
                ''')
                
                # Copier les données existantes (en ignorant les doublons)
                cursor.execute('''
                    INSERT OR IGNORE INTO learned_patterns_new 
                    (pattern_type, pattern_value, frequency, success_rate, last_used, metadata)
                    SELECT pattern_type, pattern_value, frequency, success_rate, last_used, metadata
                    FROM learned_patterns
                ''')
                
                # Supprimer l'ancienne table et renommer la nouvelle
                cursor.execute('DROP TABLE learned_patterns')
                cursor.execute('ALTER TABLE learned_patterns_new RENAME TO learned_patterns')
                
            conn.commit()
        except Exception as e:
            print(f"Migration: {e}")
        finally:
            conn.close()
    
    def _init_database(self):
        """Initialise la structure de la base de données."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table principale des Questions/Réponses validées
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_validated (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                difficulty TEXT DEFAULT 'intermediaire',
                language TEXT DEFAULT 'fr',
                tags TEXT,
                source_files TEXT,
                source_commit TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usage_count INTEGER DEFAULT 0,
                quality_score REAL DEFAULT 0.0,
                hash_signature TEXT UNIQUE,
                metadata TEXT
            )
        ''')
        
        # Table des Questions/Réponses en attente de validation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_pending (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                difficulty TEXT DEFAULT 'intermediaire',
                language TEXT DEFAULT 'fr',
                tags TEXT,
                source_files TEXT,
                source_commit TEXT,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                generation_run_id TEXT,
                hash_signature TEXT UNIQUE,
                metadata TEXT
            )
        ''')
        
        # Table des patterns appris (pour l'intelligence de la banque)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_value TEXT NOT NULL UNIQUE,
                frequency INTEGER DEFAULT 1,
                success_rate REAL DEFAULT 0.0,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # Table de l'historique des générations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT UNIQUE NOT NULL,
                commit_sha TEXT,
                files_analyzed TEXT,
                questions_generated INTEGER,
                questions_validated INTEGER DEFAULT 0,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                status TEXT DEFAULT 'running',
                metadata TEXT
            )
        ''')
        
        # Table des statistiques globales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stat_date DATE UNIQUE,
                total_validated INTEGER DEFAULT 0,
                total_pending INTEGER DEFAULT 0,
                total_rejected INTEGER DEFAULT 0,
                avg_quality_score REAL DEFAULT 0.0,
                most_common_category TEXT,
                metadata TEXT
            )
        ''')
        
        # Table des concepts clés extraits (pour améliorer les questions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept TEXT UNIQUE NOT NULL,
                definition TEXT,
                related_concepts TEXT,
                source_file TEXT,
                frequency INTEGER DEFAULT 1,
                importance_score REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Index pour améliorer les performances
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_qa_validated_category ON qa_validated(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_qa_validated_language ON qa_validated(language)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_qa_validated_hash ON qa_validated(hash_signature)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_qa_pending_hash ON qa_pending(hash_signature)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_concepts ON key_concepts(concept)')
        
        conn.commit()
        conn.close()
    
    def _generate_hash(self, question: str, answer: str) -> str:
        """Génère une signature hash unique pour détecter les doublons."""
        content = f"{question.lower().strip()}|{answer.lower().strip()}"
        return hashlib.sha256(content.encode()).hexdigest()[:32]
    
    def add_pending_qa(self, 
                       question: str, 
                       answer: str, 
                       category: str,
                       subcategory: str = None,
                       difficulty: str = "intermediaire",
                       language: str = "fr",
                       tags: List[str] = None,
                       source_files: List[str] = None,
                       source_commit: str = None,
                       run_id: str = None,
                       metadata: Dict = None) -> Optional[int]:
        """
        Ajoute une Q&R en attente de validation.
        Retourne l'ID si ajouté, None si doublon détecté.
        """
        hash_sig = self._generate_hash(question, answer)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Vérifier si cette Q&R existe déjà (dans pending ou validated)
        cursor.execute('SELECT id FROM qa_validated WHERE hash_signature = ?', (hash_sig,))
        if cursor.fetchone():
            conn.close()
            return None  # Déjà validée
        
        cursor.execute('SELECT id FROM qa_pending WHERE hash_signature = ?', (hash_sig,))
        if cursor.fetchone():
            conn.close()
            return None  # Déjà en attente
        
        try:
            cursor.execute('''
                INSERT INTO qa_pending 
                (question, answer, category, subcategory, difficulty, language, 
                 tags, source_files, source_commit, generation_run_id, hash_signature, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                question,
                answer,
                category,
                subcategory,
                difficulty,
                language,
                json.dumps(tags) if tags else None,
                json.dumps(source_files) if source_files else None,
                source_commit,
                run_id,
                hash_sig,
                json.dumps(metadata) if metadata else None
            ))
            conn.commit()
            qa_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            qa_id = None
        finally:
            conn.close()
        
        return qa_id
    
    def validate_qa(self, pending_id: int, quality_score: float = 0.8) -> bool:
        """
        Valide une Q&R en attente et la déplace vers la banque validée.
        Met également à jour les patterns appris.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupérer la Q&R en attente
        cursor.execute('SELECT * FROM qa_pending WHERE id = ?', (pending_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False
        
        # Insérer dans validated
        cursor.execute('''
            INSERT INTO qa_validated 
            (question, answer, category, subcategory, difficulty, language,
             tags, source_files, source_commit, quality_score, hash_signature, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row[1], row[2], row[3], row[4], row[5], row[6], 
              row[7], row[8], row[9], quality_score, row[12], row[13]))
        
        # Supprimer de pending
        cursor.execute('DELETE FROM qa_pending WHERE id = ?', (pending_id,))
        
        # Mettre à jour les patterns appris
        self._learn_pattern(cursor, row[3], row[4], True)
        
        conn.commit()
        conn.close()
        return True
    
    def reject_qa(self, pending_id: int) -> bool:
        """Rejette une Q&R en attente."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupérer la catégorie avant suppression pour l'apprentissage
        cursor.execute('SELECT category, subcategory FROM qa_pending WHERE id = ?', (pending_id,))
        row = cursor.fetchone()
        
        if row:
            self._learn_pattern(cursor, row[0], row[1], False)
        
        cursor.execute('DELETE FROM qa_pending WHERE id = ?', (pending_id,))
        conn.commit()
        conn.close()
        return True
    
    def _learn_pattern(self, cursor, category: str, subcategory: str, success: bool):
        """Apprend des patterns de validation pour améliorer les futures générations."""
        pattern_value = f"{category}:{subcategory or 'general'}"
        
        cursor.execute('''
            INSERT INTO learned_patterns (pattern_type, pattern_value, frequency, success_rate)
            VALUES ('category', ?, 1, ?)
            ON CONFLICT(pattern_value) DO UPDATE SET
                frequency = frequency + 1,
                success_rate = (success_rate * (frequency - 1) + ?) / frequency,
                last_used = CURRENT_TIMESTAMP
        ''', (pattern_value, 1.0 if success else 0.0, 1.0 if success else 0.0))
    
    def get_validated_qa(self, 
                         category: str = None, 
                         language: str = "fr",
                         limit: int = 100) -> List[Dict]:
        """Récupère les Q&R validées avec filtres optionnels."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM qa_validated WHERE language = ?'
        params = [language]
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        query += ' ORDER BY quality_score DESC, created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_pending_qa(self, run_id: str = None) -> List[Dict]:
        """Récupère les Q&R en attente de validation."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if run_id:
            cursor.execute('SELECT * FROM qa_pending WHERE generation_run_id = ? ORDER BY generated_at DESC', (run_id,))
        else:
            cursor.execute('SELECT * FROM qa_pending ORDER BY generated_at DESC')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_learned_patterns(self, min_frequency: int = 3) -> List[Dict]:
        """Récupère les patterns appris avec un taux de succès pour guider la génération."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM learned_patterns 
            WHERE frequency >= ? 
            ORDER BY success_rate DESC, frequency DESC
        ''', (min_frequency,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def add_key_concept(self, 
                        concept: str, 
                        definition: str = None,
                        related_concepts: List[str] = None,
                        source_file: str = None) -> bool:
        """Ajoute un concept clé extrait des documents."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO key_concepts (concept, definition, related_concepts, source_file)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(concept) DO UPDATE SET
                    frequency = frequency + 1,
                    definition = COALESCE(?, definition),
                    related_concepts = COALESCE(?, related_concepts)
            ''', (
                concept, 
                definition, 
                json.dumps(related_concepts) if related_concepts else None,
                source_file,
                definition,
                json.dumps(related_concepts) if related_concepts else None
            ))
            conn.commit()
            success = True
        except Exception:
            success = False
        finally:
            conn.close()
        
        return success
    
    def get_key_concepts(self, limit: int = 50) -> List[Dict]:
        """Récupère les concepts clés les plus importants."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM key_concepts 
            ORDER BY importance_score DESC, frequency DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def start_generation_run(self, run_id: str, commit_sha: str, files: List[str]) -> bool:
        """Enregistre le début d'une génération."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO generation_history (run_id, commit_sha, files_analyzed, questions_generated)
                VALUES (?, ?, ?, 0)
            ''', (run_id, commit_sha, json.dumps(files)))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        finally:
            conn.close()
        
        return success
    
    def complete_generation_run(self, run_id: str, questions_count: int, status: str = "completed"):
        """Marque une génération comme terminée."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE generation_history 
            SET questions_generated = ?, completed_at = CURRENT_TIMESTAMP, status = ?
            WHERE run_id = ?
        ''', (questions_count, status, run_id))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self) -> Dict:
        """Retourne les statistiques globales de la banque."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Nombre total de Q&R validées
        cursor.execute('SELECT COUNT(*) FROM qa_validated')
        stats['total_validated'] = cursor.fetchone()[0]
        
        # Nombre de Q&R en attente
        cursor.execute('SELECT COUNT(*) FROM qa_pending')
        stats['total_pending'] = cursor.fetchone()[0]
        
        # Score de qualité moyen
        cursor.execute('SELECT AVG(quality_score) FROM qa_validated')
        stats['avg_quality_score'] = cursor.fetchone()[0] or 0.0
        
        # Répartition par catégorie
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM qa_validated 
            GROUP BY category 
            ORDER BY count DESC
        ''')
        stats['categories'] = dict(cursor.fetchall())
        
        # Concepts clés
        cursor.execute('SELECT COUNT(*) FROM key_concepts')
        stats['total_concepts'] = cursor.fetchone()[0]
        
        # Nombre de générations
        cursor.execute('SELECT COUNT(*) FROM generation_history WHERE status = "completed"')
        stats['total_generations'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def get_context_for_generation(self) -> Dict:
        """
        Retourne le contexte intelligent pour améliorer la génération de questions.
        C'est ici que la banque devient "intelligente".
        """
        context = {
            "validated_examples": [],
            "successful_patterns": [],
            "key_concepts": [],
            "avoid_patterns": []
        }
        
        # Exemples de Q&R validées avec haute qualité
        context["validated_examples"] = self.get_validated_qa(limit=10)
        
        # Patterns qui fonctionnent bien
        patterns = self.get_learned_patterns(min_frequency=2)
        context["successful_patterns"] = [p for p in patterns if p['success_rate'] > 0.7]
        context["avoid_patterns"] = [p for p in patterns if p['success_rate'] < 0.3]
        
        # Concepts clés à utiliser
        context["key_concepts"] = self.get_key_concepts(limit=20)
        
        return context
    
    def export_validated_qa(self, output_path: str, format: str = "json") -> str:
        """Exporte les Q&R validées dans un fichier."""
        qa_list = self.get_validated_qa(limit=10000)
        
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(qa_list, f, ensure_ascii=False, indent=2, default=str)
        elif format == "markdown":
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# Banque de Questions/Réponses - Théorie Mathématique Savard\n\n")
                for qa in qa_list:
                    f.write(f"## Q: {qa['question']}\n\n")
                    f.write(f"**Catégorie:** {qa['category']}\n")
                    f.write(f"**Difficulté:** {qa['difficulty']}\n\n")
                    f.write(f"**Réponse:**\n{qa['answer']}\n\n")
                    f.write("---\n\n")
        
        return output_path


# Fonctions utilitaires pour le workflow GitHub Actions
def init_database(db_path: str = "qa_bank/qa_bank.db") -> QADatabase:
    """Initialise et retourne une instance de la base de données."""
    return QADatabase(db_path)


def bulk_validate(db: QADatabase, ids: List[int], quality_scores: List[float] = None) -> int:
    """Valide plusieurs Q&R en masse."""
    validated = 0
    for i, qa_id in enumerate(ids):
        score = quality_scores[i] if quality_scores and i < len(quality_scores) else 0.8
        if db.validate_qa(qa_id, score):
            validated += 1
    return validated


if __name__ == "__main__":
    # Test de la base de données
    db = QADatabase("qa_bank/qa_bank.db")
    print("Base de données initialisée avec succès!")
    print(f"Statistiques: {db.get_statistics()}")
