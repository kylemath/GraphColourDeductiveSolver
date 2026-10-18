"""EXPLORE round 46 part B: one ring of growth around a sender wheel (centre 5, link WORD), as round 42 did for R*.
2-ball: centre, link, ring 2 (the t_i between link vertices and the privates of big link vertices), all ring-2 letters
5..9 (9 = degree >= 9, never an exact match), fresh third ring.  Containment of round 44's 582 verified RSST
configurations (verdict D2 or C2cons in loop/k44/rsst_verdicts.txt) with round 42's embedding code (k42/grow.py):
exact degrees, induced, interior triangles onto faces.  Each embedding gives a requirement on the ring-2 slots; a
filling dies if it meets one.  Survivors are counted by a DFS over the slots.
usage: python3 grow46.py WORD   -> grow46_<WORD>.txt (requirements, survivor counts, survivor classes)"""
import sys, os, itertools, collections
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'k42'))
import grow
from rings import Layered
WORD = sys.argv[1]; LK = [int(c) for c in WORD]; D = 5; LET = (5, 6, 7, 8, 9)

def build(r2):
    L = Layered(D); L.add_ring(list(LK))
    Wr = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    name = {0: ('v',)}
    for i, w in enumerate(Wr): name[w] = ('x', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('t', j if (i, j) == (0, D - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    slots = [name[z] for z in Z]
    L.add_ring([r2.get(name[z], 9) for z in Z])
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj, name, {frozenset(t) for t in L.tris}, slots

def structure():
    ref = None; slots = build({})[3]
    for fill in ((6,) * len(slots), tuple(LET[k % 5] for k in range(len(slots))), (9,) * len(slots), (5,) * len(slots)):
        adj, name, faces, sl = build(dict(zip(slots, fill)))
        inv = {v: x for x, v in name.items()}
        P = [x for x in inv]
        pa = {x: {name[y] for y in adj[inv[x]] if y in name} for x in P}
        pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
        if ref is None: ref = (P, pa, pf)
        else: assert ref[1] == pa and ref[2] == pf, 'structure depends on ring-2 letters'
    return ref + (slots,)

def survivors(pats, n, let=LET):
    """count fillings in let^n meeting no requirement (tuple over slots, 0 = free); a few survivor classes"""
    ex = []
    def rec(k, pref, live):
        if any(all(p[j] == 0 for j in range(k, n)) for p in live): return 0   # a requirement fully met
        if not live:
            if len(ex) < 30: ex.append(''.join(map(str, pref)) + '*' * (n - k))
            return len(let) ** (n - k)
        tot = 0
        for a in let:
            tot += rec(k + 1, pref + [a], [p for p in live if p[k] == 0 or p[k] == a])
        return tot
    live = [p for p in pats if all(a == 0 or a in let for a in p)]
    return rec(0, [], live), ex

if __name__ == '__main__':
    P, pa, pf, slots = structure()
    fd = {('v',): 5}; fd.update({('x', i): LK[i] for i in range(D)})
    ok = {l.split()[0] for l in open(os.path.join(H, '..', 'k44', 'rsst_verdicts.txt')) if not l.startswith('#') and
          ('verdict=D2' in l.split() or 'verdict=C2cons' in l.split())}
    assert len(ok) == 582
    kcn = [l.split()[0] for l in open(os.path.join(H, '..', 'k44', 'rsst.txt')) if l.strip()]
    C = [(n,) + tuple(c[1:]) for n, c in zip(kcn, grow.rsst()) if n in ok]
    reqs = collections.defaultdict(set)
    for c in C:
        for e in grow.embeddings(c, P, pa, pf, fd):
            req = dict((v, c[3][u]) for u, v in e if v not in fd)
            reqs[tuple(req.get(x, 0) for x in slots)].add(c[0])
    n = len(slots); tot = 5 ** n
    # drop requirements implied by others (fewer constraints = stronger)
    keys = sorted(reqs, key=lambda k: (sum(1 for x in k if x), k)); keep = []
    for k in keys:
        if not any(all(a == 0 or a == b for a, b in zip(m, k)) for m in keep): keep.append(k)
    s, ex = survivors(keep, n); s6, _ = survivors(keep, n, (6, 7, 8, 9)); s7, _ = survivors(keep, n, (7, 8, 9))
    with open(os.path.join(H, 'grow46_%s.txt' % WORD), 'w') as o:
        o.write('# round 46 B: sender %s, ring-2 slots %s\n' % (WORD, ' '.join('%s%s' % (x[0], ''.join(map(str, x[1:]))) for x in slots)))
        o.write('# requirements %d (minimal %d) from %d configs; fillings %d; survivors %d (%.4f%%)\n' % (
            len(reqs), len(keep), len({c for v in reqs.values() for c in v}), tot, s, 100.0 * s / tot))
        o.write('# survivors with no 5 in ring 2: %d of %d; with every ring-2 letter >= 7: %d of %d\n' % (s6, 4 ** n, s7, 3 ** n))
        o.write('# first survivor classes (prefix, * = any of 5..9):\n' + ''.join('#   %s\n' % e for e in ex))
        for k in keep: o.write('%s | %s\n' % (''.join(str(a) if a else '.' for a in k), ' '.join(sorted(reqs[k])[:3])))
    print(WORD, 'slots', n, 'requirements', len(reqs), 'minimal', len(keep), 'survivors %d of %d (%.4f%%)' % (s, tot, 100.0 * s / tot),
          'no-5 survivors %d of %d, all->=7 survivors %d of %d' % (s6, 4 ** n, s7, 3 ** n))
