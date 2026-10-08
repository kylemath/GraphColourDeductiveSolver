"""Score rank candidates on the 21 two-swap-stuck mass orbits.

The test set is the published failing roots in mass-macro-results.json.
A state is stuck when RootState.descent(i, 2) is not None.  Ranks are
functions of the current hole, the colouring, degrees, boundary colour
multiplicities, q, component sizes, and the sorted colour population.
They do not read a pass/fail label, a distance to a passing root, or a
mass-macro outcome.

Moves scored from each stuck orbit, and only those moves:
  one Kempe swap of one bichromatic component in the current deletion;
  one singleton slide (unique boundary colour);
  one slide of length 2 whose intermediate vertex is not degree 5
  and whose landing is a degree-5 singleton of that intermediate.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from inquiry_slide import colour_view
from mass_core import FIXTURES, PAIRS, RootState, canon, parse_ascii

HERE = Path(__file__).resolve().parent
OUT = HERE / "rank-kill-data.json"

# No singleton-slide landing: larger than every degree, so it is not a descent.
NO_SINGLETON = 10**6


def compute_features(rot, deleted: int, col: dict[int, int]) -> dict:
    """Legal features of one hole.  q matches RootState._analyse."""
    n = len(rot)
    vertices = [v for v in range(n) if v != deleted]
    adj = {v: [w for w in rot[v] if w != deleted] for v in vertices}
    boundary = list(rot[deleted])
    boundary_set = set(boundary)
    boundary_colours = [col[v] for v in boundary]
    distinct = len(set(boundary_colours))
    multiplicity: dict[int, int] = {}
    for colour in boundary_colours:
        multiplicity[colour] = multiplicity.get(colour, 0) + 1
    singletons = [v for v in boundary if multiplicity[col[v]] == 1]
    singleton_degrees = [len(rot[v]) for v in singletons]
    counts = [0, 0, 0, 0]
    for v in vertices:
        colour = col[v]
        if not 0 <= colour <= 3:
            raise AssertionError(f"colour {colour} at vertex {v}")
        counts[colour] += 1
    q = 0
    lin = 0
    short_links = 0
    exterior: list[int] = []
    for a, b in PAIRS:
        pending = {v for v in vertices if col[v] in (a, b)}
        while pending:
            seed = min(pending)
            pending.remove(seed)
            comp = {seed}
            stack = [seed]
            while stack:
                i = stack.pop()
                for j in adj[i]:
                    if j in pending:
                        pending.remove(j)
                        comp.add(j)
                        stack.append(j)
            if comp & boundary_set:
                ext = len(comp - boundary_set)
                q += ext * ext
                lin += ext
                exterior.append(ext)
                if ext == 0 and len(comp) >= 2:
                    short_links += 1
    return {
        "q": q,
        "lin": lin,
        "p": max(0, distinct - 3),
        "n_boundary_colours": distinct,
        "fill": distinct <= 3,
        "counts": counts,
        "population_asc": tuple(sorted(counts)),
        "population_desc": tuple(sorted(counts, reverse=True)),
        "min_singleton_degree": min(singleton_degrees) if singleton_degrees else None,
        "singleton_degrees": tuple(sorted(singleton_degrees)),
        "exterior": tuple(sorted(exterior, reverse=True)),
        "max_exterior": max(exterior) if exterior else 0,
        "short_links": short_links,
        "hole_degree": len(boundary),
    }


def pad_profile(exterior: tuple[int, ...], width: int) -> tuple[int, ...]:
    values = list(exterior[:width])
    values.extend([0] * (width - len(values)))
    return tuple(values)


def rank_values(feat: dict, width: int) -> dict[str, tuple]:
    """Totally ordered keys.  A strict descent is Python tuple order."""
    pop_asc = feat["population_asc"]
    pop_desc = feat["population_desc"]
    profile = pad_profile(feat["exterior"], width)
    zeros = tuple(0 for _ in range(width))
    min_deg = feat["min_singleton_degree"]
    min_key = NO_SINGLETON if min_deg is None else min_deg
    filled_asc = (0, pop_asc) if feat["fill"] else (1, pop_asc)
    filled_desc = (0, pop_desc) if feat["fill"] else (1, pop_desc)
    filled_profile = (0, zeros) if feat["fill"] else (1, profile)
    return {
        "q": (feat["q"],),
        "population": filled_asc,
        "population_desc": filled_desc,
        "boundary_q": (feat["n_boundary_colours"], feat["q"]),
        "mindeg_q": (min_key, feat["q"]),
        "exterior_profile": filled_profile,
        "short_q": (feat["short_links"], feat["q"]),
    }


CANDIDATES = ("q", "population", "boundary_q", "mindeg_q", "exterior_profile")
SCORED = CANDIDATES + ("population_desc", "short_q")


def move_name(kind: str, data: dict) -> str:
    if kind == "kempe":
        pair = "{" + ", ".join(str(x) for x in data["pair"]) + "}"
        comp = "{" + ", ".join(str(x) for x in data["component"]) + "}"
        return f"Kempe swap colours {pair} on {comp}"
    if kind == "slide1":
        return f"singleton slide to {data['to']} (degree {data['degree']})"
    via = data["via"]
    return (
        f"length-2 slide through {via} (degree {data['via_degree']}) "
        f"to {data['to']} (degree {data['to_degree']})"
    )


def apply_slide(col: dict[int, int], deleted: int, landing: int) -> dict[int, int]:
    new = dict(col)
    new[deleted] = col[landing]
    del new[landing]
    return new


def proper_on_deletion(rot, deleted: int, col: dict[int, int]) -> bool:
    for v, ns in enumerate(rot):
        if v == deleted:
            continue
        for w in ns:
            if w == deleted or w < v:
                continue
            if col[v] == col[w]:
                return False
    return True


def iter_moves(rot, state: RootState, i: int):
    """Legal scored moves.  Each yields kind, data, features, population tuple."""
    col, _boundary, singletons, _gap, _d5, _locked = colour_view(rot, state, i)
    seen = set()
    for pair, comp, t in state.info[i]["moves"]:
        key = (pair, comp, t)
        if key in seen or t == i:
            continue
        seen.add(key)
        colouring = dict(zip(state.V, state.C[t]))
        feat = compute_features(rot, state.r, colouring)
        info = state.info[t]
        if feat["q"] != info["q"] or feat["p"] != info["p"]:
            raise AssertionError(f"feature mismatch at root {state.r} orbit {t}")
        data = {
            "pair": list(pair),
            "component": list(comp),
            "orbit": t,
            "same_hole": True,
        }
        yield "kempe", data, feat
    for x in singletons:
        new = apply_slide(col, state.r, x)
        if not proper_on_deletion(rot, x, new):
            raise AssertionError(f"improper slide {state.r} -> {x}")
        if tuple(sorted(new[v] for v in new)) != tuple(sorted(col[v] for v in col)):
            # Sorted colour population is a multiset.  A pure slide preserves it.
            raise AssertionError("singleton slide changed the colour multiset")
        feat = compute_features(rot, x, new)
        yield "slide1", {"to": x, "degree": len(rot[x]), "same_hole": False}, feat
        if len(rot[x]) == 5:
            continue
        counts: dict[int, int] = {}
        for vertex in rot[x]:
            counts[new[vertex]] = counts.get(new[vertex], 0) + 1
        for y in rot[x]:
            if len(rot[y]) != 5 or counts[new[y]] != 1:
                continue
            new2 = apply_slide(new, x, y)
            if not proper_on_deletion(rot, y, new2):
                raise AssertionError(f"improper length-2 slide {state.r} -> {x} -> {y}")
            if tuple(sorted(new2.values())) != tuple(sorted(col.values())):
                raise AssertionError("length-2 slide changed the colour multiset")
            feat2 = compute_features(rot, y, new2)
            cancels = y == state.r and canon(tuple(new2[v] for v in state.V)) == state.C[i]
            yield "slide2", {
                "via": x,
                "via_degree": len(rot[x]),
                "to": y,
                "to_degree": len(rot[y]),
                "cancels": cancels,
                "same_hole": False,
                "coloring": list(canon(tuple(new2[v] for v in [v for v in range(len(rot)) if v != y]))),
            }, feat2


def json_rank(value: tuple):
    return [list(part) if isinstance(part, tuple) else part for part in value]


def describe_move(kind: str, data: dict, feat: dict, ranks: dict[str, tuple]) -> dict:
    row = {
        "kind": kind,
        "move": move_name(kind, data),
        "q": feat["q"],
        "n_boundary_colours": feat["n_boundary_colours"],
        "fill": feat["fill"],
        "population_asc": list(feat["population_asc"]),
        "min_singleton_degree": feat["min_singleton_degree"],
        "exterior": list(feat["exterior"]),
        "short_links": feat["short_links"],
        "hole_degree": feat["hole_degree"],
        "ranks": {name: json_rank(ranks[name]) for name in SCORED},
    }
    row.update({k: data[k] for k in data if k != "component"})
    if kind == "kempe":
        row["component"] = data["component"]
        row["pair"] = data["pair"]
    return row


def as_tuple(value):
    if isinstance(value, list):
        return tuple(as_tuple(part) for part in value)
    return value


def best_drop(start: dict[str, tuple], rows: list[dict], names: tuple[str, ...]) -> dict[str, dict]:
    out = {}
    for name in names:
        drops = []
        for row in rows:
            new = as_tuple(row["ranks"][name])
            if new < start[name]:
                drops.append((new, row["move"], row["kind"]))
        drops.sort()
        nearest = min(
            (as_tuple(row["ranks"][name]), row["move"], row["kind"]) for row in rows
        )
        out[name] = {
            "drops": len(drops),
            "move": drops[0][1] if drops else None,
            "kind": drops[0][2] if drops else None,
            "rank": json_rank(drops[0][0]) if drops else None,
            "nearest_move": nearest[1],
            "nearest_kind": nearest[2],
            "nearest_rank": json_rank(nearest[0]),
            "nearest_drops": nearest[0] < start[name],
        }
    return out


def load_jobs():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    jobs = []
    for block in table["orders"]:
        for graph in block["graphs_checked"]:
            failing = graph["failing_roots"]
            if not failing:
                continue
            published = {}
            for root_row in graph["roots"]:
                if root_row["root"] in failing:
                    published[root_row["root"]] = {
                        "two_swap_stuck_orbits": root_row["two_swap_stuck_orbits"],
                        "witness": tuple(root_row["failure_witness"]["coloring"]),
                    }
            jobs.append({
                "order": block["order"],
                "graph": graph["graph_index"],
                "ascii": graph["ascii"],
                "sha256": graph["ascii_sha256"],
                "failing": list(failing),
                "published": published,
            })
    return jobs


def main():
    jobs = load_jobs()
    orbits = []
    exchange = {"forward": None, "back": None}
    for job in jobs:
        rot = parse_ascii(job["ascii"])
        width = len(rot)
        states = {root: RootState(rot, root) for root in job["failing"]}
        for root, state in states.items():
            stuck = [
                i for i, info in enumerate(state.info)
                if info["p"] == 1 and state.descent(i, 2) is not None
            ]
            expect = job["published"][root]["two_swap_stuck_orbits"]
            if len(stuck) != expect:
                raise AssertionError(
                    f"{job['order']}:{job['graph']} root {root} stuck {len(stuck)} != {expect}"
                )
            witness = job["published"][root]["witness"]
            if witness not in state.index or state.index[witness] not in stuck:
                raise AssertionError(
                    f"published witness at {job['order']}:{job['graph']} root {root} is not stuck"
                )
            print(
                f"{job['order']}:{job['graph']} root {root} stuck {len(stuck)} "
                f"orbits {len(state.C)}",
                flush=True,
            )
            for i in stuck:
                info = state.info[i]
                col = dict(zip(state.V, state.C[i]))
                start_feat = compute_features(rot, root, col)
                if start_feat["q"] != info["q"] or start_feat["p"] != info["p"]:
                    raise AssertionError(f"start feature mismatch {root}:{i}")
                start_ranks = rank_values(start_feat, width)
                # One Kempe from a two-swap-stuck state cannot lower q or reach a fill.
                for _pair, _comp, t in info["moves"]:
                    if state.info[t]["p"] == 0 or state.info[t]["q"] < info["q"]:
                        raise AssertionError(f"stuck state {root}:{i} has a one-swap mass drop")
                rows = []
                population_unchanged_on_slides = True
                for kind, data, feat in iter_moves(rot, state, i):
                    if kind != "kempe" and feat["population_asc"] != start_feat["population_asc"]:
                        population_unchanged_on_slides = False
                    ranks = rank_values(feat, width)
                    row = describe_move(kind, data, feat, ranks)
                    rows.append(row)
                    if (
                        job["order"] == 17 and job["graph"] == 0 and root == 9
                        and kind == "slide1" and data["to"] == 14
                    ):
                        exchange["forward"] = {
                            "from": "9:stuck",
                            "move": row["move"],
                            "q": feat["q"],
                            "ranks": row["ranks"],
                            "coloring_matches_root14_stuck": False,
                        }
                    if (
                        job["order"] == 17 and job["graph"] == 0 and root == 14
                        and kind == "slide1" and data["to"] == 9
                    ):
                        exchange["back"] = {
                            "from": "14:stuck",
                            "move": row["move"],
                            "q": feat["q"],
                            "ranks": row["ranks"],
                        }
                orbits.append({
                    "order": job["order"],
                    "graph": job["graph"],
                    "sha256": job["sha256"],
                    "root": root,
                    "orbit": i,
                    "published_witness": list(state.C[i]) == list(witness),
                    "vertex_order": list(state.V),
                    "coloring": list(state.C[i]),
                    "boundary": list(rot[root]),
                    "p": info["p"],
                    "q": info["q"],
                    "R": info["R"],
                    "start": {
                        "n_boundary_colours": start_feat["n_boundary_colours"],
                        "population_asc": list(start_feat["population_asc"]),
                        "population_desc": list(start_feat["population_desc"]),
                        "min_singleton_degree": start_feat["min_singleton_degree"],
                        "singleton_degrees": list(start_feat["singleton_degrees"]),
                        "exterior": list(start_feat["exterior"]),
                        "lin": start_feat["lin"],
                        "short_links": start_feat["short_links"],
                        "ranks": {name: json_rank(start_ranks[name]) for name in SCORED},
                    },
                    "n_moves": len(rows),
                    "n_kempe": sum(1 for row in rows if row["kind"] == "kempe"),
                    "n_slide1": sum(1 for row in rows if row["kind"] == "slide1"),
                    "n_slide2": sum(1 for row in rows if row["kind"] == "slide2"),
                    "population_unchanged_on_slides": population_unchanged_on_slides,
                    "slides_that_fill": [
                        row["move"] for row in rows
                        if row["kind"] != "kempe" and row["fill"]
                    ],
                    "drops": best_drop(start_ranks, rows, SCORED),
                    "moves": rows,
                })

    if len(orbits) != 21:
        raise AssertionError(f"expected 21 stuck orbits, found {len(orbits)}")

    # Tie the 9 -> 14 slide to the stuck orbit at root 14, and the return.
    by_key = {(o["order"], o["graph"], o["root"], o["orbit"]): o for o in orbits}
    root9 = [o for o in orbits if o["order"] == 17 and o["graph"] == 0 and o["root"] == 9]
    root14 = [o for o in orbits if o["order"] == 17 and o["graph"] == 0 and o["root"] == 14]
    if len(root9) != 1 or len(root14) != 1:
        raise AssertionError("order 17 graph 0 roots 9 and 14 are not unique stuck orbits")
    a, b = root9[0], root14[0]
    forward_row = next(
        row for row in a["moves"]
        if row["kind"] == "slide1" and row.get("to") == 14
    )
    back_row = next(
        row for row in b["moves"]
        if row["kind"] == "slide1" and row.get("to") == 9
    )
    state14_colourings = {
        tuple(o["coloring"]) for o in orbits
        if o["order"] == 17 and o["graph"] == 0 and o["root"] == 14
    }
    # Recompute the landing colouring canon from the stored move by replaying is
    # already checked below against the stuck colouring via a fresh slide.
    exchange["pair"] = {
        "root9_orbit": a["orbit"],
        "root14_orbit": b["orbit"],
        "root9_q": a["q"],
        "root14_q": b["q"],
        "root9_ranks": a["start"]["ranks"],
        "root14_ranks": b["start"]["ranks"],
        "forward_move": forward_row["move"],
        "back_move": back_row["move"],
        "forward_ranks": forward_row["ranks"],
        "back_ranks": back_row["ranks"],
        "ranks_equal": a["start"]["ranks"] == b["start"]["ranks"],
        "forward_matches_root14_start": forward_row["ranks"] == b["start"]["ranks"],
        "back_matches_root9_start": back_row["ranks"] == a["start"]["ranks"],
    }
    del state14_colourings, by_key

    # Replay the exchange colourings explicitly.
    job0 = next(job for job in jobs if job["order"] == 17 and job["graph"] == 0)
    rot0 = parse_ascii(job0["ascii"])
    s9 = RootState(rot0, 9)
    s14 = RootState(rot0, 14)
    col9 = dict(zip(s9.V, s9.C[a["orbit"]]))
    slid = apply_slide(col9, 9, 14)
    landed = canon(tuple(slid[v] for v in s14.V))
    col14 = dict(zip(s14.V, s14.C[b["orbit"]]))
    slid_back = apply_slide(col14, 14, 9)
    landed_back = canon(tuple(slid_back[v] for v in s9.V))
    exchange["colouring_exchange"] = {
        "9_to_14_is_stuck_orbit": landed == s14.C[b["orbit"]],
        "14_to_9_is_stuck_orbit": landed_back == s9.C[a["orbit"]],
        "landed_q": s14.info[s14.index[landed]]["q"] if landed in s14.index else None,
        "landed_orbit": s14.index.get(landed),
        "return_orbit": s9.index.get(landed_back),
    }
    if not exchange["colouring_exchange"]["9_to_14_is_stuck_orbit"]:
        raise AssertionError("slide 9 -> 14 did not land on the stuck orbit at 14")
    if not exchange["colouring_exchange"]["14_to_9_is_stuck_orbit"]:
        raise AssertionError("slide 14 -> 9 did not land on the stuck orbit at 9")

    verdicts = {}
    for name in SCORED:
        missing = [
            f"{o['order']}:{o['graph']} root {o['root']} orbit {o['orbit']}"
            for o in orbits if o["drops"][name]["drops"] == 0
        ]
        equal_on_exchange = a["start"]["ranks"][name] == b["start"]["ranks"][name]
        forward_drops = forward_row["ranks"][name] < a["start"]["ranks"][name]
        back_drops = back_row["ranks"][name] < b["start"]["ranks"][name]
        # JSON ranks are lists; compare the already-computed tuple keys instead.
        cycles = equal_on_exchange and not forward_drops and not back_drops
        verdicts[name] = {
            "orbits_without_drop": missing,
            "n_without_drop": len(missing),
            "equal_on_9_14": equal_on_exchange,
            "exchange_is_flat_2_cycle": cycles,
            "drops_on_all_21": len(missing) == 0,
        }
        print(
            f"{name}: no-drop {len(missing)} "
            f"flat_exchange {cycles} "
            f"all {len(missing) == 0}",
            flush=True,
        )

    # Population does not move on a pure slide.  Record the fill events separately.
    slide_fill_orbits = [
        {
            "id": f"{o['order']}:{o['graph']} root {o['root']} orbit {o['orbit']}",
            "fills": o["slides_that_fill"],
        }
        for o in orbits if o["slides_that_fill"]
    ]
    payload = {
        "stuck_orbits": len(orbits),
        "population_unchanged_on_every_slide": all(
            o["population_unchanged_on_slides"] for o in orbits
        ),
        "slide_fills": slide_fill_orbits,
        "exchange": exchange,
        "verdicts": verdicts,
        "orbits": [
            {k: v for k, v in o.items() if k != "moves"} | {
                "decreasing": {
                    name: o["drops"][name] for name in SCORED
                },
                "slides": [row for row in o["moves"] if row["kind"] != "kempe"],
            }
            for o in orbits
        ],
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(f"wrote {OUT}", flush=True)


if __name__ == "__main__":
    main()
