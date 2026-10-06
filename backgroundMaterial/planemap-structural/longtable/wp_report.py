"""Summarise a WP20/WP21 producer output as markdown (counts only; no claims).
usage: wp_report.py OUTPUT.json [--title T] [--top K]
Lists: binding hashes, totals, depth histogram, kills (each with its P verdict and the vertex-level
filled_neighbour_for_bad count), status counts, SEP-bad statistics, colour-class sizes of SEP-bad states."""
import argparse
import collections
import hashlib
import json

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--title", default="Results")
ap.add_argument("--top", type=int, default=10)
a = ap.parse_args()
o = json.load(open(a.out))
G = o["graphs"]
V = [(g["index"], v) for g in G for v in g["vertices"]]
done = [(i, v) for i, v in V if v["status"] != "interrupted"]
tot = lambda k: sum(v.get(k, 0) for _, v in done)
dep = {k: sum(v["depth"].get(k, 0) for _, v in done) for k in ("1", "2", "3", ">3")}
print(f"## {a.title}\n")
print(f"- WP `{o.get('wp')}`, phase `{o.get('phase')}`, order {o.get('order')}, truncated: {o.get('truncated')}, wall seconds: {o.get('wall_seconds')}")
print(f"- declaration SHA-256 `{o.get('declaration_sha256')}`")
print(f"- input SHA-256 `{o.get('input_sha256')}`")
print(f"- producer hashes: {o.get('producer_sha256')}")
print(f"- output file SHA-256 `{hashlib.sha256(open(a.out,'rb').read()).hexdigest()}`\n")
st = collections.Counter(g["status"] for g in G)
vs = collections.Counter(v["status"] for _, v in V)
print(f"| Quantity | Value |\n|---|---|")
print(f"| graphs | {len(G)} (status: {dict(st)}) |")
print(f"| degree-5 vertices | {len(V)} (status: {dict(vs)}) |")
print(f"| unfilled states | {tot('unfilled_total')} |")
print(f"| states with a legal admitting fan | {tot('states')} |")
print(f"| no_legal_fan | {tot('no_legal_fan')} |")
print(f"| SEP-bad states | {tot('sep_bad')} |")
print(f"| depth of SEP-bad (1 / 2 / 3 / >3) | {dep['1']} / {dep['2']} / {dep['3']} / {dep['>3']} |")
print(f"| SEP-bad with a filled pure neighbour (`filled_neighbour_for_bad`) | {tot('filled_neighbour_for_bad')} |")
print(f"| **D1 kills** | {tot('d1_kills')} |")
print(f"| **P kills** | {tot('p_kills')} |")
print(f"| P capped | {tot('p_capped')} |")
print(f"| locked classes (Tilley) | {tot('locked_classes')} |")
print()
kills = o["witnesses"]["d1_kills"]
pk = {(w["index"], w["x"], tuple(w["state"])) for w in o["witnesses"]["p_kills"]}
vert = {(i, v["x"]): v for i, v in V}
print(f"### D1 kills ({len(kills)})\n")
if not kills:
    print("None among the graphs run. This says nothing about other graphs.\n")
for w in kills:
    v = vert[(w["index"], w["x"])]
    pv = "P KILL (no filled state in the class)" if (w["index"], w["x"], tuple(w["state"])) in pk else \
         ("P capped (inconclusive)" if v["p_capped"] else "P holds (the class contains a filled state)")
    print(f"- graph {w['index']} vertex {w['x']}: P verdict: {pv}; vertex-level filled_neighbour_for_bad = {v['filled_neighbour_for_bad']}; state `{w['state']}`")
print()
print(f"### P kills ({len(o['witnesses']['p_kills'])})\n")
if not o["witnesses"]["p_kills"]:
    print("None among the graphs run.\n")
per = collections.Counter()
for i, v in V:
    if v["status"] != "interrupted":
        per[i] += v["sep_bad"]
gb = {i: c for i, c in per.items() if c}
print(f"### SEP-bad statistics\n")
print(f"- graphs with at least one SEP-bad state: {len(gb)} of {len(G)}; total {sum(gb.values())}")
print(f"- distribution of SEP-bad count per such graph: {dict(sorted(collections.Counter(gb.values()).items()))}")
top = sorted(gb.items(), key=lambda t: (-t[1], t[0]))[:a.top]
print(f"- top graphs by SEP-bad count: " + ", ".join(f"{i} ({c})" for i, c in top))
locked_graphs = collections.Counter()
for i, v in V:
    if v["status"] != "interrupted":
        locked_graphs[i] += v["locked_classes"]
lg = {i: c for i, c in locked_graphs.items() if c}
print(f"- graphs with a locked class: {len(lg)} of {len(G)}; total locked classes {sum(lg.values())}")
sizes = collections.Counter()
for w in o["witnesses"]["sep_bad"]:
    c = collections.Counter(x for k, x in enumerate(w["state"]) if k != w["x"])
    sizes[tuple(sorted(c.values()))] += 1
print(f"- colour-class sizes of SEP-bad states (sorted multisets): {dict(sorted(sizes.items()))}")
intr = [(i, v["x"], v.get("reason")) for i, v in V if v["status"] == "interrupted"]
print(f"- interrupted vertices: {len(intr)} {intr[:5]}")
