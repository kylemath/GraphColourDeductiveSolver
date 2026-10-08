#!/usr/bin/env python3
"""Heawood 1890: locate Heawood's own failing colouring at V in the state space; confirm it is a Kempe trap
(Kempe's double swap fails in both orders, with interference) and run every Track M rule from it."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tm_lib import Hole, RULES, run_rule
P = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/historical-traps/heawood1890.json'
d = json.load(open(P)); names = d['vertex_names']; rot = d['rotation']; V = d['kempe_failing_colouring']['hole_index']
col = d['kempe_failing_colouring']['colours_by_name']
H = Hole(rot, V); H.classes_and_dist()
conc = {i: 'rbyg'.index(col[names[i]]) for i in range(len(rot)) if i != V}
s0 = H.sp.state_of(conc)
out = dict(hole=names[V], link=[names[x] + ':' + col[names[x]] for x in rot[V]], state=s0, filled=H.filled[s0],
           L1=H.L1[s0], L2=H.L2[s0], dF=H.dF[s0], dNDL=H.dNDL[s0], kempe_double_swap=[dict(success=a, interference=b) for a, b, _ in H.kempe2[s0]],
           on_allDL_cycle=s0 in H.allDL_cycle_states(), kempe_degree=len(H.moves[s0]),
           rules={r: run_rule(H, r, s0)[0] for r in RULES})
print(json.dumps(out, indent=1))
# literal (simultaneous) Kempe step at Heawood's colouring
sp = H.sp; s = sp.states[s0]; cm = sp.cmasks(s); li = sp.linki; j = H.j[s0]; colr = [s[li[t]] for t in range(5)]
x = [li[(j + t) % 5] for t in range(5)]; al, A, B = colr[j], colr[(j + 3) % 5], colr[(j + 4) % 5]
K1 = sp.flood(1 << x[2], cm[al] | cm[B]); K2 = sp.flood(1 << x[0], cm[al] | cm[A])
lit = dict(K1=sp.mask_vertices(K1), K2=sp.mask_vertices(K2), shared=[names[v] for v in sp.mask_vertices(K1 & K2)])
lit['K1'] = [names[v] for v in lit['K1']]; lit['K2'] = [names[v] for v in lit['K2']]
d2 = list(s)
for i in range(sp.N):
    if K1 >> i & 1: d2[i] = B if s[i] == al else al
    elif K2 >> i & 1: d2[i] = A if s[i] == al else al
lit['simultaneous_proper'] = (not K1 & K2) and all(d2[i] != d2[w] for i in range(sp.N) for w in range(sp.N) if sp.nbm[i] >> w & 1)
out['kempe1879_literal'] = lit
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out/heawood_colouring.json'), 'w'), indent=1)
print(json.dumps(lit))
