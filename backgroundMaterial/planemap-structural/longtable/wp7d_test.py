"""WP7d: structure of the order-17 graph-3 dead-end region and the C7d charging claim.

See WP7d-declaration.md (committed before this run, amended before this run).  Part 1 at the
named fixture roots 3 and 13 in their own raw labels; Part 2 on all 39 warned runs of the math
team's breadcrumb-warning-traces.json.  Facts only; no status claims.
"""
import hashlib
import json
from collections import Counter

from automorphisms import automorphisms
from mass_core import FIXTURES, HERE, RootState, canon, parse_ascii
from wp7c_test import pattern


def analyse(s):
    n = len(s.C)
    nxt = [sorted({t for _, _, t in s.info[i]["moves"]} - {i}) for i in range(n)]
    R = [s.info[i]["R"] for i in range(n)]
    good = {}
    for i in sorted(range(n), key=lambda i: R[i]):
        if s.info[i]["p"] == 0:
            good[i] = True
            continue
        two = set(nxt[i]) | {u for x in nxt[i] for u in nxt[x]}
        good[i] = any(R[j] < R[i] and good[j] for j in two)
    strict = {i for i in range(n) if s.info[i]["p"] == 1 and s.descent(i, 2) is not None}
    return nxt, R, good, strict


def act(s, phi, c):
    """Image of colouring c (over s.V) under an automorphism fixing the root, canonicalised."""
    col = dict(zip(s.V, c))
    inv = {phi[v]: v for v in phi}
    return tuple(canon([col[inv[w]] for w in s.V]))


def part1(rot, r):
    s = RootState(rot, r)
    nxt, R, good, strict = analyse(s)
    region = sorted(i for i in range(len(s.C)) if not good[i])
    rset = set(region)
    pits, seen = [], set()
    for i in region:
        if i in seen:
            continue
        comp, stack = {i}, [i]
        while stack:
            x = stack.pop()
            for y in nxt[x]:
                if y in rset and y not in comp:
                    comp.add(y)
                    stack.append(y)
        seen |= comp
        pits.append(sorted(comp))
    pit_of = {i: k for k, p in enumerate(pits) for i in p}
    toggles = []
    for p in pits:
        t = [i for i in p if i in strict]
        w = [i for i in p if i not in strict]
        moves = [(pr, list(K)) for pr, K, x in s.info[t[0]]["moves"] if x == w[0]] if t and w else []
        toggles.append({"trap": t, "twin": w, "R": [R[i] for i in p], "toggle_moves": moves})
    rim = sorted({j for i in region for j in nxt[i]} - rset)
    touch = {j: sorted({pit_of[i] for i in nxt[j] if i in rset}) for j in rim}
    connectors = [j for j in rim if len(touch[j]) == 2]
    spurs = [j for j in rim if len(touch[j]) == 1]
    stab = [a for a in automorphisms(rot) if a[r] == r]
    orbit = lambda i: sorted({s.index[act(s, a, s.C[i])] for a in stab})
    trap_states = sorted(strict & rset)
    twin_states = sorted(rset - strict)
    trap_twin_by_symmetry = any(s.index[act(s, a, s.C[tg["trap"][0]])] == tg["twin"][0]
                                for a in stab for tg in toggles if tg["trap"] and tg["twin"])
    inter = []
    for i in region:
        for x in nxt[i]:
            for j in nxt[x]:
                if j in rset and pit_of[j] != pit_of[i] and R[j] < R[i]:
                    inter.append({"from": i, "via": x, "via_R": R[x], "to": j, "R": [R[i], R[j]]})
    # independent switches: apply pit k's toggle vertex set, if it is a component, in each region state
    joint = Counter()
    toggle_sets = [frozenset(tg["toggle_moves"][0][1]) for tg in toggles if tg["toggle_moves"]]
    for i in region:
        for S in toggle_sets:
            for pr, K, x in s.info[i]["moves"]:
                if frozenset(K) == S and x != i:
                    where = "region-same-pit" if x in rset and pit_of[x] == pit_of[i] else \
                            "region-other-pit" if x in rset else "rim" if x in set(rim) else "elsewhere"
                    joint[where] += 1
    return {"root": r, "region": region, "strict_traps": trap_states, "twins": twin_states,
            "pits": pits, "toggles": toggles, "rim_size": len(rim),
            "connectors": {str(j): {"R": R[j], "pits": touch[j]} for j in connectors},
            "spurs": {str(j): {"R": R[j], "pit": touch[j][0]} for j in spurs},
            "stabiliser_order": len(stab), "trap_orbit": orbit(trap_states[0]) if trap_states else [],
            "twin_orbit": orbit(twin_states[0]) if twin_states else [],
            "trap_to_own_twin_by_symmetry": trap_twin_by_symmetry,
            "inter_pit_macros": inter, "toggle_sets_applied_in_region": dict(joint)}


