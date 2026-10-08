"""Compare two-step singleton slides with one-swap Kempe preparation.

Scope: the four locked mass-stuck orbits named by the inquiry
(order 17 graph 0 roots 4 and 6; order 20 graph 7 roots 7 and 11).
Does not colour the order-32 or order-42 symmetric graphs.
"""

import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from inquiry_slide import colour_view, slide_returns
from mass_core import FIXTURES, RootState, canon, parse_ascii

OUT = Path(__file__).resolve().parent / "kempe-vs-twostep-data.json"
TARGETS = ((17, 0, 4), (17, 0, 6), (20, 7, 7), (20, 7, 11))


def colour_dict(state, i):
    return dict(zip(state.V, state.C[i]))


def domain_ok(col, n, deleted):
    return set(col) == set(range(n)) - {deleted}


def monochrome(rot, col):
    bad = []
    for v in col:
        for w in rot[v]:
            if w in col and w > v and col[v] == col[w]:
                bad.append((v, w, col[v]))
    return bad


def as_canon(col, n, deleted):
    order = [v for v in range(n) if v != deleted]
    return canon(tuple(col[v] for v in order))


def slide(col, src, dst):
    """Move the vacancy from src to dst. col is defined on every vertex except src."""
    new = dict(col)
    new[src] = col[dst]
    del new[dst]
    return new


def boundary_report(rot, deleted, col):
    boundary = list(rot[deleted])
    cols = [col[v] for v in boundary]
    counts = {}
    for a in cols:
        counts[a] = counts.get(a, 0) + 1
    repeated = sorted(a for a, k in counts.items() if k >= 2)
    singles = [v for v in boundary if counts[col[v]] == 1]
    return {
        "boundary": boundary,
        "degrees": [len(rot[v]) for v in boundary],
        "colours": cols,
        "counts": {str(a): counts[a] for a in sorted(counts)},
        "repeated_colours": repeated,
        "singletons": singles,
        "degree_five_singletons": [v for v in singles if len(rot[v]) == 5],
    }


def proper_record(rot, col, deleted):
    n = len(rot)
    bad = monochrome(rot, col)
    return {
        "domain": domain_ok(col, n, deleted),
        "proper": domain_ok(col, n, deleted) and not bad,
        "monochrome_edges": bad,
        "palette": sorted(set(col.values())),
    }


def raw_diff(orig, new):
    return sorted(v for v in orig if v in new and orig[v] != new[v])


def align(orig, new):
    common = [v for v in orig if v in new]
    scored = []
    for perm in itertools.permutations(range(4)):
        changed = tuple(v for v in common if perm[orig[v]] != new[v])
        scored.append((len(common) - len(changed), changed, perm))
    best = max(item[0] for item in scored)
    opts = [item for item in scored if item[0] == best]
    changed_sets = sorted({item[1] for item in opts})
    return {
        "agree": best,
        "common": len(common),
        "full": best == len(common),
        "unique_changed_set": len(changed_sets) == 1,
        "changed_sets": [list(item) for item in changed_sets],
        "n_optimal_perms": len(opts),
    }


def load_graphs():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    found = {}
    for block in table["orders"]:
        for graph in block["graphs_checked"]:
            key = (block["order"], graph["graph_index"])
            if key in {(17, 0), (20, 7)}:
                found[key] = graph
    missing = {(17, 0), (20, 7)} - set(found)
    if missing:
        raise SystemExit(f"missing graphs {missing}")
    return found


def classify_state(state):
    rows = {}
    for i, colouring in enumerate(state.C):
        info = state.info[i]
        descends = state.descent(i, 2) is None
        descends_one = state.descent(i, 1) is None
        rows[colouring] = {
            "state": i,
            "p": info["p"],
            "q": info["q"],
            "R": info["R"],
            "descends": descends,
            "descends_in_one_swap": descends_one,
            "mass_stuck": info["p"] == 1 and not descends,
        }
    return rows


