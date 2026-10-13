"""Gluing round 2 (GLUING.md): from glued graphs with a floor-tight hole h, glue a second order-22 patch at each
degree-5 vertex u at graph distance 2..3 from h (all 5 shifts), and evaluate every hole.
    python3 round2.py run-tight.jsonl a22.txt round2.jsonl [--max-graphs N]"""
import sys, json, collections, argparse
from glue import glue
from run_glue import read, evaluate


def dist_from(rot, s):
    d = [-1] * len(rot); d[s] = 0; q = collections.deque([s])
    while q:
        x = q.popleft()
        for w in rot[x]:
            if d[w] < 0: d[w] = d[x] + 1; q.append(w)
    return d


ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('B'); ap.add_argument('out'); ap.add_argument('--max-graphs', type=int, default=10 ** 9)
a = ap.parse_args()
(nb, rb), = read(a.B)[:1]
srcs = [json.loads(l) for l in open(a.src)]
srcs = [r for r in srcs if r.get('frame') and r['tight']]
done = 0
with open(a.out, 'a') as out:
    for r in srcs[:a.max_graphs]:
        rot = [[int(x) for x in s.split(',')] for s in r['rot'].split(';')]
        tight = [h['h'] for h in r['holes'] if abs(h['minFN'] - 0.25) < 1e-9]
        us = set()
        for h in tight:
            d = dist_from(rot, h)
            us |= {u for u in range(len(rot)) if len(rot[u]) == 5 and 2 <= d[u] <= 3}
        for u in sorted(us):
            for s in range(5):
                name = '%s@%d+%s@1/s%d' % (r['name'], u, nb, s)
                try: g, m, _ = glue(rot, u, rb, 1, s)
                except AssertionError as e: out.write(json.dumps({'name': name, 'error': str(e)}) + '\n'); continue
                if len(g) > 65: continue
                sel = [m[h] for h in tight]
                e = evaluate(name, g, sel); e['holesOnly'] = sel; e['rot'] = ';'.join(','.join(map(str, x)) for x in g); e['parentTight'] = tight
                out.write(json.dumps(e) + '\n'); out.flush(); done += 1
                if e.get('frame'):
                    print('%s n=%d minFN %.4f tight %d frozen %d R* %s npos %d' % (name, e['n'], e['minFN'], e['tight'], e['frozenHoles'], e['Rstar'], sum(h['npos'] for h in e['holes'])), flush=True)
