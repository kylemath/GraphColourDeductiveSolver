# For the heaviest mrowL / mrowQ rows of a dual export: which payee receiver rows carry the capped column (lQ / Q sig),
# by the payee's visible window, and how the mrow weight splits over the hidden letter(s).
import json, sys, collections, importlib.util, os
ENG = sys.argv[1]; DUAL = sys.argv[2]; RULES = sys.argv[3]; TABS = sys.argv[4].split(','); NTOP = int(sys.argv[5])
sp = importlib.util.spec_from_file_location('f2bmod', os.path.join(ENG, 'f2b.py')); f2b = importlib.util.module_from_spec(sp); sp.loader.exec_module(f2b)
f2b.load(RULES)
LET = [5, 6, 7, 8, 9]
L3T = {}
for fn in TABS:
    for k, v in json.load(open(fn)).items():
        sg, wd, ao = k.split(); L3T[(int(sg),) + tuple(int(ch) for ch in wd) + tuple(int(ch) for ch in ao)] = v[0]
def letters(m): return ''.join(str(l) for k, l in enumerate(LET) if (m >> k) & 1)
J = json.load(open(DUAL)); R = J['rows']
recv7 = [r for r in R if r['type'] == 'receiver' and r['d'] == 7]
recvall = [r for r in R if r['type'] == 'receiver']
def q7sig(U, a, b, c, e, m1=None, m2=None):
    x = (U, a, b, c, e)
    if m1 is None or (m1 == 31 and m2 == 31): return min(x, (U, e, c, b, a))
    return min(x + (m1, m2), (U, e, c, b, a, m2, m1))
# ---- lQ payee terms (d = 7): (c, ap, m & ~extra7) with window (sg, c, w2, w3, w4, ap, o)
LQP = collections.defaultdict(list)
for r in recv7:
    w = [int(ch) for ch in r['link']]; s = [int(ch) for ch in r['apex']]; n = 7
    for i in range(n):
        if w[i] != 7: continue
        for sg in (1, -1):
            c, w2, w3, w4 = (w[(i + k * sg) % n] for k in (1, 2, 3, 4))
            ap, o = (s[i], s[(i - 1) % n]) if sg == 1 else (s[(i - 1) % n], s[i])
            if c <= 6 and ap <= 6:
                m = L3T[(sg, c, w2, w3, w4, ap, o)] & ~f2b.extra7(7, w, s, i, sg)
                LQP[(c, ap, m)].append((r['w'], r['link'], r['apex'], i, sg, '%d|%d%d%d|%d%d' % (c, w2, w3, w4, ap, o), L3T[(sg, c, w2, w3, w4, ap, o)]))
# ---- lq payer terms (d = 7): (c, a, a2) = u's link letters going away from the link 7
LQY = collections.defaultdict(float)
for r in recv7:
    w = [int(ch) for ch in r['link']]
    for i in range(7):
        if w[i] != 7: continue
        for sg in (1, -1):
            c, a, a2 = w[(i + sg) % 7], w[(i + 2 * sg) % 7], w[(i + 3 * sg) % 7]
            if c <= 6 and a <= 6: LQY[(c, a, a2)] += r['w']
# ---- Q payee terms (any d): masked by L3T & ~extra7 for d = 7 (V = 8 table for d = 8 not reproduced here: those rows are listed unmasked)
QP = collections.defaultdict(list)
for r in recvall:
    d = r['d']; U = min(d, 9); w = [int(ch) for ch in r['link']]; s = [int(ch) for ch in r['apex']]
    for j in range(d):
        if w[j] != 7: continue
        ms = []
        for sgn in (1, -1):
            c = w[(j + sgn) % d]; ap_, o = (s[j], s[(j - 1) % d]) if sgn == 1 else (s[(j - 1) % d], s[j])
            if d == 7 and c <= 6 and ap_ <= 6: ms.append(L3T[(sgn, c, w[(j + 2 * sgn) % d], w[(j + 3 * sgn) % d], w[(j + 4 * sgn) % d], ap_, o)] & ~f2b.extra7(d, w, s, j, sgn))
            else: ms.append(31)
        sg = q7sig(U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d], ms[0], ms[1])
        QP[sg].append((r['w'], d, r['link'], r['apex'], j))
def show_L(top):
    print('=== mrowL: Q[(c, a, mask)] >= q[(c, a, X)], X = the payer 7\'s link letter at distance 3 from the payee (hidden) ===')
    by = collections.defaultdict(list)
    for r in R:
        if r['type'] == 'mrowL': by[tuple(r['sig'])].append((r['key'][2], r['w']))
    tot = sorted(by.items(), key=lambda kv: sum(w for _, w in kv[1]))
    for sig, ks in tot[:top]:
        c, a, m = sig; W = sum(w for _, w in ks)
        print('\nsig c=%d a=%d mask {%s}: total mrowL w %.6f; by hidden X: %s' % (c, a, letters(m), W, ', '.join('%d:%.6f' % (x, w) for x, w in sorted(ks))))
        print('  payer side (d = 7 rows paying q[(c,a,X)]), sum w by X: %s' % ', '.join('%d:%.6f' % (x, LQY.get((c, a, x), 0.0)) for x in LET))
        P = LQP.get(sig, [])
        win = collections.defaultdict(float); cnt = collections.Counter()
        for w_, lk, sv, i, sg, wd, m0 in P: win[(wd, m0)] += w_; cnt[(wd, m0)] += 1
        print('  payee rows charged Q[sig]: %d, sum w %.6f; by window c|w2w3w4|ap o (L3T mask before f2b):' % (len(P), sum(p[0] for p in P)))
        for (wd, m0), w_ in sorted(win.items(), key=lambda kv: kv[1])[:8]: print('    %s  L3T {%s}  rows %d  w %.6f' % (wd, letters(m0), cnt[(wd, m0)], w_))
def show_Q(top):
    print('\n=== mrowQ: Q[(U, a, b, c, e[, m1, m2])] >= q[(U, a, b, p1, p2, c, e)], p1/p2 = the 7\'s link letters at distance 3 from U (hidden) ===')
    by = collections.defaultdict(list)
    for r in R:
        if r['type'] == 'mrowQ': by[tuple(r['sig'])].append((tuple(r['key']), r['w']))
    tot = sorted(by.items(), key=lambda kv: sum(w for _, w in kv[1]))
    for sig, ks in tot[:top]:
        W = sum(w for _, w in ks)
        msk = ' masks p1 {%s} p2 {%s}' % (letters(sig[5]), letters(sig[6])) if len(sig) == 7 else ' (unmasked)'
        print('\nsig %s%s: total mrowQ w %.6f; keys: %s' % (''.join(map(str, sig[:5])), msk, W, ', '.join('%s:%.6f' % (''.join(map(str, k)), w) for k, w in sorted(ks, key=lambda kv: kv[1]))))
        P = QP.get(sig, [])
        print('  payee rows charged Q[sig]: %d, sum w %.6f; heaviest:' % (len(P), sum(p[0] for p in P)))
        for w_, d, lk, sv, j in sorted(P)[:5]: print('    d=%d link %s apex %s (7 at %d) w %.6f' % (d, lk, sv, j, w_))
show_L(NTOP); show_Q(NTOP)
