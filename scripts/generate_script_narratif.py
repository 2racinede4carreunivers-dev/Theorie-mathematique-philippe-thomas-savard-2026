#!/usr/bin/env python3
"""
Generateur du script narratif pour la presentation de la theorie
L'Univers est au Carre - Philippe Thomas Savard
"""

import asyncio
import sys
import os

sys.path.insert(0, str(os.path.dirname(os.path.abspath(__file__))))

from emergentintegrations.llm.chat import LlmChat, UserMessage


SECTIONS = [
    {
        "title": "INTRODUCTION",
        "instruction": """Redige une introduction narrative de 2-3 pages (~600 mots) pour une presentation video/diaporama de 15-18 minutes sur la theorie mathematique "L'Univers est au Carre" de Philippe Thomas Savard.

L'introduction doit:
1. Presenter l'auteur: Philippe Thomas Savard, ouvrier de Levis (Chaudiere-Appalaches, Quebec, Canada), autodidacte sans formation academique en mathematiques, qui a developpe cette theorie par pur plaisir intellectuel.
2. Raconter brievement son parcours: seul etudiant a reussir l'examen du ministere en math 536 au secondaire 5 sans avoir recu la bonne matiere; a aussi reussi un examen truque au cegep en genie civil.
3. Presenter la theorie: "L'Univers est au Carre" est une theorie mathematique originale qui unifie geometrie, nombres premiers, mecanique discrete et philosophie dans un cadre coherent. La convention fondamentale pi = sqrt(10) harmonise les calculs.
4. Annoncer les 5 chapitres:
   - Chapitre 1: La geometrie du spectre des nombres premiers
   - Chapitre 2: La mecanique harmonique du chaos discret
   - Chapitre 3: Le postulat de l'univers est au carre
   - Chapitre 4: L'espace de Philippot
   - Chapitre 5: La teleosemantique de l'esprit d'un analogiste
5. Mentionner que tout est valide formellement en Isabelle/HOL.

Ton narratif: pedagogique, accessible, comme un documentaire scientifique. En francais."""
    },
    {
        "title": "CHAPITRE 1 - LA GEOMETRIE DU SPECTRE DES NOMBRES PREMIERS",
        "instruction": """Redige le chapitre 1 du script narratif (~800 mots) sur "La geometrie du spectre des nombres premiers".

Contenu a couvrir (tire du fichier geometry_prime_spectrum.tex):
1. L'observation fondatrice: entre deux entiers consecutifs il y a toujours au moins 1 unite. L'auteur jeune ajoutait 1 aux nombres pairs (1+50=51, 1+100=101...) et trouvait toujours le rapport 1/2.
2. Le produit alternatif du tesseract: deux carres (1x1 et 1.5x1.5), le produit entre perimetre A x diametre B = diametre A x perimetre B. Le produit symetrique donne sqrt(72), l'asymetrique revele un volume de cube.
3. L'analyse numerique metrique: inspiree de la granulometrie - on tamise les nombres comme on tamise le sol. Les sequences A et B, les trapezoides ABCD/CDEF/EFGH dont les aires gardent le rapport constant 1/2.
4. La methode de Philippot: suites fractionnaires (1/2, 1/4, 1/8...) formalisees en Isabelle/HOL (methode_de_philippot.thy), chaque marche est exactement la moitie de la precedente.
5. Le Digamma: dans le systeme grec, Zeta vaut 7 mais occupe la 6e position a cause du Digamma - une valeur qui ne correspond pas a sa position, comme la substitution dans la sequence B.

LIEN PHILOSOPHIQUE a mentionner: L'auteur se definit comme un "analogiste" - un grammairien qui voit la grammaire comme une mathematique. Sa methode est intuitive et synthetique: "si toute cause precede temporellement son effet, alors la cause connait son effet precedemment."

Ton: narratif pedagogique, comme un documentaire."""
    },
    {
        "title": "CHAPITRE 2 - LA MECANIQUE HARMONIQUE DU CHAOS DISCRET",
        "instruction": """Redige le chapitre 2 du script narratif (~800 mots) sur "La mecanique harmonique du chaos discret".

Contenu a couvrir (tire de mecanique_harmonique_du_chaos_discret.tex):
1. La figure fondamentale: deux carres emboites ABCD (cote 2.25) et AEFG (cote 1.5) avec quadrillage fractal a 3 niveaux, deux triangles equilateraux inscrits (jaune et vert), et les diametres AC et AF.
2. L'invariance geometrique: pour chaque unite admissible u(p) = sqrt(p) + 1, la configuration encode une relation stable entre les longueurs. C'est l'idee centrale.
3. Les trois exemples d'unites:
   - Unite sqrt(2)+1: produit alternatif avec segments AL, JK, BE. L'unite geometrique est obtenue via arcsin(AL/2) = 26.06 degres, puis sqrt(4.5)*0.5/sin(angle) = sqrt(2)+1.
   - Unite sqrt(3)+1: meme structure mais angle = 22.84 degres.
   - Unite sqrt(5)+1: angle = 19.13 degres. Structure d'invariance persiste.
4. Les trois matrices:
   - M1 (mesures du plan): longueurs reelles du cardan sans blocage
   - M2 (transition): variables symboliques, structure logique pure
   - M3 (derivee premiere): coefficients = nombres premiers (37,31,29...), ponderations 7/k, unique inconnue u=sqrt(3.375)
5. Le cardan sans blocage: reference a la figure de reference qui illustre la mecanique.
6. Formalisation Isabelle/HOL: le fichier mecanique_discret.thy definit base_length, height_length, ratio_halfbase_height. L'axiome ratio_axiom formalise que le rapport est toujours sqrt(p).

LIEN PHILOSOPHIQUE: La "pulsion de vie" definie par l'auteur comme "le fantasme de l'objet qui surpasse la vie par ses raisons d'etre". L'invariance geometrique est l'expression mathematique de cette constance qui permet toujours de s'elever au-dessus des circonstances.

Ton: narratif pedagogique."""
    },
    {
        "title": "CHAPITRE 3 - LE POSTULAT DE L'UNIVERS EST AU CARRE",
        "instruction": """Redige le chapitre 3 du script narratif (~600 mots) sur "Le postulat de l'univers est au carre" (postulat du squaring).

Contenu a couvrir (tire de postulat_de_univers_carre.tex):
1. Le rectangle initial ABCD: cotes AB=CD=sqrt(2)-1, AD=BC=1, perimetre = sqrt(8).
2. L'elevation au carre (squaring): on eleve le perimetre au carre: (sqrt(8))^2 = 8. Le rectangle transforme A'B'C'D' a des cotes A'B'=4-sqrt(8) et A'D'=sqrt(8). Verification: 2(4-sqrt(8))+2*sqrt(8) = 8.
3. Le carre maximal inscrit: A'B'EF, aire = (4-sqrt(8))^2 = 1.372583002. Aire du rectangle = sqrt(128)-8. Le rapport des aires = sqrt(2)+1, qui devient l'unite symbolique.
4. Les trois diagonales fondamentales:
   - Diag(A'B'EF) = sqrt(32)-4
   - Diag(EFC'D') = 2(sqrt(1/3)+sqrt(1/6))^(-1)
   - Diag(A'B'C'D') = 3.061467459 = perimetre d'un octogone regulier inscrit dans un disque de diametre 1
5. La revelation: 3.061467459 = pi dans ce cadre geometrique, donc sqrt(10) = pi.
6. Les trois equations de l'octogone carre: trois equations encadrees qui relient les diagonales, les aires et sqrt(8).
7. Formalisation Isabelle/HOL: postulat_carre.thy avec les locales postulat_carre, rectangle_carre, polygone_carre_axiomes, et l'exemple numerique pour p=3.

LIEN PHILOSOPHIQUE: Le postulat du squaring est l'acte fondamental de la theorie - comme l'analogiste qui eleve la grammaire au rang de mathematique, le squaring eleve un perimetre au rang de nouveau perimetre. L'isossophie: projeter vers l'avenir pour verifier si les valeurs actuelles restent coherentes.

Ton: narratif pedagogique."""
    },
    {
        "title": "CHAPITRE 4 - L'ESPACE DE PHILIPPOT",
        "instruction": """Redige le chapitre 4 du script narratif (~600 mots) sur "L'espace de Philippot".

Contenu a couvrir (tire de espace_de_philippot.tex):
1. Introduction: L'espace de Philippot est le coeur conceptuel du 4e chapitre. C'est un espace geometrique represente par une structure pyramidale associee a des disques, construit selon la progression de la spirale de Theodore de Cyrene (sqrt(1), sqrt(2), sqrt(3)...).
2. Structure geometrique: 
   - Disques superieurs avec rayons r_n = sqrt(0.1*n)
   - Hauteurs de la pyramide = sqrt(1), sqrt(2), sqrt(3), sqrt(4)...
   - Points geometriques H.2, H.3, H.5, H.7, H.11, H.13, H.17, H.19 (les nombres premiers!)
   - Convention fondamentale: pi = sqrt(10)
3. Nombres hypercomplexes geometriques: pas les quaternions classiques mais une construction analogue: H = (A, A*sqrt(10), r^2)^(1/2). Encode simultanement aire, aire ponderee et mesure radiale.
4. Aires des quatre faces a la hauteur sqrt(2): face avant, droite, arriere, gauche. Somme = 6.064911064 = 4.8 + 2*A_disque.
5. Volume de la pyramide: V = 1.6(sqrt(2)+sqrt(0.2))/3 = 0.9927611508. Ce volume = 1/10 du volume d'un ellipsoide. La pyramide est une decomposition plane d'un ellipsoide equivalentt.
6. Conclusion: unifie spirale de Theodore, disques racinaires, nombres hypercomplexes et volumes dans une structure coherente.

LIEN PHILOSOPHIQUE: L'espace de Philippot est comme une "cohomologie geometrique des figures impossibles" - un objet bloque le champ de vision, mais par des methodes mathematiques on peut deduire ce qui se trouve derriere. C'est le coeur de l'isossophie.

Ton: narratif pedagogique."""
    },
    {
        "title": "CHAPITRE 5 - LA TELEOSEMANTIQUE ET LA PHILOSOPHIE DE LA THEORIE",
        "instruction": """Redige le chapitre 5 du script narratif (~800 mots) sur "La teleosemantique de l'esprit d'un analogiste et la philosophie de la theorie".

Ce chapitre doit etre le point culminant qui relie tous les fils philosophiques mentionnes dans les 4 chapitres precedents.

Contenu a couvrir (tire de teleosemantique_philosophie_esprit_analogiste.tex et pilosophy_geometry_of_prime_number.tex):

1. L'analogiste: un grammairien qui voit la grammaire comme une mathematique. Aristote et Platon etaient des analogistes. Aucune universite au Quebec n'enseigne cette discipline. L'auteur est devenu analogiste en faisant des mathematiques personnelles depuis l'enfance.

2. Esprit geometrique vs esprit de finesse: L'esprit geometrique demande des preuves, l'esprit de finesse (la pulsion de vie) est "le fantasme de l'objet qui surpasse la vie par ses raisons d'etre". LIEN: Dans le chapitre 1, les rapports 1/2 sont la manifestation geometrique de cette finesse - une constante qui traverse toute la theorie.

3. L'isossophie: "iso" = mesure egale + "sophie" = sagesse. Le specialiste qui elimine les facons de faire trompeuses. LIEN: Dans le chapitre 3, le squaring est un acte d'isossophie - on projette le perimetre vers l'avenir (au carre) pour verifier que les relations restent coherentes.

4. Le raisonnement synthetique: "si toute cause precede temporellement son effet, alors la cause connait son effet precedemment." LIEN: Dans le chapitre 2, l'invariance geometrique u(p)=sqrt(p)+1 est un raisonnement synthetique - la structure precede les valeurs numeriques.

5. L'idioschizophrenie: concept defini par l'auteur - la chiralite de la realite, l'asymetrie d'ou decoulent les comportements toxiques. LIEN: Dans le chapitre 4, l'espace de Philippot avec sa correspondance pyramide-ellipsoide montre que deux formes apparemment differentes peuvent encoder le meme volume - c'est l'antidote a l'antinomie.

6. La connaissance selon Savard: 3 lois inspirees de Newton. La connaissance est plus un souvenir qu'une nouveaute, elle se sent comme un chiasme. LIEN: toute la theorie est une redecouverte de structures deja presentes dans la nature des nombres.

7. Conclusion: la theorie n'est pas seulement mathematique, elle est une vision du monde ou la geometrie, les nombres premiers et la philosophie s'unifient. Pi = sqrt(10) n'est pas une approximation, c'est une convention qui revele des harmonies cachees.

Ton: plus personnel et philosophique que les chapitres precedents, tout en restant rigoureux."""
    }
]


