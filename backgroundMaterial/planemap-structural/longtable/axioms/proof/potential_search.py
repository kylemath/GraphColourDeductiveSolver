"""Brute-force search for a Phi-monotone potential on genuine sphere near-rigid windows (census record holes).
Features at a Hamiltonian state t (frame-relative) and at the preceding in-shape state t-1; we test every
integer combination a*F_i + b*F_j (|a|,|b| <= 2) for strict monotonicity (one sign) across all Phi-steps
(Ham t -> Ham t+2) in all windows.  Also tests 'weak' monotonicity (non-strict)."""
import json, itertools, sys
rows = [json.loads(l) for l in open('out/sphere_windows.jsonl')]
steps = []
def feats(st, prev, nxt):
    n = st['n']
    f = dict(area_in=st['area_in'], X=st['X'], Y=st['Y'], DX=st['DX_corner'], DY=st['DY_corner'], O=st['O_corner'],
             p0=st['pos_e0'], p1=st['pos_e1'], p3=st['pos_e3'], gap10=st['pos_e0'] - st['pos_e1'],
             np0=n - st['pos_e0'], d3=min(st['pos_e3'], n - st['pos_e3']))
    if prev:
        f.update(Xp=prev['X'], DXp=prev['DX_corner'], DYp=prev['DY_corner'], Op=prev['O_corner'])
    if nxt:
        f.update(Xn=nxt['X'], DXn=nxt['DX_corner'], DYn=nxt['DY_corner'], On=nxt['O_corner'])
    return f
for d in rows:
    S = d['states']
    hs = [i for i, s in enumerate(S) if s['kH'] == 1]
    for a, b in zip(hs, hs[1:]):
        A = feats(S[a], S[a - 1] if a > 0 else None, S[a + 1] if a + 1 < len(S) else None)
        B = feats(S[b], S[b - 1] if b > 0 else None, S[b + 1] if b + 1 < len(S) else None)
        steps.append((A, B))
keys = sorted(set.intersection(*[set(A) & set(B) for A, B in steps]))
print('Phi-steps', len(steps), 'features', keys)
hits = []
for i, j in itertools.combinations_with_replacement(range(len(keys)), 2):
    for a in range(-2, 3):
        for b in range(-2, 3):
            if (a, b) == (0, 0) or (i == j and b != 0): continue
            ds = [a * (B[keys[i]] - A[keys[i]]) + b * (B[keys[j]] - A[keys[j]]) for A, B in steps]
            if all(x > 0 for x in ds) or all(x < 0 for x in ds): hits.append(('STRICT', a, keys[i], b, keys[j]))
            elif all(x >= 0 for x in ds) or all(x <= 0 for x in ds): hits.append(('weak', a, keys[i], b, keys[j]))
print(len(hits), 'hits'); [print(h) for h in hits[:40]]
