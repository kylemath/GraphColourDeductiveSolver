"""EXPLORE round 53, split and kill (coordinator 18:10Z, from the user's sprint plan): a face receiver row that has no
D/C window inside its 1.5-ball, extended one ring out by the degrees of its privates, and each extension attacked
separately.  The row fixes u (degree D), w_i (LK) and s_i (SV); one ring out = the privates p_i1..p_ik of each exact
non-5 link vertex w_i (k = w_i - 5), each 5..9 (9 = degree >= 9, never exact), so a row has 5^(#privates) fillings
(census50's slots).  With RING3=1 (default) the slots also hold the ring-3 vertices next to s_(i-1), s_i, s_(i+1)
of each 5-5-5 face w_i w_(i+1) s_i (the face's second ring beyond the row), each 5..9.  A filling is covered when the row's 2-ball holds a D/C configuration:
  1. registry containment (census50 / cen51 matcher: round 44's 582 RSST verified on two engines + explore's twoeng
     names; interior onto exact vertices or privates, a private's degree becoming a requirement), then
  2. engine windows: connected interiors of the exact vertices (u, w, s; letter 9 never) plus 1..KMAX privates at
     letters 5..8, free ring <= RMAX; order fewer privates, more fives, smaller ring.  kc -C (-t TSEC), a kc D re-run
     on dfast (ring <= 16) or dfast18, a kc C on cfast --fixed with kc's X (drive45's rule).  A window whose
     requirement is already covered (no uncovered filling in its cylinder) is skipped.
Coverage is the exact count of fillings in the union of the requirement cylinders (cen51.count).  Survivors are
reported per private (letters left), with the counts for every private >= 6 and >= 7, and whether the uncovered set
is a product of per-private letter sets.
Window names g<D>_<u|-><w>_<s>_<privates>: w and s as win45 (F/N when s_(i-1), s_i are in and w_i is not), then one
character per private in slot order (letter, or '.').
usage: python3 cen53.py D LK SV RMAX KMAX TSEC CAP_S   (TWOENG = dir of twoeng's k3x_D.out, k3x_C.cfast; NW workers,
default 3)  -> cen53_<D>_<LK>_<SV>.txt (appended), kc/dfast/cfast output in G_*.out, verdicts cached in G_res.txt"""
import sys, os, re, time, itertools, collections, subprocess, tempfile, threading
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait
H = os.path.dirname(os.path.abspath(__file__)); LOOP = os.path.join(H, '..')
sys.path.insert(0, os.path.join(LOOP, 'k51'))
import fam51 as F                     # registry(), extract(); its own sys.path brings rings and grow
from rings import Layered
import grow

def count(cyl, slots, lets=None):
    """Number of fillings of slots (letters lets, default LETS) inside the union of cylinders (cen51.count)."""
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
def covered(cyl, req): return any(all(req.get(k) == v for k, v in c.items()) for c in cyl)
def minimal(cyl):
    cyl = sorted(cyl, key=len); keep = []
    for c in cyl:
        if not any(all(c.get(k) == v for k, v in m.items()) for m in keep): keep.append(c)
    return keep
BIN = os.path.join(LOOP, '..', 'bin'); KCC = os.path.join(LOOP, 'kc', 'kcc')

class LZ(Layered):
    """Layered that also takes a ring vertex with out = 0 (a ring-3 five next to three ring-2 vertices): the vertex is
    closed off by the triangle on its two ring neighbours, which then count it as an inner neighbour."""
    def add_ring(self, degs):
        R = list(self.ring()); dg = dict(zip(R, degs))
        while True:
            out = [dg[x] - self.inn[x] - 2 for x in R]
            assert all(o >= 0 for o in out), ('out < 0', [dg[x] for x in R], [self.inn[x] for x in R])
            z = [j for j, o in enumerate(out) if o == 0]
            if not z: break
            j = z[0]; p, v, n = R[j - 1], R[j], R[(j + 1) % len(R)]
            assert len(R) > 3
            self.tris.append((p, v, n)); self.deg[v] = dg[v]; self.inn[p] += 1; self.inn[n] += 1; R.pop(j)
        self.rings[-1] = R
        Layered.add_ring(self, [dg[x] for x in R])

