"""Pathway P-F [exploratory]: degree invariants of states at a degree-5 hole.
State = proper 4-colouring c of T - v (labelled colours 0..3, NOT up to permutation, so signs are meaningful).
D = T minus open star of v. n[k] = signed count of triangles of D whose colour set misses k;
sign of oriented face (p,q,r) = parity of the permutation (c p, c q, c r, k) of (0,1,2,3).
Kempe graph: all whole-component two-colour swaps in T - v. filled = link uses <= 3 colours.
DL as in thmH_independent_check.py. Radius = multi-source BFS distance from filled states.
Usage: python3 degree_invariants.py  (prints JSON-ish summary per graph/hole)."""
import itertools, sys, subprocess, os
from collections import deque, Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, '..', 'MathRadiusCensus', 'gen_tri')

def A(r):
    F=[];ring=lambda k,i:1+5*k+(i%5);top=1+5*r
    for i in range(5): F.append((0,ring(0,i),ring(0,i+1)))
    for k in range(r-1):
        for i in range(5):
            F.append((ring(k,i),ring(k+1,i),ring(k,i+1)));F.append((ring(k+1,i),ring(k+1,i+1),ring(k,i+1)))
    for i in range(5): F.append((top,ring(r-1,i+1),ring(r-1,i)))
    return F

T4 = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]

def gen(n):
    out = subprocess.run([GEN, str(n), '--all'], capture_output=True, text=True).stdout
    res = []
    for line in out.splitlines():
        if line.startswith('G '):
            p = line.split(); nf = int(p[3]); a = list(map(int, p[4:4+3*nf]))
            res.append([tuple(a[3*i:3*i+3]) for i in range(nf)])
    return res

def orient(F):
    """consistently orient a sphere triangulation (propagation)."""
    F = [list(f) for f in F]; ef = defaultdict(list)
    for i,f in enumerate(F):
        for k in range(3): ef[frozenset((f[k],f[(k+1)%3]))].append(i)
    done = [False]*len(F); done[0] = True; st = [0]
    while st:
        i = st.pop(); f = F[i]
        for k in range(3):
            a,b = f[k], f[(k+1)%3]
            for j in ef[frozenset((a,b))]:
                if j == i: continue
                g = F[j]
                # neighbour must traverse b->a
                darts = [(g[t],g[(t+1)%3]) for t in range(3)]
                if done[j]:
                    assert (b,a) in darts, 'non-orientable?'
                    continue
                if (a,b) in darts: F[j] = [g[0],g[2],g[1]]
                done[j] = True; st.append(j)
    assert all(done)
    return [tuple(f) for f in F]

PAR = {}
for p in itertools.permutations(range(4)):
    inv = sum(1 for i in range(4) for j in range(i+1,4) if p[i] > p[j]); PAR[p] = -1 if inv % 2 else 1

def nvec(faces, col):
    n = [0,0,0,0]
    for (p,q,r) in faces:
        a,b,c = col[p],col[q],col[r]; k = 6-a-b-c
        n[k] += PAR[(a,b,c,k)]
    return tuple(n)

def reduce_loop(seq):
    """free reduction (cyclic) of a closed walk in K4; returns reduced cyclic sequence."""
    s = list(seq)
    changed = True
    while changed and len(s) > 1:
        changed = False
        L = len(s)
        for i in range(L):
            if s[i] == s[(i+2) % L] and L >= 3:
                # backtrack s[i] -> s[i+1] -> s[i]: delete positions i+1, i+2 (cyclically)
                j1, j2 = (i+1) % L, (i+2) % L
                s = [s[t] for t in range(L) if t not in (j1, j2)]
                changed = True; break
    return s

