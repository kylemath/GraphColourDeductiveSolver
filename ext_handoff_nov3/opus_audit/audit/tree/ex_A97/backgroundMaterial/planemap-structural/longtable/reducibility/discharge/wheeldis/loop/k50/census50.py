"""EXPLORE round 50 (Long Table, 23:05Z): growth census of a receiver row one ring out, as round 42 did for R*.
The row fixes u, w_i and s_i.  One ring out = the privates of the non-5 link vertices (deg - 5 each), letters 5..9
(9 = degree >= 9, never an exact match); every filling is enumerated (for 7665566/6675666: 6 slots, 15,625 cases).
Forbidden = the verified registry as this loop sees it: round 44's 582 RSST configurations verified on two engines
(verdict D2 or C2cons), plus every explore name that out/job30/twoeng.py accepts (D on both engines, or C with the
same conservative X), read as configurations from their kc lines.  Containment as round 42 (k42/grow.embeddings):
exact degrees, induced, interior triangles onto faces.
usage: python3 census50.py D LK SV TWOENG_D TWOENG_C   -> census50_<D>_<LK>_<SV>.txt"""
import sys, os, re, glob, itertools, collections
H = os.path.dirname(os.path.abspath(__file__)); LOOP = os.path.join(H, '..')
sys.path.insert(0, os.path.join(LOOP, 'k42'))
import grow
from rings import Layered
D, LK, SV = int(sys.argv[1]), [int(c) for c in sys.argv[2]], [int(c) for c in sys.argv[3]]
TD, TC = sys.argv[4], sys.argv[5]; LET = (5, 6, 7, 8, 9)

def build(r2):
    L = Layered(D); L.add_ring(list(LK))
    Wr = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    var = [name[z] for z in Z if name[z][0] == 'p']
    r = {('s', i): SV[i] for i in range(D)}; r.update(r2)
    L.add_ring([r.get(name[z], 9) for z in Z])
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj, name, {frozenset(t) for t in L.tris}, var

def structure():
    ref = None; var = build({})[3]
    for fill in ((6,) * len(var), tuple(LET[k % 5] for k in range(len(var))), (9,) * len(var), (5,) * len(var)):
        adj, name, faces, _ = build(dict(zip(var, fill)))
        inv = {v: x for x, v in name.items()}
        pa = {x: {name[y] for y in adj[inv[x]] if y in name} for x in inv}
        pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
        if ref is None: ref = (list(inv), pa, pf)
        else: assert ref[1] == pa and ref[2] == pf, 'structure depends on ring-2 letters'
    return ref + (var,)

def registry():
    K44 = os.path.join(LOOP, 'k44')
    ok = {l.split()[0] for l in open(os.path.join(K44, 'rsst_verdicts.txt')) if not l.startswith('#') and
          ('verdict=D2' in l.split() or 'verdict=C2cons' in l.split())}
    assert len(ok) == 582
    kcn = [l.split()[0] for l in open(os.path.join(K44, 'rsst.txt')) if l.strip()]
    C = [(n,) + tuple(c[1:]) for n, c in zip(kcn, grow.rsst()) if n in ok]
    want = {l.split()[0] for l in open(TD) if re.match(r'^[epf]\d+_', l)} | \
           {l.split()[0] for l in open(TC) if re.match(r'^[epf]\d+_\S+ r=\d+ ', l)}
    got = {}; pat = re.compile(r'^([epf]\d+_\S+) (\d+) (\d+) (\S+) (\S+)$')
    for fn in sorted(glob.glob(os.path.join(LOOP, 'k[0-9]*', '*'))):
        if not os.path.isfile(fn): continue
        try:
            for l in open(fn):
                m = pat.match(l.rstrip('\n'))
                if m and m.group(1) in want and m.group(1) not in got: got[m.group(1)] = grow.kcline(l, 'explore')
        except UnicodeDecodeError: continue
    return C, list(got.values()), len(want), len(want) - len(got)

if __name__ == '__main__':
    P, pa, pf, VAR = structure()
    fd = {('u',): D}; fd.update({('w', i): LK[i] for i in range(D)}); fd.update({('s', i): SV[i] for i in range(D)})
    R, X, nwant, nmiss = registry()
    reqs = collections.defaultdict(set); direct = set()
    for src, CS in (('rsst', R), ('explore', X)):
        for c in CS:
            for e in grow.embeddings(c, P, pa, pf, fd):
                req = dict((v, c[3][u]) for u, v in e if v not in fd)
                if not req: direct.add(c[0])
                reqs[tuple(req.get(x, 0) for x in VAR)].add((src, c[0]))
    n = len(VAR); cases = list(itertools.product(LET, repeat=n))
    def dead(case, srcs):
        return any(all(a == 0 or a == b for a, b in zip(k, case)) for k in keys[srcs])
    keys = {}
    for srcs in (('rsst',), ('rsst', 'explore')):
        ks = [k for k, v in reqs.items() if any(s in srcs for s, _ in v)]
        ks.sort(key=lambda k: (sum(1 for a in k if a), k)); keep = []
        for k in ks:
            if not any(all(a == 0 or a == b for a, b in zip(m, k)) for m in keep): keep.append(k)
        keys[srcs] = keep
    groups = [('all', lambda c: True), ('with a 5 one ring out', lambda c: 5 in c), ('no 5', lambda c: 5 not in c),
              ('all >= 7', lambda c: min(c) >= 7), ('with a 9', lambda c: 9 in c)]
    rows = []
    for srcs in (('rsst',), ('rsst', 'explore')):
        dd = {c: dead(c, srcs) for c in cases}
        cols = []
        for g, f in groups:
            cs = [c for c in cases if f(c)]; k = sum(dd[c] for c in cs)
            cols.append('%s %d of %d (%.1f%%)' % (g, k, len(cs), 100.0 * k / len(cs) if cs else 0))
        rows.append(('+'.join(srcs), cols, [c for c in cases if not dd[c]]))
    out = os.path.join(H, 'census50_%d_%s_%s.txt' % (D, sys.argv[2], sys.argv[3]))
    with open(out, 'w') as o:
        o.write('# round 50 growth census: d %d link %s s %s; one ring out = slots %s, letters 5..9\n' % (
            D, sys.argv[2], sys.argv[3], ' '.join('%s%s' % (x[0], ''.join(map(str, x[1:]))) for x in VAR)))
        o.write('# registry: %d RSST (two-engine verified) + %d explore names (of %d twoeng names; %d without a kc line)\n' % (
            len(R), len(X), nwant, nmiss))
        o.write('# configurations contained in the row itself (no slot used): %s\n' % (' '.join(sorted(direct)) or 'none'))
        for nm, cols, sv in rows:
            o.write('# covered, %s: %s\n' % (nm, '; '.join(cols)))
        o.write('# survivors (registry), first 40: %s\n' % ' '.join(''.join(map(str, c)) for c in rows[1][2][:40]))
        for k in keys[('rsst', 'explore')]:
            o.write('%s | %s\n' % (''.join(str(a) if a else '.' for a in k), ' '.join(n_ for _, n_ in sorted(reqs[k])[:4])))
    for nm, cols, sv in rows: print(nm, '|', '; '.join(cols))
    print('direct:', sorted(direct)[:5], 'explore names', len(X), 'of', nwant)
