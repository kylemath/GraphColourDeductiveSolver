#!/usr/bin/env python3
"""Audit replay of local compute's quarter-floor data (8ab6f1d, 0c0e098). Stdlib only; imports no team code.

For each degree-5 hole v of a gentri graph (studiointel/gentri/triN.txt; line 'G n HEX ...', HEX = planar code,
1-based neighbours in rotation order, 00 ends a vertex; parsed here independently):
  * all proper 4-colourings of T - v up to renaming (canonical: colours relabelled by first occurrence in vertex order);
  * Kempe classes under whole two-colour component swaps (singletons allowed), by union-find;
  * per class [size, F0..F4, U0..U4, D0..D4], link positions in the rotation order rot[v]:
      F_i: filled (link uses <= 3 colours), singleton colour at position i;
      U_j: unfilled, repeat at positions j, j+2;  D_j subset of U_j: doubly locked;
  * checks: floor 4F >= size; ineq U_j <= F_{j+1}+F_{j+3}+F_{j+4}; Lemma A |U_j - D_j| <= F_{j+3}+F_{j+4};
    Lemma A's map phi (swap the component of a if lock 1 fails, else of b): image filled, singleton at j+4 / j+3,
    same class; injective per (j, case); collisions across j counted.
usage: qf_replay.py ORDER GENTRI_FILE [IDX:HOLE ...]   (no IDX:HOLE = every graph, every degree-5 hole)
       prints one JSON line per hole.
"""
import json, sys
from itertools import combinations


def parse(line):
    p = line.split(); n = int(p[1]); h = p[2]
    rot, cur = [], []
    for i in range(0, len(h), 2):
        b = int(h[i:i + 2], 16)
        if b == 0: rot.append(cur); cur = []
        else: cur.append(b - 1)
    assert len(rot) == n
    for v in range(n):                       # sanity: symmetric, simple
        for w in rot[v]: assert v in rot[w] and w != v
        assert len(set(rot[v])) == len(rot[v])
    return rot


def hole_data(rot, h):
    n = len(rot); L = rot[h]; assert len(L) == 5
    V = [u for u in range(n) if u != h]
    # vertex order: BFS from L[0] in T - h (pruning); index map
    order, seen = [L[0]], {L[0]}
    for x in order:
        for y in rot[x]:
            if y != h and y not in seen: seen.add(y); order.append(y)
    assert len(order) == n - 1
    pos = {u: i for i, u in enumerate(order)}
    nb = [[pos[y] for y in rot[u] if y != h] for u in order]
    back = [[y for y in nb[i] if y < i] for i in range(len(order))]
    N = len(order); link = [pos[x] for x in L]

    states = []; col = [0] * N
    def rec(i, mx):
        if i == N: states.append(tuple(col)); return
        bad = {col[y] for y in back[i]}
        for c in range(min(mx + 2, 4)):
            if c not in bad: col[i] = c; rec(i + 1, max(mx, c))
    col[0] = 0; rec(1, 0)
    idx = {s: k for k, s in enumerate(states)}

    def canon(s):
        m = {}; return tuple(m.setdefault(c, len(m)) for c in s)

    def comp(s, start, p, q):
        st = [start]; K = {start}
        while st:
            x = st.pop()
            for y in nb[x]:
                if y not in K and s[y] in (p, q): K.add(y); st.append(y)
        return K

    def swap(s, K, p, q):
        t = list(s)
        for x in K: t[x] = q if s[x] == p else p
        return canon(t)

    par = list(range(len(states)))
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for k, s in enumerate(states):
        for p, q in combinations(range(4), 2):
            done = set()
            for x in range(N):
                if s[x] in (p, q) and x not in done:
                    K = comp(s, x, p, q); done |= K
                    a, b = find(k), find(idx[swap(s, K, p, q)])
                    if a != b: par[a] = b

    def classify(s):
        lc = [s[x] for x in link]
        if len(set(lc)) <= 3:
            i = next(i for i in range(5) if lc.count(lc[i]) == 1)
            return ('F', i, None)
        j = next(j for j in range(5) if lc[j] == lc[(j + 2) % 5])
        m, a, b = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]
        K1 = comp(s, m, s[m], s[a]); K2 = comp(s, m, s[m], s[b])
        return ('U', j, (a in K1, b in K2))

    cls = {}
    for k, s in enumerate(states):
        r = find(k)
        v = cls.setdefault(r, [0] * 16); v[0] += 1
        t, i, lk = classify(s)
        if t == 'F': v[1 + i] += 1
        else:
            v[6 + i] += 1
            if lk[0] and lk[1]: v[11 + i] += 1

    # Lemma A's map phi on non-DL unfilled states
    img = {}; per_case_coll = 0; bad_image = 0
    for k, s in enumerate(states):
        t, j, lk = classify(s)
        if t != 'U' or (lk[0] and lk[1]): continue
        m = link[(j + 1) % 5]
        e = link[(j + 3) % 5] if not lk[0] else link[(j + 4) % 5]
        case = 1 if not lk[0] else 2
        K = comp(s, e, s[m], s[e]); f = swap(s, K, s[m], s[e]); fk = idx[f]
        tf, i, _ = classify(f)
        want = (j + 4) % 5 if case == 1 else (j + 3) % 5
        if tf != 'F' or i != want or find(fk) != find(k): bad_image += 1
        img.setdefault(fk, []).append((j, case, k))
    for fk, pre in img.items():
        keys = [(j, c) for j, c, _ in pre]
        if len(set(keys)) != len(keys): per_case_coll += 1
    multi = sum(1 for pre in img.values() if len(pre) > 1)
    maxpre = max((len(p) for p in img.values()), default=0)

    classes = sorted(cls.values())
    viol = {'floor': 0, 'ineq': 0, 'lemmaA': 0}
    for v in classes:
        F, U, D = v[1:6], v[6:11], v[11:16]
        if 4 * sum(F) < v[0]: viol['floor'] += 1
        for j in range(5):
            if U[j] > F[(j + 1) % 5] + F[(j + 3) % 5] + F[(j + 4) % 5]: viol['ineq'] += 1
            if U[j] - D[j] > F[(j + 3) % 5] + F[(j + 4) % 5]: viol['lemmaA'] += 1
    floor_classes = [v[0] for v in classes if 4 * sum(v[1:6]) == v[0]]
    return dict(states=len(states), classes=classes, violations=viol, floor_class_sizes=floor_classes,
                phi=dict(images=len(img), bad_image=bad_image, per_case_collisions=per_case_coll,
                         filled_with_2_preimages=multi, max_preimages=maxpre))


def main():
    order = int(sys.argv[1]); lines = [x for x in open(sys.argv[2]) if x.strip()]
    if len(sys.argv) > 3:
        tasks = [tuple(map(int, a.split(':'))) for a in sys.argv[3:]]
    else:
        tasks = [(gi, h) for gi, l in enumerate(lines) for h, r in enumerate(parse(l)) if len(r) == 5]
    for gi, h in tasks:
        rot = parse(lines[gi])
        d = hole_data(rot, h); d.update(order=order, gentri_index=gi, hole=h)
        print(json.dumps(d), flush=True)


if __name__ == '__main__':
    main()
