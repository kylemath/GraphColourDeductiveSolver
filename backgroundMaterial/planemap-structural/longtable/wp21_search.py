"""WP21 phase B driver: adversarial edge-flip search for D1 / P counterexamples.

Declaration: WP21-declaration.md. Evaluates graphs with the WP20 producer's analyse_graph
(d1_confirm.py, unchanged, hashed). Each chain is simulated annealing over minimum-degree-5
triangulations of one fixed order, using only edge flips that keep minimum degree 5.

  python3 wp21_search.py --seeds SEEDS.txt --out-prefix wp21/B --chains K --steps S
        --seed-tag WP21 [--cpu-seconds C] [--workers W]

SEEDS.txt: plantri-ascii lines (one per chain, cycled).  Writes OUT-prefix-evaluated.txt (every
evaluated graph, one plantri-ascii line each, indexed by line number), OUT-prefix.json (producer
format over those lines) and OUT-prefix-log.json (objective trace).  Deterministic given seeds.
"""
import argparse
import hashlib
import json
import math
import os
import random
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d1_confirm as P  # the hashed WP20 producer, unchanged


def parse(line):
    n, body = line.split()
    rot = [[ord(c) - 97 for c in r] for r in body.split(",")]
    assert len(rot) == int(n)
    return rot


def to_ascii(rot):
    return str(len(rot)) + " " + ",".join("".join(chr(97 + w) for w in r) for r in rot)


def flippable(rot):
    """Edges uv (u<v) whose flip keeps a simple triangulation of minimum degree 5."""
    adj = [set(r) for r in rot]
    out = []
    for u in range(len(rot)):
        if len(rot[u]) < 6:
            continue
        for i, v in enumerate(rot[u]):
            if v < u or len(rot[v]) < 6:
                continue
            d = len(rot[u])
            x = rot[u][(i - 1) % d]
            y = rot[u][(i + 1) % d]
            if x != y and y not in adj[x]:
                out.append((u, v))
    return out


def flip(rot, u, v):
    """Return a new rotation system with edge uv flipped to xy (faces uvx and uvy)."""
    rot = [list(r) for r in rot]
    i = rot[u].index(v)
    d = len(rot[u])
    x = rot[u][(i - 1) % d]
    y = rot[u][(i + 1) % d]
    rot[u].remove(v)
    rot[v].remove(u)
    for a, b, c in ((x, u, v), (y, v, u)):
        # insert the new neighbour between b and c in rot[a]
        j = rot[a].index(b)
        k = rot[a].index(c)
        m = len(rot[a])
        if (j + 1) % m == k:
            pos = k
        else:
            assert (k + 1) % m == j
            pos = j
        rot[a].insert(pos, y if a == x else x)
    return rot


def valid(rot):
    """Independent sanity check: simple, consistent triangulation, minimum degree 5, Euler."""
    n = len(rot)
    adj = [set(r) for r in rot]
    if any(len(adj[v]) != len(rot[v]) or v in adj[v] for v in range(n)):
        return False
    if any(len(rot[v]) < 5 for v in range(n)):
        return False
    if any(v not in adj[w] for v in range(n) for w in rot[v]):
        return False
    E = sum(len(r) for r in rot) // 2
    if E != 3 * n - 6:
        return False
    for v in range(n):
        d = len(rot[v])
        if any(rot[v][(i + 1) % d] not in adj[rot[v][i]] for i in range(d)):
            return False
    # face tracing: every directed edge in exactly one face; all faces triangles; F = 2n - 4
    seen = set()
    faces = 0
    for u in range(n):
        for v in rot[u]:
            if (u, v) in seen:
                continue
            a_, b_ = u, v
            length = 0
            while (a_, b_) not in seen:
                seen.add((a_, b_))
                length += 1
                d = len(rot[b_])
                c_ = rot[b_][(rot[b_].index(a_) + 1) % d]
                a_, b_ = b_, c_
            if length != 3:
                return False
            faces += 1
    return faces == 2 * n - 4


def objective(rec):
    s = 0
    for v in rec["vertices"]:
        if v["status"] == "interrupted":
            continue
        s += 1000 * (v["d1_kills"] + v["p_kills"] + v["depth"].get("2", 0) + v["depth"].get("3", 0)
                     + v["depth"].get(">3", 0))
        s += 20 * v["sep_bad"] + v["locked_classes"]
    return s


