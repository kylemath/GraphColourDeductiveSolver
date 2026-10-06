"""EXPLORATORY (D1-Hand). For each SEP-bad state and each swap that unlocks, report per admitting fan of
the swapped state c' (apex named by u-index of the ORIGINAL state): first-order broken chain (a chain
{c(y),k} not joining x to y) and separable flag.  Usage: python3 d1hand_fan.py PLANTRI"""
import sys
import tilley_apex as TA, vhphi_explore as E, d1hand_swaps as H

def first_order(adj, c2, x, ring, y):
    """chains {s,k} (k != s=c2[y]) that do NOT join x to y in G=T-xy with x coloured s"""
    s = c2[y]; broken = []
    for k in set(range(4)) - {s}:
        cs, idx = H.comps(adj, c2, {s, k}, x)
        cy = idx[y]
        ok = any(c2[w] == k and idx[w] == cy for w in ring if w != y)
        if not ok: broken.append(k)
    return broken

plantri = sys.argv[1]
for gi in (0, 1):
    rows, rot = H.analyse(plantri, gi)
    adj = [set(r) for r in rot]
    for r in rows:
        x = r["x"]; u = r["u"]; ring = rot[x]; word = r["word(u0..u4)"]
        nm = {word[0]: "D", word[1]: "a", word[3]: "b", word[4]: "g"}
        print(f"\n17:{gi} x={x} u={u} word={''.join(nm[w] for w in word)} split pairs: "
              f"{[''.join(sorted(nm[int(ch)] for ch in k)) for k,v in r['pair_comps'].items() if v>1]}")
        for (pair, size, ur, status, w2, c2, K) in r["swaps"]:
            if not status.startswith("SEP") : continue
            # skip duplicates up to colour symmetry? keep all
            c2 = list(c2)
            seps = status
            out = []
            for i in (1, 3, 4, 0, 2):
                y = u[i]
                if len({c2[w] for w in ring}) == 4 and [c2[w] for w in ring].count(c2[y]) == 1:
                    out.append(f"u{i}:broken{[nm.get(k,'?') for k in first_order(adj,c2,x,ring,y)]}")
            print(f"  swap pair {''.join(nm[p] for p in pair)} K ring u-idx {ur} |K|={size} -> word {''.join(nm.get(w,'?') if False else str(w) for w in w2)} {status}; admitting fans {out}")
