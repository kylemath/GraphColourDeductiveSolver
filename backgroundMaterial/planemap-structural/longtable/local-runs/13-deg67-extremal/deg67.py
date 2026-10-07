#!/usr/bin/env python3
"""[exploratory] Intern D cycle-6 requests (interns-2026-10-06/intern-D-cycle6.md, "Studio requests") on the two extremal
classes of item 6: degree 6, order 24 gentri 71 hole 12 (fraction 1/8); degree 7, order 23 gentri 189 hole 14 (2/17).
Link x_0..x_{d-1} in rotation order. Colours 0..3 are read as elements of Z2^2, so the Tait colour of link edge x_t x_{t+1} is
c(x_t) XOR c(x_{t+1}) in {1,2,3}. The Tait type is the sorted triple of counts (n1,n2,n3).
Degree-6 names (Intern D, section 1; dihedral classes of the link word):
  filled: ABABAB = (6,0,0); (3,2,1) = (4,2,0) with the two minor edges adjacent; (2,2,2) = the (2,2,2)-type 3-colour links;
  unfilled: T1 = abab st (minor edges at distance 2), T4 = asabtb (distance 3), T5 = absabt, T2 = the other (2,2,2)-type
  4-colour word with colour counts (2,2,1,1), (3,1,1,1) = one colour three times.
  The names are checked against Intern D's colouring counts over all proper 4-colourings of C6: ABABAB 12, (3,2,1) 144,
  (2,2,2) 96, T1 144, T4 72, T2 144, T5 72, (3,1,1,1) 48.
Degree 7: Tait type plus the colour-count multiset of the link (filled = <= 3 colours).
Rotation graph (operational analogue of Gamma): on the unfilled states of the class, join s and t when one Kempe swap takes s
to t and changes the link word up to renaming (pattern-changing swaps between unfilled states). Fill moves of a state = its
distinct filled neighbours. Reported: link-type histogram, per type the mean and distribution of fill moves and rotation
degree, rotation-graph components (count, size histogram, degree histogram), and whether ABABAB occurs.
usage: deg67.py > deg67-results.json"""
import itertools, json, os, sys
from collections import Counter, deque
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import Space, gentri_rotation, adj_from_rot
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri")


def canon_word(w):
    mp = {}; return tuple(mp.setdefault(x, len(mp)) for x in w)


def dihedral_canon(w):
    d = len(w); best = None
    for r in range(d):
        for sgn in (1, -1):
            v = canon_word([w[(r + sgn * t) % d] for t in range(d)])
            if best is None or v < best: best = v
    return best


def tait(w):
    d = len(w); c = Counter(w[t] ^ w[(t + 1) % d] for t in range(d)); return tuple(sorted((c[1], c[2], c[3]), reverse=True))


def name6(w):
    t = tait(w); cc = sorted(Counter(w).values(), reverse=True); filled = len(set(w)) <= 3
    if t == (6, 0, 0): return "ABABAB"
    if t == (4, 2, 0):
        minor = [i for i in range(6) if (w[i] ^ w[(i + 1) % 6]) == min((x for x in (1, 2, 3)), key=lambda z: sum(1 for i in range(6) if (w[i] ^ w[(i + 1) % 6]) == z) if sum(1 for i in range(6) if (w[i] ^ w[(i + 1) % 6]) == z) else 99)]
        dist = min((minor[1] - minor[0]) % 6, (minor[0] - minor[1]) % 6)
        return {1: "(3,2,1)", 2: "T1", 3: "T4"}[dist]
    if filled: return "(2,2,2)"
    if cc == [3, 1, 1, 1]: return "(3,1,1,1)"
    dc = dihedral_canon(w)
    return "T5" if dc == dihedral_canon((0, 1, 2, 0, 1, 3)) else "T2"


