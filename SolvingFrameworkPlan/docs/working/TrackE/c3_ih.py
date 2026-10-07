#!/usr/bin/env python3
"""[Track E, C3'] Class sums of the only C2/C4 survivor on lock swaps, phi = i^H (H = Heawood sum over faces of T - v),
on labelled 4-colourings of T - v.  Per labelled Kempe class K:
  S_lockedU = sum over locked unfilled (R1 domain; should be 0: R1 is a phi-flipping matching),
  S_unlockedU = sum over unfilled states with no lock (outside the involution's domain),
  S_U = sum over all unfilled, S = sum over K;  oddclosed = K contains c and tau c for an odd renaming tau
  (then sum_K phi = 0 automatically because phi o tau = -phi, H being odd).
usage: c3_ih.py ORDER [first last]  |  c3_ih.py --faces JSON HOLE  (AW/BV graphs)"""
import sys, json
from collections import defaultdict
from phase_lib import *
GENTRI = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/studiointel/gentri/tri%d.txt'
IP = [1, 1j, -1, -1j]

def run(rot, h):
    L = LSpace(rot, h); S = L.S; NN = 24 * S
    par = list(range(NN))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for k in range(S):
        for gi, g in enumerate(PERMS):
            for pq in PAIRS:
                for K in L.comps[k][pq]:
                    k2, g2 = L.move(k, g, pq, K); a, b = f(k * 24 + gi), f(k2 * 24 + PIDX[g2])
                    if a != b: par[a] = b
    m = len(L.tri)
    acc = defaultdict(lambda: dict(S=0, U=0, LU=0, NU=0, n=0, nU=0, nNU=0))
    members = defaultdict(set)
    for k in range(S):
        lk = L.locks(k); fil = L.sp.filled(k)
        for gi, g in enumerate(PERMS):
            P = L.stats(k, g)[0]; H = 2 * P - m; ph = IP[H % 4]
            A = acc[f(k * 24 + gi)]; A['S'] += ph; A['n'] += 1; members[f(k * 24 + gi)].add((k, gi))
            if not fil:
                A['U'] += ph; A['nU'] += 1
                if lk[0] is None and lk[1] is None: A['NU'] += ph; A['nNU'] += 1
                else: A['LU'] += ph
    out = []
    for r, A in acc.items():
        ks = defaultdict(set)
        for k, gi in members[r]: ks[k].add(gi)
        odd = any(psign(compose(PERMS[a], inv(PERMS[b]))) < 0 for v in ks.values() for a in v for b in v)
        c = lambda z: [round(z.real), round(z.imag)]
        out.append(dict(size=A['n'], unfilled=A['nU'], unlockedU=A['nNU'], S=c(A['S']), S_U=c(A['U']), S_lockedU=c(A['LU']),
                        S_unlockedU=c(A['NU']), oddclosed=odd))
    return out

if __name__ == '__main__':
    if sys.argv[1] == '--faces':
        sys.path.insert(0, '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/jobas')
        from flipsearch import rotation
        d = json.load(open(sys.argv[2])); rot = rotation([tuple(t) for t in d['faces']])
        hs = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [v for v in range(len(rot)) if len(rot[v]) == 5]
        for h in hs: print(json.dumps(dict(file=sys.argv[2], hole=h, classes=run(rot, h)))); sys.stdout.flush()
    else:
        n = int(sys.argv[1]); lines = open(GENTRI % n).read().splitlines()
        a, b = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1, len(lines))
        for gi in range(a, b + 1):
            rot = gentri_rotation(lines[gi - 1])
            for h in range(len(rot)):
                if len(rot[h]) == 5: print(json.dumps(dict(n=n, g=gi, hole=h, classes=run(rot, h)))); sys.stdout.flush()
