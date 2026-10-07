"""[exploratory] NightA34Two §6 on the Job AZ witness p26 #87942 h22 (both orientations).
(1) exchange pair and crossing lemma with the full graph; (2) static EPL test: all colourings of T - h with the hole
colours of the breaking run's R1k2 state; how many are DL with a pocket (a break state)."""
import json
from collections import Counter
D = json.load(open('../27-studio-positive-config/jobaz/jobaz-p26-87942-h22.json'))
def comp(adj, col, s, pair, avoid=()):
    if col.get(s) not in pair or s in avoid: return set()
    S = {s}; st = [s]
    while st:
        u = st.pop()
        for t in adj[u]:
            if t not in S and t not in avoid and col.get(t) in pair: S.add(t); st.append(t)
    return S
for O in D:
    rot = O['rotation']; g = O['geometry']; N = g['names']; link = g['link']
    h = next(v for v in range(len(rot)) if sorted(rot[v]) == sorted(link))
    adj = {v: [u for u in rot[v] if u != h] for v in range(len(rot)) if v != h}
    G = O['gamma_cycles'][0]; S = G['states']; L = G['L']
    cols = [{int(k): v for k, v in s['colouring'].items()} for s in S]
    hole = [N[k] for k in ('p', 'xp', 'x2', 'x3', 'xm', 'z', 'wp', 'w2', 'w3', 'y', 'm')]
    r4 = [s['pos'] for s in S if s['type'] == 'R3' and s['k'] == 4]
    # tau from cycle closure: pi(c_19) = tau c_0 ; recover rho from hole: c_{a+10} = rho c_a
    a0, a1 = r4
    rho = {cols[a0][v]: cols[a1][v] for v in hole}; tau = {x: rho[rho[x]] for x in rho}
    def C(t): return cols[t] if t < L else {v: tau[x] for v, x in C(t - L).items()}
    J0 = [s['J'] for s in S]
    # breaking run = the R3k4 anchor a whose a+9 has J false
    a = next(x for x in r4 if not S[(x + 9) % L]['J'])
    c = [C(a + i) for i in range(21)]; ri = {y: x for x, y in rho.items()}
    d = [{v: ri[x] for v, x in C(a + 10 + i).items()} for i in range(10)]
    X9 = {v for v in c[9] if c[9][v] != d[9][v]}
    print('==', O['orientation'], 'h', h, 'breaking anchor pos', a, 'rho', rho, '|X_i|', [len({v for v in c[i] if c[i][v] != d[i][v]}) for i in range(10)])
    print('   hole-sync', all(c[i][v] == d[i][v] for i in range(10) for v in hole))
    p, m, xp, wp, y, z, w2 = (N[k] for k in ('p', 'm', 'xp', 'wp', 'y', 'z', 'w2'))
    pm = {c[9][p], c[9][m]}; Jp = {c[9][y], c[9][z]}
    Pk = comp(adj, c[9], wp, pm, avoid=(p, xp)); print('   c9 pocket reaches m:', m in Pk, 'pocket', sorted(Pk))
    Pkd = comp(adj, d[9], wp, pm, avoid=(p, xp)); print('   d9 pocket reaches m:', m in Pkd)
    XP = Pk & X9
    print('   X9', sorted(X9), 'X9 cap pocket', sorted(XP), 'colours c/d', [(c[9][v], d[9][v]) for v in sorted(XP)], 'pair', sorted(pm), 'J', sorted(Jp))
    Zd = comp(adj, d[9], z, Jp); print('   d9: z ~ y', y in Zd, 'z ~ w2', w2 in Zd, 'Zd meets XP', sorted(Zd & XP))
    Zd2 = comp(adj, d[9], z, Jp, avoid=XP); print('   crossing lemma: removing XP cuts z from {y,w2} in d9:', not ({y, w2} & Zd2))
    # (2) static enumeration with hole colours of c9
    fixed = {v: c[9][v] for v in hole}
    free = [v for v in adj if v not in fixed]
    order = sorted(free, key=lambda v: -sum(1 for u in adj[v] if u in fixed))
    sols = []
    def rec(i, col):
        if i == len(order): sols.append(dict(col)); return
        v = order[i]
        for k in range(4):
            if all(col.get(u) != k for u in adj[v]): col[v] = k; rec(i + 1, col); del col[v]
    rec(0, dict(fixed))
    # locks at R1k2 (frame from link colours): lock1 {mu,A} x_{j+1}~x_{j+3}; lock2 {mu,B} x_{j+1}~x_{j+4}
    lc = [fixed[x] for x in link]; j = next(t for t in range(5) if lc[t] == lc[(t + 2) % 5])
    al, mu, A, B = lc[j], lc[(j + 1) % 5], lc[(j + 3) % 5], lc[(j + 4) % 5]
    st = Counter(); pocketed = []
    for u in sols:
        dl = link[(j + 3) % 5] in comp(adj, u, link[(j + 1) % 5], {mu, A}) and link[(j + 4) % 5] in comp(adj, u, link[(j + 1) % 5], {mu, B})
        pk = m in comp(adj, u, wp, pm, avoid=(p, xp))
        st[('DL', dl, 'pocket', pk)] += 1
        if dl and pk: pocketed.append(u)
    print('   static: colourings with these hole colours', len(sols), dict(st))
    # EPL static: pairs of pocketed DL colourings; does v's z-component (J pair) meet u's pocket in a vertex alpha in u?
    bad = 0; tot = 0
    for i, u in enumerate(pocketed):
        Qu = comp(adj, u, wp, pm, avoid=(p, xp))
        for v in pocketed:
            if v is u: continue
            tot += 1
            Zv = comp(adj, v, z, Jp)
            if not any(u[x] == al and v[x] != u[x] for x in Zv & Qu): bad += 1
    print('   EPL static on ordered pairs of pocketed DL colourings:', tot, 'pairs, EPL fails on', bad)
