"""WP18 producer: one pass per phase, no tuning. See ../WP18-fan-selection-length-declaration.md.

Usage: wp18_run.py P1|P2|P3 [--procs N]
P1: discovery graphs (orders 12, 14-18) from ../wp11-run-manifest.json
P2: validation graphs (orders 19-20) from the same manifest (secondary, not a holdout)
P3: order 21, ../wp17-last-roots/triangulations-min5-21.txt (sha256 checked)
Writes wp18-<phase>.json. Limits: 30 min per graph, 6 h per phase.
"""
import argparse
import hashlib
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from wp18_core import CAP, Interrupted, graph_report, parse_ascii  # noqa: E402

PER_GRAPH = 30 * 60
PER_PHASE = 6 * 3600
ORDER21 = HERE.parent / "wp17-last-roots" / "triangulations-min5-21.txt"
ORDER21_SHA = "5c20395802df3f98d81d1cf2cc68c3995ac5f1b0f8438da9b0ac281cdeeb1c6d"


def graphs(phase):
    if phase in ("P1", "P2"):
        m = json.loads((HERE.parent / "wp11-run-manifest.json").read_text())
        key = "discovery_graphs" if phase == "P1" else "validation_graphs"
        return [(g["order"], g["graph_index"], g["ascii"]) for g in m[key]]
    raw = ORDER21.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == ORDER21_SHA, "order-21 input hash mismatch"
    return [(21, i, line) for i, line in enumerate(raw.decode().splitlines()) if line.strip()]


def work(args):
    order, idx, ascii_, phase_deadline = args
    t0 = time.monotonic()
    rot = parse_ascii(ascii_)
    out = {"order": order, "graph_index": idx, "ascii": ascii_,
           "ascii_sha256": hashlib.sha256(ascii_.encode()).hexdigest()}
    try:
        out["report"] = graph_report(rot, CAP, min(t0 + PER_GRAPH, phase_deadline))
    except Interrupted as e:
        out["interrupted"] = str(e)
    out["seconds"] = round(time.monotonic() - t0, 2)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["P1", "P2", "P3"])
    ap.add_argument("--procs", type=int, default=12)
    a = ap.parse_args()
    gs = graphs(a.phase)
    deadline = time.monotonic() + PER_PHASE
    t0 = time.time()
    with Pool(a.procs) as pool:
        res = list(pool.imap_unordered(work, [(o, i, s, deadline) for o, i, s in gs]))
    res.sort(key=lambda r: (r["order"], r["graph_index"]))
    done = [r for r in res if "report" in r]
    summary = {
        "graphs": len(res),
        "interrupted": [(r["order"], r["graph_index"]) for r in res if "interrupted" in r],
        "m_hist": {},
        "max_m": None,
        "max_L_at_least": max((r["report"]["max_L_at_least"] for r in done), default=None),
        "first_m_ge_2": next(([r["order"], r["graph_index"]] for r in done if (r["report"]["m_at_least"] or 0) >= 2), None),
        "first_m_ge_3": next(([r["order"], r["graph_index"]] for r in done if (r["report"]["m_at_least"] or 0) >= 3), None),
        "wall_seconds": round(time.time() - t0, 1),
    }
    for r in done:
        k = str(r["report"]["m"]) if r["report"]["m"] is not None else f">={r['report']['m_at_least']}"
        summary["m_hist"][k] = summary["m_hist"].get(k, 0) + 1
    exact = [r["report"]["m"] for r in done if r["report"]["m"] is not None]
    summary["max_m"] = max(exact, default=None)
    out = {"phase": a.phase, "cap": CAP, "declaration": "WP18-fan-selection-length-declaration.md",
           "summary": summary, "graphs": res}
    path = HERE / f"wp18-{a.phase}.json"
    path.write_text(json.dumps(out, separators=(",", ":")))
    print(json.dumps({"phase": a.phase, **summary}))


if __name__ == "__main__":
    main()
