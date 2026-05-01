theory geometrie_spectre_premier
  imports Complex_Main
begin

text "Formalisation de base de la methode spectrale (rapport 1/2)."

definition Z :: real where
  "Z = 64"

definition SA :: "nat => real" where
  "SA n = (3.25 / 2) * (2 ^ n) - 2"

definition SB :: "nat => real" where
  "SB n = (6.5 / 2) * (2 ^ n) - 66"

definition D :: "nat => real => real" where
  "D n P = SB n - SA n - Z * P"

definition Dc :: "nat => real => real" where
  "Dc n P = SA n + D n P"

definition P_reconstruit :: "nat => real => real" where
  "P_reconstruit n P = (SB n - Dc n P) / Z"

lemma reconstruction_P:
  fixes n :: nat
  fixes P :: real
  shows "P_reconstruit n P = P"
proof -
  have "P_reconstruit n P =
        (SB n - (SA n + (SB n - SA n - Z * P))) / Z"
    unfolding P_reconstruit_def Dc_def D_def by simp
  also have "... = (SB n - SA n - SB n + SA n + Z * P) / Z"
    by simp
  also have "... = (Z * P) / Z"
    by simp
  also have "... = P"
    unfolding Z_def by simp
  finally show ?thesis .
qed

text \<open>
  Définition générale : un bloc spectral est une liste d’indices
  permettant de former une Somme A ou une Somme B.
\<close>

definition SommeA :: "nat list \<Rightarrow> real" where
  "SommeA ns = (\<Sum>n\<leftarrow>ns. SA n)"

definition SommeB :: "nat list \<Rightarrow> real" where
  "SommeB ns = (\<Sum>n\<leftarrow>ns. SB n)"

text \<open>
  ----------------------------------------------------------------------
  1. Comparaison SPECTRALE SYMÉTRIQUE 1\<times>1
  ----------------------------------------------------------------------
  Deux positions (par exemple deux premiers) sont comparées directement.
  On ne fixe aucune équation : seulement la structure 1\<times>1.
\<close>

record comparaison_1x1 =
  posA :: nat
  posB :: nat

definition est_symetrique_1x1 :: "comparaison_1x1 \<Rightarrow> bool" where
  "est_symetrique_1x1 c \<longleftrightarrow> (posA c \<noteq> posB c)"

text \<open>
  ----------------------------------------------------------------------
  2. Comparaison SPECTRALE SYMÉTRIQUE n\<times>n
  ----------------------------------------------------------------------
  On compare deux blocs de Sommes A et deux blocs de Sommes B :
    - Bloc A  (Sommes A1, A2, ..., An1)
    - Bloc B  (Sommes A3, A4, ..., An2)
    - Bloc C  (Sommes B1, B2, ..., Bn1)
    - Bloc D  (Sommes B3, B4, ..., Bn2)

  Conditions structurelles :
    - Bloc A et Bloc B ont même cardinalité
    - Bloc C et Bloc D ont même cardinalité
    - Les blocs sont distincts
  Aucune équation n’est imposée ici.
\<close>

record comparaison_nxn =
  NA :: "nat list"
  NB :: "nat list"
  NC :: "nat list"
  ND :: "nat list"

definition est_symetrique_nxn :: "comparaison_nxn \<Rightarrow> bool" where
  "est_symetrique_nxn c \<longleftrightarrow>
     length (NA c) = length (NB c) \<and>
     length (NC c) = length (ND c) \<and>
     NA c \<noteq> NB c \<and>
     NC c \<noteq> ND c"

text \<open>
  ----------------------------------------------------------------------
  3. Comparaison ASYMÉTRIQUE ORDONNÉE
  ----------------------------------------------------------------------
  Règles structurelles :
    1. Bloc B est un décalage de Bloc A (indices plus grands)
    2. Bloc D est un décalage de Bloc C
    3. Les blocs sont strictement croissants (ordre chronologique)
    4. Bloc A et Bloc C ont même structure
       Bloc B et Bloc D ont même structure

  Aucune équation n’est donnée : seulement la structure ordonnée.
\<close>

definition est_croissante :: "nat list \<Rightarrow> bool" where
  "est_croissante ns \<longleftrightarrow> (\<forall>i<length ns - 1. ns ! i < ns ! (i+1))"

record comparaison_asym_ordonnee =
  AO :: "nat list"
  BO :: "nat list"
  CO :: "nat list"
  DO :: "nat list"

definition est_asym_ordonnee :: "comparaison_asym_ordonnee \<Rightarrow> bool" where
  "est_asym_ordonnee c \<longleftrightarrow>
     est_croissante (AO c) \<and>
     est_croissante (BO c) \<and>
     est_croissante (CO c) \<and>
     est_croissante (DO c) \<and>
     (\<forall>a\<in>set (AO c). \<forall>b\<in>set (BO c). a < b) \<and>
     (\<forall>a\<in>set (CO c). \<forall>d\<in>set (DO c). a < d)"

text \<open>
  ----------------------------------------------------------------------
  4. Comparaison ASYMÉTRIQUE CHAOTIQUE
  ----------------------------------------------------------------------
  Structure :
    - Bloc A chaotique différent de Bloc B
    - Bloc B chaotique différent de Bloc D
    - Bloc A = Bloc C (même indices)
    - Bloc B = Bloc D (même indices)

  Aucune équation n’est donnée : seulement la structure chaotique.
\<close>

record comparaison_asym_chaotique =
  AC :: "nat list"
  BC :: "nat list"

definition est_asym_chaotique :: "comparaison_asym_chaotique \<Rightarrow> bool" where
  "est_asym_chaotique c \<longleftrightarrow> AC c \<noteq> BC c"


end
