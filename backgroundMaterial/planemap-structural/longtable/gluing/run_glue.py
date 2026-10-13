"""Gluing-lock search driver (GLUING.md). For graph pairs (A, B) from census frame lists, glue at degree-5 vertices
u, u' with shifts, keep frame-class results (TrackB `frame`), run `picyc --full` at every hole, and write one JSON line
per glued graph: holes with min class F/N, frozen classes (a class with F = 0), positive windings, and R* (some hole
with every class filled).

    python3 run_glue.py A.txt B.txt OUT.jsonl [--u 1,2] [--u2 all] [--shifts 0,1,2,3,4] [--limit N]
"""
import sys, json, subprocess, argparse, os, tempfile, time
from glue import glue, line

HERE = os.path.dirname(os.path.abspath(__file__))


def read(path):
    out = []
    for l in open(path):
        p = l.split()
        if len(p) < 3: continue
        rot = [[int(x) for x in r.split(',')] for r in p[2].split(';')]
        out.append((p[0], rot))
    return out


def holes_sel_note(h): return False


def evaluate(name, rot, holes=None):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f:
        f.write(line(name, rot) + '\n'); fn = f.name
    fr = subprocess.run([os.path.join(HERE, 'frame')], input=open(fn).read(), capture_output=True, text=True)
    if not fr.stdout.strip():
        os.unlink(fn); return {'name': name, 'frame': False, 'why': fr.stderr.strip()[-200:]}
    P = subprocess.run([os.path.join(HERE, 'picyc'), fn, '--full'] + (['--holes', ','.join(map(str, holes))] if holes else []), capture_output=True, text=True)
    os.unlink(fn)
    holes = []
    for l in P.stdout.splitlines():
        r = json.loads(l)
        if r.get('kind') != 'hole': continue
        cls = r['clsig']
        holes.append({'h': r['hole'], 'ld': r['linkdeg'], 'S': r['states'], 'ncls': r['nclasses'],
                      'minFN': min(c[1] / c[0] for c in cls), 'frozen': sum(1 for c in cls if c[1] == 0),
                      'npos': r['npos'], 'maxw': r['maxw'], 'sumw': r['sumw'], 'bad': r['cls_bad'] or r['f5_bad'] or r['cyc_split'],
                      'clsig': cls if min(c[1] / c[0] for c in cls) <= 0.26 else None})
    rstar = any(h['frozen'] == 0 for h in holes) if not holes_sel_note(holes) else None
    return {'name': name, 'frame': True, 'n': len(rot), 'holes': holes, 'Rstar': rstar,
            'minFN': min(h['minFN'] for h in holes) if holes else None,
            'frozenHoles': sum(1 for h in holes if h['frozen']), 'tight': sum(1 for h in holes if abs(h['minFN'] - 0.25) < 1e-9)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('A'); ap.add_argument('B'); ap.add_argument('out')
    ap.add_argument('--u', default='all'); ap.add_argument('--u2', default='all'); ap.add_argument('--shifts', default='0,1,2,3,4')
    ap.add_argument('--limit', type=int, default=10 ** 9); ap.add_argument('--pairs', default='all')
    a = ap.parse_args()
    GA, GB = read(a.A), read(a.B)
    shifts = [int(x) for x in a.shifts.split(',')]
    done = 0; t0 = time.time()
    with open(a.out, 'a') as out:
        for ia, (na, ra) in enumerate(GA):
            for ib, (nb, rb) in enumerate(GB):
                if a.pairs == 'diag' and ia != ib: continue
                us = [u for u in range(len(ra)) if len(ra[u]) == 5] if a.u == 'all' else [int(x) for x in a.u.split(',')]
                u2s = [u for u in range(len(rb)) if len(rb[u]) == 5] if a.u2 == 'all' else [int(x) for x in a.u2.split(',')]
                for u in us:
                    for u2 in u2s:
                        for s in shifts:
                            if done >= a.limit: return
                            name = '%s@%d+%s@%d/s%d' % (na, u, nb, u2, s)
                            try:
                                rot, _, _ = glue(ra, u, rb, u2, s)
                            except AssertionError as e:
                                out.write(json.dumps({'name': name, 'error': str(e)}) + '\n'); continue
                            r = evaluate(name, rot); r['rot'] = ';'.join(','.join(map(str, x)) for x in rot)
                            out.write(json.dumps(r) + '\n'); out.flush(); done += 1
                            if r.get('frame'):
                                print('%5.0fs %s n=%d minFN %.4f tight %d frozenHoles %d R* %s' % (time.time() - t0, name, r['n'], r['minFN'], r['tight'], r['frozenHoles'], r['Rstar']), flush=True)
                            else:
                                print('%5.0fs %s not frame' % (time.time() - t0, name), flush=True)


if __name__ == '__main__':
    main()
