"""WP20 producer (declaration: WP20-D1-declaration.md, format: WP20-output-format.md).

Self-contained: imports no other repository code. Statements D1 and P at degree-5 vertices of
plantri -m5 triangulations.  Usage:
  plantri -m5 N -a | python3 d1_confirm.py --phase P1 --order N --out OUT.json
        [--workers K] [--decl DECL.md] [--graph-limit M] [--first F]
Every graph is one task; per-graph deadline, per-worker memory limit and output cap are enforced
inside the loops.  Interrupted or capped items are recorded as such, never as passes.
"""
import argparse
import hashlib
import itertools
import json
import os
import resource
import sys
import time
from collections import deque
from multiprocessing import Pool

HOLE = 4
PAIRS = list(itertools.combinations(range(4), 2))
GRAPH_SECONDS = 1800
MEM_BYTES = 8 * 1024 ** 3
CLASS_CAP = 200000
OUT_CAP = 10 ** 9


class Interrupted(Exception):
    def __init__(self, reason):
        self.reason = reason


class Budget:
    def __init__(self):
        self.t0 = time.time()
        self.tick = 0

    def check(self):
        self.tick += 1
        if self.tick & 1023:
            return
        if time.time() - self.t0 > GRAPH_SECONDS:
            raise Interrupted("time")
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != "darwin":
            rss *= 1024
        if rss > MEM_BYTES:
            raise Interrupted("memory")


def parse(line):
    n, body = line.split()
    rot = [[ord(c) - 97 for c in r] for r in body.split(",")]
    assert len(rot) == int(n)
    return rot


def canon(st):
    seen = {}
    out = []
    for v in st:
        if v == HOLE:
            out.append(HOLE)
        else:
            out.append(seen.setdefault(v, len(seen)))
    return tuple(out)


def colourings(adj, n, skip, start_order, budget):
    """All proper 4-colourings, canonical (label order, skip entry = HOLE), one per renaming class."""
    order = [v for v in start_order if v != skip]
    pos = {v: i for i, v in enumerate(order)}
    earlier = [[pos[w] for w in adj[v] if w != skip and pos[w] < i] for i, v in enumerate(order)]
    cur = [0] * len(order)
    out = []

    def go(i, top):
        budget.check()
        if i == len(order):
            st = [HOLE] * n
            for j, v in enumerate(order):
                st[v] = cur[j]
            out.append(canon(st))
            return
        blocked = {cur[j] for j in earlier[i]}
        for a in range(min(3, top + 1) + 1):
            if a not in blocked:
                cur[i] = a
                go(i + 1, max(top, a))

    go(0, -1)
    return out


def bfs_order(adj, n, roots, skip):
    seen = set(roots) | {skip}
    order = list(roots)
    q = deque(roots)
    while q:
        u = q.popleft()
        for w in sorted(adj[u]):
            if w not in seen:
                seen.add(w)
                order.append(w)
                q.append(w)
    return order


def kempe_nbrs(adj, st, budget):
    """Canonical states after one whole-component swap, over all colour pairs (HOLE untouched)."""
    n = len(st)
    out = []
    for a, b in PAIRS:
        seen = set()
        for s in range(n):
            if st[s] != a and st[s] != b or s in seen:
                continue
            comp = [s]
            seen.add(s)
            i = 0
            while i < len(comp):
                u = comp[i]
                i += 1
                for w in adj[u]:
                    if w not in seen and (st[w] == a or st[w] == b):
                        seen.add(w)
                        comp.append(w)
            nxt = list(st)
            for u in comp:
                nxt[u] = b if st[u] == a else a
            out.append(canon(nxt))
        budget.check()
    return out


