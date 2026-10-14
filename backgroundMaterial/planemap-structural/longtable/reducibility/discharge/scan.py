"""B8 (exploratory): extract the 2-ball key at every degree-5 vertex of census graphs.
Usage: scan.py OUT.jsonl.gz FILE...   (lines 'name n rot0;rot1;... flags')
Writes one record per graph: {"g": name, "n": n, "h": [[v, wordcanon, keystr_or_null, status], ...]}"""
import sys, gzip, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import ball

out = gzip.open(sys.argv[1], 'wt')
for fn in sys.argv[2:]:
    op = gzip.open if fn.endswith('.gz') else open
    for line in op(fn, 'rt'):
        if not line.strip(): continue
        name, rot = ball.parse_line(line)
        H = []
        for v in range(len(rot)):
            if len(rot[v]) != 5: continue
            word, key, st = ball.ball_at(rot, v)
            H.append([v, ''.join(map(str, ball.wheel_canon(word))), ball.key_str(key) if key else None, st])
        out.write(json.dumps({'g': name, 'n': len(rot), 'h': H}) + '\n')
out.close()
