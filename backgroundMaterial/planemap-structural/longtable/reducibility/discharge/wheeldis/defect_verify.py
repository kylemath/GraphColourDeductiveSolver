"""Independent verification of a defect (README §7, test G; exploratory).
Builds the patch from its ring signature with b8b/rings.py (Layered; not defect.py's Disc), adds SEA all-6 rings, and
writes, straight from the explicit graph:
  - every wheel (vertex + link, exact degrees) of the cluster (degree != 6) and of every 6 adjacent to it;
  - every receiver-centred configuration at every 7: u + S + the link vertices of S of degree <= 6 (degree >= 7 left
    free, as in pairs2.py/gen.py), for every set S of >= 2 degree-5 neighbours of u;
in dfast format (OUT.cfg), for dfast and cfast runs that do not depend on any registry or canonical key.
Also checks: sea (every vertex outside the cluster has degree 6), separating 3-/4-cycles and nontrivial separating
5-cycles near the cluster, diamond / 2.122, 5-/6-wheel words against the Job 17 lists, and prints the closed-set
certificate t >= c(Y)/|Y| and |N_r(Y)| for r = 1, 2, 3.
Usage: python3 defect_verify.py SIG OUT.cfg [SEA=6]"""
import sys, os, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS)
from rings import Layered
import construct
SIG, OUTF = sys.argv[1], sys.argv[2]; SEA = int(sys.argv[3]) if len(sys.argv) > 3 else 6
ARGS = sys.argv[1:]
src = open(os.path.join(HERE, 'wlp.py')).read().replace('__file__', repr(os.path.join(HERE, 'wlp.py')))
sys.argv = ['wlp']; exec(src[:src.index('# sender rows')])
rings = SIG.split('|'); L = Layered(int(rings[0]))
for k in range(1, len(rings)): L.add_ring([int(c) for c in rings[k]])
for _ in range(SEA): L.add_ring([6] * len(L.ring()))
outer = set(L.ring())
adj = collections.defaultdict(set); nxt = collections.defaultdict(dict)
for a, b, c in L.tris:
    for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    nxt[a][b] = c; nxt[b][c] = a; nxt[c][a] = b
deg = dict(L.deg)
inner = [v for v in adj if v not in outer]
for v in inner: assert len(adj[v]) == deg[v], (v, len(adj[v]), deg[v])
def rot(x):
    s0 = next(iter(nxt[x])); r = [s0]; y = nxt[x][s0]
    while y != s0: r.append(y); y = nxt[x][y]
    assert len(r) == len(adj[x]); return r
Y = sorted(v for v in inner if deg[v] != 6)
assert all(deg[v] in (5, 7) for v in Y)
dist = {v: 0 for v in Y}; fr = list(Y)
for r_ in range(1, 6):
    nf = []
    for x in fr:
        for y in adj[x]:
            if y not in dist: dist[y] = r_; nf.append(y)
    fr = nf
assert all(v not in outer for v in dist if dist[v] <= 4), 'sea too thin'
c = sum(6 - deg[v] for v in Y)
n5 = sum(1 for v in Y if deg[v] == 5); n7 = sum(1 for v in Y if deg[v] == 7)
print('cluster |Y| = %d (%d fives, %d sevens), charge c = %d; every vertex outside Y within distance 4 has degree 6: %s' % (
    len(Y), n5, n7, c, all(deg[v] == 6 for v in dist if dist[v] >= 1)))
print('closed-set certificate: t >= c/|Y| = %d/%d; |N_1(Y)| = %d, |N_2(Y)| = %d, |N_3(Y)| = %d' % (
    c, len(Y), sum(1 for v in dist if dist[v] <= 1), sum(1 for v in dist if dist[v] <= 2), sum(1 for v in dist if dist[v] <= 3)))
# wheel words from the explicit rotation
bad = []
for v in sorted(dist):
    if dist[v] > 2: continue
    w = [deg[x] for x in rot(v)]
    if deg[v] == 5 and isR5(w): bad.append(('5', v, w))
    if deg[v] == 6 and (isR6(w) or canon(w) in {tuple(map(int, u)) for u in UNCERT}): bad.append(('6', v, w))
print('wheel words in R (5: Job17+fans+diamond, 6: Job17+2.122+565xxx) within distance 2 of Y:', bad or 'none')
dd = False
for a in inner:
    R = rot(a)
    for i, b in enumerate(R):
        if b in outer: continue
        cc, d_ = R[(i + 1) % len(R)], R[(i - 1) % len(R)]
        if deg.get(cc) == 5 and deg.get(d_) == 5 and d_ not in adj[cc]:
            if (deg[a], deg[b]) == (5, 5) or {deg[a], deg[b]} == {5, 6}: dd = True
