"""s36g G3/G4 check (PRIVCELL_SPEC 3.1) on the 10 g7 names: the q pattern (vertex list + frame edges, 1.5) of each name,
built in the name's own g7 coordinates, against the kc line of Studio's held file (origin/main
loop/studio/sender_held/g7_53/held53_7_7665566_6765766.txt, frame labels -> kc interior indices).
G3: same vertex set and degrees.  G4: interior-interior kc edges == pattern edges (equality, not only forced <= kc).
usage: python3 framecheck.py HELDFILE"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'eng', 'privcell.py')).read().split("if __name__ == '__main__':")[0])
bad = 0
for line in open(sys.argv[1]):
    if line.startswith('#') or not line.strip(): continue
    kcl, fr = [x.strip() for x in line.split('|')[:2]]
    f = kcl.split(); nm, ring, m = f[0], int(f[1]), int(f[2]); inner = f[4].split(';')
    assert len(inner) == m
    E_kc = {tuple(sorted((i, int(j)))) for i, x in enumerate(inner) for j in x.split(',') if j}
    lab = [x.split('=') for x in fr.replace('frame', '').strip().split(',')]
    N = g7_to_q(nm); V, E = pc_pattern(N)
    def qlab(x):   # Studio frame label -> pattern vertex name in the same (g7) coordinates
        if x == 'v': return 'u'
        if x[0] in 'ws': return x
        if x[0] == 'p':
            ks = [k for k in V if k.startswith('p%s' % x[1])]
            n = G7_FRAME_W[int(x[1])] - 5; K = int(x[2])
            cand = ['p%sL%d' % (x[1], K), 'p%sR%d' % (x[1], n + 1 - K)]
            hit = [c for c in cand if c in V]; assert len(hit) == 1, (nm, x, ks); return hit[0]
        ts = [k for k in V if k.startswith('t(')]; assert len(ts) == 1, (nm, ts); return ts[0]
    idx = {qlab(a): i for i, (a, _) in enumerate(lab)}
    deg_ok = set(idx) == set(V) and all(V[k] == frozenset((int(d),)) for k, (a, d) in zip(idx, lab))
    E_q = {tuple(sorted((idx[a], idx[b]))) for a, b in E}
    ok = deg_ok and E_q == E_kc
    bad += not ok
    print('%s -> %s | m=%d pattern V=%d | G3 %s | G4 kc edges %d, pattern edges %d, equal %s%s' % (nm, pc_canon(N), m, len(V),
          'ok' if deg_ok else 'FAIL', len(E_kc), len(E_q), E_q == E_kc,
          '' if E_q == E_kc else ' kc-only %s pattern-only %s' % (sorted(E_kc - E_q), sorted(E_q - E_kc))))
print('# names %s; failures %d' % ('checked', bad))
