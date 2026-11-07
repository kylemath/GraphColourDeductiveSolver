# usage: python3 -I viol_classes.py <vfile> : group violated rows (d load excess link sv) by canonical link class (rotation+reflection)
import sys, collections
def canon(s):
    c = [s[i:] + s[:i] for i in range(len(s))]; r = s[::-1]; c += [r[i:] + r[:i] for i in range(len(r))]; return min(c)
G = collections.defaultdict(list)
for l in open(sys.argv[1]):
    f = l.split()
    if len(f) < 5 or l.startswith('#'): continue
    d, ex, lk, sv = int(f[0]), float(f[2]), f[3], f[4]; G[(d, canon(lk))].append((ex, lk, sv))
for (d, c), v in sorted(G.items(), key=lambda kv: -max(e for e, _, _ in kv[1])):
    e, lk, sv = max(v); print('| %d | %s | %d | %.4f | %s / %s |' % (d, c, len(v), e, lk, sv))
print('rows %d classes %d' % (sum(len(v) for v in G.values()), len(G)))
