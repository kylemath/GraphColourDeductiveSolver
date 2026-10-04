"""WP7b: dynamic re-partition at traps versus shallow stuck states (see WP7b-declaration.md).

Discovery orders 12-18.  Raw colours throughout; categories fixed by the starting state.
Facts only; no status claims.
"""
import hashlib
import json
from collections import Counter

from broaden_variants import components
from mass_core import FIXTURES, HERE, PAIRS, RootState, degree_five, parse_ascii


def pair_q(s, c):
    q = {pr: 0 for pr in PAIRS}
    for pr, K in components(s, c):
        if K & s.Bset:
            q[pr] += len(K - s.Bset) ** 2
    return q


def rank(s, c):
    p = max(0, len({c[j] for j in s.B}) - 3)
    return s.scale * p + sum(pair_q(s, c).values())


def raw_moves(s, c):
    for (a, b), K in components(s, c):
        yield (a, b), K, tuple((b if x == a else a if x == b else x) if j in K else x for j, x in enumerate(c))


def split(q0, q1, rho):
    rep = sum(q1[p] - q0[p] for p in PAIRS if rho in p)
    sing = sum(q1[p] - q0[p] for p in PAIRS if rho not in p)
    return rep, sing


def main():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    viol = {"H-A": [], "H-B": [], "H-C": []}
    stats = Counter()
    trap_moves = []
    for o in table["orders"]:
        if o["order"] > 18:
            continue
        for g in o["graphs_checked"]:
            rot = parse_ascii(g["ascii"])
            for r in degree_five(rot):
                s = RootState(rot, r)
                for i, c in enumerate(s.C):
                    if s.info[i]["p"] == 0 or s.descent(i, 1) is None:
                        continue
                    trap = s.descent(i, 2) is not None
                    cols = [c[j] for j in s.B]
                    rho = next(x for x in set(cols) if cols.count(x) == 2)
                    q0, R0 = pair_q(s, c), s.info[i]["R"]
                    where = {"order": o["order"], "graph_index": g["graph_index"], "root": r, "coloring": c}
                    firsts = []
                    for pr, K, c1 in raw_moves(s, c):
                        if c1 == c:
                            continue
                        rep, sing = split(q0, pair_q(s, c1), rho)
                        kind = ("rep" if rho in pr else "sing") + ("-B" if K & s.Bset else "-interior")
                        firsts.append((pr, K, c1, kind, rep, sing))
                        stats[("trap" if trap else "shallow", kind, "rep>0" if rep > 0 else "rep<=0")] += 1
                    if trap:
                        for pr, K, c1, kind, rep, sing in firsts:
                            rec = {**where, "pair": pr, "component": sorted(s.V[j] for j in K), "kind": kind,
                                   "d_rep": rep, "d_sing": sing}
                            trap_moves.append(rec)
                            if kind == "rep-B" and rep <= 0:
                                viol["H-A"].append(rec)
                            if kind.startswith("sing") and sing < 0:
                                viol["H-C"].append(rec)
                    else:
                        ok = False
                        for pr, K, c1, kind, rep, sing in firsts:
                            if any(rank(s, c2) < R0 for _, _, c2 in raw_moves(s, c1)):
                                stats[("shallow-escape-first", kind, "rep>0" if rep > 0 else "rep<=0")] += 1
                                ok |= rep <= 0
                        if not ok:
                            viol["H-B"].append(where)
    out = {"scope": "WP7b discovery test on orders 12-18; facts, no status claims.",
           "violations": {k: len(v) for k, v in viol.items()},
           "violation_examples": {k: v[:5] for k, v in viol.items()},
           "stats": {"|".join(k): n for k, n in sorted(stats.items())},
           "trap_first_moves": trap_moves,
           "checkers": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (HERE / "wp7b_test.py", HERE / "mass_core.py", HERE / "WP7b-declaration.md")}}
    (HERE / "wp7b-discovery.json").write_text(json.dumps(out, indent=1) + "\n")
    print("violations:", out["violations"])
    for k, n in out["stats"].items():
        print(" ", k, n)


if __name__ == "__main__":
    main()