def analyse_vertex(rot, adj, n, x, budget):
    ring = rot[x]
    legal = [j for j in range(5)
             if ring[(j + 2) % 5] not in adj[ring[j]] and ring[(j + 3) % 5] not in adj[ring[j]]]
    adjTx = [set(a) - {x} for a in adj]
    adjTx[x] = set()
    states = colourings(adjTx, n, x, bfs_order(adjTx, n, [r for r in ring], x), budget)
    index = {s: i for i, s in enumerate(states)}

    def ring_cols(s):
        return [s[w] for w in ring]

    unfilled = [i for i, s in enumerate(states) if len(set(ring_cols(s))) == 4]
    # --- pure Kempe graph on all states: components (P) and neighbours for depth
    nbr = {}

    def neighbours(i):
        if i not in nbr:
            nbr[i] = [index[t] for t in set(kempe_nbrs(adjTx, states[i], budget))]
        return nbr[i]

    comp = [-1] * len(states)
    comp_filled = []
    comp_size = []
    p_capped_comp = set()
    for i in range(len(states)):
        if comp[i] != -1:
            continue
        cid = len(comp_size)
        comp[i] = cid
        q = deque([i])
        size = 0
        has_fill = False
        while q:
            u = q.popleft()
            size += 1
            if len(set(ring_cols(states[u]))) <= 3:
                has_fill = True
            if size > CLASS_CAP:
                p_capped_comp.add(cid)
                break
            for w in neighbours(u):
                if comp[w] == -1:
                    comp[w] = cid
                    q.append(w)
        comp_filled.append(has_fill)
        comp_size.append(size)
    p_kills = p_capped = 0
    p_kill_ids = []
    for i in unfilled:
        c = comp[i]
        if c in p_capped_comp:
            p_capped += 1
        elif not comp_filled[c]:
            p_kills += 1
            p_kill_ids.append(i)
    # --- separability per legal fan
    sep_state = {}                       # state index -> True if separable for some admitting legal fan
    admitting = {}
    locked_classes = 0
    for j in legal:
        y = ring[j]
        G = [set(a) for a in adj]
        G[x].discard(y)
        G[y].discard(x)
        allc = colourings(G, n, -1, bfs_order(G, n, [x] + list(ring), -1), budget)
        gi = {c: k for k, c in enumerate(allc)}
        # components of Kempe graph on colourings of G
        cls = [-1] * len(allc)
        cls_sep = []
        cls_has_equal = []
        for k in range(len(allc)):
            if cls[k] != -1:
                continue
            cid = len(cls_sep)
            cls[k] = cid
            q = deque([k])
            sep = False
            eq = False
            while q:
                u = q.popleft()
                cu = allc[u]
                if cu[x] != cu[y]:
                    sep = True
                else:
                    eq = True
                for t in kempe_nbrs(G, cu, budget):
                    w = gi[t]
                    if cls[w] == -1:
                        cls[w] = cid
                        q.append(w)
            cls_sep.append(sep)
            cls_has_equal.append(eq)
        for cid in range(len(cls_sep)):
            if cls_has_equal[cid] and not cls_sep[cid]:
                locked_classes += 1
        for i in unfilled:
            s = states[i]
            cols = ring_cols(s)
            if cols.count(s[y]) != 1:
                continue
            admitting.setdefault(i, []).append(j)
            col = list(s)
            col[x] = s[y]
            k = gi[canon(col)]
            if cls_sep[cls[k]]:
                sep_state[i] = True
    cand = [i for i in unfilled if i in admitting]
    no_legal = len(unfilled) - len(cand)
    good = {i for i in cand if sep_state.get(i)}
    bad = [i for i in cand if i not in good]
    depth_hist = {"1": 0, "2": 0, "3": 0, ">3": 0}
    filled_nb = 0
    d1_kills = 0
    witnesses_bad = []
    witnesses_kill = []
    for i in bad:
        # BFS to depth 3 over all states through pure swaps
        dist = {i: 0}
        q = deque([i])
        d = None
        while q and d is None:
            u = q.popleft()
            if dist[u] == 3:
                continue
            for w in neighbours(u):
                if w in dist:
                    continue
                dist[w] = dist[u] + 1
                if w in good:
                    d = dist[w]
                    break
                q.append(w)
        key = str(d) if d is not None else ">3"
        depth_hist[key] += 1
        if any(len(set(ring_cols(states[w]))) <= 3 for w in neighbours(i)):
            filled_nb += 1
        w_rec = {"state": list(states[i]), "depth": d if d is not None else ">3"}
        witnesses_bad.append(w_rec)
        if not any(w in good for w in neighbours(i)):
            d1_kills += 1
            witnesses_kill.append({"state": list(states[i])})
    rec = {"x": x, "status": "complete",
           "unfilled_total": len(unfilled), "states": len(cand), "no_legal_fan": no_legal,
           "sep_bad": len(bad), "depth": depth_hist, "filled_neighbour_for_bad": filled_nb,
           "d1_kills": d1_kills, "p_kills": p_kills, "p_capped": p_capped,
           "locked_classes": locked_classes, "legal_fans": legal}
    if p_capped:
        rec["status"] = "capped"
    return rec, witnesses_bad, witnesses_kill, [list(states[i]) for i in p_kill_ids]


