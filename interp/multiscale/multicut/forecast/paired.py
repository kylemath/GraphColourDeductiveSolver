import json, sys, collections
from an import load, cfg
R = []
for f in sys.argv[1:]: R += load(f)
by = collections.defaultdict(dict)
for r in R:
    m, s, o = cfg(r['spec']); by[(m, o)][s] = r
def st(r):
    if r['status'] == 'ok': return 'ok'
    if r['status'] == 'FAIL' and r.get('faillast'): return 'last'
    return 'oth'
for (m, o), D in sorted(by.items()):
    if o in ('base',) or 'log' in o: continue
    seeds = sorted(D)
    b = by.get((m, 'base'), {}); t = by.get((m, 'tz=1'), {}); dp = by.get((m, 'ord=dip'), {})
    def cnt(X):
        xs = [X[s] for s in seeds if s in X]
        return '%d/%d ok, %d last' % (sum(st(x) == 'ok' for x in xs), len(xs), sum(st(x) == 'last' for x in xs))
    print('%-6s %-26s | this %-16s | base %-16s | tz %-16s | dip %-16s' % (m, o, cnt(D), cnt(b), cnt(t), cnt(dp)))
