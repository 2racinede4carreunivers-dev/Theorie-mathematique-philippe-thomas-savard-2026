theory mecanique_discret
  imports Complex_Main
begin

text "
-------------------------------------------------------------------------------
                     TABLE DES MATIERES - L'UNIVERS EST AU CARRE
-------------------------------------------------------------------------------

CHAPITRE A - AXIOMATISATION DE LA MECANIQUE HARMONIQUE DU CHAOS DISCRET
  A1.0 Fondements geometriques
    A1.1 Unites admissibles : u(p) = sqrt(p) + 1
    A1.2 Carres emboites et structure d'echelle 1.5^n
    A1.3 Triangles inscrits et base parametrique b(n,p)
    A1.4 Rapport fondamental demi-base / hauteur = sqrt(p)
    A1.5 Angle associe theta(p) = arctan(sqrt(p))
    A1.6 Unite geometrique via le segment AL_nat
    A1.7 Axiome d'invariance geometrique

  A2.0 Invariance et dynamique interne
    A2.1 Dependence des longueurs a l'unite
    A2.2 Deplacement des segments dans la figure
    A2.3 Invariance du produit alternatif
    A2.4 Diametre equivalent LM
    A2.5 Interpretation relationnelle (analogie relativiste)

CHAPITRE B - CARDAN SANS BLOCAGE ET MATRICE A DERIVE PREMIERE
  B1.0 Cardan sans blocage
    B1.1 Definition polaire et points du cardan
    B1.2 Longueurs fondamentales (BD, DE, EF, CG, etc.)
    B1.3 Angles structurants (60, 75, 45)
    B1.4 Construction geometrique complete

  B2.0 Matrice a derive premiere
    B2.1 Definition des coefficients C1 ... C9
    B2.2 Sommes de lignes R1, R2, R3
    B2.3 Matrice M1 (mesures du plan)
    B2.4 Matrice de transition M2
    B2.5 Structure trigonometrique interne
    B2.6 Interpretation mecanique

CHAPITRE C - PRISME MATRICIEL A DERIVEE PREMIERE
  C1.0 Definition du prisme matriciel
    C1.1 Structure tridimensionnelle
    C1.2 Relations entre les trois plans
    C1.3 Interpretation geometrique du prisme

  C2.0 Proprietes du prisme
    C2.1 Equilibre matriciel
    C2.2 Invariance par changement d'unite
    C2.3 Role de l'inconnue unique u = sqrt(3.375)

-------------------------------------------------------------------------------
"

subsection "A1.0 Axiomatisation de la mecanique harmonique du chaos discret"

text "
  La configuration geometrique fondamentale repose sur une famille de carres
  emboites, tous alignes avec les axes du plan cartesien et partageant le point
  commun A = (0,0). Le carre de niveau n possede un cote de longueur 1.5^n,
  ce qui correspond exactement aux elevations visibles dans la figure TikZ :

      1.5^1, 1.5^2, 1.5^3, 1.5^4, ..., 1.5^n.

  Dans chaque carre de niveau n est inscrit un triangle isocele dont le sommet
  superieur est le point C(n) = (1.5^n, 1.5^n), et dont la base repose sur les
  axes de coordonnees. La base est constituee des deux points :

      P1(n,p) = (b(n,p), 0)
      P2(n,p) = (0, b(n,p))

  ou b(n,p) est une longueur strictement positive dependant du niveau n et du
  nombre premier p.

  Lorsque la diagonale AC(n) coupe la base du triangle inscrit, celui-ci est
  divise en deux triangles rectangles. Dans chacun de ces triangles rectangles,
  la demi-base vaut b(n,p)/2 et la hauteur vaut h(n,p). Le rapport geometrique
  fondamental de la mecanique harmonique du chaos discret est :

      (b(n,p) / 2) / h(n,p) = sqrt(p)

  ou p est un nombre premier definissant l'unite admissible.

  Ce rapport ne concerne donc pas le triangle complet, mais le demi-triangle
  rectangle issu de la coupure par la diagonale AC(n). Ce point est essentiel :
  c'est ce demi-triangle rectangle qui porte l'information geometrique
  fondamentale de l'unite p.

  Le rapport ci-dessus determine l'angle theta(p) du triangle rectangle par :

      tan(theta(p)) = sqrt(p)
      theta(p) = arctan(sqrt(p))

  Cet angle joue un role central dans les chapitres B et C, notamment dans la
  matrice a derive premiere et dans la structure du prisme matriciel.
