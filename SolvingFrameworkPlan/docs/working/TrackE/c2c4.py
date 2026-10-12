#!/usr/bin/env python3
"""[Track E, C2 + C4] Phase flip test and lock-chain involution on labelled 4-colourings of T - v.

usage: c2c4.py ORDER [first last]    (gentri census graphs, 1-based index range; every degree-5 hole; one orientation:
       the mirror maps every statistic to an equivalent one and leaves every swap graph isomorphic)

Per (graph, hole) one JSON line with:
  types[t] = {swaps, flip[stat] = #swaps with odd change (factor -1 for (-1)^stat, i.e. i^H for P), nz5 for rep,
              hull0: 0 in the F2 affine hull of the change vectors (=> NO F2-combination of ALL stats flips on every swap
              of type t), hull0_noio: same without the io_* cube-coordinate stats}
  bip[E] = #labelled Kempe classes in which the edge set E contains an odd cycle (=> NO function at all on colourings
           flips sign on every E-swap; any constant factor must be -1 because every E is closed under inversion)
  c4 = lock statistics of unfilled canonical states and well-definedness of the rule involutions
       R1: swap lock1 if it holds, else lock2;  R2: lock2 first.
Swap types: nolink / link1 / link2p (chains meeting the link in 0 / 1 / >=2 vertices, not whole-pair renamings),
  rename (component = whole {p,q}-subgraph), lock (a lock chain of an unfilled state), R1 (the R1 involution edges),
  all (every non-renaming chain).
"""
import sys, os, json, random, time
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase_lib import *

GENTRI = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/studiointel/gentri/tri%d.txt'

class PUF:
    def __init__(self, n): self.p = list(range(n)); self.x = [0] * n; self.bad = set()
    def f(self, a):
        path = []; px = 0
        while self.p[a] != a: path.append(a); a = self.p[a]
        # recompute parities along path
        root = a; acc = 0
        for y in reversed(path):
            acc ^= self.x[y]; self.x[y] = acc; self.p[y] = root
        return root
    def par(self, a): self.f(a); return self.x[a] if self.p[a] != a else 0
    def union(self, a, b, odd=1):
        ra, rb = self.f(a), self.f(b); pa = self.x[a] if a != ra else 0; pb = self.x[b] if b != rb else 0
        if ra == rb:
            if pa ^ pb != odd: self.bad.add(ra)
            return
        self.p[ra] = rb; self.x[ra] = pa ^ pb ^ odd
        if ra in self.bad: self.bad.discard(ra); self.bad.add(rb)
    def badroots(self): return {self.f(r) for r in self.bad}

def f2_hull_has_zero(vecs):
    """vecs: iterable of int bitmasks.  True iff 0 lies in the F2 affine hull, i.e. (0,1) in span{(v,1)}."""
    basis = {}   # pivot bit -> vector
    TOP = 1 << 200
    def reduce(x):
        while x:
            b = x.bit_length() - 1
            if b in basis: x ^= basis[b]
            else: return x
        return 0
    for v in vecs:
        x = reduce(v | TOP)
        if x: basis[x.bit_length() - 1] = x
    return reduce(TOP) == 0

