"""Stage 21 (RELAY_SPEC 17): sender 2-ball registry filter, drop-list builder.
usage: python3 sdrop.py EXDIR TD TC OUTPREFIX [reg=normal|empty|shift] [jobs=3] [lit=2000000] [words=w1,w2]
Writes OUTPREFIX.txt (dropped contexts: word H|F), OUTPREFIX_ctx.tsv (every context: word, bits, domain size, verdict,
literal-check status), OUTPREFIX_witness.txt (one witness completion per killer config per dropped context)."""
import sys, os, itertools, collections, json, pickle, hashlib, time, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
EX, TD, TC, OUT = sys.argv[1:5]
OPTS = dict(a.split('=', 1) for a in sys.argv[5:])
REG = OPTS.get('reg', 'normal'); JOBS = int(OPTS.get('jobs', '3')); LIT = int(OPTS.get('lit', '2000000'))
NEVER = 99
LOOP = os.path.join(EX, 'backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop')
F16 = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s22/f/s16_filter.py'
_argv = sys.argv
sys.argv = ['x', EX, TD, TC, '/dev/null']
G16 = {'__name__': 'lib', '__file__': F16}
exec(compile(open(F16).read().split("if __name__ == '__main__':")[0], F16, 'exec'), G16)
sys.argv = _argv
from rings import Layered
import grow

# ---------- engine contexts (identical loop to prelay2.R2_sender_rows with hat5, no zh/face5) ----------
def engine_env():
    root = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
    eng = os.path.join(HERE, 'pcheck.py'); sv = sys.argv
    sys.argv = [eng, 'none', 'xon', 'apexcls', 'filt16', 'hat5', 'root=' + root, 'work=' + os.path.join(HERE, 'work')]
    g = {'__name__': 'eng', '__file__': eng}
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(eng).read(), eng, 'exec'), g)
    sys.argv = sv
    return g
def contexts(g):
    out = []
    LET, CLS2, isR6 = g['LET'], g['CLS2'], g['isR6']
    for w in g['SENDERS']:
        n = 5; sixes = [k for k in range(n) if w[k] == 6]
        allow = {k: {(a_, q, b_) for a_ in LET for q in LET for b_ in LET if not isR6((5, w[(k + 1) % n], a_, q, b_, w[(k - 1) % n]))} for k in sixes}
        for hb in itertools.product((0, 1), repeat=5):
            H = dict(enumerate(hb))
            for fb in itertools.product((0, 1), repeat=len(sixes)):
                Fn = dict(zip(sixes, fb))
                if all(any((a_, q, b_) in allow[k] for a_ in CLS2[H[k]] for q in CLS2[Fn[k]] for b_ in CLS2[H[(k - 1) % n]]) for k in sixes):
                    out.append((''.join(map(str, w)), hb, fb))
    return out

# ---------- forbidden set ----------
def registry():
    cache = os.path.join(HERE, 'reg_A55.pkl')
    if os.path.exists(cache): C = pickle.load(open(cache, 'rb'))
    else: C = G16['registry'](); pickle.dump(C, open(cache, 'wb'))
    return C

