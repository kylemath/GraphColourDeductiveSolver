"""EXPLORATORY. Trace game on a designated face of length k (4 or 5), Long Table 2026-10-05.

Bits: a colour pair P is relevant when the face vertices coloured from P form exactly two runs
(maximal cyclically consecutive blocks). One bit per relevant pair ("the two runs are joined
through the far side in P"). Admissible: no two set bits with disjoint pairs whose runs
alternate around the face. A swap in P merges the other face-meeting P-component iff the bit
is set; afterwards bits of P and of the complementary pair are kept (frozen-pair fact), the
rest re-chosen adversarially. Slides (optional) keep every bit.

Members: disc triangulations from `plantri -P<k> m -a` (chordless outer k-face, the face is
phi), every interior vertex of degree >= 5.

Usage: python3 vhphi_trace_k.py K MMIN MMAX PLANTRI [--mixed]
"""
import itertools
import json
import subprocess
import sys

import vhphi_explore as E

PAIRS = [frozenset(p) for p in itertools.combinations(range(4), 2)]
HOLE = 4


def disc_faces(rot):
    pos = [{w: i for i, w in enumerate(r)} for r in rot]
    seen = set()
    faces = []
    for u in range(len(rot)):
        for v in rot[u]:
            if (u, v) in seen:
                continue
            f = []
            a, b = u, v
            while (a, b) not in seen:
                seen.add((a, b))
                f.append(a)
                i = pos[b][a]
                c = rot[b][(i + 1) % len(rot[b])]
                a, b = b, c
            faces.append(f)
    return faces


def runs(st, face, P):
    k = len(face)
    inP = [st[face[i]] in P for i in range(k)]
    if all(inP):
        return [list(range(k))]
    start = next(i for i in range(k) if not inP[i])
    out, cur = [], []
    for j in range(1, k + 1):
        i = (start + j) % k
        if inP[i]:
            cur.append(i)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def relevant(st, face):
    rel = {}
    for P in PAIRS:
        r = runs(st, face, P)
        if len(r) == 2:
            rel[P] = r
    return rel


def alternate(r1, r2, k):
    """P has runs r1 (two), R has runs r2 (two), on disjoint positions. True iff R's runs lie
    in different gaps between P's runs."""
    p0, p1 = set(r1[0]), set(r1[1])
    gap = {}
    g = 0
    s = r1[0][-1]  # walk forward from the end of run P0 (runs are listed in forward order)
    for j in range(1, k):
        i = (s + j) % k
        if i in p1:
            g = 1
        elif i in p0:
            break
        else:
            gap[i] = g
    gr = [{gap[i] for i in run if i in gap} for run in r2]
    return gr[0] != gr[1]


def admissible(on, rel, k):
    for P, R in itertools.combinations(on, 2):
        if not (P & R) and alternate(rel[P], rel[R], k):
            return False
    return True


def all_bits(rel, fixed, k):
    free = [P for P in rel if P not in fixed]
    base = [P for P, v in fixed.items() if v and P in rel]
    for vals in itertools.product((0, 1), repeat=len(free)):
        on = base + [P for P, b in zip(free, vals) if b]
        if admissible(on, rel, k):
            yield frozenset(on)


def comps(adj, st, P):
    seen, out = set(), []
    for s in range(len(st)):
        if st[s] not in P or s in seen:
            continue
        c, stack = {s}, [s]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in c and st[y] in P:
                    c.add(y)
                    stack.append(y)
        seen |= c
        out.append(c)
    return out


