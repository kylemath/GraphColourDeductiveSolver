"""WP7 test of Conjecture 7.3 (see WP7-declaration.md, committed before this run).

Discovery orders 12-18 only.  For every degree-five root and every non-target colouring:
Pi (every singleton pair linked by one chain), m_sing, m_rep, and one/two-swap stuck flags.
Also checks Lemma 7.1 (q_ab and q_cd unchanged by an {a,b} swap) on every move.  Facts only.
"""
import hashlib
import json
from collections import Counter

from broaden_variants import components
from mass_core import FIXTURES, HERE, PAIRS, RootState, degree_five, parse_ascii


def pair_masses(s, c):
    q = {pr: 0 for pr in PAIRS}
    for pr, K in components(s, c):
        if K & s.Bset:
            q[pr] += len(K - s.Bset) ** 2
    return q


def features(s, c):
    cols = [c[j] for j in s.B]
    rho = next(x for x in set(cols) if cols.count(x) == 2)
    single = {cols[k]: s.B[k] for k in range(5) if cols.count(cols[k]) == 1}
    comps = components(s, c)
    pi, link_mass = True, []
    for x, y in [(x, y) for x in single for y in single if x < y]:
        K = next(K for pr, K in comps if pr == (x, y) and single[x] in K)
        if single[y] in K:
            link_mass.append(len(K - s.Bset))
        else:
            pi = False
            link_mass.append(0)
    m_rep = max((len(K - s.Bset) for pr, K in comps if rho in pr and K & s.Bset), default=0)
    return pi, min(link_mass), m_rep


def main():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    counts = Counter()
    violations, lemma_ok, moves_checked = [], True, 0
    for o in table["orders"]:
        if o["order"] > 18:
            continue
        for g in o["graphs_checked"]:
            rot = parse_ascii(g["ascii"])
            for r in degree_five(rot):
                s = RootState(rot, r)
                for i, c in enumerate(s.C):
                    if s.info[i]["p"] == 0:
                        continue
                    pm = pair_masses(s, c)
                    for (a, b), K, _ in s.info[i]["moves"]:
                        Kidx = {s.V.index(v) for v in K}
                        raw = tuple((b if x == a else a if x == b else x) if j in Kidx else x for j, x in enumerate(c))
                        pm2 = pair_masses(s, raw)
                        cd = tuple(sorted(set(range(4)) - {a, b}))
                        lemma_ok &= pm[(a, b)] == pm2[(a, b)] and pm[cd] == pm2[cd]
                        moves_checked += 1
                    pi, ms, mr = features(s, c)
                    stuck2 = s.descent(i, 2) is not None
                    stuck1 = s.descent(i, 1) is not None
                    kind = "two_swap_stuck" if stuck2 else "one_swap_stuck" if stuck1 else "descends_in_one"
                    pred = pi and ms > mr
                    counts[(kind, pred)] += 1
                    if stuck2 and not pred:
                        violations.append({"order": o["order"], "graph_index": g["graph_index"], "root": r,
                                           "coloring": c, "pi": pi, "m_sing": ms, "m_rep": mr})
    table_rows = {f"{k}|predicate={p}": n for (k, p), n in sorted(counts.items())}
    out = {"scope": "WP7 discovery test of Conjecture 7.3 on orders 12-18 only; facts, no status claims.",
           "lemma_7_1_holds_on_all_moves": lemma_ok, "moves_checked": moves_checked,
           "conjecture_7_3_violations": violations, "counts": table_rows,
           "checkers": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (HERE / "wp7_test.py", HERE / "mass_core.py", HERE / "WP7-declaration.md")}}
    (HERE / "wp7-discovery.json").write_text(json.dumps(out, indent=1) + "\n")
    print("Lemma 7.1 holds on all", moves_checked, "moves:", lemma_ok)
    print("Conjecture 7.3 violations (two-swap stuck without predicate):", len(violations))
    for k, n in table_rows.items():
        print(" ", k, n)


if __name__ == "__main__":
    main()
