theory Philippot_Method
  imports Complex_Main
begin

text "
  Methode de Philippot - Exemple complet pour 4 termes et 3 etapes.

  On considere un rapport spectral 1/k avec k > 1, k ~= 0, k ~= -1.
  La valeur de reference Rs est definie par :


    Rs = 1 / (k - 1)

  Pour 4 termes, les trois etapes sont definies comme suit :


    Etape 1 (4 termes) :
      S1 k = 1/k^1 + 1/k^2 + 1/(k^3 - k^1) + 1/(k^4 - k^2)
           = Rs

    Etape 2 (4 termes) :
      S2 k = 1/k^1 + 1/k^3 + 1/(k^4 - k^2) + 1/(k^5 - k^3)
           = Rs - 1/k^2

    Etape 3 (4 termes) :
      S3 k = 1/k^1 + 1/k^4 + 1/(k^5 - k^3) + 1/(k^6 - k^4)
           = Rs - (1/k^2 + 1/k^3)

  Le rapport entre les termes substitues a l'etape 3 est :

      (1/k^3) / (1/k^2) = 1/k

  Ce rapport est interprete comme le rapport spectral 1/k = 1/x^1.

  Pour les suites de 3 a 7 termes, la position de substitution a partir
  de l'etape 2 est definie ainsi :

    - 3 termes : position 1
    - 4 termes : position 2
    - 5 termes : position 3
    - 6 termes : position 4
    - 7 termes : position 5

  Cette position est toujours egale a n - 2 pour une suite de longueur n.

  L'avant-dernier terme joue un role particulier : dans la methode de
  Philippot, il est en relation avec le terme qui le precede via un
  facteur (k - 1)/k, ce qui sera generalise par la suite.
"

locale philippot_4terms =
  fixes k :: real
  assumes k_gt1: "k > 1"
      and k_neq0: "k ~= 0"
      and k_neqm1: "k ~= -1"
begin

definition Rs :: real where
  "Rs = 1 / (k - 1)"

definition S1 :: real where
  "S1 = 1 / k
      + 1 / (k^2)
      + 1 / (k^3 - k)
      + 1 / (k^4 - k^2)"

definition S2 :: real where
  "S2 = 1 / k
      + 1 / (k^3)
      + 1 / (k^4 - k^2)
      + 1 / (k^5 - k^3)"

definition S3 :: real where
  "S3 = 1 / k
      + 1 / (k^4)
      + 1 / (k^5 - k^3)
      + 1 / (k^6 - k^4)"

text "
  Rs est la valeur de reference de l'etape 1.
  S1, S2 et S3 representent respectivement les sommes des etapes 1, 2 et 3
  pour le cas a 4 termes.

  Les egalites suivantes sont conceptuellement vraies dans la methode
  de Philippot :

    S1 = Rs
    S2 = Rs - 1 / (k^2)
    S3 = Rs - (1 / (k^2) + 1 / (k^3))

  Elles ne sont pas formalisees ici comme des lemmes prouvables, mais
  comme des relations definitoires de la methode.
"

text "
  Le rapport entre les termes substitues a l'etape 3 est :

    (1/k^3) / (1/k^2) = 1/k

  Ce qui confirme le rapport spectral 1/k.
"

end  (* fin de la locale philippot_4terms *)

text "
  Definition generale de la position de substitution pour les suites
  de 3 a 7 termes.
"

definition substitution_position :: "nat => nat" where
  "substitution_position n =
     (if n = 3 then 1
      else if n = 4 then 2
      else if n = 5 then 3
      else if n = 6 then 4
      else if n = 7 then 5
      else 0)"

lemma substitution_positions_correct:
  shows "substitution_position 3 = 1"
    and "substitution_position 4 = 2"
    and "substitution_position 5 = 3"
    and "substitution_position 6 = 4"
    and "substitution_position 7 = 5"
  by (simp_all add: substitution_position_def)

text "
  Ce lemme formalise la regle de substitution de la methode de Philippot :
    - pour 3 termes, la position de substitution est 1
    - pour 4 termes, la position de substitution est 2
    - pour 5 termes, la position de substitution est 3
    - pour 6 termes, la position de substitution est 4
    - pour 7 termes, la position de substitution est 5

  Ce schema sera utilise pour generaliser la methode a toutes les suites
  de 3 a 7 termes et a toutes les etapes.
