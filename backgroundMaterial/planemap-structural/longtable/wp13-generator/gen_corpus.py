"""WP13: build corpus.json of minimum-degree-five spherical triangulations of orders 21-60
(plus Goldberg-Coxeter icosahedral classes up to order 72).

Families
  gc            GC(a,b) geodesic icosahedra (a,b) in {(1,1),(2,0),(2,1)}: n = 32, 42, 72.
  gc-perturbed  GC(1,1), GC(2,0) after a few random admissible flips.
  uniform       seed (Plantri corpus graph, order 14-20) -> random vertex splits up to n,
                interleaved with unbiased random admissible flips (no energy).
  iso           as uniform but Metropolis/annealed flips rewarding degree-5 roots of type (0,5,0)
                (and more weakly (0,b,c)), mild penalty on degrees >= 8.
  near          annealed flips rewarding root types (1,4,0), (0,4,1), (1,3,1), (0,3,2).
  high          annealed flips rewarding a few vertices of degree 7/8 and roots with a degree>=7
                neighbour and no degree-5 neighbour; penalty on degrees >= 9.
  fullerene     annealed flips with heavy penalty on degrees >= 7 and reward for isolated roots
                (targets duals of isolated-pentagon fullerenes).
Random choices come from random.Random(seed) with seed recorded per graph.  Sampling is NOT
uniform over isomorphism classes.
"""
import json
import math
import random
import sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from trimap import (check_triangulation, flip, flip_ok, split, root_type, degree_five,
                    canonical_code, relabel_canonical, parse_ascii, to_ascii)
from goldberg import goldberg_coxeter

CORPUS_DIR = HERE.parent.parent
SEEDS = []
for m in range(14, 21):
    p = CORPUS_DIR / f"triangulations-min5-{m}.txt"
    SEEDS += [ln for ln in p.read_text().split("\n") if ln.strip()]

# ---------------------------------------------------------------- energies (higher = better)

FAMILIES = {
    "uniform": None,
    "iso": dict(types={(0, 5, 0): 3.0, (0, 4, 1): 1.0, (0, 3, 2): 0.8},
                deg=lambda d: -0.7 * max(0, d - 7)),
    "near": dict(types={(1, 4, 0): 2.0, (0, 4, 1): 2.0, (1, 3, 1): 1.5, (0, 3, 2): 1.2,
                        (0, 5, 0): 0.8},
                 deg=lambda d: -0.7 * max(0, d - 8)),
    "high": dict(types={(0, 4, 1): 2.0, (0, 3, 2): 2.0, (1, 3, 1): 1.2, (0, 2, 3): 1.5},
                 deg=lambda d: (1.0 if d in (7, 8) else 0.0) - 1.5 * max(0, d - 8)),
    "fullerene": dict(types={(0, 5, 0): 2.5},
                      deg=lambda d: -4.0 * max(0, d - 6)),
}


def vscore(rot, v, spec):
    d = len(rot[v])
    s = spec["deg"](d)
    if d == 5:
        s += spec["types"].get(root_type(rot, v), 0.0)
    return s


def local_set(rot, vs):
    S = set(vs)
    for v in vs:
        S.update(rot[v])
    return S


def anneal(rot, rng, spec, steps, t0, t1):
    n = len(rot)
    for s in range(steps):
        u = rng.randrange(n)
        v = rng.choice(rot[u])
        xy = flip_ok(rot, u, v)
        if not xy:
            continue
        if spec is None:
            flip(rot, u, v, xy)
            continue
        T = t0 * (t1 / t0) ** (s / max(1, steps - 1))
        x, y = xy
        S = local_set(rot, (u, v, x, y))
        before = sum(vscore(rot, w, spec) for w in S)
        flip(rot, u, v, xy)
        after = sum(vscore(rot, w, spec) for w in S)
        dE = after - before
        if dE < 0 and rng.random() >= math.exp(dE / T):
            flip(rot, x, y)  # undo (x, y now degree >= 6, u, v non-adjacent)
    return rot


def grow(n, family, seed):
    rng = random.Random(seed)
    spec = FAMILIES[family]
    rot = parse_ascii(rng.choice(SEEDS))
    while len(rot) < n:
        big = [v for v in range(len(rot)) if len(rot[v]) >= 6]
        v = rng.choice(big)
        d = len(rot[v])
        split(rot, v, rng.randrange(d), rng.randint(3, d - 3))
        anneal(rot, rng, spec, 4 * len(rot), 1.5, 0.5)
    E = 3 * n - 6
    anneal(rot, rng, spec, 250 * E, 2.0, 0.05)
    check_triangulation(rot)
    return rot


def perturb(rot, k, seed):
    rng = random.Random(seed)
    rot = [list(x) for x in rot]
    done = 0
    while done < k:
        u = rng.randrange(len(rot))
        v = rng.choice(rot[u])
        xy = flip_ok(rot, u, v)
        if xy:
            flip(rot, u, v, xy)
            done += 1
    check_triangulation(rot)
    return rot


def job(args):
    n, family, seed = args
    rot = grow(n, family, seed)
    rot = relabel_canonical(rot)
    return n, family, seed, rot, canonical_code(rot)


