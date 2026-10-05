"""Iterated alpha-swaps versus fill length, on every gap start (orders 12-22, graphs already in
wp18-P1..P4.json). Exploratory, after the fact.

At a state with hole h and link a0 b a2 g d (4 colours), the four "alpha-swaps" are the swaps
of the alpha-gamma component and the alpha-delta component at each alpha link vertex:
   ag@a0, ad@a2 (Kempe's two swaps, forced to miss g resp. d in the gap case),
   ad@a0 (component contains d), ag@a2 (component contains g).
f(s) = 0 if the link has <= 3 colours; 1 if not gap; else 1 + min over the four alpha-swaps
of f(result) (hole fixed; cap 6). f is an upper bound on kappa (pure-Kempe length) >= l.
Also records, for the l >= 3 starts, local features: degrees around v, and the sizes of the
four alpha-components. Writes mechanism-iter.txt and mechanism-iter-long.json.
"""
import json
import sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from wp18_core import deletion_states, filled, legal_fans, parse_ascii, shortest_fill  # noqa: E402
from mechanism_classify import comp  # noqa: E402
from mechanism_kempe import is_gap, kempe_only, roles_inv, swap  # noqa: E402


def alpha_swaps(rot, st):
    p0, p1, p2, p3, p4, cn = roles_inv(rot, st)
    a, g, d = cn["a"], cn["g"], cn["d"]
    return [swap(rot, st, p0, a, g), swap(rot, st, p2, a, d), swap(rot, st, p0, a, d), swap(rot, st, p2, a, g)]


def f(rot, st, cap=6):
    if filled(rot, st):
        return 0
    if not is_gap(rot, st):
        return 1
    if cap <= 1:
        return None
    best = None
    for y in alpha_swaps(rot, st):
        r = f(rot, y, cap - 1)
        if r is not None and (best is None or r + 1 < best):
            best = r + 1
    return best


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
                l, _ = shortest_fill(rot, s, 6)
                fv = f(rot, s, 6 if l >= 3 else 3)
                agg[(l, fv)] += 1
                if l >= 3:
                    p0, p1, p2, p3, p4, cn = roles_inv(rot, s)
                    a, b, g, d = cn["a"], cn["b"], cn["g"], cn["d"]
                    long.append({
                        "order": order, "graph": idx, "v": v, "l": l, "f": fv,
                        "kappa": kempe_only(rot, s),
                        "deg_link": [len(rot[x]) for x in (p0, p1, p2, p3, p4)],
                        "comp_sizes": {"ag@a0": len(comp(rot, s, p0, a, g)), "ad@a2": len(comp(rot, s, p2, a, d)),
                                       "bg@b": len(comp(rot, s, p1, b, g)), "bd@b": len(comp(rot, s, p1, b, d))},
                        "max_deg": max(len(r) for r in rot), "start": list(s)})
    return [[list(k), c] for k, c in agg.items()], long


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
    lines = ["Gap starts: fill length l versus iterated alpha-swap depth f (None = above cap)", ""]
    for k in sorted(agg, key=str):
        lines.append(f"  l={k[0]} f={k[1]}: {agg[k]}")
    (HERE / "mechanism-iter.txt").write_text("\n".join(lines) + "\n")
    json.dump(long, open(HERE / "mechanism-iter-long.json", "w"), separators=(",", ":"))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
