#!/usr/bin/env python3
"""Job BO summary from out/bo{ipr,adv,c12,c24..c27}{,m}.jsonl (picyc.bo --jobbo) at (6,6,6,6,6), (5,5,6,6,6), (5,5,7,5,7) holes."""
import json
from collections import Counter, defaultdict
A = defaultdict(Counter); RL = defaultdict(Counter); MX = defaultdict(int); MXex = {}; ENDS = defaultdict(Counter); ALLC = defaultdict(list)
for tag in ('ipr', 'adv', 'c12', 'c24', 'c25', 'c26', 'c27'):
    for suf in ('', 'm'):
        try: fh = open('../out/bo%s%s.jsonl' % (tag, suf))
        except FileNotFoundError: print('missing', tag, suf); continue
        for l in fh:
            if '"jobbo"' not in l: continue
            r = json.loads(l); b = r['jobbo']; p = r['pattern']; src = 'IPR' if tag == 'ipr' else ('adversarial' if tag == 'adv' else 'census order %d' % r['n'])
            A[p]['holes'] += 1; A[p]['all-DL cycles'] += len(b['all_DL_cycles'])
            for c in b['all_DL_cycles']: ALLC[p].append((r['name'], r['hole'], suf or 'plantri') + tuple(c))
            for k, v in b['runlen'].items(): RL[(p, src)][int(k)] += v
            if b['maxrun'] > MX[(p, src)]: MX[(p, src)] = b['maxrun']; MXex[(p, src)] = (r['name'], r['hole'], suf or 'plantri')
            for k, v in b['ends'].items(): ENDS[p][k] += v
for p in sorted(A):
    print('=' * 20, p, dict(A[p]))
    if ALLC[p]: print('   all-DL cycles (name, hole, ori, w, L, #non-DL sigma-images), first 10:', ALLC[p][:10], ' min #nonDL:', min(c[5] for c in ALLC[p]))
    for (pp, src) in sorted(k for k in RL if k[0] == p):
        h = RL[(pp, src)]; print('   %-18s runs %8d  max %3d (%s)  length histogram %s' % (src, sum(h.values()), MX[(pp, src)], MXex[(pp, src)], dict(sorted(h.items())[:16])))
    E = ENDS[p]; tot = sum(E.values())
    lock = Counter(); kx = Counter(); kw = Counter(); last = Counter()
    for k, v in E.items():
        a, rest = k.split(' -> '); leave, sets, ln = rest.split(' | '); lock[leave.split()[0]] += v; last[a] += v
        xs = sets.split()[1]; ws = sets.split()[3]; kx[xs] += v; kw[ws] += v
    print('   run ends %d; leaving state: %s' % (tot, dict(lock)))
    print('   last DL state (type, degree word from x_j): %s' % dict(last.most_common(12)))
    print('   R+3 component ∩ link x_j..x_{j+4}: %s' % dict(kx.most_common(8)))
    print('   R+3 component ∩ outer w_j..w_{j+4}: %s' % dict(kw.most_common(12)))
    print('   top end keys:'); [print('     ', v, k) for k, v in E.most_common(15)]
