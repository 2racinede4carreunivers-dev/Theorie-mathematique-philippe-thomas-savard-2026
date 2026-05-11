theory fonction_zeta_philippot
  imports Complex_Main
begin

(****************************************************************)
(*  BLOC 1 : DEFINITIONS                                         *)
(****************************************************************)

(*
  Definition 1 :
  Sa(n) represente la somme spectrale de la suite A pour un entier n strictement positif.
  Cette somme correspond a la formule generale (3.25/2) * 2^n - 2.
  Elle represente la somme totale des n termes de la suite A.
*)
definition Sa :: "nat => real" where
  "Sa n = (3.25 / 2) * (2 ^ n) - 2"

(*
  Definition 2 :
  Sb(n) represente la somme spectrale de la suite B pour un entier n strictement positif.
  Cette somme correspond a la formule generale (6.5/2) * 2^n - 66.
  Elle represente la somme totale des n termes de la suite B.
*)
definition Sb :: "nat => real" where
  "Sb n = (6.5 / 2) * (2 ^ n) - 66"


(*
  Definition 3 :
  termeA(k) represente le k-ieme terme individuel de la suite A.
  Les termes ta(k) s additionnent pour former Sa(n).
*)
definition termeA :: "nat => real" where
  "termeA k = undefined"

(*
  Definition 4 :
  termeB(k) represente le k-ieme terme individuel de la suite B.
  Les termes tb(k) s additionnent pour former Sb(n).
*)
definition termeB :: "nat => real" where
  "termeB k = undefined"


(*
  Definition 5 :
  cas_1_7(n) indique que la suite possede entre 1 et 7 termes.
  C est le premier regime structurel de la methode spectrale.
*)
definition cas_1_7 :: "nat => bool" where
  "cas_1_7 n = (n >= 1 & n <= 7)"

(*
  Definition 6 :
  cas_8_inf(n) indique que la suite possede 8 termes ou plus.
  C est le second regime structurel de la methode spectrale.
*)
definition cas_8_inf :: "nat => bool" where
  "cas_8_inf n = (n >= 8)"


(*
  Definition 7 :
  Sa_1_7(n) represente la somme de la suite A dans le cas 1 a 7 termes.
  Cette valeur est identique a Sa(n), mais separee pour distinguer les deux regimes.
*)
definition Sa_1_7 :: "nat => real" where
  "Sa_1_7 n = Sa n"

(*
  Definition 8 :
  Sb_1_7(n) represente la somme de la suite B dans le cas 1 a 7 termes.
  Cette valeur est identique a Sb(n), mais separee pour distinguer les deux regimes.
*)
definition Sb_1_7 :: "nat => real" where
  "Sb_1_7 n = Sb n"


(*
  Definition 9 :
  resteA1 represente la partie soustraite dans le cas 1 terme de la suite A.
  Le sens correct est : 2 - (1/2 + 1/4).
*)
definition resteA1 :: real where
  "resteA1 = (2 - (1/2 + 1/4))"

(*
  Definition 10 :
  resteA2 represente la partie soustraite dans le cas 2 termes de la suite A.
  Le sens correct est : (2 + 3) - (1/2).
*)
definition resteA2 :: real where
  "resteA2 = ((2 + 3) - (1/2))"


(*
  Definition 11 :
  avant_dernierA(t) represente la regle generale de l avant dernier terme
  pour les suites A, sauf pour les cas 1 terme et 2 termes.
  La regle est : t * (2 - 2^(-1)).
*)
definition avant_dernierA :: "real => real" where
  "avant_dernierA t = t * (2 - 2 powr -1)"

(*
  Definition 12 :
  dernierA(t) represente le dernier terme de la suite A,
  sauf pour les cas 1 terme et 2 termes.
  La regle est : 2 * avant_dernierA.
*)
definition dernierA :: "real => real" where
  "dernierA t = 2 * t"


(*
  Definition 13 :
  sommeB_1_7(n) represente la somme des termes tb(1) a tb(7) pour la suite B.
  Dans ce regime, la somme est identique a Sb(n).
*)
definition sommeB_1_7 :: "nat => real" where
  "sommeB_1_7 n = Sb n"


(*
  Definition 14 :
  substitution_B(t) represente la substitution fixe de la suite B.
  Cette substitution se trouve toujours a la position 6.
  Elle correspond au 7eme terme de la suite A.
*)
definition substitution_B :: "real => real" where
  "substitution_B t = t"

(*
  Definition 15 :
  progressionA(t) represente la regle de progression des termes de la suite A.
  Chaque terme suivant vaut t * 2.
*)
definition progressionA :: "real => real" where
  "progressionA t = 2 * t"

