#!/usr/bin/env python3
"""
Module optionnel d'intégration Wolfram Alpha pour enrichir les réponses mathématiques.

Wolfram Alpha offre une API gratuite limitée (2000 requêtes/mois) qui peut:
- Vérifier les calculs mathématiques
- Fournir des visualisations
- Enrichir les réponses avec des définitions précises

IMPORTANT: Cette intégration est OPTIONNELLE.
Pour l'activer, vous devez:
1. Créer un compte sur https://developer.wolframalpha.com/
2. Obtenir une clé API gratuite (App ID)
3. Ajouter la clé dans les secrets GitHub: WOLFRAM_APP_ID

Usage:
    from qa_wolfram import WolframEnricher
    enricher = WolframEnricher(api_key)
    result = await enricher.verify_equation("E = mc^2")
"""

import os
import urllib.parse
import urllib.request
import json
import xml.etree.ElementTree as ET
from typing import Optional, Dict, List


class WolframEnricher:
    """
    Enrichisseur de contenu mathématique via Wolfram Alpha API.
    
    Fonctionnalités:
    - Vérification d'équations
    - Simplification d'expressions
    - Définitions mathématiques
    - Calculs et évaluations
    """
    
    BASE_URL = "http://api.wolframalpha.com/v2/query"
    
    def __init__(self, app_id: str = None):
        """
        Initialise l'enrichisseur Wolfram.
        
        Args:
            app_id: Clé API Wolfram Alpha (App ID)
        """
        self.app_id = app_id or os.environ.get("WOLFRAM_APP_ID")
        self.enabled = bool(self.app_id)
        
        if not self.enabled:
            print("⚠️  Wolfram Alpha non configuré (WOLFRAM_APP_ID manquant)")
            print("    Le système fonctionnera sans enrichissement Wolfram.")
    
    def is_available(self) -> bool:
        """Vérifie si l'API Wolfram est disponible."""
        return self.enabled
    
    def query(self, input_text: str, output_format: str = "plaintext") -> Optional[Dict]:
        """
        Envoie une requête à Wolfram Alpha.
        
        Args:
            input_text: Expression ou question mathématique
            output_format: Format de sortie (plaintext, image, mathml)
        
        Returns:
            Dictionnaire avec les résultats ou None si erreur
        """
        if not self.enabled:
            return None
        
        try:
            # Construire l'URL de requête
            params = {
                "appid": self.app_id,
                "input": input_text,
                "format": output_format,
                "output": "json"
            }
            
            url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"
            
            # Envoyer la requête
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            return self._parse_response(data)
            
        except Exception as e:
            print(f"Erreur Wolfram Alpha: {e}")
            return None
    
    def _parse_response(self, data: Dict) -> Dict:
        """Parse la réponse JSON de Wolfram Alpha."""
        result = {
            "success": data.get("queryresult", {}).get("success", False),
            "pods": [],
            "primary_result": None
        }
        
        queryresult = data.get("queryresult", {})
        pods = queryresult.get("pods", [])
        
        for pod in pods:
            pod_data = {
                "title": pod.get("title", ""),
                "scanner": pod.get("scanner", ""),
                "subpods": []
            }
            
            for subpod in pod.get("subpods", []):
                pod_data["subpods"].append({
                    "title": subpod.get("title", ""),
                    "plaintext": subpod.get("plaintext", ""),
                    "img": subpod.get("img", {}).get("src", "")
                })
            
            result["pods"].append(pod_data)
            
            # Identifier le résultat principal
            if pod.get("primary", False):
                result["primary_result"] = pod_data
        
        return result
    
    def verify_equation(self, equation: str) -> Dict:
        """
        Vérifie une équation mathématique.
        
        Args:
            equation: Équation à vérifier (ex: "x^2 + y^2 = r^2")
        
        Returns:
            Dictionnaire avec le résultat de la vérification
        """
        result = self.query(f"verify {equation}")
        
        return {
            "valid": result is not None and result.get("success", False),
            "details": result
        }
    
    def simplify_expression(self, expression: str) -> Optional[str]:
        """
        Simplifie une expression mathématique.
        
        Args:
            expression: Expression à simplifier
        
        Returns:
            Expression simplifiée ou None
        """
        result = self.query(f"simplify {expression}")
        
        if result and result.get("primary_result"):
            subpods = result["primary_result"].get("subpods", [])
            if subpods:
                return subpods[0].get("plaintext")
        
        return None
    
    def get_definition(self, term: str) -> Optional[str]:
        """
        Obtient la définition mathématique d'un terme.
        
        Args:
            term: Terme mathématique (ex: "determinant", "eigenvalue")
        
        Returns:
            Définition ou None
        """
        result = self.query(f"definition of {term}")
        
        if result and result.get("pods"):
            for pod in result["pods"]:
                if "definition" in pod["title"].lower():
                    subpods = pod.get("subpods", [])
                    if subpods:
                        return subpods[0].get("plaintext")
        
        return None
    
    def evaluate(self, expression: str) -> Optional[str]:
        """
        Évalue une expression mathématique.
        
        Args:
            expression: Expression à évaluer
        
        Returns:
            Résultat de l'évaluation ou None
        """
        result = self.query(expression)
        
        if result and result.get("primary_result"):
            subpods = result["primary_result"].get("subpods", [])
            if subpods:
                return subpods[0].get("plaintext")
        
        return None
    
    def get_properties(self, mathematical_object: str) -> List[str]:
        """
        Obtient les propriétés d'un objet mathématique.
        
        Args:
            mathematical_object: Objet mathématique (ex: "circle", "matrix")
        
        Returns:
            Liste des propriétés
        """
        result = self.query(f"properties of {mathematical_object}")
        properties = []
        
        if result and result.get("pods"):
            for pod in result["pods"]:
                for subpod in pod.get("subpods", []):
                    text = subpod.get("plaintext", "")
                    if text:
                        properties.append(text)
        
        return properties


