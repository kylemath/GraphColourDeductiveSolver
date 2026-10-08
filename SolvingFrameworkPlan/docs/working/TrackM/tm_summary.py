#!/usr/bin/env python3
"""Aggregate Track M runs: out/parts/*.jsonl -> out/summary.txt (+ out/summary.json)."""
import json, os, glob, sys, gzip
from collections import defaultdict, Counter
HERE = os.path.dirname(os.path.abspath(__file__))
KM = 10
PD = sys.argv[1] if len(sys.argv) > 1 else 'out/parts'; ON = sys.argv[2] if len(sys.argv) > 2 else 'out/summary.txt'
files = sorted(glob.glob(os.path.join(HERE, PD, '*.jsonl')) + glob.glob(os.path.join(HERE, PD, '*.jsonl.gz')))
ds_of = lambda f: os.path.basename(f).split('.', 1)[1].replace('.jsonl', '').replace('.gz', '')
H = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0] * (KM + 2))))
meta = defaultdict(Counter); fails = defaultdict(lambda: defaultdict(list)); maxd = defaultdict(Counter)
rules = None
for f in files:
    ds = ds_of(f)
    for l in (gzip.open(f, 'rt') if f.endswith('.gz') else open(f)):
        r = json.loads(l)
        if rules is None: rules = list(r['hist'])
        m = meta[ds]; m['holes'] += 1; m['graphs_' + r['graph']] = 1; m['U'] += r['nstarts']; m['DL'] += sum(r['hist']['OPT']['DL'])
        m['CYC'] += r['ncyc']; m['TLcls'] += r['tlclasses']; m['TLstates'] += sum(r['hist']['OPT']['TL'])
        for kk, v in r['kempe2'].items(): m['kempe2_' + kk] += v
        if 'pirun' in r:
            for i, nm in ((0, 'pirun'), (1, 'pinvrun')):
                v = r['pirun'][i]; maxd[ds][nm] = 99 if v < 0 or maxd[ds][nm] == 99 else max(maxd[ds][nm], v)
        maxd[ds]['interior'] = max([maxd[ds]['interior']] + r.get('interior', []))
        for kk, v in r.get('budget_ex', {}).items(): m['budget_' + kk] += v
        maxd[ds]['dF'] = max(maxd[ds]['dF'], r['maxdF']); maxd[ds]['dNDL'] = max(maxd[ds]['dNDL'], r['maxdNDL'])
        for rule, hh in r['hist'].items():
            for c, arr in hh.items():
                A = H[ds][rule][c]
                for i, x in enumerate(arr): A[i] += x
        for rule, fl in r.get('fails', {}).items():
            for x in fl:
                x = dict(x); x['graph'] = r['graph']; x['h'] = r['h']; x['word'] = r['word']; fails[ds][rule].append(x)

SPH = [d for d in H if not d.startswith('off_')]
OFF = [d for d in H if d.startswith('off_')]
order = ['census22-29', 'census28', 'census29', 'census30', 'census31', 'census32', 'cyc13', 'ipr', 'aw', 'bv', 'traps']
SPH = [d for d in order if d in H] + [d for d in SPH if d not in order]


def comb(dss, rule, c):
    A = [0] * (KM + 2)
    for d in dss:
        for i, x in enumerate(H[d][rule][c]): A[i] += x
    return A


def row(A, notl=None):
    tot = sum(A)
    if notl is not None: tot -= sum(notl)
    cum = 0; out = []
    for k in range(1, KM + 1):
        cum += A[k] - (notl[k] if notl else 0); out.append(cum)
    fail = A[KM + 1] - (notl[KM + 1] if notl else 0)
    worst = max([k for k in range(KM + 1) if A[k] - (notl[k] if notl else 0) > 0], default=0)
    return tot, out, fail, worst


