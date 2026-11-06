"""EXPLORE round 51, one-ring-out census of the surviving sender case (Long Table, 11:39Z): 55769 [0,0,1,0,0|0] in its
all-6 case (v = 5, link 5,5,7,6,>=9, H0 = H1 = H3 = H4 = 6, H2 big, F3 = 6).  Its 10 exact vertices have no D/C window
(fam51).  One ring out = the 13 vertices of that exact set's ring other than w4 (>= 9, never exact): the big hat H2
(7, 8, >= 9), the privates p21 p22 of w2 and p41 p44 of w4 next to H4/H3, and the 8 ring-3 vertices next to the exact
hats and fan (t_s4p44, t_s0s4, t_s0s1, t_s1p21, t_p31s2, t_p31, t_p31s3, t_p41s3), each 5..9 (9 = >= 9, never exact).
A filling is covered when the 3-ball contains a D/C configuration (interior = exact vertices plus slots at their
filled letters):
  1. registry containment (as census50: 582 RSST + explore twoeng names; interior onto exact or slot vertices,
     a slot's degree becoming a requirement), then
  2. engine windows: connected interiors with at least one slot, at most KMAX slots, free-completion ring <= RMAX,
     slot letters 5..8 (H2 7..8); order: fewer slots, more fives, smaller ring.  kc -C, kc D re-run on dfast, kc C
     on cfast --fixed (fam51.Engines; cache F_res.txt).  Windows whose requirement is already covered are skipped.
Coverage is the exact count of fillings (3 * 5^12) in the union of the requirement cylinders.
Window names p5_c<exact members>_<slot><letter>...
usage: python3 cen51.py RMAX KMAX TSEC CAP_S   (TWOENG = twoeng output dir; NW workers, default 3)"""
import sys, os, time, itertools, collections
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import fam51 as F
from rings import Layered
import grow
LK = [5, 5, 7, 6, 9]
EX = {('u',): 5, ('w', 0): 5, ('w', 1): 5, ('w', 2): 7, ('w', 3): 6,
      ('s', 0): 6, ('s', 1): 6, ('s', 3): 6, ('s', 4): 6, ('p', 3, 1): 6}
SL2 = [('s', 2), ('p', 2, 1), ('p', 2, 2), ('p', 4, 1), ('p', 4, 4)]
SL3 = [('t', ('p', 4, 4), ('s', 4)), ('t', ('s', 0), ('s', 4)), ('t', ('s', 0), ('s', 1)), ('t', ('p', 2, 1), ('s', 1)),
       ('t', ('p', 3, 1), ('s', 2)), ('t', ('p', 3, 1)), ('t', ('p', 3, 1), ('s', 3)), ('t', ('p', 4, 1), ('s', 3))]
SLOTS = SL2 + SL3
LETS = {x: ((7, 8, 9) if x == ('s', 2) else (5, 6, 7, 8, 9)) for x in SLOTS}

def build(lets):
    """v's 3-ball, ring-2 and ring-3 letters by name (exact, else lets, else 9), fresh ring 4.  Returns adj, name, faces."""
    L = Layered(5); L.add_ring(list(LK))
    Wr = L.rings[1]; Z = L.ring(); adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2: i, j = ws; name[z] = ('s', j if (i, j) == (0, 4) else i)
        else: i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    allv = dict(EX); allv.update(lets)
    L.add_ring([allv.get(name[z], 9) for z in Z])
    adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    Z2 = set(Z); T = L.ring()
    for t in T:
        r2 = tuple(sorted(name[y] for y in adj[t] if y in Z2))
        if r2 in [x[1:] for x in SL3]: name[t] = ('t',) + r2
    L.add_ring([allv.get(name.get(t), 9) for t in T])
    adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    return adj, name, {frozenset(t) for t in L.tris}

