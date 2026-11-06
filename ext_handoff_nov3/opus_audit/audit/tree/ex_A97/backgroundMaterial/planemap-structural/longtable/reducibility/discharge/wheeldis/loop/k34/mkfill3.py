"""Round 41: fill3.txt = Opus's sub-patch windows of R* (opus_f_all.txt, from loop/opus/C_kc_ring17/f_all.txt at
e2b0ea90) at ring <= 15 + round 34's fillwin windows (fill.txt), stable-sorted by ring; fill3.txt.cov gives each
window's fillings (s1 s4).  Opus's names x7_<u|-><w letters>_<s letters> are in R's own orientation, s1 = s letter 1,
s4 = s letter 4; '.' covers 5-9, a letter covers itself."""
import os
H = os.path.dirname(os.path.abspath(__file__))
D = '56789'
op = [l.rstrip('\n') for l in open(os.path.join(H, 'opus_f_all.txt')) if int(l.split()[1]) <= 15]
fw = [l.rstrip('\n') for l in open(os.path.join(H, 'fill.txt'))]
cov = {l.split()[0]: l.rstrip('\n') for l in open(os.path.join(H, 'fill.txt.cov'))}
out, oc = [], []
for l in op:
    nm, r = l.split()[0], l.split()[1]
    sm = nm.split('_')[2]
    a = D if sm[1] == '.' else sm[1]
    b = D if sm[4] == '.' else sm[4]
    out.append((int(r), l)); oc.append('%s %s %s' % (nm, r, ' '.join(x + y for x in a for y in b)))
for l in fw:
    out.append((int(l.split()[1]), l)); oc.append(cov[l.split()[0]])
names = [l.split()[0] for _, l in out]
assert len(names) == len(set(names))
out.sort(key=lambda t: t[0])
open(os.path.join(H, 'fill3.txt'), 'w').write(''.join(l + '\n' for _, l in out))
open(os.path.join(H, 'fill3.txt.cov'), 'w').write(''.join(l + '\n' for l in oc))
print('opus', len(op), 'fillwin', len(fw), 'total', len(out))