def solve(adj, rot, v, face, fans, mixed=False, budget=2_000_000):
    k = len(face)
    fset = set(face)
    rotlike = [sorted(a) for a in adj]
    rotlike[v] = list(rot[v])
    starts = list(dict.fromkeys(tuple(s) for s in E.deletion_states(rotlike, v)))

    def filled(st):
        h = st.index(HOLE)
        return len({st[w] for w in adj[h]}) <= 3

    init = []
    for s in starts:
        rel = relevant(s, face)
        for b in all_bits(rel, {}, k):
            init.append((s, b))
    succ, stack, seen = {}, list(init), set(init)
    while stack:
        if len(seen) > budget:
            return None, len(seen)
        node = stack.pop()
        st, bits = node
        if filled(st):
            succ[node] = None
            continue
        moves = []
        rel = relevant(st, face)
        for P in PAIRS:
            a, b = tuple(P)
            cs = comps(adj, st, P)
            for c in cs:
                S = set(c)
                if P in rel and P in bits and (c & fset):
                    for c2 in cs:
                        if c2 is not c and (c2 & fset):
                            S |= c2
                nxt = list(st)
                for x in S:
                    nxt[x] = b if st[x] == a else a
                nxt = tuple(nxt)
                cP = frozenset(set(range(4)) - P)
                rel2 = relevant(nxt, face)
                fixed = {R: (1 if R in bits else 0) for R in (P, cP) if R in rel2}
                outs = [(nxt, b2) for b2 in all_bits(rel2, fixed, k)]
                moves.append(outs)
                for o in outs:
                    if o not in seen:
                        seen.add(o)
                        stack.append(o)
        if mixed:
            h = st.index(HOLE)
            cols = [st[w] for w in adj[h]]
            for u in adj[h]:
                if u in fset or cols.count(st[u]) != 1:
                    continue
                nxt = list(st)
                nxt[h] = st[u]
                nxt[u] = HOLE
                o = (tuple(nxt), bits)
                moves.append([o])
                if o not in seen:
                    seen.add(o)
                    stack.append(o)
        succ[node] = moves
    win = {n for n, m in succ.items() if m is None}
    changed = True
    while changed:
        changed = False
        for n, m in succ.items():
            if n in win or m is None:
                continue
            for outs in m:
                if all(o in win for o in outs):
                    win.add(n)
                    changed = True
                    break
    res = []
    for i, (p, q), (r, t) in fans:
        nodes = [(s, b) for (s, b) in init if s[p] != s[q] and s[r] != s[t]]
        res.append((i, sum(n in win for n in nodes), len(nodes)))
    return res, len(seen)


def members(k, m, plantri):
    out = subprocess.run([plantri, f"-P{k}", str(m), "-a"], capture_output=True, text=True).stdout
    for li, line in enumerate(out.splitlines()):
        parts = line.split()
        if len(parts) != 2:
            continue
        rot = [[ord(c) - 97 for c in r] for r in parts[1].split(",")]
        fs = disc_faces(rot)
        outer = [f for f in fs if len(f) == k]
        if len(outer) != 1:
            continue
        face = outer[0]
        interior = [w for w in range(m) if w not in face]
        if not interior or any(len(rot[w]) < 5 for w in interior):
            continue
        yield li, rot, face, interior


def main():
    k, mmin, mmax, plantri = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    mixed = "--mixed" in sys.argv
    report = []
    for m in range(mmin, mmax + 1):
        cnt = fails = 0
        for li, rot, face, interior in members(k, m, plantri):
            adj = [set(r) for r in rot]
            deg5 = [w for w in interior if len(rot[w]) == 5]
            best = []
            for v in deg5:
                fans = E.legal_fans(rot, v, adj)
                res, size = solve(adj, rot, v, face, fans, mixed=mixed)
                best.append((v, res))
            win = any(res and any(w == t for _, w, t in res) for _, res in best)
            cnt += 1
            fails += (not win)
            report.append({"k": k, "m": m, "idx": li, "interior": len(interior), "deg5": deg5,
                           "win": win, "detail": best, "line": None if win else
                           ",".join("".join(chr(97 + x) for x in r) for r in rot)})
            if not win:
                print("FAIL", k, m, li, "interior", len(interior), "deg5", deg5, best, flush=True)
        print("k", k, "m", m, "members", cnt, "fails", fails, flush=True)
    tag = "mixed" if mixed else "pure"
    json.dump(report, open(f"trace-k{k}-{mmin}-{mmax}-{tag}.json", "w"))


if __name__ == "__main__":
    main()
