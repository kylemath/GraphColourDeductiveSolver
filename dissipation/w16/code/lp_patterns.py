# W16: per-pattern LP (min t over the pattern's own rows + mrow closure) for families base / rrz / all, and joint LPs.
import sys, os, pickle, json, time, collections
sys.path.insert(0, '/tmp/swarm-W16/code')
import numpy as np
import w16lib as W

def pattern_lp(labs, fam):
    rows = W.build_lp(labs, fam)
    res, keys, rmap = W.solve_lp(rows)
    return res, rows, keys, rmap

def describe(cnt):
    degs = collections.Counter()
    for lab, m in cnt.items():
        d = 5 if lab[0] == 'S' else 6 if lab[0] == 'C' else lab[1]; degs[d] += m
    return dict(sorted(degs.items()))

def lab_str(lab):
    if lab[0] == 'S': return 'S %s H%s F%s' % (''.join(map(str, lab[1])), ''.join(map(str, lab[2])), ''.join('-' if x < 0 else str(x) for x in lab[3]))
    if lab[0] == 'C': return 'C %s/%s' % (''.join(map(str, lab[1])), ''.join(map(str, lab[2])))
    return 'R%d %s/%s' % (lab[1], ''.join(map(str, lab[2])), ''.join(map(str, lab[3])))

if __name__ == '__main__':
    ARGV = list(sys.argv); W.init()
    found = {}
    for f in ARGV[2:]: found.update(pickle.load(open(f, 'rb')))
    out = []
    for key, P in sorted(found.items(), key=lambda kv: (kv[1]['n'], str(describe(kv[1]['cnt'])))):
        cnt = P['cnt']; labs = list(cnt)
        bad = [l for l in labs if W.row_status(l) is not None]
        ent = dict(n=P['n'], degs=describe(cnt), tag=P['tag'], nrows=len(labs), inadmissible=len(bad), t={})
        for fam in ('base', 'rrz', 'all'):
            res, rows, keys, rmap = pattern_lp(labs, fam)
            ent['t'][fam] = (res.status, float(res.fun) if res.status == 0 else None)
        ent['rows'] = [(lab_str(l), m) for l, m in sorted(cnt.items(), key=str)]
        out.append(ent)
        print(ent['n'], ent['degs'], ent['nrows'], ent['t'], flush=True)
    json.dump(out, open(ARGV[1], 'w'), indent=1)