"
locale philippot_3terms =
  fixes k :: real
  assumes k_gt1: "k > 1"
      and k_neq0: "k ~= 0"
      and k_neqm1: "k ~= -1"
begin

definition Rs :: real where
  "Rs = 1 / (k - 1)"

definition S1_3 :: real where
  "S1_3 =
     1 / (k^1)
   + 1 / (k^2 - k^0)
   + 1 / (k^3 - k^1)"

definition S2_3 :: real where
  "S2_3 =
     1 / (k^2)
   + 1 / (k^3 - k^1)
   + 1 / (k^4 - k^2)"

definition S3_3 :: real where
  "S3_3 =
     1 / (k^3)
   + 1 / (k^4 - k^2)
   + 1 / (k^5 - k^3)"

text "
  Cas 3 termes, 3 etapes.

  Etape 1 (3 termes) :
    1/x^1 + 1/(x^2 - x^0) + 1/(x^3 - x^1) = 1/(k - 1) = Rs

  Etape 2 (3 termes) :
    1/x^2 + 1/(x^3 - x^1) + 1/(x^4 - x^2)
      = 1/(k - 1) - 1/x^1

  Etape 3 (3 termes) :
    1/x^3 + 1/(x^4 - x^2) + 1/(x^5 - x^3)
      = 1/(k - 1) - (1/x^1 + 1/x^2)

  Ces egalites sont definitoires de la methode pour 3 termes.

  Rapport spectral :
    (1/x^2) / (1/x^1) = 1/k
    et 1/k = 1/x^1.
"

end  (* fin locale philippot_3terms *)


locale philippot_5terms =
  fixes k :: real
  assumes k_gt1: "k > 1"
      and k_neq0: "k ~= 0"
      and k_neqm1: "k ~= -1"
begin

definition Rs :: real where
  "Rs = 1 / (k - 1)"

definition S1_5 :: real where
  "S1_5 =
     1 / (k^1)
   + 1 / (k^2)
   + 1 / (k^3)
   + 1 / (k^4 - k^2)
   + 1 / (k^5 - k^3)"

definition S2_5 :: real where
  "S2_5 =
     1 / (k^1)
   + 1 / (k^2)
   + 1 / (k^4)
   + 1 / (k^5 - k^3)
   + 1 / (k^6 - k^4)"

definition S3_5 :: real where
  "S3_5 =
     1 / (k^1)
   + 1 / (k^2)
   + 1 / (k^5)
   + 1 / (k^6 - k^4)
   + 1 / (k^7 - k^5)"

text "
  Cas 5 termes, 3 etapes.

  Etape 1 (5 termes) :
    1/x^1 + 1/x^2 + 1/x^3 + 1/(x^4 - x^2) + 1/(x^5 - x^3)
      = 1/(k - 1) = Rs

  Etape 2 (5 termes) :
    1/x^1 + 1/x^2 + 1/x^4 + 1/(x^5 - x^3) + 1/(x^6 - x^4)
      = 1/(k - 1) - 1/x^3

  Etape 3 (5 termes) :
    1/x^1 + 1/x^2 + 1/x^5 + 1/(x^6 - x^4) + 1/(x^7 - x^5)
      = 1/(k - 1) - (1/x^3 + 1/x^4)

  Rapport spectral a l'etape 3 :
    (1/x^4) / (1/x^3) = 1/k
    et 1/k = 1/x^1.
"

end  (* fin locale philippot_5terms *)


locale philippot_6terms =
  fixes k :: real
  assumes k_gt1: "k > 1"
      and k_neq0: "k ~= 0"
      and k_neqm1: "k ~= -1"
begin

definition Rs :: real where
  "Rs = 1 / (k - 1)"

definition S1_6 :: real where
  "S1_6 =
     1 / (k^1)
   + 1 / (k^2)
   + 1 / (k^3)
   + 1 / (k^4)
   + 1 / (k^5 - k^3)
   + 1 / (k^6 - k^4)"

