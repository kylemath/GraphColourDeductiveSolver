"""Mechanism of short fills at degree-5 fan starts (Long Table, exploratory, after the fact).

Reads only the graphs already recorded in wp18-P1..P4.json (orders 12-22). For every
distinct start (per degree-5 vertex v; a start proper on several fans is analysed once and
tagged with each fan apex) it records:
  * the start link class (3 or 4 colours), the gap flag (both Kempe paths 1-3 (beta-gamma)
    and 1-4 (beta-delta) present), and which single moves fill;
  * the fill length l (BFS, cap 6) and, for l >= 2, the set of move-type words over ALL
    shortest fills, the first-move descriptor, the hole degree sequence and the link
    pattern (degree:sorted colour counts) along each shortest fill.
Writes mechanism-classify.txt (aggregate tables) and mechanism-long.json (all l >= 3 starts).
Usage: python3 mechanism_classify.py [--procs N]
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from wp18_core import HOLE, deletion_states, filled, hole_of, legal_fans, moves, parse_ascii  # noqa: E402

CAP = 6


def link_pattern(rot, st):
    h = hole_of(st)
    c = Counter(st[w] for w in rot[h])
    return f"{len(rot[h])}:" + "".join(str(x) for x in sorted(c.values(), reverse=True))


def greek(rot, st):
    """For a 4-colour degree-5 link: position j of first alpha with alpha at j, j+2.
    Returns dict colour->name and vertex->role (a0,b,a2,g,d) with b the middle."""
    v = hole_of(st)
    L = rot[v]
    cols = [st[w] for w in L]
    for j in range(5):
        if cols[j] == cols[(j + 2) % 5]:
            roles = {L[j]: "a", L[(j + 1) % 5]: "b", L[(j + 2) % 5]: "a",
                     L[(j + 3) % 5]: "g", L[(j + 4) % 5]: "d"}
            names = {cols[j]: "a", cols[(j + 1) % 5]: "b", cols[(j + 3) % 5]: "g", cols[(j + 4) % 5]: "d"}
            return names, roles
    return None, None


def comp(rot, st, s, a, b):
    seen = {s}
    stack = [s]
    while stack:
        x = stack.pop()
        for y in rot[x]:
            if y not in seen and st[y] in (a, b):
                seen.add(y)
                stack.append(y)
    return seen


def gap_flag(rot, st):
    names, roles = greek(rot, st)
    inv = {r: v for v, r in roles.items()}
    cn = {n: c for c, n in names.items()}
    p13 = inv["g"] in comp(rot, st, inv["b"], cn["b"], cn["g"])
    p14 = inv["d"] in comp(rot, st, inv["b"], cn["b"], cn["d"])
    return p13, p14


def first_desc(rot, st, mv):
    names, roles = greek(rot, st)
    if mv[0] == "S":
        return "S" + {"b": "mid", "g": "side", "d": "side"}[roles[mv[1]]]
    pair = "".join(sorted(names[mv[1]] + names[mv[2]]))
    pair = pair.replace("d", "g") if "g" not in pair or "d" not in pair else pair
    return "K" + pair


def analyse(rot, s):
    """BFS with all shortest-path parents; returns l and set of path descriptors."""
    if filled(rot, s):
        return 0, None
    dist = {s: 0}
    info = {s: {("", (len(rot[hole_of(s)]),), (link_pattern(rot, s),), None)}}
    frontier = [s]
    for d in range(1, CAP + 1):
        nxt = []
        for x in frontier:
            for mv, y in moves(rot, x):
                dy = dist.get(y)
                if dy is None:
                    dist[y] = d
                    info[y] = set()
                    nxt.append(y)
                    dy = d
                if dy == d:
                    ypat = link_pattern(rot, y)
                    ydeg = len(rot[hole_of(y)])
                    for w, degs, pats, fd in info[x]:
                        info[y].add((w + mv[0], degs + (ydeg,), pats + (ypat,),
                                     fd if fd is not None else first_desc(rot, s, mv)))
        hits = [y for y in nxt if filled(rot, y)]
        if hits:
            out = set()
            for y in hits:
                out |= info[y]
            return d, out
        frontier = nxt
        if not frontier:
            return None, None
    return None, None


def work(args):
    order, idx, ascii_ = args
    rot = parse_ascii(ascii_)
    agg = Counter()
    long = []
    for v in (u for u in range(len(rot)) if len(rot[u]) == 5):
        states = deletion_states(rot, v)
        apex_of = defaultdict(list)
        for i, c1, c2 in legal_fans(rot, v):
            for s in states:
                if s[c1[0]] != s[c1[1]] and s[c2[0]] != s[c2[1]]:
                    apex_of[s].append(c1[0])
        for s, apices in apex_of.items():
            if filled(rot, s):
                agg[("l", 0)] += len(apices)
                continue
            names, roles = greek(rot, s)
            p13, p14 = gap_flag(rot, s)
            l, paths = analyse(rot, s)
            r = {"l": l, "nfans": len(apices), "gap": p13 and p14,
                 "apex_roles": sorted(roles[a] for a in apices)}
            if l == 1:
                one = set()
                for mv, y in moves(rot, s):
                    if filled(rot, y):
                        one.add(first_desc(rot, s, mv))
                r["one"] = sorted(one)
            if l is not None and l >= 2:
                r["words"] = sorted({p[0] for p in paths})
                r["first"] = sorted({p[3] for p in paths})
                r["degs"] = sorted({p[1] for p in paths})
                r["pats"] = sorted({p[2] for p in paths})
                r["finaldeg"] = sorted({p[1][-1] for p in paths})
                if l >= 3:
                    r.update({"order": order, "graph": idx, "v": v, "start": list(s),
                              "apices": apices, "deg_v_nbrs": [len(rot[w]) for w in rot[v]],
                              "link": rot[v]})
            for role in r["apex_roles"]:
                agg[("l_perfan", r["l"], "gap", r["gap"], "apex", role)] += 1
            # below: one count per distinct start (not per fan)
            agg[("l", r["l"], "gap", r["gap"], "p13", p13, "p14", p14)] += 1
            if l == 1:
                agg[("one", r["gap"], tuple(r["one"]))] += 1
            if l is not None and l >= 2:
                agg[("words", l, tuple(r["words"]))] += 1
                agg[("first", l, tuple(r["first"]))] += 1
                agg[("finaldeg", l, tuple(r["finaldeg"]))] += 1
                for w in r["words"]:
                    agg[("word_any", l, w)] += 1
                for dg in r["degs"]:
                    agg[("degseq", l, dg)] += 1
                for pt in r["pats"]:
                    agg[("patseq", l, pt)] += 1
            if l is not None and l >= 3:
                long.append(r)
    return order, idx, [[list(k), c] for k, c in agg.items()], long


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--procs", type=int, default=12)
    ap.add_argument("--phases", default="P1,P2,P3,P4")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    jobs = []
    for ph in a.phases.split(","):
        d = json.loads((HERE / f"wp18-{ph}.json").read_text())
        for g in d["graphs"]:
            jobs.append((g["order"], g["graph_index"], g["ascii"]))
    with Pool(a.procs) as pool:
        res = pool.map(work, jobs, chunksize=4)
    agg = Counter()
    long = []
    for order, idx, a_, lg in res:
        for k, c in a_:
            agg[tuple(tuple(x) if isinstance(x, list) else x for x in k)] += c
        long += lg
    json.dump({"agg": [[list(k), c] for k, c in sorted(agg.items(), key=str)], "long": long},
              open(HERE / f"mechanism-raw{a.tag}.json", "w"), separators=(",", ":"))
    print("graphs", len(res), "long", len(long))


if __name__ == "__main__":
    main()
