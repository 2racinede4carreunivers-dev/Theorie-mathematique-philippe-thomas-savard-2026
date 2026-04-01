theory postulat_carre
  imports Complex_Main
begin

(* ========================================================= *)
(* Table of Contents                                         *)
(* ========================================================= *)

(* 1. Unified Squared Rectangle and Prime Postulate          *)
(*    1.1 Locale: postulat_carre                             *)
(*    1.2 Definitions                                        *)
(*        - S_S, S_F, S_C                                    *)
(*        - d_S, d_F, d_C                                    *)
(*        - unit_p                                           *)
(*        - upto_from_2, k                                   *)
(*        - postulat_eq                                      *)
(*        - ratio_height_square                              *)
(*        - ratio_trunc_square                               *)

(* 2. Rectangle carre : equivalence avec un carre            *)
(*    2.1 Locale: rectangle_carre                            *)
(*    2.2 Area definitions                                   *)
(*    2.3 Equivalence condition                              *)

(* 3. Axiomatisation du polygone au carre                    *)
(*    3.1 Locale: polygone_carre_axiomes                     *)
(*    3.2 Height ratio equation                              *)
(*    3.3 Truncation ratio equation                          *)
(*    3.4 Postulate equation                                 *)
(*    3.5 Definition of a squared polygon                    *)

(* 4. Exemple numerique pour p = 3                           *)
(*    4.1 Locale: exemple_p3                                 *)
(*    4.2 Height ratio lemma                                 *)
(*    4.3 Truncation ratio lemma                             *)
(*    4.4 Diagonal lemma                                     *)
(*    4.5 Area lemma                                         *)

(* 5. Appendix: Full Isabelle/HOL Source Code                *)
(*    - postulat_carre.thy                                   *)

(* 6. License                                                *)

section "Unified Squared Rectangle and Prime Postulate"

locale postulat_carre =
  fixes w :: real
    and h :: real
    and s :: real
    and t :: real
    and p :: nat
    and diag :: real
    and area :: real
  assumes geom: "w > 0" "h > 0" "s > 0" "t > 0" "s <= w" "s <= h"
    and prime_p: "prime p"
begin

definition S_S :: real where
  "S_S = w * h"

definition S_F :: real where
  "S_F = s * s"

definition S_C :: real where
  "S_C = S_S - S_F"

definition d_S :: real where
  "d_S = sqrt (w * w + h * h)"

definition d_F :: real where
  "d_F = sqrt 2 * s"

definition d_C :: real where
  "d_C = sqrt (s * s + t * t)"

definition unit_p :: real where
  "unit_p = sqrt (real p) + 1"

definition upto_from_2 :: "nat list" where
  "upto_from_2 = [2 ..< Suc p]"

definition k :: nat where
  "k =
     (THE i. i < length upto_from_2
           & upto_from_2 ! i = p) + 1"

definition postulat_eq :: bool where
  "postulat_eq =
     ((diag * sqrt unit_p) ^ 2 = real k * area + h * h)"

definition ratio_height_square :: bool where
  "ratio_height_square =
     (h / s = sqrt (real p) + 1)"

definition ratio_trunc_square :: bool where
  "ratio_trunc_square =
     (t / s = sqrt (real p))"

end


section "Rectangle carre : equivalence avec un carre"

locale rectangle_carre =
  fixes w :: real
    and h :: real
    and s :: real
  assumes geom: "w > 0" "h > 0" "s > 0"
begin

definition area_rect :: real where
  "area_rect = w * h"

definition area_square :: real where
  "area_square = s * s"

definition rect_equiv_square :: bool where
  "rect_equiv_square =
     (area_rect = area_square)"

end


section "Axiomatisation du polygone au carre"

locale polygone_carre_axiomes =
  fixes p :: nat
    and h :: real
    and s :: real
    and t :: real
    and diag :: real
    and area :: real
  assumes prime_p: "prime p"
    and geom: "h > 0" "s > 0" "t > 0"
begin

definition eq_ratio_height :: bool where
  "eq_ratio_height =
     (h / s = sqrt (real p) + 1)"

definition eq_ratio_trunc :: bool where
  "eq_ratio_trunc =
     (t / s = sqrt (real p))"

definition eq_postulat :: bool where
  "eq_postulat =
     ((diag * sqrt (sqrt (real p) + 1)) ^ 2
        = area + h * h)"

definition polygone_defini :: bool where
  "polygone_defini =
     (eq_ratio_height & eq_ratio_trunc & eq_postulat)"

end
section "Exemple numerique pour p = 3"

