"""Coordinator test, full form: R0 with NO crossing clauses, only "e1 before e0 along H_t at EVERY
Hamiltonian state t" (H_t = M_{t-1} u M_t Hamiltonian, frame k = k_t, e_i = f_{k-2+i}; H_t numbered from the
far end of e2 (position 1) to the far end of e4 (position n-1)).  Lazy: solve, check every Ham state of the
decoded sequence, cut the violating state (its two matchings + the two chords), repeat.
usage: order_cegar.py n L [tlimit]"""
import sys, time
from pysat.solvers import Glucose4
from r0sat import R0Enc
n, L = int(sys.argv[1]), int(sys.argv[2]); tl = float(sys.argv[3]) if len(sys.argv) > 3 else 300
POS = 'poscontrol' in sys.argv
enc = R0Enc(n, L, 'r0', POS, not POS)
cl = enc.clauses()
J = range(2, n - 1)
for a in J:          # the normal-form Ham state t = 1 directly: pos(f3) < pos(f4)
    for b in J:
        if a > b: cl.append([-enc.pres[('v3', 0, a)], -enc.pres[('v4', 0, b)]])
s = Glucose4(bootstrap_with=cl)
t0 = time.time(); rounds = 0
def lit_true(e): return [] if enc.pres[e] is None else [-enc.pres[e]]
while True:
    if time.time() - t0 > tl: print(f'n={n} L={L}: TIMEOUT after {rounds} cuts'); break
    if not s.solve(): print(f'n={n} L={L}: UNSAT after {rounds} cuts ({time.time()-t0:.1f}s)'); break
    edges, N = enc.decode(s.get_model())
    vend = {}
    for e in edges:
        if e[0] in ('f0', 'f2') or e[0].startswith('v'):
            s_ = int(e[0][1]); vend[s_] = (e, e[2] if e[1] == 0 else e[1])
    bad = False
    for t in range(1 if POS else 0, L):
        A, B = N[(t - 1) % L], N[t]
        Hs = A + B
        adj = {}
        for e in Hs: adj.setdefault(e[1], []).append(e[2]); adj.setdefault(e[2], []).append(e[1])
        k = enc.k[t]
        e2, e4 = (k) % 5, (k + 2) % 5
        start = vend[e2][1]
        seq = [start]; prev = 0; x = start
        while x != 0:
            nx_ = [y for y in adj[x] if y != prev]
            prev, x = x, nx_[0]
            if x != 0: seq.append(x)
        if len(seq) != n - 1: continue        # not Hamiltonian
        pos = {x: i + 1 for i, x in enumerate(seq)}
        p0, p1 = pos[vend[(k - 2) % 5][1]], pos[vend[(k - 1) % 5][1]]
        if p1 < p0: continue                  # e1 before e0: fine
        bad = True; rounds += 1
        if POS: print('   POSITIVE CONTROL VIOLATION at t =', t)
        cut = [-enc.m[(t - 1) % L][e] for e in A] + [-enc.m[t][e] for e in B]
        cut += lit_true(vend[(k - 2) % 5][0]) + lit_true(vend[(k - 1) % 5][0])
        s.add_clause(cut)
    if not bad:
        from r0sat import verify
        info, g = verify(enc, edges, N)
        print(f'n={n} L={L}: SAT after {rounds} cuts ({time.time()-t0:.1f}s): order condition holds at every Ham state;',
              f'Ham states at t = {[t for t in info["ham_arcs"]]} (arc t -> t+1), planar_rot = {info["planar_rot"]}')
        break