definition S2_6 :: real where
  "S2_6 =
     1 / (k^1)
   + 1 / (k^2)
   + 1 / (k^3)
   + 1 / (k^5)
   + 1 / (k^6 - k^4)
   + 1 / (k^7 - k^5)"

definition S3_6 :: real where
  "S3_6 =
     1 / (k^1)
   + 1 / (k^2)
   + 1 / (k^3)
   + 1 / (k^6)
   + 1 / (k^7 - k^5)
   + 1 / (k^8 - k^6)"

text "
  Cas 6 termes, 3 etapes.

  Etape 1 (6 termes) :
    1/x^1 + 1/x^2 + 1/x^3 + 1/x^4
      + 1/(x^5 - x^3) + 1/(x^6 - x^4)
      = 1/(k - 1) = Rs

  Etape 2 (6 termes) :
    1/x^1 + 1/x^2 + 1/x^3 + 1/x^5
      + 1/(x^6 - x^4) + 1/(x^7 - x^5)
      = 1/(k - 1) - 1/x^4

  Etape 3 (6 termes) :
    1/x^1 + 1/x^2 + 1/x^3 + 1/x^6
      + 1/(x^7 - x^5) + 1/(x^8 - x^6)
      = 1/(k - 1) - (1/x^4 + 1/x^5)

  Rapport spectral a l'etape 3 :
    (1/x^5) / (1/x^4) = 1/k
    et 1/k = 1/x^1.
"

end  (* fin locale philippot_6terms *)


locale philippot_7terms =
  fixes k :: real
  assumes k_gt1: "k > 1"
      and k_neq0: "k ~= 0"
      and k_neqm1: "k ~= -1"
begin

definition Rs :: real where
  "Rs = 1 / (k - 1)"

definition S1_7 :: real where
  "S1_7 =
     1 / (k^1)
   + 1 / (k^2)
   + 1 / (k^3)
   + 1 / (k^4)
   + 1 / (k^5)
   + 1 / (k^6 - k^4)
   + 1 / (k^7 - k^5)"

definition S2_7 :: real where
  "S2_7 =
     1 / (k^1)
   + 1 / (k^2)
   + 1 / (k^3)
   + 1 / (k^4)
   + 1 / (k^6)
   + 1 / (k^7 - k^5)
   + 1 / (k^8 - k^6)"

definition S3_7 :: real where
  "S3_7 =
     1 / (k^1)
   + 1 / (k^2)
   + 1 / (k^3)
   + 1 / (k^4)
   + 1 / (k^7)
   + 1 / (k^8 - k^6)
   + 1 / (k^9 - k^7)"

text "
  Cas 7 termes, 3 etapes.

  Etape 1 (7 termes) :
    1/x^1 + 1/x^2 + 1/x^3 + 1/x^4 + 1/x^5
      + 1/(x^6 - x^4) + 1/(x^7 - x^5)
      = 1/(k - 1) = Rs

  Etape 2 (7 termes) :
    1/x^1 + 1/x^2 + 1/x^3 + 1/x^4 + 1/x^6
      + 1/(x^7 - x^5) + 1/(x^8 - x^6)
      = 1/(k - 1) - 1/x^5

  Etape 3 (7 termes) :
    1/x^1 + 1/x^2 + 1/x^3 + 1/x^4 + 1/x^7
      + 1/(x^8 - x^6) + 1/(x^9 - x^7)
      = 1/(k - 1) - (1/x^5 + 1/x^6)

  Rapport spectral a l'etape 3 :
    (1/x^6) / (1/x^5) = 1/k
    et 1/k = 1/x^1.
"

end  (* fin locale philippot_7terms *)
text "
  Definition abstraite d'un denominateur commun pour la methode de Philippot.

  Pour chaque longueur n entre 3 et 7, pour chaque etape step (naturel),
  et pour chaque k > 1, on postule l'existence d'un denominateur commun
  D(k,n,step) tel que la somme de la suite a l'etape step puisse
  s'ecrire comme un quotient N(k,n,step) / D(k,n,step).

  La methode de Philippot impose alors une forme particuliere pour
  N(k,n,step), en fonction de Rs = 1/(k-1) et des termes de substitution.
