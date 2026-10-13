"""Chord count q(M) = |M n C| relative to the Ham cycle H of a Ham arc (M0 -> M1), along every D-walk leaving
the Ham arc forward (M1 -> M2 -> ...) and backward (... -> M_{-1} -> M0).  Tests monotonicity.
usage: hdist.py n"""
import sys, json, collections
from r0lib import G5, analyse
n = int(sys.argv[1])
fwd_prof = collections.Counter(); bwd_prof = collections.Counter(); nonmono = [0, 0]; tot = [0, 0]
for l in open(f'out/census_n{n}_p.jsonl'):
    r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
    A = analyse(g); D = A['D']; P = A['P']
    for (i0, i1) in A['ham']:
        H = P[i0] | P[i1]
        q = lambda x: bin(P[x] & ~H).count('1')
        def walk(path, succ, prof, k):
            nxt = list(succ(path[-1]))
            if not nxt:
                seq = tuple(q(x) for x in path)
                prof[seq] += 1; tot[k] += 1
                if any(seq[i + 1] < seq[i] for i in range(len(seq) - 1)): nonmono[k] += 1
                return
            for y in nxt: walk(path + [y], succ, prof, k)
        walk([i1], D.successors, fwd_prof, 0)
        walk([i0], D.predecessors, bwd_prof, 1)
print(f'n={n}: maximal walks from Ham arcs: forward {tot[0]} (non-monotone q: {nonmono[0]}), backward {tot[1]} (non-monotone: {nonmono[1]})')
print('  forward q-profiles (top):', fwd_prof.most_common(12))
print('  backward q-profiles (top):', bwd_prof.most_common(8))
