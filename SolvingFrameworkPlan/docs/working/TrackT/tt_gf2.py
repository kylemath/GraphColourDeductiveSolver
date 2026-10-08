#!/usr/bin/env python3
"""Track T: GF(2) / Z4 invariants of the chord diagram (H_t, C_t) at Hamiltonian states along runs.

For a Hamiltonian state (P, M): circle = H (positions as in tt_lib.chord_diagram, v = one point for parity),
chords C.  Interlace matrix I (GF(2)), Delta = diag(chord joins two points of the same parity along H).
Checks the circuit-partition formula  k(F12) + k(F13) = 1 + nullity(I + Delta)   (F12 = M u C, F13 = P u C); with v blown up into 3 points the
   smoothings at v agree with the DL pairings, so the formula reads k(F12) + k(F13) + 2 = 1 + nullity(I + Delta).
Invariants recorded per Hamiltonian state:
   rk  = rank I,  nu = nullity(I + Delta),  nd = #Delta,  gauss sum G(q) of the Z4 form
   q(x) = sum_i Delta_i x_i + 2 sum_{i<j} I_ij x_i x_j  (mod 4)  -> (|G|^2 exponent, phase in Z8) when nonzero.
usage: tt_gf2.py tri GRAPHFILE name:hole ... | tt_gf2.py abs JSONL minscore"""
import sys, json, cmath, math
import numpy as np
from tt_lib import G5, load_graphs, tait_dual, chord_diagram, interlace, gf2_rank
from tt_phi import runs_of_hole


def mats(g, P, M):
    order, chords = chord_diagram(g, P, M)
    # parity: v's three blow-up points get the same position (index of first v point)
    pos_par = []
    nv = len(order) - 3
    for a, b, e in chords:
        pos_par.append((a - b) % 2 == 0)     # v blown up into 3 points (virtual edges classes 3, 2)
    A = interlace(chords)
    D = [1 if p else 0 for p in pos_par]
    return A, D


def nullity_plus_diag(A, D):
    m = len(A)
    rows = [A[i] ^ (D[i] << i) for i in range(m)]
    return m - gf2_rank(rows)


def gauss(A, D):
    m = len(A)
    if m > 24: return None
    X = np.arange(1 << m, dtype=np.int64)
    bits = [((X >> i) & 1).astype(np.int8) for i in range(m)]
    q = np.zeros(1 << m, dtype=np.int64)
    for i in range(m):
        if D[i]: q += bits[i]
        s = np.zeros(1 << m, dtype=np.int64)
        for j in range(i + 1, m):
            if A[i] >> j & 1: s += bits[j]
        q += 2 * bits[i] * s
    q %= 4
    cnt = np.bincount(q, minlength=4)
    G = complex(cnt[0] - cnt[2], cnt[1] - cnt[3])
    if abs(G) < 1e-9: return ('zero',)
    r = abs(G); ph = cmath.phase(G) / (2 * math.pi) * 8
    return (round(2 * math.log2(r) - m), int(round(ph)) % 8)


def state_inv(g, P, M, do_gauss=True):
    A, D = mats(g, P, M)
    nu = nullity_plus_diag(A, D)
    k12 = g.ncomp(M | (g.ALL & ~(P | M))); k13 = g.ncomp(P | (g.ALL & ~(P | M)))
    return dict(rk=gf2_rank(list(A)), nu=nu, nd=sum(D), m=len(A), k12=k12, k13=k13,
                fok=(k12 + k13 + 2 == 1 + nu), gs=gauss(A, D) if do_gauss else None)


def process(g, tag, out):
    for states in runs_of_hole(g):
        kH = [g.kH(*s) for s in states]
        if 1 not in kH: continue
        inv = [state_inv(g, *s) if kH[i] == 1 else None for i, s in enumerate(states)]
        out.write(json.dumps(dict(src=tag, n=g.n, word=''.join(str(min(k, 9)) for k in kH), inv=inv)) + '\n')
        out.flush()


def main():
    if sys.argv[1] == 'abs':
        mins = int(sys.argv[3]); seen = set()
        for l in open(sys.argv[2]):
            d = json.loads(l)
            if d['event'] not in ('record', 'closed') or d.get('sc', 0) < mins: continue
            key = json.dumps(d['edges']) + str(d['rot'])
            if key in seen: continue
            seen.add(key)
            edges = [tuple(e) for e in d['edges']]
            ve = [k for k, (a, b) in enumerate(edges) if 0 in (a, b)]
            process(G5(d['n'], edges, [ve[i] for i in d['rot']]), 'abs', sys.stdout)
    else:
        G = load_graphs(sys.argv[2], {s.rsplit(':', 1)[0] for s in sys.argv[3:]})
        for spec in sys.argv[3:]:
            nm, h = spec.rsplit(':', 1)
            process(tait_dual(G[nm], int(h)), spec, sys.stdout)


if __name__ == '__main__':
    main()
