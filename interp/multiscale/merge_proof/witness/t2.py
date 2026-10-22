# Task 2: explicit Lemma M witness.  A = C1 (two-vortex ball) + D2 (two-vortex half-ball) touching C1 only along one
# boundary edge uw (the chord of A); B = vortex-free ball around u, making u interior in U = A+B so the pockets fuse.
# Colour A weakly 1-level with |t_A|^2 >= minT2 (pocket monodromies not cancelling), B level; then for all 24
# renamings: fused-pocket |t_P| of the glued and repaired colouring, min R, min w (tau*, nb base points).
# Usage: python t2.py map k seed minT2 nb
import sys, json, time, random
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof/witness')
from w2 import *
name, k, seed, minT2, nb = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
g = G(make(name)); rng = random.Random(seed); n = g.n
deg5 = set(v for v in range(n) if g.deg[v] % 2 == 1)
half = 10 if name == 'ico20' else 5
log = open('/mnt/project-files/multiscale/merge_proof/witness/t2_%s_k%d_s%d_T%d.jsonl' % (name, k, seed, int(minT2)), 'a')
def nvor(S): return sum(1 for v in S if v in deg5)
def comp(S, v):
    if v not in S: return set()
    seen = {v}; st = [v]
    while st:
        y = st.pop()
        for z in g.adj[y]:
            if z in S and z not in seen: seen.add(z); st.append(z)
    return seen
def pverts(DX, W):
    # interior + boundary vertices of the pocket whose boundary walk is W (vertices of its triangles)
    bs = set(W['walk']); tris = [i for i in DX.tris if all(x in DX.S for x in g.faces[i])]
    # flood from a triangle on W's boundary edge not crossing chords
    ch = set(DX.chords); walk = W['walk']; m = len(walk); start = None
    for i in range(m):
        a, b = walk[i], walk[(i+1) % m]; f = g.face[(a, b)]
        if f in DX.tris: start = f; break
    seen = {start}; st = [start]
    while st:
        i = st.pop(); f = g.faces[i]
        for j in range(3):
            a, b = f[j], f[(j+1) % 3]; o = g.face[(b, a)]
            if o in DX.tris and o not in seen and (min(a, b), max(a, b)) not in ch: seen.add(o); st.append(o)
    return set(x for i in seen for x in g.faces[i])

