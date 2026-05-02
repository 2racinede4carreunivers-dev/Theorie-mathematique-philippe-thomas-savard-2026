theory geometrie_spectre_premier
  imports Complex_Main
begin

text "Formalisation de base de la methode spectrale (rapport 1/2)."

(* Constante Zeta : 6ieme terme de la suite A pour le rapport 1/2 *)
definition Z :: real where
  "Z = 64"

(* Somme de la suite A en fonction de n *)
definition SA :: "nat => real" where
  "SA n = (3.25 / 2) * (2 ^ n) - 2"

(* Somme de la suite B en fonction de n *)
definition SB :: "nat => real" where
  "SB n = (6.5 / 2) * (2 ^ n) - 66"

(* Definition du digamma D en fonction de n et de P *)
definition D :: "nat => real => real" where
  "D n P = SB n - SA n - Z * P"

(* Digamma calcule, avec le signe + *)
definition Dc :: "nat => real => real" where
  "Dc n P = SA n + D n P"

(* Formule de reconstruction du nombre premier *)
definition P_reconstruit :: "nat => real => real" where
  "P_reconstruit n P = (SB n - Dc n P) / Z"

lemma reconstruction_P:
  fixes n :: nat
  fixes P :: real
  shows "P_reconstruit n P = P"
proof -
  have "P_reconstruit n P = (SB n - (SA n + (SB n - SA n - Z * P))) / Z"
    unfolding P_reconstruit_def Dc_def D_def by simp
  also have "... = (SB n - SA n - SB n + SA n + Z * P) / Z"
    by simp
  also have "... = (Z * P) / Z"
    by simp
  also have "... = P"
    unfolding Z_def by simp
  finally show ?thesis .
qed

end
