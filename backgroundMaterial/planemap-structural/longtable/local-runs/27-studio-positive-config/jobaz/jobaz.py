#!/usr/bin/env python3
"""Job AZ [exploratory]: complete dump of p26#87942 h22 (both orientations): every Gamma-cycle at the hole, absolute names/colours (Job AV replay, start at R3k4).
Per state: position, (type, k), j, link/ring colours, Lock1/Lock2, the six 2-colour pairs (rank E - V + C and component count; absolute colours 0-3, and the period's
position-4 names 1 = c(p), 2 = c(m), 3 = c(y), 4 = c(z)), sigma fixed?, sigma-exit kind (fixed / filled / lockless / Lock1-only / Lock2-only / DL) and f (filled states after
the exit along pi, uv_lib.f_after), J (y ~ z in G_{c(y),c(z)}), the pocket ({c(p),c(m)}-component of m in T - h - p - x+, reaches w+?), |K_{c(p),c(m)}(p)|.
Per step: swapped pair and component (vertex ids and names). Plus the rotation system, the hole geometry, and the far vertices within distance 3 of the ring."""
import sys, os, json
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobax', '../jobav', '../jobuv', '../jobay'): sys.path.insert(0, os.path.join(HERE, d))
from uv_lib import Hole
from jobax import FrameQ, ustar
from jobav import partition, comp
from jobay import rank
NAME, HOLE = 'p26#87942', 22
def ncomp(adj, col, a, b):
    seen = set(); c = 0
    for v in adj:
        if col[v] in (a, b) and v not in seen: c += 1; seen |= comp(adj, col, v, a, b)
    return c
