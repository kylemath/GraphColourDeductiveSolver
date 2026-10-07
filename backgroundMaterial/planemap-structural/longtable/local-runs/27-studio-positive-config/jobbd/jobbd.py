#!/usr/bin/env python3
"""Job BD [exploratory]: exchange-pair pockets (NightA34Two Sec. 1-3). c_t = absolute replay (Job AV), rho = colour map with c_10 = rho c_0 on the hole names, d_9 = rho^-1 c_19,
X9 = {v : c_9(v) != d_9(v)}. Pocket P_c = {c9(p), c9(X)}-component of X in T - h - p - x+ (X = m at degree 6; X = M' at degree 7), P_d the same in d_9. reaches_wp = the break.
Curve test: for a pocket reaching w+, C = p x+ w+ Q X p with Q a shortest w+ -> X path inside the pocket; sides = components of T - C (h included, on the x- side); the other pocket
'crosses' C if its vertices off C lie on both sides; the crossing vertices = other pocket ∩ C, and whether they lie in X9. Degree 6: all L = 20 jobav census records. Degree 7:
the 7 consecutive-break L = 20 cycles of Job BB (census, plantri), replayed here."""
import sys, os, json
from collections import Counter, deque
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobax', '../jobav', '../jobuv'): sys.path.insert(0, os.path.join(HERE, d))
from jobav import comp
def sp_path(adj, S, a, b):
    prev = {a: None}; dq = deque([a])
    while dq:
        u = dq.popleft()
        if u == b: break
        for v in adj[u]:
            if v in S and v not in prev: prev[v] = u; dq.append(v)
    if b not in prev: return None
    P = [b]
    while prev[P[-1]] is not None: P.append(prev[P[-1]])
    return P[::-1]
def sides(adjT, Cset):
    rest = [v for v in adjT if v not in Cset]; lab = {}; k = 0
    for v in rest:
        if v in lab: continue
        st = [v]; lab[v] = k
        while st:
            u = st.pop()
            for w in adjT[u]:
                if w not in Cset and w not in lab: lab[w] = k; st.append(w)
        k += 1
    return lab
def analyse(adj, hole, n, X, cols):
    """adj: T - h adjacency; cols: absolute colourings c_0..c_19 (dicts)."""
    adjT = {v: set(a) for v, a in adj.items()}; adjT[hole] = {n[k] for k in ('p', 'xp', 'x2', 'x3', 'xm')}
    for k in ('p', 'xp', 'x2', 'x3', 'xm'): adjT[n[k]].add(hole)
    c0, c10, c9, c19 = cols[0], cols[10], cols[9], cols[19]
    rho = {}
    for k in ('p', 'xp', 'x2', 'x3', 'xm', 'z', 'wp', 'w2', 'w3', 'y', 'm'): rho.setdefault(c0[n[k]], c10[n[k]])
    assert len(rho) == 4 and all(rho[c0[n[k]]] == c10[n[k]] for k in ('p', 'xp', 'x2', 'x3', 'xm', 'z', 'wp', 'w2', 'w3', 'y', 'm'))
    ri = {b: a for a, b in rho.items()}; d9 = {v: ri[c] for v, c in c19.items()}
    sync = all(c9[n[k]] == d9[n[k]] for k in ('p', 'xp', 'x2', 'x3', 'xm', 'z', 'wp', 'w2', 'w3', 'y'))
    X9 = {v for v in c9 if c9[v] != d9[v]}
    def pocket(col):
        a, b = col[n['p']], col[X]; sub = {v: (c if v not in (n['p'], n['xp']) else -1) for v, c in col.items()}; return comp(adj, sub, X, a, b)
    Pc, Pd = pocket(c9), pocket(d9); inv = {}
    for k, v in n.items(): inv.setdefault(v, k)
    res = dict(sync=sync, Pc=len(Pc), Pd=len(Pd), PcPd=len(Pc & Pd), X9=len(X9), X9_Pc=len(X9 & Pc), X9_Pd=len(X9 & Pd), brk_c=n['wp'] in Pc, brk_d=n['wp'] in Pd,
               named_c=sorted(inv[v] for v in Pc if v in inv), named_d=sorted(inv[v] for v in Pd if v in inv),
               relation='equal' if Pc == Pd else 'P_c inside P_d' if Pc < Pd else 'P_d inside P_c' if Pd < Pc else 'disjoint' if not Pc & Pd else 'overlap, not nested')
    for me, P, other, oname in (('c', Pc, Pd, 'd'), ('d', Pd, Pc, 'c')):
        if n['wp'] not in P: continue
        Q = sp_path(adj, P, n['wp'], X); C = [n['p'], n['xp']] + Q; Cs = set(C); lab = sides(adjT, Cs)
        zs = lab.get(n['z']); hs = lab.get(hole); ys = lab.get(n['y'])
        offs = {lab[v] for v in other if v not in Cs}; onC = other & Cs
        res['curve_' + me] = dict(len=len(C), z_side_differs_from_y=zs != ys, n_sides=len(set(lab.values())), other_sides=sorted(offs), other_on_curve=sorted(inv.get(v, 'far') for v in onC),
                                 other_on_curve_in_X9=len(onC & X9), other_on_curve_far=len([v for v in onC if v not in inv]),
                                 crosses=len(offs) >= 2, other_in_z_region=zs in offs, other_in_h_region=hs in offs)
    return res
