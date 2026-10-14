"""Far-threshold scan (bnd --distscan): per hole the largest r such that R = {d >= r} solves every unfilled state
(rmax; solvability is monotone in R), with |R| and |R|/n there, and whether solvability is monotone in r.
Per graph family: distribution of dmax - rmax (how far from the far end a solving region must start), min |R|/n.
usage: farscan.py FILES..."""
import sys, json, re, collections
fam = collections.defaultdict(list); nonmono = 0; fails = collections.Counter(); skips = 0
for f in sys.argv[1:]:
    for l in open(f):
        r = json.loads(l)
        if 'skip' in r: skips += 1; continue
        g = re.sub(r'#.*', '', r['name']).rstrip('0123456789') or r['name']
        g = 'C%d' % (2 * r['n'] - 4) if r['name'].startswith('C') else g
        ge = sorted(((int(k[2:].split('_')[0]), int(k.split('_')[1]), v) for k, v in r.items() if k.startswith('ge')))
        ok = [rr for rr, sz, v in ge if v[1] == 0]
        rmax = max(ok) if ok else 1; sz = next((s for rr, s, v in ge if rr == rmax), r['n'] - 1)
        oks = [v[1] == 0 for rr, s, v in ge]
        if oks != sorted(oks, reverse=True): nonmono += 1
        fam[g].append((r['dmax'], rmax, sz / r['n'], r['n'], r['name'], r['hole'], r.get('dist3', [0, 0])[1], r.get('faceMax', [0, 0])[1], r.get('shell2', [0, 0])[1]))
print('skipped holes', skips, 'non-monotone holes', nonmono)
for g in sorted(fam, key=lambda x: (len(x), x)):
    L = fam[g]; gap = collections.Counter(d - r for d, r, *_ in L); dm = collections.Counter(d for d, *_ in L)
    mn = min(L, key=lambda x: x[2])
    print('%-8s holes %5d  n %d-%d  dmax %s  dmax-rmax %s  min|R|/n %.3f (%s h%d r=%d of dmax %d)  dist3-fail %d faceMax-fail %d shell2-fail %d' % (
        g, len(L), min(x[3] for x in L), max(x[3] for x in L), dict(sorted(dm.items())), dict(sorted(gap.items())), mn[2], mn[4], mn[5], mn[1], mn[0],
        sum(1 for x in L if x[6]), sum(1 for x in L if x[7]), sum(1 for x in L if x[8])))
