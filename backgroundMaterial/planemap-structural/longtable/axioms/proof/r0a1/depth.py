"""Anatomy on the exhaustive census (D acyclic there): for every Ham arc M0 -> M1, the longest walk ending
at M0 (back) and starting at M1 (fwd) in D; longest path in D overall; out-degree profile.
Also the sink lemma check: a PM with an in-arc is a sink iff in E - M the loop through f_{k+2} does not
contain f_{k+3}.  usage: depth.py n"""
import sys, json, collections
import networkx as nx
from r0lib import G5, analyse
def loop_partner(g, M, s):
    """in E - M, follow the loop leaving v by f_s; return the index of the v-edge it returns by"""
    S = ((1 << g.m) - 1) & ~M
    e = g.fv[s]; x = g.other(e, 0); last = e
    while x != 0:
        nxt = [f for f in g.inc[x] if (S >> f) & 1 and f != last]
        if len(nxt) != 1: return None
        last = nxt[0]; x = g.other(last, x)
    return g.fidx[last]

if __name__ == '__main__':
    n = int(sys.argv[1])
    mx = collections.Counter(); hist_back = collections.Counter(); hist_fwd = collections.Counter()
    longest = 0; sinkcheck = [0, 0]; outdeg = collections.Counter()
    for l in open(f'out/census_n{n}_p.jsonl'):
        r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
        A = analyse(g); D = A['D']
        back = {}; fwd = {}
        for x in nx.topological_sort(D):
            back[x] = max([back[p] + 1 for p in D.predecessors(x)], default=0)
        for x in reversed(list(nx.topological_sort(D))):
            fwd[x] = max([fwd[s] + 1 for s in D.successors(x)], default=0)
        longest = max(longest, max(back.values()))
        for (i, j) in A['ham']:
            hist_back[back[i]] += 1; hist_fwd[fwd[j]] += 1
            mx['through'] = max(mx['through'], back[i] + 1 + fwd[j])
        for x in D.nodes:
            if D.in_degree(x) == 0: continue
            k = A['ks'][x]; outdeg[D.out_degree(x)] += 1
            cont = loop_partner(g, A['P'][x], (k + 2) % 5) == (k + 3) % 5
            sinkcheck[0 if cont == (D.out_degree(x) > 0) else 1] += 1
    print(f'n={n}: longest path in any D: {longest} arcs; longest path through a Ham arc: {mx["through"]} arcs')
    print('   back-depth into Ham-arc tails:', dict(sorted(hist_back.items())))
    print('   fwd-depth from Ham-arc heads:', dict(sorted(hist_fwd.items())))
    print('   out-degree of PMs with an in-arc:', dict(sorted(outdeg.items())), ' sink lemma agree/disagree:', sinkcheck)
