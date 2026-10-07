#!/usr/bin/env python3
"""[Track E, C2 follow-up] Is the Heawood parity P mod 2 (i.e. i^H up to a constant) a function of the labelled ring
colouring alone?  For every degree-5 hole: map labelled link word -> set of P mod 2 over all labelled colourings of T - v.
Also compare the induced function across holes after normalising at one reference word."""
import sys, json
from collections import defaultdict, Counter
from phase_lib import *
GENTRI = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/studiointel/gentri/tri%d.txt'
holes = 0; amb = 0; funcs = Counter(); words_seen = Counter()
for n in map(int, sys.argv[1:]):
    for gi, line in enumerate(open(GENTRI % n)):
        rot = gentri_rotation(line)
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            L = LSpace(rot, h); m = len(L.tri); holes += 1
            mp = defaultdict(set)
            for k in range(L.S):
                s = L.sp.states[k]
                for g in PERMS:
                    P = L.stats(k, g)[0]; w = tuple(g[s[i]] for i in L.li); mp[w].add(P % 2)
            if any(len(v) > 1 for v in mp.values()): amb += 1; continue
            # candidate universal formula: parity of #ring words... normalise: f(w) xor f(w0) relative
            # test formula F(w) = (sum over t of Heawood-type sign of (w_t, w_{t+1})) -- reported as raw table instead
            ref = min(mp); f = {w: (next(iter(v)) ^ next(iter(mp[ref]))) for w, v in mp.items()}
            words_seen.update(f.keys())
            funcs[json.dumps(sorted((''.join(map(str, w)), b) for w, b in f.items()))] += 1
print(json.dumps(dict(holes=holes, holes_where_P_parity_not_a_function_of_ring_word=amb, distinct_normalised_functions=len(funcs))))

# ---- explicit formula check: P(c) + Pfill(w) mod 2 constant per hole, Pfill = #(+1) triangles of any proper fan
# triangulation of the pentagon by two chords from apex t (needs w_t != w_{t+2}, w_{t+3}); every proper fan is tried.
def fill_parities(w, ringtri_orient):
    out = set()
    for t in range(5):
        a, b, c, d, e = [w[(t + i) % 5] for i in range(5)]
        if a == c or a == d: continue
        tris = [(a, b, c), (a, c, d), (a, d, e)]
        if any(len(set(x)) < 3 for x in tris): continue
        cnt = 0
        for x in tris:
            sg = psign(x + (6 - sum(x),)) * ringtri_orient
            cnt += sg == 1
        out.add(cnt % 2)
    return out
if __name__ == '__main__':
    bad = 0; tot = 0; consts = Counter(); fanamb = 0
    for n in map(int, sys.argv[1:]):
        for line in open(GENTRI % n):
            rot = gentri_rotation(line)
            for h in range(len(rot)):
                if len(rot[h]) != 5: continue
                L = LSpace(rot, h); tot += 1
                # orientation of the hole pentagon as listed by rot[h] relative to the face orientation: use the face (h, L0, L1)
                fo = 1  # faces (v, r_i, r_{i+1}) are oriented, the pentagon x0..x4 in rot order is oriented the same way
                vals = set()
                for k in range(L.S):
                    s = L.sp.states[k]; w = tuple(s[i] for i in L.li)
                    fp = fill_parities(w, fo)
                    if len(fp) > 1: fanamb += 1
                    for f in fp: vals.add((L.stats(k, PERMS[0])[0] + f) % 2)
                if len(vals) != 1: bad += 1
                else: consts[(len(L.tri), vals.pop())] += 1
    print(json.dumps(dict(holes=tot, holes_formula_not_constant=bad, fan_choice_ambiguous_states=fanamb, const_by_ntri=sorted(consts.items()))))
