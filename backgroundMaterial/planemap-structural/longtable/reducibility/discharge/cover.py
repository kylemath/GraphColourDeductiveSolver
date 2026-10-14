"""B8 (exploratory): greedy minimum set of EXT 2-ball keys (beyond W12+S66+J9) hitting every census graph that
H1 misses.  Usage: cover.py out/scan-*.jsonl.gz   (needs out/fail-H1.txt and out/dres-*.txt)"""
import sys, os, gzip, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ball, h0
ext = h0.load_ext(); fail = set(open(os.path.join(HERE, 'out/fail-H1.txt')).read().split())
G = {}
for fn in sys.argv[1:]:
    for line in gzip.open(fn, 'rt'):
        g = json.loads(line)
        if g['g'] in fail: G[g['g']] = {ks for v, w, ks, st in g['h'] if ext.get(ks)}
left = set(G); chosen = []
while left:
    c = collections.Counter(k for g in left for k in G[g])
    k, n = c.most_common(1)[0]; chosen.append((k, n, ball.ring_size(ball.key_from_str(k))))
    left = {g for g in left if k not in G[g]}
print('graphs', len(G), 'greedy cover size', len(chosen))
for k, n, r in chosen: print('%-40s ring %2d  newly-hit %d' % (k, r, n))
