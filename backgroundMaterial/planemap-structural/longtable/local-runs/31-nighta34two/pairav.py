"""[exploratory] NightA34Two: exchange-pair picture on Studio Job AV records (L = 20 degree-6 Gamma-cycles).
c_t = absolute colouring t steps after the period-0 R3k4 anchor (anchor = K8[0].pos - 8; past the stored 20 states,
c_{t+20} = tau c_t with tau = closing_colour_map).  rho: c_10 = rho c_0 on the 11 named vertices.
d_i = rho^{-1} c_{10+i} (period 1 pulled back to period-0 colours).  X_i = {v : c_i(v) != d_i(v)}.
Exchange: pi^10 c = rho d and pi^10 d = rho c (needs tau = rho^2)."""
import json
from collections import Counter
F = '../27-studio-positive-config/jobav/jobav-cycles.jsonl'
st = Counter(); rows = []
for l in open(F):
    r = json.loads(l)
    if r['L'] != 20: continue
    V = r['vertices']; ix = {v: i for i, v in enumerate(V)}; N = r['names']; hole = set(N.values())
    C = r['colourings']; a = (r['K8'][0]['pos'] - 8) % 20
    tau = {int(k): v for k, v in r['closing_colour_map'].items()}
    def CC(t): return C[t] if t < 20 else [tau[x] for x in CC(t - 20)]
    c = [dict(zip(V, CC(a + i))) for i in range(21)]
    rho = {c[0][v]: c[10][v] for v in hole}
    assert len(rho) == 4 and all(rho[c[0][v]] == c[10][v] for v in hole)
    st[('tau == rho^2', all(tau[x] == rho[rho[x]] for x in rho))] += 1
    st[('rho is a 3-cycle', sum(rho[x] != x for x in rho) == 3)] += 1
    ri = {b: x for x, b in rho.items()}
    d = [{v: ri[col] for v, col in c[10 + i].items()} for i in range(11)]
    X = [{v for v in V if c[i][v] != d[i][v]} for i in range(11)]
    st[('hole-sync i=0..10', all(not (X[i] & hole) for i in range(11)))] += 1
    st[('X10 == X0 (exchange)', X[10] == X[0])] += 1
    st[('X0 nonempty (L != 10)', bool(X[0]))] += 1
    S = {s['pos']: s for s in r['steps']}
    Kc = [set(S[(a + i) % 20]['K']) for i in range(10)]; Kd = [set(S[(a + 10 + i) % 20]['K']) for i in range(10)]
    br = r['breaks']['step8break']; nb = sum(br); key = 'break' if nb else 'nobreak'
    # sanity: J / break computed from my runs equals record
    for i in range(10):
        # X update rule: X_{i+1} subset X_i u (Kc ^ Kd)
        st[(key, 'X_{i+1} sub X_i u (Kc^Kd)', X[i + 1] <= X[i] | (Kc[i] ^ Kd[i]))] += 1
        st[(key, 'Kc^Kd sub X_i u N?', 'n/a')] += 0
    st[(key, 'K8c == K8d', Kc[8] == Kd[8])] += 1
    pk = {p['pos']: set(p['vertices']) for p in r['pockets']}
    P9 = [pk[(a + 9) % 20], pk[(a + 19) % 20]]
    # pair at pos 9 in c-frame: {c9(p), c9(m)}
    pair9 = {c[9][N['p']], c[9][N['m']]}
    if nb:
        b = br.index(True)
        Pb = P9[b]; Po = P9[1 - b]
        cb, co = (c[9], d[9]) if b == 0 else (d[9], c[9])   # breaking / other colourings, same frame
        XP = Pb & X[9]
        st[('break pocket meets X9', bool(XP))] += 1
        st[('X9-vertices of break pocket leave the pair in the other run', all(co[v] not in pair9 for v in XP))] += 1
        st[('some X9-vertex of break pocket leaves the pair in other run', any(co[v] not in pair9 for v in XP))] += 1
        K8b, K8o = (Kc[8], Kd[8]) if b == 0 else (Kd[8], Kc[8])
        st[('break pocket ^ X9 sub K8b ^ K8o', XP <= (K8b ^ K8o))] += 1
        st[('break pocket ^ X9 sub X8', XP <= X[8])] += 1
        rows.append((r['name'], r['orientation'], r['hole'], 'b=%d' % b, '|X0|=%d' % len(X[0]), '|X_i|=' + ','.join(str(len(x)) for x in X),
                     '|Pk_b|=%d' % len(Pb), '|Pk_b^X9|=%d' % len(XP), '|K8b^K8o|=%d' % len(K8b ^ K8o), 'XP sub X8:%s' % (XP <= X[8]),
                     'col b/o on XP:' + ' '.join('%d/%d' % (cb[v], co[v]) for v in sorted(XP)), 'pair9=%s' % sorted(pair9)))
    st[(key, '|X0|', len(X[0]))] += 1
for k in sorted(st, key=str): print(st[k], k)
print('breaking cycles:')
for x in rows: print(*x)
# --- addendum: colour roles on the crossing set XP = pocket_b ∩ X_9
st2 = Counter()
for l in open(F):
    r = json.loads(l)
    if r['L'] != 20 or not sum(r['breaks']['step8break']): continue
    V = r['vertices']; N = r['names']; C = r['colourings']; a = (r['K8'][0]['pos'] - 8) % 20
    tau = {int(k): v for k, v in r['closing_colour_map'].items()}
    def CC(t): return C[t] if t < 20 else [tau[x] for x in CC(t - 20)]
    c = [dict(zip(V, CC(a + i))) for i in range(21)]
    rho = {c[0][v]: c[10][v] for v in N.values()}; ri = {b: x for x, b in rho.items()}
    d9 = {v: ri[x] for v, x in c[19].items()}; c9 = c[9]
    b = r['breaks']['step8break'].index(True); cb, co = (c9, d9) if b == 0 else (d9, c9)
    pk = {p['pos']: set(p['vertices']) for p in r['pockets']}; Pb = pk[(a + 9 + 10 * b) % 20]
    XP = {v for v in Pb if cb[v] != co[v]}
    al = cb[N['p']]; A = cb[N['m']]; J = {cb[N['y']], cb[N['z']]}
    st2[('XP breaking colour == c(p)=alpha', all(cb[v] == al for v in XP))] += 1
    st2[('XP other colour in J pair {c(y),c(z)}', tuple(sorted(co[v] in J for v in XP)))] += 1
    st2[('alpha fixed by rho', rho[al] == al)] += 1
    S = {s['pos']: s for s in r['steps']}
    K8b = set(S[(a + 8 + 10 * b) % 20]['K']); K8o = set(S[(a + 18 - 10 * b) % 20]['K'])
    st2[('XP sub K8_break', XP <= K8b)] += 1; st2[('XP meets K8_other', bool(XP & K8o))] += 1
for k in sorted(st2, key=str): print('ADD', st2[k], k)
