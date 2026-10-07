#!/usr/bin/env python3
"""Track A step 2 [exploratory]: PureClean census on frame-class graphs.
Per graph (picyc line): re-check frame membership (full G.summary), engine 1 (picyc --full) at every degree-5 vertex;
optional engine 2 (kempe_py, independent Python) with --verify: compares class multisets [(size, F)] hole by hole.
Output JSON lines: name, n, deg5, npc, nonpc, margin (max_v min-class F/size), worst (min_v), minfrac per hole, ncls, verify.
usage: census_eval.py IN.txt OUT.jsonl [--verify]   (Pool(4))"""
import sys, json
from multiprocessing import Pool
from tracka_lib import parse_line, G
from holes import picyc_holes, py_holes, score
VER = '--verify' in sys.argv
def work(line):
    name, rot = parse_line(line); s = G(rot).summary()
    H = picyc_holes(rot, name); sc = score(H)
    rec = dict(name=name, n=len(rot), frame=s['frame'], occ=s['occ'], maxdeg=s['maxdeg'], **sc)
    rec['minfrac'] = {str(h): v for h, v in sc['minfrac'].items()}; rec['ncls'] = {str(h): v for h, v in sc['ncls'].items()}
    rec['classes'] = {str(h): c for h, c in H.items()}
    if VER:
        Hp = py_holes(rot); rec['verify'] = all(sorted(H[h]) == Hp[h] for h in H) and set(H) == set(Hp)
    return rec
if __name__ == '__main__':
    lines = [l for l in open(sys.argv[1]) if l.strip()]
    with Pool(4) as P, open(sys.argv[2], 'w') as f:
        for r in P.imap_unordered(work, lines):
            f.write(json.dumps(r) + '\n'); f.flush()
