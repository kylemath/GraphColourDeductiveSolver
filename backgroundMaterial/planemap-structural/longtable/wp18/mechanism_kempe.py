"""Kempe's classical pair versus the observed fill length, on every gap start (orders 12-22,
graphs already recorded in wp18-P1..P4.json). Exploratory, after the fact.

Link positions 0..4 coloured (a, b, a, g, d), b in the middle. Gap: a bg-path 1~3 and a
bd-path 1~4 both exist in T - h. Kempe's pair:
  KP_g: swap the ag-component of vertex 0, then the ad-component of vertex 2;
  KP_d: swap the ad-component of vertex 2, then the ag-component of vertex 0.
(Each first swap is legal and leaves 4 colours, by the Jordan argument in swarm/fan-link.md.)
Also: kappa = pure-Kempe fill length (hole fixed), BFS cap 6, for every gap start with l >= 3;
a "slide-needed" start is one with kappa > l.
Writes mechanism-kempe.txt and mechanism-kempe-long.json (l >= 3 records).
"""
import json
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from wp18_core import canon, deletion_states, filled, hole_of, legal_fans, moves, parse_ascii, shortest_fill  # noqa: E402
from mechanism_classify import comp, greek  # noqa: E402


def swap(rot, st, s, a, b):
    out = list(st)
    for x in comp(rot, st, s, a, b):
        out[x] = b if st[x] == a else a
    return tuple(out)


def roles_inv(rot, st):
    names, roles = greek(rot, st)
    inv = {}
    for v, r in roles.items():
        inv.setdefault(r, []).append(v)
    cn = {n: c for c, n in names.items()}
    v = hole_of(st)
    L = rot[v]
    b = inv["b"][0]
    j = L.index(b)
    return L[(j - 1) % 5], b, L[(j + 1) % 5], L[(j + 2) % 5], L[(j + 3) % 5], cn


def kempe_pair(rot, st):
    p0, p1, p2, p3, p4, cn = roles_inv(rot, st)
    a, g, d = cn["a"], cn["g"], cn["d"]
    s1 = swap(rot, st, p0, a, g)
    s1 = swap(rot, s1, p2, a, d)
    s2 = swap(rot, st, p2, a, d)
    s2 = swap(rot, s2, p0, a, g)
    return filled(rot, s1), filled(rot, s2)


def kempe_only(rot, start, cap=6):
    if filled(rot, start):
        return 0
    seen = {start}
    fr = [start]
    for d in range(1, cap + 1):
        nx = []
        for x in fr:
            for mv, y in moves(rot, x):
                if mv[0] != "K" or y in seen:
                    continue
                if filled(rot, y):
                    return d
                seen.add(y)
                nx.append(y)
        fr = nx
    return None


def is_gap(rot, st):
    p0, p1, p2, p3, p4, cn = roles_inv(rot, st)
    return (p3 in comp(rot, st, p1, cn["b"], cn["g"])) and (p4 in comp(rot, st, p1, cn["b"], cn["d"]))


def work(args):
    order, idx, ascii_ = args
    rot = parse_ascii(ascii_)
    agg = Counter()
    long = []
    for v in (u for u in range(len(rot)) if len(rot[u]) == 5):
        states = deletion_states(rot, v)
        seen = set()
        for i, c1, c2 in legal_fans(rot, v):
            for s in states:
                if s in seen or s[c1[0]] == s[c1[1]] or s[c2[0]] == s[c2[1]]:
                    continue
                seen.add(s)
                if filled(rot, s) or not is_gap(rot, s):
                    continue
                kg, kd = kempe_pair(rot, s)
                l, _ = shortest_fill(rot, s, 6)
                kp = "both" if kg and kd else ("one" if kg or kd else "none")
                agg[(l, kp)] += 1
                if l >= 3:
                    kap = kempe_only(rot, s)
                    agg[("kappa", l, kap)] += 1
                    long.append({"order": order, "graph": idx, "v": v, "l": l, "kappa": kap,
                                 "kp": kp, "start": list(s)})
    return [[list(k) if isinstance(k, tuple) else k, c] for k, c in agg.items()], long


def main():
    jobs = []
    for ph in ("P1", "P2", "P3", "P4"):
        d = json.loads((HERE / f"wp18-{ph}.json").read_text())
        jobs += [(g["order"], g["graph_index"], g["ascii"]) for g in d["graphs"]]
    with Pool(12) as pool:
        res = pool.map(work, jobs, chunksize=4)
    agg = Counter()
    long = []
    for a_, lg in res:
        for k, c in a_:
            agg[tuple(k)] += c
        long += lg
    lines = ["Kempe's pair (KP) on gap starts, distinct starts per degree-5 vertex, orders 12-22", ""]
    lines.append("l  KP-both  KP-one  KP-none")
    for l in sorted({k[0] for k in agg if k[0] != "kappa"}):
        lines.append(f"{l}  {agg[(l,'both')]}  {agg[(l,'one')]}  {agg[(l,'none')]}")
    lines.append("")
    lines.append("pure-Kempe length kappa for gap starts with l >= 3:")
    for k in sorted((k for k in agg if k[0] == "kappa"), key=str):
        lines.append(f"  l={k[1]} kappa={k[2]}: {agg[k]}")
    (HERE / "mechanism-kempe.txt").write_text("\n".join(lines) + "\n")
    json.dump(long, open(HERE / "mechanism-kempe-long.json", "w"), separators=(",", ":"))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