def analyse_graph(args):
    idx, line = args
    rot = parse(line)
    n = len(rot)
    adj = [set(r) for r in rot]
    budget = Budget()
    verts = []
    wit = {"sep_bad": [], "d1_kills": [], "p_kills": []}
    status = "complete"
    for x in range(n):
        if len(rot[x]) != 5:
            continue
        try:
            rec, wb, wk, wp = analyse_vertex(rot, adj, n, x, budget)
        except Interrupted as e:
            verts.append({"x": x, "status": "interrupted", "reason": e.reason})
            status = "interrupted"
            continue
        verts.append(rec)
        for w in wb:
            wit["sep_bad"].append({"index": idx, "x": x, **w})
        for w in wk:
            wit["d1_kills"].append({"index": idx, "x": x, **w})
        for s in wp:
            wit["p_kills"].append({"index": idx, "x": x, "state": s})
    return {"index": idx, "ascii": line.strip(), "status": status, "vertices": verts}, wit


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    ap.add_argument("--order", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--decl", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                   "WP20-D1-declaration.md"))
    ap.add_argument("--graph-limit", type=int, default=0)
    ap.add_argument("--first", type=int, default=0)
    ap.add_argument("--input-file", default="")
    a = ap.parse_args()
    raw = open(a.input_file, "rb").read() if a.input_file else sys.stdin.buffer.read()
    lines = [l for l in raw.decode().splitlines() if l.strip()]
    sel = list(enumerate(lines))[a.first:]
    if a.graph_limit:
        sel = sel[:a.graph_limit]
    graphs, wit = [], {"sep_bad": [], "d1_kills": [], "p_kills": []}
    t0 = time.time()
    done = 0
    with Pool(a.workers) as pool:
        for g, w in pool.imap_unordered(analyse_graph, sel, chunksize=4):
            graphs.append(g)
            for k in wit:
                wit[k].extend(w[k])
            done += 1
            if done % 500 == 0:
                print(f"{done}/{len(sel)} graphs, {time.time()-t0:.0f}s", flush=True)
    graphs.sort(key=lambda g: g["index"])
    out = {"wp": "WP20", "phase": a.phase, "order": a.order,
           "declaration_sha256": sha(a.decl), "input_sha256": hashlib.sha256(raw).hexdigest(),
           "producer_sha256": {"d1_confirm.py": sha(os.path.abspath(__file__))},
           "graphs": graphs, "witnesses": wit, "truncated": False,
           "wall_seconds": round(time.time() - t0, 1)}
    txt = json.dumps(out)
    if len(txt) > OUT_CAP:
        out["witnesses"] = {"sep_bad": [], "d1_kills": [], "p_kills": []}
        out["truncated"] = True
        txt = json.dumps(out)
    open(a.out, "w").write(txt)
    tot = lambda k: sum(v.get(k, 0) for g in graphs for v in g["vertices"] if v["status"] != "interrupted")
    intr = sum(1 for g in graphs for v in g["vertices"] if v["status"] == "interrupted")
    dep = {k: sum(v["depth"][k] for g in graphs for v in g["vertices"] if "depth" in v) for k in ("1", "2", "3", ">3")}
    print("order", a.order, "graphs", len(graphs), "states", tot("states"), "no_legal_fan", tot("no_legal_fan"),
          "sep_bad", tot("sep_bad"), "depth", dep, "d1_kills", tot("d1_kills"), "p_kills", tot("p_kills"),
          "p_capped", tot("p_capped"), "locked", tot("locked_classes"), "interrupted_vertices", intr,
          f"{time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
