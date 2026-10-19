# s33z engine test for zr (RELAY_SPEC_s22.1): (1) window term vs recv_coef_R2 z/zr terms on random rows, with random ZV / ZRV;
# (2) sender rows: every big position carries z +1 and zr -1 on the same key; (3) physical key test (s32p/ztest32.py logic).
# usage: python3 ztest33.py [broken]   (broken = window adds ZV + ZRV, control)
import os, sys, random
E = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eng')
BR = 'broken' in sys.argv[1:]
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
sys.argv = [os.path.join(E, 'pcheck.py'), 'none', 'root=' + M, 'xon', 'apexcls', 'hat5', 'zh', 'zr', 'hatrr', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr33t']
src = open(os.path.join(E, 'pcheck.py')).read().rstrip().rsplit('\n', 1)[0]; G = {'__file__': os.path.join(E, 'pcheck.py')}
exec(compile(src, 'pcheck.py', 'exec'), G)
rng = random.Random(33); LET = G['LET']; c2 = G['c2']; zkey = G['zkey']
keys = sorted({zkey((U, a, b, c, e), h1, h2) for U in (7, 8, 9) for a in LET for b in LET for c in LET for e in LET for h1 in (0, 1) for h2 in (0, 1)})
G['ZV'].update({k: rng.random() for k in keys}); G['ZRV'].update({k: rng.random() for k in keys})
bad = 0; n = 0
for _ in range(20000):
    d = rng.choice((7, 8, 9, 10)); U = min(d, 9)
    w = [rng.choice(LET) for _ in range(d)]; s = [rng.choice(LET) for _ in range(d)]
    cf = G['recv_coef_R2'](d, ''.join(map(str, w)), ''.join(map(str, s)), True)
    lhs = sum(c * (G['ZV'][k[1]] if k[0] == 'z' else G['ZRV'][k[1]]) for k, c in cf.items() if k[0] in ('z', 'zr'))
    rhs = 0.0
    for i in range(d):
        if w[i] != 5: continue
        a, b, e, f, q, r = w[(i - 2) % d], w[(i - 1) % d], w[(i + 1) % d], w[(i + 2) % d], s[(i - 1) % d], s[i]
        k = zkey((U, e, r, q, b), c2(f), c2(a))   # exactly the window expression of window_table_R2 (zh branch)
        rhs += G['ZV'][k] + (G['ZRV'][k] if BR else -G['ZRV'][k])
    n += 1
    if abs(lhs - rhs) > 1e-9: bad += 1
print('zr window vs recv_coef_R2: %d rows, %d mismatches%s' % (n, bad, ' (BROKEN CONTROL)' if BR else ''))
bad2 = 0; ns = 0
for wd, cf, bits in G['R2_sender_rows']():
    ns += 1
    z = {k[1]: c for k, c in cf.items() if k[0] == 'z'}; zr = {k[1]: c for k, c in cf.items() if k[0] == 'zr'}
    if set(z) != set(zr) or any(z[k] != -zr[k] for k in z) or sum(z.values()) != sum(1 for ch in wd if int(ch) >= 7): bad2 += 1
print('sender rows: %d, %d with z/zr coefficients not (+1, -1) per big position' % (ns, bad2))