"

subsubsection "A1.1 Unites admissibles"

definition prime_nat :: "nat \<Rightarrow> bool" where
  "prime_nat p \<longleftrightarrow> (p > 1 \<and> (\<forall>m. m dvd p --> m = 1 \<or> m = p))"

definition admissible_unit :: "nat \<Rightarrow> bool" where
  "admissible_unit p \<longleftrightarrow> prime_nat p"

definition unit :: "nat => real" where
  "unit p = sqrt (real p) + 1"

subsubsection "A1.2 Carres emboites"

type_synonym point = "real \<times> real"

definition side :: "nat => real" where
  "side n = (1.5 :: real) ^ n"

definition A :: point where "A = (0,0)"
definition B :: "nat \<Rightarrow> point" where "B n = (side n, 0)"
definition C :: "nat \<Rightarrow> point" where "C n = (side n, side n)"
definition D :: "nat \<Rightarrow> point" where "D n = (0, side n)"

subsubsection "A1.3 Triangles inscrits"

text "
  Le triangle inscrit dans le carre de niveau n et associe a l'unite p possede
  les sommets :

      C(n), P1(n,p), P2(n,p)

  ou la base repose sur les axes et le sommet est C(n).
"

definition base_param :: "nat => nat=> real" where
  "base_param n p = (side n) / (sqrt (real p) + 0.5)"

definition P1 :: "nat => nat => point" where
  "P1 n p = (base_param n p, 0)"

definition P2 :: "nat => nat => point" where
  "P2 n p = (0, base_param n p)"

subsubsection "A1.4 Rapport fondamental : demi-base / hauteur = sqrt(p)"

definition dist2 :: "point => point => real" where
  "dist2 P Q = sqrt ((fst P - fst Q)^2 + (snd P - snd Q)^2)"

definition base_length :: "nat => nat => real" where
  "base_length n p = dist2 (P1 n p) (P2 n p)"

definition height_length :: "nat => nat => real" where
  "height_length n p =
     abs ((2 * side n - base_param n p) / sqrt 2)"

definition ratio_halfbase_height :: "nat => nat => real" where
  "ratio_halfbase_height n p =
     ((base_length n p) / 2) / (height_length n p)"

axiomatization where
  ratio_axiom:
    "\<lbrakk> admissible_unit p; n \<ge> 1 \<rbrakk>
     \<Longrightarrow> ratio_halfbase_height n p = sqrt (real p)"

subsubsection "A1.5 Angle associe a l'unite p"

definition angle_rect :: "nat \<Rightarrow> real" where
  "angle_rect p = arctan (sqrt (real p))"


subsection "B2.0 Angle oppose dans le demi-triangle rectangle"

(* 
  Lorsque la diagonale AC coupe la base du triangle inscrit, celui-ci est divise
  en deux triangles rectangles. Dans chacun de ces triangles rectangles, la
  demi-base vaut b/2 et la hauteur vaut h. Le rapport geometrique fondamental est :

      (b / 2) / h = sqrt(p)

  L'angle oppose a la demi-base est donc :

      theta(p) = arctan(sqrt(p))

  Cette fonction joue un role central dans la matrice a derive premiere.
*)


subsection "B2.1 Angle oppose pour la matrice a derive premiere"

(*
  Nous reutilisons la fonction angle_rect definie dans le Chapitre A.
  Elle encode l'angle du demi-triangle rectangle associe a l'unite p.
*)

lemma angle_rect_prime:
  assumes "prime_nat p"
  shows "angle_rect p = arctan (sqrt (real p))"
  by (simp add: angle_rect_def)


subsubsection "A1.6 Unite geometrique via le segment AL_nat"

text "
  On definit le segment AL_nat(p) de maniere a ce que l'unite geometrique :

      U(p) = sqrt 4.5 / AL_nat(p)

  soit egale a l'unite abstraite sqrt(p) + 1.

  On obtient :

      AL_nat(p) = sqrt 4.5 / (sqrt p + 1).
"

definition AL_nat :: "nat => real" where
  "AL_nat p = sqrt 4.5 / (sqrt (real p) + 1)"

