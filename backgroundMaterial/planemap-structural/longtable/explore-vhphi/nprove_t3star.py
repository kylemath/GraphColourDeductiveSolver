"""nprove_t3star.py: uniform third step.  c3 := swap of the [beta,gamma]-component of u4 in c2 (Case I and II alike).
Reports, per neighbour c' / c'': Case, sizes |K|,|Q|,|E|,|R| of the four swapped components, and whether c3 is 'good'
(3-coloured ring, or broken chain) -- T3* : c3 good.  Mirror for c'' (roles u3<->u4 swapped, beta<->gamma)."""
import sys
from nprove_lib import *
fn = sys.argv[1]
tot = good = 0
for i, line in enumerate(l for l in open(fn) if 'DISC' in l):
    col, E = parse(line); x, adj = build(col, E)
    cp, cpp, K2, K0 = neighbours_cprime(adj, x, col + [0])
    for nm, c0, apex, K, (p1, p2, pr) in (("c'", cp, 0, K2, ((AL, GA), (AL, BE), (BE, GA))), ("c''", cpp, 2, K0, ((AL, BE), (AL, GA), (BE, GA)))):
        u_a, u_b = (4, 3) if nm == "c'" else (3, 4)   # u_a: the vertex whose chains are swapped
        cs, ix = comps(adj, c0, p1, x); Q = cs[ix[u_a]]; c1 = swap(c0, Q, *p1)
        cs, ix = comps(adj, c1, p2, x); Ec = cs[ix[u_a]]; c2 = swap(c1, Ec, *p2)
        cs, ix = comps(adj, c2, pr, x); R = cs[ix[u_a]]; c3 = swap(c2, R, *pr)
        ring2 = len({c3[r] for r in range(5)})
        gd = chain_broken(adj, x, c3, apex)
        cas = (case_cprime if nm == "c'" else mirror_case)(adj, x, c0)[0]
        tot += 1; good += gd
        print(i, nm, "Case", cas, "|K|,|Q|,|E|,|R| =", len(K), len(Q), len(Ec), len(R), "ring colours", ring2, "c3 good" if gd else "c3 NOT good")
print("c3 good in", good, "of", tot)