def landing_record(rot, col, deleted, proper, kind, via):
    n = len(rot)
    pattern = boundary_report(rot, deleted, col)
    return {
        "kind": kind,
        "via": via,
        "root": deleted,
        "degree": len(rot[deleted]),
        "canonical": list(as_canon(col, n, deleted)),
        "proper": proper,
        "boundary_colours": pattern["colours"],
        "boundary_degrees": pattern["degrees"],
        "boundary": pattern["boundary"],
        "p_colours_on_boundary": len(set(pattern["colours"])),
        "colouring": {str(v): col[v] for v in sorted(col)},
    }


def annotate(record, cache, passing, failing, original, order, index):
    root = record["root"]
    state, classes = cache[(order, index, root)]
    colouring = tuple(record["canonical"])
    if colouring not in classes:
        record["orbit"] = None
        record["missing_from_enumeration"] = True
        return
    info = classes[colouring]
    record["missing_from_enumeration"] = False
    record["orbit"] = {
        "root": root,
        "state": info["state"],
        "p": info["p"],
        "q": info["q"],
        "R": info["R"],
        "descends": info["descends"],
        "descends_in_one_swap": info["descends_in_one_swap"],
        "mass_stuck": info["mass_stuck"],
        "root_status": "passing" if root in passing else "failing" if root in failing else "unlisted",
    }
    pre = {int(v): c for v, c in record["colouring"].items()}
    record["raw_diff_from_source"] = raw_diff(original, pre)
    record["align_to_source"] = align(original, pre)
    # The orbit id is the canonical tuple; the explicit colour dict is audit-only.
    del record["colouring"]


