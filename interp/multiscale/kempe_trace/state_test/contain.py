"""Do population collars that contain the minimal obstructing pattern (same colours on its cells) always obstruct?
Also: row/depth profile of the connectivity-neutral deletions."""
import json, os, collections
D = '/mnt/project-files/multiscale/kempe_trace/state_test/'
M = json.load(open(D + 'minimal_vs_deletions.json'))
out = {}
for m in M:
    e = m['exp']
    if not os.path.exists(D + f'pop_{e}.json'): continue
    P = json.load(open(D + f'pop_{e}.json'))
    cells = [(r, c, col) for r, c, col in m['cells'] if r <= P['w']]
    deeper = [x for x in m['cells'] if x[0] > P['w']]
    cnt = collections.Counter()
    for rec in P['recs']:
        if all(int(rec['rows'][r][c]) == col for r, c, col in cells): cnt['contains:' + ('ob' if rec['obstructing'] else 'pass')] += 1
        else: cnt['not:' + ('ob' if rec['obstructing'] else 'pass')] += 1
    neutral = [d for d in m['deletions'] if not d['connectivity_rows_differ']]
    out[m['name']] = dict(population=dict(cnt), cells_deeper_than_w=len(deeper),
                          neutral_deletions=len(neutral), neutral_rows=dict(collections.Counter(d['v_row'] for d in neutral)),
                          all_deletion_rows=dict(collections.Counter(d['v_row'] for d in m['deletions'])), w=P['w'])
    print(m['name'], out[m['name']])
json.dump(out, open(D + 'containment.json', 'w'), indent=1)
