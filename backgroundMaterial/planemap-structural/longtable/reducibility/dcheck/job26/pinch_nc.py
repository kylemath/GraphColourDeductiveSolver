"""Job 26, B2: does the abstract non-crossing hypothesis of RingNC hold for the theta-chains of a PINCHED outside map
G' = A ∪_u B (chains of G' itself, positions i, j both = u)?  For every proper colouring and theta: E t t' := ring
positions t, t' in one theta-chain of G' (thetaGraph: edges whose colours differ by theta).  Checks
i<j<k<l, E i k, E j l => E i j (RingKempe's hNC), and the pairGraph forms nc/ncs of RingNC.  Usage: python3 pinch_nc.py"""
import itertools
exec(open('pinch_km.py').read().split('cases = [')[0])
def chains(n, E, col, pred):
    adj = [[] for _ in range(n)]
    for a, b in E:
        if pred(col[a], col[b]): adj[a].append(b); adj[b].append(a)
    comp = [-1] * n
    for s in range(n):
        if comp[s] >= 0: continue
        st = [s]; comp[s] = s
        while st:
            x = st.pop()
            for y in adj[x]:
                if comp[y] < 0: comp[y] = s; st.append(y)
    return comp
def test(n, E, ring):
    adj = [[] for _ in range(n)]
    for a, b in E: adj[a].append(b); adj[b].append(a)
    r = len(ring); bad = {'hNC': 0, 'nc': 0, 'ncs': 0}; cols = 0; col = [0] * n
    def check():
        for th in (1, 2, 3):
            cmp_ = chains(n, E, col, lambda x, y: (x ^ y) == th)
            Ep = lambda t, u: cmp_[ring[t]] == cmp_[ring[u]]
            for i, j, k, l in itertools.combinations(range(r), 4):
                if Ep(i, k) and Ep(j, l) and not Ep(i, j): bad['hNC'] += 1
        for a, b in itertools.combinations(range(4), 2):
            pg = chains(n, E, col, lambda x, y: {x, y} == {a, b})
            ina = lambda v: col[v] in (a, b)
            for a2, b2 in itertools.combinations(range(4), 2):
                same = (a, b) == (a2, b2)
                if not same and {a, b} & {a2, b2}: continue
                pg2 = pg if same else chains(n, E, col, lambda x, y: {x, y} == {a2, b2})
                ina2 = lambda v: col[v] in (a2, b2)
                for i, j, k, l in itertools.combinations(range(r), 4):
                    R1 = ina(ring[i]) and ina(ring[k]) and pg[ring[i]] == pg[ring[k]]
                    R2 = ina2(ring[j]) and ina2(ring[l]) and pg2[ring[j]] == pg2[ring[l]]
                    if R1 and R2:
                        if not same: bad['nc'] += 1
                        elif not (pg[ring[i]] == pg[ring[j]] and ina(ring[j])): bad['ncs'] += 1
    def go(v):
        nonlocal cols
        if v == n: cols += 1; check(); return
        for c in range(4):
            if all(col[w] != c for w in adj[v] if w < v): col[v] = c; go(v + 1)
    go(0); return cols, bad
cases = [('pinch 4w+4w (ring 8)', pinched(4, 'wheel', 4, 'wheel')), ('pinch 3f+5w (ring 8)', pinched(3, 'fan', 5, 'wheel')),
         ('pinch 5two+4w (ring 9)', pinched(5, 'two', 4, 'wheel')), ('pinch 4f+4f (ring 8)', pinched(4, 'fan', 4, 'fan')),
         ('simple 8 wheel', simple(8, 'wheel'))]
for name, (n, E, ring) in cases:
    cols, bad = test(n, E, ring); print('%-24s colourings %6d  violations %s' % (name, cols, bad), flush=True)
n, E, ring = 6, {(i, (i + 1) % 6) for i in range(6)} | {(0, 3), (1, 4)}, list(range(6))
cols, bad = test(n, E, ring); print('%-24s colourings %6d  violations %s' % ('CONTROL crossing chords', cols, bad))
