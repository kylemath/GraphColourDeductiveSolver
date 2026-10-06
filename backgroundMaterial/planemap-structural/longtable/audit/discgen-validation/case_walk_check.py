#!/usr/bin/env python3
"""Independent check of the order-24 (G*) failure certificates and of the Case I/II/Ia/Ib table.

Audit code. It imports no Math or Long Table code. Definitions, as written by Math:
  - rigid triply locked state c on T - x, ring word D a D b g on u0..u4, colours 0,1,0,2,3
    (MathNAttack.md; d1-hand-attack.md);
  - fan at u_i: G_i = T - x u_i, x coloured c(u_i); separable iff the G_i-Kempe class (whole
    components of two-colour subgraphs of G_i, x included) has a colouring with c(x) != c(u_i);
    locked = not separable;
  - c' = nu_g c: swap the [D,g]-component of u2 in T - x; c'' is the mirror (reverse labelling);
  - walk (MathNCaseI.md section 1): c1 = swap the [a,g]-component of u4 in c'; c2 = swap the
    [a,b]-component of u4 in c1; Case II iff u2 !~ u4 in [b,g]_2, Case I iff u2 ~ u4;
    c3 = swap the [b,g]-component of u4 in c2;
  - (G*) at c3 (section 3): u1 ~ u3 or u1 ~ u4 in [a,g]_3; Ia = Case I and (G*) holds,
    Ib = Case I and (G*) fails (MathNIaIb.md).
The Kempe classes are explored completely (cap 500000 colourings, reported if hit).
usage: case_walk_check.py FILE...   (files of DISC lines, or res lines containing a DISC line)
"""
import sys, json, re

D, A, B, G = 0, 1, 2, 3


def parse(line):
    m = re.search(r'DISC([^;]*);([^;]*);(.*)', line)
    cols = list(map(int, m.group(2).split()))
    n = len(cols) + 1; x = n - 1
    adj = [set() for _ in range(n)]
    for e in m.group(3).split():
        a, b = map(int, e.split('-')); adj[a].add(b); adj[b].add(a)
    for k in range(5): adj[x].add(k); adj[k].add(x)
    return adj, cols, x


def comp(adj, col, s, p, q, skip):
    """Component of s in the {p,q} subgraph, over vertices not in skip."""
    seen = {s}; st = [s]
    while st:
        v = st.pop()
        for w in adj[v]:
            if w not in skip and w not in seen and col[w] in (p, q):
                seen.add(w); st.append(w)
    return seen


def swap(col, S, p, q):
    c = list(col)
    for v in S: c[v] = q if c[v] == p else p
    return c


def connected(adj, col, a, b, p, q, x):
    return b in comp(adj, col, a, p, q, {x})


def canon(col):
    m = {}; return tuple(m.setdefault(c, len(m)) for c in col)


def separable(adj, col, x, ui, cap=500000):
    """Fan at u_i: G = T - x u_i, x coloured col[u_i]. BFS of the G-Kempe class."""
    adjG = [set(s) for s in adj]; adjG[x].discard(ui); adjG[ui].discard(x)
    start = list(col); start[x] = col[ui]
    assert all(start[a] != start[b] for a in range(len(adj)) for b in adjG[a])
    seen = {canon(start)}; queue = [start]
    while queue:
        c = queue.pop()
        if c[x] != c[ui]: return True, len(seen)
        for p in range(4):
            for q in range(p + 1, 4):
                done = set()
                for s in range(len(adj)):
                    if c[s] in (p, q) and s not in done:
                        K = comp(adjG, c, s, p, q, set()); done |= K
                        d = swap(c, K, p, q); k = canon(d)
                        if k not in seen:
                            if len(seen) >= cap: return None, len(seen)
                            seen.add(k); queue.append(d)
    return False, len(seen)


def walk(adj, col, x):
    """c' and the walk at u0. Returns dict."""
    u = [0, 1, 2, 3, 4]
    cp = swap(col, comp(adj, col, u[2], D, G, {x}), D, G)            # c' ring D a g b g
    assert [cp[i] for i in u] == [D, A, G, B, G], [cp[i] for i in u]
    lock_u0 = separable(adj, cp, x, u[0])
    c1 = swap(cp, comp(adj, cp, u[4], A, G, {x}), A, G)
    c2 = swap(c1, comp(adj, c1, u[4], A, B, {x}), A, B)
    assert [c2[i] for i in u] == [D, A, G, A, B], [c2[i] for i in u]
    caseI = connected(adj, c2, u[2], u[4], B, G, x)
    c3 = swap(c2, comp(adj, c2, u[4], B, G, {x}), B, G)
    gstar = connected(adj, c3, u[1], u[3], A, G, x) or connected(adj, c3, u[1], u[4], A, G, x)
    chainDB = connected(adj, c3, u[0], u[2], D, B, x)
    return dict(neighbour_separable_u0=lock_u0[0], class_size=lock_u0[1],
                case='I' if caseI else 'II', ring_c3=[c3[i] for i in u],
                Gstar=gstar if caseI else None, chain_DB_intact_c3=chainDB if caseI else None,
                sub=('Ia' if gstar else 'Ib') if caseI else 'II')


def mirror(adj, col, x):
    """Reverse labelling: new u0..u4 = old u2,u1,u0,u4,u3; colours b<->g. Relabel vertices."""
    perm = {2: 0, 1: 1, 0: 2, 4: 3, 3: 4}
    n = len(adj); mp = {v: perm.get(v, v) for v in range(n)}
    adj2 = [set() for _ in range(n)]
    for v in range(n):
        for w in adj[v]: adj2[mp[v]].add(mp[w])
    sw = {D: D, A: A, B: G, G: B}
    col2 = [0] * n
    for v in range(n - 1): col2[mp[v]] = sw[col[v]]
    return adj2, col2, x


def check(line):
    adj, cols, x = parse(line)
    col = cols + [-1]
    assert cols[:5] == [D, A, D, B, G]
    locks = {f'u{i}': separable(adj, col, x, i)[0] for i in (1, 3, 4)}
    out = dict(triply_locked=not any(locks.values()), fan_separable=locks)
    out['c1'] = walk(adj, col, x)
    out['c2'] = walk(*mirror(adj, col, x))
    out['N_holds'] = bool(out['c1']['neighbour_separable_u0'] or out['c2']['neighbour_separable_u0'])
    return out


if __name__ == '__main__':
    res = []
    for path in sys.argv[1:]:
        for ln, line in enumerate(open(path), 1):
            if 'DISC' not in line: continue
            r = check(line); r['file'] = path.split('/')[-1]; r['line'] = ln; res.append(r)
            print(json.dumps(r), flush=True)
