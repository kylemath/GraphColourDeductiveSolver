#!/usr/bin/env python3
"""Regressions for the WP19 independent checker.

Fixtures are built here with the checker's own stdlib code (a small reference
producer below), never with the WP19 producer, wp18_core, mass_core or audit
code.  Then the checker must ACCEPT the valid fixtures and REJECT each
malformed one.  Graphs: icosahedron 12:0, order-14 dipyramid 14:0, and 17:1
(all from wp11-run-manifest.json discovery_graphs).  Order >= 21 is never used.

Run:  python3 wp19_check_regressions.py > check-regressions-output.txt
"""

import copy
import hashlib
import json
import random
import sys

import wp19_check as C

ICO = "12 bcdef,afghc,abhid,acije,adjkf,aekgb,bfklh,bglic,chljd,dilke,ejlgf,gkjih"
O14 = "14 bcdef,afghc,abhid,acije,adjkf,aeklgb,bflmh,bgmic,chmnjd,dinke,ejnlf,fknmg,glnih,imlkj"
G17_1 = ("17 bcdef,afghc,abhijd,acjkle,adlmf,aemgb,bfmnoh,bgoic,chopj,cipkd,djpql,"
         "dkqnme,elngf,gmlqo,gnqpih,ioqkj,kponl")

DECL_SHA = C.declaration_sha(C.DEFAULT_DECL)
RESULTS = []


def build_graph(ascii_, idx):
    """Reference producer for small graphs (exhaustive, uncapped in practice)."""
    g = C.parse_ascii(ascii_)
    assert not C.validate_graph(g)
    caps = C.DEFAULT_CAPS
    G = {"order": g.n, "graph_index": idx, "ascii": ascii_,
         "ascii_sha256": hashlib.sha256(ascii_.encode()).hexdigest(),
         "degrees": sorted(len(r) for r in g.rot), "interrupted": False,
         "peak_rss_kb": 0, "pairs": [], "unresolved_pairs": [], "kills": []}
    aux = {}
    for (v, i), ch in sorted(C.legal_pairs(g).items()):
        S = C.enumerate_starts(g, v, ch)
        hl, hk, ell, paths = {}, {}, {}, {}
        for s in S:
            d, p = C.shortest_fill(g, s, caps["mixed"], True)
            kd = C.first_fill_depth(g, s, caps["kempe"], False)
            assert d is not None and kd is not None
            ell[s], paths[s] = d, p
            hl[str(d)] = hl.get(str(d), 0) + 1
            hk[str(kd)] = hk.get(str(kd), 0) + 1
            assert C.is_locked(g, s) == (d >= 2)          # Lemma A
        classes = C.tstar_classes(g, v, ch, S)
        locked_cls = [cl for cl in classes if all(C.is_locked(g, s) for s in cl)]
        L = max(ell.values())
        P = {"v": v, "fan_index": i, "chords": [list(c) for c in ch], "empty": False,
             "starts": len(S), "hist_l": hl, "hist_k": hk, "L": L, "L_at_least": L,
             "unresolved_reason": None, "tstar_classes": len(classes),
             "locked_classes": len(locked_cls), "U": not locked_cls}
        if L >= 3:
            w = min(s for s in S if ell[s] == L)
            P["witness_L"] = {"start": list(w), "path": paths[w]}
        if locked_cls:
            P["u_fail_class"] = [list(s) for s in sorted(locked_cls[0])]
        G["pairs"].append(P)
        aux[(v, i)] = {"starts": S, "ell": ell, "paths": paths, "classes": classes}
    Ls = [P["L"] for P in G["pairs"]]
    G["m"] = G["m_at_least"] = min(Ls)
    G["U_exists"] = any(P["U"] for P in G["pairs"])
    return g, G, aux


def phase(graphs):
    return {"phase": "regression", "declaration": C.DECL_NAME,
            "declaration_sha256": DECL_SHA, "source_sha256": {"fixture": "n/a"},
            "input_sha256": "n/a", "caps": dict(C.DEFAULT_CAPS), "truncated": False,
            "graphs": graphs, "summary": {}}


def run(name, D, expect_ok, expect_code=None):
    r = C.check_phase(D, DECL_SHA, label=name)
    codes = sorted({f["code"] for f in r["failures"]})
    ok = not r["failures"]
    if expect_ok:
        passed = ok
    else:
        passed = (not ok) and (expect_code is None or codes == [expect_code])
    RESULTS.append(passed)
    print("%-62s %s  expected=%s codes=%s" % (name, "PASS" if passed else "FAIL",
          "accept" if expect_ok else "reject:" + str(expect_code), codes))
    if not passed or not expect_ok:
        for f in r["failures"][:2]:
            print("      ", f["msg"][:150])
    return r


