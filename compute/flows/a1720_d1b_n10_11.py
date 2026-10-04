"""D1b (Agent 1720): Tait = 4-flows = P(T,4)/4 on triangulations n=10 and n=11.

Imports ``a1720_tait_flows`` and monkeypatches its ``OUT`` path. Does not edit
that script, does not recompute ``n <= 9``, and does not write
``D1_results.json``.

Two processes, one per order. Each process stops at 600 seconds and writes a
part file. ``merge`` combines the parts into ``groups/D1_n11.json``.

Usage::

    .venv/bin/python compute/flows/a1720_d1b_n10_11.py 10
    .venv/bin/python compute/flows/a1720_d1b_n10_11.py 11
    .venv/bin/python compute/flows/a1720_d1b_n10_11.py merge
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import networkx as nx

import a1720_tait_flows as flows

ROOT = Path(__file__).resolve().parents[2]
GROUPS = ROOT / "backgroundMaterial" / "agent1720" / "groups"
FINAL = GROUPS / "D1_n11.json"
LIMIT_S = 600.0
SEED = 1720


def part_path(n: int) -> Path:
    """Temporary per-order output. Removed by ``merge``."""
    return GROUPS / f"_D1b_n{n}_part.json"


def run_n(n: int) -> None:
    """Check the 4-identity on every cached triangulation of order ``n``."""
    flows.OUT = part_path(n)
    if flows.OUT.name == "D1_results.json":
        raise RuntimeError("refusing to write D1_results.json")
    data = json.loads(flows.DATA.read_text())
    graphs = data["graphs"][str(n)]
    rng = random.Random(SEED)
    rows: list[dict] = []
    mismatches: list[dict] = []
    t0 = time.monotonic()
    hit_limit = False
    for i, el in enumerate(graphs):
        if time.monotonic() - t0 >= LIMIT_S:
            hit_limit = True
            break
        T = nx.Graph([tuple(e) for e in el])
        D = flows.simple_dual(T)
        a = flows.count_tait(D)
        b = flows.count_z2z2_flows(D)
        c = flows.count_zk_flows(D, 4, flows.default_orientation(D))
        c2 = flows.count_zk_flows(D, 4, flows.random_orientation(D, rng))
        p4 = flows.count_colourings(T, 4)
        row = {
            "name": f"T_{n}_{i}",
            "dual_vertices": D.number_of_nodes(),
            "dual_edges": D.number_of_edges(),
            "dual_vertex_connectivity": nx.node_connectivity(D),
            "dual_edge_connectivity": nx.edge_connectivity(D),
            "tait": a,
            "z2z2": b,
            "z4": c,
            "z4_random_orientation": c2,
            "P4": p4,
        }
        ok = a == b == c == c2 and 4 * a == p4 and a > 0
        row["ok"] = ok
        if not ok:
            mismatches.append(row)
        rows.append(row)
        if (i + 1) % 200 == 0:
            print(f"n={n}: {i + 1}/{len(graphs)} in {time.monotonic() - t0:.1f}s", flush=True)
    elapsed = time.monotonic() - t0
    summary = {
        "count_cached": len(graphs),
        "count_checked": len(rows),
        "all_identities_hold": (not hit_limit) and len(rows) == len(graphs) and all(r["ok"] for r in rows),
        "extra_k3_k5_checked": False,
        "hit_time_limit": hit_limit,
        "time_limit_seconds": LIMIT_S,
        "tait_min": min(r["tait"] for r in rows) if rows else None,
        "tait_max": max(r["tait"] for r in rows) if rows else None,
        "dual_vertex_connectivity_values": sorted({r["dual_vertex_connectivity"] for r in rows}),
        "dual_edge_connectivity_values": sorted({r["dual_edge_connectivity"] for r in rows}),
        "mismatches": len(mismatches),
        "elapsed_seconds": round(elapsed, 2),
        "seed": SEED,
    }
    out = {"n": n, "per_n": summary, "mismatches": mismatches, "graphs": rows}
    flows.OUT.parent.mkdir(parents=True, exist_ok=True)
    flows.OUT.write_text(json.dumps(out, indent=1))
    print(
        f"n={n}: checked {len(rows)}/{len(graphs)}, ok={summary['all_identities_hold']}, "
        f"tait in [{summary['tait_min']},{summary['tait_max']}], "
        f"edge-connectivity {summary['dual_edge_connectivity_values']}, "
        f"limit_hit={hit_limit}, {elapsed:.1f}s; wrote {flows.OUT}",
        flush=True,
    )


def merge() -> None:
    """Combine the n=10 and n=11 part files into ``D1_n11.json``."""
    flows.OUT = FINAL
    if flows.OUT.name == "D1_results.json":
        raise RuntimeError("refusing to write D1_results.json")
    parts = []
    for n in (10, 11):
        path = part_path(n)
        parts.append(json.loads(path.read_text()))
    t0 = time.monotonic()
    sanity = flows.sanity()
    sanity_s = round(time.monotonic() - t0, 2)
    out: dict = {
        "identity": "tait == z2z2 == z4 == z4_random_orientation == P4/4 and tait > 0",
        "n_le_9_recomputed": False,
        "extra_k3_k5_checked": False,
        "time_limit_seconds_per_n": LIMIT_S,
        "processes": 2,
        "seed": SEED,
        "sanity": sanity,
        "sanity_elapsed_seconds": sanity_s,
        "per_n": {},
        "mismatches": [],
        "graphs": {},
    }
    total = sanity_s
    for part in parts:
        n = str(part["n"])
        out["per_n"][n] = part["per_n"]
        out["mismatches"].extend(part["mismatches"])
        out["graphs"][n] = part["graphs"]
        total += part["per_n"]["elapsed_seconds"]
    out["elapsed_seconds"] = round(total, 2)
    out["command"] = (
        ".venv/bin/python compute/flows/a1720_d1b_n10_11.py 10  &  "
        ".venv/bin/python compute/flows/a1720_d1b_n10_11.py 11  &  wait;  "
        ".venv/bin/python compute/flows/a1720_d1b_n10_11.py merge"
    )
    flows.OUT.write_text(json.dumps(out, indent=1) + "\n")
    for n in (10, 11):
        part_path(n).unlink()
    print(
        f"mismatches: {len(out['mismatches'])}; "
        f"n10={out['per_n']['10']['elapsed_seconds']}s "
        f"n11={out['per_n']['11']['elapsed_seconds']}s; wrote {flows.OUT}",
        flush=True,
    )


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "merge"
    if arg == "merge":
        merge()
    else:
        run_n(int(arg))