def dump(mirror):
    H = Hole(NAME, HOLE, mirror); adj = {v: set(r) - {HOLE} for v, r in enumerate(H.rot) if v != HOLE}
    deg = [len(H.rot[x]) for x in H.L]; q = next(t for t in range(5) if deg[t] >= 6); F = FrameQ(adj, H.L, H.w, q); n = dict(F.names)
    n['m'] = [u for u in adj[n['p']] if u not in (n['xp'], n['xm'], n['z'], n['y'])][0]; n['ustar'] = ustar(adj, n); F.names = n
    inv = {}
    for k, v in n.items(): inv.setdefault(v, k)
    ring = [n[k] for k in ('z', 'wp', 'w2', 'w3', 'y', 'm')]; dist = {v: 0 for v in ring}; fr = list(ring)
    while fr:
        nx = []
        for u in fr:
            for v in adj[u]:
                if v not in dist and v not in H.L: dist[v] = dist[u] + 1; nx.append(v)
        fr = nx
    geom = dict(link=H.L, link_degrees=deg, degree6_vertex=n['p'], q=q, outer_w=H.w, names=n, ring=ring,
                far_within_3_of_ring={str(d): sorted(v for v, x in dist.items() if x == d) for d in (1, 2, 3)}, n_vertices=len(H.rot))
    out = []
    idx_of = {partition({v: H.col(x, v) for v in H.sp.order}): x for x in range(len(H.sp.states))}
    for z in H.cycles:
        if not all(H.DL[x] for x in z): continue
        cyc = [{v: H.col(x, v) for v in H.sp.order} for x in z]; P = [F.pos(c) for c in cyc]; s = P.index(0); z = z[s:] + z[:s]; cyc = cyc[s:] + cyc[:s]
        col = dict(cyc[0]); states = []; steps = []
        for t in range(len(z)):
            assert partition(col) == partition(cyc[t])
            j, ty, (al, mu, A, B) = F.lframe(col); k = (q - j) % 5
            li = H.L; m1 = li[(j + 1) % 5]
            l1 = li[(j + 3) % 5] in comp(adj, col, m1, mu, A); l2 = li[(j + 4) % 5] in comp(adj, col, m1, mu, B)
            Ks = comp(adj, col, m1, al, mu); fixed = all(v in Ks for v in adj if col[v] in (al, mu))
            sg = F.sigma(col); sidx = idx_of[partition(sg)]
            if fixed: kind = 'fixed'
            elif F.lframe(sg) is None: kind = 'filled'
            else:
                jj, _, (a2, m2, A2, B2) = F.lframe(sg); mm = li[(jj + 1) % 5]
                s1 = li[(jj + 3) % 5] in comp(adj, sg, mm, m2, A2); s2 = li[(jj + 4) % 5] in comp(adj, sg, mm, m2, B2)
                kind = {(False, False): 'lockless', (True, False): 'Lock1-only', (False, True): 'Lock2-only', (True, True): 'DL'}[(s1, s2)]
            pairs = {'%d%d' % (a, b): dict(rank=rank(adj, col, a, b), components=ncomp(adj, col, a, b)) for a, b in combinations(range(4), 2)}
            cy, cz = col[n['y']], col[n['z']]; a, b = col[n['p']], col[n['m']]
            sub = {v: (c if v not in (n['p'], n['xp']) else -1) for v, c in col.items()}; Pk = comp(adj, sub, n['m'], a, b)
            states.append(dict(pos=t, type='R%d' % ty, k=k, j=j, colouring={str(v): col[v] for v in sorted(col)}, link=[col[x] for x in H.L], ring=[col[v] for v in ring],
                               roles=dict(alpha=al, mu=mu, A=A, B=B), lock1=l1, lock2=l2, pairs=pairs, sigma_pair=sorted((al, mu)), sigma_fixed=fixed, sigma_exit=kind,
                               f=(H.f_after(sidx) if kind in ('lockless', 'Lock1-only') else None), J=(z_in := n['z'] in comp(adj, col, n['y'], cy, cz)),
                               pocket=dict(pair=sorted((a, b)), vertices=sorted(Pk), names=[inv.get(v, 'far') for v in sorted(Pk)], reaches_wp=n['wp'] in Pk),
                               Kpm_p=len(comp(adj, col, n['p'], a, b))))
            pair, K = F.step(col); steps.append(dict(pos=t, pair=sorted(pair), K=sorted(K), K_names=[inv.get(v, 'far') for v in sorted(K)]))
            u, w = pair; col = {v: (w if v in K and c == u else u if v in K and c == w else c) for v, c in col.items()}
        for b in range(len(z) // 10):
            st4 = states[10 * b + 4]['colouring']; cp, cyy, czz = st4[str(n['p'])], st4[str(n['y'])], st4[str(n['z'])]; cm = ({0, 1, 2, 3} - {cp, cyy, czz}).pop()
            nm = {cp: '1', cm: '2', cyy: '3', czz: '4'}
            for st in states[10 * b:10 * b + 10]: st['pos4_colour_names'] = {str(c): nm[c] for c in range(4)}
        out.append(dict(L=len(z), states=states, steps=steps))
    return dict(orientation='mirror' if mirror else 'plantri', rotation=H.rot, geometry=geom, gamma_cycles=out)
def table(D):
    L = []
    for d in D:
        g = d['geometry']; n = g['names']
        L.append('=' * 100); L.append('p26#87942 h22, %s orientation; %d vertices; link %s degrees %s; degree-6 vertex p = %d' % (d['orientation'], g['n_vertices'], g['link'], g['link_degrees'], g['degree6_vertex']))
        L.append('names: ' + ', '.join('%s=%d' % kv for kv in n.items()))
        L.append('far vertices at distance 1/2/3 from the ring: %s' % g['far_within_3_of_ring'])
        L.append('rotation system: ' + '; '.join('%d:%s' % (v, ','.join(map(str, r))) for v, r in enumerate(d['rotation'])))
        for c in d['gamma_cycles']:
            L.append('-- Gamma-cycle L = %d. Pairs: rank/components, absolute colours. Exit f = filled states after the exit.' % c['L'])
            L.append('%3s %-5s %-10s %-6s %-5s %-9s %-11s %-3s %-5s %-30s %-38s %s' % ('pos', 'type', 'link', 'ring', 'locks', 'sig pair', 'sigma exit', 'f', 'J', 'pocket (reaches w+)', 'ranks/comps 01 02 03 12 13 23', '|K(p)|'))
            for st, sp in zip(c['states'], c['steps']):
                pr = ' '.join('%d/%d' % (st['pairs'][k]['rank'], st['pairs'][k]['components']) for k in ('01', '02', '03', '12', '13', '23'))
                L.append('%3d %-5s %-10s %-6s %-5s %-9s %-11s %-3s %-5s %-30s %-38s %d' % (st['pos'], '%sk%d' % (st['type'], st['k']), ''.join(map(str, st['link'])), ''.join(map(str, st['ring'])),
                         '%d%d' % (st['lock1'], st['lock2']), ''.join(map(str, st['sigma_pair'])) + (' FIX' if st['sigma_fixed'] else ''), st['sigma_exit'], '-' if st['f'] is None else st['f'],
                         st['J'], '%s %s' % (','.join(st['pocket']['names']), st['pocket']['reaches_wp']), pr, st['Kpm_p']))
                L.append('      step %d: swap %s on %s' % (sp['pos'], ''.join(map(str, sp['pair'])), ' '.join('%d%s' % (v, '' if nm == 'far' else '(' + nm + ')') for v, nm in zip(sp['K'], sp['K_names']))))
    return '\n'.join(L) + '\n'
if __name__ == '__main__':
    D = [dump(False), dump(True)]
    json.dump(D, open(os.path.join(HERE, 'jobaz-p26-87942-h22.json'), 'w'), default=list)
    open(os.path.join(HERE, 'jobaz-table.txt'), 'w').write(table(D))