def describe(gid, family, rot, provenance):
    check_triangulation(rot)
    degs = [len(x) for x in rot]
    roots = degree_five(rot)
    types = {r: root_type(rot, r) for r in roots}
    return {
        "id": gid,
        "family": family,
        "order": len(rot),
        "provenance": provenance,
        "rotation": rot,
        "ascii": to_ascii(rot),
        "degree_counts": {str(d): c for d, c in sorted(Counter(degs).items())},
        "max_degree": max(degs),
        "degree_five_roots": roots,
        "root_types": [{"root": r, "n5": t[0], "n6": t[1], "n7plus": t[2]} for r, t in types.items()],
        "root_type_counts": {f"({a},{b},{c})": k for (a, b, c), k in sorted(Counter(types.values()).items())},
        "isolated_roots": [r for r in roots if types[r][0] == 0],
    }


def main():
    out, seen = [], {}

    def add(family, rot, prov):
        key = canonical_code(rot)
        if key in seen:
            seen[key]["also_generated_by"] = seen[key].get("also_generated_by", []) + [prov]
            return False
        gid = f"wp13-n{len(rot):02d}-{family}-{sum(1 for g in out if g['order'] == len(rot) and g['family'] == family)}"
        g = describe(gid, family, rot, prov)
        seen[key] = g
        out.append(g)
        return True

    for a, b in [(1, 1), (2, 0), (2, 1)]:
        add("gc", relabel_canonical(goldberg_coxeter(a, b)), {"construction": f"GC({a},{b})"})
    for a, b in [(1, 1), (2, 0)]:
        base = goldberg_coxeter(a, b)
        for k, seed in [(1, 1), (2, 2), (3, 3), (5, 4)]:
            add("gc-perturbed", relabel_canonical(perturb(base, k, seed)),
                {"construction": f"GC({a},{b}) + {k} random admissible flips", "seed": seed})

    fams = ["uniform", "iso", "near", "high", "fullerene"]
    want = {(n, f): 1 for n in range(21, 61) for f in fams}
    for n in range(21, 61, 3):  # extra iso / near samples on every third order
        want[(n, "iso")] += 1
        want[(n, "near")] += 1
    for n in range(21, 32):  # small orders: isolated roots are rarer, sample iso twice more
        want[(n, "iso")] += 2
    got = Counter()
    base_seed = 13_000
    with Pool() as pool:
        for rnd in range(4):
            tasks = []
            for (n, f), k in sorted(want.items()):
                for j in range(k - got[(n, f)]):
                    tasks.append((n, f, base_seed + 1000 * rnd + 37 * n + 7 * fams.index(f) + j))
            if not tasks:
                break
            for n, f, seed, rot, key in pool.imap(job, tasks, chunksize=2):
                prov = {"construction": "seed split-growth + flip chain", "seed": seed,
                        "seed_pool": "triangulations-min5-14..20.txt"}
                if add(f, rot, prov):
                    got[(n, f)] += 1
            print("round", rnd, "graphs", len(out), file=sys.stderr)

    out.sort(key=lambda g: (g["order"], g["family"], g["id"]))
    stats = summary(out)
    doc = {
        "scope": "WP13 generated corpus of simple spherical triangulations with minimum degree 5, "
                 "orders 21-60 plus Goldberg-Coxeter GC(2,1) of order 72. Facts about the graphs only.",
        "format": {
            "rotation": "list of n lists; rotation[v] is the cyclic neighbour list of vertex v (0-indexed). "
                        "Face convention as longtable/mass_core.validate_triangulation: dart (a,b) -> (b, succ_b(a)). "
                        "Equivalent to plantri ASCII with letter chr(97+v); the ASCII form cannot express n > 26, "
                        "so 'ascii' is null for n > 26 and the JSON rotation is authoritative.",
            "root_types": "for each degree-5 vertex r: n5, n6, n7plus = numbers of neighbours of degree 5, 6, >=7",
            "isomorphism": "no two entries are isomorphic as plane maps up to reflection (canonical BFS code)",
        },
        "generator_files": ["trimap.py", "goldberg.py", "gen_corpus.py"],
        "summary": stats,
        "graphs": out,
    }
    (HERE / "corpus.json").write_text(json.dumps(doc, indent=1))
    print(json.dumps(stats, indent=1))


def summary(out):
    tc = Counter()
    graphs_with = Counter()
    by_order = {}
    for g in out:
        for k, v in g["root_type_counts"].items():
            tc[k] += v
            graphs_with[k] += 1
        o = by_order.setdefault(g["order"], {"graphs": 0, "families": Counter(), "isolated_roots": 0,
                                              "graphs_with_isolated_root": 0, "max_degree": 0})
        o["graphs"] += 1
        o["families"][g["family"]] += 1
        o["isolated_roots"] += len(g["isolated_roots"])
        o["graphs_with_isolated_root"] += bool(g["isolated_roots"])
        o["max_degree"] = max(o["max_degree"], g["max_degree"])
    return {
        "graphs": len(out),
        "orders": [min(g["order"] for g in out), max(g["order"] for g in out)],
        "families": dict(Counter(g["family"] for g in out)),
        "degree_five_roots": sum(len(g["degree_five_roots"]) for g in out),
        "root_type_totals": dict(sorted(tc.items(), key=lambda kv: -kv[1])),
        "graphs_containing_root_type": dict(sorted(graphs_with.items(), key=lambda kv: -kv[1])),
        "graphs_with_isolated_root": sum(1 for g in out if g["isolated_roots"]),
        "graphs_with_degree_ge7": sum(1 for g in out if g["max_degree"] >= 7),
        "max_degree_histogram": dict(sorted(Counter(g["max_degree"] for g in out).items())),
        "by_order": {str(k): {**v, "families": dict(v["families"])} for k, v in sorted(by_order.items())},
    }


if __name__ == "__main__":
    main()
