"""WP19 producer: one pass per phase, no tuning. See ../WP19-preregistered-conjectures-declaration.md.

NOT RELEASED. No phase may run until the math team posts a written go-ahead in
SolvingFrameworkPlan/messages/ naming the declaration and its commit, and the user releases it.
The guard below refuses to run unless WP19_RELEASED=1 is set in the environment.

Usage: WP19_RELEASED=1 PLANTRI=/path/to/plantri python3 wp19_run.py P1|P2|P3 [--procs N]
  P1: order 23, every graph, from `$PLANTRI -m5 -a 23`; stdout sha256 must equal ORDER23_SHA
      before anything is computed.
  P2: U-exists only, orders 21 and 22, from ../wp17-last-roots/triangulations-min5-{21,22}.txt
      (sha256 checked). The full per-graph record is still produced; only U-exists is a test.
  P3: order 24, every graph, from `$PLANTRI -m5 -a 24`; its hash is recorded (no expected value).
Writes wp19-<phase>.json. Limits: 30 min per graph, 12 h per phase, 8 GB peak RSS per worker,
1 GB output per phase (past it witnesses are dropped and the phase is marked truncated).

Phase JSON: {"phase", "declaration", "declaration_sha256", "source_sha256", "input_sha256",
"caps":{"mixed":6,"kempe":7}, "truncated", "graphs":[G...], "summary"}; G and P as produced
by wp19_core.graph_report.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # L/; HERE may be redirected for output only
sys.path.insert(0, str(HERE))
import wp19_core  # noqa: E402
from wp19_core import CAP_KEMPE, CAP_MIXED, graph_report, parse_ascii  # noqa: E402

DECL = HERE.parent / "WP19-preregistered-conjectures-declaration.md"
PER_GRAPH = 30 * 60
PER_PHASE = 12 * 3600
OUTPUT_CAP = 1_000_000_000
ORDER23_SHA = "d233b4efafdd3510f133760d9d918beab70e7496759aef512fb302cbd594bafa"
ORDER21 = HERE.parent / "wp17-last-roots" / "triangulations-min5-21.txt"
ORDER21_SHA = "5c20395802df3f98d81d1cf2cc68c3995ac5f1b0f8438da9b0ac281cdeeb1c6d"
ORDER22 = HERE.parent / "wp17-last-roots" / "triangulations-min5-22.txt"
ORDER22_SHA = "6137dc19b7a036ae42388153ca23b93ae7cbb8f03280718529834a18ae7df2d7"
SOURCES = [HERE / "wp19_core.py", HERE / "wp19_run.py",
           HERE.parent / "wp18" / "wp18_core.py", HERE.parent / "mass_core.py"]
STATEMENTS = ["M1", "M2", "M3", "C1", "C2", "C3", "U_exists"]
WITNESS_KEYS = ("witness_L", "u_fail_class")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def plantri(order):
    exe = os.environ.get("PLANTRI")
    if not exe:
        sys.exit("set PLANTRI to the plantri 5.8 executable")
    return subprocess.run([exe, "-m5", "-a", str(order)], check=True, capture_output=True).stdout


def inputs(phase):
    """[(order, index, ascii)] and input_sha256: sha256 of the raw input bytes (plantri stdout for
    P1/P3, a string; for P2 a dict {file name: sha256} over its two files). graph_index is the
    0-based position among non-empty lines of each input. Hashes are verified before compute."""
    if phase == "P1":
        raw = plantri(23)
        h = sha(raw)
        if h != ORDER23_SHA:
            sys.exit(f"order-23 plantri output hash {h} != declared {ORDER23_SHA}; nothing computed")
        sets = [(23, raw)]
        hashes = h
    elif phase == "P2":
        sets, hashes = [], {}
        for order, path, want in ((21, ORDER21, ORDER21_SHA), (22, ORDER22, ORDER22_SHA)):
            raw = path.read_bytes()
            h = sha(raw)
            if h != want:
                sys.exit(f"{path.name} hash {h} != declared {want}; nothing computed")
            sets.append((order, raw))
            hashes[path.name] = h
    else:
        raw = plantri(24)
        sets = [(24, raw)]
        hashes = sha(raw)
    gs = []
    for order, raw in sets:
        lines = [ln for ln in raw.decode().splitlines() if ln.strip()]
        gs += [(order, i, ln) for i, ln in enumerate(lines)]
    return gs, hashes


def work(args):
    order, idx, ascii_, phase_deadline = args
    now = time.monotonic()
    if now > phase_deadline:
        rot = parse_ascii(ascii_)
        return graph_report(rot, deadline=now - 1, order=order, graph_index=idx, ascii_=ascii_)
    rot = parse_ascii(ascii_)
    assert len(rot) == order
    return graph_report(rot, deadline=min(now + PER_GRAPH, phase_deadline),
                        order=order, graph_index=idx, ascii_=ascii_)


def strip(G):
    keep_u = any(k["stmt"] == "U_exists" for k in G["kills"])  # its certificate is the classes
    for P in G["pairs"]:
        P.pop("witness_L", None)
        if not keep_u:
            P.pop("u_fail_class", None)
    G["witnesses_dropped"] = True
    return G


def graph_status(G, stmt):
    if any(k["stmt"] == stmt for k in G["kills"]):
        return "killed"
    if stmt == "C1" and G["order"] < 18:
        return "not_applicable"
    if stmt == "C3" and max(G["degrees"]) < 7:
        return "not_applicable"
    if G["interrupted"] or G["unresolved_pairs"]:
        return "unresolved"
    if stmt == "U_exists" and G["U_exists"] is not True:
        return "unresolved"
    return "passed"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["P1", "P2", "P3"])
    ap.add_argument("--procs", type=int, default=12)
    a = ap.parse_args()
    print("REMINDER: WP19 needs the math team's written go-ahead (naming the declaration, its "
          "commit, the producer and the checker) and the user's release before any phase runs.",
          file=sys.stderr)
    if os.environ.get("WP19_RELEASED") != "1":
        sys.exit("refusing to run: WP19_RELEASED=1 is not set (phase not released)")
    gs, in_hashes = inputs(a.phase)
    deadline = time.monotonic() + PER_PHASE
    t0 = time.time()
    out_path = HERE / f"wp19-{a.phase}.json"
    tmp_path = HERE / f".wp19-{a.phase}.graphs.tmp"
    head = {"phase": a.phase, "declaration": DECL.name,
            "declaration_sha256": sha(DECL.read_bytes()),
            "source_sha256": {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in SOURCES},
            "input_sha256": in_hashes,
            "caps": {"mixed": CAP_MIXED, "kempe": CAP_KEMPE}}
    budget = OUTPUT_CAP - 50_000_000  # reserve for header and summary
    written, truncated = 0, False
    summ = {"graphs": 0, "interrupted": [], "unresolved_graphs": [], "m_hist": {},
            "U_exists": {"true": 0, "false": 0, "null": 0}, "statements": {},
            "first_kill": {}, "hist_l": {}, "hist_k": {}, "max_L_at_least": None,
            "empty_pairs": [], "graphs_without_legal_pairs": [], "max_peak_rss_kb": 0}
    for s in STATEMENTS:
        summ["statements"][s] = {"killed": [], "passed": 0, "unresolved": 0, "not_applicable": 0}
    with tmp_path.open("w") as tmp, Pool(a.procs, maxtasksperchild=1) as pool:
        first = True
        for G in pool.imap(work, [(o, i, s, deadline) for o, i, s in gs]):
            key = [G["order"], G["graph_index"]]
            summ["graphs"] += 1
            if G["interrupted"]:
                summ["interrupted"].append(key + [G["interrupted"]])
            if G["unresolved_pairs"]:
                summ["unresolved_graphs"].append(key)
            mk = str(G["m"]) if G["m"] is not None else f">={G['m_at_least']}"
            summ["m_hist"][mk] = summ["m_hist"].get(mk, 0) + 1
            summ["U_exists"][json.dumps(G["U_exists"])] += 1
            for st in STATEMENTS:
                r = graph_status(G, st)
                if r == "killed":
                    summ["statements"][st]["killed"].append(key)
                    summ["first_kill"].setdefault(st, key)
                else:
                    summ["statements"][st][r] += 1
            for P in G["pairs"]:
                for hk in ("hist_l", "hist_k"):
                    for k, c in P[hk].items():
                        summ[hk][k] = summ[hk].get(k, 0) + c
                if P["empty"]:
                    summ["empty_pairs"].append(key + [P["v"], P["fan_index"]])
                m = summ["max_L_at_least"]
                summ["max_L_at_least"] = P["L_at_least"] if m is None else max(m, P["L_at_least"])
            if not G["pairs"]:
                summ["graphs_without_legal_pairs"].append(key)
            summ["max_peak_rss_kb"] = max(summ["max_peak_rss_kb"], G["peak_rss_kb"])
            s = json.dumps(G, separators=(",", ":"))
            if truncated or written + len(s) > budget:
                truncated = True
                s = json.dumps(strip(G), separators=(",", ":"))
            if written + len(s) > OUTPUT_CAP - 1_000_000:
                raise SystemExit("output cap reached even without witnesses; phase stopped")
            tmp.write(("" if first else ",") + s)
            written += len(s) + 1
            first = False
    for st in STATEMENTS:
        summ["statements"][st]["killed_count"] = len(summ["statements"][st]["killed"])
    summ["wall_seconds"] = round(time.time() - t0, 1)
    summ["output_bytes_graphs"] = written
    with out_path.open("w") as f:
        h = dict(head)
        h["truncated"] = truncated
        f.write(json.dumps(h, separators=(",", ":"))[:-1] + ',"graphs":[')
        with tmp_path.open() as tmp:
            while True:
                chunk = tmp.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
        f.write('],"summary":' + json.dumps(summ, separators=(",", ":")) + "}")
    tmp_path.unlink()
    print(json.dumps({"phase": a.phase, "truncated": truncated,
                      **{k: v for k, v in summ.items() if k != "statements"},
                      "kills": {k: v["killed_count"] for k, v in summ["statements"].items()}}))


if __name__ == "__main__":
    main()
