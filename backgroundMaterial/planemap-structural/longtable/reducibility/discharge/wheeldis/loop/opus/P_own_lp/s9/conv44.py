"""P2 s9: convert explore k44/pats44.txt (NF lines 'd k slot mask ...', slot w_i = i, s_i = d+i, mask bit v-5)
to pcheck pat= .out lines 'f<d>_<link>_<s> D=true' (every mask in pats44 is a single letter 5..8, so exact).
Also cross-checks against k44/pats44_f.map (explore's own f-names) up to the dihedral action pcheck uses."""
import sys
src, mp, out = sys.argv[1:4]
L = {1: '5', 2: '6', 4: '7', 8: '8'}
def canon(d, P):
    best = None
    for r in range(d):
        for refl in (0, 1):
            q = []
            for (t, i), ch in P:
                j = ((i + r) % d) if not refl else (((r - i) % d) if t == 'w' else ((r - i - 1) % d))
                q.append(((t, j), ch))
            q = tuple(sorted(q)); best = q if best is None or q < best else best
    return (d, best)
def fromname(nm):
    f = nm.split('_'); d = int(f[0][1:]); P = []
    for t, wd in (('w', f[1]), ('s', f[2])):
        for i, ch in enumerate(wd):
            if ch != '.': P.append(((t, i), ch))
    return d, P
names = []; mine = set()
for l in open(src):
    if l.startswith('#') or not l.strip(): continue
    f = l.split('|')[0].split(); d, k = int(f[0]), int(f[1])
    w = ['.'] * d; s = ['.'] * d
    for j in range(k):
        sl, m = int(f[2 + 2 * j]), int(f[3 + 2 * j])
        (w if sl < d else s)[sl % d] = L[m]
    nm = 'f%d_%s_%s' % (d, ''.join(w), ''.join(s)); names.append((nm, l.split('|')[2].strip()))
    mine.add(canon(*fromname(nm)))
theirs = set(); B = 0
for l in open(mp):
    if l.startswith('#') or not l.strip(): continue
    nm = l.split('|')[0].strip()
    if 'B' in nm: B += 1; continue
    theirs.add(canon(*fromname(nm)))
print('pats44 patterns', len(names), 'distinct up to dihedral', len(mine), '; map names', len(theirs), '(+%d with B)' % B,
      '; mine - map', len(mine - theirs), '; map - mine', len(theirs - mine), file=sys.stderr)
with open(out, 'w') as o:
    o.write('# k44/pats44.txt (d3def56a) converted by s9/conv44.py: NF line -> exact f-name, D=true marks it loadable\n')
    for nm, cf in names: o.write('%s D=true src=pats44 %s\n' % (nm, cf.replace(' ', ',')))