print('diamond or 2.122:', dd)
# separating short cycles near Y: remove the cycle; the part not reaching the outer ring is the inside
near = [v for v in dist if dist[v] <= 3]
def inside(cyc):
    cs = set(cyc); seen = set(cs); res = []
    for s in adj:
        if s in seen: continue
        st = [s]; seen.add(s); comp = [s]; hit = s in outer
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen: seen.add(w); st.append(w); comp.append(w); hit = hit or w in outer
        if not hit: res.append(comp)
    return sum(len(x) for x in res)
s3 = s4 = s5 = 0; seen5 = set()
NS = set(near)
for a in near:
    for b in adj[a] & NS:
        for c_ in adj[b] & NS:
            if c_ == a: continue
            if a in adj[c_] and a < b < c_ and inside((a, b, c_)) > 0: s3 += 1
            for d_ in adj[c_] & NS:
                if d_ in (a, b): continue
                if a in adj[d_] and c_ not in adj[a] and d_ not in adj[b]:
                    key = frozenset((a, b, c_, d_))
                    if key not in seen5 and inside((a, b, c_, d_)) > 0: s4 += 1
                    seen5.add(key)
                for e in adj[d_] & adj[a] & NS:
                    if e in (b, c_) or len({a, b, c_, d_, e}) < 5: continue
                    if c_ in adj[a] or d_ in adj[a] or d_ in adj[b] or e in adj[b] or e in adj[c_]: continue
                    key = ('5',) + tuple(sorted((a, b, c_, d_, e)))
                    if key in seen5: continue
                    seen5.add(key)
                    if inside((a, b, c_, d_, e)) >= 2: s5 += 1
print('separating triangles %d, separating 4-cycles %d, nontrivial separating 5-cycles %d (cycles within distance 3 of Y)' % (s3, s4, s5))
# configurations straight from the graph
def extract_cfg(I):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    assert not (RS & outer)
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nx = nb[0] if nb[0] != prev else nb[1]
        if nx == start: break
        order.append(nx); prev = cur
    if len(order) != len(RS): return None
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    for x in Il: assert len(adj[x]) == deg[x]
    return '%d %d %s %s' % (len(order), len(Il), f(ra), f(ia))
lines = []; nonsimple = []
wheelv = sorted(v for v in dist if dist[v] <= 1)
for v in wheelv:
    cfg = extract_cfg([v] + list(adj[v]))
    nm = 'w%d_%d_%s' % (deg[v], v, ''.join(str(deg[x]) for x in rot(v)))
    if cfg is None: nonsimple.append(nm)
    else: lines.append('%s %s' % (nm, cfg))
nrec = 0
for u in Y:
    if deg[u] != 7: continue
    S5 = [x for x in rot(u) if deg[x] == 5]
    for k in range(2, len(S5) + 1):
        for S in itertools.combinations(S5, k):
            I = {u} | set(S)
            for s in S: I |= {y for y in adj[s] if deg[y] <= 6}
            cfg = extract_cfg(sorted(I))
            nm = 'r7_%d_%s' % (u, '-'.join(map(str, S)))
            if cfg is None:
                # the ring has a chord in G: also write the configuration as it sits in G, with every ring vertex
                # whose whole neighbourhood lies in I + ring moved inside (exact degree), if that ring is simple
                RS = set(y for x in I for y in adj[x]) - I
                I2 = I | {y for y in RS if adj[y] <= (I | RS)}
                cfg2 = extract_cfg(sorted(I2)) if I2 != I else None
                nonsimple.append(nm + ('(+%s written)' % ','.join(str(y) for y in sorted(I2 - I)) if cfg2 else '(no simple version)'))
                if cfg2: lines.append('%sB%s %s' % (nm, '-'.join(str(y) for y in sorted(I2 - I)), cfg2)); nrec += 1
            else: lines.append('%s %s' % (nm, cfg)); nrec += 1
open(OUTF, 'w').write('\n'.join(lines) + '\n')
print('wrote %d configurations (%d wheels, %d receiver-centred); ring not a simple induced cycle: %s' % (
    len(lines), len(lines) - nrec, nrec, nonsimple or 'none'))
print('rings:', sorted(collections.Counter(int(l.split()[1]) for l in lines).items()))
