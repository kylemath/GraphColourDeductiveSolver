#!/usr/bin/env python3
"""Track A task 2: pi-cycle content of every analysed small class (N <= 64) in anat/*.jsonl, using uv_lib.Hole (independent Python:
kempe_py.Space + escape.pi_of; pi, lambda, winding w = sum lambda / 5), plantri orientation and mirror.
Per class: list of (L, w) of the pi-cycles it contains, sum w, and the Theorem W check 4F - N = -5 sum w.
Also, for the 4-regular (8,2) classes: how the 16 edges split into pi-steps and other swaps."""
import sys, os, json, glob
from multiprocessing import Pool
from collections import Counter
sys.path.insert(0, '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/jobuv')
from uv_lib import Hole
from tracka_lib import parse_line, rot_from_faces
def rots():
    d = {}
    for fn in ('out/frame-27.txt', 'out/frame28-cfree-list.txt'):
        for l in open(fn): n, r = parse_line(l); d[n] = r
    for g in json.load(open('anat/wbest-graphs.json')): d[g['name']] = rot_from_faces([tuple(t) for t in g['faces']])
    return d
ROT = rots()
def work(a):
    name, h, mirror = a; H = Hole(name, int(h), mirror, rot=ROT[name]); sp = H.sp
    sp.build_graph(); cl, n = sp.classes(); out = []
    size = Counter(cl)
    for c in range(n):
        if size[c] > 64: continue
        mem = [k for k in range(H.S) if cl[k] == c]; F = sum(H.filled(k) for k in mem)
        cyc = sorted({H.cyc[k] for k in mem}); cy = [(len(H.cycles[z]), H.W[z]) for z in cyc]
        assert all(cl[x] == c for z in cyc for x in H.cycles[z])
        sw = sum(w for _, w in cy)
        # edges that are pi steps
        E = set(); P = set()
        for k in mem:
            for t in sp.G[k]: E.add(frozenset((k, t)))
            P.add(frozenset((k, H.pi[k])))
        out.append(dict(name=name, hole=h, mirror=mirror, N=len(mem), F=F, cycles=cy, sumw=sw, thmW=(4 * F - len(mem) == -5 * sw),
                        edges=len(E), pi_edges=len(P & E), pi_not_edge=len(P - E)))
    return out
if __name__ == '__main__':
    todo = set()
    for fn in glob.glob('anat/anat-*.jsonl'):
        for l in open(fn):
            r = json.loads(l)
            for h, cs in r['holes'].items():
                if any(not c.get('skipped') and c['N'] <= 64 for c in cs): todo.add((r['name'], h))
    jobs = [(n, h, m) for n, h in sorted(todo) for m in (False, True)]
    with Pool(4) as Pp, open('anat/anat-pi.jsonl', 'w') as f:
        for res in Pp.imap_unordered(work, jobs):
            for x in res: f.write(json.dumps(x) + '\n')
    R = [json.loads(l) for l in open('anat/anat-pi.jsonl')]
    C = Counter((r['N'], r['F'], r['mirror'], tuple(sorted(map(tuple, r['cycles']))), r['sumw'], r['thmW'], r['edges'], r['pi_edges'], r['pi_not_edge']) for r in R)
    print('class records (both orientations):', len(R), '; Theorem W failures:', sum(not r['thmW'] for r in R))
    for k, v in sorted(C.items()): print(' N=%d F=%d mirror=%s cycles(L,w)=%s sumw=%d thmW=%s edges=%d pi-edges=%d pi-self/non-edge=%d : %d' % (k + (v,)))