(*
  Definition 16 :
  progressionB(t) represente la regle de progression des termes de la suite B
  pour les termes 1 a 5 avant la substitution.
  Chaque terme suivant vaut t * 2.
*)
definition progressionB :: "real => real" where
  "progressionB t = 2 * t"


(*
  Definition 17 :
  avant_dernier(t) represente la regle generale de l avant dernier terme
  pour les suites A et B dans le cas n >= 8.
  Cette regle est la meme que celle definie pour avant_dernierA.
*)
definition avant_dernier :: "real => real" where
  "avant_dernier t = t * (2 - 2 powr -1)"

(*
  Definition 18 :
  dernier(t) represente le dernier terme des suites A et B dans le cas n >= 8.
  Ce terme est nomme dernier_general.
  Il vaut toujours 2 * avant_dernier.
*)
definition dernier :: "real => real" where
  "dernier t = 2 * t"

(*
  Definition 19 :
  somme_spectrale(L) represente la somme totale des termes d une suite.
  Cette somme correspond a RsSa ou RsSb selon le cas.
*)
definition somme_spectrale :: "real list => real" where
  "somme_spectrale L = (SUM x <- L. x)"


(*
  Definition 20 :
  progression_double(t) represente la regle de croissance par multiplication par 2.
  Pour la suite A : tous les termes sauf exceptions suivent t * 2.
  Pour la suite B :
    - les termes 1 a 5 suivent t * 2
    - la position 6 est la substitution
    - la position 7 correspond au terme 8 de A
    - la position 8 correspond au terme 9 de A
    - et ainsi de suite jusqu a l avant dernier terme.
*)
definition progression_double :: "real => real" where
  "progression_double t = 2 * t"


(*
  Definition 21 :
  zeta_substitution(tA7) represente la substitution Zeta de la suite B.
  Cette substitution est toujours placee a la position 6.
  Elle correspond exactement au 7eme terme de la suite A.
*)
definition zeta_substitution :: "real => real" where
  "zeta_substitution tA7 = tA7"


(*
  Definition 22 :
  decalage_BA(k, tA) represente la regle de decalage entre les suites A et B
  a partir du 7eme terme.
  Exemple :
    7eme terme B = 8eme terme A
    8eme terme B = 9eme terme A
    9eme terme B = 10eme terme A
  Ce decalage continue jusqu a l avant dernier terme.
*)
definition decalage_BA :: "nat => real => real" where
  "decalage_BA k tA = tA"


(*
  Definition : somme_liste
  Cette fonction calcule la somme de tous les elements d une liste de reels.
  Elle sert a verifier les sommes des suites A et B dans les exemples.
*)
definition somme_liste :: "real list => real" where
  "somme_liste L = (SUM x <- L. x)"


(*
  Liste des suites A pour 1 a 7 termes.
  Ces listes correspondent aux exemples explicites de la methode spectrale.
*)
definition A1 :: "real list" where
  "A1 = [2]"

definition A2 :: "real list" where
  "A2 = [2, 3]"

definition A3 :: "real list" where
  "A3 = [2, 3, 6]"

definition A4 :: "real list" where
  "A4 = [2, 4, 6, 12]"

definition A5 :: "real list" where
  "A5 = [2, 4, 8, 12, 24]"

definition A6 :: "real list" where
  "A6 = [2, 4, 8, 16, 24, 48]"

definition A7 :: "real list" where
  "A7 = [2, 4, 8, 16, 32, 48, 96]"


(*
  Liste des suites A pour 8 termes et plus.
  Ces listes suivent la regle generale de la methode spectrale.
*)
definition A8 :: "real list" where
  "A8 = [2, 4, 8, 16, 32, 64, 96, 192]"

definition A9 :: "real list" where
  "A9 = [2, 4, 8, 16, 32, 64, 128, 192, 384]"

definition A10 :: "real list" where
  "A10 = [2, 4, 8, 16, 32, 64, 128, 256, 384, 768]"

definition A11 :: "real list" where
  "A11 = [2, 4, 8, 16, 32, 64, 128, 256, 512, 768, 1536]"

definition A12 :: "real list" where
  "A12 = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 1536, 3072]"

definition A13 :: "real list" where
  "A13 = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 3072, 6144]"


(*
  Liste des suites B pour 1 a 7 termes.
  Ces suites correspondent aux exemples explicites de la methode spectrale.
*)
definition B1 :: "real list" where
  "B1 = [-59.5]"

definition B2 :: "real list" where
  "B2 = [-59.5, 6.5]"

definition B3 :: "real list" where
  "B3 = [-59.5, 6.5, 13]"

definition B4 :: "real list" where
  "B4 = [-59.5, 6.5, 13, 26]"

definition B5 :: "real list" where
  "B5 = [-59.5, 6.5, 13, 26, 52]"

