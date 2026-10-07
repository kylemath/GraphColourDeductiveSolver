import sys, json, time
sys.path.insert(0, '../common'); sys.path.insert(0, '../22-winding-escape'); sys.path.insert(0, '../23-positive-cycles')
from collections import Counter
from kempe_py import Space, gentri_rotation, adj_from_rot
from scan import analyse
from escape import GENTRI
from conf import cfree

def holes(rot, tag):
    out = []
    adj = adj_from_rot(rot)
    for h in range(len(rot)):
        if len(rot[h]) != 5: continue
        recs = []; hist = Counter(); t = time.time()
        sp = Space(adj, h, link=rot[h])
        analyse(tag[0], tag[1], h, sp, rot, recs, hist)
        out.append(dict(tag=tag, hole=h, states=len(sp.states), npos=len(recs), secs=round(time.time() - t, 1),
                        wind=sorted(Counter({w: 0 for w, _ in hist}) .keys()),
                        hist=[[w, L, c] for (w, L), c in sorted(hist.items())],
                        poswind=sorted({w for (w, L) in hist if w > 0})))
        print(tag, 'hole', h, 'states', len(sp.states), 'windings', sorted({w for (w, L) in hist}), 'POS' if recs else 'nopos', out[-1]['secs'], 's', flush=True)
    return out

if __name__ == '__main__':
    res = []
    for n in (22, 23, 24):
        lines = [l for l in open(GENTRI % n) if l.startswith('G')]
        for gi, l in enumerate(lines, 1):
            rot = gentri_rotation(l)
            if cfree(rot):
                print('cfree', n, gi, flush=True)
                res += holes(rot, (n, gi))
    json.dump(res, open('task2.json', 'w'))
