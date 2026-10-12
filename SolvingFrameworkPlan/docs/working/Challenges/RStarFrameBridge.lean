import Challenges.RStarFrameChallenge
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameF3

/-!
# Anti-drift bridge: the frozen `RStarFrame` challenge is the project's `RStarFrame`

`mainStatement_iff : RStarFrameChallenge.MainStatement ↔ SimpleGraph.SphericalMap.RStarFrame`.

The challenge file (`RStarFrameChallenge.lean`) imports only upstream Mathlib and restates every
definition. This file translates maps both ways (`toLib`, `ofLib`: same graph, same rotation
permutation) and shows that each predicate of the statement agrees:
* `Fills`: a face potential on the quotient `Face` type is the same as a `faceNext`-invariant
  dart function;
* `Triangulated`: face length is the minimal period of `faceNext` (`face_length_eq_period`);
* `Nx`, `NoSep`, `ProperOff`, `Target`, `KempeStep`, degrees: definitional;
* the four `Occ` structures: field by field;
* `PureClean`: a `PurePath` of some length is a `ReflTransGen` chain of Kempe steps.
-/

namespace RStarFrameBridge

open SimpleGraph SimpleGraph.SphericalMap VacancySlide VacancyShortFill

variable {n : ℕ}

/-! ## Translating maps -/

/-- Library rotation system to challenge rotation system. -/
def rotOfLib {G : SimpleGraph (Fin n)} (R : SimpleGraph.RotationSystem G) :
    RStarFrameChallenge.RotationSystem G :=
  ⟨R.next, R.next_fst, R.cyclic⟩

/-- Challenge rotation system to library rotation system. -/
def rotToLib {G : SimpleGraph (Fin n)} (R : RStarFrameChallenge.RotationSystem G) :
    SimpleGraph.RotationSystem G :=
  ⟨R.next, R.next_fst, R.cyclic⟩

theorem fills_toLib {G : SimpleGraph (Fin n)} (R : RStarFrameChallenge.RotationSystem G)
    (h : R.Fills) : (rotToLib R).Fills := by
  intro φ hφ
  obtain ⟨c, hinv, hc⟩ := h φ hφ
  have key : ∀ d e, (rotToLib R).FaceRelation d e → c d = c e := by
    intro d e hde
    induction hde with
    | refl => rfl
    | step d => exact (hinv d).symm
    | symm _ ih => exact ih.symm
    | trans _ _ ih1 ih2 => exact ih1.trans ih2
  refine ⟨fun f : (rotToLib R).Face =>
    Sum.elim (Quotient.lift c (fun a b hab => key a b hab)) (fun _ => (0 : ZMod 2)) f, ?_⟩
  intro d
  exact hc d

theorem fills_ofLib {G : SimpleGraph (Fin n)} (R : SimpleGraph.RotationSystem G)
    (h : R.Fills) : (rotOfLib R).Fills := by
  intro φ hφ
  obtain ⟨c, hc⟩ := h φ hφ
  exact ⟨fun d => c (R.faceOf d), fun d => congrArg c (R.face_of_face_next d), fun d => hc d⟩

/-- Challenge map to library map. -/
def toLib (T : RStarFrameChallenge.SphericalMap n) : SimpleGraph.SphericalMap n :=
  ⟨T.graph, rotToLib T.rotation, fills_toLib _ T.fills⟩

/-- Library map to challenge map. -/
def ofLib (T : SimpleGraph.SphericalMap n) : RStarFrameChallenge.SphericalMap n :=
  ⟨T.graph, rotOfLib T.rotation, fills_ofLib _ T.fills⟩

theorem ofLib_toLib (T : RStarFrameChallenge.SphericalMap n) : ofLib (toLib T) = T := rfl

/-! ## The predicates agree -/

variable (T : SimpleGraph.SphericalMap n)

theorem degree_eq (v : Fin n) : (ofLib T).graph.degree v = T.graph.degree v := rfl

theorem triangulated_iff : (ofLib T).Triangulated ↔ T.Triangulated := by
  refine forall_congr' fun (d : T.graph.Dart) => ?_
  have e := T.rotation.face_length_eq_period d
  exact ⟨fun h => e.trans h, fun h => e.symm.trans h⟩

theorem noSep_iff : (ofLib T).NoSep ↔ NoSep T := Iff.rfl

theorem kempeStep_iff (h : Fin n) (c d : Fin n → Fin 4) :
    RStarFrameChallenge.KempeStep T.graph h c d ↔ VacancyShortFill.KempeStep T.graph h c d :=
  Iff.rfl

