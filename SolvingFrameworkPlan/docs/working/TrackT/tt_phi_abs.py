#!/usr/bin/env python3
"""Track T: Phi-step chord statistics on abstract (non-planar) graphs logged by tt_abstract.py, and on
off-sphere / sphere triangulations given as GRAPHFILE name:hole.
usage: tt_phi_abs.py abs JSONL [minscore]  |  tt_phi_abs.py tri GRAPHFILE name:hole ..."""
import sys, json
from tt_lib import G5, load_graphs, tait_dual
from tt_phi import runs_of_hole, ig_stats


def phi_stats(g, states):
    kH = [g.kH(*s) for s in states]; out = []
    for t in range(1, len(states) - 2):
        if not (kH[t] == 1 and kH[t + 1] == 2 and kH[t + 2] == 1): continue
        P0, M0 = states[t]; P2, M2 = states[t + 2]
        D = (P0 | M0) ^ (P2 | M2); C0 = g.ALL & ~(P0 | M0)
        st0, _, _ = ig_stats(g, P0, M0); st2, _, _ = ig_stats(g, P2, M2)
        out.append(dict(dC=bin(D & C0).count('1'), dcomp=g.ncomp(D), ig0=st0, ig2=st2))
    return out


def main():
    if sys.argv[1] == 'abs':
        mins = int(sys.argv[3]) if len(sys.argv) > 3 else 6
        seen = set()
        for l in open(sys.argv[2]):
            d = json.loads(l)
            if d['event'] not in ('record', 'closed') or d.get('sc', 0) < mins: continue
            key = json.dumps(d['edges']) + str(d['rot'])
            if key in seen: continue
            seen.add(key)
            edges = [tuple(e) for e in d['edges']]
            ve = [k for k, (a, b) in enumerate(edges) if 0 in (a, b)]
            g = G5(d['n'], edges, [ve[i] for i in d['rot']])
            for states in runs_of_hole(g):
                ps = phi_stats(g, states)
                if ps:
                    print(json.dumps(dict(src='abs', sc=d['sc'], n=g.n,
                                          word=''.join(str(min(g.kH(*s), 9)) for s in states), phi=ps)))
    else:
        G = load_graphs(sys.argv[2], {s.rsplit(':', 1)[0] for s in sys.argv[3:]})
        for spec in sys.argv[3:]:
            nm, h = spec.rsplit(':', 1)
            g = tait_dual(G[nm], int(h))
            for states in runs_of_hole(g):
                ps = phi_stats(g, states)
                print(json.dumps(dict(src=spec, n=g.n, word=''.join(str(min(g.kH(*s), 9)) for s in states),
                                      phi=ps)))


if __name__ == '__main__':
    main()
