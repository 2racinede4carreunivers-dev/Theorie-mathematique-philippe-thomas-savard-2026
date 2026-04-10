#!/usr/bin/env python3
import os
import asyncio
from emergent import LlmChat, UserMessage

SYSTEM = (
    "Tu es un modèle chargé de générer un script narratif structuré pour la théorie "
    "\"L'Univers est au Carré\" de Philippe Thomas Savard. "
    "Tu dois respecter les instructions fournies pour chaque section, "
    "en produisant un texte fluide, cohérent, rigoureux et adapté à une présentation orale."
)

SECTIONS_V2 = [
    {
        "title": "INTRODUCTION - PRESENTATION DE LA THEORIE",
        "instruction": (
            "Redige une introduction narrative (~500 mots) pour la presentation de la theorie "
            "\"L'Univers est au Carre\" de Philippe Thomas Savard.\n\n"
            "L'introduction doit:\n"
            "- Presenter l'auteur: Philippe Thomas Savard, de Levis au Quebec, un libre penseur autodidacte. "
            "Son parcours atypique l'a conduit a developper une theorie mathematique originale par pur interet "
            "personnel pour les nombres.\n"
            "- L'idee premiere et motrice de cette theorie est de denoncer les agissements frauduleux de "
            "l'antinomisme. L'auteur s'oppose fermement a ces individus.\n"
            "- Presenter la theorie comme un travail rigoureux qui propose des methodes originales pour etudier "
            "la distribution des nombres premiers, formalisees et validees en Isabelle/HOL.\n"
            "- Annoncer les 5 chapitres dans l'ordre: 1. Geometrie du spectre des nombres premiers, "
            "2. Mecanique harmonique du chaos discret, 3. Postulat de l'univers est au carre, "
            "4. Espace de Philippot, 5. Teleosemantique et philosophie.\n"
            "- Mentionner que chaque chapitre mathematique contient un fil philosophique qui sera tisse ensemble "
            "au chapitre 5.\n\n"
            "NE DIS PAS \"esprit libre\". NE PRESENTE PAS pi=sqrt(10) comme une revelation."
        ),
    },
    {
        "title": "CHAPITRE 1 - LA GEOMETRIE DU SPECTRE DES NOMBRES PREMIERS",
        "instruction": (
            "Redige le chapitre 1 (~800 mots) sur la geometrie du spectre des nombres premiers.\n\n"
            "Decris les METHODES et leur LOGIQUE DE PROGRESSION, pas les valeurs:\n\n"
            "CHAINE LOGIQUE A SUIVRE:\n"
            "A) L'observation fondatrice: l'auteur remarque que lorsqu'on met en rapport des nombres entiers "
            "successifs, un rapport constant emerge. Ce rapport constant est le point de depart de toute la methode.\n"
            "B) Cette observation conduit a la methode du produit alternatif: l'auteur elabore une methode ou le "
            "produit entre le perimetre d'une figure et le diametre d'une autre figure est toujours egal au produit "
            "inverse. Cette propriete symetrique revele que les surfaces planes encodent des volumes.\n"
            "C) L'analyse numerique metrique: inspiree de la granulometrie (le tamisage du sol), la methode tamise "
            "les nombres a travers deux sequences distinctes. La methode consiste a comparer des figures "
            "geometriques dont les aires maintiennent toujours le meme rapport entre elles.\n"
            "D) La methode de Philippot: une methode iterative basee sur des suites fractionnaires ou chaque terme "
            "est une fraction du precedent. Cette methode est formalisee en Isabelle/HOL. A chaque etape, une "
            "substitution est effectuee a une position precise dans la suite. La position de substitution depend du "
            "nombre de termes.\n"
            "E) La structure spectrale: le rapport entre deux termes consecutifs de la suite est toujours constant. "
            "Ce rapport spectral est valide pour toute longueur finie et conceptuellement pour une infinite de termes.\n"
            "F) AXIOMATISATION FINALE: Quand n>=1 et n<=-1, tous les n ramenent un nombre premier. Tous les n ont une "
            "valeur en consequence avec la quantite de termes dans les suites. Tous les nombres premiers entre eux "
            "respectent un rapport spectral constant. Ce rapport est numeriquement valide mais algebriquement "
            "incoherent. Cette incoherence algebrique reflete l'asymetrie ordonnee: les nombres premiers sont "
            "distribues de maniere chaotique dans l'ensemble des entiers, mais cette distribution chaotique possede "
            "un ordre objectif choisi par l'auteur -- ou le premier nombre premier est le deuxieme nombre entier, et "
            "cette attribution objective ne change pas le rapport que les premiers ont entre eux.\n\n"
            "FIL PHILOSOPHIQUE: L'auteur est un analogiste, un grammairien qui voit la grammaire comme une "
            "mathematique. Son raisonnement est synthetique: la cause connait son effet precedemment."
        ),
    },
    {
        "title": "CHAPITRE 2 - LA MECANIQUE HARMONIQUE DU CHAOS DISCRET",
        "instruction": (
            "Redige le chapitre 2 (~800 mots) sur la mecanique harmonique du chaos discret.\n\n"
            "Decris les METHODES et leur LOGIQUE, sans mentionner les noms des points/segments ni les valeurs "
            "numeriques:\n\n"
            "CHAINE LOGIQUE:\n"
            "A) La figure fondamentale: l'auteur construit une configuration de deux carres emboites avec un "
            "quadrillage fractal et des triangles inscrits. Cette figure est le theatre ou se demontre la mecanique.\n"
            "B) L'invariance geometrique (idee centrale): pour chaque unite admissible de la forme racine de p plus 1, "
            "la configuration encode une relation stable entre les longueurs. La structure de la relation reste "
            "identique quelle que soit la valeur de p. C'est la meme loi pour toutes les unites admissibles.\n"
            "C) La methode des unites: l'auteur demontre par plusieurs exemples que l'unite geometrique obtenue a "
            "partir de la figure coincide toujours avec l'unite abstraite. La forme de la relation est stable et les "
            "valeurs numeriques changent mais la structure relationnelle reste analogue. Les exemples ne sont pas des "
            "cas isoles mais des instances d'une loi universelle.\n"
            "D) Les trois matrices: la methode progresse du concret vers l'abstrait en trois etapes. La premiere "
            "matrice encode les mesures reelles. La deuxieme matrice remplace les mesures par des variables "
            "symboliques -- c'est la structure logique pure. La troisieme matrice normalise completement le systeme "
            "avec des coefficients premiers -- c'est la forme la plus epuree qui revele la structure arithmetique "
            "profonde.\n"
            "E) La formalisation: le fichier Isabelle/HOL formalise l'axiome fondamental -- le rapport entre "
            "demi-base et hauteur est toujours lie a la racine du nombre premier considere. L'unite geometrique "
            "definie par la figure coincide avec l'unite abstraite pour toute unite admissible.\n\n"
            "FIL PHILOSOPHIQUE: La pulsion de vie definie par l'auteur comme \"le fantasme de l'objet qui surpasse la "
            "vie par ses raisons d'etre\". L'invariance geometrique est l'expression mathematique de cette constance."
        ),
    },
    {
        "title": "CHAPITRE 3 - LE POSTULAT DE L'UNIVERS EST AU CARRE",
        "instruction": (
            "Redige le chapitre 3 (~600 mots) sur le postulat de l'univers est au carre.\n\n"
            "Decris la METHODE DU SQUARING sans mentionner les lettres des figures ni les valeurs numeriques:\n\n"
            "CHAINE LOGIQUE:\n"
            "A) Le rectangle initial: l'auteur part d'un rectangle dont les proportions sont liees aux nombres premiers.\n"
            "B) La methode du squaring (en lien avec le nom de la theorie): l'auteur propose que si on effectue le "
            "produit carre du perimetre d'un rectangle, ce rectangle eleve au carre produit une nouvelle figure. "
            "C'est l'acte fondamental de la theorie -- elever un perimetre au rang de nouveau perimetre.\n"
            "C) Le carre maximal inscrit: dans la nouvelle figure, on inscrit un carre maximal. Le rapport entre "
            "l'aire du carre et l'aire du rectangle donne l'unite symbolique de la theorie.\n"
            "D) Le systeme de trois equations: a l'aide de trois equations, l'auteur determine une autre figure -- "
            "elle aussi une figure autre qu'un carre -- mais dont le systeme d'equations permet d'apprecier la valeur "
            "de son perimetre eleve au carre. L'une de ces figures se revele etre un octogone regulier inscrit dans "
            "un cercle.\n"
            "E) L'echelle de mesure: la theorie adopte une echelle de mesure specifique qui harmonise les calculs "
            "entre aires circulaires et volumes. Ce n'est pas une decouverte mais un choix d'echelle qui permet la "
            "coherence du systeme.\n"
            "F) La formalisation: le fichier Isabelle/HOL formalise les rapports de hauteur, de troncature et "
            "l'equation du postulat dans des locales axiomatiques.\n\n"
            "FIL PHILOSOPHIQUE: L'isossophie -- projeter vers l'avenir pour verifier que les valeurs actuelles "
            "restent coherentes. Le squaring est un acte d'isossophie."
        ),
    },
    {
        "title": "CHAPITRE 4 - L'ESPACE DE PHILIPPOT",
        "instruction": (
            "Redige le chapitre 4 (~600 mots) sur l'espace de Philippot.\n\n"
            "Decris la METHODE DE CONSTRUCTION sans valeurs numeriques ni symbologie:\n\n"
            "CHAINE LOGIQUE:\n"
            "A) La spirale de Theodore: l'auteur construit son espace sur la progression de la spirale de Theodore de "
            "Cyrene, une spirale dont chaque longueur successive est la racine du nombre suivant.\n"
            "B) La structure pyramidale: l'espace est represente par une pyramide associee a des disques. Les hauteurs "
            "de la pyramide suivent la progression de la spirale. Les disques ont des rayons proportionnels. Les "
            "points geometriques remarquables correspondent aux nombres premiers.\n"
            "C) Les nombres hypercomplexes geometriques: l'auteur definit une construction analogue aux quaternions "
            "mais fondee sur trois composantes geometriques -- une aire, une aire ponderee selon l'echelle de la "
            "theorie, et une mesure radiale. Ces nombres encodent simultanement plusieurs informations geometriques.\n"
            "D) La correspondance pyramide-ellipsoide: le volume de la pyramide a une certaine hauteur se revele etre "
            "une fraction exacte du volume d'un ellipsoide construit selon les parametres de l'espace. La pyramide "
            "peut donc etre interpretee comme une decomposition plane d'un ellipsoide equivalent.\n"
            "E) L'unification: l'espace unifie la spirale, les disques, les nombres hypercomplexes et les volumes dans "
            "une structure coherente. C'est le pivot de la theorie.\n\n"
            "FIL PHILOSOPHIQUE: L'espace de Philippot est comme une cohomologie geometrique des figures impossibles -- "
            "quand un objet bloque le champ de vision, les methodes mathematiques permettent de deduire ce qui se "
            "trouve derriere. C'est le coeur de l'isossophie."
        ),
    },
    {
        "title": "CHAPITRE 5 - LA TELEOSEMANTIQUE ET LA PHILOSOPHIE",
        "instruction": (
            "Redige le chapitre 5 (~800 mots) sur la teleosemantique et la philosophie de la theorie.\n\n"
            "Ce chapitre est le point culminant. Il doit TISSER ENSEMBLE les fils philosophiques mentionnes dans les "
            "4 chapitres precedents et les approfondir. Il doit aussi aborder les concepts philosophiques propres a "
            "l'auteur.\n\n"
            "CHAINE LOGIQUE DES LIENS:\n"
            "A) L'analogiste: l'auteur se definit comme un grammairien qui voit la grammaire comme une mathematique. "
            "Aristote et Platon etaient des analogistes. L'analogiste intervient quand un savoir-faire devient "
            "trompeur -- il elimine les biais algorithmiques.\n\n"
            "B) LIEN CHAPITRE 1: Le rapport spectral constant est la manifestation mathematique du raisonnement "
            "synthetique -- si toute cause precede son effet, alors la structure precede les valeurs. L'incoherence "
            "algebrique du rapport spectral n'est pas un defaut mais la signature de la distribution chaotique "
            "ordonnee des premiers.\n\n"
            "C) LIEN CHAPITRE 2: L'invariance geometrique est l'expression de la pulsion de vie -- cette constance qui "
            "permet de s'elever au-dessus des circonstances. Les trois matrices montrent la progression du concret "
            "vers l'abstrait, du mesurable vers le pur.\n\n"
            "D) LIEN CHAPITRE 3: Le squaring est un acte d'isossophie. L'isossophie projette vers l'avenir pour "
            "verifier la coherence. Le specialiste isossophique elimine les facons de faire trompeuses et "
            "fallacieuses.\n\n"
            "E) LIEN CHAPITRE 4: La correspondance pyramide-ellipsoide montre que deux formes apparemment differentes "
            "encodent le meme contenu -- c'est l'antidote a l'antinomie qui cherche toujours a selectionner ce qui "
            "annule le fonctionnement.\n\n"
            "F) L'idioschizophrenie: concept defini par l'auteur. La chiralite de la realite, l'asymetrie d'ou "
            "decoulent les comportements toxiques. L'antinomisme pretend avoir le libre esprit mais son agissement "
            "est frauduleux. L'auteur denonce fermement ces individus qui disproportionnent ce qui est connu pour que "
            "cela ne soit plus connu. Le syndrome du medecin specialiste.\n\n"
            "G) Les trois lois du savoir: 1. La conscience (sans conscience, pas de savoir). 2. L'inverse du savoir -- "
            "la comprehension (reconnaitre ne pas savoir est un point fixe). 3. Les figures semblables (comparer les "
            "regles du savoir en formation avec ce qui est deja connu).\n\n"
            "H) Conclusion: la theorie n'est pas seulement mathematique. Elle est une denonciation de l'antinomisme "
            "par les mathematiques. Chaque methode demontre que l'ordre existe dans le chaos, que la structure "
            "precede les valeurs, et que la connaissance est davantage un souvenir qu'une nouveaute."
        ),
    },
]


