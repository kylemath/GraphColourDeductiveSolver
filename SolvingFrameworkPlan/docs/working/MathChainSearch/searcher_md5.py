#!/usr/bin/env python3
"""Searcher for the SECOND pre-registered F-chain search (Conjecture L, global minimum degree >= 5). [computed, exploratory]
Copy of searcher.py with ONLY these changes (per messages/2026-10-06/..._conjecture-L-falsified-as-stated.md, 'Next'):
 - every triangulation has minimum degree >= 5 throughout: flips require both ends of the flipped edge to have degree >= 6 (so the
   flipped edge's ends lose one and stay >= 5; x,y gain one); seeds are min-degree-5 triangulations built by build_md5 below.
 - seed construction (build_md5): start at the icosahedron (n=12); apply n-12 random vertex splits (a vertex u with an arc of m>=2 consecutive
   neighbours; the arc goes to a new vertex u' joined to u; may temporarily create degree-3/4 vertices); then repair by a random walk of edge flips
   minimising the deficiency sum max(0,5-deg) (accept if not worse, else with prob 0.02), up to 30000 steps; retry from scratch on failure.
   Then 25n further random flips that keep min degree >=5 (randomisation). No plantri, no discs.
 - n=13 is excluded: no triangulation of the sphere with 13 vertices and minimum degree 5 exists (known; empirically confirmed by test_n13 in this file's
   --test13 option: repair never reaches deficiency 0). Band A therefore uses orders 12,14..19. v = random degree-5 vertex (all neighbours then have degree>=5).
Original docstring follows.
Searcher for the pre-registered F-chain search (Conjecture L). [computed, exploratory]
Design fixed by messages/2026-10-06/..._PREREGISTRATION-conjecture-L-chain-search.md.
Usage: searcher.py --band A|B|C [--workers 2] [--cpu-budget 540] [--seeds 100000] [--steps 3000]
Bands (orders): A 12-19, B 20-29, C 30-40.
Interpretations of unspecified points (declared, not tuned):
 - a state is a proper 4-colouring of T-v whose link of v (5-cycle) uses four colours (one non-adjacent repeat pair x_j,x_{j+2});
 - lock 1: x_{j+1} and x_{j+3} in the same {c_{j+1},c_{j+3}}-Kempe component of T-v; lock 2: x_{j+1}, x_{j+4} in the same {c_{j+1},c_{j+4}} component;
 - F: swap the {c_j,c_{j+3}}-component of x_{j+2}; chain length = number of consecutive doubly locked terms s,F(s),... starting at s;
 - tie-break: number of doubly locked terms among the first 8 iterates F^0..F^7 (iterates continue past an unlocked term as long as the state stays valid);
 - hill climbing accepts a move if (length, tiebreak) is not lower (plateau moves accepted); moves: flip an edge with both ends outside N[v] (keeping a proper
   colouring, simple graph, ends keep degree>=3), or one random Kempe swap on T-v; a move producing an invalid state is rejected.
"""
import argparse, json, os, random, sys, time
from multiprocessing import Process

BANDS = {'A': (12, 19), 'B': (20, 29), 'C': (30, 40)}
CAP = 40  # chain length cap (reported as >=CAP)
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- triangulation as rotation system ----------
def build(n, rng):
    rot = {0: [1, 2], 1: [2, 0], 2: [0, 1]}
    # two-triangle sphere: faces (0,1,2) and (0,2,1)
    rot = {0: [1, 2], 1: [2, 0], 2: [0, 1]}
    faces = [(0, 1, 2), (0, 2, 1)]
    for w in range(3, n):
        a, b, c = faces.pop(rng.randrange(len(faces)))
        rot[w] = [a, b, c]
        i = rot[a].index(c); rot[a].insert(i, w)
        i = rot[b].index(a); rot[b].insert(i, w)
        i = rot[c].index(b); rot[c].insert(i, w)
        faces += [(a, b, w), (b, c, w), (c, a, w)]
    return rot

def flip_info(rot, a, b):
    ra = rot[a]; rb = rot[b]
    x = rb[rb.index(a) - 1]
    y = ra[ra.index(b) - 1]
    return x, y

def do_flip(rot, a, b):
    x, y = flip_info(rot, a, b)
    rot[a].remove(b); rot[b].remove(a)
    i = rot[x].index(b); rot[x].insert(i, y)
    i = rot[y].index(a); rot[y].insert(i, x)
    return x, y

def edges_of(rot):
    return [(u, w) for u in rot for w in rot[u] if u < w]

