"""L = 5 probes: which planar ingredients does UNSAT need?  Variants of r0sat (mode r0, L=5):
  full        : all clauses (expect UNSAT)
  novrot      : drop the side constraints of the v-chords (f1 alone on one side, f3, f4 on the other)
  vrot_only   : drop all crossing clauses, keep only the v-chord side rule (expect SAT)
  lone<s>     : v-chord f_s alone on its side (s = 1 is the true rotation; 3, 4 are other rotations)
usage: l5_probe.py n"""
import sys
from pysat.solvers import Glucose4
from r0sat import R0Enc, verify
n = int(sys.argv[1])
def run(tag, skip=(), lone=None):
    enc = R0Enc(n, 5, 'r0', True, True)
    if lone is not None:
        P = enc.pool; sl = {s: P.id(('vside', s)) for s in (1, 3, 4)}
        o = [s for s in (1, 3, 4) if s != lone]
        enc.groups['vrot'] = [[sl[lone], sl[o[0]]], [-sl[lone], -sl[o[0]]], [-sl[o[0]], sl[o[1]]], [sl[o[0]], -sl[o[1]]]]
    s = Glucose4(bootstrap_with=enc.clauses(skip=skip)); r = s.solve()
    print(f'n={n} L=5 {tag}: {"SAT" if r else "UNSAT"}')
run('full'); run('novrot', skip=('vrot',)); run('vrot_only', skip=('planar',))
for s_ in (1, 3, 4): run(f'lone f{s_}', lone=s_)
