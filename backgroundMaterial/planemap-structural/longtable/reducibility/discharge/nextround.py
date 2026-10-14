"""B8 (exploratory): from witness graphs (WheelMain-free 'name n rot' lines), collect 2-ball keys at degree-5 holes
that are not yet tested; write ring <= RMAX configs into out/parts/TAG_{0..3}.txt, list larger rings.
Usage: nextround.py TAG RMAX WITFILE..."""
import sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ball, h0
tag, RMAX = sys.argv[1], int(sys.argv[2])
ext = h0.load_ext(); j9 = h0.load_j9()
new = collections.Counter(); big = collections.Counter(); known = collections.Counter()
for fn in sys.argv[3:]:
    for line in open(fn):
        name, rot = ball.parse_line(line)
        for v in range(len(rot)):
            if len(rot[v]) != 5: continue
            w, key, st = ball.ball_at(rot, v)
            if key is None: known['irregular:' + st] += 1; continue
            ks = ball.key_str(key); r = ball.ring_size(key)
            nm = ball.key_to_66666_name(key)
            if ks in ext or (nm and nm in j9): known['tested'] += 1; continue
            if r <= RMAX: new[ks] += 1
            else: big[(r, ks)] += 1
print('holes:', dict(known), 'new keys <= RMAX:', len(new), 'larger keys:', len(big))
print('larger by ring:', sorted(collections.Counter(r for r, k in big).items()))
fs = [open(os.path.join(HERE, 'out/parts/%s_%d.txt' % (tag, i)), 'w') for i in range(4)]
for i, ks in enumerate(sorted(new, key=lambda k: ball.ring_size(ball.key_from_str(k)))):
    fs[i % 4].write(ball.fmt_config('k' + ks, ball.build(ball.key_from_str(ks))) + '\n')
with open(os.path.join(HERE, 'out/studio-%s.txt' % tag), 'w') as f:
    for (r, ks), c in sorted(big.items()): f.write('%d %s %d\n' % (r, ks, c))
