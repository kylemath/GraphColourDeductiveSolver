# Adversarial pairs. Usage: python exp1.py map kind ncol seed   kinds: strip, lop, cap2, vorseam, half
import sys, json, time, random, collections
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof')
from mp import *

def shell_strip(g, c, r, s0, d):
    sh = set(v for v, dd in bfs(g.adj, c, r+2).items() if dd in (r+1, r+2))
    q = [s0]; A = {s0}; dist = {s0: 0}
    while q:
        x = q.pop(0)
        if dist[x] >= d: continue
        for y in g.adj[x]:
            if y in sh and y not in A: A.add(y); dist[y] = dist[x]+1; q.append(y)
    return A

def pairs(g, kind, rng, nmax=6):
    n = g.n; out = []; tries = 0
    deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
    while len(out) < nmax and tries < 200:
        tries += 1
        if kind == 'strip':      # thin shell strip A (many chords) hugging a ball B
            c = rng.randrange(n); r = rng.randrange(2, 5); B = ball(g, c, r)
            sh = [v for v, dd in bfs(g.adj, c, r+1).items() if dd == r+1]
            A = shell_strip(g, c, r, rng.choice(sh), rng.randrange(4, 14))
        elif kind == 'lop':      # tiny B against big A
            c = rng.randrange(n); A = ball(g, c, rng.randrange(3, 6))
            bd = [v for v, dd in bfs(g.adj, c, 8).items() if dd == max(bfs(g.adj, c, 8).values())-rng.randrange(0, 2)]
            b = rng.choice([v for v in range(n) if v not in A and any(w in A for w in g.adj[v])])
            B = ball(g, b, rng.randrange(0, 2)) - A
        elif kind == 'cap2':     # A, B each a disc containing exactly two odd vertices (even monodromy, |t|=2 forcible)
            o1 = rng.choice(deg5); d1 = bfs(g.adj, o1, 30)
            near = sorted((d, o) for o, d in d1.items() if o != o1 and o in deg5)[:3]
            if not near: continue
            d, o2 = rng.choice(near); path = [o2]
            while path[-1] != o1: path.append(min((w for w in g.adj[path[-1]] if w in d1), key=lambda w: d1[w]))
            mid = path[len(path)//2]; A = ball(g, mid, d//2+1)
            if sum(1 for v in A if v in deg5) != 2: continue
            cand = [v for v in range(n) if v not in A and any(w in A for w in g.adj[v])]
            b = rng.choice(cand); B = ball(g, b, rng.randrange(2, 5)) - A
            if rng.random() < 0.5:
                # second two-vortex cap
                B = ball(g, b, max(2, d//2+1)) - A
        elif kind == 'cap2big':  # big two-vortex cap A (forced |t|=2) against a big adjacent ball B; long boundaries
            o1 = rng.choice(deg5); d1 = bfs(g.adj, o1, 40)
            near = sorted((d, o) for o, d in d1.items() if o != o1 and o in deg5)[:2]
            d, o2 = rng.choice(near); path = [o2]
            while path[-1] != o1: path.append(min((w for w in g.adj[path[-1]] if w in d1), key=lambda w: d1[w]))
            mid = path[len(path)//2]; rA = d//2 + rng.randrange(1, 4); A = ball(g, mid, rA)
            if sum(1 for v in A if v in deg5) % 2: continue
            dm = bfs(g.adj, mid, 3*rA); far = [v for v in dm if dm[v] == 2*rA+1]
            if not far: continue
            B = ball(g, rng.choice(far), rA) - A
        elif kind == 'vorseam':  # A, B halves of a ball, cut through the vortex-dense region
            c = rng.choice(deg5); r = rng.randrange(3, 6); U = ball(g, c, r)
            a = rng.choice(list(U)); da = bfs(g.adj, a, 2*r+2)
            A = set(v for v in U if da[v] <= r); B = U - A
        elif kind == 'half':     # balanced halves of a big ball, seam long
            c = rng.randrange(n); r = rng.randrange(5, 9); U = ball(g, c, r); dc = bfs(g.adj, c, r)
            a = rng.choice([v for v in U if dc[v] == r]); da = bfs(g.adj, a, 3*r)
            A = set(v for v in U if da[v] <= r); B = U - A
        if not A or not B: continue
        sa, sb, su = check(g, A), check(g, B), check(g, A | B)
        if sa[0] == 'nodisc' or sb[0] == 'nodisc' or su[0] == 'nodisc': continue
        out.append((A, B))
    return out

if __name__ == '__main__':
    name, kind, ncol, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    g = G(make(name)); rng = random.Random(seed)
    log = open('/mnt/project-files/multiscale/merge_proof/exp1_%s_%s_s%d.jsonl' % (name, kind, seed), 'a')
    for A, B in pairs(g, kind, rng):
        t0 = time.time(); D = Disc(g, A | B)
        cA = {}; cB = {}
        for f in (None, 'nonzero', 'zero'):
            cA[f] = level_cols(g, A, ncol, f, seed0=100*seed); cB[f] = level_cols(g, B, ncol, f, seed0=100*seed+50)
        for fa, fb in [(None, None), ('nonzero', 'zero'), ('zero', 'nonzero'), ('nonzero', 'nonzero')]:
            for ca in cA[fa][:ncol]:
                for cb in cB[fb][:ncol]:
                    rec = merge_all24(g, D, A, B, ca, cb)
                    rec.update(map=name, kind=kind, nA=len(A), nB=len(B), fa=fa, fb=fb, chA=len(Disc(g, A).chords), chB=len(Disc(g, B).chords), sec=round(time.time()-t0, 1))
                    log.write(json.dumps(rec)+'\n'); log.flush()
                    print({k: rec[k] for k in ('kind', 'nA', 'nB', 'chA', 'chB', 'seam_pockets', 'fa', 'fb', 'nconf', 'R', 'nR', 'w', 'wc', 'ptau_before', 'sec')}, flush=True)
