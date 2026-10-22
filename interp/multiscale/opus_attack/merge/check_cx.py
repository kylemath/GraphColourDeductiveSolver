# Stand-alone verifier for a counterexample file.   usage: python3 check_cx.py cx_ell8.pkl R w
# Checks: A, B, U = A cup B are near-triangulated discs in the triangular lattice; every interior vertex of U has
# degree 6 (U flat, no vortices); c_A, c_B proper; A and B weakly 1-level by the AUTHORS' code (hierarchy/weak/wk.py:
# Disc pockets + tau_walk); then, for each of the 24 renamings pi, that U \ (N_R(conflicts) cup N_w(dU)) carries a
# loop along which the glued colouring has non-zero height monodromy, so NO recolouring of N_R(conflicts) cup N_w(dU)
# yields a proper colouring of U (a fortiori no weakly level one).  No SAT solver is involved in this check.
import sys, pickle
sys.dont_write_bytecode = True
import pysat_stub, wk
from lat import Lat, bfs, disc_info, PERMS, INC
from heights import colouring

def main(path, R, w):
    d = pickle.load(open(path, 'rb')); g = Lat(d['pts']); A = set(d['A']); B = set(d['B']); U = A | B
    col = colouring(d['h']); cA = {v: col[v] for v in A}; cB = {v: col[v] for v in B}
    iU = disc_info(g, U); disc_info(g, A); disc_info(g, B)
    assert all(g.deg[v] == 6 and all(x in U for x in g.adj[v]) for v in U - iU['bset']), 'U not flat'
    for S, c in ((A, cA), (B, cB)):
        assert all(c[u] != c[x] for u in S for x in g.adj[u] if x in S), 'improper'
    DA, DB = wk.Disc(g, A), wk.Disc(g, B)
    tA = max(wk.tau_walk(W, cA) for W in DA.pockets); tB = max(wk.tau_walk(W, cB) for W in DB.pockets)
    print('nU=%d nA=%d nB=%d  chords A=%d B=%d  pockets A=%d B=%d  max pocket tau (authors code) A=%.3f B=%.3f  strict tau(A)=%.3f'
          % (len(U), len(A), len(B), len(DA.chords), len(DB.chords), len(DA.pockets), len(DB.pockets), tA, tB, wk.tau_walk(DA.whole, cA)))
    assert tA <= 1 + 1e-9 and tB <= 1 + 1e-9, 'not weakly level'
    dU = bfs(g.adj, list(iU['bset']), U)
    blocked = 0
    for p in PERMS:
        c = dict(cA); c.update({v: p[cB[v]] for v in B})
        K = set(x for u in A for y in g.adj[u] if y in B and c[u] == c[y] for x in (u, y))
        dK = bfs(g.adj, list(K), U) if K else {}
        rest = set(v for v in U if dK.get(v, 99) > R and dU[v] > w)
        # integrate the height of the glued colouring on each component of U \ Z; report the first inconsistency
        h = {}; witness = None
        for s in rest:
            if s in h or witness: continue
            h[s] = (0, 0); st = [s]
            while st and not witness:
                u = st.pop()
                for x in g.adj[u]:
                    if x not in rest: continue
                    l = c[u] ^ c[x]; assert l, 'conflict outside Z?'
                    e = INC[l]; sg = g.sgn(u, x); hx = (h[u][0] + sg*e[0], h[u][1] + sg*e[1])
                    if x in h:
                        if h[x] != hx: witness = (u, x, h[x], hx); break
                    else: h[x] = hx; st.append(x)
        ok = witness is not None; blocked += ok
        print('renaming %s: |conflicts|=%d  |Z|=%d  obstruction=%s%s' % (p, len(K), len(U) - len(rest), ok,
              '' if not ok else '  (edge %s-%s closes a loop with monodromy %s)' % (g.pts[witness[0]], g.pts[witness[1]],
              tuple(a - b for a, b in zip(witness[3], witness[2])))))
    print('VERDICT: %d/24 renamings obstructed at R=%d, w=%d -> %s' % (blocked, R, w,
          'no admissible merge (claim fails)' if blocked == 24 else 'not a counterexample at these (R,w)'))

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
