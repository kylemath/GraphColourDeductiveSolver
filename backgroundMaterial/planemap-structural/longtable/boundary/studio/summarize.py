"""Aggregate bnd output (census by order, or any set) for the Job 7 report.  usage: summarize.py FILES..."""
import sys, json, re, collections
K = ['faceMax', 'face3', 'shell1', 'shell2', 'dist3']
by = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0, 0]))  # order -> kind -> [holes, failholes, maxExtra, maxFailStates]
tot = collections.Counter(); rim = [0] * 6; minratio = (9, None); skip = 0
for f in sys.argv[1:]:
    for l in open(f):
        r = json.loads(l)
        if 'skip' in r: skip += 1; continue
        m = re.match(r'p(\d+)', r['name']); o = int(m.group(1)) if m else r['name'].split('#')[0].split('_')[0]
        tot['holes'] += 1; tot['S'] += r['S']; tot['unreachF'] += r['unreachF'] > 0
        for k in K:
            if k not in r: continue
            a = r[k]; b = by[o][k]; b[0] += 1; b[1] += a[1] > 0; b[2] = max(b[2], a[4]); b[3] = max(b[3], a[2])
        if 'faceMaxRim' in r:
            rim = [x + y for x, y in zip(rim, r['faceMaxRim'])]
        if r.get('dist3') and r['dist3'][1] == 0:
            # |R|/n for dist3 needs |R|: recompute from the census graph only when asked (see dist3ratio.py)
            pass
print('holes', tot['holes'], 'skipped', skip, 'holes with an unfilled state unreachable even unrestricted', tot['unreachF'])
print('%-6s' % 'order' + ''.join('%28s' % k for k in K))
for o in sorted(by, key=str):
    print('%-6s' % o + ''.join('%28s' % ('%d/%d x%d f%d' % (by[o][k][1], by[o][k][0], by[o][k][2], by[o][k][3]) if by[o][k][0] else '-') for k in K))
allk = {k: [sum(by[o][k][i] for o in by) if i < 2 else max(by[o][k][i] for o in by) for i in range(4)] for k in K}
print('ALL   ' + ''.join('%28s' % ('%d/%d x%d f%d' % tuple(allk[k])) for k in K))
print('faceMaxRim totals', rim, 'lowering-move rim fraction %.4f, states with no rim-touching lowering move %.4f, all R-moves rim fraction %.4f' % (rim[2] / rim[1], rim[3] / rim[0], rim[5] / rim[4]))
