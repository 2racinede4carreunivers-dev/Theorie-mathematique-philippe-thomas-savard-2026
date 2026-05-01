# Politique de sécurité  
Théorie Mathématique Philippe Thomas Savard — 2026

Ce document décrit les règles de sécurité, d’intégrité, de provenance et de protection appliquées au dépôt.  
Il complète les informations du README et reflète l’architecture réelle du projet.

---

# Versions prises en charge

La seule version officiellement supportée est **la version la plus récente** publiée sur la branche `main`.

Les forks, branches personnelles ou versions modifiées par des tiers ne sont **pas** supportées.

| Version | Support |
|--------|---------|
| `main` | ✔ Supportée |
| autres branches | ✖ Non supportées |

---

# Licence et permissions (Apache 2.0)

Ce dépôt est distribué sous la licence **Apache 2.0**.

Les utilisateurs peuvent :
- consulter, cloner et partager le dépôt ;
- modifier le code source et les documents ;
- contribuer via des pull requests ;
- redistribuer des versions modifiées ou non modifiées, tant que les conditions de la licence Apache 2.0 sont respectées.

Le dépôt est fourni « tel quel », sans garantie.

---

# Provenance, intégrité et attestations cryptographiques

Chaque build génère une **empreinte cryptographique SHA‑256** pour tous les documents.

Les attestations SLSA garantissent que les fichiers proviennent **exclusivement** de la branche `main`.

Garanties :
- Attestations automatiques via GitHub Actions  
- Certification SHA‑256 pour `.tex`, `.thy`, `.pdf`  
- Provenance certifiée par SLSA  
- Le dépôt constitue la **source native unique** des documents  

---

# Signalement d’une vulnérabilité

1. Ne pas créer d’issue publique.  
2. Contacter : **philippethomassavard@gmail.com**  
3. Inclure description, fichiers concernés, étapes de reproduction.

---

# Responsabilité et garanties

- dépôt fourni « tel quel »  
- aucune garantie  
- contributeurs responsables de leurs modifications  
- seule `main` est valide et authentifiée  

---

# Règles de protection appliquées à la branche `main`

Ces règles sont **actives** et s’appliquent à :
- `~DEFAULT_BRANCH`
- `refs/heads/main`

## 1. Protection contre les actions dangereuses

| Règle | Description |
|-------|-------------|
| deletion | La branche ne peut pas être supprimée. |
| non_fast_forward | Push forcé interdit. |
| update | Mises à jour directes contrôlées. |
| creation | Création régulée. |
| required_linear_history | Historique linéaire obligatoire. |

---

## 2. Exigences pour les Pull Requests

| Paramètre | Valeur |
|-----------|--------|
| Approbations requises | 1 |
| Revue par propriétaires du code | ✔ Oui |
| Approbation du dernier push | ✖ Non |
| Résolution des discussions | ✖ Non |
| Méthode de fusion autorisée | Rebase uniquement |
| Revue Copilot | PR brouillon uniquement |

---

## 3. Revue automatique Copilot

- review_on_push : false  
- review_draft_pull_requests : true  

---

## 4. Contournements (bypass)

| Acteur | Type | Mode |
|--------|------|------|
| ID 5 | RepositoryRole | always |

Seul l’administrateur peut contourner les règles.

---

# Workflows automatisés

Les workflows automatisés actifs sont :

- **Quotidien (10h UTC)** : 3 Q&R auto‑générées et auto‑validées  
- **Hebdomadaire (vendredi 14h UTC)** : Propositions `.tex` / `.thy`  
- **Mensuel (1er du mois 9h UTC)** : Rapport de maintenance  

Ces workflows participent à :
- la stabilité du dépôt  
- la cohérence documentaire  
- la mise à jour continue de la banque Q&R  
- la surveillance de l’intégrité des fichiers  

---

# Résumé final

- Historique linéaire obligatoire  
- Fusion par rebase uniquement  
- 1 approbation requise  
- Revue obligatoire par propriétaires du code  
- Pas de suppression, pas de force‑push  
- Copilot analyse les PR brouillon  
- Seul l’admin peut bypass  
- Règles appliquées à `main`  
- Attestations SLSA et SHA‑256  
- Workflows automatisés actifs (quotidien, hebdo, mensuel)  
