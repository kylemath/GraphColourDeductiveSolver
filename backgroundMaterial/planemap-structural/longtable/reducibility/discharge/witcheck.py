"""B8 (exploratory): status of witness graphs under families.  Usage: witcheck.py FAMILIES WITFILE..."""
import sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ball, h0, construct
red = h0.make_pred(set(sys.argv[1].split(','))); ext = h0.load_ext(); j9 = h0.load_j9()
tot = 0; free = []
for fn in sys.argv[2:]:
    for line in open(fn):
        name, rot = ball.parse_line(line); tot += 1
        hit = None; unk = []; nonred = []
        for v in range(len(rot)):
            if len(rot[v]) != 5: continue
            w, key, st = ball.ball_at(rot, v); ks = ball.key_str(key)
            ws = ''.join(map(str, ball.wheel_canon(w)))
            if red(ws, ks): hit = (v, ws, ks); break
            nm = ball.key_to_66666_name(key)
            if ks in ext or (nm and nm in j9) or ws in h0.W12: nonred.append((v, ball.ring_size(key), ks))
            else: unk.append((v, ball.ring_size(key), ks))
        if not hit:
            free.append((len(rot), name, unk, nonred))
print('graphs', tot, 'with an R member', tot - len(free), 'R-free (so far)', len(free))
for n, name, unk, nonred in sorted(free)[:15]:
    print(n, name[:40], 'untested holes', len(unk), 'min ring of untested', min([r for _, r, _ in unk], default=None),
          'tested-not-reducible holes', len(nonred))
print('R-free graphs with no untested hole (true witnesses):', sum(1 for f in free if not f[2]))