D, LK, SV = int(sys.argv[1]), [int(c) for c in sys.argv[2]], [int(c) for c in sys.argv[3]]
EX = {('u',): D}
EX.update({('w', i): LK[i] for i in range(D) if LK[i] != 9})
EX.update({('s', i): SV[i] for i in range(D) if SV[i] != 9})
SL2 = [('p', i, k) for i in range(D) if 6 <= LK[i] <= 8 for k in range(1, LK[i] - 4)]
FACES = [i for i in range(D) if LK[i] == 5 and LK[(i + 1) % D] == 5 and SV[i] == 5]   # 5-5-5 faces w_i w_i+1 s_i
J3 = sorted({(i + e) % D for i in FACES for e in (-1, 0, 1)}) if os.environ.get('RING3', '1') == '1' else []

def build(lets, want3=None):
    """The row's 3-ball: ring-2 letters s (SV) and privates, ring-3 letters for the named ring-3 vertices (lets;
    unspecified = 9), fresh ring 4.  A ring-3 vertex is named ('t', its ring-2 neighbours..., k), k counting
    repeats in ring order."""
    L = LZ(D); L.add_ring(list(LK))
    Wr = L.rings[1]; Z = L.ring(); adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2: i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else: i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    r2 = {('s', i): SV[i] for i in range(D)}; r2.update(lets)
    L.add_ring([r2.get(name[z], 9) for z in Z])
    adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    Z2 = set(Z); T = L.ring(); cnt = collections.Counter()
    for t in T:
        r = tuple(sorted(name[y] for y in adj[t] if y in Z2)); cnt[r] += 1; name[t] = ('t',) + r + (cnt[r],)
    L.add_ring([lets.get(name[t], 9) for t in T])
    adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    deg = {('u',): D}; deg.update({('w', i): LK[i] for i in range(D)}); deg.update(r2); deg.update(lets)
    for v, x in name.items():
        if x in deg and deg[x] != 9: assert len(adj[v]) == deg[x], (x, len(adj[v]), deg[x])
    return adj, name, {frozenset(t) for t in L.tris}

_a, _n, _f = build({})
SL3 = sorted({x for x in _n.values() if x[0] == 't' and any(y[0] == 's' and y[1] in J3 for y in x[1:-1])},
             key=lambda x: min(k for k, v in _n.items() if v == x))
SLOTS = SL2 + SL3
LETS = {x: (5, 6, 7, 8, 9) for x in SLOTS}
def sname(x): return 'p%d%d' % x[1:] if x[0] == 'p' else 't' + '/'.join(''.join(map(str, y)) for y in x[1:-1]) + ('#%d' % x[-1] if x[-1] > 1 else '')

def structure(EXp, SLp, LETp):
    """P = exact (EXp: the row's exact vertices plus slots fixed in this part) + free slots SLp, induced adjacency and
    faces by name; checked to be independent of the free slots' letters."""
    ref = None; fix = {x: v for x, v in EXp.items() if x in LETS}
    for fill in (9, 5, 6, 7, 8):
        lets = dict(fix); lets.update({x: (fill if fill in LETp[x] else min(LETp[x])) for x in SLp})
        adj, name, faces = build(lets)
        inv = {v: x for x, v in name.items()}; P = list(EXp) + SLp
        assert all(x in inv for x in P), [x for x in P if x not in inv]
        for x in EXp: assert len(adj[inv[x]]) == EXp[x], x
        pa = {x: {name[y] for y in adj[inv[x]] if name.get(y) in set(P)} for x in P}
        pf = {frozenset(name[y] for y in f) for f in faces if all(name.get(y) in set(P) for y in f)}
        if ref is None: ref = (P, pa, pf)
        else: assert ref[1] == pa and ref[2] == pf, 'structure depends on slot letters'
    return ref

