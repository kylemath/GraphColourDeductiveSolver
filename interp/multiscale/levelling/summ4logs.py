# per-run summary from per-merge logs (includes runs still in progress / not finished)
import json, glob, collections
S = {}
for l in open('e4_summary.jsonl'):
    r = json.loads(l); S[(r['name'], r['mode'], r['variant'], r['seed'], bool(r.get('chordless')))] = r
print('| map (n) | mode | variant | merges logged | R histogram | max R | final R [sizes] | w histogram | max τ before re-level | re-level skips |')
print('|---|---|---|---|---|---|---|---|---|---|')
N = {'ico14': 1962, 'ico20': 4002, 'ico30': 9002, 'BASE_rand22': 4842, 'M3_ico22_hard': 4842}
rows = []
for f in sorted(glob.glob('e4_logs/*.jsonl')):
    R = [json.loads(l) for l in open(f)]
    if not R: continue
    cl = f.endswith('_cl.jsonl'); r0 = R[0]
    key = (r0['name'], r0['mode'], r0['variant'], r0['seed'], cl)
    s = S.get(key)
    fin = '%s %s' % (s['R_final'], s['final_sizes']) if s else ('(final merge running)' if key[0] != 'x' else '')
    skips = len(s['relevel_fails']) if s else '?'
    hw = dict(sorted(collections.Counter(r['w'] for r in R).items())) if r0['variant'].startswith('level') else '-'
    rows.append((r0['name'], r0['mode'], r0['variant'] + ('+chordless' if cl else ''), r0['seed'], len(R), dict(sorted(collections.Counter(r['R'] for r in R).items())), max(r['R'] for r in R), fin, hw, max(r['tau_before'] for r in R), skips, 'done' if s else 'partial'))
for r in sorted(rows, key=lambda x: (x[0], x[1], x[2], x[3])):
    print('| %s s%d (%d) | %s | %s | %d%s | %s | %s | %s | %s | %.2f | %s |' % (r[0], r[3], N[r[0]], r[1], r[2], r[4], '' if r[11] == 'done' else ' (partial)', r[5], r[6], r[7], r[8], r[9], r[10]))
