"""WP7f: check hypothesis H-T on the 39 warned runs (see WP7f-declaration.md).

For every non-strict warned colouring, look for a strict warned colouring of the same run that
reaches it by one swap of a two-vertex component {h, x} with h outside N[r].  Uses the math
team's warning traces; no new colourings.  Facts only; no status claims.
"""
import hashlib
import json

from mass_core import FIXTURES, HERE, RootState, parse_ascii


def hub_toggles(s, i, closed_root_nbhd):
    """(hub, partner, successor index) for each two-vertex component with a vertex outside N[r]."""
    out = []
    for _, K, t in s.info[i]["moves"]:
        if len(K) == 2 and t != i:
            hubs = [v for v in K if v not in closed_root_nbhd]
            for h in hubs:
                out.append((h, next(v for v in K if v != h), t))
    return out


def main():
    path = FIXTURES / "breadcrumb-warning-traces.json"
    traces = json.loads(path.read_text())
    rows, kills = [], []
    for row in traces["rows"]:
        rot = parse_ascii(row["ascii"])
        r = row["root"]
        s = RootState(rot, r)
        assert s.V == row["vertex_order"]
        closed = set(rot[r]) | {r}
        for k, run in enumerate(row["runs"]):
            warned = sorted({s.index[tuple(w["coloring"])] for w in run["warnings"]})
            if not warned:
                continue
            strict = [i for i in warned if s.descent(i, 2) is not None]
            loose = [i for i in warned if i not in strict]
            links, hubs = {}, set()
            for w in loose:
                found = None
                for t in strict:
                    for h, x, succ in hub_toggles(s, t, closed):
                        if succ == w:
                            found = (h, x, t)
                            break
                    if found:
                        break
                links[w] = found
                if found:
                    hubs.add(found[0])
                else:
                    diffs = [sum(a != b for a, b in zip(s.C[w], s.C[t])) for t in strict] or [None]
                    kills.append({"order": row["order"], "graph_index": row["graph_index"], "root": r, "run": k,
                                  "warned_non_strict": list(s.C[w]), "strict_in_run": len(strict),
                                  "min_raw_difference_to_a_strict_warning": min(d for d in diffs if d is not None) if strict else None})
            rows.append({"order": row["order"], "graph_index": row["graph_index"], "root": r, "run": k,
                         "strict": len(strict), "non_strict": len(loose),
                         "toggles": {str(w): (list(v[:2]) if v else None) for w, v in links.items()},
                         "distinct_hubs": sorted(hubs)})
    out = {"scope": "WP7f check of H-T on the 39 warned runs; finite evidence, no status claims.",
           "runs": len(rows), "kills": kills, "h_t_survives": not kills,
           "max_non_strict_per_run": max(r["non_strict"] for r in rows),
           "max_hubs_per_run": max(len(r["distinct_hubs"]) for r in rows),
           "rows": rows,
           "inputs": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()},
           "checkers": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (HERE / "wp7f_test.py", HERE / "WP7f-declaration.md", HERE / "mass_core.py")}}
    (HERE / "wp7f-results.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"runs {len(rows)}; H-T kills {len(kills)}; max non-strict per run {out['max_non_strict_per_run']}; "
          f"max hubs per run {out['max_hubs_per_run']}")
    from collections import Counter
    print(Counter((r["order"], r["graph_index"], r["root"], r["strict"], r["non_strict"], tuple(r["distinct_hubs"])) for r in rows))
    for kk in kills[:5]:
        print("KILL", kk)


if __name__ == "__main__":
    main()