def validate(rot):
    n = len(rot); E = sum(len(r) for r in rot.values()) // 2
    if E != 3 * n - 6: return False
    for u in rot:
        if len(set(rot[u])) != len(rot[u]) or u in rot[u]: return False
        for w in rot[u]:
            if u not in rot[w]: return False
    seen = set(); F = 0
    for u in rot:
        for w in rot[u]:
            if (u, w) in seen: continue
            F += 1; d = (u, w); L = 0
            while d not in seen:
                seen.add(d); a, b = d
                rb = rot[b]; d = (b, rb[rb.index(a) - 1]); L += 1
            if L != 3: return False
    return n - E + F == 2

# ---------- states, F, locks ----------
class Inst:
    def __init__(self, rot, v, col):
        self.rot = rot; self.v = v; self.col = col
        self.link = list(rot[v])
        self.adj = {u: [w for w in rot[u] if w != v] for u in rot if u != v}
    def refresh(self, us):
        for u in us: self.adj[u] = [w for w in self.rot[u] if w != self.v]

def comp(adj, col, s, c1, c2):
    seen = {s}; st = [s]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen and (col[w] == c1 or col[w] == c2):
                seen.add(w); st.append(w)
    return seen

def repeat_index(col, link):
    cs = [col[x] for x in link]
    if len(set(cs)) != 4: return None
    for j in range(5):
        if cs[j] == cs[(j + 2) % 5]: return j
    return None

def doubly_locked(adj, col, link, j):
    x1, x3, x4 = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]
    b, g, d = col[x1], col[x3], col[x4]
    return (x3 in comp(adj, col, x1, b, g)) and (x4 in comp(adj, col, x1, b, d))

def apply_F(adj, col, link, j):
    x2 = link[(j + 2) % 5]
    a, g = col[link[j]], col[link[(j + 3) % 5]]
    K = comp(adj, col, x2, a, g)
    new = list(col)
    for u in K: new[u] = g if col[u] == a else a
    return new

def evaluate(adj, col, link):
    """returns (chain length, locked count among first 8 iterates, chain terms) """
    L = 0; cnt = 0; c = col; broken = False
    for it in range(max(CAP, 8)):
        j = repeat_index(c, link)
        if j is None: break
        lk = doubly_locked(adj, c, link, j)
        if lk:
            if not broken: L += 1
            if it < 8: cnt += 1
        else:
            broken = True
            if it >= 8: break
        if broken and it >= 7: break
        if L >= CAP: break
        c = apply_F(adj, c, link, j)
    return L, cnt

def kempe_swap(adj, col, u, d):
    c1 = col[u]
    K = comp(adj, col, u, c1, d)
    new = list(col)
    for w in K: new[w] = d if col[w] == c1 else c1
    return new

def initial_colouring(adj, v, n, rng):
    verts = [u for u in range(n) if u != v]
    for _ in range(200):
        col = [-1] * n
        order = verts[:]; rng.shuffle(order)
        # DSATUR-like with backtracking limit
        def sat(u): return {col[w] for w in adj[u] if col[w] >= 0}
        stack = []; ok = True; steps = 0
        un = set(verts)
        def pick():
            return max(un, key=lambda u: (len(sat(u)), rng.random()))
        def solve():
            nonlocal steps
            if not un: return True
            steps += 1
            if steps > 20000: return False
            u = pick(); un.discard(u)
            cs = [c for c in range(4) if c not in sat(u)]; rng.shuffle(cs)
            for c in cs:
                col[u] = c
                if solve(): return True
            col[u] = -1; un.add(u); return False
        sys.setrecursionlimit(10000)
        if solve(): return col
    return None

ICO = None
def icosahedron():
    adj = {0: set(range(1, 6)), 11: set(range(6, 11))}
    for i in range(5):
        adj[1 + i] = {0, 1 + (i + 1) % 5, 1 + (i - 1) % 5, 6 + i, 6 + (i - 1) % 5}
        adj[6 + i] = {11, 6 + (i + 1) % 5, 6 + (i - 1) % 5, 1 + i, 1 + (i + 1) % 5}
    cyc = {}
    for u, ns in adj.items():   # cyclic order of link 5-cycle
        ns = set(ns); o = [min(ns)]
        while len(o) < 5:
            o.append(min(w for w in ns if w not in o and w in adj[o[-1]] and (len(o) > 1 or True) and w != o[-1]))
        cyc[u] = o
    for mask in range(1 << 12):
        rot = {u: (cyc[u][::-1] if mask >> u & 1 else list(cyc[u])) for u in adj}
        if validate(rot): return rot
    raise RuntimeError('icosahedron construction failed')

