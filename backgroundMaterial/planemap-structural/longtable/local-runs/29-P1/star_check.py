#!/usr/bin/env python3
"""[exploratory] NightP1 section 4: the 'star' form. In each sigma-group containing a positive cycle, let M be its most negative cycle.
Star(g): M is sigma-adjacent (undirected, one hop) to every positive cycle of g, and -Lambda(M) >= sum of Lambda over the positive cycles of g.
Star_rem(g) (same with -rem(M) in place of -Lambda(M)) implies P1^str on g, hence charge-back P1 and sigma-C on g. Output star-check.txt."""
import json, os
from collections import Counter, defaultdict
here = os.path.dirname(os.path.abspath(__file__)); out = []; C = Counter(); bad = []
for o in ['17', '20', '21', '22', '23', '24']:
    for m in ['', 'm']:
        for l in open(os.path.join(here, 'out%s%s.jsonl' % (o, m))):
            if '"p1"' not in l: continue
            r = json.loads(l); p = r['p1']; cyc = {int(k): v for k, v in p['cyc'].items()}; grp = {int(k): v for k, v in p['grp'].items()}
            adj = defaultdict(set)
            for a, b in p['edges']: adj[a].add(b); adj[b].add(a)
            hit = Counter()
            for Z, ls in p['links'].items():
                for i, T, ty, kd, l1, l2, f, e in ls:
                    if f >= 0 and ty == 3 and T != int(Z) and cyc[T][0] <= 0: hit[T] += 3 * f - 1
            groups = defaultdict(list)
            for c, g in grp.items(): groups[g].append(c)
            for g, cs in groups.items():
                P = [c for c in cs if cyc[c][0] > 0]
                if not P: continue
                C['groups'] += 1; M = min(cs, key=lambda c: cyc[c][0]); sup = sum(cyc[c][0] for c in P)
                adjall = all(M in adj[z] for z in P); big = -cyc[M][0] >= sup; bigrem = -(cyc[M][0] + hit[M]) >= sup
                C['bigrem'] += bigrem; C['starrem'] += adjall and bigrem
                C['adj'] += adjall; C['big'] += big; C['star'] += adjall and big
                # distance from each positive cycle to M
                if not adjall:
                    for z in P:
                        if M in adj[z]: continue
                        d = {z: 0}; q = [z]
                        while q:
                            x = q.pop(0)
                            for y in adj[x]:
                                if y not in d: d[y] = d[x] + 1; q.append(y)
                        C['dist%d' % d.get(M, -1)] += 1
                        bad.append((o + m, r['name'], r['hole'], r.get('pattern'), z, cyc[z][0], cyc[z][1], 'M', M, cyc[M][0], 'dist', d.get(M), 'nbrs', sorted((y, cyc[y][0]) for y in adj[z])[:8]))
out.append('sigma-groups with a positive cycle (gentri orders 17, 20-24, both orientations): %d' % C['groups'])
out.append('M (most negative cycle of the group) sigma-adjacent to every positive cycle: %d; -Lambda(M) >= total positive Lambda: %d; both (Star): %d' % (C['adj'], C['big'], C['star']))
out.append('with rem: -rem(M) = -Lambda(M) - (R3 lockless credit into M) >= total positive Lambda: %d; Star with rem: %d' % (C['bigrem'], C['starrem']))
out.append('distance from positive cycles not adjacent to M: %s' % {k: v for k, v in C.items() if k.startswith('dist')})
for b in bad[:20]: out.append('  %s' % (b,))
open(os.path.join(here, 'star-check.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
