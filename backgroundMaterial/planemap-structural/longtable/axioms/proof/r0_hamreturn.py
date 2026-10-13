"""R0 reachability between Hamiltonian pairs.  Open R0 sequence M_0..M_{W-1} (perfect matchings, consecutive
disjoint, v-edge of M_t = f_{2-2t}), M_0 u M_1 Hamiltonian (normal form), and additionally
M_{T-1} u M_T Hamiltonian for the given T (lazy cuts: a non-Hamiltonian union is blocked by one of its cycles).
usage: r0_hamreturn.py n W T planar(0/1) [tlimit]"""
import sys, time
import sat_planar
from sat_t1v import Enc
from pysat.solvers import Cadical153
n, W, T, planar = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
tl = float(sys.argv[5]) if len(sys.argv) > 5 else 500
Enc._eager_loops = lambda self: None
enc = sat_planar.PEnc(n, W, 0, closed=False) if planar else Enc(n, W, 0, eager=0, closed=False)
s = Cadical153(bootstrap_with=enc.cl); t0 = time.time(); it = 0
while True:
    if time.time() - t0 > tl: print(f'n={n} W={W} T={T} planar={planar} -> TIMEOUT ({it} rounds)'); break
    if not s.solve(): print(f'n={n} W={W} T={T} planar={planar} -> UNSAT ({it} rounds, {time.time()-t0:.1f}s)'); break
    it += 1
    E, M, fv = enc.decode(s.get_model())
    U = M[T - 1] | M[T]
    adj = {}
    for e in U:
        a, b = enc.edges[e]; adj.setdefault(a, []).append(e); adj.setdefault(b, []).append(e)
    # trace the cycle through vertex 0
    seen = set(); x = 0; prev = None; cyc = []
    while True:
        e = [g for g in adj[x] if g != prev][0] if prev is not None else adj[x][0]
        cyc.append(e); seen.add(x); a, b = enc.edges[e]; x = b if a == x else a; prev = e
        if x == 0: break
    if len(seen) == n:
        print(f'n={n} W={W} T={T} planar={planar} -> SAT ({it} rounds, {time.time()-t0:.1f}s)'); break
    s.add_clause([-enc.Y[T - 1, e] if e in M[T - 1] else -enc.Y[T, e] for e in cyc])
