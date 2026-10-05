"""WP11 certificate producer (schema wp11-cert-v1) and the three named-fixture examples.

This is NOT the rank search. It builds the frozen certificate format and three small examples
that reproduce already-published results, for the math team's schema review:
  - pass:                  icosahedron root 0, rank (p, q)            [weights e1]
  - all_roots_fail_witness: order 17 graph 0 root 4, rank (p, q)      [published mass failure]
  - existential_fail_witness: order 17 graph 1, rank (p, L)           [published WP4b Lonly kill]

Moves are serialised in the NAMED colour coordinates of the colouring they act on: move 1 acts on
the listed (canonical) start colouring; the intermediate colouring is the raw named result; move 2
acts on that raw intermediate; the endpoint is raw, with its canonical form for state identity.
No renaming happens between moves.  Endpoint lists in failure certificates are complete.
"""
import hashlib
import itertools
import json
from pathlib import Path

from mass_core import FIXTURES, HERE, RootState, canon, degree_five, parse_ascii, rotation_from_fixture

PAIRS = list(itertools.combinations(range(4), 2))
FEATURES = ["q", "lin", "L", "Lall", "links", "shortLinks", "repMass", "hubToggles"]
OUT = HERE / "wp11-schema-examples"


def components(adj, col):
    """Active bichromatic components: components of the subgraph induced on vertices coloured a or b."""
    out = []
    for a, b in PAIRS:
        pending = {v for v, x in col.items() if x in (a, b)}
        while pending:
            seed = min(pending)
            pending.discard(seed)
            comp, stack = {seed}, [seed]
            while stack:
                v = stack.pop()
                for w in adj[v]:
                    if w in pending:
                        pending.discard(w)
                        comp.add(w)
                        stack.append(w)
            out.append(((a, b), frozenset(comp)))
    return out


def features(adj, B, col):
    Bset = set(B)
    cols = [col[v] for v in B]
    p = max(0, len(set(cols)) - 3)
    comps = components(adj, col)
    hub = sum(1 for _, K in comps if len(K) == 2 and any(v not in Bset for v in K))
    if p == 0:
        f = dict.fromkeys(FEATURES, 0)
        f["hubToggles"] = hub
        return p, f
    rho = next(x for x in set(cols) if cols.count(x) == 2)
    where = {(pr, v): K for pr, K in comps for v in K}
    meets = [(pr, K) for pr, K in comps if K & Bset]

    def linked(v, x):
        K = where[(tuple(sorted((col[v], x))), v)]
        return bool((K & Bset) - {v})

    single = [v for v in B if cols.count(col[v]) == 1]
    return p, {
        "q": sum(len(K - Bset) ** 2 for _, K in meets),
        "lin": sum(len(K - Bset) for _, K in meets),
        "L": sum(linked(v, x) for v in single for x in range(4) if x != col[v]),
        "Lall": sum(linked(v, x) for v in B for x in range(4) if x != col[v]),
        "links": sum(1 for _, K in comps if len(K & Bset) >= 2),
        "shortLinks": sum(1 for _, K in comps if len(K & Bset) >= 2 and K <= Bset),
        "repMass": sum(len(K - Bset) ** 2 for pr, K in meets if rho in pr),
        "hubToggles": hub,
    }


def rank(feat, w):
    p, f = feat
    return (p, sum(w[i] * f[name] for i, name in enumerate(FEATURES)))


def swap(col, pr, K):
    a, b = pr
    return {v: (b if x == a else a if x == b else x) if v in K else x for v, x in col.items()}


def endpoints(adj, col):
    """Complete list of 1- and 2-move macro endpoints, components recomputed after move 1."""
    out = []
    for pr1, K1 in components(adj, col):
        c1 = swap(col, pr1, K1)
        out.append(({"pair": list(pr1), "component": sorted(K1)}, None, None, c1))
        for pr2, K2 in components(adj, c1):
            out.append(({"pair": list(pr1), "component": sorted(K1)}, c1,
                        {"pair": list(pr2), "component": sorted(K2)}, swap(c1, pr2, K2)))
    return out


def root_setup(rot, r):
    s = RootState(rot, r)
    adj = {v: [w for w in rot[v] if w != r] for v in s.V}
    return s, adj, list(rot[r])


def as_list(V, col):
    return [col[v] for v in V]


