#!/usr/bin/env python3
"""[exploratory] P9-F (Math path 9, MathPath9StuckClass.md section 8), Studio compute implementation (fresh stdlib script).
For a degree-5 hole v of a triangulation T without separating triangles: all 4-colourings of G = T - v up to renaming;
DL as in kempe.cpp / radius.py (link on 4 colours, repeat x_j = x_{j+2}, both locks present); frame index j.
Link moves = swaps of two-colour components that meet the link; silent moves = the others.
Depth sets: D0 = DL; D1 = DL states all of whose link-move images are DL; D1p = D1 with all silent images DL;
D2 = D1 states all of whose link-move images are in D1; Dinf = largest subset of DL closed under link moves.
Pattern key (frame-normalised, x_0 = first vertex of the repeat pair): degrees d_0..d_4 (capped at 8) and the colour words
of R_0..R_4 (neighbours of x_t outside link and v, read in rotation from w_{t-1} to w_t) in letters a (alpha), m (mu), A, B.
Features: "d_t=k", "R_t has c", "R_t starts c", "R_t ends c", "|R_t|=k". Output per hole: sizes of D0, D1, D1p, D2, Dinf.
Aggregate (driver): per-feature counts over D1 and over D2 states, and the features at 100% of D2 but < 100% of D1.
usage: p9f.py --plantri-file FILE N  (all degree-5 holes, one orbit rep each, from ../census/km-N.jsonl) | --faces FILE.json HOLE"""
import itertools, json, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))


def rot_from_faces(F):
    succ = {}
    for a, b, c in F:  # ccw faces: around a, after b comes c (one orientation, consistent)
        succ.setdefault(a, {})[b] = c; succ.setdefault(b, {})[c] = a; succ.setdefault(c, {})[a] = b
    rot = {}
    for v, s in succ.items():
        L = [next(iter(s))]
        while len(L) < len(s): L.append(s[L[-1]])
        rot[v] = L
    return rot


def analyse(rot, hole):
    adj = {v: set(r) for v, r in rot.items()}
    link0 = list(rot[hole])
    V = [u for u in rot if u != hole]; A = {u: adj[u] - {hole} for u in V}
    order, seen = [link0[0]], {link0[0]}
    for x in order:
        for y in sorted(A[x]):
            if y not in seen: seen.add(y); order.append(y)
    states, col = [], {}

    def rec(i, used):
        if i == len(order): states.append(tuple(col[u] for u in order)); return
        u = order[i]; forb = {col[w] for w in A[u] if w in col}
        for c in range(min(used + 1, 4)):
            if c not in forb: col[u] = c; rec(i + 1, max(used, c + 1)); del col[u]
    rec(0, 0)
    index = {s: k for k, s in enumerate(states)}
    L = set(link0)

    def comps(c, p, q):
        Vs = {u for u in order if c[u] in (p, q)}; out, sn = [], set()
        for s in Vs:
            if s in sn: continue
            comp, st = {s}, [s]; sn.add(s)
            while st:
                x = st.pop()
                for y in A[x]:
                    if y in Vs and y not in sn: sn.add(y); comp.add(y); st.append(y)
            out.append(comp)
        return out

    def canon(d):
        mp = {}; return tuple(mp.setdefault(d[u], len(mp)) for u in order)

    def dl(c, CP):
        lc = [c[x] for x in link0]
        if len(set(lc)) <= 3: return None
        j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
        m, a, b = link0[(j + 1) % 5], link0[(j + 3) % 5], link0[(j + 4) % 5]
        for t in (a, b):
            K = [K for K in CP[tuple(sorted((c[m], c[t])))] if m in K][0]
            if t not in K: return None
        return j
    info, linkmv, silentmv = {}, {}, {}
    for si, s in enumerate(states):
        c = dict(zip(order, s)); CP = {pq: comps(c, *pq) for pq in itertools.combinations(range(4), 2)}
        j = dl(c, CP)
        if j is None: continue
        info[si] = (j, c)
        lm, sm = set(), set()
        for (p, q), cs in CP.items():
            for K in cs:
                d = dict(c)
                for u in K: d[u] = q if c[u] == p else p
                t = index[canon(d)]
                (lm if K & L else sm).add(t)
        linkmv[si], silentmv[si] = lm, sm
    D0 = set(info)
    D1 = {s for s in D0 if linkmv[s] <= D0}
    D1p = {s for s in D1 if silentmv[s] <= D0}
    D2 = {s for s in D1 if linkmv[s] <= D1}
    Dinf = set(D0)
    while True:
        nxt = {s for s in Dinf if linkmv[s] <= Dinf}
        if nxt == Dinf: break
        Dinf = nxt

    def key(si):
        j, c = info[si]
        x = [link0[(j + t) % 5] for t in range(5)]
        al, mu, Ac, Bc = c[x[0]], c[x[1]], c[x[3]], c[x[4]]
        let = {al: "a", mu: "m", Ac: "A", Bc: "B"}
        feats = set(); words = []
        for t in range(5):
            d = len(rot[x[t]]); feats.add("d%d=%d" % (t, min(d, 8)))
            r = rot[x[t]]; i = r.index(hole)
            seq = r[i + 1:] + r[:i]  # neighbours of x_t after v, in rotation, excluding v
            seq = [u for u in seq if u not in L]
            prev = x[(t - 1) % 5]
            w = [u for u in seq if u in adj[prev]]
            if seq and w and seq[0] not in adj[prev] and seq[-1] in adj[prev]: seq = seq[::-1]
            word = "".join(let[c[u]] for u in seq); words.append(word)
            feats.add("|R%d|=%d" % (t, len(seq)))
            for ch in "amAB":
                if ch in word: feats.add("R%d has %s" % (t, ch))
            if word: feats.add("R%d starts %s" % (t, word[0])); feats.add("R%d ends %s" % (t, word[-1]))
        return tuple([min(len(rot[x[t]]), 8) for t in range(5)] + words), feats
    keys = {s: key(s) for s in D1}
    f1, f2 = Counter(), Counter()
    for s in D1:
        for f in keys[s][1]: f1[f] += 1
        if s in D2:
            for f in keys[s][1]: f2[f] += 1
    k1, k2 = Counter(keys[s][0] for s in D1), Counter(keys[s][0] for s in D2)
    return {"hole": hole, "states": len(states), "D0": len(D0), "D1": len(D1), "D1p": len(D1p), "D2": len(D2), "Dinf": len(Dinf),
            "feat_D1": dict(f1), "feat_D2": dict(f2), "keys_D1": len(k1), "keys_D2": len(k2),
            "keys_killed_D1_to_D2": len(set(k1) - set(k2))}


def main():
    if sys.argv[1] == "--faces":
        d = json.load(open(sys.argv[2])); F = d.get("faces") or d.get("faces_ccw")
        print(json.dumps({"graph": sys.argv[2], **analyse(rot_from_faces([tuple(f) for f in F]), int(sys.argv[3]))}))
        return
    lines = [l for l in open(sys.argv[2]).read().splitlines() if l.strip()]; n = int(sys.argv[3])
    for l in open(os.path.join(HERE, "..", "census", "km-%d.jsonl" % n)):
        r = json.loads(l)
        rot = {v: nb for v, nb in enumerate([[ord(c) - 97 for c in x] for x in lines[r["index"]].split()[1].split(",")])}
        for v in r["vertices"]:
            if v["deg"] == 5:
                print(json.dumps({"order": n, "index": r["index"], "orbit_size": v["orbit_size"], **analyse(rot, v["v"])}), flush=True)


if __name__ == "__main__":
    main()
