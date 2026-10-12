#!/usr/bin/env python3
"""Track T: maximal Hamiltonian-anchored Q-runs in the matching form, from scratch (no colouring engine).

For each hole: enumerate all Hamiltonian states (P, M) (H = P|M Hamiltonian through v, v-edges f_k in M, f_{k+2}
in P) such that (P, M) is DL-type (E - M connected figure-eight with DL pairing).  From each, iterate forward and
backward while DL-type.  Record the k(H) word of the maximal run, and the NRC-M run length = longest stretch with
k(H) = 1 at every other state (alternating positions) and DL-type throughout.
usage: tt_runs.py GRAPHFILE name:hole ... > out.jsonl"""
import sys, json
from tt_lib import load_graphs, tait_dual, ham_states, run_from, run_back


def nrcm_len(word):
    """longest window of consecutive states such that k(H)=1 at every other state (starting with the first or
    second state of the window)"""
    best = 0; L = len(word)
    for par in (0, 1):
        cur = 0
        for i in range(L):
            if (i % 2 == par and word[i] == 1) or (i % 2 != par):
                cur += 1
            else:
                cur = 0
            # window must also start correctly: handled by allowing either parity
            best = max(best, cur)
    return best


def analyse_hole(rot, h, maxham=200000):
    g = tait_dual(rot, h)
    hs = ham_states(g, limit=maxham)
    seen = set(); res = []
    for P, M in hs:
        if (P, M) in seen: continue
        if g.dl_info(P, M) is None: continue
        fw, closed = run_from(g, P, M)
        if not closed and g.dl_info(*fw[-1]) is None: fw = fw[:-1]   # drop the non-DL image
        bw = run_back(g, P, M) if closed is not True else [(P, M)]
        states = list(reversed(bw))[:-1] + fw
        for s in states: seen.add(s)
        word = [g.kH(*s) for s in states]
        res.append(dict(L=len(states), closed=closed, word=''.join(str(min(w, 9)) for w in word),
                        nrcm=nrcm_len(word)))
    return g, len(hs), res


def main():
    G = load_graphs(sys.argv[1], {s.rsplit(':', 1)[0] for s in sys.argv[2:]})
    for spec in sys.argv[2:]:
        nm, h = spec.rsplit(':', 1); h = int(h)
        g, nh, res = analyse_hole(G[nm], h)
        best = max(res, key=lambda r: (r['nrcm'], r['L'])) if res else None
        print(json.dumps(dict(g=nm, h=h, n=g.n, ham=nh, runs=len(res),
                              maxL=max([r['L'] for r in res], default=0),
                              maxNRCM=max([r['nrcm'] for r in res], default=0),
                              closed=[r for r in res if r['closed']][:3], best=best)), flush=True)


if __name__ == '__main__':
    main()
