# s43 fy2 pricer (RELAY_SPEC_s43 43.5).  Prices the level-2 z columns against the l3q + rpatN3 A74 cert
# s39o/run_n3_A74/cert_q39n3A74L.json (class without z) by the lifting LP:
#   sender row (word, label): weight spread over the contexts of the word with the same NO-FY coefficient row;
#   receiver row (d, link, sv): weight spread over its fy2 cells (t class per face).
# Old columns keep their reduced costs (identical coefficients across a split); only z2 columns are tested.
#  (P1) min worst violation over all z2 keys;  (P2) rc >= 0 required only on z2 keys in a cell of the 5 face rows.
# Kill line: (P2) infeasible (a face-row z2 column has rc < 0 under every lifting).
import sys, re, json, collections, itertools
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
E = B + '/s43/eng'; Q = B + '/s33z/reg_A74'; H = B + '/s39o'
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
CERT = H + '/run_n3_A74/cert_q39n3A74L.json'
ARGS = ['xon', 'apexcls', 'filt16', 'killtab=' + Q + '/f/kill/kill6', 'hat5', 'consall', 'l3q',
        'l3qtab=' + Q + '/tab_1.json,' + Q + '/tab_-1.json', 'lqcap=3', 'rpatN=' + H + '/rpatN3.txt', 'fy', 'fy2',
        'xcap=3', 'root=' + M, 'args=' + Q + '/args_A74.txt', 'rpat=' + B + '/rpatD.txt',
        'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr43_price']
sys.argv = [E + '/pcheck.py', 'none'] + ARGS
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1)
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
assert G['FY'] and G['FY2'] and G['ZH'] and not G['ZR']
p2 = open(E + '/prelay2.py').read()
f = re.search(r'\ndef R2_sender_rows\(\):\n(.*?)\n(?=\S)', p2, re.S).group(0)
OLD = "                if k_ not in seen: seen.add(k_); out.append((''.join(map(str, w)), dict(cf), list(hb) + ['|'] + list(fb)))"
assert f.count(OLD) == 1
f = f.replace(OLD, "                out.append((''.join(map(str, w)), dict(cf), list(hb) + ['|'] + list(fb)))").replace('def R2_sender_rows', 'def R2_all_contexts')
exec(f, G)
def flags(on):
    G['FY'] = G['FY2'] = G['ZH'] = on
flags(False); OLDC = G['R2_all_contexts'](); flags(True); NEWC = G['R2_all_contexts']()
assert [(a, c) for a, _, c in OLDC] == [(a, c) for a, _, c in NEWC]
ctx = collections.defaultdict(list)   # word -> [(bits, oldrow, z2 part)]
for (wd, co, bt), (_, cn, _) in zip(OLDC, NEWC):
    zn = {k: v for k, v in cn.items() if k[0] == 'z'}
    assert {k: v for k, v in cn.items() if k[0] != 'z'} == co
    ctx[wd].append((tuple(map(str, bt)), tuple(sorted(co.items(), key=str)), zn))
C = json.load(open(CERT)); xon = True
FACE = {('7766556', '6567566'), ('7766556', '6566576'), ('7766556', '6576576'), ('7665566', '6675676'), ('7665566', '6775676')}
rows = []; tco = Fraction(0)
for c in C:
    w = Fraction(c['w']).limit_denominator(10 ** 7); r = c['row']
    if r[0] == 'senderR2':
        lab = tuple(map(str, r[2])); L = ctx[r[1]]
        mine = [x for x in L if x[0] == lab]; assert len(mine) == 1, r
        same = [x for x in L if x[1] == mine[0][1]]
        rows.append(('S', '%s %s' % (r[1], ''.join(lab)), w, [(''.join(x[0]), x[2]) for x in same], False)); tco += w
    elif r[0] == 'receiverR2':
        d, lk, sv = int(r[1]), r[2], r[3]
        flags(False); old = G['recv_coef_R2'](d, lk, sv, xon); flags(True)
        opts = []
        for cl, tau in G['fy2_cells'](d, [int(ch) for ch in lk], [int(ch) for ch in sv]):
            cf = G['recv_coef_R2'](d, lk, sv, xon, tau)
            assert {k: v for k, v in cf.items() if k[0] != 'z' and v} == {k: v for k, v in old.items() if v}, r
            opts.append((cl or '-', {k: v for k, v in cf.items() if k[0] == 'z' and v}))
        rows.append(('R', '%d %s %s' % (d, lk, sv), w, opts, (lk, sv) in FACE)); tco -= w