L = []
P = L.append
P('Track M summary (data). Starts = unfilled states; DL = doubly-locked starts; CYC = starts on all-DL pi-cycles.')
P('Success within k = the rule reaches a filled state in <= k Kempe swaps. Off-sphere rows exclude starts in targetless classes.')
P('')
P('## Datasets')
for d in SPH + OFF:
    m = meta[d]; ng = sum(1 for k in m if k.startswith('graphs_'))
    P('%-12s graphs %5d holes %6d unfilled %9d DL %8d cyc-states %5d targetless classes %5d (states %d)  max dF %d  max dNDL %d  max interior-DL comp %d  max interior run along pi/pi^-1 %s  budget-exceeded %s  Kempe sequential double swap at DL: %s' % (
        d, ng, m['holes'], m['U'], m['DL'], m['CYC'], m['TLcls'], m['TLstates'], maxd[d]['dF'], maxd[d]['dNDL'], maxd[d]['interior'], '%s/%s' % (maxd[d].get('pirun', '-'), maxd[d].get('pinvrun', '-')), {k[7:]: v for k, v in m.items() if k.startswith('budget_')},
        {k[7:]: v for k, v in m.items() if k.startswith('kempe2_')}))
P('')
for title, dss, cat in (('ALL SPHERE, DL starts', SPH, 'DL'), ('ALL SPHERE, all-DL-cycle starts', SPH, 'CYC'),
                        ('ALL SPHERE, all unfilled starts', SPH, 'U')):
    P('## %s' % title)
    P('%-18s %9s  %s  %8s %5s' % ('rule', 'starts', ' '.join('k<=%-4d' % k for k in range(1, KM + 1)), 'fails', 'worst'))
    for rule in rules:
        tot, cum, fail, worst = row(comb(dss, rule, cat))
        if tot == 0: continue
        P('%-18s %9d  %s  %8d %5d' % (rule, tot, ' '.join('%.4f' % (x / tot) if x < tot else '1     ' for x in cum), fail, worst))
    P('')
P('## Per sphere dataset: DL fails (within 10) / worst-case swaps')
P('%-18s ' % 'rule' + ' '.join('%-16s' % d for d in SPH))
for rule in rules:
    s = []
    for d in SPH:
        tot, cum, fail, worst = row(H[d][rule]['DL'])
        s.append('%-16s' % ('%d/%d w%d' % (fail, tot, worst)))
    P('%-18s ' % rule + ' '.join(s))
P('')
if OFF:
    P('## Off sphere: fails in classes WITH filled states (U minus targetless) / starts; and TL starts (must fail)')
    P('%-18s ' % 'rule' + ' '.join('%-22s' % d for d in OFF))
    for rule in rules:
        s = []
        for d in OFF:
            U = H[d][rule]['U']; T = H[d][rule]['TL']
            tot, cum, fail, worst = row(U, T)
            s.append('%-22s' % ('%d/%d w%d TL%d' % (fail, tot, worst, sum(T))))
        P('%-18s ' % rule + ' '.join(s))
    P('')
P('## Failure anatomy (sphere, sampled failure records, <= 6 per rule per hole)')
for rule in rules:
    fl = [x for d in SPH for x in fails[d][rule]]
    if not fl: continue
    c = Counter()
    for x in fl:
        c['n'] += 1; c['cyc'] += x['cyc']; c['dF=%d' % x['dF']] += 1; c['dNDL=%d' % x['dNDL']] += 1
        if x['k2']:
            c['kempe2_fails_both'] += all(not y[0] for y in x['k2']); c['interference_both'] += all(y[1] for y in x['k2'])
        c['trapped(tabu exhausted)' if x['path_len'] < KM else 'wandered 10 steps'] += 1
        c['never_left_DL'] += all(p == 2 for p in x['path_phi'])
    P('%-18s %s' % (rule, dict(sorted(c.items()))))
kf = os.path.join(HERE, 'out/kempe1879.jsonl')
if os.path.exists(kf):
    A = defaultdict(Counter)
    for l in open(kf):
        r = json.loads(l); g = r['graph']; key = g if not g.startswith('p') else ('census' + g[1:3])
        A[key].update({k: v for k, v in r.items() if isinstance(v, int) and k != 'h'}); A[key]['holes'] += 1
    P('')
    P('## Kempe 1879 step at DL states (lit = simultaneous swap, Heawood trap iff lit fails; seq = sequential, either order)')
    for g, c in A.items(): P('%-34s %s' % (g, dict(sorted(c.items()))))
open(os.path.join(HERE, ON), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
