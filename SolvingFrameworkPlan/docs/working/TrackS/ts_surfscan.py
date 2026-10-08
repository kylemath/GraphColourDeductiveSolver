#!/usr/bin/env python3
"""Track S: random min-degree-5 triangulations of a surface (TrackP surfaces.make, read-only), all degree-5 holes.
C engine (tj_eng --allholes) finds holes with all-DL pi-cycles; those are re-analysed in Python with Tait component counts
(dual on the surface) to flag Tait-Q-cycles (F13 connected at every state) and whether they pass through Tait-rigid states.
usage: ts_surfscan.py SURFACE COUNT NMIN NMAX SEED OUT.jsonl"""
import sys, os, json, random, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackP'))
import surfaces as S
from ts_lib import HoleData
from tl_lib import TaitState
from ts_qcyc import cycles

surf, count, nmin, nmax, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
rng = random.Random(seed); fo = open(out, 'w')
eng = subprocess.Popen([os.path.join(HERE, '..', 'TrackJ', 'tj_eng'), '--allholes', '--maxstates', '60000'],
                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
k = tries = 0; tot = dict(graphs=0, holes=0, cychole=0, cycles=0, taitQ=0, taitQ_rigid=0)
while k < count and tries < 50 * count:
    tries += 1; T = S.make(surf, rng.randint(nmin, nmax), rng)
    if T is None: continue
    rot = [S.link_cycle(T.F, v) for v in range(T.n)]
    holes = [h for h in range(T.n) if len(rot[h]) == 5]
    if not holes: continue
    k += 1; tot['graphs'] += 1; tot['holes'] += len(holes)
    name = f"{surf}{seed}_{k}"; line = f"{name} {T.n} " + ';'.join(','.join(map(str, r)) for r in rot)
    eng.stdin.write(line + '\n'); eng.stdin.flush()
    res = [json.loads(eng.stdout.readline()) for _ in holes]
    for d in res:
        if 'err' in d or d.get('ncyc', 0) == 0: continue
        tot['cychole'] += 1
        hd = HoleData(rot, d['hole'])
        for c in cycles(hd):
            ks = []
            for q in c:
                St = TaitState(hd, q); Tt = St.T
                ks.append('%d%d%d' % (Tt.ncomp(St.H), Tt.ncomp(St.F13), Tt.ncomp(St.F12)))
            tot['cycles'] += 1; isq = all(x[1] == '1' for x in ks); tot['taitQ'] += isq
            rig = isq and any(x == '111' for x in ks); tot['taitQ_rigid'] += rig
            fo.write(json.dumps(dict(g=name, h=d['hole'], L=len(c), taitQ=isq, rigid=rig, word=' '.join(ks),
                                     N=[hd.info[q]['N'] for q in c], graph=line if isq else None)) + '\n'); fo.flush()
    if k % 20 == 0: print(json.dumps(tot), flush=True)
print('DONE', json.dumps(tot), flush=True)
