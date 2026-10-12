#!/usr/bin/env python3
"""Track T: one Phi step (rigid t -> in-shape t+1 -> rigid t+2) in chord-diagram terms, on sphere holes.

For every Hamiltonian DL-type state, runs are generated with tt_lib (matching form).  A state t of a run is
"rigid" if k(H_t) = 1 and t is not the first state of the run (so Q_{t-1} = F12_t is connected and DL-type).
For every Phi step we record (all on the chord diagram of H_t, chords C_t = E - H_t):
  yc   = |Y_t cap C_t|  (chords of the first flip loop), y1c = |Y_{t+1} cap C_{t+1}|
  D    = H_t ^ H_{t+2} = Y_t ^ Y_{t+1};  dC = |D cap C_t| (chords that become H-edges), dcomp = #components of D
  side changes of persistent chords (C_t cap C_{t+2}): side = region of S^2 - H containing the chord, with the
       reference side = side of the v-edge f_{k+1} (= e3 at t)
  interlace graph IG_t: bipartite?, #edges, GF(2) rank; |inside|, |outside|
usage: tt_phi.py GRAPHFILE (name:hole ... | stride off maxg) > out.jsonl"""
import sys, json
from collections import Counter
from tt_lib import (load_graphs, tait_dual, ham_states, run_from, run_back, chord_diagram, interlace,
                     bipartition, gf2_rank)


def sides(g, H, ref_edge):
    """side of every non-H edge: 0 if in the same region of S^2 - H as ref_edge, else 1 (primal computation)"""
    par = {}
    def f(x):
        par.setdefault(x, x)
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for e in range(g.m):
        if not (H >> e & 1):
            u, w = g.prim[e]; par[f(u)] = f(w)
    r0 = f(g.prim[ref_edge][0])
    return {e: (0 if f(g.prim[e][0]) == r0 else 1) for e in range(g.m) if not (H >> e & 1)}


def runs_of_hole(g, maxham=200000):
    hs = ham_states(g, limit=maxham); seen = set(); out = []
    for P, M in hs:
        if (P, M) in seen or g.dl_info(P, M) is None: continue
        fw, closed = run_from(g, P, M)
        if not closed and g.dl_info(*fw[-1]) is None: fw = fw[:-1]
        bw = run_back(g, P, M) if closed is not True else [(P, M)]
        states = list(reversed(bw))[:-1] + fw
        if closed is True: states = states + states[:3]     # unroll a closed orbit so Phi steps wrap
        for s in states: seen.add(s)
        out.append(states)
    return out


def ig_stats(g, P, M):
    order, chords = chord_diagram(g, P, M)
    A = interlace(chords)
    bip = bipartition(A) is not None
    ne = sum(bin(a).count('1') for a in A) // 2
    rk = gf2_rank(A)
    return dict(bip=bip, ne=ne, rk=rk, m=len(chords)), chords, A


def phi_records(g, states):
    recs = []
    kH = [g.kH(*s) for s in states]
    for t in range(1, len(states) - 2):
        if not (kH[t] == 1 and kH[t + 2] == 1 and kH[t + 1] == 2): continue
        P0, M0 = states[t]; P1, M1 = states[t + 1]; P2, M2 = states[t + 2]
        k0, X0, Y0 = g.dl_info(P0, M0); k1, X1, Y1 = g.dl_info(P1, M1)
        H0 = P0 | M0; H2 = P2 | M2; C0 = g.ALL & ~H0; C1 = g.ALL & ~(P1 | M1); C2 = g.ALL & ~H2
        D = H0 ^ H2
        s0 = sides(g, H0, g.fv[(k0 + 1) % 5]); k2 = g.dl_info(P2, M2)[0] if g.dl_info(P2, M2) else (k0 - 4) % 5
        s2 = sides(g, H2, g.fv[(k2 + 1) % 5])
        pers = [e for e in g.edges_of(C0 & C2)]
        flips = sum(1 for e in pers if s0[e] != s2[e])
        st0, _, _ = ig_stats(g, P0, M0); st2, _, _ = ig_stats(g, P2, M2)
        nin0 = sum(1 for e in s0 if s0[e] == 0); nin2 = sum(1 for e in s2 if s2[e] == 0)
        recs.append(dict(t=t, yc=bin(Y0 & C0).count('1'), y1c=bin(Y1 & C1).count('1'),
                         dC=bin(D & C0).count('1'), dH=bin(D & H0).count('1'), dcomp=g.ncomp(D),
                         pers=len(pers), flips=flips, nin=(nin0, nin2), ig0=st0, ig2=st2,
                         k=(k0, k2)))
    return recs


def main():
    a = sys.argv
    if ':' in a[2]:
        G = load_graphs(a[1], {s.rsplit(':', 1)[0] for s in a[2:]})
        specs = [(s.rsplit(':', 1)[0], int(s.rsplit(':', 1)[1])) for s in a[2:]]
    else:
        s, off, mx = int(a[2]), int(a[3]), int(a[4]); G = {}; specs = []
        for ln, l in enumerate(open(a[1])):
            if ln % s != off: continue
            p = l.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            G[p[0]] = rot; specs += [(p[0], h) for h in range(len(rot)) if len(rot[h]) == 5]
            if len(G) >= mx: break
    for nm, h in specs:
        g = tait_dual(G[nm], h)
        rs = runs_of_hole(g)
        for states in rs:
            recs = phi_records(g, states)
            if not recs: continue
            word = ''.join(str(min(g.kH(*s), 9)) for s in states)
            print(json.dumps(dict(g=nm, h=h, n=g.n, word=word, phi=recs)), flush=True)


if __name__ == '__main__':
    main()