if __name__ == '__main__':
    out = []
    for l in open(os.path.join(HERE, '../jobav/jobav-cycles.jsonl')):
        r = json.loads(l)
        if r['source'] != 'census' or r['L'] != 20: continue
        rot = r['rotation']; h = r['hole']; adj = {v: set(rot[v]) - {h} for v in range(len(rot)) if v != h}
        cols = [dict(zip(r['vertices'], c)) for c in r['colourings']]; n = {k: v for k, v in r['names'].items()}
        a = analyse(adj, h, n, n['m'], cols); a.update(degree=6, name=r['name'], hole=h, orientation=r['orientation']); out.append(a)
    # degree 7 controls
    from uv_lib import Hole
    from jobax import FrameQ
    deg7 = json.load(open(os.path.join(HERE, '../jobbb/jobbb-deg7-pockets.json')))
    want = sorted({(r['name'], r['hole'], r['orientation']) for r in deg7 if 'periods' in r and r['L'] == 20 and all(p['brk'] for p in r['periods'])})
    for name, h, ori in want:
        H = Hole(name, h, ori == 'mirror'); adj = {v: set(rr) - {h} for v, rr in enumerate(H.rot) if v != h}; deg = [len(H.rot[x]) for x in H.L]
        F = FrameQ(adj, H.L, H.w, deg.index(7)); n = dict(F.names)
        ins = [u for u in adj[n['p']] if u not in (n['xp'], n['xm'], n['y'], n['z'])]; Mp = [u for u in ins if n['z'] in adj[u]][0]; n['m'] = Mp
        for z in H.cycles:
            if len(z) != 20 or not all(H.DL[x] for x in z): continue
            cyc = [{v: H.col(x, v) for v in H.sp.order} for x in z]; P = [F.pos(c) for c in cyc]; s = P.index(0); cyc = cyc[s:] + cyc[:s]
            col = dict(cyc[0]); cols = []
            for t in range(20):
                cols.append(dict(col)); pair, K = F.step(col); u, w = pair; col = {v: (w if v in K and c == u else u if v in K and c == w else c) for v, c in col.items()}
            a = analyse(adj, h, n, Mp, cols)
            if a['brk_c'] and a['brk_d']: a.update(degree=7, name=name, hole=h, orientation=ori); out.append(a)
    json.dump(out, open(os.path.join(HERE, 'jobbd.json'), 'w'), indent=0)
    for deg in (6, 7):
        R = [r for r in out if r['degree'] == deg]; c = Counter()
        for r in R:
            nb = r['brk_c'] + r['brk_d']; g = '%d pockets reach w+' % nb
            c[(g, 'hole sync at 9: %s' % r['sync'])] += 1; c[(g, 'pocket relation: ' + r['relation'])] += 1
            for me in ('c', 'd'):
                cv = r.get('curve_' + me)
                if not cv: continue
                c[(g, 'curve separates z from y: %s' % cv['z_side_differs_from_y'])] += 1
                c[(g, 'other pocket crosses the curve: %s' % cv['crosses'])] += 1
                c[(g, 'other pocket meets the curve at %s' % (','.join(cv['other_on_curve']) or 'nothing'))] += 1
                c[(g, 'other pocket curve-vertices in X9: %d of %d' % (cv['other_on_curve_in_X9'], len(cv['other_on_curve'])))] += 1
                c[(g, 'other pocket enters the z-region: %s' % cv['other_in_z_region'])] += 1
        print('== degree %d: %d cycles' % (deg, len(R)))
        for k, v in sorted(c.items()): print('   ', v, k)
        hdr = ('name', 'ori', '|Pc|', '|Pd|', 'PcPd', '|X9|', 'X9Pc', 'X9Pd', 'brk c/d', 'relation')
        print('    %-12s %-7s %5s %5s %5s %5s %5s %5s %8s  %s' % hdr)
        for r in R:
            if deg == 7 or r['brk_c'] or r['brk_d']:
                print('    %-12s %-7s %5d %5d %5d %5d %5d %5d %8s  %s' % (r['name'] + ' h%d' % r['hole'], r['orientation'][:7], r['Pc'], r['Pd'], r['PcPd'], r['X9'], r['X9_Pc'], r['X9_Pd'], '%d/%d' % (r['brk_c'], r['brk_d']), r['relation']))
        st = Counter((r['Pc'], r['Pd'], r['X9']) for r in R if not (r['brk_c'] or r['brk_d']))
        print('    non-breaking (|Pc|,|Pd|,|X9|) most common:', st.most_common(8))
