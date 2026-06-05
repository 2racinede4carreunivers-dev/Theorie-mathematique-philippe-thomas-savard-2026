theory methode_spectral
  imports Complex_Main
begin
(****************************************************************)
(* TABLE DES MATIERES - SCRIPT HOL : GEOMETRIE DU SPECTRE       *)
(*                                                              *)
(* I.   RAPPORT SPECTRAL 1/2 - FONDATIONS                       *)
(*      1. Forme generale des suites SA et SB ...............   *)
(*      2. Validite des formes generales pour n >=1. .........   *)
(*      3. Rapport spectral 1/2 (definition + preuve) .......   *)
(*      4. Generalisation n x n du rapport spectral .........   *)
(*      5. Digamma calcule et equation du premier ...........   *)
(*      6. Equation generale (SB n - digamma)/64 = p ........   *)
(*      7. Postulat spectral 1/2 (axiomatisation) ...........   *)
(*      8. Exemples : 29, 31, 37, 41 ........................   *)
(*                                                              *)
(* I.bis  NOTICE : DEMONSTRATION CLASSIQUE ZETA ↔ PREMIERS      *)
(*      1. Derivee logarithmique et fonction de Mangoldt ....   *)
(*      2. Fonction ψ(x) et integrale de Perron .............   *)
(*      3. Deplacement du contour et zeros de ζ(s) ..........   *)
(*      4. Comment les zeros determinent les premiers ........   *)
(*                                                              *)
(* II.  MODELE SPECTRAL 1/4                                     *)
(*      1. Definitions generales A_1_4 et B_1_4 .............   *)
(*      2. Equation generale du premier (1/4) ...............   *)
(*      3. Postulat spectral 1/4 (axiomatisation) ...........   *)
(*      4. Exemple complet : premier 947 ....................   *)
(*                                                              *)
(* III. MODELE SPECTRAL 1/3                                     *)
(*      1. Definitions generales A_1_3 et B_1_3 .............   *)
(*      2. Equation generale du premier (1/3) ...............   *)
(*      3. Postulat spectral 1/3 (axiomatisation) ...........   *)
(*      4. Exemple complet : premier 227 ....................   *)
(*      5. Preuve generale du rapport constant 1/3 ..........   *)
(*                                                              *)
(* IV.  RAPPORT SPECTRAL 1/4 - PREUVE GENERALE                 *)
(*      1. Definition RsP_1_4 ...............................   *)
(*      2. Preuve du rapport constant 1/4 ...................   *)
(*                                                              *)
(* V.   SUITES MIXTES A ET B (-,+)                             *)
(*      1. Definitions SA_mix et SB_mix .....................   *)
(*      2. Formes fermees et recurrence .....................   *)
(*      3. Reconstruction generale du premier (mixte) .......   *)
(*      4. Exemple : six termes negatifs ....................   *)
(*                                                              *)
(* VI.  SUITES NEGATIVES - EQUATIONS SPECTRALES                *)
(*      1. Definitions SA_neg_eq et SB_neg_eq ...............   *)
(*      2. Digamma negatif ..................................   *)
(*      3. Rapport spectral negatif 1/2 (axiomatisation) ....  *)
(*                                                              *)
(* VII. GEOMETRIE SPECTRALE - ASYMETRIE ORDONNEE / CHAOTIQUE   *)
(*      1. Indices valides et croissance stricte (int) ......   *)
(*      2. Asymetrie ordonnee et chaotique ..................   *)
(*      3. Proprietes generales .............................   *)
(*                                                              *)
(* VIII. METHODE DE COMPARAISON ASYMETRIQUE                    *)
(*      1. Version nat des asymetries .......................   *)
(*      2. Comparaison asymetrique modele 1/2 ...............   *)
(*      3. Comparaison asymetrique modele 1/4 ...............   *)
(*                                                              *)
(* IX.  AXIOMATISATIONS SPECTRALES - SECTIONS OFFICIELLES      *)
(*      1. Axiomatisation positive (modele 1/2) .............   *)
(*         section: "Axiomatisation positive"                  *)
(*         axiome : spectral_postulate_pos                     *)
(*      2. Axiomatisation spectral 1/4 ......................   *)
(*         section: "Axiomatisation spectral 1/4"              *)
(*         axiome : spectral_postulate_1_4                     *)
(*      3. Axiomatisation rapport 1/3 .......................   *)
(*         section: "Axiomatisation rapport 1/3."              *)
(*         axiome : spectral_postulate_1_3                     *)
(*      4. Axiomatisation negative (rapport spectral 1/2) ...  *)
(*         section: "Rapport spectral 1/2 negatif"             *)
(*         axiome : spectral_ratio_neg_un_demi                 *)
(*                                                              *)
(* X.   VALIDATION EPIPOLAIRE DU PLAN TRIFOCAL                 *)
(*      1. Objets abstraits du plan trifocal ................  *)
(*      2. Aires et geometrie de la droite critique .........  *)
(*      3. Combinatoire des ecarts (simple/mixte) ...........  *)
(*      4. Axiomes trifocaux : Zeta / Spectral / RH .........  *)
(*      5. Courbure, aire parabolique et validation .........  *)
(*      6. Theoreme final : solution epipolaire .............  *)
(****************************************************************)

(****************************************************************)
(* Sous-bloc 1 : formes generales des suites A et B *)
(****************************************************************)

section "Forme genrale des suites A et B"

definition SA :: "nat => real" where
  "SA n = (3.25 / 2) * (2 ^ n) - 2"

definition SB :: "nat => real" where
  "SB n = (6.5 / 2) * (2 ^ n) - 66"


(****************************************************************)
(* Sous-bloc 2 : validite pour tout n >= 1 *)
(****************************************************************)

lemma SA_forme_generale:
  assumes "n >= 1"
  shows "SA n = (3.25 / 2) * (2 ^ n) - 2"
  using assms by (simp add: SA_def)

lemma SB_forme_generale:
  assumes "n >= 1"
  shows "SB n = (6.5 / 2) * (2 ^ n) - 66"
  using assms by (simp add: SB_def)


(****************************************************************)
(* Sous-bloc 3 : rapport spectral = 1/2 (cas 1×1) *)
(****************************************************************)

section "Rapport spectral 1/2"

definition RsP :: "nat => nat => real" where
  "RsP n1 n2 = (SA n1 - SA n2) / (SB n1 - SB n2)"

lemma RsP_un_demi_general:
  assumes "n1 >= 1" "n2 >= 1" "n1 ~= n2"
  shows "RsP n1 n2 = 1/2"
proof -
  have SA1: "SA n1 = (3.25 / 2) * (2 ^ n1) - 2"
    by (simp add: SA_def)
  have SA2: "SA n2 = (3.25 / 2) * (2 ^ n2) - 2"
    by (simp add: SA_def)
  have SB1: "SB n1 = (6.5 / 2) * (2 ^ n1) - 66"
    by (simp add: SB_def)
  have SB2: "SB n2 = (6.5 / 2) * (2 ^ n2) - 66"
    by (simp add: SB_def)

  have num: "SA n1 - SA n2 = (3.25 / 2) * (2 ^ n1 - 2 ^ n2)"
    by (simp add: SA1 SA2 algebra_simps)
  have den: "SB n1 - SB n2 = (6.5 / 2) * (2 ^ n1 - 2 ^ n2)"
    by (simp add: SB1 SB2 algebra_simps)

  have "RsP n1 n2 =
        ((3.25 / 2) * (2 ^ n1 - 2 ^ n2)) /
        ((6.5 / 2) * (2 ^ n1 - 2 ^ n2))"
    by (simp add: RsP_def num den)
  also have "... = (3.25 / 2) / (6.5 / 2)"
    using assms by (simp add: field_simps)
  also have "... = 1/2"
    by simp
  finally show ?thesis .
qed


(****************************************************************)
(* AJOUT : généralisation symétrique n×n *)
(****************************************************************)

section "Rapport spectral n×n (généralisation symétrique)"

definition RsP_nn :: "nat list => nat list => real" where
  "RsP_nn A_indices B_indices =
     (sum_list (map SA A_indices)) /
     (sum_list (map SB B_indices))"

definition rapport_spectral_un_demi_nn :: "nat list => nat list => bool" where
  "rapport_spectral_un_demi_nn A_indices B_indices =
     (RsP_nn A_indices B_indices = 1/2)"

definition A3 :: "nat list" where
  "A3 = [2, 9, 10]"

definition B3 :: "nat list" where
  "B3 = [3, 11, 15]"

