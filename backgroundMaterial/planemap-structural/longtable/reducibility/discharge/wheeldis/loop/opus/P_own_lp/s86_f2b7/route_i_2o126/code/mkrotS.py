#!/usr/bin/env python3
"""mkrotS.py (Opus, 10 Nov 2026): RotOcc for a target rotation `rotS` whose lists are cyclic shifts of the generated `rot`.
Reads the Occ fields `rA_j : Nx T (int a) (X) (Y)` of gen_occ_kc.py's <NS>.lean, takes the target lists, checks that every
target list is a cyclic shift of the Occ rotation at that vertex (same direction), and that for every slot k the field used,
r<a>_<(k+s) mod len>, states exactly Nx T (int a) (slot S[k+1]) (slot S[k]); then writes the Lean module.
usage: python3 -I mkrotS.py <NS>.lean NS 'TARGET' OUT.lean MODNAME"""
import sys, re
src, NS, target, out, MODNAME = sys.argv[1:6]
T = open(src).read()
fld = {}
for a, j, x, y in re.findall(r'^\s*r(\d+)_(\d+) : Nx T \(int (?:\d+)\) \((\w+ \d+)\) \((\w+ \d+)\)', T, re.M):
    fld[(int(a), int(j))] = (x, y)
m = max(a for a, _ in fld) + 1
occrot = []
for a in range(m):
    L = max(j for b, j in fld if b == a) + 1
    seq = [fld[(a, j)][1] for j in range(L)]                      # Occ's rot[j] = second argument of field j
    assert all(fld[(a, j)][0] == seq[(j + 1) % L] for j in range(L)), a
    occrot.append(seq)
def slot(tok):
    k, v = tok.split('.')[1].split()
    return ('ring ' if k == 'inr' else 'int ') + v
tgt = [[slot(t.strip()) for t in lst.split(',')] for lst in re.findall(r'\[([^\[\]]*)\]', target)]
assert len(tgt) == m
lines = []; shifts = []
for a in range(m):
    S, R = tgt[a], occrot[a]; L = len(R)
    assert len(S) == L and sorted(S) == sorted(R), (a, S, R)
    s = [i for i in range(L) if R[i:] + R[:i] == S]; assert len(s) == 1, (a, S, R); s = s[0]; shifts.append(s)
    lines.append('    · replace hk : k < %d := hk' % L)
    lines.append('      interval_cases k')
    for k in range(L):
        j = (k + s) % L
        assert fld[(a, j)] == (S[(k + 1) % L], S[k]), (a, k, j)
        lines.append('      · exact h.r%d_%d' % (a, j))
r = int(re.search(r'\(ring : Fin (\d+) → Fin n\)', T).group(1))
txt = '''import COcc%(NS)s

/-! # %(MOD)s (Opus, 10 Nov 2026): `RotOcc` for the rotation `rotS`, each list started where the Studio's `rot2o126`
(job_ST123 C2o126Glue) starts it. The lists are cyclic shifts of `rot` (COcc%(NS)s), shifts %(SH)s, so the
orientation is the same. Written by mkrotS.py, which checks in Python that each field used states the slot pair of `rotS`.
`rotS` is the same `![..]` literal as `rot2o126`, so `rotS = rot2o126` holds by `rfl`. -/

namespace SimpleGraph.SphericalMap.%(NS)s
open VacancyIcosahedral DCheck DCheck.R2

variable {n : ℕ}

/-- The rotation of `Occ`, each list started as in `rot2o126`. -/
def rotS : Fin %(m)d → List (Fin %(m)d ⊕ ℕ) :=
  %(TGT)s

theorem rotS_ok : rotOK (DCheck.Conf.of18 cf) rotS = true := by decide +kernel

theorem rotOccS_of_occ {T : SphericalMap n} {ring : Fin %(r)d → Fin n} {int : Fin %(m)d → Fin n}
    (h : Occ T ring int) : RotOcc T (ρOf ring) int rotS where
  ιinj := h.int_inj
  disj := fun t a => h.disj _ a
  deg := fun a => by rw [h.deg a]; fin_cases a <;> rfl
  nx := by
    intro a k hk
    fin_cases a
%(LINES)s

end SimpleGraph.SphericalMap.%(NS)s

#print axioms SimpleGraph.SphericalMap.%(NS)s.rotS_ok
#print axioms SimpleGraph.SphericalMap.%(NS)s.rotOccS_of_occ
''' % dict(NS=NS, MOD=MODNAME, SH=', '.join('I%d %d' % (a, s) for a, s in enumerate(shifts)), m=m, r=r, TGT=target.strip(), LINES='\n'.join(lines))
open(out, 'w').write(txt)
print('shifts', shifts, '->', out)
