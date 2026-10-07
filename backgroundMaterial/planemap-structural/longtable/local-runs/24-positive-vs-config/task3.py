import sys, json, time, collections
sys.path.insert(0, '../common'); sys.path.insert(0, '../22-winding-escape'); sys.path.insert(0, '../23-positive-cycles')
from task2 import holes
from conf import configs
PC = '../../../studiointel/ipr/ipr_32_52.pc'
def read(path):
    b = open(path, 'rb').read(); i = len(b'>>planar_code<<'); gs = []
    while i < len(b):
        n = b[i]; i += 1; adj = []
        for v in range(n):
            l = []
            while b[i] != 0: l.append(b[i] - 1); i += 1
            i += 1; adj.append(l)
        gs.append(adj)
    return gs
GS = read(PC)
def job(a):
    n, i = a; rot = GS[i]
    assert not configs(rot)
    return a, holes(rot, (n, i))
if __name__ == '__main__':
    gs = GS; byn = collections.defaultdict(list)
    for i, g in enumerate(gs): byn[len(g)].append(i)
    print({n: len(v) for n, v in sorted(byn.items())}, flush=True)
    import multiprocessing as mp
    sel = []
    for n in sorted(byn):
        if n > int(sys.argv[1]): break
        sel += [(n, i) for i in byn[n][:int(sys.argv[2])]]
    res = []
    with mp.Pool(4) as p:
        for a, r in p.imap_unordered(job, sel):
            res += r
            print('DONE', a, len(r), 'holes, pos:', sum(x['npos'] for x in r), flush=True)
    json.dump(res, open('task3-%s.json' % sys.argv[1], 'w'))
