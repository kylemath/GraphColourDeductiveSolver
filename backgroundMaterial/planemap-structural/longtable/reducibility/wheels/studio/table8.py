"""Job 8 table: Lean wheelcheck results (run8/*.out) + dfast cross-check + RSST matches (DCheckData: same ring, m = 6,
same extendable count) + which Track B hole types are excluded (every 8/9 instance D-reducible)."""
import json, re, glob, collections
L = {}
for f in glob.glob('run8/part*.out'):
    for l in open(f):
        p = l.split()
        if 'D=' in l: L[p[0][1:]] = dict(r=int(p[1][2:]), classes=int(p[3].split('=')[1]), ext=int(p[4].split('=')[1]), reached=int(p[5].split('=')[1]), D=p[6] == 'D=true', depth=int(p[7].split('=')[1]))
        elif 'SKIP' in l: L[p[0][1:]] = dict(r=int(p[1][2:]), skip=True)
F = {}
for l in open('fast8.out'):
    p = l.split()
    if 'D=' in l: F[p[0][1:]] = (int(p[4].split('=')[1]), int(p[5].split('=')[1]), int(p[7].split('=')[1]))
rs = re.findall(r'name := "([^"]+)", r := (\d+), m := (\d+),.*?rsstExt := (\d+), rsstContract := (\d+)', open('../../dcheck/DCheckData.lean').read())
rsst = collections.defaultdict(list)
for nm, r, m, e, c in rs: rsst[(int(r), int(m), int(e))].append(nm)
inst = json.load(open('instances.json')); words = json.load(open('words.json'))
rows = []; agree = 0; cmp = 0
for w in sorted(L, key=lambda w: (L[w]['r'], w)):
    x = L[w]
    if x.get('skip'): rows.append('| %s | %d | – | – | – | not run (ring > 15) | | %s |' % (w, x['r'], ', '.join(inst[w]))); continue
    if w in F: cmp += 1; agree += F[w] == (x['ext'], x['reached'], x['depth'])
    m = rsst.get((x['r'], 6, x['ext']), [])
    rows.append('| %s | %d | %d | %d | %d | %s | %s | %s |' % (w, x['r'], x['classes'], x['ext'], x['reached'], 'yes' if x['D'] else 'no', ', '.join(m), ', '.join(inst[w])))
# Track B types
tb = {k: v for k, v in words.items() if any(s.startswith('TrackB') for s in v['sources'])}
excl, keep = [], []
for k, v in sorted(tb.items()):
    ins = [w for w, srcs in inst.items() if k in srcs]
    st = [L[w].get('D') for w in ins]
    (excl if all(st) else keep).append((k, ins, st, v['sources'], v['census33_holes']))
open('table8.md', 'w').write('| wheel (instance) | ring | ring colourings | extendable | fixable (reached) | D-reducible | RSST match (r, m=6, ext) | hole words |\n|---|---|---|---|---|---|---|---|\n' + '\n'.join(rows) + '\n')
print('Lean results', len(L), 'dfast agree', agree, '/', cmp)
print('D-reducible instances:', [w for w in L if L[w].get('D')])
print('Track B types:', len(tb), 'excluded by D-reducibility (all instances):', [(k, s) for k, i, st, s, c in excl])
print('remaining Track B types:', len(keep))