def fact(name, cond):
    RESULTS.append(bool(cond))
    print("%-62s %s" % (name, "PASS" if cond else "FAIL"))


def pair_of(G, k):
    return next(P for P in G["pairs"] if (P["v"], P["fan_index"]) == k)


def main():
    gI, GI, auxI = build_graph(ICO, 0)
    g14, G14, aux14 = build_graph(O14, 0)
    g17, G17, aux17 = build_graph(G17_1, 1)

    print("== Independent reference values (own code) vs. recorded project values ==")
    fact("icosahedron: 60 legal pairs", len(GI["pairs"]) == 60)
    fact("icosahedron: 8 starts and L=1 at every pair",
         all(P["starts"] == 8 and P["L"] == 1 for P in GI["pairs"]))
    fact("icosahedron: kappa <= 1 everywhere",
         all(set(P["hist_k"]) <= {"0", "1"} for P in GI["pairs"]))
    fact("icosahedron: U holds at every pair", all(P["U"] for P in GI["pairs"]))
    locked14 = [(k, s) for k, a in aux14.items() for s in a["starts"] if a["ell"][s] == 2
                and C.is_locked(g14, s)]
    fact("order 14: a locked start with l = 2 exists (%d such starts)" % len(locked14),
         len(locked14) > 0)
    fact("17:1: m = 3 (got %d)" % G17["m"], G17["m"] == 3)
    nU = sum(P["U"] for P in G17["pairs"])
    fact("17:1: 38 of 60 pairs satisfy U (got %d of %d)" % (nU, len(G17["pairs"])),
         nU == 38 and len(G17["pairs"]) == 60)
    fact("17:1 v=0 tau0: hist l = {0:6,1:16,2:7,3:2,4:2}",
         pair_of(G17, (0, 0))["hist_l"] == {"0": 6, "1": 16, "2": 7, "3": 2, "4": 2})
    rnd = random.Random(19)
    inv = True
    for g, aux in ((gI, auxI), (g14, aux14), (g17, aux17)):
        k = rnd.choice(sorted(aux))
        s = rnd.choice(aux[k]["starts"])
        perm = list(range(4))
        rnd.shuffle(perm)
        t = tuple(C.HOLE if x == C.HOLE else perm[x] for x in s)
        d1 = C.shortest_fill(g, C.canon(t), 6, True)[0]
        inv &= C.canon(t) == s and d1 == aux[k]["ell"][s]
    fact("colour-renaming invariance on one random start per graph", inv)

    print("\n== Valid fixtures must be accepted ==")
    run("valid: icosahedron 12:0", phase([GI]), True)
    run("valid: order 14 dipyramid 14:0", phase([G14]), True)
    run("valid: 17:1 (22 verified u_fail classes, L>=3 witnesses)", phase([G17]), True)
    r = C.check_phase(phase([G17]), DECL_SHA)
    fact("17:1: u_fail classes verified = 22 (got %d)" % r["stats"]["u_fail_classes_verified"],
         r["stats"]["u_fail_classes_verified"] == 22)

    print("\n== Malformed fixtures must be rejected ==")
    # 1. improper start (witness on 17:1)
    D = phase([copy.deepcopy(G17)])
    P = next(P for P in D["graphs"][0]["pairs"] if "witness_L" in P)
    s = P["witness_L"]["start"]
    v = P["v"]
    u = next(x for x in range(len(s)) if x != v and s[x] != 0)
    w = next(y for y in g17.rot[u] if y != v)
    s[w] = s[u]
    s[:] = list(C.canon(s))
    run("reject: improper witness start", D, False, "witness")
    # 1b. improper start inside an M1 kill
    D = phase([copy.deepcopy(G17)])
    D["graphs"][0]["kills"] = [{"stmt": "M1", "pair": [P["v"], P["fan_index"]], "start": s}]
    run("reject: improper start in an M1 kill", D, False, "kill_M1")
    # 2. non-closed u_fail_class: a single locked start (order 14)
    D = phase([copy.deepcopy(G14)])
    k, s = locked14[0]
    PP = pair_of(D["graphs"][0], k)
    PP["U"] = False
    PP["locked_classes"] = 1
    PP["u_fail_class"] = [list(s)]
    D["graphs"][0]["U_exists"] = any(P["U"] for P in D["graphs"][0]["pairs"])
    run("reject: non-closed u_fail_class (one locked start, 14:0)", D, False, "u_fail")
    # 2b. non-closed: a verified 17:1 class with one member removed
    D = phase([copy.deepcopy(G17)])
    PP = next(P for P in D["graphs"][0]["pairs"] if not P["U"])
    PP["u_fail_class"] = PP["u_fail_class"][:-1]
    run("reject: verified 17:1 class with one member dropped", D, False, "u_fail")
    # 3. class containing an unlocked member: the full T*-class of the locked start
    D = phase([copy.deepcopy(G14)])
    cl = next(c for c in aux14[k]["classes"] if s in c)
    PP = pair_of(D["graphs"][0], k)
    PP["U"] = False
    PP["locked_classes"] = 1
    PP["u_fail_class"] = [list(x) for x in sorted(cl)]
    D["graphs"][0]["U_exists"] = any(P["U"] for P in D["graphs"][0]["pairs"])
    run("reject: closed class containing an unlocked member (14:0)", D, False, "u_fail")
    # 3b. a closed class whose members are not starts (chord monochromatic)
    D = phase([copy.deepcopy(G17)])
    PP = next(P for P in D["graphs"][0]["pairs"] if not P["U"])
    other = next(P for P in D["graphs"][0]["pairs"] if P["v"] != PP["v"] and P["U"])
    other["U"] = False
    other["locked_classes"] = 1
    other["u_fail_class"] = PP["u_fail_class"]
    run("reject: u_fail_class of another pair (hole not at v)", D, False, "u_fail")
    # 4. short path claimed as kills
    D = phase([copy.deepcopy(GI)])
    a = auxI[(0, 0)]
    s1 = next(x for x in a["starts"] if a["ell"][x] == 1)
    D["graphs"][0]["kills"] = [{"stmt": "M1", "pair": [0, 0], "start": list(s1)}]
    run("reject: M1 kill on an l=1 start (icosahedron)", D, False, "kill_M1")
    D = phase([copy.deepcopy(G17)])
    a = aux17[(0, 0)]
    s4 = next(x for x in a["starts"] if a["ell"][x] == 4)
    D["graphs"][0]["kills"] = [{"stmt": "M1", "pair": [0, 0], "start": list(s4)}]
    run("reject: M1 kill on an l=4 start (17:1)", D, False, "kill_M1")

    def worst_per_pair(aux):
        return [{"pair": list(k), "start": list(max(a["starts"], key=lambda x: (a["ell"][x], x)))}
                for k, a in sorted(aux.items())]
    D = phase([copy.deepcopy(GI)])
    D["graphs"][0]["kills"] = [{"stmt": "C2", "per_pair": worst_per_pair(auxI)}]
    run("reject: C2 kill on the icosahedron (all l <= 1)", D, False, "kill_C2")
    D = phase([copy.deepcopy(G17)])
    D["graphs"][0]["kills"] = [{"stmt": "C2", "per_pair": worst_per_pair(aux17)}]
    run("reject: C2 kill on 17:1 (m = 3, some pair fills in 3)", D, False, "kill_C2")
    D = phase([copy.deepcopy(G17)])
    D["graphs"][0]["kills"] = [{"stmt": "C1", "per_pair": worst_per_pair(aux17)}]
    r = run("reject: C1 kill on 17:1 (layers fine, but order < 18)", D, False, "kill_C1")
    fact("   ...and the rejection reason is the order, not the layers",
         "order 17 < 18" in r["failures"][0]["msg"])
    # C1-type layer content is valid at 17:1: show it via C3 (rejected only for degree)
    D = phase([copy.deepcopy(G17)])
    D["graphs"][0]["kills"] = [{"stmt": "C3", "per_pair": worst_per_pair(aux17)}]
    r = run("reject: C3 kill on 17:1 (no vertex of degree >= 7)", D, False, "kill_C3")
    # the same per_pair with a short start substituted at one pair
    D = phase([copy.deepcopy(G17)])
    pp = worst_per_pair(aux17)
    a = aux17[(0, 0)]
    pp[0]["start"] = list(next(x for x in a["starts"] if a["ell"][x] == 2))
    D["graphs"][0]["kills"] = [{"stmt": "C2", "per_pair": pp}]
    run("reject: C2 per_pair with an l=2 start", D, False, "kill_C2")
    # M2 / M3 false kills
    D = phase([copy.deepcopy(G17)])
    D["graphs"][0]["kills"] = [{"stmt": "M2", "pair": [0, 0], "start": list(s4),
                                "l_path": a["paths"][s4], "kappa": "lower",
                                "kappa_lower": len(a["paths"][s4]) + 2}]
    run("reject: M2 lower kill where kappa <= l+1", D, False, "kill_M2")
    D = phase([copy.deepcopy(G17)])
    D["graphs"][0]["kills"] = [{"stmt": "M2", "pair": [0, 0], "start": list(s4),
                                "kappa": "nofill"}]
    run("reject: M2 nofill kill where the Kempe class has a fill", D, False, "kill_M2")
    s2 = next(x for x in a["starts"] if a["ell"][x] == 2)
    D = phase([copy.deepcopy(G17)])
    D["graphs"][0]["kills"] = [{"stmt": "M3", "pair": [0, 0], "start": list(s2),
                                "l_path": a["paths"][s2]}]
    run("reject: M3 kill where kappa = 2", D, False, "kill_M3")
    D = phase([copy.deepcopy(G17)])
    D["graphs"][0]["kills"] = [{"stmt": "U_exists"}]
    run("reject: U_exists kill on 17:1 (38 pairs have U)", D, False, "kill_U_exists")
    # witness path claims
    D = phase([copy.deepcopy(G17)])
    P = pair_of(D["graphs"][0], (0, 0))
    P["witness_L"]["path"] = P["witness_L"]["path"] + [P["witness_L"]["path"][-1]]
    run("reject: witness path with an extra move", D, False, "witness")
    D = phase([copy.deepcopy(G17)])
    P = pair_of(D["graphs"][0], (0, 0))
    s3 = next(x for x in a["starts"] if a["ell"][x] == 3)
    # the first move only of the shortest fill of an l=3 start
    P["witness_L"] = {"start": list(s3), "path": a["paths"][s3][:1]}
    run("reject: witness path that does not end filled", D, False, "witness")
    # 5. wrong pair coverage
    D = phase([copy.deepcopy(GI)])
    D["graphs"][0]["pairs"] = D["graphs"][0]["pairs"][1:]
    run("reject: one legal pair missing (icosahedron)", D, False, "coverage")
    D = phase([copy.deepcopy(G14)])
    extra = copy.deepcopy(D["graphs"][0]["pairs"][0])
    extra["v"] = 5   # vertex 5 of 14:0 has degree 6
    D["graphs"][0]["pairs"].append(extra)
    run("reject: extra pair at a degree-6 vertex (14:0)", D, False, "coverage")
    D = phase([copy.deepcopy(GI)])
    D["graphs"][0]["pairs"][0]["chords"] = [[1, 3], [2, 4]]
    run("reject: chords not those of the named fan", D, False, "chords")
    # 6. binding and accounting
    D = phase([copy.deepcopy(GI)])
    D["declaration_sha256"] = "0" * 64
    r = run("reject: wrong declaration_sha256 (refused)", D, False, "declaration_sha256")
    fact("   ...and the file is refused before any graph is read", r.get("refused") is True)
    D = phase([copy.deepcopy(G17)])
    P = pair_of(D["graphs"][0], (0, 0))
    P["unresolved_reason"] = "interrupted"
    P["L"] = None
    D["graphs"][0]["unresolved_pairs"] = [[0, 0]]
    run("reject: unresolved pair but m still exact", D, False, "m_exact")
    D["graphs"][0]["m"] = None
    r = run("accept: unresolved pair with m null (counted unresolved)", D, True)
    fact("   ...graph counted as unresolved, not as passing",
         r["stats"]["graphs_unresolved"] == 1)
    D = phase([copy.deepcopy(G17)])
    pair_of(D["graphs"][0], (0, 0))["unresolved_reason"] = "capped"
    run("reject: pair with a reason not listed in unresolved_pairs", D, False, None)
    D = phase([copy.deepcopy(GI)])
    D["graphs"][0]["ascii_sha256"] = "f" * 64
    run("reject: wrong ascii_sha256", D, False, "ascii_hash")
    D = phase([copy.deepcopy(G17)])
    D["graphs"][0]["m_at_least"] = 2
    D["graphs"][0]["m"] = 2
    run("reject: m_at_least not min of L_at_least", D, False, "m_at_least")

    print("\nTOTAL: %d checks, %d passed, %d failed"
          % (len(RESULTS), sum(RESULTS), len(RESULTS) - sum(RESULTS)))
    print("Note: " + C.PRODUCER_CLAIMS_NOTE)
    return 0 if all(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
