import json
from collections import Counter, defaultdict
R = json.load(open("kempe-distance-results.json"))
eccA = Counter(); eccB = Counter(); unrB = 0; rootsB_unr = []
kc = Counter(); cwt = Counter(); minecc = Counter(); hist = Counter()
bytype = defaultdict(Counter); badecc = []
for g in R:
    m = min(r["all"]["ecc"] for r in g["roots"])
    minecc[m] += 1
    for r in g["roots"]:
        eccA[r["all"]["ecc"]] += 1; eccB[r["Bonly"]["ecc"]] += 1
        if r["Bonly"]["unreachable"]:
            unrB += 1; rootsB_unr.append((g["order"], g["graph_index"], r["root"], r["Bonly"]["unreachable"], r["non_target"]))
        kc[r["all"]["kempe_classes"]] += 1
        cwt[r["all"]["classes_without_target"]] += 1
        for d, c in r["all"]["dist_hist"].items(): hist[int(d)] += c
        nd = r["nbr_degrees"]; t = tuple(sorted(nd)); 
        # cyclic type canonical
        cyc = min(tuple(nd[i:]+nd[:i]) for i in range(5)); cyc = min(cyc, min(tuple((nd[::-1])[i:]+(nd[::-1])[:i]) for i in range(5)))
        bytype[cyc][r["all"]["ecc"]] += 1
        if r["root"] in g["q_failing_roots"]:
            badecc.append((g["order"], g["graph_index"], r["root"], cyc, r["all"]["ecc"], r["Bonly"]["ecc"], r["Bonly"]["unreachable"]))
print("ecc(all swaps) over roots:", dict(sorted(eccA.items())))
print("ecc(B-touching swaps only):", dict(sorted(eccB.items(), key=str)))
print("roots with B-only unreachable:", unrB, rootsB_unr[:20])
print("Kempe classes per root (all colourings of T-r):", dict(sorted(kc.items())))
print("classes without any target:", dict(cwt))
print("per graph min ecc:", dict(sorted(minecc.items())))
print("dist histogram of all non-target states:", dict(sorted(hist.items())))
print("by cyclic nbr-degree type -> ecc counts:")
for k in sorted(bytype): print("  ", k, dict(sorted(bytype[k].items())))
print("q-failing roots (order,g,root,type,ecc,eccB,unrB):")
for b in badecc: print("  ", b)
# graphs with min ecc >=3
for g in R:
    m = min(r["all"]["ecc"] for r in g["roots"])
    if m >= 3:
        degs = Counter(len(x) for x in g["ascii"].split()[1].split(","))
        print("min-ecc", m, g["order"], g["graph_index"], dict(degs), [r["all"]["ecc"] for r in g["roots"]])
