"""EXPLORE round 51 part 3 (Long Table, 07:08Z): the published set D of Inoue, Kawarabayashi, Miyashita, Mohar,
Thomassen, Thorup (arXiv:2603.24880; github.com/near-linear-4ct/reducible-configurations, MIT, 8200 .conf files)
against the face family of K=2 binder rows (d = 7: 7665566/6675666, 7655666/6756666, 7655667/6756656).
.conf format: blank line, 'n r', then one line per interior vertex r+1..n: 'v deg nbrs' (nbrs in cyclic order; ring
vertices 1..r in ring order).  Containment as round 42/44 (exact degrees, induced, interior triangles onto faces):
- row: gen44 patterns in the d = 7 1.5-ball, matched against each row (a hit kills the row outright);
- one ring out: census50-style 2-ball of each row (privates 5..9, 9 never exact): which cases a configuration covers.
Writes nl51_kc.txt (every configuration as a kc line, names nlNNNN_r<ring>), nl51_hits.txt (row hits and one-ring
requirements), and prints coverage of each row's one-ring cases by D alone and by D + this loop's registry.
usage: python3 -I nl51.py CONFDIR TWOENG_D TWOENG_C"""
import sys, os, re, glob, itertools, collections
H = os.path.dirname(os.path.abspath(__file__)); LOOP = os.path.join(H, '..')
sys.path.insert(0, os.path.join(LOOP, 'k42')); sys.path.insert(0, os.path.join(LOOP, 'k44'))
import grow, gen44
from rings import Layered
CD, TD, TC = sys.argv[1], sys.argv[2], sys.argv[3]
ROWS = [(7, '7665566', '6675666'), (7, '7655666', '6756666'), (7, '7655667', '6756656')]
LET = (5, 6, 7, 8, 9)

def parse(fn):
    L = open(fn).read().split('\n'); n, r = map(int, L[1].split()[:2])
    nb = {}
    for l in L[2:]:
        f = l.split()
        if f: nb[int(f[0])] = [int(x) for x in f[2:]]; assert int(f[1]) == len(f) - 2, fn
    U = list(range(r + 1, n + 1)); assert sorted(nb) == U, fn
    g = {u: len(nb[u]) for u in U}; E = {u: {w for w in nb[u] if w > r} for u in U}; tri = set()
    for u in U:
        for k in range(len(nb[u])):
            x, y = nb[u][k], nb[u][(k + 1) % len(nb[u])]
            if x > r and y > r: tri.add(frozenset((u, x, y)))
    # kc line: ring index v-1, interior index v-r-1, sorted lists; check the ring is a free-completion cycle
    rn = {v: set() for v in range(1, r + 1)}
    for u in U:
        for w in nb[u]:
            if w <= r: rn[w].add(u)
    ok = all(rn[v] for v in rn) and all(rn[v] & rn[v % r + 1] for v in rn)
    rp = ';'.join(','.join(str(w - 1) for w in sorted(x for x in nb[u] if x <= r)) or '-' for u in U)
    ip = ';'.join(','.join(str(w - r - 1) for w in sorted(x for x in nb[u] if x > r)) or '-' for u in U)
    return (U, g, E, tri), r, '%d %d %s %s' % (r, len(U), rp, ip), ok

def build(D, LK, SV, r2):
    L = Layered(D); L.add_ring([int(c) for c in LK])
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
    rr = {('s', i): int(SV[i]) for i in range(D)}; rr.update(r2)
    L.add_ring([rr.get(name[z], 9) for z in Z])
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj, name, {frozenset(t) for t in L.tris}, var

def ball2(D, LK, SV):
    var = build(D, LK, SV, {})[3]; ref = None
    for fill in ((6,) * len(var), tuple(LET[k % 5] for k in range(len(var))), (9,) * len(var), (5,) * len(var)):
        adj, name, faces, _ = build(D, LK, SV, dict(zip(var, fill)))
        inv = {v: x for x, v in name.items()}
        pa = {x: {name[y] for y in adj[inv[x]] if y in name} for x in inv}
        pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
        if ref is None: ref = (list(inv), pa, pf)
        else: assert ref[1] == pa and ref[2] == pf
    fd = {('u',): D}; fd.update({('w', i): int(LK[i]) for i in range(D)}); fd.update({('s', i): int(SV[i]) for i in range(D)})
    return ref + (var, fd)

def face_kite(c):
    """a degree-7 vertex x with interior 5-neighbours a, b (x a b a face) and a 5-vertex c with a b c a face"""
    U, g, E, tri = c
    for t in tri:
        for x in t:
            a, b = sorted(t - {x})
            if g[x] == 7 and g[a] == 5 and g[b] == 5 and any(g[y] == 5 for t2 in tri if {a, b} <= t2 for y in t2 - {a, b} if y != x):
                return True
    return False