definition B6 :: "real list" where
  "B6 = [-59.5, 6.5, 13, 26, 52, 104]"

definition B7 :: "real list" where
  "B7 = [-59.5, 6.5, 13, 26, 52, 104, 208]"


(*
  Liste des suites B pour 8 termes et plus.
  Ces listes suivent la regle generale incluant la substitution.
*)
definition B8 :: "real list" where
  "B8 = [2, 4, 8, 16, 32, 128, 192, 384]"

definition B9 :: "real list" where
  "B9 = [2, 4, 8, 16, 32, 128, 256, 384, 768]"

definition B10 :: "real list" where
  "B10 = [2, 4, 8, 16, 32, 128, 256, 512, 768, 1536]"

definition B11 :: "real list" where
  "B11 = [2, 4, 8, 16, 32, 128, 256, 512, 1024, 1536, 3072]"

definition B12 :: "real list" where
  "B12 = [2, 4, 8, 16, 32, 128, 256, 512, 1024, 2048, 3072, 6144]"

definition B13 :: "real list" where
  "B13 = [2, 4, 8, 16, 32, 128, 256, 512, 1024, 2048, 4096, 6144, 12288]"


definition Z :: real where
  "Z = 64"

definition D :: "nat \<Rightarrow> real \<Rightarrow> real" where
  "D n P = Sb n - Sa n - Z * P"

definition Dc :: "nat \<Rightarrow> real \<Rightarrow> real" where
  "Dc n P = Sa n + D n P"

definition P_reconstruit :: "nat \<Rightarrow> real \<Rightarrow> real" where
  "P_reconstruit n P = (Sb n - Dc n P) / Z"

(****************************************************************)
(*  BLOC 2 : LEMMES (EXEMPLES ET SOMMES)                         *)
(****************************************************************)

(*
  Exemple A1 :
  Cette liste contient 1 terme.
  1 terme correspond au 1er nombre premier.
  Le 1er nombre premier est 2.
*)
lemma somme_A1_2:
  "somme_liste A1 = 2"
  unfolding somme_liste_def A1_def by simp


(*
  Exemple A2 :
  Cette liste contient 2 termes.
  2 termes correspondent au 2e nombre premier.
  Le 2e nombre premier est 3.
*)
lemma somme_A2_3:
  "somme_liste A2 = 2 + 3"
  unfolding somme_liste_def A2_def by simp


(*
  Exemple A3 :
  Cette liste contient 3 termes.
  3 termes correspondent au 3e nombre premier.
  Le 3e nombre premier est 5.
*)
lemma somme_A3_5:
  "somme_liste A3 = 2 + 3 + 6"
  unfolding somme_liste_def A3_def by simp


(*
  Exemple A4 :
  Cette liste contient 4 termes.
  4 termes correspondent au 4e nombre premier.
  Le 4e nombre premier est 7.
*)
lemma somme_A4_7:
  "somme_liste A4 = 2 + 4 + 6 + 12"
  unfolding somme_liste_def A4_def by simp


(*
  Exemple A5 :
  Cette liste contient 5 termes.
  5 termes correspondent au 5e nombre premier.
  Le 5e nombre premier est 11.
*)
lemma somme_A5_11:
  "somme_liste A5 = 2 + 4 + 8 + 12 + 24"
  unfolding somme_liste_def A5_def by simp


(*
  Exemple A6 :
  Cette liste contient 6 termes.
  6 termes correspondent au 6e nombre premier.
  Le 6e nombre premier est 13.
*)
lemma somme_A6_13:
  "somme_liste A6 = 2 + 4 + 8 + 16 + 24 + 48"
  unfolding somme_liste_def A6_def by simp


(*
  Exemple A7 :
  Cette liste contient 7 termes.
  7 termes correspondent au 7e nombre premier.
  Le 7e nombre premier est 17.
*)
lemma somme_A7_17:
  "somme_liste A7 = 2 + 4 + 8 + 16 + 32 + 48 + 96"
  unfolding somme_liste_def A7_def by simp

(****************************************************************)
(*  BLOC 2 : LEMMES (EXEMPLES ET SOMMES suite B)                         *)
(****************************************************************)

(*
  Exemple B1 :
  Cette liste contient 1 terme.
  1 terme correspond au 1er nombre premier.
  Le 1er nombre premier est 2.
*)
lemma somme_B1_2:
  "somme_liste B1 = -59.5"
  unfolding somme_liste_def B1_def by simp


(*
  Exemple B2 :
  Cette liste contient 2 termes.
  2 termes correspondent au 2e nombre premier.
  Le 2e nombre premier est 3.
*)
lemma somme_B2_3:
  "somme_liste B2 = -59.5 + 6.5"
  unfolding somme_liste_def B2_def by simp