def parts():
    """Split the fillings so each part has a letter-independent structure: a slot whose 5 changes the induced
    structure (a ring-3 five next to three ring-2 vertices closes off its two ring-3 neighbours) is fixed at 5 in
    one part and runs over 6..9 in the other.  Returns [(label, EXp, SLp, LETp)]."""
    def pa_of(lets):
        adj, name, _ = build(lets); inv = {v: x for x, v in name.items()}; P = list(EX) + SLOTS
        return {x: frozenset(name[y] for y in adj[inv[x]] if name.get(y) in set(P)) for x in P}
    base = pa_of({x: 9 for x in SLOTS}); dep = []
    for x in SLOTS:
        for l in (5, 6, 7, 8):
            lets = {y: 9 for y in SLOTS}; lets[x] = l
            if pa_of(lets) != base:
                assert l == 5, (x, l); dep.append(x); break
    out = []
    for fv in itertools.product((5, None), repeat=len(dep)):
        EXp = dict(EX); EXp.update({x: 5 for x, f in zip(dep, fv) if f == 5})
        SLp = [x for x in SLOTS if x not in EXp]
        LETp = {x: ((6, 7, 8, 9) if x in dep else LETS[x]) for x in SLp}
        lab = ' '.join('%s=%s' % (sname(x), '5' if f == 5 else '6-9') for x, f in zip(dep, fv)) or 'all'
        out.append((lab, EXp, SLp, LETp))
    return out

def gname(S, deg):
    w = ''.join(str(LK[j]) if ('w', j) in S else (('F' if LK[j] == 5 else 'N') if (('s', (j - 1) % D) in S and ('s', j) in S) else '.')
                for j in range(D))
    s = ''.join(str(SV[j]) if ('s', j) in S else '.' for j in range(D))
    p = ''.join(str(deg[x]) if x in S else '.' for x in SLOTS)
    return 'g%d_%s%s_%s_%s' % (D, 'u' if ('u',) in S else '-', w, s, p)

class Engines:
    """fam51.Engines with this round's files (G_kcc.out, G_df.out, G_cf.out, G_res.txt)."""
    def __init__(self, TSEC):
        self.T = TSEC; self.lock = threading.Lock()
        self.ko, self.do, self.co = (open(os.path.join(H, x), 'a') for x in ('G_kcc.out', 'G_df.out', 'G_cf.out'))
        self.res = {}; fr = os.path.join(H, 'G_res.txt')
        if os.path.exists(fr):
            for l in open(fr):
                f = l.rstrip('\n').split(' ', 2)
                if len(f) == 3: self.res[f[2]] = f[1]
        self.fr = open(fr, 'a')
    def run(self, cmd, inp=None):
        return subprocess.run(cmd, input=inp, capture_output=True, text=True).stdout.rstrip('\n')
    def verdict(self, line):
        k = line.split(' ', 1)[1]
        if k in self.res: return self.res[k]
        nm, r = line.split()[0], int(line.split()[1])
        o = self.run([KCC, '-C', '-s', '60', '-t', str(self.T)], line + '\n')
        with self.lock: self.ko.write(o + '\n'); self.ko.flush()
        v = 'none'
        if 'D=true' in o.split('\n')[0]:
            o2 = self.run([os.path.join(BIN, 'dfast' if r <= 16 else 'dfast18'), '/dev/stdin'], line + '\n')
            with self.lock: self.do.write(o2 + '\n'); self.do.flush()
            v = 'D' if 'D=true' in o2 else 'MISMATCH-D'
        m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', o)
        if v == 'none' and m:
            with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as t: t.write(line + '\n')
            o3 = self.run([os.path.join(BIN, 'cfast'), t.name, '--fixed', m.group(1)]); os.unlink(t.name)
            with self.lock: self.co.write(o3 + '\n'); self.co.flush()
            v = 'C{%s}' % m.group(1) if 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in o3 else 'CFAST-REJECTS'
        if v == 'none' and 'INCOMPLETE' in o.split('\n')[0]: v = 'timeout'
        with self.lock:
            self.res[k] = v; self.fr.write('%s %s %s\n' % (nm, v, k)); self.fr.flush()
        return v

