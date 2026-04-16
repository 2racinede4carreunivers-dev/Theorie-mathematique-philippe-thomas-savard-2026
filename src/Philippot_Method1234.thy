theory Philippot_Method
  imports Complex_Main
begin

text \<open>
**********************************************************************
*******************   Chapitre A — Règles de la méthode de Philippôt   *******************
**********************************************************************
\<close>

text \<open>
  Méthode de Philippôt — Règles structurelles fondamentales.

  1. La méthode comporte un minimum de trois étapes,
     mais peut en contenir une infinité.

  2. Chaque étape contient exactement une suite.

  3. Toutes les suites d'une même méthode possèdent
     le même nombre de termes.

  4. Chaque suite contient au minimum trois termes,
     tous strictement inférieurs à 1 (termes fractionnaires).

  5. Tous les termes fractionnaires de toutes les suites
     doivent être strictement inférieurs à 1.

  6. À partir de l'étape 2, chaque suite doit subir
     exactement une substitution à chaque étape.

  7. Pour les suites de longueur \<le> 7, la substitution
     s'effectue selon la position suivante :
       - 3 termes \<rightarrow> position 1 (index 0)
       - 4 termes \<rightarrow> position 2 (index 1)
       - 5 termes \<rightarrow> position 3 (index 2)
       - 6 termes \<rightarrow> position 4 (index 3)
       - 7 termes \<rightarrow> position 5 (index 4)

  8. Pour les suites de longueur \<ge> 8, la substitution
     s'effectue toujours à la 6ᵉ position (index 5).

  9. L'avant-dernier terme d'une suite est obtenu en
     multipliant le terme précédent par le facteur :
       1 / (k - 1/k)

  10. Tous les autres termes d'une suite, dans l'ordre croissant,
      sont obtenus en multipliant le terme précédent par k.

  11. Les suites sont ordonnées de la première à la dernière position
      de manière croissante.

  12. À chaque étape, tous les termes de la suite sont additionnés.

  13. À l'étape 1, la somme est Rs = 1/k.
      À partir de l'étape 2, la somme est Rs moins la valeur substituée.

  14. Le rapport spectral entre deux valeurs substituées consécutives
      est toujours égal à 1/k.
\<close>

type_synonym term  = real
type_synonym suite = "real list"

locale philippot_structure =
  fixes k :: real
  assumes k_gt1: "k > 1"
begin

definition valid_suite :: "suite \<Rightarrow> bool" where
  "valid_suite s \<longleftrightarrow>
     (length s \<ge> 3 \<and>
      (\<forall>x \<in> set s. x < 1) \<and>
      sorted s)"

definition valid_method :: "(nat \<Rightarrow> suite) \<Rightarrow> bool" where
  "valid_method S \<longleftrightarrow>
     (\<forall>n. valid_suite (S n)) \<and>
     (\<forall>m n. length (S m) = length (S n)) \<and>
     (\<exists>n0. n0 \<ge> 3)"

fun subst_pos :: "nat \<Rightarrow> nat option" where
  "subst_pos 3 = Some 0" |
  "subst_pos 4 = Some 1" |
  "subst_pos 5 = Some 2" |
  "subst_pos 6 = Some 3" |
  "subst_pos 7 = Some 4" |
  "subst_pos n = (if n >= 8 then Some 5 else None)"

fun substitute_at :: "suite \<Rightarrow> nat \<Rightarrow> real \<Rightarrow> suite" where
  "substitute_at [] _ _ = []" |
  "substitute_at (x#xs) 0 v = v # xs" |
  "substitute_at (x#xs) (Suc p) v = x # substitute_at xs p v"

fun substitute :: "suite \<Rightarrow> real \<Rightarrow> suite" where
  "substitute s v =
     (case subst_pos (length s) of
        None \<Rightarrow> s
      | Some p \<Rightarrow> substitute_at s p v)"

fun build_terms :: "nat \<Rightarrow> real \<Rightarrow> suite" where
  "build_terms 0 a = []" |
  "build_terms 1 a = [a]" |
  "build_terms 2 a = [a, k * a]" |
  "build_terms n a =
     (let s = build_terms (n - 1) a in
      if n = 3 then
        s @ [k * last s]
      else if n = 4 then
        s @ [last s * (1 / (k - 1/k))]
      else
        s @ [k * last s])"

fun next_term :: "term \<Rightarrow> term" where
  "next_term t = k * t"

definition sum_suite :: "suite \<Rightarrow> real" where
  "sum_suite s = sum_list s"

definition Rs :: real where
  "Rs = 1 / k"

definition valid_step1 :: "suite \<Rightarrow> bool" where
  "valid_step1 s \<longleftrightarrow> (sum_suite s = Rs \<and> valid_suite s)"

definition valid_stepN :: "suite \<Rightarrow> real \<Rightarrow> bool" where
  "valid_stepN s v \<longleftrightarrow> (sum_suite s = Rs - v \<and> valid_suite s)"

definition spectral_ratio :: "real \<Rightarrow> real \<Rightarrow> real" where
  "spectral_ratio a b = a / b"

lemma spectral_ratio_is_1_over_k:
  assumes "x (n+1) = k * x n" "x n \<noteq> 0"
  shows "spectral_ratio (1 / x (n+1)) (1 / x n) = 1 / k"
  using assms unfolding spectral_ratio_def
  by (simp add: field_simps)

end

end