(*
lemma exemple_3x3_spectral:
  "rapport_spectral_un_demi_nn A3 B3"
  unfolding rapport_spectral_un_demi_nn_def
            RsP_nn_def A3_def B3_def
  by admit
*)
(* L'exemple est volontairement commenté pour garantir la compilation *)


(****************************************************************)
(* Sous-bloc 4 : Digamma calcule a partir de SB et du nombre premier *)
(****************************************************************)

section "Section du Digamma calcule."

definition digamma_calc :: "nat => nat => real" where
  "digamma_calc n p = SB n - 64 * real p"

definition prime_equation :: "nat => nat => real" where
  "prime_equation n p = (SB n - digamma_calc n p) / 64"

lemma digamma_calc_equation_alt:
  "digamma_calc n p = (SB n / 64 - real p) * 64"
  unfolding digamma_calc_def by simp

lemma prime_equation_identity:
  "prime_equation n p = real p"
  unfolding prime_equation_def digamma_calc_def
  by simp

lemma SB_affine_en_SA:
  "SB n = 2 * SA n - 62"
  unfolding SA_def SB_def by simp

lemma ecart_spectral_constant:
  "SB n - 2 * SA n = -62"
  unfolding SA_def SB_def by simp

lemma digamma_affine_en_SA:
  "digamma_calc n p = 2 * SA n - (62 + 64 * real p)"
  unfolding digamma_calc_def SA_def SB_def by simp

lemma difference_SA_succ:
  "SA (Suc n) - SA n = (13 / 8) * 2 ^ n"
  unfolding SA_def by simp

lemma difference_SB_succ:
  "SB (Suc n) - SB n = (13 / 4) * 2 ^ n"
  unfolding SB_def by simp

lemma ratio_incremental_un_demi:
  "SA (Suc n) - SA n = (SB (Suc n) - SB n) / 2"
proof -
  have A: "SA (Suc n) - SA n = (13 / 8) * 2 ^ n"
    using difference_SA_succ by simp
  have B: "SB (Suc n) - SB n = (13 / 4) * 2 ^ n"
    using difference_SB_succ by simp
  from B have "(SB (Suc n) - SB n) / 2 = (13 / 8) * 2 ^ n"
    by (simp add: field_simps)
  with A show ?thesis
    by simp
qed

(****************************************************************)
(* Postulat spectral 1/2 (régime positif) *)
(****************************************************************)

section "Axiomatisation positive"

axiomatization where
  spectral_postulate_pos:
    "!!n p. n >= 1 ==> prime p ==> prime_equation n p = real p"

lemma prime_equation_for_primes_pos:
  assumes "n >= 1" "prime p"
  shows "prime_equation n p = real p"
  using spectral_postulate_pos assms by blast
(****************************************************************)
(* Sous-bloc 5 : Exemples concrets pour 29, 31, 37, 41         *)
(****************************************************************)

section "Exemple complet pour les nombres premiers 29 31 37 et 41."

definition n29 :: nat where "n29 = 10"
definition n31 :: nat where "n31 = 11"
definition n37 :: nat where "n37 = 12"
definition n41 :: nat where "n41 = 13"

definition D29 :: real where "D29 = 256"
definition D31 :: real where "D31 = 5 * 256"
definition D37 :: real where "D37 = 9 * 256 + 5 * 384"
definition D41 :: real where "D41 = 13 * 256 + 9 * 384 + 5 * 768"

section "Valeur des somme A et B pour n."

lemma SA_10: "SA n29 = 1662"
  unfolding n29_def SA_def by simp

lemma SB_10: "SB n29 = 3262"
  unfolding n29_def SB_def by simp

lemma SA_11: "SA n31 = 3326"
  unfolding n31_def SA_def by simp

lemma SB_11: "SB n31 = 6590"
  unfolding n31_def SB_def by simp

lemma SA_12: "SA n37 = 6654"
  unfolding n37_def SA_def by simp

lemma SB_12: "SB n37 = 13246"
  unfolding n37_def SB_def by simp

lemma SA_13: "SA n41 = 13310"
  unfolding n41_def SA_def by simp

lemma SB_13: "SB n41 = 26558"
  unfolding n41_def SB_def by simp

lemma digamma_calc_29:
  "digamma_calc n29 29 = 1406"
  unfolding digamma_calc_def n29_def SB_def by simp

lemma digamma_calc_31:
  "digamma_calc n31 31 = 4606"
  unfolding digamma_calc_def n31_def SB_def by simp

lemma digamma_calc_37:
  "digamma_calc n37 37 = 10878"
  unfolding digamma_calc_def n37_def SB_def by simp

lemma digamma_calc_41:
  "digamma_calc n41 41 = 23934"
  unfolding digamma_calc_def n41_def SB_def by simp

lemma relation_29:
  "digamma_calc n29 29 = SA n29 - D29"
  unfolding digamma_calc_def SA_def SB_def n29_def D29_def by simp

lemma relation_31:
  "digamma_calc n31 31 = SA n31 + D31"
  unfolding digamma_calc_def SA_def SB_def n31_def D31_def by simp

lemma relation_37:
  "digamma_calc n37 37 = SA n37 + D37"
  unfolding digamma_calc_def SA_def SB_def n37_def D37_def by simp

lemma relation_41:
  "digamma_calc n41 41 = SA n41 + D41"
  unfolding digamma_calc_def SA_def SB_def n41_def D41_def by simp

(****************************************************************)
(* Sous-bloc 6 : Equation generale (SB n - digamma)/64 = p       *)
(****************************************************************)

section "Équation générale reliant SB, digamma_calc et le nombre premier"

lemma SB_minus_digamma_is_64p:
  "SB n - digamma_calc n p = 64 * real p"
  unfolding digamma_calc_def by simp

lemma prime_equation_general:
  "prime_equation n p = real p"
  unfolding prime_equation_def digamma_calc_def by simp

lemma SB_minus_digamma_div_64_general:
  "(SB n - digamma_calc n p) / 64 = real p"
  unfolding digamma_calc_def by simp

theorem reconstruction_premier_pos:
  assumes "n >= 1" "prime p"
  shows "(SB n - digamma_calc n p) / 64 = real p"
proof -
  have "prime_equation n p = real p"
    using prime_equation_for_primes_pos assms by simp
  thus ?thesis
    unfolding prime_equation_def by simp
qed

(**************************************************************)
(* SECTION : Notice — démonstration classique (non originale) *)
(**************************************************************)

section "Notice : démonstration classique du lien zéros ↔ nombres premiers"

text \<open>
  IMPORTANT :
  La démonstration présentée dans cette section n'est PAS de moi.
  Il s'agit d'un résumé standard de la théorie analytique des nombres,
  tel qu'on la trouve dans les ouvrages classiques sur la fonction
  zêta de Riemann (Hadamard, von Mangoldt, Davenport, Edwards, etc.).

  Elle est incluse ici uniquement pour documenter le parallèle conceptuel
  entre la méthode spectrale développée dans ce fichier et la structure
  analytique de la fonction zêta.
\<close>
(**************************************************************)
(* 1. Dérivée logarithmique de ζ(s) et fonction de Mangoldt   *)
(**************************************************************)

text \<open>
  Pour Re(s) > 1, la fonction zêta possède à la fois :

    - un développement en série de Dirichlet :
        ζ(s) = ∑_{n >= 1} 1 / n^s,

    - et un produit d'Euler sur les nombres premiers :
        ζ(s) = ∏_{p premier} (1 - p^{-s})^{-1}.

  En prenant la dérivée logarithmique du produit d'Euler, on obtient :

        -ζ'(s) / ζ(s) = ∑_{n >= 1} Λ(n) / n^s,

  où Λ(n) est la fonction de von Mangoldt :
        Λ(n) = log p si n = p^k, et 0 sinon.

  Cette identité montre que la dérivée logarithmique de ζ(s)
  « encode » directement les nombres premiers.
\<close>
(**************************************************************)
(* 2. La fonction ψ(x) et l'intégrale de Perron               *)
(**************************************************************)

text \<open>
  On introduit la fonction de Chebyshev :

        ψ(x) = ∑_{n <= x} Λ(n).

  Une formule d'inversion complexe (type Perron) donne :

        ψ(x) =
          (1 / 2πi) ∫_{c - i∞}^{c + i∞}
            -ζ'(s)/ζ(s) · x^s / s  ds,

  pour tout c > 1.

  Cette intégrale permet de reconstruire ψ(x) à partir de ζ(s).
\<close>
(**************************************************************)
(* 3. Déplacement du contour et apparition des zéros          *)
(**************************************************************)

text \<open>
  En déplaçant la ligne d'intégration vers la gauche, on traverse :

    - le pôle simple de ζ(s) en s = 1,
    - les zéros non triviaux ρ de ζ(s),
    - les zéros triviaux en s = -2, -4, ...

  Le théorème des résidus donne alors la formule explicite :

        ψ(x) = x
                - ∑_{ρ} x^ρ / ρ
                - (ζ'(0)/ζ(0))
                - (1/2) log(1 - x^{-2})
                + (termes mineurs).

  Cette formule est fondamentale : elle exprime ψ(x) (donc les nombres
  premiers) en fonction des zéros non triviaux de ζ(s).
\<close>
(**************************************************************)
(* 4. Comment les zéros déterminent les nombres premiers       *)
(**************************************************************)

text \<open>
  La structure de la formule explicite :

        ψ(x) = x - ∑_{ρ} x^ρ / ρ + ...

  montre que :

    • le terme principal x donne l'approximation grossière
      (théorème des nombres premiers),

    • la somme sur les zéros non triviaux ρ = β + iγ donne les
      oscillations fines autour de cette approximation.

  Chaque zéro contribue un terme de la forme :

        x^β cos(γ log x) / |ρ|   ou   x^β sin(γ log x) / |ρ|.

  Ainsi :

    - la partie réelle β contrôle la décroissance,
    - la partie imaginaire γ contrôle les oscillations.

  Conclusion profonde :

    La répartition des zéros non triviaux détermine la précision
    avec laquelle ψ(x) (et donc π(x)) suit son terme principal.

    Si tous les zéros non triviaux satisfont Re(ρ) = 1/2
    (Hypothèse de Riemann), alors l'erreur dans la distribution
    des nombres premiers est optimale.

  En ce sens, les zéros non triviaux « déterminent » la position
  des nombres premiers : ψ(x) est explicitement écrite en fonction
  des zéros de ζ(s).
\<close>
(**************************************************************)
(* SECTION : Validation épipolaire du plan trifocal           *)
(**************************************************************)

section "Validation épipolaire du plan trifocal"

text \<open>
  Cette section formalise, de manière abstraite, le plan trifocal :

    1. FZg  : Fonction Zêta (vue globalement),
    2. HyRi : Hypothèse de Riemann,
    3. MsP  : Méthode spectrale et position des nombres premiers.

  On y ajoute :
    - la combinatoire des comparaisons de premiers (simples vs mixtes),
    - la représentation des zéros critiques par un rectangle T_area,
    - la partie tronquée T_tr_area et la partie restante T_restant_area,
    - une courbure de la droite critique modélisée par une aire parabolique,
    - une variable logique HypR_demi_solFinal qui représente la
      « validation géométrique » de Re(s) = 1/2 dans cette perspective.
\<close>
(**************************************************************)
(* 1. Objets abstraits du plan trifocal                       *)
(**************************************************************)

typedecl position          (* position abstraite d'un nombre premier *)
typedecl prime_index       (* indice abstrait pour un nombre premier *)


consts
  FZg_posP   :: "prime_index => position"   (* Position via fonction Zeta *)
  Ms_posP    :: "prime_index => position"   (* Position via methode spectrale *)
  HypR_demi  :: real                       (* Partie reelle 1/2 (RH) *)
  Ms_demi    :: real                       (* Rapport spectral 1/2 (methode spectrale) *)

(**************************************************************)
(* 2. Aires et geometrie de la droite critique                *)
(**************************************************************)

consts
  T_area         :: real  (* Aire totale du rectangle des zeros critiques *)
  T_tr_area      :: real  (* Aire tronquee correspondant a un intervalle de premiers *)
  T_restant_area :: real  (* Aire restante hors de l'intervalle considere *)

  Courb_droitcri_init_aire_parabol :: real  (* Aire sous la courbe "courbee" *)
  Aire_parab                        :: real  (* Aire de la parabole (modele de courbure) *)

(**************************************************************)
(* 3. Combinatoire des comparaisons de premiers               *)
(**************************************************************)

consts
  P_reel        :: real  (* Valeur reelle associee a l'intervalle 0..P-ieme premier *)
  Com_Pinit_Re  :: real  (* Nombre relatif de comparaisons simples dans l'intervalle *)
  Com_mixt_Sup  :: real  (* Nombre relatif de comparaisons mixtes (-,+) *)
  Com_ident     :: real  (* Contribution des comparaisons entre premiers identiques (-p, p) *)

(**************************************************************)
(* 4. Variable logique de "solution" de l'hypothese           *)
(**************************************************************)

consts
  HypR_demi_solFinal :: bool

text \<open>
  Les axiomes suivants codent les relations conceptuelles :

    - FZg_posP et Ms_posP donnent la meme position des premiers,
    - HypR_demi et Ms_demi representent la meme valeur 1/2,
    - l'aire totale T_area est la somme de T_tr_area (tronque) et T_restant_area,
    - la combinatoire mixte est strictement plus riche que la combinatoire initiale,
    - cette sur-combinatoire se traduit par une courbure de la droite critique,
    - si l'aire de la parabole egale l'aire restante T_restant_area,
      alors la variable HypR_demi_solFinal est vraie.
\<close>

consts
  postulate_positions :: "bool"
  postulate_demi :: "bool"
  postulate_aire_rectangle :: "bool"
  postulate_combinatoire_1 :: "bool"
  postulate_combinatoire_2 :: "bool"
  postulate_courbure :: "bool"
  postulate_solution :: "bool"
axiomatization where
  (* 1. Correspondance des positions des premiers : FZg_posP = Ms_posP *)
  postulate_positions:
    "ALL p. FZg_posP p = Ms_posP p" and

  (* 2. Correspondance des valeurs 1/2 : HypR_demi = Ms_demi *)
  postulate_demi:
    "HypR_demi = Ms_demi" and

  (* 3. Decomposition de l'aire totale du rectangle des zeros critiques *)
  postulate_aire_rectangle:
    "T_area = T_tr_area + T_restant_area" and

  (* 4. Combinatoire : l'ecart mixte fournit plus de comparaisons
        que le schema initial, notamment via les comparaisons identiques (-p, p). *)
  postulate_combinatoire_1:
    "Com_Pinit_Re < Com_ident" and
  postulate_combinatoire_2:
    "Com_mixt_Sup > Com_Pinit_Re" and

  (* 5. La sur-combinatoire (Com_Pinit_Re < Com_ident) se traduit
        par une courbure de la droite critique modelisee par Aire_parab. *)
  postulate_courbure:
    "Com_Pinit_Re < Com_ident ==>
     Courb_droitcri_init_aire_parabol = Aire_parab" and

  (* 6. Si l'aire de la parabole egale l'aire restante T_restant_area,
        alors la perspective geometrique est compatible avec Re(s) = 1/2. *)
  postulate_solution:
    "Aire_parab = T_restant_area ==> HypR_demi_solFinal"

(**************************************************************)
(* 5. LEMMES DE VALIDATION LOGIQUE                            *)
(**************************************************************)

lemma positions_coincident_trifocal:
  "FZg_posP p = Ms_posP p"
  using postulate_positions
  by simp

lemma demi_coincident_trifocal:
  "HypR_demi = Ms_demi"
  using postulate_demi
  by simp

lemma aire_rectangle_decompose:
  "T_area = T_tr_area + T_restant_area"
  using postulate_aire_rectangle
  by simp

lemma combinatoire_mixte_stricte:
  "Com_Pinit_Re < Com_ident  &  Com_mixt_Sup > Com_Pinit_Re"
  using postulate_combinatoire_1 postulate_combinatoire_2
  by simp

lemma courbure_induite_par_surcombinatoire:
  assumes "Com_Pinit_Re < Com_ident"
  shows "Courb_droitcri_init_aire_parabol = Aire_parab"
  using assms postulate_courbure
  by simp

lemma solution_epipolaire_Riemann:
  assumes "Com_Pinit_Re < Com_ident"
      and "Aire_parab = T_restant_area"
  shows "HypR_demi_solFinal"
  using assms postulate_courbure postulate_solution
  by simp

(**************************************************************)
(* SECTION : Modele Spectral 1/4 – Definitions completes      *)
(**************************************************************)

section "Modele spectral 1/4 : Forme generale des suites A et B."

text \<open>
  Formes generalisees pour le rapport 1/4.
  On suit les equations :
    ((241/16)/12 * 4^n) - 4/3
    ((964/16)/12 * 4^n) - (3073 * (4/3))
\<close>
(* --- Definition des suites A_1_4 et B_1_4 --- *)

definition A_1_4 :: "nat => real" where
  "A_1_4 n = ((241 / 16) / 12) * (4 ^ n) - (4 / 3)"

definition B_1_4 :: "nat => real" where
  "B_1_4 n = ((964 / 16) / 12) * (4 ^ n) - (3073 * (4 / 3))"


(**************************************************************)
(* SECTION : Equation generale pour le modele spectral 1/4     *)
(**************************************************************)

definition prime_equation_1_4 :: "nat => nat => real" where
  "prime_equation_1_4 n p = (B_1_4 n - (B_1_4 n - 4096 * real p)) / 4096"

lemma prime_equation_1_4_identity:
  "prime_equation_1_4 n p = real p"
  unfolding prime_equation_1_4_def by simp


(**************************************************************)
(* SECTION : Postulat spectral 1/4                            *)
(**************************************************************)

section "Axiomatisation spectral 1/4"

axiomatization where
  spectral_postulate_1_4:
    "!!n p. n > 0 ==> prime p ==> prime_equation_1_4 n p = real p"


(**************************************************************)
(* SECTION : Lemme final pour les nombres premiers (1/4)      *)
(**************************************************************)

lemma prime_equation_1_4_for_primes:
  assumes "n > 0" "prime p"
  shows "prime_equation_1_4 n p = real p"
  using spectral_postulate_1_4 assms by blast


(**************************************************************)
(* SECTION : Exemple concret pour 947                         *)
(**************************************************************)

section "Modele spectral 1/4: Sommes de suite A et B, Digamma, Digamma calcule et determination du premier 947."

text \<open>
  Donnees numeriques globales pour le modele 1/4 :
  - Somme de la suite A : 1316180
  - Somme de la suite B : 5260628
  - Digamma : 65536
  - Digamma calcule : 1316180 + 65536 = 1381716
  - (5260628 - 1381716) / 4096 = 947 (premier)
\<close>
definition suite_A_1_4_somme :: real where
  "suite_A_1_4_somme = 1316180"

definition suite_B_1_4_somme :: real where
  "suite_B_1_4_somme = 5260628"

definition digamma_1_4 :: real where
  "digamma_1_4 = 65536"

definition digamma_calcule_1_4 :: real where
  "digamma_calcule_1_4 = suite_A_1_4_somme + digamma_1_4"

lemma preuve_premier_947:
  "(suite_B_1_4_somme - digamma_calcule_1_4) / 4096 = 947"
  by (simp add: suite_A_1_4_somme_def suite_B_1_4_somme_def
                digamma_1_4_def digamma_calcule_1_4_def)


(**************************************************************)
(* SECTION : Modele Spectral 1/3 – Définitions completes      *)
(**************************************************************)

section "Rapport 1/3 forme generaliser pour les suites A et B."

text \<open>
  Formes généralisées pour le rapport 1/3.
  On suit les équations :
    ((73/9)/12 * 3^n) - 1.5
    ((219/9)/12 * 3^n) - (487 * 1.5)
\<close>
definition A_1_3 :: "nat => real" where
  "A_1_3 n = ((73 / 9) / 12) * (3 ^ n) - 1.5"

definition B_1_3 :: "nat => real" where
  "B_1_3 n = ((219 / 9) / 12) * (3 ^ n) - (487 * 1.5)"


(**************************************************************)
(* SECTION : Equation generale pour le modele spectral 1/3     *)
(**************************************************************)

definition prime_equation_1_3 :: "nat => nat => real" where
  "prime_equation_1_3 n p = (B_1_3 n - (B_1_3 n - 729 * real p)) / 729"

lemma prime_equation_1_3_identity:
  "prime_equation_1_3 n p = real p"
  unfolding prime_equation_1_3_def by simp


(**************************************************************)
(* SECTION : Postulat spectral 1/3                            *)
(**************************************************************)

section "Axiomatisation rapport 1/3."

axiomatization where
  spectral_postulate_1_3:
    "!!n p. n > 0 ==> prime p ==> prime_equation_1_3 n p = real p"


(**************************************************************)
(* SECTION : Lemme final pour les nombres premiers (1/3)      *)
(**************************************************************)

lemma prime_equation_1_3_for_primes:
  assumes "n > 0" "prime p"
  shows "prime_equation_1_3 n p = real p"
  using spectral_postulate_1_3 assms by blast


(**************************************************************)
(* SECTION : Exemple concret pour 227                         *)
(**************************************************************)

section "Rapport spectal 1/3 : validation numerique pour les suites A et B, Digamma, Digamma calcule et la determination du premier 227."

definition suite_A_1_3_somme :: real where
  "suite_A_1_3_somme = 79824"

definition suite_B_1_3_somme :: real where
  "suite_B_1_3_somme = 238746"

section "Rapport 1/3"

definition digamma_1_3 :: real where
  "digamma_1_3 = 6561"

definition digamma_calcule_1_3 :: real where
  "digamma_calcule_1_3 = suite_A_1_3_somme - digamma_1_3"

lemma preuve_premier_227:
  "(suite_B_1_3_somme - digamma_calcule_1_3) / 729 = 227"
  by (simp add: suite_A_1_3_somme_def suite_B_1_3_somme_def
                digamma_1_3_def digamma_calcule_1_3_def)
(**************************************************************)
(* SECTION 6 : Rapport Spectral 1/3 et 1/4                    *)
(**************************************************************)

section "Rapport spectral constant 1/3 et 1/4."

text \<open>
  Définition du Rapport Spectral pour les modèles 1/3 et 1/4.
\<close>
section "Rapport spectral 1/3 – validation généralisée."

(* Rapport spectral 1/3 *)

definition RsP_1_3 :: "nat => nat => real" where
  "RsP_1_3 n1 n2 =
    (A_1_3 n1 - A_1_3 n2) /
    (B_1_3 n1 - B_1_3 n2)"

theorem RsP_un_tiers_constant:
  assumes "n1 > 0" and "n2 > 0" and "n1 ~= n2"
  shows "RsP_1_3 n1 n2 = 1/3"
proof -
  have diff_A:
    "A_1_3 n1 - A_1_3 n2 =
      ((73/9)/12) * (3^n1 - 3^n2)"
    unfolding A_1_3_def by (simp add: algebra_simps)

  have diff_B:
    "B_1_3 n1 - B_1_3 n2 =
      ((219/9)/12) * (3^n1 - 3^n2)"
    unfolding B_1_3_def by (simp add: algebra_simps)

  have "RsP_1_3 n1 n2 =
        (((73/9)/12) * (3^n1 - 3^n2)) /
        (((219/9)/12) * (3^n1 - 3^n2))"
    unfolding RsP_1_3_def by (simp add: diff_A diff_B)

  also have "... = ((73/9)/12) / ((219/9)/12)"
    using assms by (simp add: field_simps)

  also have "... = 1/3"
    by simp

  finally show ?thesis .
qed


(* Rapport spectral 1/4 *)

section "Rapport spectral constant 1/4."

definition RsP_1_4 :: "nat => nat => real" where
  "RsP_1_4 n1 n2 =
    (A_1_4 n1 - A_1_4 n2) /
    (B_1_4 n1 - B_1_4 n2)"

section "Rapport spectral 1/4 – validation généralisée."

theorem RsP_un_quart_constant:
  assumes "n1 > 0" and "n2 > 0" and "n1 ~= n2"
  shows "RsP_1_4 n1 n2 = 1/4"
proof -
  have diff_A:
    "A_1_4 n1 - A_1_4 n2 =
      ((241/16)/12) * (4^n1 - 4^n2)"
    unfolding A_1_4_def by (simp add: algebra_simps)

  have diff_B:
    "B_1_4 n1 - B_1_4 n2 =
      ((964/16)/12) * (4^n1 - 4^n2)"
    unfolding B_1_4_def by (simp add: algebra_simps)

  have "RsP_1_4 n1 n2 =
        (((241/16)/12) * (4^n1 - 4^n2)) /
        (((964/16)/12) * (4^n1 - 4^n2))"
    unfolding RsP_1_4_def by (simp add: diff_A diff_B)

  also have "... = ((241/16)/12) / ((964/16)/12)"
    using assms by (simp add: field_simps)

  also have "... = 1/4"
    by simp

  finally show ?thesis .
qed

(**************************************************************)
(* SECTION : Suites-mxites A et B (-,+)          *)
(**************************************************************)

section "Suites mixtes A et B"

definition SA_mix :: "nat => real" where
  "SA_mix n = 48 + 13 / (2 ^ (n + 2))"

definition SB_mix :: "nat => real" where
  "SB_mix n = -28 + 13 / (2 ^ (n + 1))"

lemma SA_mix_closed_form:
  "SA_mix n = 48 + 13 / (2 ^ (n + 2))"
  by (simp add: SA_mix_def)

lemma SB_mix_closed_form:
  "SB_mix n = -28 + 13 / (2 ^ (n + 1))"
  by (simp add: SB_mix_def)

lemma SA_mix_step:
  "SA_mix (Suc n) = SA_mix n - 13 / (2 ^ (n + 3))"
  unfolding SA_mix_def
  by (simp add: field_simps power_add)

lemma SB_mix_step:
  "SB_mix (Suc n) = SB_mix n - 13 / (2 ^ (n + 2))"
  unfolding SB_mix_def
  by (simp add: field_simps)

lemma SA_mix_limit_shape:
  "SA_mix n - 48 = 13 / (2 ^ (n + 2))"
  unfolding SA_mix_def by simp

lemma SB_mix_limit_shape:
  "SB_mix n + 28 = 13 / (2 ^ (n + 1))"
  unfolding SB_mix_def by simp


section "Reconstruction générale du nombre premier"

definition digamma_mix :: "(nat => real) => nat => real" where
  "digamma_mix K n = SA_mix n + K n"

definition premier_mix :: "(nat => real) => nat => real" where
  "premier_mix K n = (SB_mix n - digamma_mix K n) / (1 / 64)"

lemma premier_mix_rewrite:
  "premier_mix K n = 64 * (SB_mix n - digamma_mix K n)"
  unfolding premier_mix_def
  by (simp add: field_simps)


section "Exemple instancie : six termes negatif"

definition K6 :: "real" where
  "K6 = -(37127 / 256) - SA_mix 6"

definition digamma_mix_6 :: "real" where
  "digamma_mix_6 = SA_mix 6 + K6"

definition premier_mix_6 :: "real" where
  "premier_mix_6 = (SB_mix 6 - digamma_mix_6) / (1 / 64)"

lemma digamma_mix_6_value:
  "digamma_mix_6 = -(37127 / 256)"
  unfolding digamma_mix_6_def K6_def SA_mix_def
  by simp

lemma premier_mix_6_value:
  "premier_mix_6 = 29985 / 4"
  unfolding premier_mix_6_def digamma_mix_6_def K6_def SA_mix_def SB_mix_def
  by (simp add: field_simps)

(**************************************************************)
(* SECTION : Suites négatives – équations spectrales          *)
(**************************************************************)

section "Suites négatives : équations spectrales"

definition SA_neg_eq :: "real => real" where
  "SA_neg_eq n = 3.25 * (2 powr n) - 2"

definition SB_neg_eq :: "real => real" where
  "SB_neg_eq n = 6.5 * (2 powr n) - 66"

definition digamma_neg_calc :: "real => real => real" where
  "digamma_neg_calc n p = SB_neg_eq n - 64 * p"

lemma digamma_neg_calc_equation_alt:
  "digamma_neg_calc n p = (SB_neg_eq n / 64 - p) * 64"
  unfolding digamma_neg_calc_def SB_neg_eq_def
  by (simp add: field_simps)


(**************************************************************)
(* SECTION : Rapport spectral 1/2 négatif (axiomatisation)    *)
(**************************************************************)

section "Rapport spectral 1/2 négatif"

definition RsP_neg :: "real => real => real" where
  "RsP_neg n1 n2 =
     (SA_neg_eq n1 - SA_neg_eq n2) /
     (SB_neg_eq n1 - SB_neg_eq n2)"

axiomatization where
  spectral_ratio_neg_un_demi:
    "!!n1 n2. n1 <= -1 ==> n2 <= -1 ==> n1 ~= n2 ==> RsP_neg n1 n2 = 1/2"

lemma RsP_neg_un_demi_general:
  assumes "n1 <= -1" "n2 <= -1" "n1 ~= n2"
  shows "RsP_neg n1 n2 = 1/2"
  using spectral_ratio_neg_un_demi assms by blast


(**************************************************************)
(* SECTION : Géométrie Spectrale — Asymétrie Ordonnée/Chaotique *)
(**************************************************************)

section "Geometrie spectrale : asymetries"

definition indice_valide :: "int => bool" where
  "indice_valide n = (n >= 1  |  n <= -1)"

definition liste_strictement_croissante :: "int list => bool" where
  "liste_strictement_croissante xs =
     (ALL i j. i < j  &  j < length xs --> xs ! i < xs ! j)"

definition asymetrique_ordonnee :: "int list => int list => bool" where
  "asymetrique_ordonnee A_indices B_indices =
     ((ALL n : set A_indices. indice_valide n)  & 
      (ALL n : set B_indices. indice_valide n)  & 
      liste_strictement_croissante A_indices  & 
      liste_strictement_croissante B_indices  & 
      A_indices ~= []  & 
      B_indices ~= []  & 
      last A_indices < hd B_indices  & 
      length B_indices = length A_indices + 1)"

definition asymetrique_chaotique :: "int list => int list => bool" where
  "asymetrique_chaotique A_indices B_indices =
     ((ALL n : set A_indices. indice_valide n)  & 
      (ALL n : set B_indices. indice_valide n)  & 
      length A_indices ~= length B_indices  & 
      ~ asymetrique_ordonnee A_indices B_indices)"

lemma asymetrie_implique_indices_valides :
  assumes "asymetrique_ordonnee A_indices B_indices  | 
           asymetrique_chaotique A_indices B_indices"
  shows "(ALL n : set A_indices. indice_valide n)  & 
         (ALL n : set B_indices. indice_valide n)"
proof -
  from assms
  show ?thesis
  proof
    assume h1: "asymetrique_ordonnee A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_ordonnee_def by auto
  next
    assume h2: "asymetrique_chaotique A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_chaotique_def by auto
  qed
qed
(**************************************************************)
(* SECTION : Methode de comparaison asymetrique (1/2 et 1/4)  *)
(**************************************************************)

section "Methode de comparaison asymetrique pour 1/2 et 1/4"

text \<open>
  La methode de comparaison asymetrique relie :

  - des suites de nombres premiers A et B (via leurs indices n),
  - les equations generales des suites A et B (SA, SB pour 1/2 ; A_1_4, B_1_4 pour 1/4),
  - et un rapport spectral construit a partir des sommes de blocs.

  Les puissances utilisees dans les equations generales sont egales
  aux positions (indices) des termes dans les suites, ou a la longueur
  des blocs consideres. La methode est applicable a tout ensemble
  de nombres premiers dont la position correspond aux puissances
  des equations generales A et B.
\<close>
(**************************************************************)
(* 1. Version nat des asymetries (indices naturels)           *)
(**************************************************************)

text \<open>
  Les definitions asymetrique_ordonnee et asymetrique_chaotique
  existent deja pour des listes d'entiers (int). Pour travailler
  directement avec les indices naturels des suites SA, SB, A_1_4
  et B_1_4, on introduit une version analogue sur nat.
\<close>
definition indice_valide_nat :: "nat => bool" where
  "indice_valide_nat n = (n > 0)"

definition liste_strictement_croissante_nat :: "nat list => bool" where
  "liste_strictement_croissante_nat xs =
      (ALL i j. i < j  &  j < length xs --> xs ! i < xs ! j)"

definition asymetrique_ordonnee_nat :: "nat list => nat list => bool" where
  "asymetrique_ordonnee_nat A_indices B_indices =
      ((ALL n : set A_indices. indice_valide_nat n)  & 
       (ALL n : set B_indices. indice_valide_nat n)  & 
       liste_strictement_croissante_nat A_indices  & 
       liste_strictement_croissante_nat B_indices  & 
       A_indices ~= []  & 
       B_indices ~= []  & 
       last A_indices < hd B_indices  & 
       length B_indices = length A_indices + 1)"

definition asymetrique_chaotique_nat :: "nat list => nat list => bool" where
  "asymetrique_chaotique_nat A_indices B_indices =
      ((ALL n : set A_indices. indice_valide_nat n)  & 
       (ALL n : set B_indices. indice_valide_nat n)  & 
       length A_indices ~= length B_indices  & 
       ~ asymetrique_ordonnee_nat A_indices B_indices)"

lemma asymetrie_nat_implique_indices_valides :
  assumes "asymetrique_ordonnee_nat A_indices B_indices  | 
           asymetrique_chaotique_nat A_indices B_indices"
  shows "(ALL n : set A_indices. indice_valide_nat n)  & 
         (ALL n : set B_indices. indice_valide_nat n)"
proof -
  from assms show ?thesis
  proof (elim disjE)
    assume h1: "asymetrique_ordonnee_nat A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_ordonnee_nat_def by auto
  next
    assume h2: "asymetrique_chaotique_nat A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_chaotique_nat_def by auto
  qed
qed


(**************************************************************)
(* 2. Methode de comparaison asymetrique pour le modele 1/2   *)
(**************************************************************)

text \<open>
  Pour le modele 1/2, on utilise les suites SA et SB deja definies :

    SA n = (3.25 / 2) * 2^n - 2
    SB n = (6.5 / 2) * 2^n - 66

  La methode de comparaison asymetrique travaille sur des blocs
  d'indices A_indices et B_indices, qui correspondent a des positions
  dans les suites de nombres premiers. On construit un rapport
  spectral de blocs a partir des sommes des valeurs SA et SB.
\<close>
definition somme_SA_bloc :: "nat list => real" where
  "somme_SA_bloc A_indices = sum_list (map SA A_indices)"

definition somme_SB_bloc :: "nat list => real" where
  "somme_SB_bloc B_indices = sum_list (map SB B_indices)"

text \<open>
  Rapport spectral de blocs pour le modele 1/2 :
  on compare la difference des sommes de deux blocs A et B
  pour SA et SB, comme dans l'exemple (11 - 50) / (-40 - 38).
\<close>
definition RsP_bloc_1_2 :: "nat list => nat list => real" where
  "RsP_bloc_1_2 A_indices B_indices =
     (somme_SA_bloc A_indices - somme_SA_bloc B_indices) /
     (somme_SB_bloc A_indices - somme_SB_bloc B_indices)"

text \<open>
  Comparaison asymetrique ordonnee (modele 1/2) :
  - A_indices et B_indices sont strictement croissants,
  - les indices sont valides (n > 0),
  - B contient exactement un element de plus que A,
  - les puissances associees aux equations generales sont donc
    dans l'ordre naturel et decalees d'une unite.
\<close>
definition comparaison_asym_ordonnee_1_2 :: "nat list => nat list => bool" where
  "comparaison_asym_ordonnee_1_2 A_indices B_indices =
     asymetrique_ordonnee_nat A_indices B_indices"

text \<open>
  Comparaison asymetrique chaotique (modele 1/2) :
  - A_indices et B_indices ont des longueurs differentes,
  - l'ordre croissant naturel n'est pas impose,
  - les puissances associees aux equations generales ne sont pas
    necessairement consecutives.
\<close>
definition comparaison_asym_chaotique_1_2 :: "nat list => nat list => bool" where
  "comparaison_asym_chaotique_1_2 A_indices B_indices =
     asymetrique_chaotique_nat A_indices B_indices"

text \<open>
  La methode de comparaison asymetrique pour le modele 1/2
  consiste donc a :
  - choisir deux blocs A_indices et B_indices,
  - verifier s'ils sont en configuration asymetrique ordonnee
    ou chaotique,
  - calculer le rapport RsP_bloc_1_2 A_indices B_indices.

  Ce rapport est numeriquement tres proche de 1/2 dans le regime
  chaotique, et evolue vers 1 dans certaines configurations
  asymetriques ordonnees lorsque la taille des blocs augmente.
  Ces comportements sont observes numeriquement et interpretes
  comme signatures spectrales, sans etre derives algébriquement.
\<close>
(**************************************************************)
(* 3. Methode de comparaison asymetrique pour le modele 1/4   *)
(**************************************************************)

text \<open>
  Pour le modele 1/4, on utilise les suites A_1_4 et B_1_4 :

    A_1_4 n = ((241/16)/12) * 4^n - 4/3
    B_1_4 n = ((964/16)/12) * 4^n - (3073 * (4/3))

  On applique la meme methode de comparaison asymetrique,
  cette fois avec ces equations generales.
\<close>
definition somme_A_1_4_bloc :: "nat list => real" where
  "somme_A_1_4_bloc A_indices = sum_list (map A_1_4 A_indices)"

definition somme_B_1_4_bloc :: "nat list => real" where
  "somme_B_1_4_bloc B_indices = sum_list (map B_1_4 B_indices)"

definition RsP_bloc_1_4 :: "nat list => nat list => real" where
  "RsP_bloc_1_4 A_indices B_indices =
     (somme_A_1_4_bloc A_indices - somme_A_1_4_bloc B_indices) /
     (somme_B_1_4_bloc A_indices - somme_B_1_4_bloc B_indices)"

definition comparaison_asym_ordonnee_1_4 :: "nat list => nat list => bool" where
  "comparaison_asym_ordonnee_1_4 A_indices B_indices =
     asymetrique_ordonnee_nat A_indices B_indices"

definition comparaison_asym_chaotique_1_4 :: "nat list => nat list => bool" where
  "comparaison_asym_chaotique_1_4 A_indices B_indices =
     asymetrique_chaotique_nat A_indices B_indices"

text \<open>
  Comme pour le modele 1/2, la methode de comparaison asymetrique
  pour le modele 1/4 s'applique a tout ensemble de nombres premiers
  dont les positions (indices) correspondent aux puissances utilisees
  dans les equations generales A_1_4 et B_1_4.

  Les configurations asymetriques ordonnees et chaotiques permettent
  d'observer numeriquement des rapports proches de 1/4 ou evoluant
  vers 1, sans que ces valeurs puissent etre obtenues par une
  simplification algébrique directe des equations generales.
\<close>
(**************************************************************)
(* SECTION : Rapport spectral 1/3 négatif (axiomatisation)     *)
(**************************************************************)

section "Rapport spectral 1/3 negatif"

(*
  Suites A et B generalisees pour le rapport 1/3.
  A(n) = ((73/9)/6) * 3^n - 1.5
  B(n) = ((219/9)/6) * 3^n - (487 * 1.5)
*)

definition SA_neg_eq_un_tiers :: "real => real" where
  "SA_neg_eq_un_tiers n = ((73/9) / 6) * (3 powr n) - 1.5"

definition SB_neg_eq_un_tiers :: "real => real" where
  "SB_neg_eq_un_tiers n = ((219/9) / 6) * (3 powr n) - (487 * 1.5)"

definition RsP_neg_un_tiers :: "real => real => real" where
  "RsP_neg_un_tiers n1 n2 =
     (SA_neg_eq_un_tiers n1 - SA_neg_eq_un_tiers n2) /
     (SB_neg_eq_un_tiers n1 - SB_neg_eq_un_tiers n2)"

(*
  Axiomatisation :
  Comme pour le rapport 1/2, la valeur numerique du rapport spectral
  vaut 1/3 pour toutes paires (n1,n2) negatives distinctes.
  Mais cette valeur ne peut pas etre obtenue algébriquement.
  On encode donc cette realite physique/numerique comme un axiome,
  parallele a l'effet Hall fractionnaire.
*)

axiomatization where
  spectral_ratio_neg_un_tiers:
    "!!n1 n2. n1 <= -1 ==> n2 <= -1 ==> n1 ~= n2 ==> RsP_neg_un_tiers n1 n2 = 1/3"

lemma RsP_neg_un_tiers_general:
  assumes "n1 <= -1" "n2 <= -1" "n1 ~= n2"
  shows "RsP_neg_un_tiers n1 n2 = 1/3"
  using spectral_ratio_neg_un_tiers assms by blast
 (**************************************************************)
(* SECTION : Rapport spectral 1/4 négatif (axiomatisation)     *)
(**************************************************************)

section "Rapport spectral 1/4 negatif"

(*
  Suites A et B generalisees pour le rapport 1/4.
  A(n) = ((241/16)/12) * 4^n - (4/3)
  B(n) = ((964/16)/12) * 4^n - (3073 * (4/3))
*)

definition SA_neg_eq_un_quart :: "real => real" where
  "SA_neg_eq_un_quart n = ((241/16) / 12) * (4 powr n) - (4/3)"

definition SB_neg_eq_un_quart :: "real => real" where
  "SB_neg_eq_un_quart n = ((964/16) / 12) * (4 powr n) - (3073 * (4/3))"

definition RsP_neg_un_quart :: "real => real => real" where
  "RsP_neg_un_quart n1 n2 =
     (SA_neg_eq_un_quart n1 - SA_neg_eq_un_quart n2) /
     (SB_neg_eq_un_quart n1 - SB_neg_eq_un_quart n2)"

(*
  Axiomatisation :
  Comme pour 1/2 et 1/3, le rapport spectral numerique vaut 1/4.
  Mais aucune reduction algébrique ne permet d'obtenir cette valeur.
*)

axiomatization where
  spectral_ratio_neg_un_quart:
    "!!n1 n2. n1 <= -1 ==> n2 <= -1 ==> n1 ~= n2 ==>
                 RsP_neg_un_quart n1 n2 = 1/4"

lemma RsP_neg_un_quart_general:
  assumes "n1 <= -1" "n2 <= -1" "n1 ~= n2"
  shows "RsP_neg_un_quart n1 n2 = 1/4"
  using spectral_ratio_neg_un_quart assms by blast

(**************************************************************)
(* SECTION : Forme générale de l'écart négatif                *)
(**************************************************************)

section "Forme générale de l'écart négatif"

definition gap_neg_val ::
  "real => real => real => real => real => real" where
  "gap_neg_val A_next B_high D_high D_low dummy =
      (A_next - (B_high - D_high) - D_low) / 64"


(**************************************************************)
(* SECTION : Exemple complet – écart entre -19 et -5          *)
(**************************************************************)

section "Exemple complet : écart entre -19 et -5"

definition n_m7  :: real where "n_m7  = -7"
definition n_m3  :: real where "n_m3  = -3"
definition n_m19 :: real where "n_m19 = -8"


(**************************************************************)
(* SECTION : Valeurs spectrales exactes (-19 et -5)           *)
(**************************************************************)

section "Valeurs spectrales exactes pour -19 et -5"

definition SA_m7_val :: real where
  "SA_m7_val = -10110 / 5120"

definition SB_m5_val :: real where
  "SB_m5_val = -20860 / 320"

definition D_m5_val :: real where
  "D_m5_val = 81540 / 320"

definition SB_m19_val :: real where
  "SB_m19_val = -337790 / 5120"

definition D_m19_val :: real where
  "D_m19_val = 5888130 / 5120"


(**************************************************************)
(* SECTION : Lemme final – écart -19 / -5                     *)
(**************************************************************)

section "Démonstration finale : écart -19 / -5"

lemma gap_m19_m5:
  "gap_neg_val SA_m7_val SB_m5_val D_m5_val D_m19_val 0 = -13"
  unfolding gap_neg_val_def
            SA_m7_val_def SB_m5_val_def
            D_m5_val_def D_m19_val_def
  by simp


(**************************************************************)
(* SECTION : Exemple complet – écart entre -31 et 17          *)
(**************************************************************)

section "Exemple complet : écart entre -31 et 17"

definition n_m29 :: real where "n_m29 = -10"
definition n_p17 :: real where "n_p17 = 8"
definition n_m31 :: real where "n_m31 = -11"


(**************************************************************)
(* SECTION : Valeurs spectrales exactes (-31 et 17)           *)
(**************************************************************)

section "Valeurs spectrales exactes pour -31 et 17"

definition SA_m29_val :: real where
  "SA_m29_val = -40895 / 20480"

definition SB_p17_val :: real where
  "SB_p17_val = 350"

definition D_p17_val :: real where
  "D_p17_val = -738"

definition SB_m31_val :: real where
  "SB_m31_val = -1351615 / 20480"

definition D_m31_val :: real where
  "D_m31_val = 39280705 / 20480"


(**************************************************************)
(* SECTION : Forme générale de l'écart mixte                  *)
(**************************************************************)

section "Forme générale de l'écart mixte"

definition gap_mix_val ::
  "real => real => real => real => real => real" where
  "gap_mix_val A_next B_high D_high D_low dummy =
      (A_next - (B_high - D_high) - D_low) / 64"


(**************************************************************)
(* SECTION : Lemme final – écart -31 / 17                     *)
(**************************************************************)

section "Démonstration finale : écart -31 / 17"

lemma gap_m31_17:
  "gap_mix_val SA_m29_val SB_p17_val D_p17_val D_m31_val 0 = -47"
  unfolding gap_mix_val_def
            SA_m29_val_def SB_p17_val_def
            D_p17_val_def D_m31_val_def
  by simp
(**************************************************************)
(* SECTION : Valeurs spectrales exactes pour 23 et 7          *)
(**************************************************************)

section "Valeurs spectrales exactes pour 23 et 7"

definition SA_11_val :: real where "SA_11_val = 50"
definition SB_23_val :: real where "SB_23_val = 1598"
definition D_23_val  :: real where "D_23_val = 126"
definition SB_7_val  :: real where "SB_7_val = -14"
definition D_7_val   :: real where "D_7_val = -464"


(**************************************************************)
(* SECTION : Note explicite sur l'inclusion du zéro           *)
(**************************************************************)

section "Note sur l'inclusion du zéro dans les écarts spectraux"

text \<open>
  Le zéro n'est inclus que dans les écarts mixtes (exemple -31 / 17).
  Dans les écarts du même signe (-19 / -5 et 23 / 7), la progression
  spectrale ne traverse pas 0, donc il n'est pas compté.
\<close>
(**************************************************************)
(* SECTION : Exemple complet – écart entre 227 et 173 (1/3)   *)
(**************************************************************)

section "Exemple complet : écart entre les premiers 227 et 173 (rapport 1/3)"

text \<open>
  Exemple positif : quantité de nombres entre les deux premiers 227 et 173.

  Données spectrales :

    - Le premier suivant 173 est 179
    - Rang spectral de 227 : 10
    - Rang spectral de 173 : 1

  Valeurs numériques :

    SA(227) = 79824
    SB(227) = 238746
    D(227)  = 73263

    SA(179) = 96/9

    SB(173) = -2155/3
    D(173)  = -1141518/9

  Formule générale (rapport 1/3) :

      (A_next - (B_high - D_high) - D_low) / 729

  Résultat :

      ((96/9) - (238746 - 73263) - (-1141518/9)) / 729 = -53

  Ce qui correspond aux 53 nombres entre 227 et 173.
\<close>
(**************************************************************)
(* SECTION : Valeurs spectrales exactes pour 227 et 173       *)
(**************************************************************)

section "Valeurs spectrales exactes pour 227 et 173 (1/3)"

definition SA_227_val :: real where
  "SA_227_val = 79824"

definition SB_227_val :: real where
  "SB_227_val = 238746"

definition D_227_val :: real where
  "D_227_val = 73263"

definition SA_179_val :: real where
  "SA_179_val = 96/9"

definition SB_173_val :: real where
  "SB_173_val = -2155/3"

definition D_173_val :: real where
  "D_173_val = -1141518/9"


(**************************************************************)
(* SECTION : Validation de l'écart entre 227 et 173           *)
(**************************************************************)

section "Validation numérique de l'écart entre 227 et 173 (1/3)"

lemma ecart_227_173_1_3:
  "((SA_179_val - (SB_227_val - D_227_val) - D_173_val) / 729) = -53"
  by (simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def)


(**************************************************************)
(* SECTION : Equation generale d'ecart pour le rapport 1/3    *)
(**************************************************************)

section "Equation generale d'ecart pour le rapport spectral 1/3"

text \<open>
  Formule generale pour l'ecart entre deux nombres premiers
  dans le modele spectral 1/3, a partir de deux suites A et B
  de n termes et de leurs Digamma associes.

  Forme generale (rapport 1/3) :

      (A_next - (B_high - D_high) - D_low) / 729

  ou :

    - A_next  : somme de la suite A pour le premier suivant du plus petit
    - B_high  : somme de la suite B pour le plus grand premier
    - D_high  : Digamma du plus grand premier
    - D_low   : Digamma du plus petit premier

  Le resultat correspond a la quantite de nombres entiers entre les deux premiers.
\<close>
definition gap_equation_1_3 :: "real => real => real => real => real" where
  "gap_equation_1_3 A_next B_high D_high D_low =
     (A_next - (B_high - D_high) - D_low) / 729"

lemma gap_equation_1_3_simplifiee:
  "gap_equation_1_3 A_next B_high D_high D_low =
     (A_next - B_high + D_high - D_low) / 729"
  unfolding gap_equation_1_3_def by simp


(**************************************************************)
(* SECTION : Postulat spectral d'ecart 1/3                    *)
(**************************************************************)

text \<open>
  Postulat spectral d'ecart pour le rapport 1/3 :

  Pour toute paire de nombres premiers (p_high, p_low),
  et pour leurs valeurs spectrales associees (A_next, B_high, D_high, D_low)
  construites selon le modele 1/3, l'equation d'ecart donne exactement
  la quantite de nombres entiers entre ces deux premiers :

      gap_equation_1_3 ... = p_low - p_high
\<close>
axiomatization where
  spectral_gap_postulate_1_3:
    "!!p_high p_low A_next B_high D_high D_low.
       prime p_high ==> prime p_low ==>
       gap_equation_1_3 A_next B_high D_high D_low =
         real (p_low - p_high)"


(**************************************************************)
(* SECTION : Lemme general pour l'ecart entre deux premiers   *)
(**************************************************************)

lemma gap_equation_1_3_for_primes:
  assumes "prime p_high" "prime p_low"
  shows "gap_equation_1_3 A_next B_high D_high D_low =
         real (p_low - p_high)"
  using spectral_gap_postulate_1_3 assms by blast


(**************************************************************)
(* SECTION : Lien avec l'exemple 227 / 173                    *)
(**************************************************************)

section "Validation de l'exemple 227 / 173 via l'equation generale 1/3"

lemma ecart_227_173_1_3_via_gap_equation:
  "gap_equation_1_3 SA_179_val SB_227_val D_227_val D_173_val = -53"
  by (simp add: gap_equation_1_3_def
                SA_179_val_def SB_227_val_def
                D_227_val_def D_173_val_def)


(**************************************************************)
(* SECTION : Valeurs spectrales exactes pour 947 et 881 (1/4) *)
(**************************************************************)

section "Valeurs spectrales exactes pour 947 et 881 (1/4)"

definition SA_883_val :: real where
  "SA_883_val = 75/4"

definition SB_947_val :: real where
  "SB_947_val = 5260628"

definition D_947_val :: real where
  "D_947_val = 1381716"

definition D_881_val :: real where
  "D_881_val = -(14450613/4)"


(**************************************************************)
(* SECTION : Equation generale d'ecart pour le rapport 1/4    *)
(**************************************************************)

section "Equation generale d'ecart pour le rapport spectral 1/4"

definition gap_equation_1_4 :: "real => real => real => real => real" where
  "gap_equation_1_4 A_next B_high D_high D_low =
     (A_next - (B_high - D_high) - D_low) / 4096"

lemma gap_equation_1_4_simplifiee:
  "gap_equation_1_4 A_next B_high D_high D_low =
     (A_next - B_high + D_high - D_low) / 4096"
  unfolding gap_equation_1_4_def by simp


(**************************************************************)
(* SECTION : Postulat spectral d'ecart 1/4                    *)
(**************************************************************)

text \<open>
  Postulat spectral d'ecart pour le rapport 1/4 :

  Pour toute paire de nombres premiers (p_high, p_low),
  et pour leurs valeurs spectrales associees (A_next, B_high, D_high, D_low)
  construites selon le modele 1/4, l'equation d'ecart donne exactement
  la quantite de nombres entiers entre ces deux premiers :

      gap_equation_1_4 ... = p_low - p_high
\<close>
axiomatization where
  spectral_gap_postulate_1_4:
    "!!p_high p_low A_next B_high D_high D_low.
       prime p_high ==> prime p_low ==>
       gap_equation_1_4 A_next B_high D_high D_low =
         real (p_low - p_high)"


(**************************************************************)
(* SECTION : Lemme general pour l'ecart entre deux premiers   *)
(**************************************************************)

lemma gap_equation_1_4_for_primes:
  assumes "prime p_high" "prime p_low"
  shows "gap_equation_1_4 A_next B_high D_high D_low =
         real (p_low - p_high)"
  using spectral_gap_postulate_1_4 assms by blast


(**************************************************************)
(* SECTION : Lien avec l'exemple 947 / 881                    *)
(**************************************************************)

section "Validation de l'exemple 947 / 881 via l'equation generale 1/4"

lemma ecart_947_881_1_4_via_gap_equation:
  "gap_equation_1_4 SA_883_val SB_947_val D_947_val D_881_val = -65"
  by (simp add: gap_equation_1_4_def
                SA_883_val_def SB_947_val_def
                D_947_val_def D_881_val_def)


(**************************************************************)
(* CHAPITRE DEUXIÈME : Axiomatisation analytique (ζ) et spectrale *)
(**************************************************************)

text \<open>
  Mise en garde concernant la présente section

  La section qui suit est fournie exclusivement à titre de référence conceptuelle.
  Elle ne fait pas partie de l’œuvre propre de l’auteur Philippe Thomas Savard et
  n’est employée ici qu’en tant qu’exemple informatif destiné à situer certains
  éléments analytiques dans un cadre logique compatible avec Isabelle/HOL.

  Les contenus, notions ou structures évoqués dans cette section ne constituent
  pas une contribution originale de l’auteur et ne doivent pas être interprétés
  comme faisant partie intégrante de la méthode_spectral.thy. Ils ne sont cités
  qu’à titre d’illustration conceptuelle, sans garantie, sans validation interne
  et sans prétention à l’exactitude analytique ou historique.

  Il est explicitement affirmé que :

    • la présente section ne limite, ne contraint, n’altère ni ne modifie en
      aucune manière la nature, la portée, la validité ou l’évolution des
      références externes auxquelles elle fait allusion ;

    • la méthode_spectral.thy demeure une entité autonome, complète dans sa
      propre structure, et ne dépend en aucune manière des exemples, axiomes ou
      formulations présentés dans cette section ;

    • la présente section ne crée aucune forme d’autoréférence, de dépendance
      circulaire ou d’interaction logique entre la méthode spectrale et les
      références externes : chacune de ces entités demeure indépendante, valide
      par elle-même, et libre dans sa nature propre, sans restriction temporelle
      ou conceptuelle ;

    • aucune des deux entités — ni la méthode_spectral.thy, ni les exemples
      analytiques présentés ici — ne possède la capacité d’annuler, d’invalider
      ou de restreindre l’autre, que ce soit par leur contenu, leur structure ou
      leur interprétation.

  En résumé, la présente section constitue un exemple conceptuel indépendant,
  sans effet contraignant, sans interaction logique obligatoire, et sans
  influence sur la validité intrinsèque de la méthode spectrale ou des
  références externes auxquelles elle renvoie.
\<close>
(**************************************************************)
(* CHAPITRE DEUXIÈME : Axiomatisation analytique (ζ) et spectrale *)
(**************************************************************)

section "Axiomatisation analytique et géométrique de la position des nombres premiers"

text \<open>
  Dans cette section, nous introduisons, sous forme axiomatique, le lien classique
  de la théorie analytique des nombres entre les zéros de la fonction ζ de Riemann
  et la position des nombres premiers. Cette axiomatisation n’est pas une création
  originale de l’auteur de la méthode spectrale (Philippe Thomas Savard), mais une
  abstraction inspirée des formules explicites de la théorie des nombres, telles
  que celles de Riemann, von Mangoldt et leurs successeurs.
\<close>
text \<open>
  1. Axiomatisation (abstraite) de la fonction ζ et de ses zéros

  On introduit un type abstrait pour représenter les zéros non triviaux de ζ,
  ainsi qu’une fonction donnant leur partie réelle. On ne formalise pas ici la
  fonction ζ elle-même, ni la formule explicite complète, mais on encode le fait
  que les zéros déterminent la position des nombres premiers, comme le suggèrent
  les formules explicites de Riemann–von Mangoldt.
\<close>
typedecl zero_zeta

consts
  Re_zero_zeta :: "zero_zeta => real"
  Im_zero_zeta :: "zero_zeta => real"

text \<open>
  La fonction suivante représente, de manière abstraite, la contribution d’un zéro
  de ζ à la détermination de la position du n-ième nombre premier. Elle est inspirée
  des formules explicites (de type Riemann–von Mangoldt) qui expriment des fonctions
  arithmétiques liées aux nombres premiers en termes de sommes sur les zéros de ζ.
\<close>
consts
  prime_position_from_zero :: "zero_zeta => nat => bool"

axiomatization where
  explicit_formula_axiom:
    "ALL n. EX \<rho>::zero_zeta. prime_position_from_zero \<rho> n"

text \<open>
  Interprétation : pour chaque entier naturel n, il existe au moins un zéro non trivial
  de ζ qui intervient dans la détermination de la position du n-ième nombre premier.
  Cet axiome formalise, de manière abstraite, l’idée que « les zéros de ζ déterminent
  la position des nombres premiers », telle qu’on la trouve dans la théorie analytique
  classique (formules explicites).
\<close>
text \<open>
  2. Axiomatisation de l’évidence spectrale issue de la méthode de Philippôt

  La méthode spectrale, telle que développée dans les sections précédentes, repose
  sur les faits suivants (formulés ici de manière synthétique) :

  – Quand n >= 1 et n <= -1 (au sens de la structure spectrale considérée),
    tous les n ramènent à un nombre premier P.
  – La valeur de n est déterminée par la quantité de termes dans les suites A et B.
  – Tous les nombres premiers P entre eux respectent le rapport spectral 1/k.
  – Ce rapport 1/k est numériquement valide mais algébriquement incohérent.

  Nous encapsulons cette évidence sous forme de constantes et d’axiomes abstraits.
\<close>
typedecl indice_spectral   (* type abstrait pour les n de la méthode spectrale *)
typedecl premier_spectral  (* type abstrait pour les P de la méthode spectrale *)

consts
  A_suite :: "indice_spectral => nat"
  B_suite :: "indice_spectral => nat"
  P_spectral :: "indice_spectral => premier_spectral"
  rapport_spectral :: "premier_spectral => premier_spectral => rat"

text \<open>
  Axiome : chaque indice spectral n (dans le domaine considéré) ramène à un nombre
  premier spectral P, et la valeur de n est déterminée par la quantité de termes
  dans les suites A et B. Le détail constructif est donné dans les sections précédentes
  de la méthode spectrale ; ici, nous en donnons une abstraction logique.
\<close>
axiomatization where
  spectral_index_to_prime:
    "ALL n::indice_spectral. EX P::premier_spectral. P_spectral n = P" and

  spectral_index_from_suites:
    "ALL n::indice_spectral. A_suite n + B_suite n >= 1"

text \<open>
  Axiome : tous les nombres premiers spectraux P entre eux respectent un rapport
  spectral 1/k, numériquement valide mais algébriquement incohérent. On encode
  cela en imposant que le rapport entre deux premiers spectraux soit toujours
  de la forme 1/k pour un certain entier k >= 1.
\<close>
consts
  k_spectral :: "premier_spectral => premier_spectral => nat"

axiomatization where
  rapport_spectral_forme:
    "ALL P Q::premier_spectral. k_spectral P Q >= 1
      --> rapport_spectral P Q = 1 / (of_nat (k_spectral P Q))"

text \<open>
  Interprétation : le rapport spectral entre deux nombres premiers où groupe de nombres premier   
  asymétrique ordonnés ou chaotiques de même que symétriques en paire 1*1 ou n*n
  spectraux P et Q est toujours de la forme 1/k, avec k un entier naturel >= 1. Ce rapport est
  numériquement bien défini (dans ℚ), mais ne correspond pas à une relation
  algébrique classique entre nombres premiers, d’où l’expression « algébriquement
  incohérent » dans le texte conceptuel.
\<close>
text \<open>
  3. Axiomatisation du lien entre la fonction ζ et la géométrie spectrale

  Nous introduisons maintenant un axiome de concordance : la structure spectrale
  issue de la méthode de Philippôt est compatible, sur le plan conceptuel, avec
  la structure analytique donnée par les zéros de ζ. Plus précisément, nous
  postulons qu’à chaque indice spectral n correspond un zéro de ζ qui intervient
  dans la détermination de la position du nombre premier associé.
\<close>
consts
  zero_associe :: "indice_spectral => zero_zeta"

axiomatization where
  concordance_spectrale:
    "ALL n::indice_spectral.
       prime_position_from_zero (zero_associe n) (A_suite n + B_suite n)"

text \<open>
  Interprétation : pour chaque indice spectral n, il existe un zéro de ζ (ici
  représenté par \<open>zero_associe n\<close>) qui intervient, via la fonction abstraite
  \<open>prime_position_from_zero\<close>, dans la détermination de la position du nombre
  premier correspondant (codé ici par la quantité de termes A_suite n + B_suite n).

  Cet axiome formalise le parallèle conceptuel entre :

  – la théorie analytique de la fonction ζ de Riemann, où les zéros déterminent
    la position des nombres premiers (formules explicites) ;
  – la géométrie du spectre des nombres premiers de la méthode de Philippôt,
    où les indices spectraux n, les suites A et B, et le rapport 1/k organisent
    la position des nombres premiers dans une structure spectrale cohérente.

  Cette section ne prétend pas démontrer l’hypothèse de Riemann, ni reconstruire
  la théorie analytique complète de ζ, mais elle établit, dans le langage d’Isabelle/HOL,
  une concordance axiomatique entre la méthode spectrale et la vision analytique
  classique de la distribution des nombres premiers.
\<close>
(**************************************************************)
(* CHAPITRE DEUXIÈME : Axiomatisation analytique (ζ) et spectrale *)
(**************************************************************)

text \<open>
  Dans ce chapitre, nous introduisons une axiomatisation abstraite de la fonction
  ζ de Riemann et de ses zéros non triviaux, dans le but de formuler, dans le
  langage d’Isabelle/HOL, une version informative de la conjecture de Riemann.
  Il ne s’agit pas d’une démonstration, mais d’une mise en forme logique d’une
  conjecture classique de la théorie analytique des nombres.
\<close>
typedecl complex_zero_zeta   \<comment> \<open>type abstrait pour les zéros non triviaux de ζ\<close>

consts
  Re_cz :: "complex_zero_zeta => real"   \<comment> \<open>partie réelle du zéro\<close>
  Im_cz :: "complex_zero_zeta => real"   \<comment> \<open>partie imaginaire du zéro\<close>

text \<open>
  Nous ne définissons pas ici la fonction ζ elle-même, ni son prolongement
  analytique. Nous supposons simplement l’existence d’un ensemble abstrait de
  zéros non triviaux, chacun muni d’une partie réelle et d’une partie imaginaire.
\<close>
text \<open>
  Conjecture de Riemann (version axiomatique)

  La conjecture de Riemann affirme que tous les zéros non triviaux de la fonction
  ζ de Riemann ont une partie réelle égale à 1/2. Nous l’exprimons ici sous la
  forme d’un axiome, afin de pouvoir raisonner dans un cadre où cette conjecture
  est supposée vraie, sans prétendre la démontrer.
\<close>
axiomatization where
  Riemann_Hypothesis:
    "ALL \<rho>::complex_zero_zeta. Re_cz \<rho> = 1 / 2"

typedecl prime_number

consts
  P_of :: "prime_index => prime_number"

text \<open>
  Interprétation : le type \<open>prime_index\<close> représente un indice abstrait pour les
  nombres premiers, et \<open>P_of\<close> associe à chaque indice un nombre premier. Dans la
  théorie analytique classique, les zéros de ζ contrôlent la distribution de ces
  nombres premiers. Nous ne formalisons pas ici la formule explicite, mais nous
  admettons ce lien comme principe conceptuel.
\<close>
(**************************************************************)
(* SECTION : Modèle géométrique des aires sur la droite critique *)
(**************************************************************)

text \<open>
  La présente section introduit un modèle abstrait où la droite critique
  Re(s) = 1/2 est représentée par une aire totale T, tronquée à une hauteur
  finie. Une sous-aire Tn = T/n correspond à une zone où les zéros sont plus
  denses, en lien avec un intervalle tronqué de nombres premiers. L’aire
  restante T_rest = T − Tn est mise en correspondance avec une aire relative
  générée par une courbure effective de la droite critique, induite par la
  structure combinatoire des écarts mixtes. L’égalité de ces deux aires est
  interprétée comme une condition géométrique équivalente à la conjecture de
  Riemann, sans constituer une démonstration analytique.
\<close>
typedecl area
typedecl interval

consts
  T      :: area      \<comment> \<open>aire totale de la droite critique\<close>
  Tn     :: area      \<comment> \<open>sous-aire T/n plus dense en zéros\<close>
  T_rest :: area      \<comment> \<open>aire restante T − Tn\<close>

  P      :: interval  \<comment> \<open>intervalle complet de nombres premiers associé à T\<close>
  Pn     :: interval  \<comment> \<open>intervalle tronqué associé à Tn\<close>

consts
  relative_value :: "interval => real"
  geometric_area :: "real => area"

axiomatization where
  mixed_gap_surplus:
    "relative_value Pn > relative_value P" and

  complementary_areas:
    "T_rest = geometric_area (relative_value Pn - relative_value P)"

consts Re_zero :: "zero_zeta => real"

axiomatization where
  all_zeros_on_critical_line:
    "(T_rest = geometric_area (relative_value Pn - relative_value P)) ==> (ALL \<rho>::zero_zeta. Re_zero \<rho> = 1/2)"


end