def main():
    RMAX, KMAX, TSEC, CAP = (int(a) for a in sys.argv[4:8]); NW = int(os.environ.get('NW', '3')); TW = os.environ['TWOENG']
    log = open(os.path.join(H, 'cen53_%d_%s_%s.txt' % (D, sys.argv[2], sys.argv[3])), 'a')
    def say(*a):
        s = ' '.join(map(str, a)); print(s, flush=True); log.write(s + '\n'); log.flush()
    TOT = prod(len(LETS[x]) for x in SLOTS); PARTS = parts()
    say('# cen53 start %s: row %d %s/%s, %d slots %s, %d fillings in %d parts (%s), RMAX %d, KMAX %d, TSEC %d, cap %d s, registry %s' % (
        time.strftime('%H:%MZ', time.gmtime()), D, sys.argv[2], sys.argv[3], len(SLOTS), ' '.join(sname(x) for x in SLOTS),
        TOT, len(PARTS), '; '.join(p[0] for p in PARTS), RMAX, KMAX, TSEC, CAP, TW))
    REG, miss = F.registry(os.path.join(TW, 'k3x_D.out'), os.path.join(TW, 'k3x_C.cfast'))
    say('registry: %d configurations (%d names not found)' % (len(REG), miss))
    eng = Engines(TSEC); T0 = time.time(); bc = {}; done_all = [0, 0]
    for lab, EXp, SLp, LETp in PARTS:
        P, pa, pf = structure(EXp, SLp, LETp); PT = prod(len(LETp[x]) for x in SLp)
        fix = {x: v for x, v in EXp.items() if x in LETS}
        cyl = []; src = {}; inrow = []
        for c in REG:
            for e in grow.embeddings(c, P, pa, pf, EXp):
                req = {v: c[3][u] for u, v in e if v not in EXp}
                if not req: inrow.append(c[0])
                if all(l in LETp[x] and l != 9 for x, l in req.items()):
                    k = tuple(sorted(req.items(), key=repr)); cyl.append(dict(req)); src.setdefault(k, c[0])
        cyl = minimal(cyl); n0 = count(cyl, SLp, LETp)
        say('part %s (%d fillings): registry %d inside the fixed vertices; %d minimal requirements, covers %d (%.2f%%)%s' % (
            lab, PT, len(inrow), len(cyl), n0, 100.0 * n0 / PT, ' [%s]' % ' '.join(sorted(set(inrow))[:3]) if inrow else ''))
        for c in cyl[:40]: say('  reg %s | %s' % (' '.join('%s=%d' % (sname(k), v) for k, v in sorted(c.items(), key=repr)) or '(none)', src[tuple(sorted(c.items(), key=repr))]))
        idx = {x: k for k, x in enumerate(P)}
        def ring(S, lets):
            ll = dict(fix); ll.update(lets); key = tuple(sorted(ll.items(), key=repr))
            if key not in bc: bc[key] = build(ll)
            adj, name, _ = bc[key]; inv = {v: x for x, v in name.items()}; deg = dict(EXp); deg.update(lets)
            return F.extract(adj, [inv[x] for x in S], {inv[x]: deg[x] for x in S}), deg
        cand = []; seen = set()
        def grow_(S, ext):
            if S in seen: return
            seen.add(S); T = [x for x in SLp if x in S]
            if (T or any(x in fix for x in S)) and len(S) >= 3:
                c5, _ = ring(S, {x: min(LETp[x]) for x in T})      # a bigger slot letter never shrinks the ring
                if c5 and c5[0] <= RMAX:
                    for ls in itertools.product(*[[l for l in LETp[x] if l != 9] for x in T]):
                        lets = dict(zip(T, ls)); c, deg = ring(S, lets)
                        if c and c[0] <= RMAX:
                            nm = gname(S, deg)
                            cand.append((len(T), -sum(deg[x] == 5 for x in S), c[0], nm, lets, '%s %d %d %s %s' % ((nm,) + c)))
            for y in ext:
                if idx[y] > idx[min(S, key=lambda z: idx[z])] and (y not in LETp or len(T) < KMAX):
                    grow_(S | {y}, (ext | pa[y]) - S - {y})
        for x in P: grow_(frozenset([x]), frozenset(pa[x]))
        cand.sort(key=lambda w: w[:4])
        say('  engine windows: %d (connected subsets %d), by free slots %s, by ring %s' % (len(cand), len(seen),
            sorted(collections.Counter(w[0] for w in cand).items()), sorted(collections.Counter(w[2] for w in cand).items())))
        nrun = nskip = 0; kills = []; memo = {}; ver = [0]
        def gain(req):
            k = (ver[0], tuple(sorted(req.items(), key=repr)))
            if k not in memo:
                sub = {x: ((req[x],) if x in req else LETp[x]) for x in SLp}
                memo[k] = prod(len(sub[x]) for x in SLp) - count(cyl, SLp, sub)
            return memo[k]
        with ThreadPoolExecutor(NW) as ex:
            it = iter(cand); fut = {}
            def top():
                nonlocal nskip
                while len(fut) < NW and time.time() - T0 < CAP:
                    w = next(it, None)
                    if w is None: return
                    if covered(cyl, w[4]) or not gain(w[4]): nskip += 1; continue
                    fut[ex.submit(eng.verdict, w[5])] = w
            top()
            while fut:
                done, _ = wait(list(fut), return_when=FIRST_COMPLETED)
                for f in done:
                    w = fut.pop(f); v = f.result(); nrun += 1
                    if v.startswith('MISMATCH') or v == 'CFAST-REJECTS': say('  !! %s %s' % (v, w[3]))
                    if F.kills(v):
                        cyl.append(dict(w[4])); kills.append((w, v)); ver[0] += 1; say('  kill %s ring %d %s' % (v, w[2], w[3]))
                top()
        cyl = minimal(cyl); n1 = count(cyl, SLp, LETp); done_all[0] += n1; done_all[1] += PT
        say('  engines: %d windows run, %d skipped as covered, %d kills, %s; capped %s' % (nrun, nskip, len(kills),
            time.strftime('%H:%MZ', time.gmtime()), time.time() - T0 >= CAP))
        say('  coverage: registry %d + windows -> %d of %d (%.2f%%); uncovered %d' % (n0, n1, PT, 100.0 * n1 / PT, PT - n1))
        left = {}
        for x in SLp:
            byl = {l: prod(len(LETp[y]) for y in SLp if y != x) - count(
                [{k: v for k, v in c.items() if k != x} for c in cyl if c.get(x, l) == l], [y for y in SLp if y != x], LETp) for l in LETp[x]}
            left[x] = tuple(l for l in LETp[x] if byl[l]); say('  slot %-14s uncovered by letter %s' % (sname(x), byl))
        for lo, nm_ in ((6, 'every free slot >= 6'), (7, 'every free slot >= 7')):
            sub = {x: tuple(l for l in LETp[x] if l >= lo) for x in SLp}; nb = prod(len(sub[x]) for x in SLp)
            say('  fillings with %s: %d, uncovered %d' % (nm_, nb, nb - count(cyl, SLp, sub)))
        box = prod(len(left[x]) for x in SLp)
        say('  uncovered set %s the product of its letters per slot (%s; box %d)' % ('IS' if box == PT - n1 else 'is NOT',
            ' '.join('%s in %s' % (sname(x), ''.join(map(str, left[x]))) for x in SLp), box))
    say('total: %d of %d fillings covered (%.2f%%), uncovered %d' % (done_all[0], done_all[1], 100.0 * done_all[0] / done_all[1], done_all[1] - done_all[0]))
    say('# cen53 end %s' % time.strftime('%H:%MZ', time.gmtime()))

if __name__ == '__main__':
    main()
