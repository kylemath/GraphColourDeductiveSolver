#!/usr/bin/env python3
"""Spec v2 (a7915274) §13 A.4 test vectors for d = 9..14 (u is a host, §13 A.1). Privates are given 3 per site in
site order (9 = 9+ or absent). Checks hi = lo, the contained configurations, and the 37-fit list of one vector."""
import sys, os, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rcore as R
R.U_HOST_ALWAYS = True
JOB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
txt = open(os.path.join(JOB, 'in_spec_v2_a7915274.md')).read()
sec = txt[txt.index('**Test vectors** (all of them re-evaluated'):txt.index('<!--/D9TABLES-->')]
out = open(os.path.join(JOB, 'logs', 'vectors_s13%s.log' % (('_' + R.CONTROL) if R.CONTROL else '')), 'w')
def log(s): print(s); out.write(s + '\n')
n = bad = 0
for line in sec.split('\n'):
    f = [z.strip() for z in line.strip().strip('|').split('|')]
    if len(f) != 7 or not f[0].isdigit(): continue
    d, what, link, apex, priv, hl, conf = int(f[0]), f[1], f[2], f[3], f[4], int(f[5]), f[6]
    L = [int(c) for c in link]; S = [int(c) for c in apex]
    pv = '9' * (3 * d) if priv == '9..9' else priv
    assert len(pv) == 3 * d, (line, len(pv))
    fill = {}
    for i in range(d):
        for j in range(1, R.npriv(L[i]) + 1): fill['p%d.%d' % (i, j)] = int(pv[3 * i + j - 1])
    W = R.Window(d, L, S); ins = R.instances(W)
    lo, hi, fired = R.ledger(d, ins, fill)
    mine = sorted('%s (%s)' % (R.CONFIGS[c]['name'], R.CONFIGS[c]['verdict']) for c in R.contained(R.requirements(W), fill))
    th = sorted(z.strip() for z in conf.split(',')) if conf != '-' else []
    first = None
    if lo != hl or hi != hl: first = 'lo/hi (mine %d/%d, theirs %d)' % (lo, hi, hl)
    elif mine != th: first = 'configs (mine %s, theirs %s)' % (mine, th)
    n += 1; bad += first is not None
    log('s13 d=%d %-45s %s %s %s%s' % (d, what[:45], link, apex, 'MATCH' if first is None else 'MISMATCH', '' if first is None else '  first diff: ' + first))
    if d == 9 and link == '555665566' and apex == '595565666':
        m = re.search(r'37 fits into u: (.*)\n', txt)
        theirs = collections.Counter(z.strip() for z in m.group(1).split(','))
        me = collections.Counter('%s@%s' % (I['tag'], I['hub']) for I, s in fired)
        ok = theirs == me
        n += 1; bad += not ok
        log('s13 fit list (37 fits) %s%s' % ('MATCH' if ok else 'MISMATCH', '' if ok else ' mine-only %s theirs-only %s' % (list((me - theirs).elements()), list((theirs - me).elements()))))
log('TOTAL s13: %d vectors, %d mismatches' % (n, bad))
