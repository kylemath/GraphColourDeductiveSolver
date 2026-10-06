#!/usr/bin/env python3
"""studiointel frozen_scan.py -- [exploratory] for every degree-5 hole: the distribution, over doubly locked states, of the number of
colour pairs {p,q} (of 6) whose bichromatic subgraph of T - v is connected. A DL state with all 6 connected is FROZEN (its Kempe class
is itself), i.e. a targetless class. Uses fast/kempe_frozen. usage: frozen_scan.py OUT.jsonl WORKERS inputs... (json graphs or gt:FILE)"""
import sys, os, json
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); os.environ['KEMPE_BIN'] = os.path.join(HERE, 'fast', 'kempe_frozen')
sys.path.insert(0, os.path.join(HERE, 'fast')); sys.path.insert(0, HERE)
import fast, graphs
from coset_potential import orient
def load(arg):
    if arg.startswith('gt:'):
        gi = -1
        for line in open(arg[3:]):
            t = line.split()
            if t and t[0] == 'G':
                gi += 1; nf = int(t[3]); x = list(map(int, t[4:4 + 3 * nf])); yield '%s#%d' % (arg[3:].split('/')[-1], gi), orient([tuple(x[3*i:3*i+3]) for i in range(nf)])
    else: yield arg, [tuple(f) for f in json.load(open(arg))['faces']]
def job(a):
    name, F, h = a; r = fast.analyse(F, h)
    return {'graph': name, 'hole': h, 'n_DL': r.get('n_DL'), 'rho': r.get('rho'), 'conn': r.get('conn_pairs_hist_DL'), 'maxconn': r.get('max_conn_pairs_DL')}
if __name__ == '__main__':
    out = open(sys.argv[1], 'w'); tasks = []
    for arg in sys.argv[3:]:
        for name, F in load(arg):
            dg = graphs.degrees(F); tasks += [(name, F, h) for h in sorted(dg) if dg[h] == 5]
    with Pool(int(sys.argv[2])) as p:
        for r in p.imap_unordered(job, tasks, chunksize=4): out.write(json.dumps(r) + '\n'); out.flush()
