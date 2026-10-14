"""B8 (exploratory, resumed run): write the census 2-ball keys with ring 15 (not W12/S66/J9-named, not yet tested)
to out/parts/c15_{0..3}.txt for dfast.  Usage: mk_c15.py"""
import os, sys, gzip, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ball, h0
ext = h0.load_ext(); j9 = h0.load_j9(); K = set()
for fn in glob.glob(os.path.join(HERE, 'out/scan-*.jsonl.gz')):
    for line in gzip.open(fn, 'rt'):
        for v, w, ks, st in json.loads(line)['h']:
            if ks is None or w in h0.W12 or ks in ext: continue
            key = ball.key_from_str(ks)
            if ball.ring_size(key) != 15 or ball.key_to_66666_name(key) in j9: continue
            K.add(ks)
fs = [open(os.path.join(HERE, 'out/parts/c15_%d.txt' % i), 'w') for i in range(4)]
for i, ks in enumerate(sorted(K)): fs[i % 4].write(ball.fmt_config('k' + ks, ball.build(ball.key_from_str(ks))) + '\n')
print('census ring-15 untested keys:', len(K))
