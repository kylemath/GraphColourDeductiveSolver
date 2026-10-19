"""EXPLORE round 53b (Long Table 21:28Z, Opus s26r e6bf1acb): the 87 tightest one-ring-out survivors of the face binder
7665566/6675676 (Opus's orientation; the mirror of explore's 7665566/6765766).  Each is a full 3-ball: privates 666666,
ring 3 r0..r19 in Layered ring order (Opus's s26r/ball.py frame, checked here by its touch list), every ring-3 vertex 5
or 6 except t = r13 (next to s2, s3, s4) at 7, 8 or >= 9 (9 = >= 9: never exact, never in a window).  Ring 4 is free.
  1. registry containment of the whole exact 3-ball (cen53's matcher, census registry TWOENG);
  2. windows: connected subsets of the exact vertices with at most MMAX vertices, at least FMIN fives, free ring
     <= RMAX, shared across patterns by kc line; run in order more fives, smaller ring, then the patterns they serve;
     kc -C (-t TSEC), kc D on dfast (ring <= 16), kc C on cfast --fixed (cen53.Engines, cache T_res.txt).  A pattern
     dies at its first two-engine kill; windows serving only dead patterns are skipped.
Kill line (Long Table): all 87 survive ring <= RMAX.  A survivor here means: no D/C among the windows tried.
usage: python3 tight53.py TIGHT29 RMAX MMAX FMIN TSEC CAP_S   (TWOENG, NW as cen53) -> tight53.txt (appended)"""
import sys, os, time, collections
H = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[1:]
sys.argv = [os.path.join(H, 'cen53.py'), '7', '7665566', '6675676', '16', '2', '600', '0']
__file__ = os.path.join(H, 'cen53.py')
exec(open(__file__).read().replace("if __name__ == '__main__':\n    main()", ''))
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait
TOUCH = 'p61+s6 p01+s6 p01 p01+p02 p02 p02+s0 p11+s0 p11 p11+s1 p21+s1 p21 p21+s2 s2 s2+s3+s4 p51+s4 p51 p51+s5 s5 p61+s5 p61'.split()

def build3(r3):
    """3-ball: ring 2 = s (SV) + privates 6, ring 3 letters r3 (list, 9 = >= 9), fresh ring 4."""
    L = LZ(D); L.add_ring(list(LK)); Wr = L.rings[1]; Z = L.ring(); adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2: i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else: i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    r2 = {('s', i): SV[i] for i in range(D)}; r2.update({x: 6 for x in SL2})
    L.add_ring([r2[name[z]] for z in Z]); Z3 = list(L.ring()); Zs = set(Z)
    adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    for k, z in enumerate(Z3):
        name[z] = ('r', k)
        assert '+'.join(sorted('%s%s' % (y[0], ''.join(map(str, y[1:]))) for y in (name[v] for v in adj[z] if v in Zs))) == '+'.join(sorted(TOUCH[k].split('+'))), k
    L.add_ring(list(r3))
    adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    deg = {('u',): D}; deg.update({('w', i): LK[i] for i in range(D)}); deg.update(r2); deg.update({('r', k): r3[k] for k in range(len(r3))})
    inv = {v: x for x, v in name.items()}
    for x, d in deg.items():
        if d != 9: assert len(adj[inv[x]]) == d, x
    return adj, name, inv, deg, {frozenset(t) for t in L.tris}

def tname(S, deg):
    w = ''.join(str(LK[j]) if ('w', j) in S else (('F' if LK[j] == 5 else 'N') if (('s', (j - 1) % D) in S and ('s', j) in S) else '.') for j in range(D))
    s = ''.join(str(SV[j]) if ('s', j) in S else '.' for j in range(D))
    p = ''.join(str(deg[x]) if x in S else '.' for x in SL2)
    r = ''.join(str(deg[('r', k)]) if ('r', k) in S else '.' for k in range(20))
    return 'h%d_%s%s_%s_%s_%s' % (D, 'u' if ('u',) in S else '-', w, s, p, r)

