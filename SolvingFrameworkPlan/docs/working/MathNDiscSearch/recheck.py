"""MathNDiscSearch / recheck.py  [exploratory, undeclared, post hoc]
Independent re-check of ONE disc line (as printed by disc_gen / test_N.py after the '|').
Shares no code with test_N.py. Certifies, from the edge list and colours alone:
 (1) T = disc + x is a triangulation of the sphere (every vertex link is one cycle, Euler 2),
     min degree >= 5, no chord of the ring (4-connectivity at x);
 (2) proper colouring of T-x, all six pair subgraphs forests, component vector (1,2,2,1,1,1);
 (3) the fans u1,u3,u4 are locked: full Kempe class in G=T-xy (x coloured c(y)) enumerated,
     size printed, never separates x from y;
 (4) the two neighbours nu_gamma c, nu_beta c: full class at u0 resp. u2 enumerated; (N) fails
     iff both classes are finite and never separate. Prints 'N HOLDS' or 'N FAILS (counterexample certificate)'.
Usage: python3 recheck.py 'DISC ... ; ... ; ...'   (or a file with one line, argument -f FILE)
"""
import sys

def load(line):
    _, rest = line.strip().split(' ', 1)
    a, b, c = rest.split(';')
    col = list(map(int, b.split()))
    E = [tuple(map(int, t.split('-'))) for t in c.split()]
    return col, E

def uf_components(vs, edges):
    p = {v: v for v in vs}
    def f(a):
        while p[a] != a:
            p[a] = p[p[a]]; a = p[a]
        return a
    for u, v in edges:
        ru, rv = f(u), f(v)
        if ru == rv: return None
        p[ru] = rv
    return len({f(v) for v in vs}), f

def class_enum(nbr, col, x, y, limit=3_000_000):
    """enumerate all colourings reachable by Kempe changes in G=T-xy from col (x coloured as y); canonical form by first occurrence."""
    n = len(col)
    base = tuple(col)
    def canon(c):
        m = {}
        return tuple(m.setdefault(t, len(m)) for t in c)
    seen = {canon(base)}
    todo = [base]; sep = False
    while todo:
        c = todo.pop()
        if c[x] != c[y]: return True, len(seen)
        for a in range(4):
            for b in range(a + 1, 4):
                vis = set()
                for s in range(n):
                    if c[s] in (a, b) and s not in vis:
                        comp = [s]; vis.add(s); i = 0
                        while i < len(comp):
                            u = comp[i]; i += 1
                            for w in nbr[u]:
                                if c[w] in (a, b) and w not in vis:
                                    vis.add(w); comp.append(w)
                        d = list(c)
                        for w in comp: d[w] = a + b - c[w]
                        k = canon(d)
                        if k not in seen:
                            if len(seen) >= limit: raise RuntimeError('class too large')
                            seen.add(k); todo.append(tuple(d))
    return False, len(seen)

def main():
    line = open(sys.argv[2]).readline() if sys.argv[1] == '-f' else ' '.join(sys.argv[1:])
    col, E = load(line)
    V = len(col); n = V + 1; x = V
    E = [tuple(sorted(e)) for e in E]
    assert len(set(E)) == len(E)
    nbr = [set() for _ in range(n)]
    for u, v in E: nbr[u].add(v); nbr[v].add(u)
    for r in range(5): nbr[x].add(r); nbr[r].add(x)
    m = sum(len(a) for a in nbr) // 2
    assert m == 3 * n - 6, 'edge count'
    assert all(len(a) >= 5 for a in nbr), 'min degree'
    ring = [0, 1, 2, 3, 4]
    assert all((i + 1) % 5 in nbr[i] for i in range(5)), 'ring cycle'
    assert not any(j in nbr[i] for i in range(5) for j in range(5) if (j - i) % 5 in (2, 3)), 'ring chord'
    # link is one cycle for every vertex; with m = 3n-6 and connected this certifies a sphere triangulation
    faces = 0
    for v in range(n):
        L = list(nbr[v]); deg = {w: len([z for z in nbr[w] if z in nbr[v]]) for w in L}
        assert all(d == 2 for d in deg.values()), f'link of {v} not 2-regular'
        seen = {L[0]}; st = [L[0]]
        while st:
            u = st.pop()
            for w in nbr[u]:
                if w in nbr[v] and w not in seen: seen.add(w); st.append(w)
        assert len(seen) == len(L), f'link of {v} disconnected'
        faces += len(L)
    assert faces == 3 * (2 * n - 4) and n - m + (2 * m // 3) == 2, 'Euler'
    # colouring
    assert all(col[u] != col[v] for u, v in E)
    assert [col[i] for i in ring] == [0, 1, 0, 2, 3]
    vec = []
    for a, b in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
        vs = [v for v in range(V) if col[v] in (a, b)]
        es = [(u, v) for u, v in E if col[u] in (a, b) and col[v] in (a, b)]
        r = uf_components(vs, es)
        assert r is not None, f'pair {a}{b} has a cycle'
        vec.append(r[0])
    assert vec == [1, 2, 2, 1, 1, 1], vec
    print('structure ok: triangulation, min degree 5, proper, six forests, comps', vec,
          'sizes', [col.count(k) for k in range(4)])
    # fans
    full = col + [0]
    G = lambda y: [nbr[v] - ({y} if v == x else set()) if v != y else nbr[v] - {x} for v in range(n)]
    for j in (1, 3, 4):
        c = list(col) + [col[j]]
        s, sz = class_enum(G(j), c, x, j)
        print(f'fan u{j}: separable={s} class size {sz}')
        assert not s, 'fan not locked'
    def swapped(a, b, seed):
        # component of vertex seed in pair [a,b] of T-x
        comp = {seed}; st = [seed]
        while st:
            u = st.pop()
            for w in nbr[u]:
                if w != x and col[w] in (a, b) and w not in comp: comp.add(w); st.append(w)
        d = list(col)
        for w in comp: d[w] = a + b - col[w]
        return d
    res = []
    for name, (a, b), seed, y in (('nu_gamma', (0, 3), 2, 0), ('nu_beta', (0, 2), 0, 2)):
        d = swapped(a, b, seed) + [0]; d[x] = d[y]
        s, sz = class_enum(G(y), d, x, y)
        print(f'{name} at fan u{y}: separable={s} class size {sz}')
        res.append(s)
    print('N HOLDS' if any(res) else 'N FAILS (counterexample certificate: all classes enumerated above, none separates)')

main()
