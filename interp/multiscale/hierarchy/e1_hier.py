# E1: top-down chordless hierarchy on a test suite. Usage: python e1_hier.py L
import sys, time, json, random, collections
sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy')
from multiprocessing import Pool
from hier import *
from lev import load_map
def make(name):
    if name.startswith('ico'): return icosphere(int(name[3:]))
    if name.startswith('flip'):
        f, s = name[4:].split('_'); return flips(icosphere(int(f)), 3*len(icosphere(int(f))), random.Random(int(s)), 5, 9)
    if name.startswith('drum'):
        d, k = name[4:].split('_'); return drum(int(d), int(k))
    if name.startswith('glue'):
        return glue_faces([icosphere(int(x)) for x in name[4:].split('_')], random.Random(1))
    return load_map(name)
def job(a):
    name, L, seed = a; t = time.time()
    adj = make(name); g = G(adj); sc = sep_short_cycles(g)
    try: st = build(g, L=L, seed=seed, exh=16)
    except Exception as e: return dict(name=name, err=repr(e))
    prim = [b for b in st['bad'] if b['chordlessU']]
    return dict(name=name, n=g.n, L=L, seed=seed, degs=sorted(collections.Counter(g.deg).items()), **sc,
                nodes=st['nodes'], bad=len(st['bad']), primary_bad=len(prim),
                max_chords_bad=max([(b['chA'] or 0)+(b['chB'] or 0) for b in st['bad']], default=0),
                prim=prim[:8], unsplit=sorted(st['unsplit']), maxleaf=max(st['leaves']), depth=st['depth'],
                minbal=round(min(st['balance']), 3), meanbal=round(sum(st['balance'])/len(st['balance']), 3), sec=round(time.time()-t))
if __name__ == '__main__':
    L = int(sys.argv[1]); names = sys.argv[2].split(',')
    jobs = [(nm, L, s) for nm in names for s in range(int(sys.argv[3]) if len(sys.argv) > 3 else 1)]
    out = open('e1_hier_L%d.jsonl' % L, 'a')
    with Pool(4) as p:
        for r in p.imap_unordered(job, jobs):
            out.write(json.dumps(r)+'\n'); out.flush()
            print({k: r.get(k) for k in ('name', 'n', 'L', 'seed', 'sep3', 'ind4', 'nodes', 'bad', 'primary_bad', 'max_chords_bad', 'maxleaf', 'depth', 'minbal', 'sec', 'err')}, flush=True)
