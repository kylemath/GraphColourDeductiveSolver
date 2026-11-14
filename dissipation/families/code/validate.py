import sys, random, importlib.util
sys.path.insert(0, sys.argv[1])
from behav import W2B, fit_part, canon_words, to3
from parts import parse
spec = importlib.util.spec_from_file_location('vc', sys.argv[2]); vc = importlib.util.module_from_spec(spec); spec.loader.exec_module(vc)
sc, P = parse(sys.argv[3])
pbn = {}
for p in P: pbn.setdefault(p['hub'], []).append((p['tag'], p['w'], to3(p['slots'])))
rng = random.Random(5); bad = 0; n = 0; nz = 0
for d in (5, 6, 7, 8, 9):
    for _ in range(60):
        w = [rng.choice([5, 5, 5, 6, 6, 7, 8, 9]) for _ in range(d)]
        A = W2B(d, w); B = vc.Window2Ball(d, w)
        hubs = [0] + [1 + i for i in range(d) if w[i] <= 8]
        for h in hubs:
            L = d if h == 0 else w[h - 1]
            if L > 8: continue
            for tag, wt, subs in pbn[L]:
                for a in range(L):
                    r1 = fit_part(A, h, subs, a); r2 = vc.fit_part(B, h, subs, a)
                    n += 1
                    if (r1 > 0) != (r2 is not None): bad += 1
                    elif r2 is not None:
                        nz += 1
                        p = 1.0
                        for _, lo, hi in r2[0]: p *= (hi - lo + 1) / 5
                        if abs(p - r1) > 1e-9: bad += 1
print('checked', n, 'fits', nz, 'mismatch', bad)