def analyse(Fraw, v, name):
    F = orient(Fraw)
    V = sorted({x for f in F for x in f})
    adj = {u:set() for u in V}
    for f in F:
        for a,b in itertools.combinations(f,2): adj[a].add(b); adj[b].add(a)
    if len(adj[v]) != 5: return None
    star = [f for f in F if v in f]; D = [f for f in F if v not in f]
    # oriented link: from star faces (v,x,y) rotated so v first, x->y
    nxt = {}
    for f in star:
        i = f.index(v); nxt[f[(i+1)%3]] = f[(i+2)%3]
    link = [next(iter(nxt))]
    while len(link) < 5: link.append(nxt[link[-1]])
    W = [u for u in V if u != v]; Ad = {u:[w for w in adj[u] if w != v] for u in W}
    idx = {u:i for i,u in enumerate(W)}
    # enumerate canonical colourings, expand to labelled
    canon = []
    order = sorted(W, key=lambda u: (u not in link, link.index(u) if u in link else u))
    # BFS order for pruning
    order = []; seen = set(); dq = deque([link[0]])
    while dq:
        u = dq.popleft()
        if u in seen: continue
        seen.add(u); order.append(u)
        for w in sorted(Ad[u]):
            if w not in seen: dq.append(w)
    c = {}
    def rec(k, m):
        if k == len(order): canon.append(tuple(c[u] for u in W)); return
        u = order[k]
        for x in range(min(m+1,4)):
            if all(c.get(w) != x for w in Ad[u]):
                c[u] = x; rec(k+1, max(m, x+1)); del c[u]
    sys.setrecursionlimit(10000); rec(0, 0)
    states = set()
    for t in canon:
        for p in itertools.permutations(range(4)):
            states.add(tuple(p[x] for x in t))
    states = sorted(states); sid = {t:i for i,t in enumerate(states)}; S = len(states)
    li = [idx[x] for x in link]
    def filled(t): return len({t[i] for i in li}) <= 3
    def comps(t, p, q):
        seen = set(); out = []
        for u in W:
            if t[idx[u]] in (p,q) and u not in seen:
                comp = [u]; seen.add(u); st = [u]
                while st:
                    x = st.pop()
                    for y in Ad[x]:
                        if t[idx[y]] in (p,q) and y not in seen: seen.add(y); comp.append(y); st.append(y)
                out.append(comp)
        return out
    def path(t, s, e, pq):
        seen = {s}; st = [s]
        while st:
            x = st.pop()
            if x == e: return True
            for y in Ad[x]:
                if y not in seen and t[idx[y]] in pq: seen.add(y); st.append(y)
        return False
    def dl(t):
        cs = [t[i] for i in li]
        if len(set(cs)) < 4: return False
        j = [j for j in range(5) if cs[j] == cs[(j+2)%5]][0]; x = [link[(j+i)%5] for i in range(5)]
        return path(t,x[1],x[3],{t[idx[x[1]]],t[idx[x[3]]]}) and path(t,x[1],x[4],{t[idx[x[1]]],t[idx[x[4]]]})
    info = []
    edges = defaultdict(set); swapdelta = Counter()
    for i,t in enumerate(states):
        col = {u:t[idx[u]] for u in W}
        n = nvec(D, col)
        red = reduce_loop([t[k] for k in li])
        assert len(red) == 3, red
        m = 6 - sum(red)
        eps = PAR[(red[0],red[1],red[2],m)]
        # prediction: n = (N,N,N,N+s) with special index m
        others = [n[k] for k in range(4) if k != m]
        assert len(set(others)) == 1, (n, m, red)
        N = others[0]; sp = n[m] - N
        ext = None
        if filled(t):
            col2 = dict(col); col2[v] = m
            nf = nvec(F, col2); assert len(set(nf)) == 1, nf; ext = nf[0]
        info.append(dict(n=n, m=m, eps=eps, N=N, sp=sp, filled=filled(t), dl=dl(t), ext=ext))
        for p,q in itertools.combinations(range(4),2):
            for comp in comps(t,p,q):
                d = list(t)
                for x in comp: d[idx[x]] = q if t[idx[x]] == p else p
                j = sid[tuple(d)]
                if j != i: edges[i].add(j)
                touch = sum(1 for x in comp if x in link)
                # record delta of N and of special-shape
                t2 = tuple(d); col3 = {u:t2[idx[u]] for u in W}
                n2 = nvec(D, col3)
                swapdelta[('touch' if touch else 'free', tuple(n2[k]-n[k] for k in range(4)) if not touch else None)] += 1
    # Kempe classes
    cls = [-1]*S; nc = 0
    for s in range(S):
        if cls[s] >= 0: continue
        cls[s] = nc; st = [s]
        while st:
            x = st.pop()
            for y in edges[x]:
                if cls[y] < 0: cls[y] = nc; st.append(y)
        nc += 1
    dist = [-1]*S; dq = deque()
    for s in range(S):
        if info[s]['filled']: dist[s] = 0; dq.append(s)
    while dq:
        x = dq.popleft()
        for y in edges[x]:
            if dist[y] < 0: dist[y] = dist[x]+1; dq.append(y)
    return dict(name=name, v=v, link=link, S=S, ncanon=len(canon), info=info, cls=cls, nc=nc, dist=dist,
                swapdelta=swapdelta, edges=edges, states=states, li=li, idx=idx)

if __name__ == '__main__':
    jobs = [('T4', T4, [4])]
    for r in (3,4,5): jobs.append((f'A_{r}', A(r), [0]))
    ico = gen(12)[0]; jobs.append(('ico', ico, [0]))
    g14 = gen(14)[0]
    deg = Counter(x for f in g14 for x in f)
    jobs.append(('n14', g14, sorted(u for u in deg if deg[u] == 5)))
    import pickle
    allres = []
    for name, Fr, holes in jobs:
        for v in holes:
            R = analyse(Fr, v, name)
            if R is None: continue
            info = R['info']; cls = R['cls']; dist = R['dist']
            print(f"== {name} v={v} labelled states {R['S']} (canon {R['ncanon']}) classes {R['nc']}")
            # free-swap deltas
            fd = Counter(k[1] for k in R['swapdelta'].elements() if k[0] == 'free')
            print('  free swaps (component misses link): n-vector deltas', dict(fd))
            # per-state invariants
            hist = Counter((s['filled'], s['dl'], dist[i], s['N'], s['sp']) for i,s in enumerate(info))
            byr = defaultdict(Counter)
            for i,s in enumerate(info):
                key = 'filled' if s['filled'] else ('DL' if s['dl'] else 'unf-nonDL')
                byr[(key, dist[i])][(s['N'], s['sp'])] += 1
            for k in sorted(byr, key=lambda z:(z[0],z[1])): print('  ', k, '(N,sp):', dict(byr[k]))
            ext = Counter(s['ext'] for s in info if s['filled'])
            print('  extension degrees of filled states:', dict(ext))
            # per class: set of N values, ext values, filled count
            cl = defaultdict(lambda: [set(), set(), 0, 0])
            for i,s in enumerate(info):
                c = cl[cls[i]]; c[0].add(s['N']); c[2] += 1
                if s['filled']: c[1].add(s['ext']); c[3] += 1
            print('  classes: (size, filled, Nvalues, extdegs):', Counter((c[2], c[3], tuple(sorted(c[0])), tuple(sorted(c[1]))) for c in cl.values()))
            allres.append(R)
    pickle.dump([{k:R[k] for k in ('name','v','link','S','info','cls','dist','states','li')} for R in allres], open(os.path.join(os.environ.get('PF_OUT','.'),'pf_results.pkl'),'wb'))
