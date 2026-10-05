"""Kempe-component signature of gap starts by fill length (orders 12-22, graphs already in
wp18-P1..P4.json; exploratory, after the fact).

For a gap start with link a0 b a2 g d, count the bichromatic components (in T - h) of each of
the six colour pairs, and record deg(b), deg of the other link vertices. Signature
ncomp = (ab, ag, ad, bg, bd, gd) with g/d merged by mirror (ag<->ad, bg<->bd).
Writes mechanism-features.txt.
"""
import json
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from wp18_core import HOLE, deletion_states, filled, legal_fans, parse_ascii, shortest_fill  # noqa: E402
from mechanism_kempe import is_gap, roles_inv  # noqa: E402


def ncomp(rot, st, a, b):
    seen = set()
    k = 0
    for s, c in enumerate(st):
        if c in (a, b) and s not in seen:
            k += 1
            stack = [s]
            seen.add(s)
            while stack:
                x = stack.pop()
                for y in rot[x]:
                    if y not in seen and st[y] in (a, b):
                        seen.add(y)
                        stack.append(y)
    return k


def work(args):
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
                l, _ = shortest_fill(rot, s, 6)
                p0, p1, p2, p3, p4, cn = roles_inv(rot, s)
                a, b, g, d = cn["a"], cn["b"], cn["g"], cn["d"]
                sig = (ncomp(rot, s, a, b), ncomp(rot, s, a, g), ncomp(rot, s, a, d),
                       ncomp(rot, s, b, g), ncomp(rot, s, b, d), ncomp(rot, s, g, d))
                mir = (sig[0], sig[2], sig[1], sig[4], sig[3], sig[5])
                sig = min(sig, mir)
                agg[("n", l)] += 1
                agg[("degb", l, len(rot[p1]))] += 1
                agg[("bgbd_connected", l, sig[3] == 1 and sig[4] == 1)] += 1
                agg[("ones", l, sum(x == 1 for x in sig))] += 1
                agg[("sig", l, sig)] += 1
                pop = sorted(Counter(c for c in s if c != HOLE).values())
                agg[("pop", l, tuple(pop))] += 1
    return [[list(k), c] for k, c in agg.items()]


def main():
    jobs = []
    for ph in ("P1", "P2", "P3", "P4"):
        d = json.loads((HERE / f"wp18-{ph}.json").read_text())
        jobs += [(g["order"], g["graph_index"], g["ascii"]) for g in d["graphs"]]
    with Pool(12) as pool:
        res = pool.map(work, jobs, chunksize=4)
    agg = Counter()
    for a_ in res:
        for k, c in a_:
            agg[tuple(tuple(x) if isinstance(x, list) else x for x in k)] += c
    lines = ["Gap-start features by fill length l (distinct starts)", ""]
    for l in (2, 3, 4):
        n = agg[("n", l)]
        lines.append(f"l = {l}: {n} starts")
        for key in ("degb", "bgbd_connected", "ones"):
            row = sorted(((k[2], c) for k, c in agg.items() if k[0] == key and k[1] == l), key=str)
            lines.append(f"  {key}: " + ", ".join(f"{x}: {c} ({100*c/n:.1f}%)" for x, c in row))
        sigs = sorted(((k[2], c) for k, c in agg.items() if k[0] == "sig" and k[1] == l), key=lambda t: -t[1])
        lines.append("  top component signatures (ab,ag,ad,bg,bd,gd): " +
                     "; ".join(f"{s}: {c}" for s, c in sigs[:8]))
        pops = sorted(((k[2], c) for k, c in agg.items() if k[0] == "pop" and k[1] == l), key=lambda t: -t[1])
        lines.append("  top populations: " + "; ".join(f"{s}: {c}" for s, c in pops[:6]))
        lines.append("")
    (HERE / "mechanism-features.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
