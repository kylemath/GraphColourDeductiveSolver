import json, glob, collections
tot = collections.Counter(); first = {}
rows = []
for f in sorted(glob.glob('out-*.jsonl'), key=lambda f: int(f[4:-6])):
    for l in open(f):
        r = json.loads(l)
        for c in r['cycles']:
            rows.append((r, c))
print('positive cycles', len(rows), 'classes with positive', len({(r['n'], r['gentri'], r['hole']) for r, c in rows}))
print(collections.Counter(c['n'] for r, c in rows))
for key in ['X', 'Xp', 'X2', 'X2b', 'X2any_neg', 'X3', 'X3b']:
    ok = sum(c[key] for r, c in rows); print(key, ok, '/', len(rows))
    bad = [(r, c) for r, c in rows if not c[key]]
    if bad:
        r, c = bad[0]; print('  first counterexample:', {k: v for k, v in c.items()})
print('cycles with a DL state having any LP swap:', sum(c['nDL_LP'] > 0 for r, c in rows), ' with X-type swap:', sum(c['nDL_X'] > 0 for r, c in rows))
print('mixed (F>0):', sum(c['F'] > 0 for r, c in rows), ' pure Gamma:', sum(c['F'] == 0 for r, c in rows))
print('classes: flow components', collections.Counter(r['flow_components'] for r in {(r['n'], r['gentri'], r['hole']): r for r, c in rows}.values()))
seen = {}
for r, c in rows: seen[(r['n'], r['gentri'], r['hole'])] = r
print('classes with positive: pos cycles having a negative LP-neighbour cycle:', sum(r['pos_with_neg_nb'] for r in seen.values()), '/', sum(r['npos'] for r in seen.values()),
      ' nonpositive nbr:', sum(r['pos_with_nonpos_nb'] for r in seen.values()))
print()
for r, c in rows:
    print(r['n'], 'g%d h%d' % (r['gentri'], r['hole']), 'L=%d F=%d w=%d nDL=%d nDL_LP=%d nDL_X=%d' % (c['L'], c['F'], c['w'], c['nDL'], c['nDL_LP'], c['nDL_X']),
          'Xw', c['Xw'], 'X2w', c['X2w'], 'X3w', c['X3w'], 'X2any', c['X2any'])
print()
for r in seen.values():
    print(r['n'], 'g%d h%d' % (r['gentri'], r['hole']), 'class', r['states'], 'U/F', r['U'], r['F'], 'cycles', r['ncyc'], 'flowcomp', r['flow_components'], 'npos', r['npos'], 'negnb', r['pos_with_neg_nb'], 'windings', r['windings'])
