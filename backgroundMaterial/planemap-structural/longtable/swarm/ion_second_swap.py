"""Second Kempe swap of every ion created by a neutral swap.

Scope: order 17, graph 3, root 3 colouring 44, and the sibling stuck
colourings at roots 3 and 13 when their first-swap patterns agree.
Also reconfirms the locked traps at order 17, graph 0, root 4 state 25
and root 6 state 27.  Uses mass_core.RootState only.  Does not edit
planning.json.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from inquiry_slide import colour_view
from mass_core import FIXTURES, PAIRS, RootState, parse_ascii

HERE = Path(__file__).resolve().parent
OUT = HERE / "ion-second-swap-data.json"

ROOT3 = (44, 47, 77, 91, 93)
ROOT13 = (19, 29, 52, 76, 96)


def load_ascii(order: int, graph: int) -> str:
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    for block in table["orders"]:
        if block["order"] != order:
            continue
        for item in block["graphs_checked"]:
            if item["graph_index"] == graph:
                return item["ascii"]
    raise SystemExit(f"missing graph {order}:{graph}")


def population(colouring: tuple[int, ...]) -> tuple[int, int, int, int]:
    counts = [0, 0, 0, 0]
    for colour in colouring:
        counts[colour] += 1
    return tuple(sorted(counts))


def link_view(state: RootState, index: int) -> dict:
    colouring = state.C[index]
    vertices = list(state.rot[state.r])
    colours = [colouring[state.pos[v]] for v in vertices]
    counts = Counter(colours)
    multiplicities = tuple(sorted(counts.values(), reverse=True))
    unique_colours = sorted(colour for colour, count in counts.items() if count == 1)
    n_colours = len(counts)
    return {
        "vertices": vertices,
        "colours": colours,
        "multiplicities": multiplicities,
        "n_colours": n_colours,
        "unique_colours": unique_colours,
        "has_unique": bool(unique_colours),
        "fill": n_colours <= 3,
        "frozen_four": n_colours == 4,
    }


def bichromatic_components(state: RootState, index: int) -> list[dict]:
    """Components in the same order as RootState.info[index]['moves']."""
    colouring = state.C[index]
    moves = state.info[index]["moves"]
    found: list[dict] = []
    cursor = 0
    for a, b in PAIRS:
        pending = {i for i, colour in enumerate(colouring) if colour in (a, b)}
        while pending:
            seed = min(pending)
            pending.remove(seed)
            comp = {seed}
            stack = [seed]
            while stack:
                vertex = stack.pop()
                for nbr in state.adj[vertex]:
                    if nbr in pending:
                        pending.remove(nbr)
                        comp.add(nbr)
                        stack.append(nbr)
            na = sum(colouring[i] == a for i in comp)
            nb = sum(colouring[i] == b for i in comp)
            vertices = tuple(sorted(state.V[i] for i in comp))
            pair, move_vertices, target = moves[cursor]
            if pair != (a, b) or move_vertices != vertices:
                raise AssertionError(f"move list diverged at state {index} step {cursor}")
            found.append({
                "pair": (a, b),
                "vertices": vertices,
                "na": na,
                "nb": nb,
                "counts": tuple(sorted((na, nb))),
                "neutral": na == nb,
                "size": len(comp),
                "target": target,
                "meets_link": bool(comp & state.Bset),
            })
            cursor += 1
    if cursor != len(moves):
        raise AssertionError(f"state {index}: {cursor} components, {len(moves)} moves")
    return found


def ion_signature(comps: list[dict]) -> tuple:
    return tuple(sorted(comp["counts"] for comp in comps if not comp["neutral"]))


def pattern_row(state: RootState, comp: dict, target_comps: list[dict]) -> tuple:
    link = link_view(state, comp["target"])
    info = state.info[comp["target"]]
    return (
        comp["size"],
        comp["counts"],
        ion_signature(target_comps),
        population(state.C[comp["target"]]),
        link["multiplicities"],
        info["p"],
        info["q"],
    )


def colouring_pattern(state: RootState, index: int) -> dict:
    comps = bichromatic_components(state, index)
    rows = []
    for comp in comps:
        if not comp["neutral"]:
            raise AssertionError(f"state {index} has a charged component before any swap")
        target_comps = bichromatic_components(state, comp["target"])
        rows.append(pattern_row(state, comp, target_comps))
    creating = [row for row in rows if row[2]]
    return {
        "rows": tuple(sorted(rows)),
        "creating": tuple(sorted(creating)),
        "n_components": len(comps),
        "n_creating": len(creating),
        "population": population(state.C[index]),
        "all_neutral": all(comp["neutral"] for comp in comps),
    }


def second_swaps(state: RootState, index: int) -> list[dict]:
    start = state.info[index]
    start_link = link_view(state, index)
    records = []
    for comp in bichromatic_components(state, index):
        if not comp["neutral"]:
            continue
        mid = comp["target"]
        mid_comps = bichromatic_components(state, mid)
        ions = [item for item in mid_comps if not item["neutral"]]
        if not ions:
            continue
        mid_info = state.info[mid]
        mid_link = link_view(state, mid)
        for ion in ions:
            end = ion["target"]
            end_info = state.info[end]
            end_link = link_view(state, end)
            _col, boundary, singletons, gap, d5, locked = colour_view(state.rot, state, end)
            records.append({
                "start": index,
                "start_q": start["q"],
                "start_R": start["R"],
                "start_population": list(population(state.C[index])),
                "start_link_colours": start_link["colours"],
                "start_link_multiplicities": list(start_link["multiplicities"]),
                "first_pair": list(comp["pair"]),
                "first_component": list(comp["vertices"]),
                "first_counts": list(comp["counts"]),
                "mid": mid,
                "mid_population": list(population(state.C[mid])),
                "mid_q": mid_info["q"],
                "mid_p": mid_info["p"],
                "mid_R": mid_info["R"],
                "mid_link_colours": mid_link["colours"],
                "mid_link_multiplicities": list(mid_link["multiplicities"]),
                "mid_fill": mid_link["fill"],
                "mid_has_unique": mid_link["has_unique"],
                "mid_ions": [list(item["counts"]) for item in ions],
                "second_pair": list(ion["pair"]),
                "second_component": list(ion["vertices"]),
                "second_counts": list(ion["counts"]),
                "second_na_nb_labelled": [ion["na"], ion["nb"]],
                "end": end,
                "end_colouring": list(state.C[end]),
                "end_population": list(population(state.C[end])),
                "end_q": end_info["q"],
                "end_p": end_info["p"],
                "end_R": end_info["R"],
                "end_link_vertices": end_link["vertices"],
                "end_link_colours": end_link["colours"],
                "end_link_multiplicities": list(end_link["multiplicities"]),
                "end_n_colours": end_link["n_colours"],
                "gains_unique_colour": end_link["has_unique"] and not mid_link["has_unique"],
                "has_unique_colour": end_link["has_unique"],
                "drops_to_three_colours": end_link["n_colours"] == 3,
                "fill": end_link["fill"],
                "frozen_four": end_link["frozen_four"],
                "q_falls_vs_mid": end_info["q"] < mid_info["q"],
                "q_falls_vs_start": end_info["q"] < start["q"],
                "q_rises_vs_mid": end_info["q"] > mid_info["q"],
                "q_rises_vs_start": end_info["q"] > start["q"],
                "R_falls_vs_start": end_info["R"] < start["R"],
                "descent_returns_none": state.descent(end, 2) is None,
                "end_stuck": end_info["p"] == 1 and state.descent(end, 2) is not None,
                "locked": locked,
                "singletons": singletons,
                "gap": gap,
                "degree_five_on_link": d5,
                "same_root": True,
            })
            # silence unused in case the boundary is wanted later
            del boundary
    return records


def locked_report(state: RootState, index: int) -> dict:
    comps = bichromatic_components(state, index)
    created = []
    for comp in comps:
        target_comps = bichromatic_components(state, comp["target"])
        ions = ion_signature(target_comps)
        if ions:
            created.append({
                "pair": list(comp["pair"]),
                "component": list(comp["vertices"]),
                "neutral": comp["neutral"],
                "counts": list(comp["counts"]),
                "target": comp["target"],
                "ions": [list(item) for item in ions],
                "population": list(population(state.C[comp["target"]])),
            })
    info = state.info[index]
    return {
        "root": state.r,
        "state": index,
        "colouring": list(state.C[index]),
        "population": list(population(state.C[index])),
        "p": info["p"],
        "q": info["q"],
        "stuck": info["p"] == 1 and state.descent(index, 2) is not None,
        "n_components": len(comps),
        "n_ions_at_start": sum(not comp["neutral"] for comp in comps),
        "start_ions": [list(comp["counts"]) for comp in comps if not comp["neutral"]],
        "n_one_step_creating_an_ion": len(created),
        "creations": created,
        "link": link_view(state, index),
    }


def summarise_records(records: list[dict]) -> dict:
    if not records:
        return {"n": 0}
    def count(key: str) -> int:
        return sum(1 for row in records if row[key])
    populations = sorted({tuple(row["end_population"]) for row in records})
    multiplicities = sorted({tuple(row["end_link_multiplicities"]) for row in records})
    return {
        "n": len(records),
        "fills": count("fill"),
        "drops_to_three": count("drops_to_three_colours"),
        "gains_unique": count("gains_unique_colour"),
        "has_unique": count("has_unique_colour"),
        "frozen_four": count("frozen_four"),
        "q_falls_vs_mid": count("q_falls_vs_mid"),
        "q_falls_vs_start": count("q_falls_vs_start"),
        "q_rises_vs_start": count("q_rises_vs_start"),
        "R_falls_vs_start": count("R_falls_vs_start"),
        "descent_returns_none": count("descent_returns_none"),
        "end_stuck": count("end_stuck"),
        "populations": [list(item) for item in populations],
        "link_multiplicities": [list(item) for item in multiplicities],
    }


def main() -> None:
    ascii3 = load_ascii(17, 3)
    ascii0 = load_ascii(17, 0)
    rot3 = parse_ascii(ascii3)
    rot0 = parse_ascii(ascii0)
    print("building root 3", flush=True)
    root3 = RootState(rot3, 3)
    print(f"root 3 orbits {len(root3.C)}", flush=True)
    print("building root 13", flush=True)
    root13 = RootState(rot3, 13)
    print(f"root 13 orbits {len(root13.C)}", flush=True)
    print("building locked roots", flush=True)
    root4 = RootState(rot0, 4)
    root6 = RootState(rot0, 6)
    print(f"root 4 orbits {len(root4.C)} root 6 orbits {len(root6.C)}", flush=True)

    stuck3 = [i for i, info in enumerate(root3.info) if info["p"] == 1 and root3.descent(i, 2) is not None]
    stuck13 = [i for i, info in enumerate(root13.info) if info["p"] == 1 and root13.descent(i, 2) is not None]
    print("stuck root 3", stuck3)
    print("stuck root 13", stuck13)
    if tuple(stuck3) != ROOT3 or tuple(stuck13) != ROOT13:
        raise SystemExit(f"stuck orbits drifted: {stuck3} {stuck13}")

    patterns = {}
    for index in ROOT3:
        patterns[("root3", index)] = colouring_pattern(root3, index)
    for index in ROOT13:
        patterns[("root13", index)] = colouring_pattern(root13, index)

    base = patterns[("root3", 44)]["creating"]
    uniform = all(patterns[key]["creating"] == base and patterns[key]["all_neutral"] for key in patterns)
    print("uniform", uniform)
    print("44 creating", len(base), "of", patterns[("root3", 44)]["n_components"])
    for key, pattern in patterns.items():
        print(key, "creating", pattern["n_creating"], "of", pattern["n_components"], "match", pattern["creating"] == base)

    # Distinct ion signatures on 44, ignoring q so a shared shape is visible.
    shapes = sorted({(row[0], row[1], row[2], row[3], row[4], row[5]) for row in base})
    print("44 ion-creating shapes", len(shapes))
    for shape in shapes:
        print(" ", shape)

    records_44 = second_swaps(root3, 44)
    print("second swaps from 44", len(records_44))
    print(json.dumps(summarise_records(records_44), indent=1))

    sibling_records = {}
    if uniform:
        for index in ROOT3:
            if index == 44:
                continue
            sibling_records[f"3:{index}"] = second_swaps(root3, index)
        for index in ROOT13:
            sibling_records[f"13:{index}"] = second_swaps(root13, index)
        for key, rows in sibling_records.items():
            print(key, json.dumps(summarise_records(rows)))

    locked = {
        "4:25": locked_report(root4, 25),
        "6:27": locked_report(root6, 27),
    }
    for key, row in locked.items():
        print(key, "start ions", row["n_ions_at_start"], "created", row["n_one_step_creating_an_ion"], "stuck", row["stuck"])

    payload = {
        "uniform": uniform,
        "shapes_44": [list(item) if not isinstance(item, tuple) else item for item in []],
        "summary_44": summarise_records(records_44),
        "records_44": records_44,
        "sibling_summaries": {key: summarise_records(rows) for key, rows in sibling_records.items()},
        "sibling_records": sibling_records,
        "locked": locked,
        "patterns": {
            f"{root}:{index}": {
                "n_components": pattern["n_components"],
                "n_creating": pattern["n_creating"],
                "population": list(pattern["population"]),
                "all_neutral": pattern["all_neutral"],
                "match_44": pattern["creating"] == base,
            }
            for (root, index), pattern in patterns.items()
        },
    }
    # JSON cannot encode tuples nested in shapes; records are already lists.
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
