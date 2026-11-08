# s86 v2r copy of ../binding86.py: also counts receiverV2 rows (KEYSPEC v2 realisation rows; a class sums |w| over its masked and v2 rows, every rho)
import json, sys, collections
J = json.load(open(sys.argv[1])); R = J['rows']
def canon(L, A):
    d = len(L); best = None
    for r in range(d):
        for (l, a) in ((L[r:] + L[:r], A[r:] + A[:r]),):
            best = min(best or (l, a), (l, a))
    Lr, Ar = L[::-1], A[::-1]
    for r in range(d):
        l = Lr[r:] + Lr[:r]; s = (r + 1) % d; a = Ar[s:] + Ar[:s]
        best = min(best, (l, a))
    return best
cls = collections.defaultdict(lambda: [0.0, 0, None])
for r in R:
    if r['type'] not in ('receiver', 'receiverV2'): continue
    k = (r['d'],) + canon(r['link'], r['apex']); c = cls[k]; c[0] += abs(r['w']); c[1] += 1
    if c[2] is None or abs(r['w']) > abs(c[2]['w']): c[2] = r
tot = sum(abs(r['w']) for r in R); trec = sum(v[0] for v in cls.values())
print('# BINDING (receiver rows of the k86GL phase-1 dual, by dihedral class of link/apex; |w| summed over the class)')
print('# dual %s; stamp: %s' % (sys.argv[1].split('/')[-1], J.get('stamp', '')[:160]))
print('# total |w| %.6f; receiver rows %d in %d classes, |w| %.6f (%.1f%%)' % (tot, sum(v[1] for v in cls.values()), len(cls), trec, 100 * trec / tot))
print('# rank  d  canonical link/apex      rows  sum|w|     cum%%   largest row (link/apex, w)   8+ in link/apex')
cum = 0.0
for i, (k, (w, n, r)) in enumerate(sorted(cls.items(), key=lambda kv: -kv[1][0])):
    cum += w
    print('%4d  %2d  %s/%s  %4d  %.6f  %5.1f   %s/%s %+.6f   %s/%s' % (i + 1, k[0], k[1], k[2], n, w, 100 * cum / trec, r['link'], r['apex'], r['w'], 'Y' if r['link_has_8plus'] else '-', 'Y' if r['apex_has_8plus'] else '-'))
    if i + 1 >= int(sys.argv[2]): break