def candidates():
    vs = sorted(deg5); rng.shuffle(vs)
    for o1 in vs:
        d1 = bfs(g.adj, o1, 40)
        d, o2 = sorted((d, o) for o, d in d1.items() if o != o1 and o in deg5)[0]
        path = [o2]
        while path[-1] != o1: path.append(min((w for w in g.adj[path[-1]] if w in d1), key=lambda w: d1[w]))
        mid = path[len(path)//2]; r1 = d//2 + k; C1 = ball(g, mid, r1)
        if nvor(C1) != 2 or check(g, C1)[0] != 'ok': continue
        D1 = Disc(g, C1); walk = D1.whole['walk']; m = len(walk)
        N1 = {}
        for i in range(m):
            u, w = walk[i], walk[(i+1) % m]; f = g.faces[g.face[(w, u)]]; x = [y for y in f if y not in (u, w)][0]
            if len(g.adj[x] & C1) != 2: continue
            fan_u = [y for y in g.adj[u] if y not in C1]; fan_w = [y for y in g.adj[w] if y not in C1]
            out = set(range(n)) - C1
            Nout = set(y for z in C1 - {u, w} for y in g.adj[z] if y not in C1)
            for gap in (1, 2):
                Ex = set(Nout)
                for _ in range(gap-1): Ex |= set(y for z in Ex for y in g.adj[z] if y not in C1)
                Al = out - Ex
                if x not in Al: continue
                yk = [y for y in fan_u if y in Nout]
                if not yk: continue
                dyk = bfs(g.adj, yk[0], 8); dx = bfs(g.adj, x, 40)
                for r2, rb in itertools.product(range(r1+1, r1+8), (2, 3, 4, 5)):
                    Broom = set(v for v, dv in dyk.items() if dv <= rb and dv < dx[v])
                    D2 = comp((ball(g, x, r2) & Al) - Broom, x)
                    if nvor(D2) != 2 or check(g, D2)[0] == 'nodisc': continue
                    A = C1 | D2
                    if check(g, A)[0] != 'chord': continue
                    DA = Disc(g, A)
                    if (min(u, w), max(u, w)) not in DA.chords: continue
                    if any(nvor(set(W['walk'])) for W in DA.pockets): continue
                    big = [W for W in DA.pockets if nvor(pverts(DA, W)) == 2]
                    if len(big) != 2 or sum(nvor(pverts(DA, W)) for W in DA.pockets) != 4: continue
                    for rb2 in (rb+1,):
                        B = comp(ball(g, u, rb2) - A, yk[0])
                        if nvor(B) or check(g, B)[0] == 'nodisc' or check(g, A | B)[0] == 'nodisc': continue
                        D = Disc(g, A | B)
                        PU = [W for W in D.pockets if nvor(pverts(D, W)) == 4]
                        if len(PU) != 1 or nvor(D.S) != 4: continue
                        WU = PU[0]
                        dBU = multi_bfs(g.adj, list(D.bset), D.S)
                        if min(dBU[o] for o in D.S if o in deg5) < k: continue
                        yield dict(WU=WU, C1=C1, D2=D2, A=A, B=B, u=u, w=w, x=x, r1=r1, r2=r2, rb=rb, gap=gap, DA=DA, D=D)
                        break
                    break
                break

found = 0
for c in candidates():
    A, B, DA, D, WU = c['A'], c['B'], c['DA'], c['D'], c['WU']
    dB = multi_bfs(g.adj, list(D.bset), D.S); depths = sorted(dB[o] for o in D.S if o in deg5 and o not in D.bset)
    seam = [(a, b) for (a, b) in D.edges if (a in A) != (b in A)]
    dS = multi_bfs(g.adj, [v for e in seam for v in e], D.S); dseam = sorted(dS[o] for o in D.S if o in deg5)
    print('candidate', dict(nA=len(A), nB=len(B), r1=c['r1'], r2=c['r2'], rb=c['rb'], pocketsA=len(DA.pockets), mA=[len(W['walk']) for W in DA.pockets], mU=len(D.whole['walk']), depths=depths, dseam=dseam), flush=True)
    t0 = time.time()
    cA = sat2(DA, DA.pockets, 1.0, seed=seed, budget=10**8, big_walk=(DA.whole, 30.0, minT2))
    print('  A colouring:', 'UNSAT' if cA is None else cA if cA == 'UNK' else 'SAT', round(time.time()-t0, 1), flush=True)
    if cA in (None, 'UNK'):
        log.write(json.dumps(dict(map=name, k=k, nA=len(A), nB=len(B), r1=c['r1'], r2=c['r2'], A_status=str(cA), minT2=minT2))+'\n'); log.flush(); continue
    cB = level_cols(g, B, 1, None, seed0=seed, budget=3*10**7)
    if not cB: continue
    cb = cB[0]
    tA = tvec(DA.whole, cA); tAp = [tvec(W, cA) for W in DA.pockets]; tauA = [round(tau_walk(W, cA), 3) for W in DA.pockets]
    rows = []
    for ip, p in enumerate(PERMS):
        cc = {v: cA[v] for v in A}; cc.update({v: p[cb[v]] for v in B})
        K = set(y for e in seam if cc[e[0]] == cc[e[1]] for y in e)
        R = None
        for RR in range(5):
            r, c2 = (0, cc) if not K else proper_repair_at(g, D.S, cc, K, RR)
            if r is not None: R = RR; break
        row = dict(perm=''.join(map(str, p)), nconf=len(K), tP_glued=tvec(WU, cc), R=R)
        if R is not None:
            zone = set(v for v in D.S if c2[v] != cc[v]); row['tP_rep'] = tvec(WU, c2)
            row['tau_star_before'] = round(tau_star(WU, c2), 3); row['pocketsU'] = len(D.pockets)
            if ip < 4 or len(K) == 0:
                ws, bps, calls = min_w_star(g, D, c2, zone, wmax=max(depths)+1, nb=nb)
                row.update(w_star=ws, bp=bps, calls=calls)
        rows.append(row); print('  ', row, flush=True)
    rec = dict(map=name, k=k, seed=seed, minT2=minT2, nA=len(A), nB=len(B), r1=c['r1'], r2=c['r2'], rb=c['rb'], u=c['u'], w=c['w'], x=c['x'],
               mA=[len(W['walk']) for W in DA.pockets], mU=len(D.whole['walk']), depths=depths, dseam=dseam, tA=tA, tA_pockets=tAp, tauA=tauA,
               tB=[tvec(W, cb) for W in Disc(g, B).pockets], rows=rows, sec=round(time.time()-t0, 1),
               colA={str(v): cA[v] for v in A}, colB={str(v): cb[v] for v in B}, Averts=sorted(A), Bverts=sorted(B))
    log.write(json.dumps(rec)+'\n'); log.flush(); found += 1
    print('WITNESS', found, dict(tA=tA, tA_pockets=tAp, tauA=tauA, depths=depths, dseam=dseam, tP=sorted(set(r['tP_glued'] for r in rows)), w=sorted(set(str(r.get('w_star')) for r in rows))), flush=True)
    if found >= 2: break
print('done', found)
