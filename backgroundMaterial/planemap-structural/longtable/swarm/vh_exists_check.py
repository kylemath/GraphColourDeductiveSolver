"""Sanity checks for vh-exists.md on the WP11 manifest graphs (orders 12-20 only).

For each graph T (minimum degree 5) this computes, from scratch:

  A. The mixed move graph M(T) on all states (h, c), h any vertex, c a proper
     4-colouring of T - h, canonical under colour renaming.  Kempe swaps (hole
     fixed, any bichromatic component of T - h) and singleton slides.
     - strong-VH: does every component of M(T) contain a fill state?
     - KD(h): does every Kempe class of T - h contain a fill state?  (swap only)
     - for Kempe classes of T - h with no fill: does the M(T) component (slides
       allowed) contain one?  This is what slides add.
  B. For every degree-5 v and legal fan tau:
     - S(v,tau) equals the colourings of T - v proper on tau;
     - apex-singleton: the apex colour is unique on the link for every c in S;
     - containment: every Kempe class of T*_tau lies inside one Kempe class of
       T - v (checked, though it is proved by hand);
     - KT*: does every Kempe class of T*_tau contain a fill state?  (the
       strongest sufficient condition in vh-exists.md, section 3)
     - the number of T*_tau classes, of T - v classes meeting S, and whether
       S contains a fill state at all (F n S empty iff the double
       identification graph T_i is not 4-colourable).
     - VH(v,tau) itself (mixed) -- cannot fail here, recorded as a check.

Orders above 20 are never read.  Run: python3 vh_exists_check.py > vh-exists-check.txt
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mass_core import parse_ascii  # noqa: E402

HOLE = 4
PAIRS = list(itertools.combinations(range(4), 2))


def canon(state):
    seen = {}
    return tuple(HOLE if x == HOLE else seen.setdefault(x, len(seen)) for x in state)


def colourings(adj, hole, extra=()):
    """All proper 4-colourings of T - hole (+ extra edges), canonical, HOLE at hole."""
    n = len(adj)
    nb = [set(a) for a in adj]
    for a, b in extra:
        nb[a].add(b)
        nb[b].add(a)
    order = [u for u in range(n) if u != hole]
    pos = {u: i for i, u in enumerate(order)}
    earlier = [[pos[w] for w in nb[u] if w != hole and pos[w] < i] for i, u in enumerate(order)]
    cur = [0] * len(order)
    out = []

    def go(i, top):
        if i == len(order):
            st = [HOLE] * n
            for j, u in enumerate(order):
                st[u] = cur[j]
            out.append(tuple(st))  # already first-occurrence canonical along `order`
            return
        blocked = {cur[j] for j in earlier[i]}
        for a in range(min(3, top + 1) + 1):
            if a not in blocked:
                cur[i] = a
                go(i + 1, max(top, a))

    go(0, -1)
    return [canon(s) for s in out]


def kempe_moves(nb, state):
    for a, b in PAIRS:
        seen = set()
        for s, col in enumerate(state):
            if (col != a and col != b) or s in seen:
                continue
            comp = {s}
            stack = [s]
            while stack:
                x = stack.pop()
                for y in nb[x]:
                    if y not in comp and (state[y] == a or state[y] == b):
                        comp.add(y)
                        stack.append(y)
            seen |= comp
            nxt = list(state)
            for x in comp:
                nxt[x] = b if state[x] == a else a
            yield canon(nxt)


def slide_moves(adj, state):
    h = state.index(HOLE)
    cols = [state[w] for w in adj[h]]
    for u in adj[h]:
        if cols.count(state[u]) == 1:
            nxt = list(state)
            nxt[h] = state[u]
            nxt[u] = HOLE
            yield canon(nxt)


class UF:
    def __init__(self):
        self.p = {}

    def add(self, x):
        self.p.setdefault(x, x)

    def find(self, x):
        p = self.p
        r = x
        while p[r] != r:
            r = p[r]
        while p[x] != r:
            p[x], x = r, p[x]
        return r

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def is_fill(adj, state):
    h = state.index(HOLE)
    return len({state[w] for w in adj[h]}) <= 3


def legal_fans(adj, v):
    link = adj[v]
    fans = []
    for i in range(5):
        a, far, near = link[i], link[(i + 2) % 5], link[(i + 3) % 5]
        if far in adj[a] or near in adj[a]:
            continue
        fans.append((i, (a, far), (a, near)))
    return fans


def analyse(rot):
    n = len(rot)
    adj = rot
    nbs = [set(a) for a in adj]
    states_by_hole = {h: colourings(adj, h) for h in range(n)}
    kuf = UF()  # Kempe classes (hole fixed)
    muf = UF()  # mixed components
    for h, sts in states_by_hole.items():
        for s in sts:
            kuf.add(s)
            muf.add(s)
    for h, sts in states_by_hole.items():
        for s in sts:
            for t in kempe_moves(nbs, s):
                kuf.union(s, t)
                muf.union(s, t)
            for t in slide_moves(adj, s):
                muf.union(s, t)
    fill = {s: is_fill(adj, s) for sts in states_by_hole.values() for s in sts}
    kfill, mfill = set(), set()
    for s, f in fill.items():
        if f:
            kfill.add(kuf.find(s))
            mfill.add(muf.find(s))
    mcomps = {muf.find(s) for s in fill}
    out = {
        "n": n,
        "states": len(fill),
        "M_components": len(mcomps),
        "M_components_without_fill": sum(1 for r in mcomps if r not in mfill),
        "holes": [],
        "pairs": [],
    }
    for h, sts in states_by_hole.items():
        classes = {kuf.find(s) for s in sts}
        bad = [r for r in classes if r not in kfill]
        rescued = sum(1 for r in bad if muf.find(r) in mfill)
        out["holes"].append({"h": h, "deg": len(adj[h]), "colourings": len(sts),
                             "kempe_classes": len(classes), "classes_without_fill": len(bad),
                             "of_which_rescued_by_slides": rescued})
    for v in range(n):
        if len(adj[v]) != 5:
            continue
        link = adj[v]
        for i, c1, c2 in legal_fans(adj, v):
            S = [s for s in states_by_hole[v] if s[c1[0]] != s[c1[1]] and s[c2[0]] != s[c2[1]]]
            S2 = colourings(adj, v, extra=(c1, c2))
            assert set(S) == set(S2), "S(v,tau) != Col(T*_tau)"
            apex = link[i]
            for s in S:
                cols = [s[w] for w in link]
                assert cols.count(s[apex]) == 1, "apex singleton fails"
            nb_star = [set(a) for a in adj]
            for a, b in (c1, c2):
                nb_star[a].add(b)
                nb_star[b].add(a)
            suf = UF()
            Sset = set(S)
            for s in S:
                suf.add(s)
            for s in S:
                for t in kempe_moves(nb_star, s):
                    assert t in Sset
                    suf.union(s, t)
            star_classes = {}
            for s in S:
                star_classes.setdefault(suf.find(s), []).append(s)
            contained = all(len({kuf.find(s) for s in mem}) == 1 for mem in star_classes.values())
            kt_star_bad = sum(1 for mem in star_classes.values() if not any(fill[s] for s in mem))
            near = {s: fill[s] or any(is_fill(adj, t) for t in kempe_moves(nbs, s)) for s in S}
            near_mixed = {s: near[s] or any(is_fill(adj, t) for t in slide_moves(adj, s)) for s in S}
            u_bad = sum(1 for mem in star_classes.values() if not any(near[s] for s in mem))
            um_bad = sum(1 for mem in star_classes.values() if not any(near_mixed[s] for s in mem))
            tv_classes_meeting_S = len({kuf.find(s) for s in S})
            swap_only_bad = sum(1 for r in {kuf.find(s) for s in S} if r not in kfill)
            vh_bad = sum(1 for s in S if muf.find(s) not in mfill)
            out["pairs"].append({"v": v, "fan": i, "apex": apex, "S": len(S),
                                 "Tstar_classes": len(star_classes),
                                 "containment_ok": contained,
                                 "Tstar_classes_without_fill_in_S": kt_star_bad,
                                 "fill_in_S": sum(1 for s in S if fill[s]),
                                 "U_bad_classes": u_bad,
                                 "Umixed_bad_classes": um_bad,
                                 "Tv_classes_meeting_S": tv_classes_meeting_S,
                                 "swap_only_VH_failures": swap_only_bad,
                                 "VH_failures": vh_bad})
    return out


def main():
    man = json.loads((HERE.parent / "wp11-run-manifest.json").read_text())
    graphs = man["discovery_graphs"] + man["validation_graphs"]
    graphs = [g for g in graphs if g["order"] <= 20]
    print("vh_exists_check.py: WP11 manifest graphs, orders <= 20, count", len(graphs))
    tot = {"graphs": 0, "M_bad": 0, "deg5_KD_bad": 0, "high_KD_bad_classes": 0,
           "high_KD_rescued": 0, "pairs": 0, "pairs_KTstar_fail": 0,
           "graphs_no_KTstar_pair": 0, "pairs_fill_in_S_empty": 0,
           "containment_fail": 0, "VH_fail": 0, "swap_only_fail": 0,
           "pairs_U_fail": 0, "graphs_no_U_pair": 0, "pairs_Umixed_fail": 0, "graphs_no_Umixed_pair": 0}
    t0 = time.time()
    for g in graphs:
        rot = parse_ascii(g["ascii"])
        r = analyse(rot)
        tot["graphs"] += 1
        tot["M_bad"] += r["M_components_without_fill"]
        d5bad = sum(x["classes_without_fill"] for x in r["holes"] if x["deg"] == 5)
        hb = [x for x in r["holes"] if x["deg"] > 5 and x["classes_without_fill"]]
        tot["deg5_KD_bad"] += d5bad
        tot["high_KD_bad_classes"] += sum(x["classes_without_fill"] for x in hb)
        tot["high_KD_rescued"] += sum(x["of_which_rescued_by_slides"] for x in hb)
        P = r["pairs"]
        tot["pairs"] += len(P)
        kfail = [p for p in P if p["Tstar_classes_without_fill_in_S"]]
        tot["pairs_KTstar_fail"] += len(kfail)
        if len(kfail) == len(P):
            tot["graphs_no_KTstar_pair"] += 1
        uf = [p for p in P if p["U_bad_classes"]]
        umf = [p for p in P if p["Umixed_bad_classes"]]
        tot["pairs_U_fail"] += len(uf)
        tot["pairs_Umixed_fail"] += len(umf)
        tot["graphs_no_U_pair"] += int(len(uf) == len(P))
        tot["graphs_no_Umixed_pair"] += int(len(umf) == len(P))
        tot["pairs_fill_in_S_empty"] += sum(1 for p in P if p["fill_in_S"] == 0)
        tot["containment_fail"] += sum(1 for p in P if not p["containment_ok"])
        tot["VH_fail"] += sum(p["VH_failures"] for p in P)
        tot["swap_only_fail"] += sum(p["swap_only_VH_failures"] for p in P)
        degs = sorted({len(a) for a in rot})
        print(f"{g['order']}:{g['graph_index']} degs={degs} states={r['states']} "
              f"Mcomp={r['M_components']} Mcomp_nofill={r['M_components_without_fill']} "
              f"deg5_KD_bad={d5bad} "
              f"highdeg_holes_KD_bad={[(x['h'], x['deg'], x['classes_without_fill'], x['of_which_rescued_by_slides']) for x in hb]} "
              f"pairs={len(P)} KTstar_fail_pairs={len(kfail)} "
              f"max_Tstar_classes={max((p['Tstar_classes'] for p in P), default=0)} "
              f"fillInS_empty_pairs={sum(1 for p in P if p['fill_in_S'] == 0)} "
              f"U_fail_pairs={len(uf)} Umixed_fail_pairs={len(umf)} "
              f"holes_with_split_Kempe_classes={[(x['h'], x['deg'], x['kempe_classes']) for x in r['holes'] if x['kempe_classes'] > 1]}", flush=True)
        for p in P:
            if p["fill_in_S"] == 0:
                print(f"   F n S empty: v={p['v']} fan={p['fan']} apex={p['apex']} |S|={p['S']}", flush=True)
        if uf and len(uf) == len(P):
            ex = uf[0]
            print(f"   no pair satisfies U; e.g. v={ex['v']} fan={ex['fan']} T*classes={ex['Tstar_classes']} "
                  f"locked-only classes={ex['U_bad_classes']}", flush=True)
        if kfail:
            ex = kfail[0]
            print(f"   first KT* failure: v={ex['v']} fan={ex['fan']} apex={ex['apex']} |S|={ex['S']} "
                  f"T*classes={ex['Tstar_classes']} without fill in S={ex['Tstar_classes_without_fill_in_S']} "
                  f"T-v classes meeting S={ex['Tv_classes_meeting_S']}", flush=True)
    print("TOTALS", json.dumps(tot))
    print(f"elapsed {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
