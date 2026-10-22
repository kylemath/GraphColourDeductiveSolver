# E4: full level-preserving recursion on a sphere triangulation.
#   leaves: Voronoi cells (discs), each given a level (tau<=1) colouring.
#   merge(A,B): renaming + min-radius repair near conflicts (R), then re-level U = A u B by recolouring a
#   boundary collar of width w (w=0 if already level).  Final merge (two discs covering the sphere): repair only.
#   modes: 'bal' (greedy balanced matching rounds), 'lop' (one giant absorbs neighbours one by one).
#   variant 'plain': no re-levelling (leaves level only) -- control.
import sys, json, random, time, os
from lev import *
from e1_survey import graph
from e3_merge import level_col
from e3b_relevel import relevel
from pysat.solvers import Cadical153

def voronoi_cells(T, spacing, rng):
    n = len(T.adj); order = list(range(n)); rng.shuffle(order); seeds = []; cover = {}
    for v in order:
        if v in cover: continue
        seeds.append(v)
        for u, d in bfs(T.adj, v, spacing-1).items(): cover.setdefault(u, d)
    owner = {}; dist = {}; q = collections.deque()
    for i, s in enumerate(seeds): owner[s] = i; dist[s] = 0; q.append(s)
    while q:
        x = q.popleft()
        for y in T.adj[x]:
            if y not in owner: owner[y] = owner[x]; dist[y] = dist[x]+1; q.append(y)
    cells = [set() for _ in seeds]
    for v, i in owner.items(): cells[i].add(v)
    for it in range(100):
        bad = 0
        for i in range(len(cells)):
            c = cells[i]
            if not c or fast_disc(T, c): continue
            bad += 1
            try: S2 = Cluster(T, c).S
            except Exception: S2 = set()
            for v in list(c - S2):          # pendant / pinch vertices -> a neighbouring cell
                js = [owner[w] for w in T.adj[v] if owner[w] != i]
                if js: j = rng.choice(js); c.discard(v); cells[j].add(v); owner[v] = j
            for v in list(S2 - c):          # holes -> absorb
                cells[owner[v]].discard(v); c.add(v); owner[v] = i
        if bad == 0: break
    # leftover non-disc cells: absorb into a neighbouring cell when the union is a disc
    for i in range(len(cells)):
        if cells[i] and not fast_disc(T, cells[i]):
            js = set(owner[w] for v in cells[i] for w in T.adj[v] if owner[w] != i)
            for j in js:
                if cells[j] and fast_disc(T, cells[i] | cells[j]):
                    for v in cells[i]: owner[v] = j
                    cells[j] |= cells[i]; cells[i] = set(); break
    return [c for c in cells if c]

def sphere_repair(T, col, K, Rmax=12):
    n = len(T.adj)
    for R in range(Rmax+1):
        d = multi_bfs(T.adj, list(K), set(range(n)))
        free = [v for v in range(n) if d.get(v, 99) <= R]; fs = set(free)
        x = lambda v, c: 4*v+c+1; cls = []
        for v in free:
            cls.append([x(v, c) for c in range(4)])
            for w in T.adj[v]:
                for c in range(4):
                    if w in fs:
                        if w > v: cls.append([-x(v, c), -x(w, c)])
                    elif col[w] == c: cls.append([-x(v, c)])
        s = Cadical153(bootstrap_with=cls); ok = s.solve()
        if ok:
            mod = set(l for l in s.get_model() if l > 0); s.delete()
            for v in free: col[v] = next(c for c in range(4) if x(v, c) in mod)
            return R
        s.delete()
    return None

def final_merge(T, cells, col):
    A = cells[0]; B = cells[1]
    best = None
    for p in PERMS:
        c2 = dict(col)
        for v in B: c2[v] = p[col[v]]
        K = set(x for v in A for x in [v] + [w for w in T.adj[v] if w in B and c2[w] == c2[v]] if any(w in B and c2[w] == c2[v] for w in T.adj[v]))
        if best is None or len(K) < len(best[0]): best = (K, c2)
    K, c2 = best
    if not K: col.update(c2); return 0
    R = sphere_repair(T, c2, K); col.update(c2); return R

