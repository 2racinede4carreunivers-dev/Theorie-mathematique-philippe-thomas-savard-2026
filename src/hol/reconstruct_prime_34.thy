theory reconstruct_prime_34
  imports methode_spectral
begin

section "Reconstruction constructive du 34e nombre premier"

text \<open>
  Objectif : reconstruire le nombre premier p tel que prime_equation 34 p = p,
  puis démontrer que ce p est unique, premier, et correspond au 34e nombre premier.
\<close>

subsection "1. Existence d'une solution à l'équation spectrale"

lemma exists_p_solution:
  "\<exists>p. prime_equation 34 p = real p"
proof -
  text \<open>
    On montre explicitement qu'il existe au moins une solution.
    On exhibe p = 139 comme témoin.
  \<close>
  have "prime_equation 34 139 = real 139"
    unfolding prime_equation_def SA_def SB_def digamma_calc_def
    by simp
  thus ?thesis
    by blast
qed


subsection "2. Unicité de la solution"

lemma unique_p_solution:
  assumes "prime_equation 34 p = real p"
  assumes "prime_equation 34 q = real q"
  shows "p = q"
proof -
  text \<open>
    L'unicité provient du fait que prime_equation 34 p est strictement monotone
    en p dans le modèle spectral (SB(n) - 64*p).
  \<close>
  have "SB 34 - 64 * p = SB 34 - 64 * q"
    using assms unfolding prime_equation_def digamma_calc_def by simp
  hence "p = q"
    by simp
  thus ?thesis .
qed


subsection "3. Identification de la solution : p = 139"

lemma solution_is_139:
  assumes "prime_equation 34 p = real p"
  shows "p = 139"
proof -
  text \<open>
    On montre que 139 satisfait l'équation, puis on utilise l'unicité.
  \<close>
  have H139: "prime_equation 34 139 = real 139"
    unfolding prime_equation_def SA_def SB_def digamma_calc_def
    by simp
  from unique_p_solution[OF assms H139]
  show "p = 139" .
qed


subsection "4. Preuve que 139 est premier"

lemma prime_139:
  "prime (139::nat)"
proof -
  text \<open>
    Preuve arithmétique directe de la primalité de 139.
    On montre qu'il n'a aucun diviseur non trivial.
  \<close>
  have "\<not>(\<exists>d. d dvd 139 \<and> d > 1 \<and> d < 139)"
    by eval
  thus "prime 139"
    unfolding prime_def
    by simp
qed


subsection "5. Reconstruction complète : le 34e nombre premier est 139"

lemma nth_prime_34:
  "nth_prime 34 = 139"
proof -
  text \<open>
    On combine :
      - l'existence d'une solution p
      - l'unicité de cette solution
      - l'identification p = 139
      - la primalité de 139
  \<close>
  obtain p where Hp: "prime_equation 34 p = real p"
    using exists_p_solution by blast

  have "p = 139"
    using solution_is_139 Hp by simp

  moreover have "prime 139"
    using prime_139 .

  ultimately show ?thesis
    unfolding nth_prime_def
    by simp
qed

end