def chain(args):
    cid, seed_line, steps, tag, cpu_cap = args
    rng = random.Random(int(hashlib.sha256(f"{tag}-chain-{cid}".encode()).hexdigest()[:12], 16))
    rot = parse(seed_line)
    assert valid(rot)
    t0 = time.process_time()
    evaluated = []   # (ascii, record, witnesses, accepted flag, objective)

    def evaluate(r):
        line = to_ascii(r)
        rec, wit = P.analyse_graph((len(evaluated), line))
        evaluated.append([line, rec, wit, False, objective(rec)])
        return evaluated[-1][4]

    cur = evaluate(rot)
    evaluated[-1][3] = True
    best = cur
    temp0 = max(10.0, 0.5 * cur)
    for step in range(1, steps + 1):
        if time.process_time() - t0 > cpu_cap:
            break
        cand = flippable(rot)
        if not cand:
            break
        u, v = rng.choice(cand)
        new = flip(rot, u, v)
        assert valid(new)
        val = evaluate(new)
        temp = temp0 * (1 - step / (steps + 1)) + 1e-9
        if val >= cur or rng.random() < math.exp((val - cur) / temp):
            rot, cur = new, val
            evaluated[-1][3] = True
        best = max(best, cur)
    return cid, evaluated, best, time.process_time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", required=True)
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--chains", type=int, default=12)
    ap.add_argument("--steps", type=int, default=100)
    ap.add_argument("--seed-tag", default="WP21")
    ap.add_argument("--cpu-seconds", type=float, default=1e12, help="per-chain CPU cap")
    ap.add_argument("--workers", type=int, default=12)
    a = ap.parse_args()
    seeds = [l.strip() for l in open(a.seeds) if l.strip()]
    jobs = [(c, seeds[c % len(seeds)], a.steps, a.seed_tag, a.cpu_seconds) for c in range(a.chains)]
    results = []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(chain, jobs):
            results.append(r)
            print("chain", r[0], "evaluated", len(r[1]), "best", r[2], f"{r[3]:.0f}s", flush=True)
    results.sort(key=lambda r: r[0])
    lines, graphs, wit = [], [], {"sep_bad": [], "d1_kills": [], "p_kills": []}
    log = []
    for cid, evaluated, best, secs in results:
        for step, (line, rec, w, acc, obj) in enumerate(evaluated):
            idx = len(lines)
            lines.append(line)
            rec = dict(rec)
            rec["index"] = idx
            graphs.append(rec)
            for k in wit:
                for item in w[k]:
                    item = dict(item)
                    item["index"] = idx
                    wit[k].append(item)
            log.append({"chain": cid, "step": step, "index": idx, "objective": obj, "accepted": acc})
    open(a.out_prefix + "-evaluated.txt", "w").write("\n".join(lines) + "\n")
    raw = open(a.out_prefix + "-evaluated.txt", "rb").read()
    out = {"wp": "WP21", "phase": "B", "order": parse(lines[0]).__len__(),
           "declaration_sha256": "", "input_sha256": hashlib.sha256(raw).hexdigest(),
           "producer_sha256": {"d1_confirm.py": P.sha(os.path.join(os.path.dirname(os.path.abspath(__file__)), "d1_confirm.py")),
                               "wp21_search.py": P.sha(os.path.abspath(__file__))},
           "graphs": graphs, "witnesses": wit, "truncated": False}
    decl = os.path.join(os.path.dirname(os.path.abspath(__file__)), "WP21-declaration.md")
    if os.path.exists(decl):
        out["declaration_sha256"] = P.sha(decl)
    json.dump(out, open(a.out_prefix + ".json", "w"))
    json.dump({"seed_tag": a.seed_tag, "chains": a.chains, "steps": a.steps, "log": log,
               "best": {r[0]: r[2] for r in results}}, open(a.out_prefix + "-log.json", "w"))
    tot = lambda k: sum(v.get(k, 0) for g in graphs for v in g["vertices"] if v["status"] != "interrupted")
    print("evaluated graphs", len(lines), "sep_bad", tot("sep_bad"), "d1_kills", tot("d1_kills"),
          "p_kills", tot("p_kills"), "locked", tot("locked_classes"),
          "max chain objective", max(r[2] for r in results))


if __name__ == "__main__":
    main()