async def generate_section(section):
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    chat = (
        LlmChat(
            api_key=api_key,
            session_id=f"script-v2-{section['title'][:15]}",
            system_message=SYSTEM,
        )
        .with_model("openai", "gpt-4o")
    )
    return await chat.send_message(UserMessage(text=section["instruction"]))


async def main():
    print("Generation du script narratif V2 - Version pragmatique")
    print("=" * 60)

    all_sections = []

    for i, section in enumerate(SECTIONS_V2):
        print(f"\nSection {i+1}/{len(SECTIONS_V2)}: {section['title']}...")
        try:
            text = await generate_section(section)
            all_sections.append((section["title"], text))
            print(f"  OK ({len(text)} car.)")
        except Exception as e:
            print(f"  ERREUR: {e}")
            all_sections.append((section["title"], f\"[Erreur: {e}]\"))

    lines = []
    lines.append("SCRIPT NARRATIF V2 - VERSION PRAGMATIQUE")
    lines.append("L'UNIVERS EST AU CARRE")
    lines.append("Theorie mathematique de Philippe Thomas Savard")
    lines.append("Presentation video/diaporama - 15 a 18 minutes")
    lines.append("")
    lines.append("=" * 60)

    for title, text in all_sections:
        lines.append("")
        lines.append("-" * 60)
        lines.append(title)
        lines.append("-" * 60)
        lines.append("")
        lines.append(text)
        lines.append("")

    lines.append("=" * 60)
    lines.append("FIN DU SCRIPT")
    lines.append("=" * 60)

    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "SCRIPT_NARRATIF.md",
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    total = sum(len(t.split()) for _, t in all_sections)
    print(f"\nScript V2 sauvegarde: SCRIPT_NARRATIF.md")
    print(f"Total: {total} mots (~{total // 150} min de narration)")


if __name__ == "__main__":
    asyncio.run(main())
