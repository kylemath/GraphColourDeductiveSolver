"""WP14 check 3: which structural ranks (p, s) satisfy Gate-D descent at which discovery roots.

Gate D at a root needs, for every p=1 state c, a <=2-swap endpoint e with (p(e), s(e)) < (1, s(c)).
Non-hard states always have a p=0 endpoint, so only the 172 HARD states impose constraints; their
complete endpoint lists come from the read-only tables.  Candidate s (all graph+colouring functions,
polynomial-time):
  H        1 if hard (no target within two swaps) else 0
  Lock     1 if Kempe-locked (Lemma 1: no target in one swap) else 0
  nLS      number of single swaps whose successor is locked (0 if unlocked)
  apexStar |XY-comp(apex) U XZ-comp(apex)|  (the two chains that lock the apex)
  apexSum  |XY-comp(apex)| + |XZ-comp(apex)|
  apexMin  min of the two
  kempe4   number of the four repeated-colour/far-singleton (Kempe/Heawood) swaps whose successor is locked
  q, lin   from the table (for reference)
plus lexicographic pairs (Lock, q), (Lock, lin), (Lock, apexStar).
"""
import json
from collections import defaultdict

from wp14_common import (all_components, comp_of, lock, ncol, pattern, setup, swap, tables, HERE)


def apex_chains(adj, col, B):
    i, _ = pattern([col[v] for v in B])
    s0, f1, f2 = B[i], B[(i + 2) % 5], B[(i + 3) % 5]
    k1 = comp_of(adj, col, s0, col[s0], col[f1])
    k2 = comp_of(adj, col, s0, col[s0], col[f2])
    return k1, k2


def feats(adj, col, B, V):
    if ncol(col, B) == 3:
        return None
    L = lock(adj, col, B)
    k1, k2 = apex_chains(adj, col, B)
    nls, kem = 0, 0
    hard = L
    if L:
        i, _ = pattern([col[v] for v in B])
        Aplus, Aminus = B[(i + 1) % 5], B[(i - 1) % 5]
        for pr, K in all_components(adj, col, V):
            c1 = swap(col, pr, K)
            l1 = ncol(c1, B) == 4 and lock(adj, c1, B)
            nls += l1
            if not l1:
                hard = False
            rho = col[Aplus]
            if rho in pr and (Aplus in K or Aminus in K) and not (B[i] in K):
                kem += l1
    return {"H": int(hard), "Lock": int(L), "nLS": nls, "apexStar": len(k1 | k2),
            "apexSum": len(k1) + len(k2), "apexMin": min(len(k1), len(k2)), "kempe4": kem}


RANKS = ["H", "Lock", "nLS", "apexStar", "apexSum", "apexMin", "kempe4", "q", "lin",
         ("Lock", "q"), ("Lock", "lin"), ("Lock", "apexStar"), ("nLS", "q"), ("kempe4", "q")]


def val(f, tq, r):
    if isinstance(r, tuple):
        return tuple(val(f, tq, x) for x in r)
    return tq[r] if r in ("q", "lin") else f[r]


def main():
    bad = defaultdict(list)
    for name, d in tables():
        if not d["hard_states"]:
            continue
        rot, r, B, V, adj = setup(d)
        failing = defaultdict(int)
        for h in d["hard_states"]:
            s = d["states"][h]
            col = dict(zip(V, s["coloring"]))
            f0 = feats(adj, col, B, V)
            assert f0["H"] == 1
            ends = []
            for e in s["endpoints"]:
                if e["endpoint_p"] == 0:
                    raise AssertionError("hard state with target endpoint")
                ce = dict(zip(V, e["endpoint"]))
                ends.append((feats(adj, ce, B, V), e["endpoint_features"]))
            for rk in RANKS:
                v0 = val(f0, s["features"], rk)
                if not any(val(fe, te, rk) < v0 for fe, te in ends):
                    failing[rk] += 1
        for rk in RANKS:
            if failing[rk]:
                bad[str(rk)].append(f"{name}({failing[rk]})")
    out = {str(rk): {"bad_roots": len(bad[str(rk)]), "list": bad[str(rk)]} for rk in RANKS}
    (HERE / "rank_probe.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out.items():
        print(k, v["bad_roots"], v["list"])


if __name__ == "__main__":
    main()
