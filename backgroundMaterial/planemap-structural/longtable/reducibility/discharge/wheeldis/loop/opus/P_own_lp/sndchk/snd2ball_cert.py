"""sender five 2-ball containment: for each context (word, H, F) enumerate exact completions and test the forbidden set."""
import sys, os, itertools, collections, json, pickle
EX, TD, TC, TAG = sys.argv[1:5]
F16 = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s22/f/s16_filter.py'
sys.argv = ['x', EX, TD, TC, '/dev/null']
g = {'__name__': 'lib', '__file__': F16}
exec(compile(open(F16).read().split("if __name__ == '__main__':")[0], F16, 'exec'), g)
from rings import Layered
import grow
cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reg_%s.pkl' % TAG)
if os.path.exists(cache): C = pickle.load(open(cache, 'rb'))
else: C = g['registry'](); pickle.dump(C, open(cache, 'wb'))
print('forbidden set', len(C), flush=True)
NEVER = 99
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
    return list(inv), pa, pf
def reqs(wd):
    LK = [int(c) for c in wd]; P, pa, pf = build5(LK)
    # sanity: s_i adjacent to w_i and w_{i+1}
    for i in range(5): assert ('w', i) in pa[('s', i)] and ('w', (i + 1) % 5) in pa[('s', i)], (i, pa[('s', i)])
    fd = {('v',): 5}
    for i in range(5): fd[('w', i)] = LK[i]
    R = collections.defaultdict(set)
    for c in C:
        for e_ in grow.embeddings(c, P, pa, pf, fd):
            req = tuple(sorted((v, c[3][u]) for u, v in e_ if v not in fd))
            R[req].add(c[0])
    return P, R
SM, BG = (5, 6), (7, 8, NEVER)
def run(wd, H, F, R, P):
    LK = [int(c) for c in wd]; sixes = [k for k in range(5) if LK[k] == 6]
    slots = sorted(x for x in P if x[0] in ('s', 'p'))
    dom = {}
    for x in slots:
        if x[0] == 's': dom[x] = SM if H[x[1]] == 0 else BG
        elif LK[x[1]] == 6: dom[x] = SM if F[sixes.index(x[1])] == 0 else BG
        else: dom[x] = (5, 6, 7, 8, NEVER)          # privates of a big spoke: not in the context, free
    keys = list(dom); n = 0; alive = []; used = collections.Counter()
    for vals in itertools.product(*[dom[k] for k in keys]):
        a = dict(zip(keys, vals)); n += 1; hit = None
        for req, nms in R.items():
            if all(a[v] == d for v, d in req): hit = (req, nms); break
        if hit is None: alive.append(a)
        else: used[min(hit[1])] += 1
    return n, alive, used

CJ = json.load(open(os.environ['CJ'])); RR = {}; tot = 0.0; deadw = 0.0
for r in CJ:
    wd = r['word']
    if wd not in RR: RR[wd] = reqs(wd)
    P, R = RR[wd]; st = []
    for H, F in r['ctx']:
        n, alive, used = run(wd, H, F, R, P); st.append((n, len(alive)))
    dead = all(a == 0 for n, a in st); tot += r['w']; deadw += r['w'] if dead else 0
    print('%s H=%s F=%s w=%.6f  %s  %s' % (wd, r['H'], r['F'], r['w'], 'DEAD' if dead else 'live', st), flush=True)
print('total sender weight %.6f, on 2-ball-dead rows %.6f' % (tot, deadw))
