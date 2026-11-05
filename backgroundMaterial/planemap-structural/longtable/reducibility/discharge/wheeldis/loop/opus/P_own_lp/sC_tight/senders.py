# sender-row slacks at a sol (all R2 sender contexts); writes sorted list: slack word bits family-split
import sys, os, collections
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ana.py')).read())
S = Sol(OPT['sol']); out = OPT['out']
L = sorted(S.senders(), key=lambda r: r[0])
with open(out, 'w') as f:
    f.write('# sender rows at %s, t = %.12f: slack = value - (1 - t); %d rows\n' % (OPT['sol'], S.t, len(L)))
    for sl, wd, bits, g, cf in L: f.write('S %s %s %.9f %s\n' % (wd, bits, sl, ' '.join('%s=%+.5f' % kv for kv in sorted(g.items()))))
for th in (1e-6, 0.001, 0.003, 0.01):
    print('senders with slack < %g: %d' % (th, sum(1 for r in L if r[0] < th)))
print('min slack %.3g' % L[0][0])