def part2(traces):
    kills, rows, chis = [], [], set()
    for row in traces["rows"]:
        rot = parse_ascii(row["ascii"])
        r, B = row["root"], row["boundary_cyclic_order"]
        s = RootState(rot, r)
        assert s.V == row["vertex_order"]
        stab = [a for a in automorphisms(rot) if a[r] == r]
        for k, run in enumerate(row["runs"]):
            warned = sorted({tuple(w["coloring"]) for w in run["warnings"]})
            if not warned:
                continue
            chi = {}
            for c in warned:
                pats = frozenset(json.dumps(pattern(rot, r, s.V, B, act(s, a, c))) for a in stab)
                tau = s.descent(s.index[c], 2) is not None
                chi[c] = (pats, tau)
                chis.add((row["order"], row["graph_index"], r, pats, tau))
            for a_i in range(len(warned)):
                for b_i in range(a_i + 1, len(warned)):
                    c1, c2 = warned[a_i], warned[b_i]
                    if chi[c1] == chi[c2] and not any(act(s, a, c1) == c2 for a in stab):
                        kills.append({"order": row["order"], "graph_index": row["graph_index"], "root": r, "run": k,
                                      "colorings": [list(c1), list(c2)]})
            rows.append({"order": row["order"], "graph_index": row["graph_index"], "root": r, "run": k,
                         "warnings": len(warned), "distinct_chi": len(set(chi.values())),
                         "stabiliser_order": len(stab)})
    return {"runs_checked": len(rows), "c7d_kills": kills, "c7d_survives": not kills,
            "distinct_chi_values_observed": len(chis), "max_warnings_per_chi_in_a_run":
            max(r["warnings"] - r["distinct_chi"] + 1 for r in rows), "rows": rows}


def main():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    g = next(g for o in table["orders"] if o["order"] == 17 for g in o["graphs_checked"] if g["graph_index"] == 3)
    rot = parse_ascii(g["ascii"])
    p1 = {str(r): part1(rot, r) for r in (3, 13)}
    path = FIXTURES / "breadcrumb-warning-traces.json"
    p2 = part2(json.loads(path.read_text()))
    out = {"scope": "WP7d: fixture structure (order 17 graph 3, roots 3 and 13) and the C7d charging claim on the "
                    "39 warned runs. Finite evidence; no status claims.",
           "part1": p1, "part2": p2,
           "inputs": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (path, FIXTURES / "mass-macro-results.json")},
           "checkers": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (HERE / "wp7d_test.py", HERE / "WP7d-declaration.md", HERE / "mass_core.py")}}
    (HERE / "wp7d-results.json").write_text(json.dumps(out, indent=1, default=list) + "\n")
    for r, d in p1.items():
        print(f"root {r}: region {len(d['region'])} = {len(d['strict_traps'])} strict + {len(d['twins'])} twins; "
              f"pits {len(d['pits'])}; rim {d['rim_size']} = {len(d['connectors'])} connectors "
              f"(R {sorted({v['R'] for v in d['connectors'].values()})}) + {len(d['spurs'])} spurs "
              f"(R {sorted({v['R'] for v in d['spurs'].values()})}); |Stab| {d['stabiliser_order']}; "
              f"trap orbit {len(d['trap_orbit'])}, twin orbit {len(d['twin_orbit'])}; "
              f"trap->own twin by symmetry {d['trap_to_own_twin_by_symmetry']}; "
              f"inter-pit macros {len(d['inter_pit_macros'])}; toggle sets applied in region {d['toggle_sets_applied_in_region']}")
        for tg in d["toggles"]:
            print("   pit", tg["trap"], tg["twin"], "toggle", tg["toggle_moves"])
    print(f"C7d: {p2['runs_checked']} runs, kills {len(p2['c7d_kills'])}, distinct chi {p2['distinct_chi_values_observed']}, "
          f"max warnings sharing one chi in a run {p2['max_warnings_per_chi_in_a_run']}")


if __name__ == "__main__":
    main()
