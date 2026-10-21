L3Q = 'l3q' in FLAGS                 # stage 28 (RELAY_SPEC_s21): l3q, a 7 u -> adjacent 7 v, q[(c, a, a2)] keyed on u's link out
LQV = {}; LQQ = {}                   # to distance 3; v credits Q[(c, a, mask)]. V = 7 subfamily: d = 7 rows only.
LQCAP = float(OPT.get('lqcap', '3')); L3T = {}; L3FILE = [None]
def l3q_load():
    if L3Q and not L3T:
        for fn in OPT['l3qtab'].split(','):
            for k, v in json.load(open(fn)).items():
                sg, wd, ao = k.split(); L3T[(int(sg),) + tuple(int(ch) for ch in wd) + tuple(int(ch) for ch in ao)] = v[0]
        assert len(L3T) == 2 * 2500, len(L3T)
def l3q_terms(d, w, s):
    """RELAY_SPEC_s21 21.3: payer -1 on lq (c, a, a2) and payee +1 on lQ (c, a', mask) at every link 7, both sides; d = 7 only"""
    cf = collections.Counter()
    if not L3Q or d != 7: return cf
    l3q_load(); n = 7
    for i in range(n):
        if w[i] != 7: continue
        for sg in (1, -1):
            c, a, a2 = w[(i + sg) % n], w[(i + 2 * sg) % n], w[(i + 3 * sg) % n]
            if c <= 6 and a <= 6: cf[('lq', (c, a, a2))] -= 1
            ap, o = (s[i], s[(i - 1) % n]) if sg == 1 else (s[(i - 1) % n], s[i])
            if c <= 6 and ap <= 6:
                m = L3T[(sg, c, a, a2, w[(i + 4 * sg) % n], ap, o)]
                cf[('lQ', (c, ap, m))] += 1
    return cf
def l3q_mask_letters(m): return [l for k, l in enumerate(LET) if (m >> k) & 1]
def l3q_Qeff(c, a, m):
    """value of Q[(c, a, m)] in the extended solution: max(LP value, max q over the mask) (mrowL rows hold for every mask)"""
    return max([LQQ.get((c, a, m), 0.0)] + [LQV.get((c, a, a2), 0.0) for a2 in l3q_mask_letters(m)])
def l3q_UB(c, a):
    if c > 6 or a > 6: return 0.0
    l3q_load(); return max(l3q_Qeff(c, a, m) for k, m in L3T.items() if k[1] == c and k[5] == a)
def write_l3q():
    l3q_load()
    QX = np.zeros(31250); PQ = np.zeros(125); MK = -np.ones(31250)
    for k, m in L3T.items():
        sg, c, w2, w3, w4, a, o = k
        i = (((((0 if sg == 1 else 1) * 5 + LI[c]) * 5 + LI[w2]) * 5 + LI[w3]) * 5 + LI[w4]) * 25 + LI[a] * 5 + LI[o]
        QX[i] = l3q_Qeff(c, a, m) - l3q_UB(c, a); MK[i] = m
    for (c, a, a2), v in LQV.items(): PQ[(LI[c] * 5 + LI[a]) * 5 + LI[a2]] = v
    assert QX.max() <= 1e-15 and PQ.min() >= -1e-15
    fn = os.path.join(WORK, 'l3q.bin')
    with open(fn, 'wb') as f: f.write(QX.astype(np.float64).tobytes()); f.write(PQ.astype(np.float64).tobytes()); f.write(MK.astype(np.float64).tobytes())
    L3FILE[0] = fn; return fn
def l3q_win(W, U):
    """window term at a link 7 (c = index 2): UB of the payee credit on both sides, sides read in the window:
    + side c = w_{i+1} = e, a = s_i = r ; - side c = w_{i-1} = b, a = s_{i-1} = q.  The leaf corrects it exactly (jsep5)."""
    if not L3Q or U != 7: return
    for b, e, q, r in itertools.product(range(5), repeat=4):
        W[:, b, 2, e, :, :, q, r, :] += l3q_UB(LET[e], LET[r]) + l3q_UB(LET[b], LET[q])