def state_record(s, adj, B, c, w, with_witness):
    col = dict(zip(s.V, c))
    feat = features(adj, B, col)
    rec = {"coloring": list(c), "p": feat[0], "features": feat[1], "rank": list(rank(feat, w))}
    if feat[0] == 1 and with_witness:
        r0 = rank(feat, w)
        for m1, c1, m2, c2 in endpoints(adj, col):
            f2 = features(adj, B, c2)
            if rank(f2, w) < r0:
                rec["witness"] = {"move1": m1, "intermediate": as_list(s.V, c1) if c1 else None,
                                  "move2": m2, "endpoint": as_list(s.V, c2),
                                  "endpoint_canonical": list(canon(as_list(s.V, c2))),
                                  "endpoint_features": f2[1], "endpoint_rank": list(rank(f2, w))}
                break
        else:
            rec["witness"] = None
    return rec


def stuck_record(s, adj, B, w):
    for c in s.C:
        col = dict(zip(s.V, c))
        feat = features(adj, B, col)
        if feat[0] != 1:
            continue
        r0 = rank(feat, w)
        eps = endpoints(adj, col)
        if any(rank(features(adj, B, c2), w) < r0 for *_, c2 in eps):
            continue
        return {"coloring": list(c), "features": feat[1], "rank": list(r0),
                "endpoints": [{"move1": m1, "intermediate": as_list(s.V, c1) if c1 else None,
                               "move2": m2, "endpoint": as_list(s.V, c2),
                               "endpoint_rank": list(rank(features(adj, B, c2), w))}
                              for m1, c1, m2, c2 in eps]}
    return None


def graph_block(source, order, gi, rot, ascii_line):
    return {"source": source, "order": order, "graph_index": gi, "ascii": ascii_line,
            "ascii_sha256": hashlib.sha256(ascii_line.encode()).hexdigest() if ascii_line else None,
            "rotation": rot}


def header(kind, w, graph):
    return {"schema": "wp11-cert-v1", "kind": kind, "features": FEATURES,
            "weights": w, "rank": "lexicographic (p, sum_i w_i f_i)", "macro_bound": 2,
            "moves": "whole active bichromatic components, interior allowed; components recomputed after move 1",
            "colour_coordinates": "moves named in the colours of the colouring they act on; no renaming between moves",
            "graph": graph,
            "producer": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (HERE / "wp11_cert.py", HERE / "mass_core.py")},
            "note": "Schema example reproducing a published result; not a WP11 search output."}


def main():
    OUT.mkdir(exist_ok=True)
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())

    def corpus(order, gi):
        line = next(g for o in table["orders"] if o["order"] == order
                    for g in o["graphs_checked"] if g["graph_index"] == gi)["ascii"]
        return line, parse_ascii(line)

    e1 = [1, 0, 0, 0, 0, 0, 0, 0]
    e3 = [0, 0, 1, 0, 0, 0, 0, 0]

    # pass: icosahedron root 0 with (p, q)
    irot = rotation_from_fixture(FIXTURES / "icosahedron-fixture.json")
    s, adj, B = root_setup(irot, 0)
    states = [state_record(s, adj, B, c, e1, True) for c in s.C]
    assert all(st.get("witness") is not False and (st["p"] == 0 or st["witness"]) for st in states)
    cert = header("pass", e1, graph_block("icosahedron-fixture.json", 12, None, irot, None))
    cert.update({"degree_five_roots": degree_five(irot), "root": 0, "vertex_order": s.V, "boundary_cyclic_order": B,
                 "state_count": len(states), "states": states})
    (OUT / "pass-icosahedron-root0-q.json").write_text(json.dumps(cert, indent=1) + "\n")

    # all-roots failure witness: order 17 graph 0 root 4 with (p, q)
    line, rot = corpus(17, 0)
    s, adj, B = root_setup(rot, 4)
    st = stuck_record(s, adj, B, e1)
    assert st is not None
    cert = header("all_roots_fail_witness", e1, graph_block("corpus", 17, 0, rot, line))
    cert.update({"degree_five_roots": degree_five(rot), "failing_root": {"root": 4, "vertex_order": s.V,
                 "boundary_cyclic_order": B, "stuck": st}})
    (OUT / "all-roots-fail-17-0-root4-q.json").write_text(json.dumps(cert, indent=1) + "\n")

    # existential failure witness: order 17 graph 1, every degree-five root stuck, with (p, L)
    line, rot = corpus(17, 1)
    roots = []
    for r in degree_five(rot):
        s, adj, B = root_setup(rot, r)
        st = stuck_record(s, adj, B, e3)
        assert st is not None, f"root {r} not stuck under (p, L)"
        roots.append({"root": r, "vertex_order": s.V, "boundary_cyclic_order": B, "stuck": st})
    cert = header("existential_fail_witness", e3, graph_block("corpus", 17, 1, rot, line))
    cert.update({"degree_five_roots": degree_five(rot), "roots": roots})
    (OUT / "existential-fail-17-1-L.json").write_text(json.dumps(cert, indent=1) + "\n")

    for p in sorted(OUT.iterdir()):
        print(p.name, p.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
