"""Breadcrumb (two-wave) descent: exploratory run at the published mass-macro failing roots.

Idea from the user (4 October): a first wave descends and, at a dead end, leaves a warning one
link back, like slime-mould trails; a second, bounded wave escapes only when no warned-free
descent remains.  This script is EXPLORATORY: the wave-2 depth of three was informed by the
observed escape depths, so this run is not a holdout test.  The precise candidate is stated
in SolvingFrameworkPlan/messages/; validation belongs to the corpus team.

Policy, per root, per run (warnings W start empty and are discarded after the run):
  at colouring c with p(c) = 1:
    wave 1: among states reachable by <= 2 single-component swaps with R < R(c) and not in W,
            move to the one with least (R, index);
    if none: add c to W; if c has a predecessor in this run, step back one link;
    otherwise (c is the start or the stack is empty) wave 2: among states reachable by
            <= 3 swaps with R < R(c) and not in W, move to the least, and restart the stack there;
    if wave 2 also finds nothing, the run fails (that would be a kill witness).
Reported per root: every non-target start, success, warnings placed, wave-2 uses, steps.
"""
import hashlib
import json

from mass_core import FIXTURES, HERE, RootState, parse_ascii

WAVE2_DEPTH = 3
MAX_STEPS = 10_000


def run(state, nxt, R, start):
    warned, stack, steps, wave2 = set(), [start], 0, 0
    while steps < MAX_STEPS:
        c = stack[-1]
        steps += 1
        if state.info[c]["p"] == 0:
            return {"ok": True, "warnings": len(warned), "wave2": wave2, "steps": steps}
        cands = sorted({(R[j], j) for x in nxt[c] for j in [x] + nxt[x] if R[j] < R[c] and j not in warned})
        if cands:
            stack.append(cands[0][1])
            continue
        warned.add(c)
        if len(stack) > 1:
            stack.pop()
            continue
        seen, level, found = {c}, [c], None
        for _ in range(WAVE2_DEPTH):
            level = [y for x in level for y in nxt[x] if not (y in seen or seen.add(y))]
            ok = sorted((R[j], j) for j in level if R[j] < R[c] and j not in warned)
            if ok:
                found = ok[0][1]
                break
        if found is None:
            return {"ok": False, "warnings": len(warned), "wave2": wave2, "steps": steps, "stuck_at": c}
        wave2 += 1
        stack = [found]
    return {"ok": False, "warnings": len(warned), "wave2": wave2, "steps": steps, "reason": "step cap"}


def main():
    path = FIXTURES / "mass-macro-results.json"
    table = json.loads(path.read_text())
    rows = []
    for o in table["orders"]:
        for g in o["graphs_checked"]:
            if not g["failing_roots"]:
                continue
            rot = parse_ascii(g["ascii"])
            for r in g["failing_roots"]:
                s = RootState(rot, r)
                nxt = [[x for _, _, x in s.info[i]["moves"]] for i in range(len(s.C))]
                R = [s.info[i]["R"] for i in range(len(s.C))]
                res = [run(s, nxt, R, i) for i in range(len(s.C)) if s.info[i]["p"] == 1]
                row = {"order": o["order"], "graph_index": g["graph_index"], "root": r, "starts": len(res),
                       "all_reach_target": all(x["ok"] for x in res),
                       "max_warnings": max(x["warnings"] for x in res),
                       "runs_using_wave2": sum(x["wave2"] > 0 for x in res),
                       "max_steps": max(x["steps"] for x in res),
                       "failures": [x for x in res if not x["ok"]]}
                rows.append(row)
                print(f"order {row['order']} graph {row['graph_index']} root {r}: starts {row['starts']}, "
                      f"all reach target {row['all_reach_target']}, max warnings {row['max_warnings']}, "
                      f"wave-2 runs {row['runs_using_wave2']}, max steps {row['max_steps']}")
    out = {"scope": "Exploratory run of breadcrumb two-wave descent at the 12 published failing roots only. "
                    "Wave-2 depth 3 was informed by observed escape depths; not a holdout test; no status claims.",
           "wave2_depth": WAVE2_DEPTH,
           "inputs": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()},
           "checkers": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (HERE / "breadcrumb_descent.py", HERE / "mass_core.py")},
           "rows": rows}
    (HERE / "breadcrumb-descent.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
