"""[exploratory] NightPotential: the closing permutation rho (c_L = rho(c_0) as actual colourings) of the 54 regenerated Gamma-cycles,
the role of its fixed colour, and the lap-closure of the three absolute pair ranks through the fixed colour."""
import json
from peng import Hole
from gamma_regen import D, L2I, trace_cycle
from collections import Counter
dump = json.load(open(D + 'jobak-66dump.json')); done = set(); T = Counter()
for r in dump:
    cid = (r['run'], r['name'], r['hole'], r['cycle'])
    if cid in done: continue
    done.add(cid); H = Hole(r['rotation'], r['hole'])
    c0 = {int(v): L2I[x] for v, x in r['colourings']['4'].items()}
    seq = trace_cycle(H, c0); cL = H.pi(seq[-1])[0]
    rho = {c0[v]: cL[v] for v in c0}
    f = [a for a in range(4) if rho[a] == a]; f = f[0]
    j, ty, k, (al, mu, A, B) = H.frame(c0)          # c0 is position 4 (R3k2)
    role = {al: 'alpha', mu: 'mu', A: 'A', B: 'B'}[f]
    T[('fixed colour role at R3k2', role, 'p colour', role if c0[H.p] == f else 'p not fixed')] += 1
    # period map: c_10 vs c_0 colours on the 2-ball are not a global permutation in general; record rho on pairings
    others = [a for a in range(4) if a != f]
    T[('rho on the three other colours is a 3-cycle', len({others[0], rho[others[0]], rho[rho[others[0]]]}) == 3)] += 1
for k in sorted(T, key=str): print(k, T[k])