theorem purePath_rtg {h : Fin n} {m : ℕ} {c d : Fin n → Fin 4}
    (p : PurePath T.graph h m c d) :
    Relation.ReflTransGen (RStarFrameChallenge.KempeStep T.graph h) c d := by
  induction p with
  | nil => exact .refl
  | cons s _ ih => exact .head s ih

theorem rtg_purePath {h : Fin n} {c d : Fin n → Fin 4}
    (p : Relation.ReflTransGen (RStarFrameChallenge.KempeStep T.graph h) c d) :
    ∃ m, PurePath T.graph h m c d := by
  induction p using Relation.ReflTransGen.head_induction_on with
  | refl => exact ⟨0, .nil _⟩
  | head s _ ih =>
    obtain ⟨m, q⟩ := ih
    exact ⟨m + 1, .cons s q⟩

theorem pureClean_iff (v : Fin n) : (ofLib T).PureClean v ↔ PureClean T v := by
  refine forall_congr' fun c => imp_congr_right fun _ => ?_
  constructor
  · rintro ⟨d, p, t⟩
    obtain ⟨m, q⟩ := rtg_purePath T p
    exact ⟨m, m, le_rfl, d, q, t⟩
  · rintro ⟨_, m, _, d, q, t⟩
    exact ⟨d, purePath_rtg T q, t⟩

theorem diamondM_iff (ring : Fin 6 → Fin n) (int : Fin 4 → Fin n) :
    RStarFrameChallenge.DiamondMOcc (ofLib T) ring int ↔ DiamondM.Occ T ring int :=
  ⟨fun o => by cases o; constructor <;> assumption,
    fun o => by cases o; constructor <;> assumption⟩

theorem diamondP_iff (ring : Fin 6 → Fin n) (int : Fin 4 → Fin n) :
    RStarFrameChallenge.DiamondPOcc (ofLib T) ring int ↔ DiamondP.Occ T ring int :=
  ⟨fun o => by cases o; constructor <;> assumption,
    fun o => by cases o; constructor <;> assumption⟩

theorem c2122M_iff (ring : Fin 7 → Fin n) (int : Fin 4 → Fin n) :
    RStarFrameChallenge.C2122MOcc (ofLib T) ring int ↔ C2122M.Occ T ring int :=
  ⟨fun o => by cases o; constructor <;> assumption,
    fun o => by cases o; constructor <;> assumption⟩

theorem c2122P_iff (ring : Fin 7 → Fin n) (int : Fin 4 → Fin n) :
    RStarFrameChallenge.C2122POcc (ofLib T) ring int ↔ C2122P.Occ T ring int :=
  ⟨fun o => by cases o; constructor <;> assumption,
    fun o => by cases o; constructor <;> assumption⟩

theorem diamondFree_iff :
    RStarFrameChallenge.DiamondFree (ofLib T) ↔ SimpleGraph.SphericalMap.DiamondFree T := by
  simp only [RStarFrameChallenge.DiamondFree, SimpleGraph.SphericalMap.DiamondFree,
    diamondM_iff, diamondP_iff]

theorem conf2122Free_iff :
    RStarFrameChallenge.Conf2122Free (ofLib T) ↔ SimpleGraph.SphericalMap.Conf2122Free T := by
  simp only [RStarFrameChallenge.Conf2122Free, SimpleGraph.SphericalMap.Conf2122Free,
    c2122M_iff, c2122P_iff]

/-! ## The statements agree -/

/-- **Anti-drift check.** The frozen challenge statement is the project's `RStarFrame`. -/
theorem mainStatement_iff : RStarFrameChallenge.MainStatement ↔ RStarFrame := by
  constructor
  · intro H m T hm hconn htri hdeg hns hD hC
    obtain ⟨v, hv, hp⟩ := H m (ofLib T) hm hconn ((triangulated_iff T).2 htri) hdeg
      ((noSep_iff T).2 hns) ((diamondFree_iff T).2 hD) ((conf2122Free_iff T).2 hC)
    exact ⟨v, hv, (pureClean_iff T v).1 hp⟩
  · intro H m T hm hconn htri hdeg hns hD hC
    obtain ⟨v, hv, hp⟩ := H m (toLib T) hm hconn ((triangulated_iff _).1 htri) hdeg
      ((noSep_iff _).1 hns) ((diamondFree_iff _).1 hD) ((conf2122Free_iff _).1 hC)
    exact ⟨v, hv, (pureClean_iff _ v).2 hp⟩

end RStarFrameBridge

#print axioms RStarFrameBridge.mainStatement_iff