def name_generic(w):
    return "tait%s_counts%s_%s" % ("".join(map(str, tait(w))), "".join(map(str, sorted(Counter(w).values(), reverse=True))),
                                   "filled" if len(set(w)) <= 3 else "unfilled")


def selfcheck6():
    cnt = Counter()
    for w in itertools.product(range(4), repeat=6):
        if all(w[i] != w[(i + 1) % 6] for i in range(6)): cnt[name6(w)] += 1
    return dict(cnt)


def run(order, gi, hole, frac):
    line = [x for x in open(os.path.join(GENTRI, "tri%d.txt" % order)) if x.strip()][gi]
    rot = gentri_rotation(line); S = Space(adj_from_rot(rot), hole, link=rot[hole]); S.build_graph(); cl, ncl = S.classes()
    d = len(rot[hole]); L = S.linki
    filled = [S.filled(k) for k in range(len(S.states))]
    sizes = Counter(cl); target = [k for k in sizes if 0 < sizes[k] and sum(filled[s] for s in range(len(S.states)) if cl[s] == k) * frac[1] == sizes[k] * frac[0]]
    k0 = min(target, key=lambda k: sizes[k]) if target else None
    C = [s for s in range(len(S.states)) if cl[s] == k0]
    word = {s: tuple(S.states[s][i] for i in L) for s in C}
    name = {s: (name6(word[s]) if d == 6 else name_generic(word[s])) for s in C}
    pat = {s: canon_word(word[s]) for s in C}
    fillm = {s: sum(1 for t in S.G[s] if filled[t]) for s in C}
    rotn = {s: sorted(t for t in S.G[s] if not filled[s] and not filled[t] and pat[t] != pat[s]) for s in C}
    types = Counter(name.values())
    per = {}
    for ty in types:
        ss = [s for s in C if name[s] == ty]
        per[ty] = {"count": len(ss), "fill_moves_hist": dict(sorted(Counter(fillm[s] for s in ss).items())),
                   "rotation_degree_hist": dict(sorted(Counter(len(rotn[s]) for s in ss).items())) if not filled[ss[0]] else None,
                   "unfilled_neighbours_hist": dict(sorted(Counter(sum(1 for t in S.G[s] if not filled[t]) for s in ss).items())) if filled[ss[0]] else None}
    U = [s for s in C if not filled[s]]; seen = set(); comps = []
    for s in U:
        if s in seen: continue
        comp = [s]; seen.add(s); q = deque([s])
        while q:
            x = q.popleft()
            for t in rotn[x]:
                if t not in seen: seen.add(t); comp.append(t); q.append(t)
        comps.append(comp)
    comp_summary = Counter()
    for comp in comps:
        comp_summary[(len(comp), tuple(sorted(Counter(len(rotn[s]) for s in comp).items())), sum(1 for s in comp if fillm[s] > 0))] += 1
    return {"order": order, "gentri_index": gi, "hole": hole, "degree": d, "class_size": len(C), "filled": sum(filled[s] for s in C),
            "fraction": "%d/%d" % (sum(filled[s] for s in C), len(C)), "link_type_hist": dict(sorted(types.items())), "per_type": per,
            "ABABAB_present": types.get("ABABAB", 0) > 0 if d == 6 else None,
            "rotation_graph": {"unfilled_states": len(U), "components": len(comps), "component_size_hist": dict(sorted(Counter(len(c) for c in comps).items())),
                               "degree_hist": dict(sorted(Counter(len(rotn[s]) for s in U).items())),
                               "edges": sum(len(rotn[s]) for s in U) // 2,
                               "components_by_(size, degree multiset, #nodes with a fill move)": [[list(k[0:1]) + [dict(k[1]), k[2]], v] for k, v in sorted(comp_summary.items())]}}


if __name__ == "__main__":
    print(json.dumps({"selfcheck_C6_colouring_counts": selfcheck6(),
                      "deg6": run(24, 71, 12, (1, 8)), "deg7": run(23, 189, 14, (2, 17))}, indent=1))