def structure():
    """P = exact + slots, induced adjacency and faces by name; checked to be letter-independent."""
    ref = None
    for fill in (9, 5, 6, 7):
        adj, name, faces = build({x: (fill if fill in LETS[x] else 7) for x in SLOTS})
        inv = {v: x for x, v in name.items()}; P = list(EX) + SLOTS
        assert all(x in inv for x in P), [x for x in P if x not in inv]
        pa = {x: {name[y] for y in adj[inv[x]] if name.get(y) in set(P)} for x in P}
        pf = {frozenset(name[y] for y in f) for f in faces if all(name.get(y) in set(P) for y in f)}
        if ref is None: ref = (P, pa, pf)
        else: assert ref[1] == pa and ref[2] == pf, 'structure depends on slot letters'
    return ref

def count(cyl, slots, lets=None):
    """Number of fillings of slots (letters lets, default LETS) inside the union of cylinders (dicts slot -> letter)."""
    lets = lets or LETS
    cyl = [c for c in cyl if all(v in lets[k] for k, v in c.items())]
    if not cyl: return 0
    if any(not c for c in cyl): return prod(len(lets[x]) for x in slots)
    fr = collections.Counter(x for c in cyl for x in c); x = max(slots, key=lambda s: fr[s])
    rest = [s for s in slots if s != x]; tot = 0
    for l in lets[x]:
        sub = [{k: v for k, v in c.items() if k != x} for c in cyl if c.get(x, l) == l]
        tot += count(sub, rest, lets)
    return tot
def prod(it):
    p = 1
    for v in it: p *= v
    return p

def covered(cyl, req):
    return any(all(req.get(k) == v for k, v in c.items()) for c in cyl)

def minimal(cyl):
    cyl = sorted(cyl, key=len); keep = []
    for c in cyl:
        if not any(all(c.get(k) == v for k, v in m.items()) for m in keep): keep.append(c)
    return keep

def sname(x): return ''.join(map(str, x)) if x[0] != 't' else 't' + '/'.join(''.join(map(str, y)) for y in x[1:])