(*
  Exemple B3 :
  Cette liste contient 3 termes.
  3 termes correspondent au 3e nombre premier.
  Le 3e nombre premier est 5.
*)
lemma somme_B3_5:
  "somme_liste B3 = -59.5 + 6.5 + 13"
  unfolding somme_liste_def B3_def by simp


(*
  Exemple B4 :
  Cette liste contient 4 termes.
  4 termes correspondent au 4e nombre premier.
  Le 4e nombre premier est 7.
*)
lemma somme_B4_7:
  "somme_liste B4 = -59.5 + 6.5 + 13 + 26"
  unfolding somme_liste_def B4_def by simp


(*
  Exemple B5 :
  Cette liste contient 5 termes.
  5 termes correspondent au 5e nombre premier.
  Le 5e nombre premier est 11.
*)
lemma somme_B5_11:
  "somme_liste B5 = -59.5 + 6.5 + 13 + 26 + 52"
  unfolding somme_liste_def B5_def by simp


(*
  Exemple B6 :
  Cette liste contient 6 termes.
  6 termes correspondent au 6e nombre premier.
  Le 6e nombre premier est 13.
*)
lemma somme_B6_13:
  "somme_liste B6 = -59.5 + 6.5 + 13 + 26 + 52 + 104"
  unfolding somme_liste_def B6_def by simp


(*
  Exemple B7 :
  Cette liste contient 7 termes.
  7 termes correspondent au 7e nombre premier.
  Le 7e nombre premier est 17.
*)
lemma somme_B7_17:
  "somme_liste B7 = -59.5 + 6.5 + 13 + 26 + 52 + 104 + 208"
  unfolding somme_liste_def B7_def by simp



(*
  Exemple A9 :
  Cette liste contient 9 termes.
  9 termes correspondent au 9e nombre premier.
  Le 9e nombre premier est 23.
*)
lemma somme_A9_23:
  "somme_liste A9 = 2 + 4 + 8 + 16 + 32 + 64 + 128 + 192 + 384"
  unfolding somme_liste_def A9_def by simp


(*
  Exemple A10 :
  Cette liste contient 10 termes.
  10 termes correspondent au 10e nombre premier.
  Le 10e nombre premier est 29.
*)
lemma somme_A10_29:
  "somme_liste A10 = 2 + 4 + 8 + 16 + 32 + 64 + 128 + 256 + 384 + 768"
  unfolding somme_liste_def A10_def by simp


(*
  Exemple A11 :
  Cette liste contient 11 termes.
  11 termes correspondent au 11e nombre premier.
  Le 11e nombre premier est 31.
*)
lemma somme_A11_31:
  "somme_liste A11 = 2 + 4 + 8 + 16 + 32 + 64 + 128 + 256 + 512 + 768 + 1536"
  unfolding somme_liste_def A11_def by simp

(*
  Exemple A12 :
  Cette liste contient 12 termes.
  12 termes correspondent au 12e nombre premier.
  Le 12e nombre premier est 37.
*)
lemma somme_A12_37:
  "somme_liste A12 =
     (2 + 4 + 8 + 16 + 32 + 64 + 128 + 256 + 512 + 1024 + 1536 + 3072)"
  unfolding somme_liste_def A12_def by simp


(*
  Exemple A13 :
  Cette liste contient 13 termes.
  13 termes correspondent au 13e nombre premier.
  Le 13e nombre premier est 41.
*)

lemma reconstruction_P:
  fixes n :: nat
  fixes P :: real
  shows "P_reconstruit n P = P"
proof -
  have "P_reconstruit n P =
        (Sb n - (Sa n + (Sb n - Sa n - Z * P))) / Z"
    unfolding P_reconstruit_def Dc_def D_def by simp
  also have "... = (Sb n - Sa n - Sb n + Sa n + Z * P) / Z"
    by simp
  also have "... = (Z * P) / Z"
    by simp
  also have "... = P"
    unfolding Z_def by simp
  finally show ?thesis .
qed

definition Premier_spectral :: "nat \<Rightarrow> real \<Rightarrow> real" where
  "Premier_spectral n Dg = (Sb n - Dg) / Z"

lemma digamma_is:
  fixes n :: nat
  fixes P :: real
  fixes Dg :: real
  assumes "Premier_spectral n Dg = P"
  shows "Dg = Sb n - P * Z"
proof -
  have "(Sb n - Dg) / Z = P"
    using assms unfolding Premier_spectral_def by simp
  hence "Sb n - Dg = P * Z"
    unfolding Z_def by (simp add: field_simps)
  hence "Dg = Sb n - P * Z"
    by simp
  thus ?thesis .
qed

end