# ---------- frame ----------
def build5(LK):
    D = 5; L = Layered(D); L.add_ring(list(LK)); Wr = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    name = {0: ('v',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2: i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else: i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    L.add_ring([9 for z in Z]); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    inv = {v: x for x, v in name.items()}
    pa = {x: {name[y] for y in adj[inv[x]] if y in name} for x in inv}
    pf = {frozenset(name[y] for y in f) for f in L.tris if all(y in name for y in f)}
    for i in range(5):
        assert ('w', i) in pa[('s', i)] and ('w', (i + 1) % 5) in pa[('s', i)]
        assert sum(1 for x in inv if x[0] == 'p' and x[1] == i) == max(LK[i], 5) - 5
    return list(inv), pa, pf

def word_reqs(wd, C):
    """requirement sets of one word: {frozenset((slot, deg)): [(config, image)]}; unknown vertices coded 99 in fd."""
    LK = [int(c) for c in wd]; P, pa, pf = build5(LK)
    fd = {('v',): 5}
    for i in range(5):
        fd[('w', i)] = LK[i] if LK[i] <= 8 else NEVER
    for x in P:
        if x[0] == 'p' and LK[x[1]] >= 9: fd[x] = NEVER
    R = collections.defaultdict(list)
    for c in C:
        for e_ in grow.embeddings(c, P, pa, pf, fd):
            img = tuple(v for u, v in e_)
            assert not any(fd.get(v) == NEVER for v in img)
            req = frozenset((v, c[3][u]) for u, v in e_ if v not in fd)
            R[req].append((c[0], img))
    free = sorted(x for x in P if x not in fd)
    return free, dict(R)

def domain(wd, hb, fb, free):
    LK = [int(c) for c in wd]; sixes = [k for k in range(5) if LK[k] == 6]
    SM, BG, ALL = (5, 6), (7, 8, NEVER), (5, 6, 7, 8, NEVER)
    dom = {}
    for x in free:
        if x[0] == 's': dom[x] = SM if hb[x[1]] == 0 else BG
        elif LK[x[1]] == 6: dom[x] = SM if fb[sixes.index(x[1])] == 0 else BG
        else: assert LK[x[1]] in (7, 8); dom[x] = ALL
    return dom

def covered(dom, reqs):
    """exact case split: True iff every completion in dom satisfies some req (req = dict slot->deg)."""
    reqs = [r for r in reqs if all(d in dom[v] for v, d in r.items())]
    if not reqs: return False
    for r in reqs:
        if all(len(dom[v]) == 1 for v in r): return True
    cnt = collections.Counter(v for r in reqs for v in r if len(dom[v]) > 1)
    x = max(cnt, key=lambda v: (cnt[v], str(v)))
    for val in dom[x]:
        d2 = dict(dom); d2[x] = (val,)
        if not covered(d2, reqs): return False
    return True

def literal(dom, reqs, free):
    """literal enumeration of every completion (numpy); returns number of uncovered completions."""
    doms = [dom[x] for x in free]
    if not doms: A = np.zeros((1, 0), dtype=np.int16)
    else:
        grids = np.meshgrid(*[np.array(d, dtype=np.int16) for d in doms], indexing='ij')
        A = np.stack([g_.ravel() for g_ in grids], axis=1)
    ix = {x: i for i, x in enumerate(free)}; hit = np.zeros(len(A), dtype=bool)
    for r in reqs:
        m = np.ones(len(A), dtype=bool)
        for v, d in r.items(): m &= A[:, ix[v]] == d
        hit |= m
    return int((~hit).sum()), len(A)

def do_word(args):
    wd, ctxs = args
    C = WC
    t0 = time.time(); free, R = word_reqs(wd, C)
    reqs = [dict(r) for r in R]; keys = list(R)
    res = []
    for _, hb, fb in ctxs:
        dom = domain(wd, hb, fb, free)
        size = 1
        for x in free: size *= len(dom[x])
        cv = covered(dom, reqs)
        lit = 'skip'
        if size <= LIT:
            nunc, n = literal(dom, reqs, free); assert n == size
            lit = 'agree' if (nunc == 0) == cv else 'DISAGREE(%d uncovered)' % nunc
        wit = []
        if cv:
            seen = set()
            for k, r in zip(keys, reqs):
                if not all(d in dom[v] for v, d in r.items()): continue
                for nm, img in R[k]:
                    if nm in seen: continue
                    seen.add(nm)
                    comp = {x: (r[x] if x in r else dom[x][0]) for x in free}
                    wit.append((nm, comp, img))
        res.append((wd, hb, fb, size, cv, lit, wit))
    return wd, len(R), time.time() - t0, res

def init(C):
    global WC; WC = C

if __name__ == '__main__':
    t0 = time.time()
    g = engine_env(); CT = contexts(g)
    if 'words' in OPTS: CT = [c for c in CT if c[0] in OPTS['words'].split(',')]
    C = registry()
    nm_md5 = hashlib.md5('\n'.join(sorted(c[0] for c in C)).encode()).hexdigest()
    if REG == 'empty': C = []
    elif REG == 'shift': C = [(c[0], c[1], c[2], {u: d + 1 for u, d in c[3].items()}, c[4], c[5]) for c in C]
    print('registry %s: %d configs (name-list md5 %s); %d contexts over %d words' % (REG, len(C), nm_md5, len(CT), len({c[0] for c in CT})), flush=True)
    byw = collections.defaultdict(list)
    for c in CT: byw[c[0]].append(c)
    import multiprocessing as mp
    tasks = sorted(byw.items())
    allres = []
    with mp.Pool(JOBS, initializer=init, initargs=(C,)) as pool:
        for i, (wd, nr, dt, res) in enumerate(pool.imap_unordered(do_word, tasks)):
            allres += res
            nd = sum(r[4] for r in res)
            print('  [%d/%d] %s: %d req sets, %d contexts, %d dropped, %.0fs' % (i + 1, len(tasks), wd, nr, len(res), nd, dt), flush=True)
    allres.sort(key=lambda r: (r[0], r[1], r[2]))
    bad = [r for r in allres if r[5].startswith('DISAGREE')]
    with open(OUT + '.txt', 'w') as f:
        for r in allres:
            if r[4]: f.write('%s %s|%s\n' % (r[0], ''.join(map(str, r[1])), ''.join(map(str, r[2]))))
    with open(OUT + '_ctx.tsv', 'w') as f:
        f.write('word\tH|F\tdomain\tverdict\tliteral\n')
        for r in allres: f.write('%s\t%s|%s\t%d\t%s\t%s\n' % (r[0], ''.join(map(str, r[1])), ''.join(map(str, r[2])), r[3], 'DROP' if r[4] else 'keep', r[5]))
    with open(OUT + '_witness.txt', 'w') as f:
        f.write('# context | config | completion (free vertex=letter, 99 = >=9) | embedding image\n')
        for r in allres:
            if not r[4]: continue
            for nm, comp, img in r[6]:
                cs = ' '.join('%s=%d' % (''.join(map(str, x)), comp[x]) for x in sorted(comp))
                im = ' '.join(''.join(map(str, x)) for x in img)
                f.write('%s %s|%s | %s | %s | %s\n' % (r[0], ''.join(map(str, r[1])), ''.join(map(str, r[2])), nm, cs, im))
    nd = sum(r[4] for r in allres); nl = sum(r[5] == 'agree' for r in allres)
    print('DONE: %d contexts, %d dropped; literal cross-check on %d contexts (domain <= %d): %d agree, %d DISAGREE; max domain %d; %.0fs'
          % (len(allres), nd, nl + len(bad), LIT, nl, len(bad), max(r[3] for r in allres), time.time() - t0))
    if bad:
        for r in bad[:10]: print('  DISAGREE', r[:4], r[5])
        sys.exit(2)
