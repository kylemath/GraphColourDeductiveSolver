(* Job 20 (Studio, exploratory): the 66666 wheel w66666 checked with Gonthier's fourcolor reducibility checker.
   Program found by cfprog.py (a Python transcription of cfmap.v, used only as a search aid):
     H 1 H 3 H 1 H 3 H 1 Y 1 H 2 Y 1 Y Y 1 Y Y Y Y
   kernel faces: 5-face I0 and five 6-faces I1..I5 (a wheel), ring 10.  Contract indices (ctrenum order, 0-based)
   0, 20, 11, 23 = R0-I1, I2-I3, I3-I4, I4-I5 with I1 the rim face whose private ring face is R0.
   Usage (opam switch "fourcolor"):  coqc fourcolor_w66666.v *)
From mathcomp Require Import ssreflect ssrfun ssrbool eqtype ssrnat seq.
From fourcolor Require Import hypermap geometry color coloring cfmap ctree initctree kempetree cfcontract cfreducible.
From fourcolor Require Import configurations.

Import ConfigSyntax.

Definition cfW := Config 0 20 11 23 H 1 H 3 H 1 H 3 H 1 Y 1 H 2 Y 1 Y Y 1 Y Y Y Y.
Definition cfW_noX := Config H 1 H 3 H 1 H 3 H 1 Y 1 H 2 Y 1 Y Y 1 Y Y Y Y.

Fixpoint ct_count t := match t with
  | CtreeNode t1 t2 t3 => ct_count t1 + ct_count t2 + ct_count t3
  | CtreeLeaf _ => 1
  | CtreeEmpty => 0 end.

(* 1. The encoding: ring size, kernel face arities (expect 10 and [5;6;6;6;6;6] in some order). *)
Eval vm_compute in cprsize (cfprog cfW).
(* arities: not evaluated (finType orbit computation is too slow under vm_compute); see cfprog.py *)
Eval vm_compute in ctrmsize (cfprog cfW).

(* 2. D-closure: number of ring traces (normalised) and of traces NOT in the Kempe co-closure. *)
Eval vm_compute in ct_count (ctree_init_tree 9).
Eval vm_compute in ct_count (Kempe_tree (cfprog cfW)).

(* 3. Contract X: is it accepted (cfctr Some, valid_ctrm), how many contract traces, and the verdict. *)
Eval vm_compute in valid_ctrm (cfcontract_mask cfW) (cfprog cfW).
Eval vm_compute in
  if cfctr (nseq (cprsize (cfprog cfW)) false) (cfcontract_mask cfW) (cfprog cfW) is Some _ then true else false.
Eval vm_compute in if contract_ctree cfW is Some ct then ct_count ct else 0.
Eval vm_compute in check_reducible cfW.

(* 4. Control: RSST/Gonthier configuration 1 (the Birkhoff diamond) must be reducible. *)
Eval vm_compute in cprsize (cfprog cf001).
Eval vm_compute in check_reducible cf001.

(* 5. Kernel-checked statement: w66666 with contract X is C-reducible in Gonthier's sense. *)
Lemma w66666_check : check_reducible cfW. Proof. by vm_compute. Qed.
Lemma w66666_Creducible : cfreducible cfW. Proof. exact: (@check_reducible_valid cfW w66666_check). Qed.
Print Assumptions w66666_Creducible.
