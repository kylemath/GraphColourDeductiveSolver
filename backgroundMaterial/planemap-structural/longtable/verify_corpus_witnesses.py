"""Long Table: independent replay of the corpus team's mass-macro failures.

Recomputes, with mass_core.py (no code shared with mass-macro.py): every degree-five root of
the named fixture order 17 / graph 0, and every root the published table marks as failing.
Compares orbit, non-target, one- and two-swap stuck counts and the outcome, and replays each
published first witness rank.  Not a corpus enumeration.  Reports facts, not statuses.
"""
import hashlib
import json
from pathlib import Path

from mass_core import FIXTURES, HERE, RootState, degree_five, parse_ascii


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    table_path = FIXTURES / "mass-macro-results.json"
    table = json.loads(table_path.read_text())
    graphs = {(o["order"], g["graph_index"]): g for o in table["orders"] for g in o["graphs_checked"]}
    targets = {key: [r["root"] for r in g["roots"] if r["outcome"] == "fails"] for key, g in graphs.items()}
    targets = {k: v for k, v in targets.items() if v}
    targets[(17, 0)] = degree_five(parse_ascii(graphs[(17, 0)]["ascii"]))
    rows, ok = [], True
    for key in sorted(targets):
        g = graphs[key]
        rot = parse_ascii(g["ascii"])
        published = {r["root"]: r for r in g["roots"]}
        for r in targets[key]:
            st = RootState(rot, r)
            st.check_closure()
            m = st.mass_summary(keep_witness=True)
            p = published[r]
            mine = (m["coloring_orbits"], m["non_target"], m["one_swap_stuck"], m["two_swap_stuck"],
                    "passes" if m["good_macro2"] else "fails")
            theirs = (p["coloring_orbits"], p["non_target_orbits"], p["one_swap_stuck_orbits"],
                      p["two_swap_stuck_orbits"], p["outcome"])
            same = mine == theirs and st.V == p["vertex_order"]
            row = {"order": key[0], "graph_index": key[1], "root": r, "mine": mine, "published": theirs,
                   "match": same}
            if m.get("two_swap_first_stuck"):
                w = m["two_swap_first_stuck"]
                row["first_stuck_rank"] = w["rank"]
                row["first_stuck_integer_rank"] = w["integer_rank"]
                row["first_stuck_coloring"] = w["coloring"]
            ok &= same
            rows.append(row)
            print(("OK  " if same else "DIFF") + f" order {key[0]} graph {key[1]} root {r}: {mine}"
                  + ("" if same else f" vs published {theirs}"))
    first = next(x for x in rows if (x["order"], x["graph_index"], x["root"]) == (17, 0, 4))
    want = [0, 1, 2, 3, 2, 0, 3, 1, 0, 1, 0, 3, 1, 2, 3, 2]
    witness_ok = first.get("first_stuck_integer_rank") == 1878 and tuple(first.get("first_stuck_rank", ())) == (1, 143)
    print("first witness order 17 graph 0 root 4 at R = 1878, (p,q) = (1,143):", witness_ok,
          "| same first colouring:", list(first.get("first_stuck_coloring", [])) == want)
    out = {"scope": "Independent replay of published mass-macro failing roots and of every root of the "
                    "order-17 graph-0 fixture. Not a corpus enumeration; no status claims.",
           "inputs": {table_path.name: sha(table_path)},
           "checkers": {p.name: sha(p) for p in (HERE / "mass_core.py", HERE / "verify_corpus_witnesses.py")},
           "all_match": ok, "first_witness_rank_match": witness_ok, "rows": rows}
    (HERE / "verify-corpus-witnesses.json").write_text(json.dumps(out, indent=1) + "\n")
    print("all match:", ok)


if __name__ == "__main__":
    main()
