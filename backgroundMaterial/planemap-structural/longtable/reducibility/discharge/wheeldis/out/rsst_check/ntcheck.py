"""Near-triangulation check of a kc line (ring R0..R(r-1) as a cycle, interior I0..I(m-1)): every interior vertex's
neighbourhood is one cycle in the graph (a wheel), ring size = r, and Euler V - E + F = 2 with F = triangles + 1
(the outer face, the ring). Prints interior degrees. Usage: python3 ntcheck.py FILE"""
import sys, itertools
for line in open(sys.argv[1]):
    f = line.split(); nm, r, m = f[0], int(f[1]), int(f[2]); rp, ip = f[3].split(';'), f[4].split(';')
    V = ['R%d' % i for i in range(r)] + ['I%d' % i for i in range(m)]; E = set()
    for i in range(r): E.add(frozenset(('R%d' % i, 'R%d' % ((i + 1) % r))))
    for u in range(m):
        if rp[u] != '-': E |= {frozenset(('I%d' % u, 'R%s' % x)) for x in rp[u].split(',')}
        if ip[u] != '-': E |= {frozenset(('I%d' % u, 'I%s' % x)) for x in ip[u].split(',')}
    nb = {v: {w for e in E if v in e for w in e if w != v} for v in V}
    T = {frozenset(t) for t in itertools.combinations(V, 3) if all(frozenset(p) in E for p in itertools.combinations(t, 2))}
    ok = True
    for u in range(m):
        v = 'I%d' % u; L = nb[v]
        # link graph: x ~ y iff x, y adjacent (and both adjacent to v): must be a single cycle covering L
        lk = {x: {y for y in L if frozenset((x, y)) in E} for x in L}
        if any(len(lk[x]) != 2 for x in L): ok = False; print(nm, v, 'link not 2-regular', {x: sorted(lk[x]) for x in L}); continue
        seen = {next(iter(L))}; st = list(seen)
        while st:
            x = st.pop()
            for y in lk[x]:
                if y not in seen: seen.add(y); st.append(y)
        if seen != L: ok = False; print(nm, v, 'link not one cycle')
    F = len(T) + 1; eu = len(V) - len(E) + F
    deg = [len(nb['I%d' % u]) for u in range(m)]
    print('%s: ring %d, m %d, interior degrees %s, V %d E %d triangles %d, Euler %d, wheels %s' % (nm, r, m, deg, len(V), len(E), len(T), eu, 'OK' if ok else 'FAIL'))
