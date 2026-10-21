# s47 jsep7 exactness test (as s28q/test_jsep5.py): random window table + random V = 7 and V = 8 lq / lQ values + random mask
# tables; every row jsep7 reports (mode 2, top K distinct) at d = 7 and d = 8 must have tot == python window sum + python l3q
# terms (recv_coef_R2's l3q_terms + l3q_terms_payeeV keys at Qeff / QeffV).  broken: no V = 8 file -> mismatches expected.
import sys, os, json, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from eng_exec import engine
ARGV0 = sys.argv[1:]; S = os.path.dirname(os.path.abspath(__file__)); rng = random.Random(47)
SC = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P'
for nm in ('fake7', 'fake8'):
    fake = {}
    for sg in (1, -1):
        for c, a in itertools.product((5, 6), repeat=2):
            for w2, w3, w4, o in itertools.product((5, 6, 7, 8, 9), repeat=4): fake['%+d %d%d%d%d %d%d' % (sg, c, w2, w3, w4, a, o)] = [rng.choice((31, 30, 30, 28, 29, 1, 0)), {}]
    json.dump(fake, open(os.path.join(SC, nm + '_tab.json'), 'w'))
G = {}; engine(['root=' + SC + '/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis', 'xon', 'l3q', 'l3qtab=' + SC + '/fake7_tab.json',
                'l3qV=7,8', 'l3qtab8=' + SC + '/fake8_tab.json', 'threads=1', 'work=' + SC + '/wr47t'], G)
exec('''
import numpy as np
brk = 'broken' in TESTFLAGS; tot_rows = 0; tot_bad = 0
for d in (7, 8):
    bad = 0; nrows = 0; nhit = 0; npay = 0; npe = 0
    for seed in range(int(TESTN)):
        r = np.random.RandomState(100 * d + seed)
        W = r.rand(*(5,) * 9) * 0.3
        W[:, :, 2, :, :, :, :, :, :] += 1.0; W[:, :, 3, :, :, :, :, :, :] += (3.0 if d == 7 else 1.0); W[:, :, 0:2, :, :, :, :, :, :] += (2.9 if d == 7 else 0.6)
        LQV.clear(); LQQ.clear()
        for c, a, a2 in itertools.product((5, 6), (5, 6), LET): LQV[(c, a, a2)] = r.rand() * 2; LQV[(8, c, a, a2)] = r.rand() * 2
        for c, a, m in itertools.product((5, 6), (5, 6), (31, 30, 1)): LQQ[(c, a, m)] = r.rand() * 3; LQQ[(8, c, a, m)] = r.rand() * 3
        W0 = W.copy(); l3q_win(W, min(d, 9)); l3q_winV(W, min(d, 9)); write_l3q()
        if brk: L3VFILE[0] = None
        CLSFILE[0] = os.path.join(WORK, 'clsT.bin'); class_table_R2(True).tofile(CLSFILE[0])
        rr, dt, ni = run_sep(d, W, -1e9, 300, 2, pats=False)
        for x in rr:
            if x[0] != 'V': continue
            nrows += 1; lk, sv = x[2], x[3]; w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]; tot = 0.0
            for i in range(d):
                idx = tuple(LI[w[(i + k) % d]] for k in (-2, -1, 0, 1, 2)) + tuple(LI[s[(i + k) % d]] for k in (-2, -1, 0, 1))
                tot += W0[idx]
            cf = l3q_terms(d, w, s); cf.update(l3q_terms_payeeV(d, w, s))
            nhit += any(len(k[1]) == 4 for k in cf); npay += any(k[0] == 'lq' and len(k[1]) == 4 for k in cf); npe += any(k[0] == 'lQ' and len(k[1]) == 4 for k in cf)
            for k, v in cf.items(): tot += v * (LQV.get(k[1], 0.0) if k[0] == 'lq' else l3q_QeffV(*k[1]) if len(k[1]) == 4 else l3q_Qeff(*k[1]))
            if abs(tot - float(x[1])) > 1e-9:
                bad += 1
                if bad <= 3: print("  MISMATCH d=%d" % d, lk, sv, x[1], tot, flush=True)
        print('d', d, 'seed', seed, 'rows', nrows, 'mismatches', bad, '%.1fs' % dt, flush=True)
    print('d=%d: %d rows, %d with V = 8 terms (payer %d, payee %d), %d mismatches' % (d, nrows, nhit, npay, npe, bad)); tot_rows += nrows; tot_bad += bad
print('JSEP7 TEST%s: %d rows, %d mismatches' % (' (BROKEN CONTROL: no V = 8 leaf file)' if brk else '', tot_rows, tot_bad))
''', dict(G, TESTFLAGS=ARGV0, TESTN=os.environ.get("TESTN", "4")))
