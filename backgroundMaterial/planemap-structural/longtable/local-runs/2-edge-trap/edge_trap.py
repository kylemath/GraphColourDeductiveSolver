#!/usr/bin/env python3
"""[exploratory] Local compute item 2: Intern D's edge-trap requests (intern-D-cycle4.md) and Math's Theorem 1 (MathEdgeTrap.md)
on the 16 edge-deletion new classes in studio-explore/kempe-classes/edge-new-classes.jsonl.
For each new class: walk the class in T - e from the stored representative (whole-component swaps, states up to renaming,
plain-Python BFS from ../common/kempe_py.py helpers). x, y = ends of e, c = their common colour, p, q = the two common
neighbours of x and y in T (apexes of the two triangles on e), r = the colour on none of x, p, q (when c(p) != c(q)).
Per state:
 (1) x and y lie in one {c, r}-component of T - e;
 (2) p and q are NOT joined in the {c(p), c(q)}-subgraph (n/a when c(p) = c(q));
 (3) colour class c dominates T - e (every vertex not coloured c has a neighbour coloured c);
 (4) c(p) = c(q).
Also: Theorem 1's full condition (x, y share a {c, t}-component for all three t != c), and closure (every swap image is in
the class, with c(x) = c(y)), which is Intern D's request 3.
usage: python3 edge_trap.py > edge-trap-results.json"""
import json, os, sys, itertools
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import plantri_ascii, adj_from_rot

SRC = os.path.join(H, "..", "..", "studio-explore", "kempe-classes", "edge-new-classes.jsonl")


class Lazy:
    def __init__(self, adj):
        self.order = sorted(adj); self.idx = {u: i for i, u in enumerate(self.order)}; self.N = len(self.order)
        self.nbm = [sum(1 << self.idx[w] for w in adj[u]) for u in self.order]

    def canon(self, c):
        mp = {}; return tuple(mp.setdefault(x, len(mp)) for x in c)

    def flood(self, start, M):
        comp = front = start
        while front:
            nb = 0; f = front
            while f:
                low = f & -f; nb |= self.nbm[low.bit_length() - 1]; f ^= low
            nb &= M & ~comp; comp |= nb; front = nb
        return comp

    def cm(self, s):
        m = [0] * 4
        for i, x in enumerate(s): m[x] |= 1 << i
        return m

    def moves(self, s):
        cm = self.cm(s); out = []
        for p, q in itertools.combinations(range(4), 2):
            M = cm[p] | cm[q]
            while M:
                K = self.flood(M & -M, cm[p] | cm[q]); M &= ~K
                d = [(q if x == p else p) if K >> i & 1 else x for i, x in enumerate(s)]
                out.append(self.canon(d))
        return out

    def joined(self, s, u, w, cols):
        cm = self.cm(s); M = 0
        for t in cols: M |= cm[t]
        iu, iw = self.idx[u], self.idx[w]
        if not (M >> iu & 1 and M >> iw & 1): return False
        return bool(self.flood(1 << iu, M) >> iw & 1)


def main():
    rows = []; theorem1_all = True; pred1_all = True
    for li, line in enumerate(open(SRC)):
        r = json.loads(line); rot = plantri_ascii(r["plantri_ascii"]); adj = adj_from_rot(rot)
        x, y = r["edge"]; common = sorted(adj[x] & adj[y]); assert len(common) == 2, common
        p, q = common
        adj2 = {u: set(nb) for u, nb in adj.items()}; adj2[x].discard(y); adj2[y].discard(x)
        Z = Lazy(adj2)
        for ci, nc in enumerate(r["new_classes"]):
            s0 = Z.canon([nc["colouring"][str(u)] for u in Z.order])
            cls, seen = [s0], {s0}
            for s in cls:
                for t in Z.moves(s):
                    if t not in seen: seen.add(t); cls.append(t)
            per = []
            for s in cls:
                col = {u: s[Z.idx[u]] for u in Z.order}; c = col[x]
                assert col[y] == c
                cp, cq = col[p], col[q]
                rest = [t for t in range(4) if t not in (c, cp, cq)]
                f1 = {str(t): Z.joined(s, x, y, (c, t)) for t in rest}           # (1), per remaining colour r
                f2 = None if cp == cq else (not Z.joined(s, p, q, (cp, cq)))       # (2)
                f3 = all(col[u] == c or any(col[w] == c for w in adj2[u]) for u in Z.order)  # (3)
                f4 = cp == cq                                                       # (4)
                th1 = all(Z.joined(s, x, y, (c, t)) for t in range(4) if t != c)
                closure = all(t in seen for t in Z.moves(s))
                per.append({"c": c, "c_p": cp, "c_q": cq, "r": rest if len(rest) > 1 else rest[0],
                            "1_cr_joins_xy": f1, "2_pq_not_joined": f2, "3_c_dominating": f3, "4_cp_eq_cq": f4,
                            "theorem1_all_three_chains": th1, "closed_under_swaps": closure})
                theorem1_all &= th1; pred1_all &= all(f1.values())
            rows.append({"record": li, "order": r["order"], "plantri_index": r["plantri_index"], "edge": [x, y],
                         "endpoint_degrees": r["endpoint_degrees"], "p": p, "q": q, "class": ci, "class_size_walked": len(cls),
                         "class_size_stored": nc["size"], "states": per})
    summ = {"classes": len(rows), "edge_records": li + 1,
            "all_sizes_match": all(x["class_size_walked"] == x["class_size_stored"] for x in rows),
            "prediction_1_holds_every_state": pred1_all, "theorem1_condition_every_state": theorem1_all}
    print(json.dumps({"summary": summ, "classes": rows}, indent=1))


if __name__ == "__main__":
    main()
