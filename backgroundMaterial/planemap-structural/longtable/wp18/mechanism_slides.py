"""(1) Sanity check of Lemma E on every gap start: if Kempe's pair fails in the order ag@a0 then
ad@a2, the ag-component C0 of a0 contains a gamma vertex of every bg-path from b to g
(tested as: deleting C0's gamma vertices disconnects b from g in the bg-subgraph); mirror for
the other order. (2) The slide-needed starts (kappa > l, from mechanism-kempe-long.json): the
optimal first slides, target role and degree, and the move words. Exploratory, after the fact.
Writes mechanism-slides.txt.
"""
import json
import sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from wp18_core import HOLE, deletion_states, filled, hole_of, legal_fans, moves, parse_ascii, shortest_fill  # noqa: E402
from mechanism_classify import comp  # noqa: E402
from mechanism_kempe import is_gap, roles_inv, swap  # noqa: E402
from mechanism_first import optimal_first  # noqa: E402


def blocked(rot, st, src, dst, a, b, removed):
    seen = {src}
    stack = [src]
    while stack:
        x = stack.pop()
        if x == dst:
            return False
        for y in rot[x]:
            if y not in seen and y not in removed and st[y] in (a, b):
                seen.add(y)
                stack.append(y)
    return True


def lemma_e(args):
    order, idx, ascii_ = args
    rot = parse_ascii(ascii_)
    agg = Counter()
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
                p0, p1, p2, p3, p4, cn = roles_inv(rot, s)
                a, b, g, d = cn["a"], cn["b"], cn["g"], cn["d"]
                C0 = comp(rot, s, p0, a, g)
                D2 = comp(rot, s, p2, a, d)
                xg = blocked(rot, s, p1, p3, b, g, {x for x in C0 if s[x] == g})
                xd = blocked(rot, s, p1, p4, b, d, {x for x in D2 if s[x] == d})
                kg = filled(rot, swap(rot, swap(rot, s, p0, a, g), p2, a, d))
                kd = filled(rot, swap(rot, swap(rot, s, p2, a, d), p0, a, g))
                agg[("KPg_fail_implies_Xg", (not kg) <= xg)] += 1
                agg[("KPd_fail_implies_Xd", (not kd) <= xd)] += 1
                agg[("Xg,KPg", xg, kg)] += 1
    return [[list(k), c] for k, c in agg.items()]


def main():
    jobs = []
    rots = {}
    for ph in ("P1", "P2", "P3", "P4"):
        dd = json.loads((HERE / f"wp18-{ph}.json").read_text())
        for g in dd["graphs"]:
            jobs.append((g["order"], g["graph_index"], g["ascii"]))
            rots[(g["order"], g["graph_index"])] = g["ascii"]
    with Pool(12) as pool:
        res = pool.map(lemma_e, jobs, chunksize=4)
    agg = Counter()
    for a_ in res:
        for k, c in a_:
            agg[tuple(k)] += c
    lines = ["(1) Lemma E check over all gap starts (orders 12-22):"]
    for k in sorted(agg, key=str):
        lines.append(f"  {k}: {agg[k]}")
    lines.append("")
    lines.append("(2) Slide-needed starts (pure-Kempe length kappa > mixed length l):")
    L = json.load(open(HERE / "mechanism-kempe-long.json"))
    need = [r for r in L if r["kappa"] is None or r["kappa"] > r["l"]]
    lines.append(f"  count: {len(need)}; by l: {dict(Counter(r['l'] for r in need))}; "
                 f"kappa - l: {dict(Counter((r['kappa'] or 99) - r['l'] for r in need))}")
    tgt = Counter()
    for r in need:
        rot = parse_ascii(rots[(r["order"], r["graph"])])
        s = tuple(r["start"])
        p0, p1, p2, p3, p4, cn = roles_inv(rot, s)
        roles = {p0: "a0", p1: "b", p2: "a2", p3: "g", p4: "d"}
        l, fm = optimal_first(rot, s)
        kinds = sorted({("S:" + ("b" if roles[m[1]] == "b" else "side") + f"(deg {len(rot[m[1]])})") if m[0] == "S" else "K"
                        for m in fm})
        tgt[tuple(kinds)] += 1
    for k, c in tgt.most_common():
        lines.append(f"    optimal first moves {k}: {c}")
    ex = sorted(need, key=lambda r: (r["order"], r["graph"], r["v"]))[0]
    lines.append(f"  smallest example: order {ex['order']} graph {ex['graph']} v {ex['v']} l {ex['l']} "
                 f"kappa {ex['kappa']} start {ex['start']}")
    (HERE / "mechanism-slides.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