def vertex_split(rot, rng):
    u = rng.choice(list(rot.keys())); ns = rot[u]; d = len(ns)
    if d < 4: return False
    i = rng.randrange(d); m = rng.randint(2, d - 1)
    arc = [ns[(i + k) % d] for k in range(m)]
    rest = [ns[(i + m + k) % d] for k in range(d - m)]   # from after arc to before arc
    w = max(rot) + 1
    a, b = arc[0], arc[-1]
    snap = {k: list(v) for k, v in rot.items()}
    for ordr in ((0, 0), (0, 1), (1, 0), (1, 1)):
        rot.clear(); rot.update({k: list(v) for k, v in snap.items()})
        rot[w] = arc + [u]
        rot[u] = [a, w] + [b] + rest   # a, w, b, rest...
        for x in arc[1:-1]:
            rot[x] = [w if y == u else y for y in rot[x]]
        for x, o in ((a, ordr[0]), (b, ordr[1])):
            r = rot[x]; k = r.index(u); r[k:k + 1] = [u, w] if o == 0 else [w, u]
        if validate(rot): return True
    rot.clear(); rot.update(snap); return False

def deficiency(rot): return sum(max(0, 5 - len(r)) for r in rot.values())

def build_md5(n, rng):
    for attempt in range(200):
        rot = icosahedron(); ok = True
        while len(rot) < n:
            if not vertex_split(rot, rng): ok = False; break
        if not ok: continue
        D = deficiency(rot); keys = list(rot.keys())
        for step in range(30000):
            if D == 0: break
            a = rng.choice(keys); b = rng.choice(rot[a])
            if len(rot[a]) < 4 or len(rot[b]) < 4: continue
            x, y = flip_info(rot, a, b)
            if x == y or y in rot[x]: continue
            dD = sum(max(0, 5 - len(rot[t]) - dl) - max(0, 5 - len(rot[t])) for t, dl in ((a, -1), (b, -1), (x, 1), (y, 1)))
            if dD <= 0 or rng.random() < 0.02:
                do_flip(rot, a, b); D += dD
        if D != 0: continue
        for _ in range(25 * n):
            a = rng.choice(keys); b = rng.choice(rot[a])
            if len(rot[a]) < 6 or len(rot[b]) < 6: continue
            x, y = flip_info(rot, a, b)
            if x == y or y in rot[x]: continue
            do_flip(rot, a, b)
        if validate(rot) and min(len(r) for r in rot.values()) >= 5: return rot
    return None

def make_instance(n, rng):
    for _ in range(50):
        rot = build_md5(n, rng)
        if rot is None: return None
        cands = [u for u in rot if len(rot[u]) == 5]
        if not cands: continue
        v = rng.choice(cands)
        inst = Inst(rot, v, None)
        col = initial_colouring(inst.adj, v, n, rng)
        if col is None: continue
        for _ in range(60 * n):
            u = rng.choice([w for w in range(n) if w != v]); d = rng.randrange(4)
            if d == col[u]: continue
            nc = kempe_swap(inst.adj, col, u, d)
            if len({nc[x] for x in inst.link}) == 4 or len({col[x] for x in inst.link}) != 4: col = nc
        if len({col[x] for x in inst.link}) != 4: continue
        inst.col = col
        return inst
    return None

def run_seed(band, seed, steps):
    t0 = time.process_time()
    lo, hi = BANDS[band]
    rng = random.Random(f"md5-{band}-{seed}")
    n = rng.choice([k for k in range(lo, hi + 1) if k != 13])
    inst = make_instance(n, rng)
    if inst is None:
        return dict(band=band, seed=seed, status='no-instance', n=n, cpu_s=time.process_time() - t0)
    rot, v, link = inst.rot, inst.v, inst.link
    col = inst.col
    cur = evaluate(inst.adj, col, link)
    best = cur; bestcert = None
    hist_eval = {}; hist_cur_end = None
    nacc = nflip = nkemp = 0
    def cert(c, L):
        return dict(n=n, v=v, link=link, rot={str(u): list(rot[u]) for u in rot}, colour=c, claimed_length=L)
    bestcert = cert(list(col), cur[0]) if cur[0] >= 4 else None
    for st in range(steps):
        if rng.random() < 0.5:
            a = rng.choice(list(rot.keys())); b = rng.choice(rot[a])
            if a == v or b == v or a in link or b in link: continue
            if len(rot[a]) < 6 or len(rot[b]) < 6: continue
            x, y = flip_info(rot, a, b)
            if x == y or y in rot[x] or col[x] == col[y]: continue
            saved = {u: list(rot[u]) for u in (a, b, x, y)}
            do_flip(rot, a, b); inst.refresh((a, b, x, y)); nflip += 1
            new = evaluate(inst.adj, col, link)
            hist_eval[new[0]] = hist_eval.get(new[0], 0) + 1
            if new >= cur:
                cur = new; nacc += 1
            else:
                for u in saved: rot[u] = saved[u]
                inst.refresh((a, b, x, y))
        else:
            u = rng.choice([w for w in range(n) if w != v]); d = rng.randrange(4)
            if d == col[u]: continue
            nc = kempe_swap(inst.adj, col, u, d); nkemp += 1
            if len({nc[x] for x in link}) != 4: continue
            new = evaluate(inst.adj, nc, link)
            hist_eval[new[0]] = hist_eval.get(new[0], 0) + 1
            if new >= cur:
                cur = new; col = nc; nacc += 1
        if cur > best:
            best = cur
            if cur[0] >= 4: bestcert = cert(list(col), cur[0])
    assert validate(rot)
    out = dict(band=band, seed=seed, status='done', n=n, v=v, steps=steps, best_len=best[0], best_tiebreak=best[1],
               final_len=cur[0], accepted=nacc, flips_tried=nflip, kempe_tried=nkemp,
               eval_hist={str(k): c for k, c in sorted(hist_eval.items())}, cpu_s=time.process_time() - t0,
               certificate=bestcert)
    return out

