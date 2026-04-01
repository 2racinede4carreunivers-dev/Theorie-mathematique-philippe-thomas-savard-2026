theory espace_philippot
  imports Complex_Main
begin

section "Cotes de la pyramide selon la spirale de Theodore"

text "
  Chaque cote possede une longueur de reference Lref a la position 1^(1/2).
  La longueur a la position n^(1/2) est donnee par la formule :
     L(n) = (n * (Lref^2))^(1/2)
  Cette loi correspond a la progression de la spirale de Theodore.
"

subsection "Longueurs de reference"

definition L1_ref :: real where "L1_ref = 1.65301407"
definition L2_ref :: real where "L2_ref = 1.72784193"
definition L3_ref :: real where "L3_ref = 1.65301407"
definition L4_ref :: real where "L4_ref = 0.93780239"

subsection "Definition generale d un cote"

definition cote :: "real \<Rightarrow> nat \<Rightarrow> real"
  where
  "cote Lref n = sqrt (real n * (Lref^2))"

definition cote1 :: "nat \<Rightarrow> real"
  where "cote1 n = cote L1_ref n"

definition cote2 :: "nat \<Rightarrow> real"
  where "cote2 n = cote L2_ref n"

definition cote3 :: "nat \<Rightarrow> real"
  where "cote3 n = cote L3_ref n"

definition cote4 :: "nat \<Rightarrow> real"
  where "cote4 n = cote L4_ref n"

subsection "Propriete generale"

text "
  Nous montrons que la definition est bien la forme exacte voulue :
     cote Lref n = sqrt (real n * (Lref^2))
"

lemma cote_formule_exacte:
  "cote Lref n = sqrt (real n * (Lref^2))"
  by (simp add: cote_def)


section "Hauteurs, rayons et spirale de Theodore"

text "
  Les hauteurs de la pyramide suivent la progression de la spirale
  de Theodore de Cyrene : a l indice n correspond la valeur sqrt(real n).
"

definition hauteur :: "nat \<Rightarrow> real"
  where
  "hauteur n = sqrt (real n)"

text "
  A chaque extremite de hauteur est associe un disque dont le rayon
  suit le meme rythme, avec un facteur 1/10 et une racine supplementaire,
  selon l intuition :
    pour hauteur = (n^(1/2)), rayon = (( (n^(1/2)) / 10 ))^(1/2).
"

definition rayon :: "nat \<Rightarrow> real"
  where
  "rayon n = sqrt (hauteur n / 10)"

lemma rayon_def_simplifie:
  "rayon n = sqrt (sqrt (real n) / 10)"
  by (simp add: rayon_def hauteur_def)

text "
  La grande diagonale de la base de la pyramide, multipliee par la hauteur,
  plus le rayon, le tout divise par 2, est reliee a la somme :
    (hauteur^2) + Aire_du_disque.
  Nous axiomatisons cette relation comme une propriete caracteristique
  de la pyramide dans l Espace de Philippot.
"

axiomatization diag_base :: real and aire_disque :: real
where relation_diag_hauteur_rayon:
  "(diag_base * hauteur n + rayon n) / 2 = (hauteur n)^2 + aire_disque"


section "Nombres hypercomplexes geometriques"

text "
  Nous definissons ici trois formes de nombres hypercomplexes geometriques,
  en suivant les expressions donnees dans la description de l Espace de
  Philippot. Ils dependent de l aire d un disque A et de son rayon r.
"

type_synonym hypercomplexe = "real * real * real"

text "Premier type de nombre hypercomplexe (associe a P.2, R.2, P.5, P.7, etc.)."

definition hyper1 :: "real \<Rightarrow> real \<Rightarrow> real"
  where
  "hyper1 A r =
     sqrt ( (2 * A) + (2 * A * sqrt 10) + (r^2) )"

text "Deuxieme type (associe a P.2, P.19 et paralleles)."

definition hyper2 :: "real \<Rightarrow> real \<Rightarrow> real"
  where
  "hyper2 A r =
     sqrt ( (2.8 * A) + (2 * A * sqrt 10) + sqrt r )"

text "Troisieme type, avec correction par (2 * r^2) et un terme non lineaire en A."

definition hyper3 :: "real \<Rightarrow> real \<Rightarrow> real"
  where
  "hyper3 A r =
     sqrt ( (2 * A) / 10
          + sqrt (1 + (A - A^2))
          + (2 * (r^2)) )"

text "
  Ces trois formes hyper1, hyper2 et hyper3 representent des nombres
  hypercomplexes geometriques lies aux aires des disques et a leurs rayons.
  Leur lien detaille avec les quaternions pourra etre precise plus tard.
"


text \<open>
  Axiomatisation intuitive de la "pyramide hypercomplexe" de Philippe,
  en analogie avec les quaternions et la spirale de Théodore de Cyrène.
\<close>

typedecl event   (* type abstrait pour les événements *)
typedecl index   (* type abstrait pour indexer les disques / niveaux *)

consts
  r         :: "index \<Rightarrow> real"          (* rayon du disque à l'étage n *)
  a         :: "index \<Rightarrow> real"          (* 4 paramètres hypercomplexes *)
  b         :: "index \<Rightarrow> real"
  c         :: "index \<Rightarrow> real"
  d         :: "index \<Rightarrow> real"
  V_pyr     :: "index \<Rightarrow> real"          (* volume de la pyramide *)
  V_ell     :: "index \<Rightarrow> real"          (* volume de l'ellipsoïde associé *)
  val_geom  :: "index \<Rightarrow> real"          (* valeur géométrique caractéristique *)
  spiral_pos :: "index \<Rightarrow> event \<Rightarrow> real \<times> real \<times> real"
    (* position d'un événement sur la spirale (espace-temps abstrait) *)


text \<open>
  Axiomes globaux liant spirale, valeurs géométriques, norme hypercomplexe,
  rapport de volumes et position des événements.
\<close>

axiomatization where

  spiral_Theodore:
    "\<exists>f :: nat \<Rightarrow> index. \<forall>n. r (f n) = sqrt (real n)" and

  val_geom_form:
    "\<exists>u v :: index \<Rightarrow> real. \<forall>n. val_geom n = sqrt (u n) + v n" and

  hypercomplex_norm:
    "\<exists>N :: (real \<times> real \<times> real \<times> real) \<Rightarrow> real.
       \<forall>n. N (a n, b n, c n, d n) =
             sqrt ((a n)^2 + (b n)^2 + (c n)^2 + (d n)^2)" and

  volume_ratio:
    "\<forall>n. V_ell n = 10 * V_pyr n" and

  events_on_spiral:
    "\<exists>F :: (real \<times> real \<times> real \<times> real) \<Rightarrow> event \<Rightarrow> real \<times> real \<times> real.
       \<forall>n e. spiral_pos n e = F (a n, b n, c n, d n) e"

end