async def generate_section(section, session_base):
    """Genere une section du script narratif."""
    api_key = os.environ.get("EMERGENT_LLM_KEY")

    chat = LlmChat(
        api_key=api_key,
        session_id=f"{session_base}-{section['title'][:20]}",
        system_message="""Tu es un scenariste et narrateur scientifique specialise dans les documentaires mathematiques.
Tu rediges le script narratif d'une presentation video/diaporama de 15-18 minutes sur une theorie mathematique originale.
Le texte doit etre:
- En francais
- Pedagogique et accessible, mais sans simplifier les mathematiques
- Ecrit comme un texte de narration (voix off d'un documentaire)
- Fluide, captivant, avec des transitions naturelles
- Fidele au contenu mathematique source
- Les formules importantes doivent etre mentionnees textuellement (ex: "racine carree de 10 egale pi")
Ne mets PAS de balises markdown. Ecris du texte pur narratif avec seulement des retours a la ligne entre les paragraphes."""
    ).with_model("openai", "gpt-4o")

    response = await chat.send_message(UserMessage(text=section['instruction']))
    return response


async def main():
    print("Generation du script narratif - L'Univers est au Carre")
    print("=" * 60)

    all_sections = []

    for i, section in enumerate(SECTIONS):
        print(f"\nGeneration section {i+1}/6: {section['title']}...")
        try:
            text = await generate_section(section, "script-narratif")
            all_sections.append((section['title'], text))
            print(f"  OK ({len(text)} caracteres)")
        except Exception as e:
            print(f"  ERREUR: {e}")
            all_sections.append((section['title'], f"[Erreur de generation: {e}]"))

    # Assembler le script final
    print("\nAssemblage du script final...")

    script_lines = []
    script_lines.append("SCRIPT NARRATIF")
    script_lines.append("L'UNIVERS EST AU CARRE")
    script_lines.append("Theorie mathematique de Philippe Thomas Savard")
    script_lines.append("Presentation video/diaporama - 15 a 18 minutes")
    script_lines.append("")
    script_lines.append("=" * 60)
    script_lines.append("")

    for title, text in all_sections:
        script_lines.append("")
        script_lines.append("-" * 60)
        script_lines.append(title)
        script_lines.append("-" * 60)
        script_lines.append("")
        script_lines.append(text)
        script_lines.append("")

    script_lines.append("")
    script_lines.append("=" * 60)
    script_lines.append("FIN DU SCRIPT")
    script_lines.append("=" * 60)

    # Sauvegarder
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SCRIPT_NARRATIF.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(script_lines))

    print(f"\nScript sauvegarde: {output_path}")
    total_words = sum(len(text.split()) for _, text in all_sections)
    print(f"Total: {total_words} mots (~{total_words // 150} minutes de narration)")


if __name__ == "__main__":
    asyncio.run(main())
