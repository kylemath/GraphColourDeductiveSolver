#!/usr/bin/env python3
"""[UNTESTED] Independent whole-class checker for path 3 (pure Python; imports nothing from kmap/kreach/kempe).
Use it (a) to confirm any KILL-CANDIDATE from run_path3.py, (b) to test whether a rep-level diagnostic is a
class invariant. Practical up to roughly 10^6 states (orders ~30-36 for these families); --max-states aborts.

For T and H = T - v: all proper 4-colourings up to colour renaming (canonical by first occurrence along a BFS
order), Kempe classes by union-find over all whole-component two-colour swaps. Each colouring of T is
restricted to H; an H class is HIT if it contains a restriction (equivalently a filled state). Per H class it
reports: size, hit, filled (independent recount: link of v on <= 3 colours), the SET of odd-parity vectors O
(O_i = #T-odd vertices of colour i, mod 2) seen in the class, the SET of |winding| values of each vertex of
degree >= 7 not adjacent to v, and the SET of link colour counts.

Usage: python3 path3_kclasses.py OUTDIR/NAME.json --hole V|reps|all [--max-states 2000000]
"""
import argparse
import json
import sys
from collections import defaultdict


def bfs_order(adj, start, skip):
    order, seen = [start], {start}
    for x in order:
        for y in sorted(adj[x]):
            if y != skip and y not in seen:
                seen.add(y)
                order.append(y)
    return order


def enumerate_states(adj, order, cap):
    idx = {x: i for i, x in enumerate(order)}
    nb = [[idx[y] for y in adj[x] if y in idx and idx[y] < i] for i, x in enumerate(order)]
    N = len(order)
    out, col = [], [0] * N

    def rec(i, used):
        if i == N:
            out.append(tuple(col))
            if len(out) > cap:
                raise OverflowError
            return
        forb = {col[j] for j in nb[i]}
        for c in range(min(used + 1, 4)):
            if c not in forb:
                col[i] = c
                rec(i + 1, max(used, c + 1))
    sys.setrecursionlimit(10000)
    rec(0, 0)
    return out


def canon(c):
    mp, out = {}, []
    for x in c:
        if x not in mp:
            mp[x] = len(mp)
        out.append(mp[x])
    return tuple(out)


def classes(adj, order, states):
    idx = {x: i for i, x in enumerate(order)}
    nbi = [[idx[y] for y in adj[x] if y in idx] for x in order]
    where = {s: i for i, s in enumerate(states)}
    par = list(range(len(states)))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for si, s in enumerate(states):
        for p in range(4):
            for q in range(p + 1, 4):
                seen = set()
                for st in range(len(s)):
                    if s[st] not in (p, q) or st in seen:
                        continue
                    comp, stack = {st}, [st]
                    while stack:
                        x = stack.pop()
                        for y in nbi[x]:
                            if s[y] in (p, q) and y not in comp:
                                comp.add(y)
                                stack.append(y)
                    seen |= comp
                    t = list(s)
                    for x in comp:
                        t[x] = q if s[x] == p else p
                    ti = where[canon(t)]
                    a, b = find(si), find(ti)
                    if a != b:
                        par[a] = b
    return [find(i) for i in range(len(states))]


def winding(cmap, ring):
    cs = sorted({cmap[x] for x in ring})
    if len(cs) < 3:
        return 0
    pos = {c: i for i, c in enumerate(cs)}
    tot = sum(1 if (pos[cmap[ring[(k + 1) % len(ring)]]] - pos[cmap[ring[k]]]) % 3 == 1 else -1 for k in range(len(ring)))
    return abs(tot) // 3


def analyse_hole(info, v, cap):
    rot = info["rotation"]
    n = len(rot)
    adj = [set(r) for r in rot]
    deg = [len(r) for r in rot]
    start = rot[v][0]
    oT = bfs_order(adj, start, None)
    oH = bfs_order(adj, start, v)
    ST = enumerate_states(adj, oT, cap)
    SH = enumerate_states(adj, oH, cap)
    rT = classes(adj, oT, ST)
    rH = classes(adj, oH, SH)
    whereH = {s: i for i, s in enumerate(SH)}
    posT = {x: i for i, x in enumerate(oT)}
    hit = defaultdict(set)
    for i, s in enumerate(ST):
        h = whereH[canon([s[posT[x]] for x in oH])]
        hit[rH[h]].add(rT[i])
    big = [x for x in range(n) if deg[x] >= 7 and x != v and v not in adj[x]]
    per = defaultdict(lambda: {"size": 0, "filled": 0, "O": set(), "wind": defaultdict(set), "linkc": set()})
    for i, s in enumerate(SH):
        cm = {x: s[k] for k, x in enumerate(oH)}
        d = per[rH[i]]
        d["size"] += 1
        lc = len({cm[y] for y in rot[v]})
        d["linkc"].add(lc)
        d["filled"] += lc <= 3
        d["O"].add(tuple(sum(1 for x in cm if cm[x] == c and deg[x] % 2) % 2 for c in range(4)))
        for x in big:
            d["wind"][x].add(winding(cm, rot[x]))
    out = []
    for r, d in per.items():
        out.append({"size": d["size"], "hit_by_T": r in hit, "T_classes_here": len(hit.get(r, ())),
                    "filled_states": d["filled"], "link_colour_counts": sorted(d["linkc"]),
                    "odd_parity_vectors": sorted(d["O"]), "pole_windings": {str(k): sorted(w) for k, w in d["wind"].items()}})
    return {"name": info["name"], "v": v, "T_states": len(ST), "kT": len(set(rT)), "H_states": len(SH),
            "kH": len(set(rH)), "new_classes": sum(1 for c in out if not c["hit_by_T"]),
            "consistency_hit_iff_filled": all((c["filled_states"] > 0) == c["hit_by_T"] for c in out),
            "classes": sorted(out, key=lambda c: -c["size"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("instance")
    ap.add_argument("--hole", default="reps")
    ap.add_argument("--max-states", type=int, default=2000000)
    a = ap.parse_args()
    info = json.load(open(a.instance))
    deg = [len(r) for r in info["rotation"]]
    if a.hole == "reps":
        holes = [r["v"] for r in info["deg5_orbit_reps"]]
    elif a.hole == "all":
        holes = [x for x in range(info["n"]) if deg[x] == 5]
    else:
        holes = [int(a.hole)]
    for v in holes:
        try:
            print(json.dumps(analyse_hole(info, v, a.max_states)), flush=True)
        except OverflowError:
            print(json.dumps({"name": info["name"], "v": v, "inconclusive": "state cap"}), flush=True)


if __name__ == "__main__":
    main()