FAILS = []
STRICT = False
CHORDLESS = False
def run(name, mode, variant, seed, spacing=3, log=None):
    global STRICT
    T = graph(name); rng = random.Random(seed); n = len(T.adj)
    for attempt in range(20):
        cells = voronoi_cells(T, spacing, rng)
        cl = [disc_or_none(T, c) for c in cells]
        if all(c is not None for c in cl): break
    else:
        return dict(err='cells not discs')
    col = {}
    for c in cl: col.update(level_col(c, rng.randrange(10**6)))
    if variant == 'nolevel':     # control: leaves get unconstrained random colourings, no re-levelling
        for c in cl: col.update(rand_col(c, rng.randrange(10**6)))
    clusters = [c.S for c in cl]
    recs = []
    def do_merge(i, j, level):
        A, B = clusters[i], clusters[j]
        U = disc_or_none(T, A | B)
        if U is None: return False
        if STRICT and chords(U): return False
        cA = {v: col[v] for v in A}; cB = {v: col[v] for v in B}
        t0 = time.time()
        R, p, c = merge(T, A, B, cA, cB, U=U, Rmax=12)
        if R is None:
            recs.append(dict(level=level, nA=len(A), nB=len(B), R=None)); raise RuntimeError('merge failed')
        glued = dict(cA); glued.update({v: p[cB[v]] for v in B})
        zone = set(v for v in U.S if c[v] != glued[v])
        tau_before, t_before = U.tau(c)
        w = None
        if variant.startswith('level'):
            w, c2 = relevel(T, U, c, zone, wmax=12, K2={'level': 1.0, 'levelS': 3.0}[variant])
            if c2 is None:
                FAILS.append(dict(level=level, nA=len(A), nB=len(B), R=R, tau_before=tau_before, t_before=t_before, oddU=len(U.odd), chords=len(chords(U)), depth=max(multi_bfs(T.adj, U.walk, U.S).values())))
                pickle.dump(dict(name=name, A=A, B=B, c=c, zone=zone), open('fail_%s_%s_%d_%d.pkl' % (name, mode, seed, len(FAILS)), 'wb'))
                return False
            c = c2
        col.update(c)
        rec = dict(level=level, nA=len(A), nB=len(B), chords=len(chords(U)), changed=len(set(v for v in U.S if c[v] != glued[v])), nzone=len(zone), seam=sum(1 for (u, x) in U.edges if (u in A) != (x in A)), mU=U.m,
                   R=R, tau_before=round(tau_before, 3), t_before=t_before, w=w, tau_after=round(U.tau(c)[0], 3),
                   oddU=len(U.odd), sec=round(time.time()-t0, 1))
        recs.append(rec)
        if log: log.write(json.dumps(dict(name=name, mode=mode, variant=variant, seed=seed, **rec))+'\n'); log.flush()
        clusters[i] = A | B; clusters[j] = None
        return True
    level = 0
    try:
        if mode == 'bal':
            while sum(1 for c in clusters if c) > 2:
                level += 1
                alive = [i for i, c in enumerate(clusters) if c]
                own = {v: i for i in alive for v in clusters[i]}
                nb = {i: set() for i in alive}
                for i in alive:
                    for v in clusters[i]:
                        for w in T.adj[v]:
                            if own[w] != i: nb[i].add(own[w])
                order = sorted(alive, key=lambda i: (len(clusters[i]), rng.random()))
                used = set(); merged = 0
                for strict in ([True, False] if CHORDLESS else [False]):
                    STRICT = strict
                    for i in order:
                        if i in used or clusters[i] is None: continue
                        cand = sorted([j for j in nb[i] if j not in used and clusters[j] is not None], key=lambda j: (len(clusters[j]), rng.random()))
                        for j in cand:
                            if sum(1 for c in clusters if c) <= 2: break
                            if do_merge(i, j, level): used |= {i, j}; merged += 1; break
                    if merged: break
                if merged == 0: return dict(err='stuck', recs=recs)
        else:
            alive = [i for i, c in enumerate(clusters) if c]
            g = rng.choice(alive)
            while sum(1 for c in clusters if c) > 2:
                level += 1
                own = {v: i for i, c in enumerate(clusters) if c for v in c}
                nbs = list(set(own[w] for v in clusters[g] for w in T.adj[v] if own[w] != g)); rng.shuffle(nbs)
                ok = False
                for strict in ([True, False] if CHORDLESS else [False]):
                    STRICT = strict
                    for j in nbs:
                        if do_merge(g, j, level): ok = True; break
                    if ok: break
                if not ok:
                    # absorb a non-giant pair elsewhere to unblock
                    return dict(err='stuck', recs=recs)
        last = [c for c in clusters if c]
        Rf = final_merge(T, last, col)
    except RuntimeError as e:
        return dict(err=str(e), recs=recs)
    ok = all(col[u] != col[w] for u in range(n) for w in T.adj[u])
    return dict(recs=recs, R_final=Rf, final_sizes=[len(c) for c in last], proper=ok)

if __name__ == '__main__':
    name, mode, variant, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    CHORDLESS = len(sys.argv) > 5 and sys.argv[5] == 'chordless'
    os.makedirs('e4_logs', exist_ok=True)
    log = open('e4_logs/%s_%s_%s_%d%s.jsonl' % (name, mode, variant, seed, '_cl' if CHORDLESS else ''), 'w')
    t = time.time()
    res = run(name, mode, variant, seed, log=log)
    recs = res.get('recs', [])
    summ = dict(name=name, mode=mode, variant=variant, seed=seed, err=res.get('err'), R_final=res.get('R_final'),
                final_sizes=res.get('final_sizes'), proper=res.get('proper'), merges=len(recs),
                maxR=max([r['R'] for r in recs if r['R'] is not None], default=None),
                maxw=max([r['w'] for r in recs if r.get('w') is not None], default=None),
                hist_R=dict(collections.Counter(r['R'] for r in recs)), hist_w=dict(collections.Counter(r.get('w') for r in recs)),
                max_tau_before=max([r['tau_before'] for r in recs if 'tau_before' in r], default=None),
                max_tau_after=max([r['tau_after'] for r in recs if 'tau_after' in r], default=None), sec=round(time.time()-t),
                chordless=CHORDLESS, relevel_fails=FAILS, max_chords=max([r.get('chords', 0) for r in recs], default=0))
    print(json.dumps(summ), flush=True)
    open('e4_summary.jsonl', 'a').write(json.dumps(summ)+'\n')
