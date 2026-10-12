#!/usr/bin/env python3
"""Track G [exploratory]: aggregate tables for README (DL runs, cycle-class certificates, cycle anatomy).
usage: tg_summary.py > out/summary.txt"""
import json, gzip, os as _os
def _open(f):
    return open(f) if _os.path.exists(f) else gzip.open(f + '.gz', 'rt')
import json, glob, os
from collections import Counter
O = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')


def runs(prefixes):
    """lengths (in states) of maximal DL pi-runs that are paths (non-cycle), from the DL->DL step lists."""
    L = Counter(); nh = 0
    for p in prefixes:
        for l in _open(p + '.steps.jsonl'):
            d = json.loads(l); nh += 1
            nxt = {s['s']: s['t'] for s in d['steps'] if not s['cyc']}
            prev = set(nxt.values())
            for s in nxt:
                if s in prev: continue
                n = 1; x = s
                while x in nxt: x = nxt[x]; n += 1
                L[n] += 1
    return nh, L


def certs(files):
    R = [json.loads(l) for f in files for l in open(f)]
    c = Counter()
    for r in R:
        cl = 'clean' if r['nviol'] == 0 else 'viol'
        c[(cl, 'classes')] += 1
        c[(cl, 'F>0')] += r['F'] > 0
        c[(cl, 'max dS', max(k for k, v in r['dS']))] += 1
        c[(cl, 'max dF', max(k for k, v in r['dF']))] += 1
        c[(cl, 'drains = states on cycles')] += r['drains'] == sum(r['cyc'])
        c[(cl, 'escape targets only single-lock/no-lock (never filled)')] += set(r['esc_to']) <= {'S'}
        for k, v in r.get('viol_homology', {}).items(): c[(cl, 'violator crossing pair Z2 classes ' + k)] += v
        for k, v in r.get('cyc_homology', {}).items(): c[(cl, 'cycle-state lock classes ' + k)] += v
    return len(R), c


def cyc_anat(files):
    R = [json.loads(l) for f in files if os.path.exists(f) for l in open(f)]
    c = Counter(); ex = {}
    for r in R:
        cl = 'clean' if r['cls'][4] == 0 else 'viol'
        e = r['esc']
        c[(cl, 'cycles')] += 1
        c[(cl, 'sigma escapes at >=1 state')] += 's' in e
        c[(cl, 'sigma escapes at every 2nd state, nothing else (.s.s or s.s.)')] += e in ('.s' * (len(e) // 2), 's.' * (len(e) // 2))
        c[(cl, 'states with no escape (dS>=2)')] += e.count('.')
        c[(cl, 'states total')] += len(e)
        c[(cl, 'states with sigma escape')] += e.count('s')
        c[(cl, 'max dS on cycle', max(map(int, r['dS'])) if r.get('dS') else None)] += 1
        h = r.get('hseq', '')
        if h:
            nontriv = [i for i, x in enumerate(h) if x != '0']
            c[(cl, 'cycles with a non-separating lock cycle at some state')] += bool(nontriv)
            deep = [i for i, x in enumerate(r['dS']) if int(x) >= 3]
            c[(cl, 'states with dS>=3')] += len(deep)
            c[(cl, 'states with dS>=3 and non-sep lock cycle')] += sum(1 for i in deep if h[i] != '0')
            c[(cl, 'states with non-sep lock cycle')] += len(nontriv)
            c[(cl, 'states with non-sep lock cycle and dS>=3')] += sum(1 for i in nontriv if int(r['dS'][i]) >= 3)
        for t, v in r['types'].items(): c[(cl, 'escape type ' + t)] += v
        for t, v in r['targets'].items(): c[(cl, 'escape target ' + t)] += v
        c[(cl, 'noncyc DL sigma-escape rate (mean over cycles x1000)')] += round(1000 * r['noncyc_sigma_rate'])
    return len(R), c


if __name__ == '__main__':
    sph = sorted(set(glob.glob(O + '/census2?.steps.jsonl*')) | set(glob.glob(O + '/census30s4.steps.jsonl*')))
    nh, L = runs(sorted({p.split('.steps.jsonl')[0] for p in sph}))
    print('== DL pi-runs that are paths, sphere census holes (%d holes) ==' % nh)
    print('length (states): count', sorted(L.items()))
    nh, L = runs([O + '/off', O + '/off555'])
    print('== DL pi-runs that are paths, off-sphere cycle holes (%d holes) ==' % nh)
    print('length (states): count', sorted(L.items()))
    for title, fs in (('sphere (census cycle graphs 30-32 + C30#0, C40#0)', [O + '/cyc30.cert.jsonl', O + '/cyc31.cert.jsonl', O + '/cyc32.cert.jsonl', O + '/c30.cert.jsonl', O + '/c40.cert.jsonl'] + glob.glob(O + '/census2?.cert.jsonl') + glob.glob(O + '/census30s4.cert.jsonl')),
                      ('off-sphere (TrackF cyc_graphs + cyc555_graphs)', [O + '/off.cert.jsonl', O + '/off555.cert.jsonl'])):
        n, c = certs([f for f in fs if os.path.exists(f)])
        print('== cycle-class certificates: %s, %d classes ==' % (title, n))
        for k, v in sorted(c.items(), key=str): print('  ', k, v)
    for title, fs in (('sphere', [O + '/cycles_c30.jsonl', O + '/cycles_c40.jsonl'] + glob.glob(O + '/cycles_sph*.jsonl')),
                      ('off-sphere', [O + '/cycles_off.jsonl', O + '/cycles_off555.jsonl'])):
        n, c = cyc_anat(fs)
        print('== all-DL cycle anatomy: %s, %d cycles ==' % (title, n))
        for k, v in sorted(c.items(), key=str): print('  ', k, v)
