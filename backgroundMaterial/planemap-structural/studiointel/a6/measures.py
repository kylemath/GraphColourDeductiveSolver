"""Decreasing-measure search along the rule's paths (a6_run 'feats': per step [lock (-1 = filled), dF, Fisk deg, t, N, nm]).
A measure 'strictly decreases' at a step if mu(next) < mu(current) (tuples compared lexicographically).  Reports, per
measure: the fraction of steps that decrease, and the fraction of walks on which it decreases at every step."""
import json, glob, sys, collections
walks = []
for f in sys.argv[1:]:
    for l in open(f):
        r = json.loads(l)
        if 'feats' in r: walks += [(r['family'], w) for w in r['feats'] if len(w) > 1]
M = {
    'dF': lambda s: s[1],
    'lock': lambda s: s[0],
    'Fisk deg': lambda s: s[2],
    '-Fisk deg': lambda s: -s[2],
    '|Fisk deg|': lambda s: abs(s[2]),
    'N chains': lambda s: s[4],
    'moves nm': lambda s: s[5],
    '(lock, dF)': lambda s: (s[0], s[1]),
    '(dF, lock)': lambda s: (s[1], s[0]),
    '(lock, |deg|)': lambda s: (s[0], abs(s[2])),
    '(lock, N)': lambda s: (s[0], s[4]),
    '(lock, nm)': lambda s: (s[0], s[5]),
    '(lock, -nm)': lambda s: (s[0], -s[5]),
    'dF + lock': lambda s: s[1] + s[0],
}
res = {}
for name, mu in M.items():
    st = dec = 0; wall = 0; by = collections.Counter(); byall = collections.Counter()
    for fam, w in walks:
        ok = True
        for a, b in zip(w, w[1:]):
            st += 1; d = mu(b) < mu(a); dec += d; ok &= d
        wall += ok; by[fam] += 1; byall[fam] += ok
    res[name] = (dec / st, wall / len(walks))
print('walks', len(walks), 'steps', sum(len(w) - 1 for f, w in walks), 'families', dict(collections.Counter(f for f, w in walks)))
for name, (a, b) in sorted(res.items(), key=lambda x: -x[1][1]):
    print('%-16s steps decreasing %.4f   walks decreasing at every step %.4f' % (name, a, b))
# where does dF fail to decrease?
nd = collections.Counter()
for fam, w in walks:
    for a, b in zip(w, w[1:]):
        if not b[1] < a[1]: nd[(a[0], a[1], b[0], b[1])] += 1
print('dF non-decreasing steps (lock,dF -> lock,dF):', nd.most_common(8))
