"""print feature sequences of selected runs.  show.py prefix kind minR feats..."""
import sys, json, gzip
from collections import defaultdict
pref, kind, minR = sys.argv[1], sys.argv[2], int(sys.argv[3]); feats = sys.argv[4].split(',')
runs = defaultdict(list)
for l in gzip.open(pref + '_feat.jsonl.gz', 'rt'):
    r = json.loads(l)
    if r['kind'] == kind and r['R'] >= minR: runs[r['run']].append(r)
meta = {r['id']: r for r in json.load(gzip.open(pref + '_runs.json.gz', 'rt'))}
mx = int(sys.argv[5]) if len(sys.argv) > 5 else 30
for i, (rid, s) in enumerate(sorted(runs.items())):
    if i >= mx: break
    s.sort(key=lambda r: r['t']); m = meta[rid]
    print(f"run {rid} {m['src']} n={m['n']} R={len(s)} start={m['start']} end={m['end']} w={m['word']}")
    for f in feats:
        print(f'   {f:9s}', ' '.join(f"{str(r.get(f, '.')):>4s}" for r in s))