print('cert %s: %d rows, %d sender + %d receiver in the lifting; tco = %s' % (CERT.split('/')[-1], len(C), sum(r[0] == 'S' for r in rows), sum(r[0] == 'R' for r in rows), tco))
for k, lab, w, opts, fc in rows:
    print('  %s %-26s w=%-9s splits=%d%s' % (k, lab, w, len(opts), ' FACE' if fc else ''))
    if k == 'R' and fc:
        for cl, z in opts: print('        cell %-5s z2 keys %s' % (cl, sorted(z)))
keys = sorted({kk for r in rows for _, z in r[3] for kk in z})
kix = {kk: i for i, kk in enumerate(keys)}
FK = sorted({kk for r in rows if r[4] for _, z in r[3] for kk in z})
var = [(ri, ci) for ri, r in enumerate(rows) for ci in range(len(r[3]))]
A = np.zeros((len(keys), len(var)))
for vi, (ri, ci) in enumerate(var):
    for kk, v in rows[ri][3][ci][1].items(): A[kix[kk], vi] += v * (1 if rows[ri][0] == 'S' else -1)
Aeq = np.zeros((len(rows), len(var))); beq = np.array([float(abs(r[2])) for r in rows])
for vi, (ri, ci) in enumerate(var): Aeq[ri, vi] = 1
def worst(sub):
    """min over liftings of max_{K in sub} tot_K (tot_K = -rc_K * tco); returns (e, lam)"""
    ix = [kix[k] for k in sub]; nv = len(var)
    res = linprog(np.r_[np.zeros(nv), 1.0], A_ub=np.hstack([A[ix], -np.ones((len(ix), 1))]), b_ub=np.zeros(len(ix)),
                  A_eq=np.hstack([Aeq, np.zeros((len(rows), 1))]), b_eq=beq, bounds=[(0, None)] * nv + [(None, None)], method='highs')
    assert res.status == 0, res.message
    return res.x[-1], res.x[:-1]
T = float(tco)
e1, lam1 = worst(keys); e2, lam2 = worst(FK)
print('\nz2 keys touched: %d (on face rows: %d)' % (len(keys), len(FK)))
print('(P1) all keys:  best lifting worst rc = %+.9f = %+.4f/183  -> %s' % (-e1 / T, -e1 / T * 183, 'null (cert survives fy2)' if e1 <= 1e-12 else 'INVALID under every lifting'))
print('(P2) face keys: best lifting worst rc = %+.9f = %+.4f/183  -> KILL LINE %s' % (-e2 / T, -e2 / T * 183, 'PASSED: a face-row z2 column is negative under every lifting' if e2 > 1e-12 else 'NOT passed: some lifting keeps every face-row z2 column >= 0'))
def report(lam, title):
    tv = A @ lam
    print('\n%s: columns with rc < 0: %d, sum(-rc) = %.9f' % (title, int((tv > 1e-12).sum()), float(tv[tv > 1e-12].sum()) / T))
    for i in np.argsort(-tv):
        if tv[i] <= 1e-12: break
        who = ['%s%s[%s] lam=%.6f x%+d' % (rows[ri][0], ' FACE' if rows[ri][4] else '', rows[ri][1] + ' ' + rows[ri][3][ci][0], lam[vi], int(A[i, vi])) for vi, (ri, ci) in enumerate(var) if A[i, vi] and lam[vi] > 1e-12]
        print('  rc %+.6f (%+.3f/183) z2 %s %s | %s' % (-tv[i] / T, -tv[i] / T * 183, keys[i], 'FACE-KEY' if keys[i] in FK else '-', '; '.join(who)))
    print('  lifting (split rows):')
    for ri, r in enumerate(rows):
        ls = [(r[3][ci][0], lam[vi]) for vi, (rj, ci) in enumerate(var) if rj == ri and lam[vi] > 1e-12]
        if len(r[3]) > 1: print('    %s %s%s: %s' % (r[0], r[1], ' FACE' if r[4] else '', ', '.join('%s %.6f' % x for x in ls)))
    return tv
tv1 = report(lam1, '(P1) at its optimum')
tv2 = report(lam2, '(P2) at its optimum')
for cap in (0.05, 0.1):
    print('first-order gain at cap %.2f: (P1) %.6f, (P2) %.6f  [sum over rc<0 of -rc * cap]' % (cap, float(tv1[tv1 > 1e-12].sum()) / T * cap, float(tv2[tv2 > 1e-12].sum()) / T * cap))
