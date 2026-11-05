"""Bridge test generator (Long Table, 19 Oct 2026): for an occ24 per-key module Kxx.lean, emit a module that reads
the interior rotation `rot` off `Occ`'s own Nx fields (r<a>_<k> : Nx T (int a) X Y, so slot k is Y and slot k+1 is X),
proves `Occ -> RotOcc` from int_inj, disj, deg and the Nx fields only, checks `rotOK` by native_decide, and derives
OccExact, NbrInj and ApexFacts (COccBridge). Usage: python3 gen_rotbridge.py Kxx.lean NAMESPACE MODULE > COccKxx.lean"""
import re,sys
src,ns,mod=sys.argv[1],sys.argv[2],sys.argv[3]
t=open(src).read()
m=int(re.search(r'structure Occ \(T : SphericalMap n\) \(ring : Fin (\d+) → Fin n\) \(int : Fin (\d+) → Fin n\)',t).group(2))
facts={}
for a,k,x,y in re.findall(r'  r(\d+)_(\d+) : Nx T \(int \d+\) (\((?:int|ring) \d+\)) (\((?:int|ring) \d+\))',t):
    facts.setdefault(int(a),{})[int(k)]=(x,y)
def slot(v):
    kind,i=v.strip('()').split()
    return '.inl %s'%i if kind=='int' else '.inr %s'%i
rot={}
for a in range(m):
    F=facts[a]; d=len(F)
    L=[slot(F[k][1]) for k in range(d)]
    for k in range(d): assert slot(F[k][0])==L[(k+1)%d],(a,k)
    rot[a]=L
out=[]
out.append('import COccBridge\nimport %s\n'%mod)
out.append('/-! Bridge test (Long Table, 19 Oct 2026): the occ24 key `%s`\'s rotation occurrence `Occ` gives\n`RotOcc` with the rotation read off its own `Nx` fields, hence `OccExact`, `NbrInj` and `ApexFacts`.\nOnly `int_inj`, `disj`, `deg` and the `Nx` fields of `Occ` are used (no `ring_inj`). -/\n'%ns)
out.append('namespace SimpleGraph.SphericalMap.%s\nopen VacancyIcosahedral DCheck DCheck.R2\n\nvariable {n : ℕ}\n'%ns)
out.append('/-- The rotation at each interior vertex, as `Occ` states it. -/')
out.append('def rot : Fin %d → List (Fin %d ⊕ ℕ) := ![%s]\n'%(m,m,', '.join('['+', '.join(rot[a])+']' for a in range(m))))
out.append('theorem rot_ok : rotOK (DCheck.Conf.of18 cf) rot = true := by\n  native_decide\n')
out.append('theorem rotOcc_of_occ {T : SphericalMap n} {ring : Fin %d → Fin n} {int : Fin %d → Fin n}\n    (h : Occ T ring int) : RotOcc T (ρOf ring) int rot where'%(int(re.search(r'ring : Fin (\d+)',t).group(1)),m))
out.append('  ιinj := h.int_inj\n  disj := fun t a => h.disj _ a\n  deg := fun a => by rw [h.deg a]; fin_cases a <;> rfl')
out.append('  nx := by\n    intro a k hk\n    fin_cases a')
for a in range(m):
    d=len(rot[a])
    out.append('    · replace hk : k < %d := hk\n      interval_cases k'%d)
    for k in range(d):
        out.append('      · exact h.r%d_%d'%(a,k))
out.append('''
/-- **Falsification test, passed**: `Occ` gives the three local facts. -/
theorem local_facts_of_occ {T : SphericalMap n} {ring : Fin %d → Fin n} {int : Fin %d → Fin n}
    (h : Occ T ring int) :
    OccExact T (DCheck.Conf.of18 cf).r (ρOf ring) int (intAdjOf (DCheck.Conf.of18 cf)) (ringAdjOf (DCheck.Conf.of18 cf)) ∧
    NbrInj (DCheck.Conf.of18 cf).r (ρOf ring) (ringAdjOf (DCheck.Conf.of18 cf)) ∧
    ApexFacts T (DCheck.Conf.of18 cf).r (ρOf ring) int (intAdjOf (DCheck.Conf.of18 cf)) (ringAdjOf (DCheck.Conf.of18 cf)) :=
  ⟨(rotOcc_of_occ h).occExact rot_ok, (rotOcc_of_occ h).nbrInj rot_ok,
    (rotOcc_of_occ h).apexFacts rot_ok cf_sym⟩

end SimpleGraph.SphericalMap.%s

#print axioms SimpleGraph.SphericalMap.%s.local_facts_of_occ
'''%(int(re.search(r'ring : Fin (\d+)',t).group(1)),m,ns,ns))
print('\n'.join(out))
