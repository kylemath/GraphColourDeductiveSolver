#!/usr/bin/env python3
"""Job BV [exploratory]: the 12 statement-(c) ratio-search hits (jobbj/chits/). (1) independent verification + BI accounting (jobbi.account, Python engine, hole 22, both
orientations): (c) per Gamma-cycle, sigma-images with kinds/targets, the payer, IB-N0 (a lockless image on a heavy cycle Lambda(T) <= -Lambda(Z)). (2) BJ-style backfill on every
hole of each graph (picyc.bj --jobbj --jobh --full: sigma-C, H1, H2, sigma u sigma' groups, floor) and P1 variants at every Gamma hole (jobbj_p1.job). (3) B' slack (picyc.bq --jobbq)."""
import sys, os, json, subprocess, tempfile
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobbi', '../jobbj', '../jobas'): sys.path.insert(0, os.path.join(HERE, d))
import jobbi, jobbj_p1
from flipsearch import rotation
GD = os.path.join(HERE, '../jobbj/chits/')
def acc(a): return jobbi.account(a)
def p1(a): return jobbj_p1.job(a)
def picyc(binary, line, opts):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh: fh.write(line + '\n'); fn = fh.name
    try: o = subprocess.run([os.path.join(HERE, '..', binary), fn] + opts, capture_output=True, text=True).stdout
    finally: os.unlink(fn)
    return [json.loads(l) for l in o.splitlines() if '"kind": "hole"' in l]
def engine(a):
    g, m = a; F = json.load(open(GD + 'best-%s.json' % g))['faces']; rot = rotation([tuple(t) for t in F])
    line = '%s %d %s' % (g, len(rot), ';'.join(','.join(map(str, x)) for x in rot)); mo = ['--mirror'] if m else []
    return g, m, picyc('picyc.bj', line, ['--jobbj', '--jobh', '--full'] + mo), picyc('picyc.bq', line, ['--jobbq'] + mo)
if __name__ == '__main__':
    L = json.load(open(GD + 'list.json')); G = [(g, h) for g, h, *_ in L]
    with Pool(8) as P:
        A = P.map(acc, [('c', GD, g, h, m) for g, h in G for m in (False, True)])
        E = P.map(engine, [(g, m) for g, _ in G for m in (False, True)])
        gh = [(g, r['hole'], m) for g, m, bj, bq in E for r in bj if r.get('jobbj', {}).get('gamma', 0) > 0]
        P1 = P.map(p1, gh)
    out = dict(accounting=A, engine=[dict(graph=g, mirror=m, holes=[dict(hole=r['hole'], pattern=r['pattern'], sigC=r['sigC']['fail'], H1=r['H1_sigmap']['fail'], H2=r['H2_sigmap_plus_sigmaR3']['fail'],
                                                                           U=r['jobbj']['U_fail'], Umax=r['jobbj']['U_max_sumw_posgroups'], minFN=r['jobbj']['min_F_over_N'], gamma=r['jobbj']['gamma']) for r in bj],
                                                bq=[dict(hole=r['hole'], pattern=r['pattern'], **r['jobbq']) for r in bq]) for g, m, bj, bq in E], gamma_holes=gh, p1=P1)
    json.dump(out, open(os.path.join(HERE, 'jobbv.json'), 'w'), default=str)
    print('done: accounting records', sum(len(a) for a in A), 'engine runs', len(E), 'gamma holes', len(gh))
