"""Rescue-chain lengths after a shortest vacancy landing.

For each two-swap-stuck orbit at a published mass-failing root, take the
lexicographically shortest vacancy path that lands on a target (p = 0) or a
descending orbit at a passing root.  From that landing colouring, follow
R-lowering Kempe macros until p = 0.

Eager rule: among length-1 macros that lower R, the least successor colouring
index; if none exist, among length-2 macros that lower R, the lexicographically
least pair of successor indices (first move, second move).

Pessimistic rule: among length-1 and length-2 macros that lower R, the endpoint
of largest R.  Ties break by the least endpoint index, then the shorter macro,
then the lexicographically least successor pair.

A move whose successor is the source colouring is skipped: it does not change
the canonical colouring.  Does not colour the pentakis dodecahedron or the
order-42 geodesic, and does not read planning documents.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from inquiry_slide import colour_view
from mass_core import FIXTURES, RootState, canon, parse_ascii

OUT = Path(__file__).resolve().parent / "chain-length-data.json"


def lowering_steps(state: RootState, i: int):
    """Length-1 and length-2 macros from i that strictly lower R.

    Each length-1 item is (t,).  Each length-2 item is (t, u).
    Successor indices equal to the source are omitted.
    """
    start = state.info[i]["R"]
    ones = []
    seen_one = set()
    for _pair, _comp, t in state.info[i]["moves"]:
        if t == i or t in seen_one:
            continue
        if state.info[t]["R"] < start:
            seen_one.add(t)
            ones.append((t,))
    twos = []
    seen_two = set()
    for _pair, _comp, t in state.info[i]["moves"]:
        if t == i:
            continue
        for _pair2, _comp2, u in state.info[t]["moves"]:
            if u == t or (t, u) in seen_two:
                continue
            if state.info[u]["R"] < start:
                seen_two.add((t, u))
                twos.append((t, u))
    return ones, twos


def choose_eager(state: RootState, i: int):
    ones, twos = lowering_steps(state, i)
    if ones:
        return min(ones)
    if twos:
        return min(twos)
    return None


def choose_eager_positions(state: RootState, i: int):
    """Same preference order, but length 2 is the least move-list position pair."""
    start = state.info[i]["R"]
    best_t = None
    for _pair, _comp, t in state.info[i]["moves"]:
        if t == i:
            continue
        if state.info[t]["R"] < start and (best_t is None or t < best_t):
            best_t = t
    if best_t is not None:
        return (best_t,)
    best = None
    best_key = None
    for mi, (_pair, _comp, t) in enumerate(state.info[i]["moves"]):
        if t == i:
            continue
        for mj, (_pair2, _comp2, u) in enumerate(state.info[t]["moves"]):
            if u == t:
                continue
            if state.info[u]["R"] < start:
                key = (mi, mj)
                if best_key is None or key < best_key:
                    best_key = key
                    best = (t, u)
    return best


def choose_pessimistic(state: RootState, i: int):
    ones, twos = lowering_steps(state, i)
    best = None
    best_key = None
    for step in ones + twos:
        end = step[-1]
        # Max endpoint R, then least endpoint index, then shorter macro, then lex step.
        key = (-state.info[end]["R"], end, len(step), step)
        if best_key is None or key < best_key:
            best_key = key
            best = step
    return best


def follow(state: RootState, i: int, choose):
    """Walk macros until p = 0.  Endpoint R strictly falls, so endpoints cannot cycle."""
    info = state.info
    start_R = info[i]["R"]
    seen = {i}
    peak = start_R
    peak_end = start_R
    first_drop = None
    first_len = 0
    macros = 0
    revisited = False
    revisit_note = None
    trace = [{"i": i, "p": info[i]["p"], "q": info[i]["q"], "R": start_R}]
    blocked = False
    while info[i]["p"] != 0:
        step = choose(state, i)
        if step is None:
            blocked = True
            break
        for j in step[:-1]:
            peak = max(peak, info[j]["R"])
            if j in seen and not revisited:
                revisited = True
                revisit_note = {"at_macro": macros + 1, "index": j, "kind": "intermediate"}
            seen.add(j)
        end = step[-1]
        drop = info[i]["R"] - info[end]["R"]
        if drop <= 0:
            raise RuntimeError(f"macro did not lower R: {i} -> {step}")
        if first_drop is None:
            first_drop = drop
            first_len = len(step)
        if end in seen and not revisited:
            revisited = True
            revisit_note = {"at_macro": macros + 1, "index": end, "kind": "endpoint"}
        seen.add(end)
        peak = max(peak, info[end]["R"])
        peak_end = max(peak_end, info[end]["R"])
        macros += 1
        i = end
        trace.append({"i": i, "p": info[i]["p"], "q": info[i]["q"], "R": info[i]["R"]})
        if macros > start_R + 5:
            blocked = True
            revisit_note = revisit_note or {"at_macro": macros, "kind": "cap"}
            break
    if first_drop is None:
        first_drop = 0
    return {
        "macros": macros,
        "first_drop": first_drop,
        "first_len": first_len,
        "peak_R": peak,
        "peak_endpoint_R": peak_end,
        "revisited": revisited,
        "revisit": revisit_note,
        "reached": info[i]["p"] == 0 and not blocked,
        "blocked": blocked,
        "end_p": info[i]["p"],
        "end_q": info[i]["q"],
        "trace": trace,
    }


def orbit_kind(state: RootState, colouring):
    idx = state.index.get(colouring)
    if idx is None:
        return None
    if state.info[idx]["p"] == 0:
        return "target", idx
    if state.descent(idx, 2) is None:
        return "descends", idx
    return "stuck", idx


def vacancy_paths(rot, source: RootState, i: int, passing: set, get_state):
    """All vacancy paths of length 1 or 2 that land on a passing root's descending or target orbit."""
    col, _boundary, singletons, _gap, _d5, _locked = colour_view(rot, source, i)
    root = source.r
    found = []
    for x in singletons:
        new = dict(col)
        new[root] = col[x]
        if len(rot[x]) == 5 and x in passing:
            order_x = [v for v in range(len(rot)) if v != x]
            kind = orbit_kind(get_state(x), canon(tuple(new[v] for v in order_x)))
            if kind is not None and kind[0] in ("descends", "target"):
                found.append({"length": 1, "vertices": (x,), "landing": x, "kind": kind[0], "orbit": kind[1]})
        counts = {}
        for vertex in rot[x]:
            counts[new[vertex]] = counts.get(new[vertex], 0) + 1
        for y in rot[x]:
            if y == root or len(rot[y]) != 5 or y not in passing or counts[new[y]] != 1:
                continue
            new2 = dict(new)
            new2[x] = new[y]
            order_y = [v for v in range(len(rot)) if v != y]
            kind = orbit_kind(get_state(y), canon(tuple(new2[v] for v in order_y)))
            if kind is not None and kind[0] in ("descends", "target"):
                found.append({
                    "length": 2,
                    "vertices": (x, y),
                    "landing": y,
                    "kind": kind[0],
                    "orbit": kind[1],
                })
    return found


