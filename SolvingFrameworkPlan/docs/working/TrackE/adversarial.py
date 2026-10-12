#!/usr/bin/env python3
"""[Track E] C2/C3'/C4 headline checks on single holes of large graphs (AW/BV constructions, census 66666 holes).
usage: adversarial.py --faces F.json [F2.json ...]     (hole from the file)
       adversarial.py --census ORDER --link66666        (every 66666 hole of the gentri census at ORDER)
Per hole: labelled classes; P-parity (i^H) a function of the ring word?; i^H class sums (S, S_U) and odd-renaming closure;
C4: canonical unfilled by lock type, R1 involution failures, lock-graph odd path components; R1+ab bipartiteness."""
import sys, json, time
from collections import Counter, defaultdict
from phase_lib import *
from c2c4 import PUF, GENTRI
IP = [1, 1j, -1, -1j]

def run(rot, h):
    L = LSpace(rot, h); S = L.S; NN = 24 * S; m = len(L.tri)
    locks = [L.locks(k) for k in range(S)]
    R1 = [lk[0] if lk[0] is not None else lk[1] for lk in locks]
    full = PUF(NN); pab = {pq: PUF(NN) for pq in PAIRS}; lockadj = defaultdict(set)
    for k in range(S):
        for gi, g in enumerate(PERMS):
            node = k * 24 + gi
            for pq in PAIRS:
                lab = tuple(sorted((g[pq[0]], g[pq[1]])))
                for K in L.comps[k][pq]:
                    k2, g2 = L.move(k, g, pq, K); n2 = k2 * 24 + PIDX[g2]
                    full.union(node, n2); pab[lab].union(node, n2)
                    if (pq, K) in [x for x in locks[k] if x is not None]: lockadj[node].add(n2); lockadj[n2].add(node)
                    if R1[k] == (pq, K):
                        for P2 in PAIRS: pab[P2].union(node, n2)
    croot = [full.f(x) for x in range(NN)]
    cls = sorted(set(croot)); res = dict(S=S, labelled_classes=len(cls))
    # i^H and ring function
    ring = defaultdict(set); sums = defaultdict(lambda: [0, 0]); ks = defaultdict(lambda: defaultdict(set))
    for k in range(S):
        s = L.sp.states[k]; fil = L.sp.filled(k)
        for gi, g in enumerate(PERMS):
            P = L.stats(k, g)[0]; ph = IP[(2 * P - m) % 4]; r = croot[k * 24 + gi]
            ring[tuple(g[s[i]] for i in L.li)].add(P % 2)
            sums[r][0] += ph
            if not fil: sums[r][1] += ph
            ks[r][k].add(gi)
    res['P_parity_not_ring_function_words'] = sum(len(v) > 1 for v in ring.values())
    res['iH_class_sums_zero'] = sum(1 for r in cls if abs(sums[r][0]) < 1e-9)
    res['iH_unfilled_sums_zero'] = sum(1 for r in cls if abs(sums[r][1]) < 1e-9)
    res['odd_renaming_closed_classes'] = sum(1 for r in cls if any(psign(compose(PERMS[a], inv(PERMS[b]))) < 0
                                                                for v in ks[r].values() for a in v for b in v))
    # C4
    c4 = Counter()
    for k in range(S):
        if L.sp.filled(k): continue
        lk = locks[k]; c4['unfilled'] += 1
        c4[('none', 'L1only', 'L2only', 'DL')[(lk[0] is not None) + 2 * (lk[1] is not None)]] += 1
        if R1[k] is not None:
            k2, g2 = L.move(k, PERMS[0], *R1[k])
            if k2 == k: c4['R1_canon_fixed'] += 1
            if R1[k2] is None or L.move(k2, g2, *R1[k2]) != (k, PERMS[0]): c4['R1_not_involution'] += 1
    seen = set()
    for x in lockadj:
        if x in seen: continue
        comp = [x]; seen.add(x)
        for y in comp:
            for z in lockadj[y]:
                if z not in seen: seen.add(z); comp.append(z)
        kind = 'cycle' if all(len(lockadj[y]) == 2 for y in comp) else 'path'
        c4[kind + '_components'] += 1
        if len(comp) % 2: c4[kind + '_components_odd'] += 1
    res['c4'] = dict(c4)
    lockedcls = {croot[k * 24 + gi] for k in range(S) if R1[k] is not None for gi in range(24)}
    res['locked_classes'] = len(lockedcls)
    res['R1+ab_bipartite_locked_classes'] = {'%d%d' % pq: len(lockedcls - {croot[x] for x in range(NN) if pab[pq].f(x) in pab[pq].badroots()})
                                             for pq in PAIRS}
    return res

if __name__ == '__main__':
    if sys.argv[1] == '--faces':
        sys.path.insert(0, '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/jobas')
        from flipsearch import rotation
        for fn in sys.argv[2:]:
            d = json.load(open(fn)); rot = rotation([tuple(t) for t in d['faces']]); h = d['hole']; t = time.time()
            r = run(rot, h); r.update(file=os.path.basename(fn), hole=h, linkdeg=[len(rot[x]) for x in rot[h]], secs=round(time.time() - t, 1))
            print(json.dumps(r)); sys.stdout.flush()
    else:
        n = int(sys.argv[2])
        for gi, line in enumerate(open(GENTRI % n)):
            rot = gentri_rotation(line)
            for h in range(len(rot)):
                if len(rot[h]) == 5 and all(len(rot[x]) == 6 for x in rot[h]):
                    t = time.time(); r = run(rot, h); r.update(n=n, g=gi + 1, hole=h, linkdeg=[6] * 5, secs=round(time.time() - t, 1))
                    print(json.dumps(r)); sys.stdout.flush()
