"""s37c: the forbidden cells of binder 7 8666655/5677657, exactly as explore's census cen54 (round 54b, 4770a564) counts
them, written out as requirement cylinders per structural part.  No engine is run: the registry part is cen54's own
containment (fam51.registry + grow.embeddings), the window part takes every enumerated window (KMAX 2, ring <= 16, the
three tiers) whose kc line has a two-engine kill in explore's cache (G_res.txt, which holds Studio's S_res.txt).
usage: python3 -I cyl37.py K53DIR TWOENGDIR OUT.json      (K53DIR = explore's loop/k53, from git archive 4770a564)"""
import sys, os, json, time, collections, itertools
K53, TW, OUT = sys.argv[1:4]
os.environ.update(J3S='3', FOCUS='3,6', TORDER='joint,single,6,3', ORDER='fives', RING3='1', TWOENG=TW)
SRC = os.path.join(K53, 'cen54.py')
g = {'__file__': SRC, '__name__': 'cen54_s37c'}
sys.argv = [SRC, '7', '8666655', '5677657', '16', '2', '600', '0']
exec(compile(open(SRC).read(), SRC, 'exec'), g)
DRIVER = r'''
RMAX, KMAX = 16, 2
t0 = time.time()
def say(*a): print(' '.join(map(str, a)), '[%.0fs]' % (time.time() - t0), flush=True)
RES = {}
for fn in ('G_res.txt', 'S_res.txt'):
    for l in open(os.path.join(H, fn)):
        f = l.rstrip('\n').split(' ', 2)
        if len(f) == 3: RES.setdefault(f[2], (f[0], f[1]))
PARTS = parts()
REG, miss = F.registry(os.path.join(TWOENG_, 'k3x_D.out'), os.path.join(TWOENG_, 'k3x_C.cfast'))
say('registry: %d configurations (%d names not found); slots %s; parts %s' % (len(REG), miss, [sname(x) for x in SLOTS], [p[0] for p in PARTS]))
bc = {}
def regpart(EXp, SLp, LETp):
    P, pa, pf = structure(EXp, SLp, LETp)
    cyl = []; src = {}
    for c in REG:
        for e in grow.embeddings(c, P, pa, pf, EXp):
            req = {v: c[3][u] for u, v in e if v not in EXp}
            if all(l in LETp[x] and l != 9 for x, l in req.items()):
                k = tuple(sorted(req.items(), key=repr)); cyl.append(dict(req)); src.setdefault(k, c[0])
    return P, pa, pf, cyl, src
def enum(P, pa, fix, EXp, SLp, LETp):
    idx = {x: k for k, x in enumerate(P)}
    A7 = {j: {x for x in pa[('s', j)] if x in LETS} for j in FOCUS}
    def ring(S, lets):
        ll = dict(fix); ll.update(lets); key = tuple(sorted(ll.items(), key=repr))
        if key not in bc:
            try: bc[key] = build(ll)
            except AssertionError: bc[key] = None
        deg = dict(EXp); deg.update(lets)
        if bc[key] is None: return None, deg
        adj, name, _ = bc[key]; inv = {v: x for x, v in name.items()}
        return F.extract(adj, [inv[x] for x in S], {inv[x]: deg[x] for x in S}), deg
    cand = []; seen = set()
    def grow_(S, ext):
        if S in seen: return
        seen.add(S); T = [x for x in SLp if x in S]
        if (T or any(x in fix for x in S)) and len(S) >= 3:
            c5, _ = ring(S, {x: min(LETp[x]) for x in T})
            if c5 and c5[0] <= RMAX:
                for ls in itertools.product(*[[l for l in LETp[x] if l != 9] for x in T]):
                    lets = dict(zip(T, ls)); c, deg = ring(S, lets)
                    if c and c[0] <= RMAX:
                        nm = gname(S, deg); key = '%d %d %s %s' % c; hit = key in RES
                        cls = ['joint'] if all(QF[j] & S for j in FOCUS) else []
                        cls += [str(j) for j in FOCUS if ('s', j) in S and len(A7[j] & S) >= 2]
                        if any(x in S for x in FOC): cls.append('single')
                        tier = 0 if hit else min((1 + TORD.index(c_) for c_ in cls if c_ in TORD), default=99)
                        if FOC and tier == 99: continue
                        cand.append((nm, lets, key, c[0], sorted(sname(x) if x in LETS else '%s%d' % (x[0], x[1]) if len(x) > 1 else 'u' for x in S)))
        for y in ext:
            if idx[y] > idx[min(S, key=lambda z: idx[z])] and (y not in LETp or len(T) < KMAX):
                grow_(S | {y}, (ext | pa[y]) - S - {y})
    for x in P: grow_(frozenset([x]), frozenset(pa[x]))
    return cand
out = []
for lab, EXp, SLp, LETp in PARTS:
    P, pa, pf, rcyl, src = regpart(EXp, SLp, LETp)
    PT = prod(len(LETp[x]) for x in SLp); rmin = minimal(rcyl); n0 = count(rmin, SLp, LETp)
    say('part %s: %d fillings; registry %d minimal requirements, covers %d (%.2f%%)' % (lab, PT, len(rmin), n0, 100.0 * n0 / PT))
    fix = {x: v for x, v in EXp.items() if x in LETS}
    wins = enum(P, pa, fix, EXp, SLp, LETp) if n0 < PT else []
    kills = [w for w in wins if F.kills(RES.get(w[2], ('', 'none'))[1])]
    kseen = {};
    for w in kills: kseen.setdefault(w[2], w)
    allc = minimal(rcyl + [dict(w[1]) for w in kills]); n1 = count(allc, SLp, LETp)
    say('   windows enumerated %d, cached %d, killing %d (distinct kc %d); coverage %d (%.2f%%), uncovered %d' % (
        len(wins), sum(1 for w in wins if w[2] in RES), len(kills), len(kseen), n1, 100.0 * n1 / PT, PT - n1))
    out.append({'part': lab, 'fixed': {sname(x): v for x, v in fix.items()}, 'free': [sname(x) for x in SLp],
                'letters': {sname(x): list(LETp[x]) for x in SLp}, 'fillings': PT, 'covered_registry': n0, 'covered': n1,
                'registry': [{'req': {sname(k): v for k, v in c.items()}, 'src': src[tuple(sorted(c.items(), key=repr))]} for c in rmin],
                'windows': [{'req': {sname(k): v for k, v in w[1].items()}, 'name': w[0], 'verdict': RES[w[2]][1], 'ring': w[3], 'kc': w[2], 'inside': w[4]} for w in kseen.values()]})
tot = sum(p['fillings'] for p in out); cov = sum(p['covered'] for p in out)
say('total: %d of %d covered (%.2f%%), uncovered %d' % (cov, tot, 100.0 * cov / tot, tot - cov))
json.dump({'row': '7 8666655/5677657', 'slots': [sname(x) for x in SLOTS], 'parts': out}, open(OUT_, 'w'), indent=0)
'''
g["TWOENG_"] = TW; g["OUT_"] = OUT; g["json"] = json
exec(DRIVER, g)