def analyse(rot, state, classes, passing, failing):
    n = len(rot)
    reports = []
    for i, info in enumerate(state.info):
        if info["p"] != 1 or state.descent(i, 2) is None:
            continue
        col, boundary, singletons, gap, d5, locked = colour_view(rot, state, i)
        repeated = [a for a in set(col[v] for v in boundary) if sum(col[v] == a for v in boundary) >= 2]
        locked_exact = bool(d5) and all(
            sum(col[w] == col[v] for w in boundary) >= 2 for v in d5
        )
        if not (locked is True and locked_exact and len(singletons) == 3 and len(repeated) == 1):
            reports.append({
                "skipped": True,
                "state": i,
                "locked": locked,
                "singletons": singletons,
                "reason": "stuck but not a locked three-singleton orbit",
            })
            continue
        repeated_colour = repeated[0]
        source_proper = proper_record(rot, col, state.r)
        slides = []
        for x in singletons:
            stepped = slide(col, state.r, x)
            back, onward = slide_returns(rot, state.r, col, x)
            proper_mid = proper_record(rot, stepped, x)
            # Independent singleton recount on the intermediate link.
            mid = boundary_report(rot, x, stepped)
            expect_onward = [v for v in mid["degree_five_singletons"] if v != state.r]
            onward_matches = expect_onward == onward and (state.r in mid["degree_five_singletons"]) == back
            seconds = []
            targets = ([state.r] if back else []) + list(onward)
            for y in targets:
                if y not in mid["singletons"] or len(rot[y]) != 5:
                    seconds.append({"root": y, "error": "not a degree-five singleton"})
                    continue
                landed = slide(stepped, x, y)
                proper_land = proper_record(rot, landed, y)
                restores = y == state.r and as_canon(landed, n, y) == state.C[i]
                seconds.append({
                    "record": landing_record(
                        rot, landed, y, proper_land,
                        "return" if y == state.r else "forward", x,
                    ),
                    "restores_source": restores,
                    "raw_diff": raw_diff(col, landed),
                })
            slides.append({
                "intermediate": x,
                "degree": len(rot[x]),
                "colour": col[x],
                "proper": proper_mid,
                "slides_back": back,
                "other_degree_five": onward,
                "onward_matches_independent_recount": onward_matches,
                "intermediate_boundary": mid["boundary"],
                "intermediate_colours": mid["colours"],
                "intermediate_degrees": mid["degrees"],
                "seconds": seconds,
            })
        kempe = []
        seen_moves = set()
        for pair, comp, t in info["moves"]:
            if t == i:
                continue
            comp = tuple(comp)
            key = (pair, comp, t)
            if key in seen_moves:
                continue
            seen_moves.add(key)
            swapped = dict(col)
            a, b = pair
            outside = [v for v in comp if swapped.get(v) not in (a, b)]
            for v in comp:
                if swapped[v] == a:
                    swapped[v] = b
                elif swapped[v] == b:
                    swapped[v] = a
            proper_swap = proper_record(rot, swapped, state.r)
            canon_swap = as_canon(swapped, n, state.r)
            canon_ok = canon_swap == state.C[t]
            # Maximal connected component in the pair, checked independently.
            pending = {v for v in col if col[v] in (a, b)}
            maximal = True
            if not set(comp) <= pending:
                maximal = False
            else:
                stack = [comp[0]]
                reached = set()
                while stack:
                    v = stack.pop()
                    if v in reached:
                        continue
                    reached.add(v)
                    for w in rot[v]:
                        if w in pending and w not in reached:
                            stack.append(w)
                maximal = reached == set(comp) and all(
                    w not in pending or w in reached for v in comp for w in rot[v]
                )
            pattern = boundary_report(rot, state.r, colour_dict(state, t))
            d5_singles = pattern["degree_five_singletons"]
            if not d5_singles:
                continue
            prepared = []
            for s in d5_singles:
                # Slide the canonical representative and the explicit swap; both must agree.
                landed = slide(swapped, state.r, s)
                proper_land = proper_record(rot, landed, s)
                canon_land = as_canon(landed, n, s)
                canon_from_rep = as_canon(slide(colour_dict(state, t), state.r, s), n, s)
                prepared.append({
                    "along": s,
                    "degree": len(rot[s]),
                    "record": landing_record(
                        rot, landed, s, proper_land, "kempe-prepared", list(pair),
                    ),
                    "canonical_agrees_with_representative_slide": canon_land == canon_from_rep,
                    "raw_diff": raw_diff(col, landed),
                })
            neighbour = classes[state.C[t]]
            kempe.append({
                "pair": list(pair),
                "component": list(comp),
                "component_size": len(comp),
                "boundary_in_component": [v for v in boundary if v in set(comp)],
                "successor_state": t,
                "successor_canonical": list(state.C[t]),
                "successor_orbit": {
                    "p": neighbour["p"],
                    "q": neighbour["q"],
                    "R": neighbour["R"],
                    "descends": neighbour["descends"],
                    "mass_stuck": neighbour["mass_stuck"],
                },
                "swap_proper": proper_swap,
                "swap_canon_matches_mass_core": canon_ok,
                "component_is_maximal_bichromatic": maximal and not outside,
                "boundary_colours_after": pattern["colours"],
                "degree_five_singletons": d5_singles,
                "prepared_slides": prepared,
            })
        reports.append({
            "state": i,
            "canonical": list(state.C[i]),
            "p": info["p"],
            "q": info["q"],
            "R": info["R"],
            "gap": gap,
            "locked": locked_exact,
            "boundary": list(boundary),
            "boundary_degrees": [len(rot[v]) for v in boundary],
            "boundary_colours": [col[v] for v in boundary],
            "repeated_colour": repeated_colour,
            "repeated_vertices": [v for v in boundary if col[v] == repeated_colour],
            "degree_five_neighbours": list(d5),
            "singletons": list(singletons),
            "source_proper": source_proper,
            "slides": slides,
            "kempe": kempe,
            "_original": col,
        })
    return reports


def kempe_signature(entry, source_root):
    """Vertices recoloured by the swap, excluding the vacancy landing."""
    return sorted(set(entry["component"]) - {entry["along"]} - {source_root})


