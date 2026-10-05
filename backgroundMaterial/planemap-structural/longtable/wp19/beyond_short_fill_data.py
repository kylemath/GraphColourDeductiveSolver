"""beyond-short-fill: (ell, kappa) from the SAVED WP19 outputs wp19-P1/P2/P3.json (post hoc).
Streams each file graph by graph (P3 is ~200 MB).  No graph is recomputed.
Output: beyond-short-fill-data.txt.

Per pair (v, fan) the outputs store only the two marginals hist_l and hist_k over the
admitted starts S(v, tau).  The joint is reconstructed as far as the marginals allow:
  * ell <= 2  <=>  kappa = ell  (MathShortFillTheorem; and kappa <= 2 forces ell <= kappa <= 2),
    so for j = 0,1,2 the classes {ell = j} and {kappa = j} coincide: n(j,j) = hist_l[j] = hist_k[j]
    (checked per pair);
  * kappa = 3 forces ell = 3, so n(3,3) = hist_k[3];
  * the rest (ell in {3,4}, kappa in {4,5}) satisfies
        n(3,4) + n(4,4) = k4,  n(3,5) + n(4,5) = k5,  n(4,4) + n(4,5) = l4,  n(3,4)+n(3,5) = l3-k3,
    which is exact when k5 = 0 or l4 = 0 and otherwise leaves one free parameter n(4,5).
Counts are pair-weighted: a start at v admitted by several fans is counted once per fan.
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = ["wp19-P1.json", "wp19-P2.json", "wp19-P3.json"]


def stream_graphs(path, chunk=1 << 23):
    """Yield (graph_record, sha_state) one at a time; also hashes the whole file."""
    dec = json.JSONDecoder()
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        buf = ""
        started = False
        pos = 0
        pending = b""
        while True:
            data = f.read(chunk)
            sha.update(data)
            if data:
                pending += data
                try:
                    text = pending.decode("utf-8")
                    pending = b""
                except UnicodeDecodeError as e:
                    text = pending[:e.start].decode("utf-8")
                    pending = pending[e.start:]
                buf = buf[pos:] + text
                pos = 0
            if not started:
                i = buf.find('"graphs":[')
                if i < 0:
                    if not data:
                        raise ValueError("no graphs array")
                    continue
                pos = i + len('"graphs":[')
                started = True
            while True:
                while pos < len(buf) and buf[pos] in " \n\r\t,":
                    pos += 1
                if pos < len(buf) and buf[pos] == "]":
                    # drain rest of file for the hash
                    while data:
                        data = f.read(chunk)
                        sha.update(data)
                    yield None, sha.hexdigest()
                    return
                try:
                    obj, end = dec.raw_decode(buf, pos)
                except json.JSONDecodeError:
                    break
                pos = end
                yield obj, None
            if not data:
                raise ValueError("truncated")


def pair_joint(P):
    hl, hk = P["hist_l"], P["hist_k"]
    for j in ("0", "1", "2"):
        assert hl[j] == hk[j], ("ell<=2 class mismatch", P["v"], P["fan_index"], j)
    assert all(hl.get(x, 0) == 0 for x in ("5", "6", "capped"))
    assert all(hk.get(x, 0) == 0 for x in ("6", "7", "capped", "nofill")), "kappa > 5 present"
    l3, l4 = hl["3"], hl["4"]
    k3, k4, k5 = hk["3"], hk["4"], hk["5"]
    assert l3 + l4 == k3 + k4 + k5 + sum(hk.get(x, 0) for x in ("6", "7", "capped", "nofill"))
    lo = max(0, l4 - k4)
    hi = min(l4, k5)
    assert lo <= hi
    exact = {(j, j): hl[str(j)] for j in range(3)}
    exact[(3, 3)] = k3
    return exact, (l3, l4, k3, k4, k5), (lo, hi)


def main():
    out_tot = Counter()
    per_order = defaultdict(Counter)
    ambiguous = []
    k5_pairs = []
    nofill = capped = 0
    maxk = 0
    graphs = 0
    for fn in FILES:
        path = HERE / fn
        print(f"--- {fn}")
        g_in = 0
        for g, sha in stream_graphs(path):
            if g is None:
                print(f"    sha256 {sha}; graphs {g_in}")
                break
            g_in += 1
            graphs += 1
            o = g["order"]
            for P in g["pairs"]:
                if P.get("empty") or not P["hist_l"]:
                    continue
                hk = P["hist_k"]
                nofill += hk.get("nofill", 0)
                capped += hk.get("capped", 0) + P["hist_l"].get("capped", 0)
                for x in range(8):
                    if hk.get(str(x), 0):
                        maxk = max(maxk, x)
                exact, (l3, l4, k3, k4, k5), (lo, hi) = pair_joint(P)
                C = per_order[o]
                for key, c in exact.items():
                    C[key] += c
                C["pairs"] += 1
                C["starts"] += P["starts"]
                # remaining block
                if k5 == 0 or l4 == 0:
                    n45 = 0  # k5 == 0, or l4 == 0 forces n(4,5) = 0
                    n44 = l4 - n45
                    C[(4, 4)] += n44
                    C[(4, 5)] += n45
                    C[(3, 4)] += k4 - n44
                    C[(3, 5)] += k5 - n45
                else:
                    ambiguous.append((o, g["graph_index"], P["v"], P["fan_index"],
                                      (l3, l4, k3, k4, k5), (lo, hi)))
                    C["amb_pairs"] += 1
                    C["amb_l3_minus_k3"] += l3 - k3
                    C["amb_l4"] += l4
                    C["amb_k4"] += k4
                    C["amb_k5"] += k5
                    C["amb_n45_lo"] += lo
                    C["amb_n45_hi"] += hi
                if k5:
                    k5_pairs.append((o, g["graph_index"], P["v"], P["fan_index"],
                                     (l3, l4, k3, k4, k5)))
    print(f"\ngraphs read: {graphs}")
    keys = [(0, 0), (1, 1), (2, 2), (3, 3), (3, 4), (3, 5), (4, 4), (4, 5)]
    print("\npair-weighted joint (ell, kappa) by order (unambiguous pairs only for the last four):")
    print("order  pairs  starts  " + "  ".join(f"{k}" for k in keys))
    T = Counter()
    for o in sorted(per_order):
        C = per_order[o]
        T.update(C)
        print(f"{o:5d} {C['pairs']:6d} {C['starts']:9d}  " + "  ".join(f"{C[k]}" for k in keys))
    print("total", T["pairs"], T["starts"], "  ".join(f"{T[k]}" for k in keys))
    for o in sorted(per_order):
        C = per_order[o]
        if C["amb_pairs"]:
            print(f"order {o}: {C['amb_pairs']} ambiguous pairs (k5>0 and l4>0): "
                  f"l3-k3={C['amb_l3_minus_k3']}, l4={C['amb_l4']}, k4={C['amb_k4']}, "
                  f"k5={C['amb_k5']}, n(4,5) in [{C['amb_n45_lo']}, {C['amb_n45_hi']}]")
    print("\nambiguous pairs:")
    for a in ambiguous:
        print("  ", a)
    print(f"\npairs with kappa = 5 present ({len(k5_pairs)}): (order, graph, v, fan, "
          f"(l3, l4, k3, k4, k5))")
    for a in k5_pairs:
        print("  ", a)
    print(f"\nmax kappa observed: {maxk};  nofill total: {nofill};  capped total: {capped}")


if __name__ == "__main__":
    sys.exit(main())
