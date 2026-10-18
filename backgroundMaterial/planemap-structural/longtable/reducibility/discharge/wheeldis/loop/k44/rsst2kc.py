"""Round 44: RSST's unavoidable.conf as kc/dfast lines (rsst.txt, names rsst<idx>_<RSST name with '.' -> 'o'>) and
RSST's contraction sets in kc/cfast X notation (rsst_x.txt: name {X} or '-' for D).  Ring vertices 1..r -> R0..R(r-1)
(the conf's ring order), interior r+1..n -> I0..I(m-1).  usage: python3 rsst2kc.py"""
import os
H = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.normpath(os.path.join(H, '..', '..', '..', '..', '..', '..', 'studiointel', 'routeb', 'rsst', 'unavoidable.conf'))
blocks = [b for b in open(CONF).read().split('\n\n') if b.strip()]
out, xs = [], []
for k, b in enumerate(blocks):
    L = [l for l in b.split('\n') if l.strip()]
    nm = L[0].strip(); n, r = int(L[1].split()[0]), int(L[1].split()[1])
    c = [int(x) for x in L[2].split()]
    nb = {}
    for l in L[3:3 + n]:
        f = [int(x) for x in l.split()]; nb[f[0]] = f[2:]; assert f[0] <= r or len(f[2:]) == f[1]
    assert sorted(nb) == list(range(1, n + 1))
    I = list(range(r + 1, n + 1)); ii = {v: j for j, v in enumerate(I)}
    for v in I:                        # ring adjacency sanity: ring nbrs of interior are ring vertices 1..r
        assert all(1 <= w <= n for w in nb[v])
    rp = ';'.join(','.join(str(w - 1) for w in sorted(x for x in nb[v] if x <= r)) or '-' for v in I)
    ip = ';'.join(','.join(str(ii[w]) for w in sorted(x for x in nb[v] if x > r)) or '-' for v in I)
    name = 'rsst%03d_%s' % (k, nm.replace('.', 'o'))
    out.append('%s %d %d %s %s' % (name, r, n - r, rp, ip))
    lab = lambda v: ('R%d' % (v - 1)) if v <= r else ('I%d' % ii[v])
    if c[0] == 0: xs.append('%s -' % name)
    else:
        e = c[1:1 + 2 * c[0]]; pairs = [(e[2 * j], e[2 * j + 1]) for j in range(c[0])]
        def ed(a, b):
            a, b = sorted((a, b), key=lambda v: (v > r, v)); return '%s-%s' % (lab(a), lab(b))
        xs.append('%s {%s}' % (name, ','.join(ed(a, b) for a, b in pairs)))
open(os.path.join(H, 'rsst.txt'), 'w').write('\n'.join(out) + '\n')
open(os.path.join(H, 'rsst_x.txt'), 'w').write('\n'.join(xs) + '\n')
print(len(out), 'configs;', sum(1 for x in xs if x.endswith(' -')), 'D-labelled')