locale exemple_p3 =
  fixes s3 :: real
    and h3 :: real
    and t3 :: real
    and diag3 :: real
    and area3 :: real
  assumes s3_pos: "s3 > 0"
    and ratio_height_3: "h3 / s3 = sqrt 3 + 1"
    and ratio_trunc_3: "t3 / s3 = sqrt 3"
    and diag_trunc_3: "sqrt (s3 * s3 + t3 * t3) = sqrt 6"
    and area_def_3: "area3 = s3 * h3"
begin

text "
Cet exemple formalise le cas p = 3.
Les valeurs numeriques (0.896575..., 1.552914..., etc.)
ne sont pas utilisees directement : seules les relations exactes
sont axiomatisées.
"

lemma hauteur_sur_cote:
  shows "h3 / s3 = sqrt 3 + 1"
  using ratio_height_3 .

lemma tronque_sur_cote:
  shows "t3 / s3 = sqrt 3"
  using ratio_trunc_3 .

lemma diagonale_tronquee_exacte:
  shows "sqrt (s3 * s3 + t3 * t3) = sqrt 6"
  using diag_trunc_3 .

lemma aire_rectangle:
  shows "area3 = s3 * h3"
  using area_def_3 .

end
end

(* ========================================================= *)
(* Apache License 2.0                                        *)
(* ========================================================= *)

(* Apache License                                            *)
(* Version 2.0, January 2004                                *)
(* http://www.apache.org/licenses/                          *)

(* TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION *)

(* 1. Definitions.                                           *)
(* "License" shall mean the terms and conditions for use,    *)
(* reproduction, and distribution as defined by Sections 1   *)
(* through 9 of this document.                              *)

(* "Licensor" shall mean the copyright owner or entity       *)
(* authorized by the copyright owner that is granting the    *)
(* License.                                                  *)

(* "Legal Entity" shall mean the union of the acting entity  *)
(* and all other entities that control, are controlled by,   *)
(* or are under common control with that entity.             *)

(* "Source" form shall mean the preferred form for making    *)
(* modifications.                                            *)

(* "Object" form shall mean any form resulting from          *)
(* mechanical transformation or translation of a Source form.*)

(* "Work" shall mean the work of authorship made available   *)
(* under the License.                                        *)

(* "Derivative Works" shall mean any work that is based on   *)
(* the Work.                                                 *)

(* "Contribution" shall mean any work submitted to the       *)
(* Licensor.                                                 *)

(* "Contributor" shall mean the Licensor and any individual  *)
(* or Legal Entity that submits a Contribution.              *)

(* 2. Grant of Copyright License.                            *)
(* Subject to the terms of this License, each Contributor    *)
(* grants you a perpetual, worldwide, non-exclusive,         *)
(* no-charge, royalty-free, irrevocable copyright license    *)
(* to reproduce, prepare Derivative Works of, publicly       *)
(* display, publicly perform, sublicense, and distribute     *)
(* the Work and such Derivative Works in Source or Object    *)
(* form.                                                     *)

(* 3. Grant of Patent License.                               *)
(* Each Contributor grants you a perpetual, worldwide,       *)
(* non-exclusive, no-charge, royalty-free, irrevocable       *)
(* patent license to make, use, offer to sell, sell, import, *)
(* and otherwise transfer the Work.                          *)

(* 4. Redistribution.                                        *)
(* You may reproduce and distribute copies of the Work or    *)
(* Derivative Works thereof in any medium, with or without   *)
(* modifications, provided that you give proper notice and   *)
(* include a copy of this License.                           *)

(* 5. Submission of Contributions.                           *)
(* Unless explicitly stated otherwise, any Contribution      *)
(* intentionally submitted for inclusion in the Work shall   *)
(* be under the terms of this License.                       *)

(* 6. Trademarks.                                            *)
(* This License does not grant permission to use trade names,*)
(* trademarks, service marks, or product names of the        *)
(* Licensor.                                                 *)

(* 7. Disclaimer of Warranty.                                *)
(* Unless required by applicable law or agreed to in writing,*)
(* the Licensor provides the Work on an "AS IS" BASIS,       *)
(* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.             *)

(* 8. Limitation of Liability.                               *)
(* In no event shall the Licensor be liable for any damages  *)
(* arising from the use of the Work.                         *)

(* 9. Accepting Warranty or Additional Liability.            *)
(* You may offer additional warranties or liabilities        *)
(* consistent with this License, but only on your own behalf.*)

(* END OF TERMS AND CONDITIONS                               *)