def main():
    RMAX, KMAX, TSEC, CAP = (int(a) for a in sys.argv[1:5]); NW = int(os.environ.get('NW', '3')); TW = os.environ['TWOENG']
    log = open(os.path.join(H, 'cen51.txt'), 'a')
    def say(*a):
        s = ' '.join(map(str, a)); print(s, flush=True); log.write(s + '\n'); log.flush()
    P, pa, pf = structure(); TOT = prod(len(LETS[x]) for x in SLOTS)
    say('# cen51 start %s: 55769 [0,0,1,0,0|0] all-6, %d slots, %d fillings, RMAX %d, KMAX %d, TSEC %d, cap %d s' % (
        time.strftime('%H:%MZ', time.gmtime()), len(SLOTS), TOT, RMAX, KMAX, TSEC, CAP))
    REG, miss = F.registry(os.path.join(TW, 'k3x_D.out'), os.path.join(TW, 'k3x_C.cfast'))
    cyl = []; src = {}
    for c in REG:
        for e in grow.embeddings(c, P, pa, pf, EX):
            req = {v: c[3][u] for u, v in e if v not in EX}
            if all(l in LETS[x] and l != 9 for x, l in req.items()):
                k = tuple(sorted(req.items())); cyl.append(dict(req)); src.setdefault(k, c[0])
    cyl = minimal(cyl); n0 = count(cyl, SLOTS)
    say('registry (%d configurations): %d minimal requirements, covers %d of %d fillings (%.2f%%)' % (len(REG), len(cyl), n0, TOT, 100.0 * n0 / TOT))
    for c in cyl[:30]: say('  reg %s | %s' % (' '.join('%s=%d' % (sname(k), v) for k, v in sorted(c.items())), src[tuple(sorted(c.items()))]))
    # engine windows
    idx = {x: k for k, x in enumerate(P)}; bc = {}
    def ring(S, lets):
        key = tuple(sorted(lets.items()))
        if key not in bc: bc[key] = build(lets)
        adj, name, _ = bc[key]; inv = {v: x for x, v in name.items()}; deg = dict(EX); deg.update(lets)
        return F.extract(adj, [inv[x] for x in S], {inv[x]: deg[x] for x in S})
    cand = []; seen = set()
    def grow_(S, ext):
        if S in seen: return
        seen.add(S); T = [x for x in S if x in LETS]
        if T and len(S) >= 3:
            for ls in itertools.product(*[[l for l in LETS[x] if l != 9] for x in T]):
                lets = dict(zip(T, ls)); c = ring(S, lets)
                if c and c[0] <= RMAX:
                    nm = 'p5_c%s_%s' % ('.'.join(sname(x) for x in sorted(S - set(T), key=lambda z: idx[z])),
                                       '.'.join('%s%d' % (sname(x), lets[x]) for x in T))
                    cand.append((len(T), -sum(v == 5 for v in ls), c[0], nm, lets, '%s %d %d %s %s' % ((nm,) + c)))
        for y in ext:
            if idx[y] > idx[min(S, key=lambda z: idx[z])] and (y not in LETS or len(T) < KMAX):
                grow_(S | {y}, (ext | pa[y]) - S - {y})
    for x in P: grow_(frozenset([x]), frozenset(pa[x]))
    cand.sort(key=lambda w: w[:4])
    say('engine windows: %d (connected subsets %d), by slots %s, by ring %s' % (len(cand), len(seen),
        sorted(collections.Counter(w[0] for w in cand).items()), sorted(collections.Counter(w[2] for w in cand).items())))
    eng = F.Engines(TSEC); T0 = time.time(); nrun = nskip = 0; kills = []
    with ThreadPoolExecutor(NW) as ex:
        it = iter(cand); fut = {}
        def top():
            nonlocal nskip
            while len(fut) < NW and time.time() - T0 < CAP:
                w = next(it, None)
                if w is None: return
                if covered(cyl, w[4]): nskip += 1; continue
                fut[ex.submit(eng.verdict, w[5])] = w
        top()
        while fut:
            done, _ = wait(list(fut), return_when=FIRST_COMPLETED)
            for f in done:
                w = fut.pop(f); v = f.result(); nrun += 1
                if v.startswith('MISMATCH') or v == 'CFAST-REJECTS': say('  !! %s %s' % (v, w[3]))
                if F.kills(v):
                    cyl.append(dict(w[4])); kills.append((w, v)); say('  kill %s ring %d %s' % (v, w[2], w[3]))
            top()
    cyl = minimal(cyl); n1 = count(cyl, SLOTS)
    say('engines: %d windows run, %d skipped as covered, %d kills, %s; capped %s' % (nrun, nskip, len(kills),
        time.strftime('%H:%MZ', time.gmtime()), time.time() - T0 >= CAP))
    say('coverage: registry %d + windows -> %d of %d fillings (%.2f%%); uncovered %d' % (n0, n1, TOT, 100.0 * n1 / TOT, TOT - n1))
    # what is left: per slot, the letters that occur in uncovered fillings, and the uncovered count with every slot >= 7
    for x in SLOTS:
        say('  slot %-12s uncovered by letter %s' % (sname(x), {l: prod(len(LETS[y]) for y in SLOTS if y != x) - count(
            [{k: v for k, v in c.items() if k != x} for c in cyl if c.get(x, l) == l], [y for y in SLOTS if y != x]) for l in LETS[x]}))
    for lo, nm_ in ((6, 'every slot >= 6'), (7, 'every slot >= 7')):
        sub = {x: tuple(l for l in LETS[x] if l >= lo) for x in SLOTS}; nb = prod(len(sub[x]) for x in SLOTS)
        say('  fillings with %s: %d, uncovered %d' % (nm_, nb, nb - count(cyl, SLOTS, sub)))
    no5 = [x for x in SLOTS if all(c.get(x) != 5 for c in cyl)]
    say('  slots never at 5 in any covering requirement: %s' % ' '.join(sname(x) for x in no5))
    say('# cen51 end %s' % time.strftime('%H:%MZ', time.gmtime()))

if __name__ == '__main__':
    main()