"

locale philippot_general =
  fixes k   :: real
    and len :: nat
    and step :: nat
    and D :: "real \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real"   (* denominateur commun abstrait *)
    and N :: "real \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real"   (* numerateur abstrait *)
  assumes k_gt1: "k > 1"
      and k_neq0: "k \<noteq> 0"
      and k_neqm1: "k \<noteq> -1"
      and len_range: "3 \<le> len" "len \<le> 7"
begin

definition Rs :: real where
  "Rs = 1 / (k - 1)"

text "
  D(k,len,step) represente un denominateur commun abstrait pour la
  suite de longueur len a l'etape step, pour le rapport 1/k.

  On suppose que la somme de la suite a l'etape step peut s'ecrire
  sous la forme :

      somme(len, step, k) = N k len step / D k len step

  et que la methode de Philippot impose, pour les trois premieres
  etapes, les formes suivantes du numerateur :

    step = 1 : N k len 1 / D k len 1 = Rs
    step = 2 : N k len 2 / D k len 2 = Rs - (un terme)
    step = 3 : N k len 3 / D k len 3 = Rs - (deux termes)

  Les cas particuliers len = 3,4,5,6,7 et step = 1,2,3 sont deja
  explicitement definis dans les locales specialisees
  philippot_3terms, philippot_4terms, philippot_5terms, etc.
"
text "
  Exemple pour les suites de 8 termes et plus (etape 1) :

    1/x^1 + 1/x^2 + 1/x^3 + 1/x^4 + 1/x^5 + 1/x^6
    + 1/(x^7 - x^5) + 1/(x^8 - x^6)
    = Rs

  Cet exemple illustre que l'etape 1 pour les suites de longueur >= 8
  suit le meme motif general que pour les suites de 4 a 7 termes.
  Aucune regle speciale n'est requise pour l'etape 1.

"

end

locale philippot_len_ge8 =
  fixes k :: real
    and len :: nat
    and step :: nat
  assumes k_gt1: "k > 1"
      and k_neq0: "k \<noteq> 0"
      and k_neqm1: "k \<noteq> -1"
      and len_ge8: "len \<ge> 8"
begin


text "
  Pour toutes les suites de longueur >= 8, la methode de Philippot
  impose que la position de substitution a l'etape 2 et aux etapes
  suivantes est toujours la position 6.

  Cela signifie :

    - Etape 1 : aucune substitution
    - Etape 2 : substitution du terme 1/x^6
    - Etape 3 : substitution des termes 1/x^6 et 1/x^7
    - Etape 4 : substitution des termes 1/x^6, 1/x^7, 1/x^8
    - etc.

  Cette regle est independante de la longueur exacte de la suite,
  tant que len >= 8.
"

definition substitution_position :: nat where
  "substitution_position = 6"

text "
  Exemple concret pour len = 8 :

  Etape 1 :
    1/x^1 + 1/x^2 + 1/x^3 + 1/x^4 + 1/x^5 + 1/x^6
    + 1/(x^7 - x^5) + 1/(x^8 - x^6)
    = Rs

  Etape 2 :
    1/x^1 + 1/x^2 + 1/x^3 + 1/x^4 + 1/x^5 + 1/x^7
    + 1/(x^8 - x^6) + 1/(x^9 - x^7)
    = Rs - 1/x^6

  Ces exemples illustrent la regle generale pour toutes les suites
  de longueur >= 8.
"

text "
  Rapport spectral general pour len >= 8 :

  A partir de l'etape 3 et pour toutes les etapes suivantes (step >= 3),
  le rapport spectral entre les deux termes substitues consecutifs
  demeure constant et egal a 1/k.

  Plus precisement :

      (1/x^(6 + (step - 2))) / (1/x^(5 + (step - 2))) = 1/k

  puisque la methode impose que :

      x^(n+1) = k * x^n
      et donc 1/x^(n+1) = (1/k) * 1/x^n.

  Ainsi, le rapport spectral reste invariant et vaut toujours 1/k
  pour toutes les etapes step >= 3, independamment de la longueur
  exacte de la suite tant que len >= 8.
"


end



end
