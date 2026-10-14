"""Job 17 summary: per wheel D / C (with working X count and one X) / neither (best leftover)."""
import glob, re, collections, json
rows = {}; cur = None
for f in sorted(glob.glob('part*.out')):
    for l in open(f):
        if re.match(r'^c[56]_', l):
            p = l.split(); cur = p[0]
            rows[cur] = dict(ring=int(p[1][2:]), D=('D=true' in l), bad=int(re.search(r'bad=(\d+)', l).group(1)), Xs=[], works=0, best=None)
        elif 'C-REDUCIBLE with' in l and cur:
            rows[cur]['Xs'].append(l.split('X=')[1].strip())
        elif 'search |X|' in l and cur:
            m = re.search(r'working X (\d+), best X=\{([^}]*)\} leftover (\d+)', l)
            rows[cur]['works'] = int(m.group(1)); rows[cur]['best'] = (m.group(2), int(m.group(3)))
def verdict(r): return 'D' if r['D'] else ('C' if r['works'] > 0 else 'neither')
out = open('wheels17_verdicts.txt', 'w'); out.write('# wheel ring verdict workingX example_X_or_best(leftover)\n')
tally = collections.Counter(); H17 = []
for w, r in sorted(rows.items(), key=lambda x: (x[0][:2], x[1]['ring'], x[0])):
    v = verdict(r); tally[(w[:2], v)] += 1
    ex = r['Xs'][0] if r['Xs'] else ('best {%s} leftover %d' % r['best'] if r['best'] else '')
    out.write('%s %d %s %d %s\n' % (w, r['ring'], v, r['works'], ex))
    word = w.split('_')[1]
    if w.startswith('c5') and max(map(int, word)) <= 6 and v == 'neither': H17.append(w)
print('wheels', len(rows), dict(tally))
print('H17 (5-wheels with all link degrees <= 6 that are neither):', H17 or 'none: H17 survives')
for fam in ('c5', 'c6'):
    for v in ('C', 'neither'):
        print(fam, v, [w.split('_')[1] for w, r in sorted(rows.items(), key=lambda x: (x[1]['ring'], x[0])) if w.startswith(fam) and verdict(r) == v][:60])