def main():
    TF = ARGS[0]; RMAX, MMAX, FMIN, TSEC, CAP = (int(a) for a in ARGS[1:6])
    NW = int(os.environ.get('NW', '3')); TW = os.environ['TWOENG']
    base = [l.split()[0] for l in open(TF) if l[:1] in '56' and len(l.split()[0]) == 20]
    pats = [b[:13] + t + b[14:] for t in '789' for b in base]
    assert len(pats) == 87 and len(set(pats)) == 87
    log = open(os.path.join(H, os.environ.get('TOUT', 'tight53.txt')), 'a')
    def say(*a):
        s = ' '.join(map(str, a)); print(s, flush=True); log.write(s + '\n'); log.flush()
    say('# tight53 start %s: %d patterns from %s, RMAX %d, MMAX %d, FMIN %d, TSEC %d, cap %d s, registry %s' % (
        time.strftime('%H:%MZ', time.gmtime()), len(pats), TF, RMAX, MMAX, FMIN, TSEC, CAP, TW))
    REG, miss = F.registry(os.path.join(TW, 'k3x_D.out'), os.path.join(TW, 'k3x_C.cfast'))
    dead = {}; wins = {}
    for pt in pats:
        adj, name, inv, deg, faces = build3([int(c) for c in pt])
        V = [x for x in deg if deg[x] != 9]; Vs = set(V)
        pa = {x: {name[y] for y in adj[inv[x]] if name.get(y) in Vs} for x in V}
        pf = {frozenset(name[y] for y in f) for f in faces if all(name.get(y) in Vs for y in f)}
        fd = {x: deg[x] for x in V}
        for c in REG:
            if grow.embeddings(c, V, pa, pf, fd): dead[pt] = 'registry ' + c[0]; break
        if pt in dead: continue
        idx = {x: k for k, x in enumerate(V)}; seen = set()
        def grow_(S, ext):
            if S in seen: return
            seen.add(S)
            if len(S) >= 3 and sum(deg[x] == 5 for x in S) >= FMIN:
                I = [inv[x] for x in S]
                if len(set(y for v in I for y in adj[v]) - set(I)) <= RMAX:
                    c = F.extract(adj, I, {inv[x]: deg[x] for x in S})
                    if c and c[0] <= RMAX:
                        key = '%d %d %s %s' % c
                        if key not in wins: wins[key] = [sum(deg[x] == 5 for x in S), c[0], tname(S, deg), set()]
                        wins[key][3].add(pt)
            if len(S) >= MMAX: return
            lo = idx[min(S, key=lambda z: idx[z])]
            for y in ext:
                if idx[y] > lo: grow_(S | {y}, (ext | pa[y]) - S - {y})
        for x in V: grow_(frozenset([x]), frozenset(pa[x]))
    say('registry: %d configurations; %d patterns contain one: %s' % (len(REG), len(dead), ' '.join(sorted(dead))[:400]))
    order = sorted(wins.items(), key=lambda kv: (-kv[1][0], kv[1][1], -len(kv[1][3]), kv[1][2]))
    say('windows: %d distinct kc lines over the live patterns; by fives %s; by ring %s' % (len(order),
        sorted(collections.Counter(v[0] for _, v in order).items()), sorted(collections.Counter(v[1] for _, v in order).items())))
    eng = Engines(TSEC, 'T'); T0 = time.time(); nrun = nskip = 0
    if os.path.exists(os.path.join(H, 'G_res.txt')):    # cen53's verdicts on the same kc lines (read only)
        for l in open(os.path.join(H, 'G_res.txt')):
            f = l.rstrip('\n').split(' ', 2)
            if len(f) == 3: eng.res.setdefault(f[2], f[1])
    with ThreadPoolExecutor(NW) as ex:
        it = iter(order); fut = {}
        def top():
            nonlocal nskip
            while len(fut) < NW and time.time() - T0 < CAP:
                kv = next(it, None)
                if kv is None: return
                if all(p in dead for p in kv[1][3]): nskip += 1; continue
                fut[ex.submit(eng.verdict, kv[1][2] + ' ' + kv[0])] = kv
        top()
        while fut:
            done, _ = wait(list(fut), return_when=FIRST_COMPLETED)
            for f in done:
                key, w = fut.pop(f); v = f.result(); nrun += 1
                if v.startswith('MISMATCH') or v == 'CFAST-REJECTS': say('  !! %s %s' % (v, w[2]))
                if F.kills(v):
                    newd = sorted(p for p in w[3] if p not in dead)
                    for p in newd: dead[p] = '%s %s' % (v, w[2])
                    say('  kill %s ring %d fives %d %s -> %d patterns (%d dead)' % (v, w[1], w[0], w[2], len(newd), len(dead)))
            top()
    say('engines: %d windows run, %d skipped (patterns already dead), %s; capped %s' % (nrun, nskip,
        time.strftime('%H:%MZ', time.gmtime()), time.time() - T0 >= CAP))
    for t in '789':
        tp = [p for p in pats if p[13] == t]
        say('t = %s: %d of %d dead' % ('>=9' if t == '9' else t, sum(p in dead for p in tp), len(tp)))
    for p in pats:
        say('  %s %s' % (p, dead.get(p, 'SURVIVES')))
    say('# tight53 end %s' % time.strftime('%H:%MZ', time.gmtime()))

main()
