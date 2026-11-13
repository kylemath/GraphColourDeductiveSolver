import sys, random, time; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W, torus as TT
ns = W.init()
random.seed(7); t0 = time.time(); nb = 0; agree = 0; whyc = {}
# random arrangements, biased to small letters
for it in range(600):
    d = random.choice([7, 7, 7, 8, 8, 9])
    w = [random.choice([5, 5, 5, 6, 7, 7, 8]) for _ in range(d)]; s = [random.choice([5, 5, 6, 7, 7, 8, 9]) for _ in range(d)]
    a = ns['admissible'](d, w, s); b = W.admissible_fast(d, w, s) is None
    agree += (a == b); whyc[W.admissible_fast(d, w, s)] = whyc.get(W.admissible_fast(d, w, s), 0) + 1
    if a != b: nb += 1; print('MISMATCH', d, w, s, a, b)
print('admissible agree %d/600, mismatches %d, reasons %s, %.1fs' % (agree, nb, whyc, time.time() - t0))
# dihedral invariance of rows
bad = 0
for it in range(300):
    d = random.choice([7, 8, 9]); w = [random.choice([5, 6, 7, 8]) for _ in range(d)]; s = [random.choice([5, 6, 7, 8, 9]) for _ in range(d)]
    ref = dict(ns['recv_spec'](d, ''.join(map(str, w)), ''.join(map(str, s))))
    for a, b in TT.dihedral(w, s):
        if dict(ns['recv_spec'](d, ''.join(map(str, a)), ''.join(map(str, b)))) != ref: bad += 1; break
print('receiver dihedral non-invariant: %d / 300' % bad)
bad = 0; nn = 0
for it in range(300):
    w = [random.choice([5, 6, 7, 8]) for _ in range(5)]; H = [random.randint(0, 1) for _ in range(5)]; F = [random.randint(0, 1) if x == 6 else -1 for x in w]
    six = [k for k in range(5) if w[k] == 6]
    ref = ns['sender_row'](w, dict(enumerate(H)), {k: F[k] for k in six})
    if ref is None: nn += 1; continue
    for (a, b), (f, _) in zip(TT.dihedral(w, H), TT.dihedral(F, F)):
        sx = [k for k in range(5) if a[k] == 6]
        r = ns['sender_row'](list(a), dict(enumerate(b)), {k: f[k] for k in sx})
        if r is None or {k: v for k, v in r.items() if v} != {k: v for k, v in ref.items() if v}: bad += 1; print('S', w, H, F, a, b, f); break
print('sender dihedral non-invariant: %d / %d' % (bad, 300 - nn))
bad = 0
for it in range(200):
    L = [random.choice([5, 6, 7, 8]) for _ in range(6)]; s = [random.choice([5, 6, 7]) for _ in range(6)]
    ref = dict(ns['cons2_row'](L, s))
    for a, b in TT.dihedral(L, s):
        if dict(ns['cons2_row'](a, b)) != ref: bad += 1; break
print('cons2 dihedral non-invariant: %d / 200' % bad)
