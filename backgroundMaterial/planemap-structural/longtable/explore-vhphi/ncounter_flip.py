"""Local modifications of triply locked rigid states: all single edge flips and all pairs of flips that keep
(simple, proper colouring, min degree >= 5, x untouched, ring unchanged).  For each result test: rigid (six forests,
comps 1,2,2,1,1,1)?, triply locked?, and the neighbour types.  A hit would be: rigid + triply locked + both neighbours
locked (not separable).   [exploratory, post hoc]
Input: (a) plantri output at order N (rigid triply locked states found by own enumeration), or (b) a res_23-style file.
usage: python3 ncounter_flip.py plantri PLANTRI N   |   python3 ncounter_flip.py res FILE"""
import sys, subprocess, itertools
from collections import Counter
from ncounter_lib import *
import ncounter_p17 as P

def faces_of_edge(adj, a, b):
    return sorted(adj[a] & adj[b])

def flips(adj, x, ring):
    """list of (a,b,c,d) flippable edges: faces abc, abd (exactly two common neighbours), x not among a,b,c,d."""
    out = []
    n = len(adj)
    for a in range(n):
        for b in adj[a]:
            if b < a or a == x or b == x: continue
            cm = faces_of_edge(adj, a, b)
            if len(cm) != 2 or x in cm: continue
            c, d = cm
            if d in adj[c]: continue          # would create a multi-edge
            if len(adj[a]) < 6 or len(adj[b]) < 6: continue   # min degree 5 afterwards
            out.append((a, b, c, d))
    return out

def apply_flip(adj, f):
    a, b, c, d = f
    adj2 = [set(s) for s in adj]
    adj2[a].discard(b); adj2[b].discard(a); adj2[c].add(d); adj2[d].add(c)
    return adj2

def evaluate(adj, col, x, ring, cap=3000):
    if not proper(adj, col): return 'improper'
    if not is_rigid(adj, col, x): return 'notrigid'
    L = fan_locks(adj, col, x, ring, cap)
    if any(r[0] is not False for r in L): return 'rigid-notlocked'
    t = classify_both(adj, col, x, ring)
    K2 = comp_of(adj, col, ring[2], {D, G}, x); K0 = comp_of(adj, col, ring[0], {D, B}, x)
    s1 = kempe_class(adj, swapK(col, K2, D, G), x, ring[0], cap)
    s2 = kempe_class(adj, swapK(col, K0, D, B), x, ring[2], cap)
    return 'LOCKED3 c1sep=%s c2sep=%s types=%s,%s' % (s1[0], s2[0], t[0][0], t[1][0])

def run_state(adj, col, x, ring, label, tally):
    F = flips(adj, x, ring)
    tally['states'] += 1; tally['single-flip candidates'] += len(F)
    res = Counter()
    for f in F:
        a2 = apply_flip(adj, f)
        res[evaluate(a2, col, x, ring)] += 1
    for f1 in F:
        a1 = apply_flip(adj, f1)
        for f2 in flips(a1, x, ring):
            if f2[:2] == f1[2:4] or set(f2[:2]) == set(f1[:2]): continue
            res2 = evaluate(apply_flip(a1, f2), col, x, ring)
            res['2flip:' + res2] += 1
            tally['2flip-total'] += 1
    print(label, 'single-flip candidates', len(F), dict(res))
    for k, v in res.items(): tally[k] += v

def main():
    mode = sys.argv[1]; tally = Counter()
    if mode == 'plantri':
        pl, N = sys.argv[2], sys.argv[3]
        lines = [l for l in subprocess.run([pl, '-m5', '-a', N], capture_output=True, text=True).stdout.split('\n') if l and l[0].isdigit()]
        for gi, line in enumerate(lines):
            adjl = P.parse_p(line)
            for x in range(len(adjl)):
                if len(adjl[x]) != 5: continue
                adj = [set(s) for s in adjl]
                ro = adjl[x]
                if any(ro[(i + 2) % 5] in adj[ro[i]] for i in range(5)): continue
                for ring, col in P.states(adjl, x, ro):
                    if all(r[0] is False for r in fan_locks(adj, col, x, ring)):
                        run_state(adj, col, x, ring, f'graph{gi} x={x}', tally)
    else:
        for line in open(sys.argv[2]):
            if '| DISC' not in line: continue
            adj, col, x, ring = parse_disc('DISC' + line.split('| DISC')[1])
            run_state(adj, col, x, ring, 'n23', tally)
    print('TOTAL', dict(tally))
main()
