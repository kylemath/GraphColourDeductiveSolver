#!/usr/bin/env python3
"""studiointel ipr_run.py -- [exploratory] exact Kempe radius (fast engine) at every degree-5 hole of every graph in a planar_code file.
usage: ipr_run.py FILE.pc WORKERS CPU_SECONDS_TOTAL_HINT > out.jsonl   (graphs in file order; one JSON line per hole)"""
import sys, os, json, time
from multiprocessing import Pool
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fast'))
import fast
def read_pc(path):
    data = open(path, 'rb').read(); assert data[:15] == b'>>planar_code<<'; i = 15; out = []
    while i < len(data):
        n = data[i]; i += 1; rot = []
        for v in range(n):
            nb = []
            while data[i] != 0: nb.append(data[i] - 1); i += 1
            i += 1; rot.append(nb)
        fs = set()
        for u in range(n):
            r = rot[u]
            for k in range(len(r)):
                f = (u, r[(k + 1) % len(r)], r[k])          # reverse the clockwise rotation: counter-clockwise faces
                j = f.index(min(f)); fs.add(f[j:] + f[:j])
        out.append(sorted(fs))
    return out
def job(a):
    gi, F, h = a; t = time.time(); r = fast.analyse(F, h); r.pop('witness', None); r.pop('targetless', None)
    return {'graph': gi, 'n': len({x for f in F for x in f}), 'hole': h, **r, 'secs': round(time.time() - t, 2)}
if __name__ == '__main__':
    G = read_pc(sys.argv[1]); W = int(sys.argv[2])
    tasks = []
    for gi, F in enumerate(G):
        deg = {}
        for f in F:
            for x in f: deg[x] = deg.get(x, 0) + 1          # faces per vertex = degree
        tasks += [(gi, F, h) for h in sorted(deg) if deg[h] == 5]
    print(json.dumps({'graphs': len(G), 'holes': len(tasks)}), flush=True)
    with Pool(W) as p:
        for r in p.imap(job, tasks, chunksize=1): print(json.dumps(r), flush=True)
