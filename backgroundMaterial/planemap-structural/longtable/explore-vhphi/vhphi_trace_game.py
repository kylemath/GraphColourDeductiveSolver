"""EXPLORATORY. Trace-constrained 4-ring game (Long Table, 2026-10-05).

Adversary state = exterior bridge bits on the 4-face phi = (q0,q1,q2,q3), following Math's
trace lemma (docs/reports/MathTriangleCarryResearch.md): for each colour pair P whose
phi-vertices are exactly one opposite pair, a bit "joined through the far side in P".
Constraint (Jordan): two set bits on different diagonals with disjoint colour pairs cannot
coexist.
Dynamics:
  - a player Kempe swap in pair P merges the opposite component iff the P-bit is set;
  - afterwards the bits of P and of its complement are FROZEN (their coloured vertex sets
    in the far side are unchanged); the adversary re-chooses the other bits (any admissible);
  - colours on phi may change, so relevance is recomputed; frozen bits keep their value.
Pure version (hole fixed at v). Player wins at a filled colouring.
The player must win from every start and every admissible initial bit assignment.

Usage: python3 vhphi_trace_game.py MEMBER_JSON
"""
import itertools
import json
import sys

import vhphi_explore as E

PAIRS = [frozenset(p) for p in itertools.combinations(range(4), 2)]


def relevant(st, quad):
    """pairs P meeting phi in exactly one opposite pair -> diagonal index (0: q0q2, 1: q1q3)."""
    out = {}
    for P in PAIRS:
        hit = [i for i in range(4) if st[quad[i]] in P]
        if hit == [0, 2]:
            out[P] = 0
        elif hit == [1, 3]:
            out[P] = 1
    return out


def admissible(bits, rel):
    on = [P for P, b in bits.items() if b]
    for P, R in itertools.combinations(on, 2):
        if rel[P] != rel[R] and not (P & R):
            return False
    return True


def all_bits(rel, fixed):
    free = [P for P in rel if P not in fixed]
    for vals in itertools.product((0, 1), repeat=len(free)):
        b = dict(fixed)
        b.update(zip(free, vals))
        b = {P: v for P, v in b.items() if P in rel}
        if admissible(b, rel):
            yield frozenset(P for P, v in b.items() if v)


def comps(adj, st, P):
    a, b = tuple(P)
    seen = set()
    out = []
    for s in range(len(st)):
        if st[s] not in P or s in seen:
            continue
        c = {s}
        stack = [s]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in c and st[y] in P:
                    c.add(y)
                    stack.append(y)
        seen |= c
        out.append(c)
    return out


def solve(adj, rot, v, quad, fans):
    rotlike = [sorted(a) for a in adj]
    rotlike[v] = list(rot[v])
    starts = list(dict.fromkeys(tuple(s) for s in E.deletion_states(rotlike, v)))
    # states: (colouring tuple, frozenset of on-bits). Colourings not canonicalised (bits name colours).
    def filled(st):
        return len({st[w] for w in adj[v]}) <= 3

    init = []
    for s in starts:
        rel = relevant(s, quad)
        for b in all_bits(rel, {}):
            init.append((s, b))
    # explore closure
    succ = {}
    stack = list(init)
    seen = set(init)
    while stack:
        node = stack.pop()
        st, bits = node
        if filled(st):
            succ[node] = None
            continue
        moves = []
        for P in PAIRS:
            a, b = tuple(P)
            cs = comps(adj, st, P)
            for c in cs:
                S = set(c)
                if P in relevant(st, quad) and P in bits and (c & set(quad)):
                    for c2 in cs:
                        if c2 is not c and (c2 & set(quad)):
                            S |= c2
                nxt = list(st)
                for x in S:
                    nxt[x] = b if st[x] == a else a
                nxt = tuple(nxt)
                comp_P = frozenset(set(range(4)) - P)
                rel2 = relevant(nxt, quad)
                fixed = {}
                for R in (P, comp_P):
                    if R in rel2:
                        fixed[R] = 1 if R in bits else 0
                outs = [(nxt, b2) for b2 in all_bits(rel2, fixed)]
                moves.append(outs)
                for o in outs:
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


def main():
    member = json.load(open(sys.argv[1]))["member"]
    n = member["n"]
    faces = {tuple(f) for f in member["faces"]}
    adjT = E.adjacency(faces, n)
    rot = E.rotation(faces, n)
    s, t = member["deleted"]
    em = E.edge_face_map(faces)
    x, y = em[(s, t)], em[(t, s)]
    quad = [s, y, t, x]
    adj = [set(a) for a in adjT]
    adj[s].discard(t)
    adj[t].discard(s)
    deg5 = [w for w in range(n) if w not in quad and len(adj[w]) == 5]
    report = {}
    for w in deg5:
        fans = E.legal_fans(rot, w, adj)
        res, size = solve(adj, rot, w, quad, fans)
        report[w] = res
        print(w, "states", size, "fans (won, starts x bits):", res, flush=True)
    json.dump({str(k): v for k, v in report.items()}, open("trace-game-order16.json", "w"))


if __name__ == "__main__":
    main()
