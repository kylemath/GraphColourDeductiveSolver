import DCheckT
import DCheck16
import DCheck18
/-! Job 23: `DCheck16` and `DCheck18` are the parametrised checker at N = 9, 10. The copies' own
structural recursions (`ncm`, `extAux`) are not definitionally the originals, so they are equated by
induction; everything else is `rfl`. -/
namespace DCheck

def Conf.of16 (cf : DCheck16.Conf) : Conf :=
  { name := cf.name, r := cf.r, m := cf.m, ringAdj := cf.ringAdj, intAdj := cf.intAdj,
    rsstExt := cf.rsstExt, rsstContract := cf.rsstContract }

theorem ncm16_eq' : ∀ f pts, DCheck16.ncm f pts = DCheck.ncm f pts := by
  intro f
  induction f with
  | zero => intro pts; cases pts <;> rfl
  | succ f ih => intro pts; cases pts <;> simp [DCheck16.ncm, DCheck.ncm, ih]

theorem matchTable16_eq : DCheck16.matchTable = matchTableN 9 := by
  unfold DCheck16.matchTable matchTableN
  congr 1; funext p; congr 2; exact ncm16_eq' _ _

theorem extAux16_eq (cf : DCheck16.Conf) (k : Nat) :
    ∀ f cols, DCheck16.extAux cf k f cols = DCheck.extAux (Conf.of16 cf) k f cols := by
  intro f
  induction f with
  | zero => intro cols; rfl
  | succ f ih => intro cols; simp only [DCheck16.extAux, DCheck.extAux, ih]; rfl

theorem extendsQ16_eq (cf : DCheck16.Conf) :
    DCheck16.extendsQ cf = DCheck.extendsQ (Conf.of16 cf) := by
  funext k; exact extAux16_eq cf k _ _

theorem dReducible16_eq_T (cf : DCheck16.Conf) :
    DCheck16.dReducible cf = dReducibleT (matchTableN 9) (Conf.of16 cf) := by
  unfold DCheck16.dReducible DCheck16.run dReducibleT runT
  rw [extendsQ16_eq, matchTable16_eq]
  rfl

def Conf.of18 (cf : DCheck18.Conf) : Conf :=
  { name := cf.name, r := cf.r, m := cf.m, ringAdj := cf.ringAdj, intAdj := cf.intAdj,
    rsstExt := cf.rsstExt, rsstContract := cf.rsstContract }

theorem ncm18_eq' : ∀ f pts, DCheck18.ncm f pts = DCheck.ncm f pts := by
  intro f
  induction f with
  | zero => intro pts; cases pts <;> rfl
  | succ f ih => intro pts; cases pts <;> simp [DCheck18.ncm, DCheck.ncm, ih]

theorem matchTable18_eq : DCheck18.matchTable = matchTableN 10 := by
  unfold DCheck18.matchTable matchTableN
  congr 1; funext p; congr 2; exact ncm18_eq' _ _

theorem extAux18_eq (cf : DCheck18.Conf) (k : Nat) :
    ∀ f cols, DCheck18.extAux cf k f cols = DCheck.extAux (Conf.of18 cf) k f cols := by
  intro f
  induction f with
  | zero => intro cols; rfl
  | succ f ih => intro cols; simp only [DCheck18.extAux, DCheck.extAux, ih]; rfl

theorem extendsQ18_eq (cf : DCheck18.Conf) :
    DCheck18.extendsQ cf = DCheck.extendsQ (Conf.of18 cf) := by
  funext k; exact extAux18_eq cf k _ _

theorem dReducible18_eq_T (cf : DCheck18.Conf) :
    DCheck18.dReducible cf = dReducibleT (matchTableN 10) (Conf.of18 cf) := by
  unfold DCheck18.dReducible DCheck18.run dReducibleT runT
  rw [extendsQ18_eq, matchTable18_eq]
  rfl

end DCheck

#print axioms DCheck.dReducible16_eq_T
#print axioms DCheck.dReducible18_eq_T