def compare(report):
    forward = []
    returns = []
    for step in report["slides"]:
        for second in step["seconds"]:
            if "record" not in second:
                continue
            bucket = returns if second["record"]["kind"] == "return" else forward
            bucket.append((step, second))
    prepared = []
    for move in report["kempe"]:
        for slide_row in move["prepared_slides"]:
            prepared.append((move, slide_row))
    one_each = []
    for move in report["kempe"]:
        if move["prepared_slides"]:
            chosen = min(move["prepared_slides"], key=lambda row: row["along"])
            one_each.append((move, chosen))

    def key_of(record):
        orbit = record.get("orbit") or {}
        return (record["root"], tuple(record["canonical"]), orbit.get("state"))

    set_forward = {key_of(second["record"]) for _, second in forward}
    set_return = {key_of(second["record"]) for _, second in returns}
    set_a = set_forward | set_return
    set_b = {key_of(row["record"]) for _, row in prepared}
    set_b_one = {key_of(row["record"]) for _, row in one_each}

    def rel(left, right):
        if not left or not right:
            return "empty"
        if left == right:
            return "same"
        if left & right:
            return "overlapping"
        return "disjoint"

    same_orbit_pairs = sum(
        key_of(second["record"]) == key_of(row["record"])
        for _, second in forward for _, row in prepared
    )
    return {
        "n_forward": len(forward),
        "n_return": len(returns),
        "n_prepared_all": len(prepared),
        "n_prepared_one_per_neighbour": len(one_each),
        "relation_forward_vs_all_prepared": rel(set_forward, set_b),
        "relation_all_seconds_vs_all_prepared": rel(set_a, set_b),
        "relation_forward_vs_one_per_neighbour": rel(set_forward, set_b_one),
        "intersection_forward_prepared": [
            {"root": k[0], "state": k[2], "canonical": list(k[1])}
            for k in sorted(set_forward & set_b, key=lambda item: (item[0], -1 if item[2] is None else item[2]))
        ],
        "forward_roots": sorted({k[0] for k in set_forward}),
        "prepared_roots": sorted({k[0] for k in set_b}),
        "shared_landing_roots": sorted({k[0] for k in set_forward} & {k[0] for k in set_b}),
        "any_prepared_mass_stuck": any(
            (row["record"].get("orbit") or {}).get("mass_stuck") for _, row in prepared
        ),
        "any_prepared_descent_blocked": any(
            not (row["record"].get("orbit") or {}).get("descends", False) for _, row in prepared
        ),
        "every_prepared_descends": bool(prepared) and all(
            (row["record"].get("orbit") or {}).get("descends") for _, row in prepared
        ),
        "every_one_per_neighbour_descends": bool(one_each) and all(
            (row["record"].get("orbit") or {}).get("descends") for _, row in one_each
        ),
        "any_forward_descends": any(
            (second["record"].get("orbit") or {}).get("descends") for _, second in forward
        ),
        "any_forward_mass_stuck": any(
            (second["record"].get("orbit") or {}).get("mass_stuck") for _, second in forward
        ),
        "pair_same_orbit_count": same_orbit_pairs,
    }


def colour_relations(report):
    """Align pre-canonical colourings. Recomputed from stored raw diffs plus source."""
    # Colour dicts are gone; this pass is done before deletion in main.
    return report.get("colour_relations", [])