class WolframAnswerEnricher:
    """
    Enrichit les réponses générées avec des informations Wolfram Alpha.
    S'intègre avec le système de génération Q&R principal.
    """
    
    def __init__(self, wolfram_enricher: WolframEnricher):
        self.wolfram = wolfram_enricher
    
    def enrich_answer(self, answer: str, question: str) -> str:
        """
        Enrichit une réponse avec des informations Wolfram.
        
        Args:
            answer: Réponse originale générée par l'IA
            question: Question associée
        
        Returns:
            Réponse enrichie
        """
        if not self.wolfram.is_available():
            return answer
        
        # Détecter les expressions mathématiques dans la réponse
        import re
        
        # Pattern pour les expressions entre $ ou \[ \]
        math_patterns = [
            r'\$([^$]+)\$',           # $expression$
            r'\\\[([^\]]+)\\\]',      # \[expression\]
            r'\\\(([^\)]+)\\\)',      # \(expression\)
        ]
        
        enrichments = []
        
        for pattern in math_patterns:
            matches = re.findall(pattern, answer)
            for expr in matches[:3]:  # Limiter à 3 enrichissements
                simplified = self.wolfram.simplify_expression(expr)
                if simplified and simplified != expr:
                    enrichments.append(f"Note Wolfram: '{expr}' se simplifie en '{simplified}'")
        
        if enrichments:
            answer += "\n\n---\n**Enrichissements Wolfram Alpha:**\n"
            answer += "\n".join(f"- {e}" for e in enrichments)
        
        return answer
    
    def verify_mathematical_claims(self, answer: str) -> Dict:
        """
        Vérifie les affirmations mathématiques dans une réponse.
        
        Returns:
            Dictionnaire avec les vérifications
        """
        if not self.wolfram.is_available():
            return {"verified": False, "reason": "Wolfram non disponible"}
        
        import re
        
        # Chercher les équations
        equations = re.findall(r'([a-zA-Z0-9\s\+\-\*\/\^\=\(\)]+\s*=\s*[a-zA-Z0-9\s\+\-\*\/\^\(\)]+)', answer)
        
        verifications = []
        for eq in equations[:5]:  # Limiter
            result = self.wolfram.verify_equation(eq.strip())
            verifications.append({
                "equation": eq.strip(),
                "valid": result.get("valid", False)
            })
        
        return {
            "verified": len(verifications) > 0,
            "verifications": verifications
        }


# Configuration pour l'intégration avec le système principal
WOLFRAM_CONFIG = {
    "enabled": False,  # Mettre True pour activer
    "max_requests_per_run": 10,  # Limite pour ne pas épuiser le quota
    "enrich_answers": True,
    "verify_equations": True
}


def create_wolfram_enricher() -> Optional[WolframEnricher]:
    """
    Factory pour créer un enrichisseur Wolfram si configuré.
    """
    app_id = os.environ.get("WOLFRAM_APP_ID")
    
    if app_id and WOLFRAM_CONFIG["enabled"]:
        return WolframEnricher(app_id)
    
    return None


if __name__ == "__main__":
    # Test de l'intégration Wolfram
    print("Test de l'intégration Wolfram Alpha")
    print("=" * 40)
    
    enricher = WolframEnricher()
    
    if enricher.is_available():
        print("✅ Wolfram Alpha disponible")
        
        # Test de simplification
        result = enricher.simplify_expression("(x+1)^2")
        print(f"Simplification de (x+1)^2: {result}")
        
        # Test de définition
        definition = enricher.get_definition("determinant")
        print(f"Définition de 'determinant': {definition}")
    else:
        print("❌ Wolfram Alpha non configuré")
        print("   Pour l'activer:")
        print("   1. Obtenez une clé API sur https://developer.wolframalpha.com/")
        print("   2. Définissez WOLFRAM_APP_ID dans vos secrets GitHub")
