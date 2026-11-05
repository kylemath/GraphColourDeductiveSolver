import json, sys, itertools
LET = (5, 6, 7, 8, 9)
def letters(m): return [l for k, l in enumerate(LET) if (m >> k) & 1]
for fn in sys.argv[1:]:
    S = json.load(open(fn))
    LQQ = {tuple(k): v for k, v in S.get('lQ', [])}; LQV = {tuple(k): v for k, v in S.get('lq', [])}
    out = []
    for V in (7, 8):
        def Qe(c, a, m):
            kq = (c, a, m) if V == 7 else (V, c, a, m)
            vals = [LQQ.get(kq, 0.0)] + [LQV.get((c, a, a2) if V == 7 else (V, c, a, a2), 0.0) for a2 in letters(m)]
            return max(vals)
        worst = (0.0, None)
        for c, a in itertools.product((5, 6), repeat=2):
            Q = [Qe(c, a, m) for m in range(32)]
            for m in range(32):
                sub = m
                while True:
                    sub = (sub - 1) & m
                    if sub == m: break
                    dlt = Q[sub] - Q[m]
                    if dlt > worst[0]: worst = (dlt, (c, a, bin(m), bin(sub), Q[m], Q[sub]))
                    if sub == 0: break
        out.append('V%d max delta %.6g at %s' % (V, worst[0], worst[1]))
    print(fn.split('/')[-1], 't=%.6f' % S['t'], '|', ' ; '.join(out))