def finish_relations(original, slides, kempe):
    relations = []
    for step in slides:
        for second in step["seconds"]:
            if "record" not in second or second["record"]["kind"] == "return":
                continue
            for move in kempe:
                for row in move["prepared_slides"]:
                    left = second["_pre"]
                    right = row["_pre"]
                    aligned = align(left, right)
                    relations.append({
                        "via": step["intermediate"],
                        "two_step_root": second["record"]["root"],
                        "two_step_state": (second["record"].get("orbit") or {}).get("state"),
                        "kempe_component": move["component"],
                        "kempe_pair": move["pair"],
                        "along": row["along"],
                        "kempe_root": row["record"]["root"],
                        "kempe_state": (row["record"].get("orbit") or {}).get("state"),
                        "same_canonical_orbit": (
                            second["record"]["root"] == row["record"]["root"]
                            and second["record"]["canonical"] == row["record"]["canonical"]
                        ),
                        "align": aligned,
                        "raw_diff_same_names": raw_diff(left, right),
                    })
    full = [row for row in relations if row["align"]["full"]]
    best = max((row["align"]["agree"] / row["align"]["common"]) for row in relations) if relations else None
    changed_a = []
    for step in slides:
        for second in step["seconds"]:
            if "record" not in second or second["record"]["kind"] == "return":
                continue
            changed_a.append({
                "via": step["intermediate"],
                "root": second["record"]["root"],
                "raw_diff_from_source": second["raw_diff"],
                "expected_diff": [step["intermediate"]] if second["record"]["root"] != step["intermediate"] else [],
            })
    changed_b = []
    for move in kempe:
        for row in move["prepared_slides"]:
            expected = sorted(set(move["component"]) - {row["along"]})
            changed_b.append({
                "along": row["along"],
                "successor_state": move["successor_state"],
                "raw_diff_from_source": row["raw_diff"],
                "expected_component_without_landing": expected,
                "diff_equals_component_without_landing": row["raw_diff"] == expected,
            })
    return {
        "n_pairs": len(relations),
        "n_full_colour_agreement": len(full),
        "best_agreement_ratio": best,
        "full_pairs": [
            {
                "via": row["via"],
                "two_step_root": row["two_step_root"],
                "two_step_state": row["two_step_state"],
                "along": row["along"],
                "kempe_root": row["kempe_root"],
                "kempe_state": row["kempe_state"],
            }
            for row in full
        ],
        "closest_pairs": sorted(relations, key=lambda row: (-row["align"]["agree"], row["align"]["common"]))[:8],
        "two_step_diffs": changed_a,
        "kempe_diffs": changed_b,
        "source_domain": sorted(original),
    }


def build_root(cache, order, index, rot, root):
    key = (order, index, root)
    if key not in cache:
        t0 = time.time()
        state = RootState(rot, root)
        state.check_closure()
        cache[key] = (state, classify_state(state))
        print(f"built {order}:{index} root {root} orbits {len(state.C)} in {time.time() - t0:.2f}s", flush=True)
    return cache[key]


def main():
    graphs = load_graphs()
    cache = {}
    payload = {"targets": []}
    for order, index, root in TARGETS:
        graph = graphs[(order, index)]
        rot = parse_ascii(graph["ascii"])
        passing = set(graph["passing_roots"])
        failing = set(graph["failing_roots"])
        state, classes = build_root(cache, order, index, rot, root)
        reports = analyse(rot, state, classes, passing, failing)
        needed = set()
        for report in reports:
            if report.get("skipped"):
                continue
            for step in report["slides"]:
                for second in step["seconds"]:
                    if "record" in second:
                        needed.add(second["record"]["root"])
            for move in report["kempe"]:
                for row in move["prepared_slides"]:
                    needed.add(row["record"]["root"])
        for landing_root in sorted(needed):
            build_root(cache, order, index, rot, landing_root)
        cleaned = []
        for report in reports:
            if report.get("skipped"):
                cleaned.append(report)
                continue
            original = report.pop("_original")
            for step in report["slides"]:
                for second in step["seconds"]:
                    if "record" not in second:
                        continue
                    # Keep the pre-canon dict until relations are computed.
                    second["_pre"] = {int(v): c for v, c in second["record"]["colouring"].items()}
                    annotate(second["record"], cache, passing, failing, original, order, index)
            for move in report["kempe"]:
                for row in move["prepared_slides"]:
                    row["_pre"] = {int(v): c for v, c in row["record"]["colouring"].items()}
                    annotate(row["record"], cache, passing, failing, original, order, index)
            report["colour_relations"] = finish_relations(original, report["slides"], report["kempe"])
            for step in report["slides"]:
                for second in step["seconds"]:
                    second.pop("_pre", None)
            for move in report["kempe"]:
                for row in move["prepared_slides"]:
                    row.pop("_pre", None)
            report["comparison"] = compare(report)
            cleaned.append(report)
        payload["targets"].append({
            "order": order,
            "graph": index,
            "root": root,
            "ascii_sha256": graph["ascii_sha256"],
            "passing_roots": sorted(passing),
            "failing_roots": sorted(failing),
            "orbits": len(state.C),
            "locked_stuck": cleaned,
        })
        print(f"done {order}:{index} root {root} locked_stuck {len(cleaned)}", flush=True)
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(f"wrote {OUT}", flush=True)


if __name__ == "__main__":
    main()
