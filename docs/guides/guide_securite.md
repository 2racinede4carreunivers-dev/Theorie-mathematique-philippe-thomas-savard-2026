#  Guide de sécurité du dépôt — *L’univers est au carré*

Ce document présente les règles, procédures et bonnes pratiques de sécurité liées à l’utilisation, la reproduction et la contribution au dépôt *L’univers est au carré*.  
Il s’adresse à tous les utilisateurs, chercheurs, développeurs et contributeurs souhaitant interagir avec le projet de manière responsable et sécurisée.

---

##  1. Principes généraux de sécurité

Le dépôt est conçu pour être :
- **ouvert**,  
- **reproductible**,  
- **transparent**,  
- **scientifiquement rigoureux**.

Cependant, comme tout projet open‑source, il peut contenir :
- des erreurs,  
- des vulnérabilités potentielles,  
- des incohérences dans les scripts ou workflows,  
- des fichiers sensibles par inadvertance.

Les utilisateurs sont encouragés à :
- signaler toute anomalie,  
- éviter de diffuser publiquement une faille avant qu’elle ne soit corrigée,  
- contribuer à l’amélioration continue du projet.

---

##  2. Signaler un problème de sécurité

Si vous détectez une erreur, une vulnérabilité ou un comportement pouvant mettre en péril :
- l’intégrité du dépôt,  
- la reproductibilité scientifique,  
- la sécurité des workflows,  
- ou la confidentialité de données accidentellement exposées,

veuillez contacter immédiatement le mainteneur du projet :

📧 **philippethomassavard@gmail.com**

### ⏱ Délais de réponse  
Le mainteneur s’engage à fournir un **retour dans les plus brefs délais**, selon la gravité du problème signalé.

###  Confidentialité  
Les signalements de sécurité doivent être effectués **en privé**, afin d’éviter toute exploitation malveillante avant la mise en place d’un correctif.

---

##  3. Utilisation sécurisée du dépôt

Pour utiliser le dépôt de manière sécurisée, il est recommandé de :

###  Bonnes pratiques
- Cloner le dépôt dans un environnement isolé si vous exécutez des scripts.  
- Vérifier les fichiers exécutables (`.sh`, `.ps1`, `.py`, etc.) avant de les lancer.  
- Examiner les workflows GitHub Actions avant d’activer des actions dans un fork.  
- Ne jamais exécuter un script sans en comprendre la fonction.  
- Maintenir vos outils (Git, LaTeX, Cosign, etc.) à jour.

###  Points d’attention
- Les workflows automatisés peuvent télécharger des dépendances externes.  
- Les fichiers générés automatiquement ne doivent pas être modifiés manuellement.  
- Les signatures cryptographiques (Cosign) doivent être vérifiées avant utilisation.

---

##  4. Garantie et limitations

Le code du dépôt est fourni sous licence **Apache 2.0**, ce qui implique :

###  Ce que vous pouvez faire
- utiliser le code librement,  
- l’étudier,  
- le modifier,  
- le redistribuer,  
- l’intégrer dans d’autres projets.

###  Ce que vous devez respecter
- conserver les avis de copyright,  
- inclure une copie de la licence,  
- mentionner les modifications apportées,  
- ne pas utiliser les marques associées sans autorisation.

###  Clause de non‑garantie
Le dépôt est fourni **« tel quel »**, sans aucune garantie, explicite ou implicite.  
Cela signifie notamment que :

- aucune garantie n’est donnée quant à l’exactitude scientifique,  
- aucune garantie n’est donnée quant à la sécurité absolue du code,  
- aucune responsabilité ne peut être engagée en cas de dommages résultant de son utilisation.

---

##  5. Responsabilité des contributeurs

En contribuant au dépôt, vous acceptez de :

- respecter les règles de sécurité décrites ici,  
- ne pas introduire volontairement de vulnérabilité,  
- tester vos modifications avant de soumettre une Pull Request,  
- documenter tout changement ayant un impact sur la sécurité,  
- signaler immédiatement toute faille découverte, même si vous en êtes l’auteur involontaire.

---

## 6. Vérification des artefacts et signatures

Le projet utilise des mécanismes de traçabilité et de signature (ex. : **Cosign**) pour garantir l’intégrité des artefacts.

Les utilisateurs sont encouragés à :

- vérifier les signatures avant d’utiliser un artefact,  
- ne jamais exécuter un fichier non signé ou altéré,  
- signaler toute incohérence dans les métadonnées ou attestations.

---

##  7. Contact et support

Pour toute question liée à la sécurité, à la reproductibilité ou à l’intégrité du dépôt :

**philippethomassavard@gmail.com**

Le mainteneur répondra **dans les délais les plus courts possibles**, selon la disponibilité et la nature du problème.

---

Merci de contribuer à la sécurité, la stabilité et la pérennité du projet *L’univers est au carré*.