def atomic_write(path, obj):
    tmp = path + '.tmp%d' % os.getpid()
    with open(tmp, 'w') as f: json.dump(obj, f)
    os.replace(tmp, path)

def worker(band, w, nw, budget_each, nseeds, steps, outdir):
    used = 0.0; maxcost = 0.0
    for fn in os.listdir(outdir):
        if fn.startswith('seed_') and fn.endswith('.json'):
            r = json.load(open(os.path.join(outdir, fn)))
            if r['seed'] % nw == w:
                used += r['cpu_s']; maxcost = max(maxcost, r['cpu_s'])
    for seed in range(w, nseeds, nw):
        p = os.path.join(outdir, 'seed_%05d.json' % seed)
        if os.path.exists(p): continue
        if used + max(maxcost, 1.0) > budget_each: break
        r = run_seed(band, seed, steps)
        atomic_write(p, r)
        used += r['cpu_s']; maxcost = max(maxcost, r['cpu_s'])

def summarise(band, outdir):
    rs = [json.load(open(os.path.join(outdir, f))) for f in sorted(os.listdir(outdir)) if f.startswith('seed_') and f.endswith('.json')]
    done = [r for r in rs if r['status'] == 'done']
    bh = {}; eh = {}
    for r in done:
        bh[r['best_len']] = bh.get(r['best_len'], 0) + 1
        for k, c in r['eval_hist'].items(): eh[int(k)] = eh.get(int(k), 0) + c
    s = dict(band=band, seeds_done=len(done), seeds_no_instance=len(rs) - len(done),
             cpu_s_total=round(sum(r['cpu_s'] for r in rs), 1),
             best_length=max([r['best_len'] for r in done], default=None),
             best_len_histogram_over_seeds=dict(sorted(bh.items())), evaluated_len_histogram=dict(sorted(eh.items())),
             orders=sorted({r['n'] for r in done}), seeds_with_len_ge_6=[r['seed'] for r in done if r['best_len'] >= 6])
    manifest = dict(band=band, finished_seeds=[r['seed'] for r in rs], summary=s)
    atomic_write(os.path.join(outdir, 'manifest.json'), manifest)
    return s

def test13():
    rng = random.Random('t13'); okc = 0
    for t in range(5):
        r = build_md5(13, rng)
        if r is not None: okc += 1
    print('n=13: min-degree-5 seeds found in 5 attempts (each 200 internal retries):', okc)

def main():
    if '--test13' in sys.argv: return test13()
    ap = argparse.ArgumentParser()
    ap.add_argument('--band', required=True); ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--cpu-budget', type=float, default=540.0)  # total CPU seconds for this band-run (<= 600)
    ap.add_argument('--seeds', type=int, default=100000); ap.add_argument('--steps', type=int, default=2000)
    a = ap.parse_args()
    assert a.workers <= 2 and a.cpu_budget <= 600
    outdir = os.path.join(HERE, 'runs_md5', 'band_' + a.band); os.makedirs(outdir, exist_ok=True)
    log = os.path.join(HERE, 'runs_md5', 'band_%s.log' % a.band)
    with open(log, 'a') as f:
        f.write('%s START band=%s orders=%s workers=%d total CPU budget=%.0fs (%.1f CPU-min, cap 10) steps/seed=%d seed-ids 0.. (rng seed string "md5-%s-<id>") [computed, exploratory]\n'
                % (time.strftime('%F %T'), a.band, BANDS[a.band], a.workers, a.cpu_budget, a.cpu_budget / 60, a.steps, a.band))
    ps = [Process(target=worker, args=(a.band, w, a.workers, a.cpu_budget / a.workers, a.seeds, a.steps, outdir)) for w in range(a.workers)]
    for p in ps: p.start()
    for p in ps: p.join()
    s = summarise(a.band, outdir)
    with open(log, 'a') as f: f.write('%s END %s\n' % (time.strftime('%F %T'), json.dumps(s)))
    print(json.dumps(s, indent=1))

if __name__ == '__main__':
    main()