if __name__ == '__main__':
    files = sorted(glob.glob(os.path.join(CD, 'D*.conf'))); assert len(files) == 8200, len(files)
    NL = []; bad = 0; kc = []
    for fn in files:
        c, r, line, ok = parse(fn); nm = 'nl%s_r%d' % (os.path.basename(fn)[1:5], r)
        bad += not ok; kc.append('%s %s' % (nm, line)); NL.append((nm, 'NL', ) + c)
    open(os.path.join(H, 'nl51_kc.txt'), 'w').write('\n'.join(kc) + '\n')
    fit = [c for c in NL if max(c[3].values()) <= 8 and len(c[2]) <= 21]
    kite = [c for c in fit if face_kite(c[2:])]
    print('configurations %d (ring not a free-completion cycle: %d); all degrees <= 8: %d; with a 7-5-5 / 5-5-5 kite: %d' % (
        len(NL), bad, len(fit), len(kite)))
    # registry configurations (as census50)
    ok44 = {l.split()[0] for l in open(os.path.join(LOOP, 'k44', 'rsst_verdicts.txt')) if not l.startswith('#') and
            ('verdict=D2' in l.split() or 'verdict=C2cons' in l.split())}
    kcn = [l.split()[0] for l in open(os.path.join(LOOP, 'k44', 'rsst.txt')) if l.strip()]
    REG = [(n,) + tuple(c[1:]) for n, c in zip(kcn, grow.rsst()) if n in ok44]
    want = {l.split()[0] for l in open(TD) if re.match(r'^[epf]\d+_', l)} | {l.split()[0] for l in open(TC) if re.match(r'^[epf]\d+_\S+ r=\d+ ', l)}
    got = {}; pat = re.compile(r'^([epf]\d+_\S+) (\d+) (\d+) (\S+) (\S+)$')
    for fn in sorted(glob.glob(os.path.join(LOOP, 'k[0-9]*', '*'))):
        if not os.path.isfile(fn): continue
        try:
            for l in open(fn):
                m = pat.match(l.rstrip('\n'))
                if m and m.group(1) in want and m.group(1) not in got: got[m.group(1)] = grow.kcline(l, 'explore')
        except UnicodeDecodeError: continue
    REG += list(got.values())
    out = open(os.path.join(H, 'nl51_hits.txt'), 'w')
    out.write('# round 51 part 3: published set D (8200) against the face family; registry = %d configurations\n' % len(REG))
    H7 = gen44.host(7)
    for d, lk, sv in ROWS:
        hits = []
        for c in fit:
            for phi, rq in gen44.embeddings(c, d, H7):
                F = gen44.pattern(d, c, phi, rq)
                if gen44.matches(d, F, lk, sv): hits.append((c[0], gen44.word(d, F))); break
        P, pa, pf, VAR, fd = ball2(d, lk, sv)
        reqs = collections.defaultdict(set)
        for src, CS in (('NL', fit), ('reg', REG)):
            for c in CS:
                for e in grow.embeddings(c, P, pa, pf, fd):
                    rq = dict((v, c[3][u]) for u, v in e if v not in fd)
                    reqs[tuple(rq.get(x, 0) for x in VAR)].add((src, c[0]))
        cases = list(itertools.product(LET, repeat=len(VAR)))
        def cov(srcs, sel):
            ks = [k for k, v in reqs.items() if any(s in srcs for s, _ in v)]
            dead = [c for c in cases if sel(c) and any(all(a == 0 or a == b for a, b in zip(k, c)) for k in ks)]
            return len(dead), sum(1 for c in cases if sel(c))
        surv = lambda c: min(c) >= 6     # census50 survivors are a subset of these (no private 5)
        line = '%s/%s: row hits %d %s | one ring out (%s): NL alone %d/%d, registry alone %d/%d, both %d/%d; no-5 cases: NL %d/%d, registry %d/%d, both %d/%d' % (
            lk, sv, len(hits), hits[:3], ' '.join('%s%s' % (x[0], ''.join(map(str, x[1:]))) for x in VAR),
            *cov(('NL',), lambda c: True), *cov(('reg',), lambda c: True), *cov(('NL', 'reg'), lambda c: True),
            *cov(('NL',), surv), *cov(('reg',), surv), *cov(('NL', 'reg'), surv))
        print(line); out.write('# ' + line + '\n')
        for k in sorted(reqs, key=lambda k: (sum(1 for a in k if a), k)):
            srcs = sorted(reqs[k])
            if any(s == 'NL' for s, _ in srcs):
                out.write('%s %s | %s\n' % (lk, ''.join(str(a) if a else '.' for a in k), ' '.join(n for _, n in srcs[:4])))
        out.flush()
