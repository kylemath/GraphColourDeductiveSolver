"""beyond-short-fill: check Lemma L3 and the new Lemma L4 (beyond-short-fill.md, section 4)
on the two SAVED order-24 graph records (24:6406, 24:7228) from
../audit/wp19-counterexamples.json, and report the exact joint (ell, kappa) over all
deletion states at their degree-5 holes.  No new graph is generated.
Output: beyond-short-fill-lemma.txt.
"""
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from beyond_short_fill_core import (all_distances, anatomy, component, kempe_moves,  # noqa
                                    canon)

SRC = HERE.parent / "audit" / "wp19-counterexamples.json"


def parse_ascii(a):
    """'n lists' with letters a.. for vertices; each list is the rotation of that vertex."""
    n, body = a.split(" ", 1)
    rot = [[ord(ch) - 97 for ch in part] for part in body.split(",")]
    assert len(rot) == int(n)
    for v, r in enumerate(rot):
        for w in r:
            assert v in rot[w]
    return rot


def faces_on_edge(rot, h, u):
    """The two vertices w with h-u-w a face (rotation neighbours of u around h)."""
    r = rot[h]
    i = r.index(u)
    return {r[(i - 1) % len(r)], r[(i + 1) % len(r)]}


def main():
    raw = SRC.read_bytes()
    print("input", SRC.name, "sha256", hashlib.sha256(raw).hexdigest())
    d = json.loads(raw)
    tot = Counter()
    for g in d["graphs"]:
        rot = g["ascii"]
        assert hashlib.sha256(rot.encode()).hexdigest() == g["ascii_sha256"]
        rot = parse_ascii(rot)
        adj = [sorted(r) for r in rot]
        n = len(adj)
        deg5 = [v for v in range(n) if len(adj[v]) == 5]
        t0 = time.time()
        states, ell, kap = all_distances(adj, 4, deg5)
        print(f"\n=== 24:{g['graph_index']}  ({sum(len(x) for x in states.values())} deletion "
              f"states over all holes; {time.time() - t0:.1f}s)")
        J = Counter()
        for h in deg5:
            for s in states[h]:
                J[(ell.get((h, s)), kap[h].get(s))] += 1
        print("  joint (ell, kappa), all colourings of T - v, v of degree 5 (no fan filter):")
        for key in sorted(J, key=str):
            print("    ", key, J[key])
        nofill = sum(c for (l_, k_), c in J.items() if k_ is None)
        print("  nofill states:", nofill)
        # ---- lemma checks on every ell = 3 start
        stats = Counter()
        for h in deg5:
            for s in states[h]:
                if ell.get((h, s)) != 3:
                    continue
                k = kap[h][s]
                tag = "kappa>3" if k > 3 else "kappa=3"
                # L3(a): no shortest path starts with a swap
                swap_first = any(ell.get((h, canon(nc))) == 2
                                 for _, nc in kempe_moves(adj, 4, h, s))
                stats[(tag, "a Kempe first move is on a shortest path")] += swap_first
                stats[(tag, "starts")] += 1
                an = anatomy(adj, 4, h, s, ell)
                stats[(tag, "decompositions S K1 K2")] += len(an)
                uni = True
                condB = False
                for r in an:
                    if not r["sigma_in_pair"]:
                        stats[(tag, "K1 avoids sigma")] += 1
                        uni = False
                        continue
                    rho = r["rho"]
                    m_rho = sum(1 for y in adj[h] if s[y] == rho)
                    if r["h_in_K1"]:
                        stats[(tag, "h in K1")] += 1
                        if not r["rho_nbrs_u_in_K1"]:
                            stats[(tag, "h in K1, u has no rho-nbr in K1")] += 1
                            K1 = set(r["K1"]) - {h}
                            # number of {sigma,rho}-components of G-h meeting K1 - h
                            pieces, seen = 0, set()
                            for x in K1:
                                if x not in seen:
                                    pieces += 1
                                    seen |= component(adj, h, s, x, (r["sigma"], rho))
                            stats[(tag, "   ... and kappa <= #pieces (L4b)")] += (k <= pieces)
                            stats[(tag, "   ... #pieces <= m_rho")] += (pieces <= m_rho)
                    else:
                        stats[(tag, "h not in K1")] += 1
                        ok = (not r["K1_meets_Nh"] and r["rho_nbrs_u_in_K1"]
                              and r["rho_nbrs_u_in_Ht"])
                        stats[(tag, "h not in K1 and L4a structure holds")] += bool(ok)
                    if not r["rho_nbrs_u_in_Ht"]:
                        uni = False
                    w = faces_on_edge(rot, h, r["u"])
                    if any(s[x] == rho for x in w) and (not r["h_in_K1"]):
                        condB = True
                stats[(tag, "every decomposition: u has a rho-nbr in H_t (L4c)")] += uni
                stats[(tag, "Conjecture B pattern present (h not in K1, face vertex rho)")] += condB
                tot[(k,)] += 1
        for key in sorted(stats):
            print("  ", key, stats[key])
    print("\nell = 3 starts by kappa over both graphs:", dict(tot))


if __name__ == "__main__":
    main()
