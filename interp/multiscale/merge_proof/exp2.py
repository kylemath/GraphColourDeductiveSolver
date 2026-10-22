# (ii) collar re-levelling in isolation: a chordless disc U (ball) whose boundary word is level on two arcs
# with a prescribed relative offset q (arc1 within 1 of 0, arc2 within 1 of q), interior otherwise arbitrary.
# Min collar width w (interior at depth > w fixed) that restores tau(U) <= 1.   Usage: python exp2.py map rmin rmax seed
import sys, json, time, random, itertools, math
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof')
from mp import *

def two_arc_col(D, W, q, seed, budget=5*10**6, big=16.0, force_t=None, cut=None):
    V = sorted(D.S); ix = {v: i for i, v in enumerate(V)}
    x = lambda v, c: 4*ix[v]+c+1; top = [4*len(V)]
    def new(): top[0] += 1; return top[0]
    cls = []
    for v in V:
        cls.append([x(v, c) for c in range(4)])
        for a, b in itertools.combinations(range(4), 2): cls.append([-x(v, a), -x(v, b)])
    for u, w in D.edges:
        for c in range(4): cls.append([-x(u, c), -x(w, c)])
    Dm = domain(big); Ds = set(Dm); walk, s = W['walk'], W['s']; m = len(walk)
    H = [{p: new() for p in Dm} for _ in range(m+1)]
    for i in range(m):
        u, w = walk[i], walk[(i+1) % m]; L = {l: new() for l in (1, 2, 3)}
        for a in range(4):
            for b in range(4):
                if a != b: cls.append([-x(u, a), -x(w, b), L[a ^ b]])
        for p in Dm:
            for l in (1, 2, 3):
                d = INC[l]; qq = (p[0]+s[i]*d[0], p[1]+s[i]*d[1])
                cls.append([-H[i][p], -L[l], H[i+1][qq]] if qq in Ds else [-H[i][p], -L[l]])
    for i in range(m+1):
        cls.append([H[i][p] for p in Dm])
    cut = cut or m//2
    b1 = set(p for p in Dm if n2(p) <= 1+1e-9); b2 = set(p for p in Dm if n2((p[0]-q[0], p[1]-q[1])) <= 1+1e-9)
    for i in range(0, cut+1):
        for p in Dm:
            if p not in b1: cls.append([-H[i][p]])
    for i in range(cut+1, m+1):
        for p in Dm:
            if p not in b2: cls.append([-H[i][p]])
    if W['odd']:
        for p in Dm: cls.append([-H[m][p], H[0][(-p[0], -p[1])]])
    elif force_t == 'nonzero':
        for p in Dm: cls.append([-H[0][p], -H[m][p]])
    elif force_t == 'zero':
        for p in Dm: cls.append([-H[0][p], H[m][p]])
    s_ = Glucose4(bootstrap_with=cls); rng = random.Random(seed)
    s_.set_phases([(4*i+c+1)*(1 if rng.random() < 0.25 else -1) for i in range(len(V)) for c in range(4)])
    s_.conf_budget(budget); ok = s_.solve_limited()
    if not ok: s_.delete(); return None if ok is False else 'UNK'
    mod = set(l for l in s_.get_model() if l > 0); s_.delete()
    return {v: next(c for c in range(4) if x(v, c) in mod) for v in V}

def min_w(g, D, col, wmax=7):
    dB = multi_bfs(g.adj, list(D.bset), D.S)
    for ww in range(wmax+1):
        fx = {v: col[v] for v in D.S if dB[v] > ww}
        r = sat2(D, D.pockets, 1.0, fixed=fx)
        if r not in (None, 'UNK'): return ww
        if r == 'UNK': return 'UNK%d' % ww
    return '>%d' % wmax

if __name__ == '__main__':
    name, rmin, rmax, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    g = G(make(name)); rng = random.Random(seed); n = g.n
    deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
    log = open('/mnt/project-files/multiscale/merge_proof/exp2_%s_s%d.jsonl' % (name, seed), 'a')
    QS = [(2, 0), (4, 0), (4, 2), (6, 0), (6, 3), (8, 4)]   # |q| = 1, 2, sqrt3, 3, 3, 4
    for r in range(rmin, rmax+1):
        for trial in range(2):
            mode = ['any', 'cap2'][trial % 2]
            if mode == 'cap2':
                o1 = rng.choice(deg5); d1 = bfs(g.adj, o1, 40)
                d, o2 = sorted((d, o) for o, d in d1.items() if o != o1 and o in deg5)[0]
                path = [o2]
                while path[-1] != o1: path.append(min((w for w in g.adj[path[-1]] if w in d1), key=lambda w: d1[w]))
                c = path[len(path)//2]; rr = max(r, d//2+1)
            else: c = rng.randrange(n); rr = r
            U = ball(g, c, rr)
            if check(g, U)[0] != 'ok': continue
            D = Disc(g, U); W = D.whole; nodd = sum(1 for v in U if v in deg5 and v not in D.bset)
            for q in QS:
                for ft in ([None] if W['odd'] else ['zero', 'nonzero']):
                    t0 = time.time(); col = two_arc_col(D, W, q, seed, force_t=ft)
                    if col in (None, 'UNK'):
                        rec = dict(map=name, r=rr, m=len(W['walk']), nodd=nodd, q=q, qn=round(math.sqrt(n2(q)), 3), ft=ft, feasible=str(col)); log.write(json.dumps(rec)+'\n'); log.flush(); print(rec, flush=True); continue
                    tb = tau_walk(W, col); w = min_w(g, D, col)
                    rec = dict(map=name, r=rr, m=len(W['walk']), n=len(U), nodd=nodd, q=q, qn=round(math.sqrt(n2(q)), 3), ft=ft, t=tvec(W, col), tau_before=round(tb, 3), w=w, sec=round(time.time()-t0, 1))
                    log.write(json.dumps(rec)+'\n'); log.flush(); print(rec, flush=True)