definition geometric_unit :: "nat => real" where
  "geometric_unit p = sqrt 4.5 / AL_nat p"


lemma geometric_unit_eq_unit:
  assumes "AL_nat p \<noteq> 0"
  shows "geometric_unit p = sqrt (real p) + 1"
proof -
  have "geometric_unit p = sqrt 4.5 / AL_nat p"
    by (simp add: geometric_unit_def)
  also have "... = sqrt 4.5 / (sqrt 4.5 / (sqrt (real p) + 1))"
    by (simp add: AL_nat_def)
  also have "... = sqrt (real p) + 1"
    using assms by (simp add: field_simps)
  finally show ?thesis .
qed


axiomatization where
  AL_nat_domain:
    "admissible_unit p ==> AL_nat p \<noteq> 0"


subsubsection "A1.6 Axiome d'invariance (version demontree)"

text "
  Pour toute unite admissible p, l'unite geometrique definie par AL_nat(p)
  coincide avec l'unite abstraite sqrt(p) + 1.
"

(* Definition correcte de l'unite abstraite *)
definition u_nat :: "nat \<Rightarrow> real" where
  "u_nat p = sqrt (real p) + 1"

lemma invariance_geometric_unit:
  assumes "admissible_unit p"
  shows "geometric_unit p = u_nat p"
proof -
  have "AL_nat p \<noteq> 0"
    using assms AL_nat_domain by blast
  hence "geometric_unit p = sqrt (real p) + 1"
    using geometric_unit_eq_unit by blast
  thus ?thesis
    by (simp add: u_nat_def)
qed


subsection "B1.0 Cardan sans blocage (formalise)"

definition pol :: "real => real => point" where
  "pol r \<theta> = (r * cos \<theta>, r * sin \<theta>)"

definition ang_BDE :: real where "ang_BDE = (pi / 3)"     (* 60 deg *)
definition ang_CGF :: real where "ang_CGF = (5*pi / 12)"  (* 75 deg *)
definition ang_BAC :: real where "ang_BAC = (pi / 4)"     (* 45 deg *)

definition BD_len :: real where "BD_len = sqrt (1/3)"
definition DE_len :: real where "DE_len = sqrt (1/12)"
definition BC_len :: real where "BC_len = 0.5"
definition EF_len :: real where "EF_len = 0.5"
definition FG_len :: real where "FG_len = 1 / (sqrt (12 :: real) + 4)"
definition CG_len :: real where "CG_len = 1 / (sqrt (3 :: real) + 2)"
definition AB_len :: real where "AB_len = 1 / (sqrt (12 :: real) - 2)"
definition AC_len :: real where "AC_len = sqrt (1.5 :: real) / 2"
definition DG_len :: real where "DG_len = 1.26"
definition AG_len :: real where "AG_len = 1.13"

definition card_D :: point where "card_D = (0,0)"
definition card_G :: point where "card_G = pol DG_len 0"
definition card_A :: point where "card_A = pol AG_len ang_BDE"
definition card_B :: point where "card_B = pol BD_len ang_BDE"
definition card_E :: point where "card_E = pol DE_len (ang_BDE + ang_BDE)"
definition card_C :: point where "card_C = pol AC_len (ang_BDE - ang_BAC)"
definition card_F :: point where "card_F = pol EF_len (ang_BDE - ang_BAC + (pi/2))"
definition card_G2 :: point where "card_G2 = pol CG_len (ang_BDE - ang_BAC - ang_CGF)"


chapter C
section "C1.0 Matrice a derive premiere"

text "
  Formalisation de la matrice a derive premiere associee au cardan sans blocage.
"

type_synonym length = real

record cardan_lengths =
  AD      :: length
  AB      :: length
  BD      :: length
  AG      :: length
  AC      :: length
  CG      :: length
  DG      :: length
  EF      :: length
  DE      :: length
  FG      :: length
  diam_eq :: real
  u15     :: real
  u3375   :: real

definition C1 :: "cardan_lengths => length" where "C1 L = AD L"
definition C2 :: "cardan_lengths => length" where "C2 L = AB L"
definition C3 :: "cardan_lengths => length" where "C3 L = BD L"
definition C4 :: "cardan_lengths => length" where "C4 L = AG L"
definition C5 :: "cardan_lengths => length" where "C5 L = AC L"
definition C6 :: "cardan_lengths => length" where "C6 L = CG L"
definition C7 :: "cardan_lengths => length" where "C7 L = DG L"
definition C8 :: "cardan_lengths => length" where "C8 L = EF L"
definition C9 :: "cardan_lengths => length" where "C9 L = DE L + FG L"

definition R1 :: "cardan_lengths => length" where
  "R1 L = C1 L + C2 L + C3 L"

definition R2 :: "cardan_lengths => length" where
  "R2 L = C4 L + C5 L + C6 L"

definition R3 :: "cardan_lengths => length" where
  "R3 L = C7 L + C8 L + C9 L"


subsection "1. Matrice deduite des mesures du plan"

definition M1_L1 :: "cardan_lengths => bool" where
  "M1_L1 L \<longleftrightarrow>
     C1 L * diam_eq L + C2 L * diam_eq L + C3 L * diam_eq L
       = 2 * C1 L * diam_eq L"

definition M1_L2 :: "cardan_lengths => bool" where
  "M1_L2 L \<longleftrightarrow>
     C4 L * u15 L + C5 L * u15 L + C6 L * u15 L
       = 2 * C4 L * u15 L"

definition M1_L3 :: "cardan_lengths => bool" where
  "M1_L3 L \<longleftrightarrow>
     C7 L * u3375 L + C8 L * u3375 L + C9 L * u3375 L
       = 2 * C7 L * u3375 L"

definition M1_matrix :: "cardan_lengths => bool" where
  "M1_matrix L \<longleftrightarrow> M1_L1 L \<and> M1_L2 L \<and> M1_L3 L"


subsection "2. Matrice de transition"

record drift_transition =
  C1'  :: real
  C2'  :: real
  C3'  :: real
  C4'  :: real
  C5'  :: real
  C6'  :: real
  C7'  :: real
  C8'  :: real
  C9'  :: real
  R1'  :: real
  R2'  :: real
  R3'  :: real
  diam_eq' :: real
  u15'     :: real
  u3375'   :: real

text "
  Structure de la matrice de transition :

    C1' + C2' + C3' = R1'
    C4' + C5' + C6' = R2'
    C7' + C8' + C9' = R3'

    R1' = 2 * C1' * diam_eq'
    R2' = 2 * C3' * u15'
    R3' = 2 * C6' * u3375'
"

definition M2_structure :: "drift_transition => bool" where
  "M2_structure T \<longleftrightarrow>
     C1' T + C2' T + C3' T = R1' T \<and>
     C4' T + C5' T + C6' T = R2' T \<and>
     C7' T + C8' T + C9' T = R3' T \<and>
     R1' T = 2 * C1' T * diam_eq' T \<and>
     R2' T = 2 * C3' T * u15' T \<and>
     R3' T = 2 * C6' T * u3375' T"


subsection "3. Matrice a derive premiere simplifiee"

text "
  Matrice simplifiee (nombres premiers) :

    L1 : 37x + 31x + 29x = 41x
    L2 : 19y + 17y + 13y = 23y
    L3 :  7z +  5z +  3z = 11z

  Version ponderee avec l'inconnue unique u = sqrt 3.375 :

    L1 : 37 (7/48.5) u + 31 (7/48.5) u + 29 (7/48.5) u = 41 (7/20.5) u
    L2 : 19 (7/24.5) u + 17 (7/24.5) u + 13 (7/24.5) u = 23 (7/11.5) u
    L3 :  7 (7/7.5)  u +  5 (7/7.5)  u +  3 (7/7.5)  u = 11 (7/5.5)  u
"

definition u :: real where
  "u = sqrt (3.375 :: real)"

definition L1_simplified :: "real \<Rightarrow> bool" where
  "L1_simplified x \<longleftrightarrow> 37*x + 31*x + 29*x = 41*x"

definition L2_simplified :: "real \<Rightarrow> bool" where
  "L2_simplified y \<longleftrightarrow> 19*y + 17*y + 13*y = 23*y"

definition L3_simplified :: "real \<Rightarrow> bool" where
  "L3_simplified z \<longleftrightarrow> 7*z + 5*z + 3*z = 11*z"

definition L1_weighted :: bool where
  "L1_weighted \<longleftrightarrow>
     37 * (7/48.5) * u +
     31 * (7/48.5) * u +
     29 * (7/48.5) * u =
     41 * (7/20.5) * u"

definition L2_weighted :: bool where
  "L2_weighted \<longleftrightarrow>
     19 * (7/24.5) * u +
     17 * (7/24.5) * u +
     13 * (7/24.5) * u =
     23 * (7/11.5) * u"

definition L3_weighted :: bool where
  "L3_weighted \<longleftrightarrow>
     7 * (7/7.5) * u +
     5 * (7/7.5) * u +
     3 * (7/7.5) * u =
     11 * (7/5.5) * u"

subsection "D1.0 Generalisation du facteur trigonometrique alternatif"

text
  "Definitions et lemmes liant l'expression trigonometrique `alt_factor` au
   rapport geometrique hauteur/demi-base = 1 / sqrt p. On introduit aussi la
   notion de diametre equivalent au carre."

definition inv_ratio_height_halfbase :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "inv_ratio_height_halfbase n p = 1 / ratio_halfbase_height n p"

lemma inv_ratio_height_halfbase_simpl:
  fixes n :: nat
  assumes "admissible_unit p" "n \<ge> 1"
  shows "inv_ratio_height_halfbase n p = 1 / sqrt (real p)"
  using ratio_axiom[OF assms]
  unfolding inv_ratio_height_halfbase_def
  by simp

definition alt_factor :: "nat \<Rightarrow> real" where
  "alt_factor p =
     sqrt (4 * real p) *
     (sin (arcsin (((1 / 2) / ((sqrt (real p) + 1) / sqrt 18)) * (1 / 2)))) ^ 2"

text
  "Axiome liant la quantite trigonometrique `alt_factor` et l'invariant geometrique.
   L'annotation de type sur n garantit l'instanciation correcte dans les lemmes."
axiomatization where
  alt_factor_axiom:
    "\<lbrakk> admissible_unit p; prime_nat p; (n :: nat) \<ge> 1 \<rbrakk>
     \<Longrightarrow> alt_factor p = inv_ratio_height_halfbase n p"

lemma alt_factor_for_primes:
  fixes n :: nat
  assumes "admissible_unit p" "prime_nat p" "n \<ge> 1"
  shows "alt_factor p = 1 / sqrt (real p)"
proof -
  from alt_factor_axiom[OF \<open>admissible_unit p\<close> \<open>prime_nat p\<close> \<open>n \<ge> 1\<close>]
  have eq1: "alt_factor p = inv_ratio_height_halfbase n p" .
  from inv_ratio_height_halfbase_simpl[OF \<open>admissible_unit p\<close> \<open>n \<ge> 1\<close>]
  have eq2: "inv_ratio_height_halfbase n p = 1 / sqrt (real p)" .
  from eq1 eq2 show ?thesis by simp
qed

definition diam_equiv_sq :: "nat \<Rightarrow> real" where
  "diam_equiv_sq p = alt_factor p"

lemma diam_equiv_sq_for_primes:
  fixes n :: nat
  assumes "admissible_unit p" "prime_nat p" "n \<ge> 1"
  shows "diam_equiv_sq p = 1 / sqrt (real p)"
  using alt_factor_for_primes[OF \<open>admissible_unit p\<close> \<open>prime_nat p\<close> \<open>n \<ge> 1\<close>]
  unfolding diam_equiv_sq_def
  by simp

lemma alt_factor_explicit_for_primes:
  fixes n :: nat
  assumes "admissible_unit p" "prime_nat p" "n \<ge> 1"
  shows
    "sqrt (4 * real p) *
       (sin (arcsin (((1 / 2) / ((sqrt (real p) + 1) / sqrt 18)) * (1 / 2)))) ^ 2
     = 1 / sqrt (real p)"
  using alt_factor_for_primes[OF \<open>admissible_unit p\<close> \<open>prime_nat p\<close> \<open>n \<ge> 1\<close>]
  unfolding alt_factor_def
  by simp

text "            
-------------------------------------------------------------------------------
                           CREDITS ET LICENCE
-------------------------------------------------------------------------------

Titre  : Mecanique harmonique du chaos discret
Auteur : Philippe Thomas Savard
Date   : 10 mars 2026
Lieu   : Levis, Chaudieres-Appalaches, Canada

Ce travail est distribue sous la licence Apache 2.0.

-------------------------------------------------------------------------------
LICENCE APACHE 2.0 (TEXTE COMPLET)
-------------------------------------------------------------------------------

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.

   \"License\" shall mean the terms and conditions for use, reproduction,
   and distribution as defined by Sections 1 through 9 of this document.

   \"Licensor\" shall mean the copyright owner or entity authorized by
   the copyright owner that is granting the License.

   \"Legal Entity\" shall mean the union of the acting entity and all
   other entities that control, are controlled by, or are under common
   control with that entity. For the purposes of this definition,
   \"control\" means (i) the power, direct or indirect, to cause the
   direction or management of such entity, whether by contract or
   otherwise, or (ii) ownership of fifty percent (50%) or more of the
   outstanding shares, or (iii) beneficial ownership of such entity.

   \"You\" (or \"Your\") shall mean an individual or Legal Entity
   exercising permissions granted by this License.

   \"Source\" form shall mean the preferred form for making modifications,
   including but not limited to software source code, documentation source,
   and configuration files.

   \"Object\" form shall mean any form resulting from mechanical
   transformation or translation of a Source form, including but not
   limited to compiled object code, generated documentation, and
   conversions to other media types.

   \"Work\" shall mean the work of authorship, whether in Source or
   Object form, made available under the License, as indicated by a
   copyright notice that is included in or attached to the work.

   \"Derivative Works\" shall mean any work, whether in Source or Object
   form, that is based on (or derived from) the Work and for which the
   editorial revisions, annotations, elaborations, or other modifications
   represent, as a whole, an original work of authorship. For the purposes
   of this License, Derivative Works shall not include works that remain
   separable from, or merely link (or bind by name) to the interfaces of,
   the Work and Derivative Works thereof.

   \"Contribution\" shall mean any work of authorship, including the
   original version of the Work and any modifications or additions to
   that Work or Derivative Works thereof, that is intentionally submitted
   to Licensor for inclusion in the Work by the copyright owner or by an
   individual or Legal Entity authorized to submit on behalf of the
   copyright owner.

   \"Contributor\" shall mean Licensor and any individual or Legal Entity
   on behalf of whom a Contribution has been received by Licensor and
   subsequently incorporated within the Work.

2. Grant of Copyright License.

   Subject to the terms and conditions of this License, each Contributor
   hereby grants to You a perpetual, worldwide, non-exclusive, no-charge,
   royalty-free, irrevocable copyright license to reproduce, prepare
   Derivative Works of, publicly display, publicly perform, sublicense,
   and distribute the Work and such Derivative Works in Source or Object
   form.

3. Grant of Patent License.

   Subject to the terms and conditions of this License, each Contributor
   hereby grants to You a perpetual, worldwide, non-exclusive, no-charge,
   royalty-free, irrevocable (except as stated in this section) patent
   license to make, have made, use, offer to sell, sell, import, and
   otherwise transfer the Work.

4. Redistribution.

   You may reproduce and distribute copies of the Work or Derivative
   Works thereof in any medium, with or without modifications, and in
   Source or Object form, provided that You meet the following conditions:

   (a) You must give any other recipients of the Work a copy of this
       License; and

   (b) You must cause any modified files to carry prominent notices
       stating that You changed the files; and

   (c) You must retain, in the Source form of any Derivative Works that
       You distribute, all copyright, patent, trademark, and attribution
       notices from the Source form of the Work.

5. Submission of Contributions.

   Unless You explicitly state otherwise, any Contribution intentionally
   submitted for inclusion in the Work shall be under the terms and
   conditions of this License.

6. Trademarks.

   This License does not grant permission to use the trade names,
   trademarks, service marks, or product names of the Licensor.

7. Disclaimer of Warranty.

   Unless required by applicable law or agreed to in writing, Licensor
   provides the Work (and each Contributor provides its Contributions)
   on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.

8. Limitation of Liability.

   In no event and under no legal theory shall any Contributor be liable
   to You for damages, including any direct, indirect, special,
   incidental, or consequential damages.

9. Accepting Warranty or Additional Liability.

   While redistributing the Work, You may choose to offer support or
   warranty protection for a fee, but You must do so on Your own behalf.

END OF TERMS AND CONDITIONS

-------------------------------------------------------------------------------
"
end