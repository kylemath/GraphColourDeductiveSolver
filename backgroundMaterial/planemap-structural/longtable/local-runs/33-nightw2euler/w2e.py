#!/usr/bin/env python3
"""[exploratory] NightW2Euler: six-pair rank/component bookkeeping on every DL window R3k2..R3k0 (positions 4..8)
at (5,5,5,5,6) holes, in the absolute colours of NightW2 §1 (alpha=1, mu=2, A=3, B=4 at R3k2).
Sources: jobak-66dump holes (orders 25-27, both orientations; all windows, Gamma and open), the p25#668 counterexample,
gentri orders given on the command line (open-run control).  One JSON line per window.  Single core."""
import sys, os, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../27-studio-positive-config/jobuv'))
sys.path.insert(0, os.path.join(HERE, '../32-nightsigmaimage'))
import uv_lib
from kempe_py import gentri_rotation
NM = {(3, 4): 0, (1, 1): 1, (3, 3): 2, (1, 0): 3, (3, 2): 4, (1, 4): 5, (3, 1): 6, (1, 3): 7, (3, 0): 8, (1, 2): 9}
# absolute link colours x0..x4 (x2 = p, the degree-6 link vertex) at positions 3..9 (NightW2 §1, §11.3)
LINK = {3: [4, 2, 1, 3, 1], 4: [1, 2, 1, 3, 4], 5: [1, 2, 3, 1, 4], 6: [2, 1, 3, 1, 4], 7: [2, 1, 3, 4, 1],
        8: [2, 3, 1, 4, 1], 9: [1, 3, 1, 4, 2]}
SWAP = {3: (1, 4), 4: (1, 3), 5: (1, 2), 6: (1, 4), 7: (1, 3), 8: (1, 2)}  # pair swapped by step pos -> pos+1
PAIRS = list(itertools.combinations((1, 2, 3, 4), 2))
def holes6(rot):
    for h, L in enumerate(rot):
        if len(L) != 5: continue
        if sorted(len(rot[x]) for x in L) != [5, 5, 5, 5, 6]: continue
        ring = set(u for x in L for u in rot[x]) - set(L) - {h}
        if len(ring) != 6: continue
        if sum(1 for a in ring for b in rot[a] if b in ring) != 12: continue
        yield h
def analyse(rot, h, tag, fo):
    uv_lib.load = lambda name, mirror: rot
    H = uv_lib.Hole('x', h, False); sp = H.sp
    q = next(t for t in range(5) if len(rot[H.L[t]]) == 6)
    X = [H.L[(q + t - 2) % 5] for t in range(5)]  # table names x0..x4
    edges = [(sp.idx[u], sp.idx[v]) for u in range(len(rot)) for v in rot[u] if u < v and h not in (u, v)]
    def pos(k):
        if not H.DL[k] and H.locks(k) is None: return None
        j, ty, hi, roles = H.frame(k); return NM.get((ty, (q - j) % 5))
    def absc(k, p):  # canonical colouring of state k -> absolute colours via the link table
        s = sp.states[k]; mp = {}
        for t in range(5):
            c = s[sp.idx[X[t]]]
            if mp.setdefault(c, LINK[p][t]) != LINK[p][t]: return None
        if len(set(mp.values())) != 4: return None
        return [mp[c] for c in s]
    def stats(a):
        out = {}
        for (x, y) in PAIRS:
            V = sum(1 for c in a if c in (x, y)); E = sum(1 for (u, v) in edges if {a[u], a[v]} == {x, y})
            cm = [0] * 5
            for i, c in enumerate(a): cm[c] |= 1 << i
            C = len(sp.components(tuple(c - 1 for c in a), x - 1, y - 1))
            out['%d%d' % (x, y)] = (E - V + C, C)
        return out
    for t in range(H.S):
        if pos(t) != 4 or not H.DL[t]: continue
        ks = {4: t}
        for i in range(5, 10): ks[i] = H.pi[ks[i - 1]]
        ks[3] = H.pinv[t]
        if not all(H.DL[ks[i]] for i in range(4, 9)): continue
        if [pos(ks[i]) for i in range(4, 9)] != [4, 5, 6, 7, 8]: continue
        rec = dict(tag=tag, hole=h, t=t, gamma=all(H.DL[x] for x in H.cycles[H.cyc[t]]), L=len(H.cycles[H.cyc[t]]),
                   fixed=[H.sigma(ks[i]) == ks[i] for i in (4, 6, 8)], DL={i: H.DL[ks[i]] for i in (3, 9)},
                   locks={i: H.locks(ks[i]) for i in (3, 9)})
        # DL run extent around the window
        b = 0; x = ks[3]
        while H.DL[x] and b < 400: b += 1; x = H.pinv[x]
        f = 0; x = ks[9]
        while H.DL[x] and f < 400: f += 1; x = H.pi[x]
        rec['back'], rec['fwd'] = b, f
        A = {}; ok = True
        for i in range(3, 10):
            if i in (3, 9) and pos(ks[i]) != i: continue
            a = absc(ks[i], i)
            if a is None: ok = False; break
            A[i] = a
        rec['ok'] = ok
        if ok:
            # verify each step is one swap of the tabulated pair on one component (up to the global renaming already fixed)
            for i in range(3, 9):
                if i not in A or i + 1 not in A: continue
                d = [v for v in range(sp.N) if A[i][v] != A[i + 1][v]]
                pr = set(SWAP[i])
                ok &= all(A[i][v] in pr and A[i + 1][v] in pr for v in d)
            rec['swapok'] = ok
            rec['st'] = {i: stats(A[i]) for i in A}
            rec['loc'] = {i: [H.locks(ks[i]), list(H.frame(ks[i])[3])] for i in A}
        fo.write(json.dumps(rec) + '\n')
if __name__ == '__main__':
    fo = open(sys.argv[2], 'w')
    if sys.argv[1] == 'dump':
        d = json.load(open(os.path.join(HERE, '../27-studio-positive-config/jobuv/jobak-66dump.json'))); seen = set()
        for r in d:
            key = (r['run'], r['name'], r['hole'])
            if key in seen: continue
            seen.add(key); analyse(r['rotation'], r['hole'], '%s:%s' % (r['run'], r['name']), fo); print(key, flush=True)
        ce = json.load(open(os.path.join(HERE, '../27-studio-positive-config/jobuv/jobak-counterexample.json')))
        analyse(ce['rotation_system'], ce['hole'], 'ce:' + ce['graph'], fo)
    else:
        G = os.path.join(HERE, '../../../studiointel/gentri/tri%d.txt')
        if not os.path.exists(G % 20): G = os.path.join(HERE, '../../studiointel/gentri/tri%d.txt')
        for n in [int(x) for x in sys.argv[1].split(',')]:
            for gi, l in enumerate(open(G % n)):
                if not l.startswith('G'): continue
                rot0 = gentri_rotation(l)
                for mir in (0, 1):
                    rot = [list(reversed(x)) for x in rot0] if mir else rot0
                    for h in holes6(rot): analyse(rot, h, 'g%d#%d%s' % (n, gi, 'm' if mir else ''), fo)
            print(n, flush=True)