def summarise_chain(row):
    trace = row["trace"]
    qs = [step["q"] for step in trace]
    ps = [step["p"] for step in trace]
    drops = [qs[k] - qs[k + 1] for k in range(len(qs) - 1)]
    return {
        "macros": row["macros"],
        "first_drop": row["first_drop"],
        "first_len": row["first_len"],
        "peak_R": row["peak_R"],
        "peak_endpoint_R": row["peak_endpoint_R"],
        "revisited": row["revisited"],
        "revisit": row["revisit"],
        "reached": row["reached"],
        "blocked": row["blocked"],
        "end_p": row["end_p"],
        "end_q": row["end_q"],
        "p_trace": ps,
        "q_trace": qs,
        "q_drops": drops,
        "min_q_drop": min(drops) if drops else None,
        "macros_while_p1": sum(1 for p in ps[1:] if False) ,  # filled below
    }


def macros_before_p0(ps):
    """Number of macro endpoints still at p = 1.  The last endpoint should be p = 0."""
    return sum(1 for p in ps[1:] if p == 1)


def main():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    jobs = []
    for block in table["orders"]:
        for graph in block["graphs_checked"]:
            failing = graph["failing_roots"]
            if not failing:
                continue
            jobs.append({
                "order": block["order"],
                "graph": graph["graph_index"],
                "ascii": graph["ascii"],
                "failing": list(failing),
                "passing": set(graph["passing_roots"]),
            })

    records = []
    t_all = time.time()
    for job in jobs:
        rot = parse_ascii(job["ascii"])
        cache = {}

        def get_state(root, _rot=rot, _cache=cache, _job=job):
            if root not in _cache:
                t0 = time.time()
                _cache[root] = RootState(_rot, root)
                state = _cache[root]
                print(
                    f"state { _job['order'] }:{ _job['graph'] } root {root} "
                    f"orbits {len(state.C)} {time.time() - t0:.2f}s",
                    flush=True,
                )
            return _cache[root]

        for root in job["failing"]:
            state = get_state(root)
            stuck = [
                i for i, info in enumerate(state.info)
                if info["p"] == 1 and state.descent(i, 2) is not None
            ]
            print(
                f"failing {job['order']}:{job['graph']} root {root} stuck {len(stuck)}",
                flush=True,
            )
            for i in stuck:
                paths = vacancy_paths(rot, state, i, job["passing"], get_state)
                if not paths:
                    records.append({
                        "order": job["order"],
                        "graph": job["graph"],
                        "root": root,
                        "orbit": i,
                        "stuck_q": state.info[i]["q"],
                        "stuck_R": state.info[i]["R"],
                        "paths": [],
                    })
                    continue
                shortest = min(p["length"] for p in paths)
                short = sorted(
                    (p for p in paths if p["length"] == shortest),
                    key=lambda p: p["vertices"],
                )
                chosen = short[0]
                land_state = get_state(chosen["landing"])
                eager = follow(land_state, chosen["orbit"], choose_eager)
                pessimistic = follow(land_state, chosen["orbit"], choose_pessimistic)
                positions = follow(land_state, chosen["orbit"], choose_eager_positions)
                envelope = []
                seen_landings = set()
                for path in short:
                    key = (path["landing"], path["orbit"])
                    if key in seen_landings:
                        continue
                    seen_landings.add(key)
                    walked = follow(get_state(path["landing"]), path["orbit"], choose_eager)
                    envelope.append({
                        "vertices": list(path["vertices"]),
                        "landing": path["landing"],
                        "kind": path["kind"],
                        "orbit": path["orbit"],
                        "macros": walked["macros"],
                        "first_drop": walked["first_drop"],
                        "peak_R": walked["peak_R"],
                        "revisited": walked["revisited"],
                        "reached": walked["reached"],
                        "land_p": land_state.info[path["orbit"]]["p"] if path["landing"] == chosen["landing"] else get_state(path["landing"]).info[path["orbit"]]["p"],
                        "land_q": get_state(path["landing"]).info[path["orbit"]]["q"],
                        "land_R": get_state(path["landing"]).info[path["orbit"]]["R"],
                    })
                land_info = land_state.info[chosen["orbit"]]
                records.append({
                    "order": job["order"],
                    "graph": job["graph"],
                    "root": root,
                    "orbit": i,
                    "stuck_p": state.info[i]["p"],
                    "stuck_q": state.info[i]["q"],
                    "stuck_R": state.info[i]["R"],
                    "n_paths": len(paths),
                    "n_shortest": len(short),
                    "path": list(chosen["vertices"]),
                    "path_length": chosen["length"],
                    "landing": chosen["landing"],
                    "landing_kind": chosen["kind"],
                    "landing_orbit": chosen["orbit"],
                    "land_p": land_info["p"],
                    "land_q": land_info["q"],
                    "land_R": land_info["R"],
                    "scale": state.scale,
                    "eager": eager,
                    "pessimistic": pessimistic,
                    "eager_positions": {
                        "macros": positions["macros"],
                        "first_drop": positions["first_drop"],
                        "peak_R": positions["peak_R"],
                        "revisited": positions["revisited"],
                        "reached": positions["reached"],
                        "same_trace": [a["i"] for a in positions["trace"]] == [a["i"] for a in eager["trace"]],
                    },
                    "eager_envelope": envelope,
                })
                print(
                    f"  orbit {i} path {chosen['vertices']} -> {chosen['landing']} "
                    f"p {land_info['p']} q {land_info['q']} "
                    f"eager {eager['macros']} pess {pessimistic['macros']} "
                    f"rev {eager['revisited']}/{pessimistic['revisited']}",
                    flush=True,
                )

    print(f"total {time.time() - t_all:.1f}s records {len(records)}", flush=True)
    OUT.write_text(json.dumps(records, indent=1) + "\n")
    print(f"wrote {OUT}", flush=True)


if __name__ == "__main__":
    main()