def analyse(rot, h, rng):
    L = LSpace(rot, h); S = L.S; NN = S * 24
    st = {}
    def stats(node):
        if node not in st: st[node] = L.stats(node // 24, PERMS[node % 24])
        return st[node]
    lockset = [L.locks(k) for k in range(S)]
    def R(k, pref):
        lk = lockset[k]; a, b = (lk[0], lk[1]) if pref == 1 else (lk[1], lk[0])
        return a if a is not None else b
    TYPES = ['nolink', 'link1', 'link2p', 'rename', 'lock', 'R1', 'all', 'nl2', 'nl3', 'nl4', 'nl5', 'lock_nonrename']
    acc = {t: dict(swaps=0, flip=[0] * NS, nz5=0, D=set(), Dn=set()) for t in TYPES}
    iomask = 0
    for i, nme in enumerate(STAT_NAMES):
        if nme.startswith('io_'): iomask |= 1 << i
    full = PUF(NN)
    E_sets = ['lock', 'R1', 'all', 'nolink', 'link', 'chains_all_incl_rename'] + ['ab%d%d' % pq for pq in PAIRS] + \
             ['R1+ab%d%d' % pq for pq in PAIRS] + ['lock+ab%d%d' % pq for pq in PAIRS]
    # edge cubes: fixed edge e0 = (x0,y0) of T - v, cube pair = the two colours not on e0
    e0s = [e for e in L.E if e[0] in L.li and e[1] in L.li][:5]
    others = [e for e in L.E if not (e[0] in L.li or e[1] in L.li)]
    rng.shuffle(others); e0s += others[:5]
    E_sets += ['R1+e%d' % i for i in range(len(e0s))]
    puf = {E: PUF(NN) for E in E_sets}
    for k in range(S):
        locks = lockset[k]; r1 = R(k, 1)
        s = L.sp.states[k]
        for gi_, g in enumerate(PERMS):
            node = k * 24 + gi_; sv = stats(node)
            for pq in PAIRS:
                lab = tuple(sorted((g[pq[0]], g[pq[1]])))
                for K in L.comps[k][pq]:
                    k2, g2 = L.move(k, g, pq, K); node2 = k2 * 24 + PIDX[g2]
                    full.union(node, node2)
                    nl, allK = L.chain_type(k, pq, K)
                    types = []
                    if allK: types.append('rename')
                    else:
                        types.append('all'); types.append('nolink' if nl == 0 else ('link1' if nl == 1 else 'link2p'))
                        if nl >= 2: types.append('nl%d' % nl)
                    islock = (pq, K) in [x for x in locks if x is not None]
                    if islock: types.append('lock')
                    if islock and not allK: types.append('lock_nonrename')
                    if r1 is not None and r1 == (pq, K): types.append('R1')
                    tv = stats(node2); d = [b - a for a, b in zip(sv, tv)]
                    m2 = 0
                    for i, x in enumerate(d):
                        if x & 1: m2 |= 1 << i
                    for t in types:
                        A = acc[t]; A['swaps'] += 1
                        for i in range(NS):
                            if d[i] & 1: A['flip'][i] += 1
                        if d[SI['rep']] % 5: A['nz5'] += 1
                        A['D'].add(m2 & ~(1 << SI['fil'])); A['Dn'].add(m2 & ~(1 << SI['fil']) & ~iomask)
                    # edge sets
                    puf['chains_all_incl_rename'].union(node, node2)
                    if not allK: puf['all'].union(node, node2)
                    if nl == 0 and not allK: puf['nolink'].union(node, node2)
                    if nl > 0 and not allK: puf['link'].union(node, node2)
                    if islock: puf['lock'].union(node, node2)
                    if 'R1' in types:
                        puf['R1'].union(node, node2)
                        for p2 in PAIRS: puf['R1+ab%d%d' % p2].union(node, node2)
                        for i in range(len(e0s)): puf['R1+e%d' % i].union(node, node2)
                    if islock:
                        for p2 in PAIRS: puf['lock+ab%d%d' % p2].union(node, node2)
                    E = 'ab%d%d' % lab
                    puf[E].union(node, node2); puf['R1+' + E].union(node, node2); puf['lock+' + E].union(node, node2)
                    for i, (x0, y0) in enumerate(e0s):
                        cube = set(range(4)) - {s[x0], s[y0]}
                        if set(pq) == cube: puf['R1+e%d' % i].union(node, node2)
    # labelled Kempe classes
    croot = {}
    for x in range(NN): croot[x] = full.f(x)
    ncls = len(set(croot.values()))
    cid = {r: i for i, r in enumerate(sorted(set(croot.values())))}
    csize = Counter(cid[croot[x]] for x in range(NN))
    cunf = Counter(cid[croot[x]] for x in range(NN) if not L.sp.filled(x // 24))
    clock = Counter(cid[croot[x]] for x in range(NN) if R(x // 24, 1) is not None)
    bip = {}; bipcls = {}
    for E in E_sets:
        bad = puf[E].badroots(); cls_bad = sorted({cid[croot[x]] for x in range(NN) if puf[E].f(x) in bad})
        bip[E] = len(cls_bad); bipcls[E] = cls_bad
    classes = [dict(size=csize[i], unfilled=cunf[i], locked=clock[i]) for i in range(len(cid))]
    types_out = {}
    for t, A in acc.items():
        types_out[t] = dict(swaps=A['swaps'], flip={STAT_NAMES[i]: A['flip'][i] for i in range(NS)}, nz5=A['nz5'],
                            hull0=f2_hull_has_zero(A['D']) if A['D'] else None,
                            hull0_noio=f2_hull_has_zero(A['Dn']) if A['Dn'] else None)
    # C4 on canonical states
    c4 = Counter();
    for k in range(S):
        if L.sp.filled(k): continue
        lk = lockset[k]; c4['unfilled'] += 1
        c4[('none', 'L1only', 'L2only', 'DL')[(lk[0] is not None) + 2 * (lk[1] is not None)]] += 1
        for pref in (1, 2):
            r = R(k, pref)
            if r is None: continue
            k2, hmap = L.trans[k][r]
            if k2 == k: c4['R%d_canon_fixed' % pref] += 1
            # involution check at labelled level: apply to (k, id), then rule at result must return to (k, id)
            g = PERMS[0]; k2, g2 = L.move(k, g, *r); r2 = R(k2, pref)
            if r2 is None: c4['R%d_undefined_at_image' % pref] += 1; continue
            k3, g3 = L.move(k2, g2, *r2)
            if (k3, g3) != (k, g): c4['R%d_not_involution' % pref] += 1
            if L.sp.filled(k2): c4['R%d_image_filled' % pref] += 1
    return dict(S=S, labelled=NN, labelled_classes=ncls, tri=len(L.tri), types=types_out, bip=bip, bipcls=bipcls, classes=classes, c4=dict(c4),
                e0s=[[L.sp.order[a], L.sp.order[b]] for a, b in e0s])

if __name__ == '__main__':
    n = int(sys.argv[1]); lines = open(GENTRI % n).read().splitlines()
    a, b = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1, len(lines))
    rng = random.Random(n)
    for gi in range(a, b + 1):
        rot = gentri_rotation(lines[gi - 1])
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            t = time.time(); r = analyse(rot, h, rng)
            r.update(n=n, g=gi, hole=h, secs=round(time.time() - t, 2))
            print(json.dumps(r)); sys.stdout.flush()
