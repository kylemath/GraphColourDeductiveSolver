# jsep5 exactness test: random window table + random l3q values + a random mask table; every row jsep5 reports
# (mode 2, top K distinct) must have tot == python window sum + python l3q terms (recv_coef_R2 keys, Qeff values).
import sys, os, json, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from eng_exec import engine
ARGV0 = sys.argv[1:]; S = os.path.dirname(os.path.abspath(__file__)); rng = random.Random(5)
fake = {}
for sg in (1, -1):
    for c, a in itertools.product((5, 6), repeat=2):
        for w2, w3, w4, o in itertools.product((5, 6, 7, 8, 9), repeat=4): fake['%+d %d%d%d%d %d%d' % (sg, c, w2, w3, w4, a, o)] = [rng.choice((31, 30, 30, 28, 29, 1, 0)), {}]
json.dump(fake, open(os.path.join(S, 'fake_tab.json'), 'w'))
G = {}; engine(['root=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis', 'xon', 'l3q', 'l3qtab=' + os.path.join(S, 'fake_tab.json'), 'threads=2', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr28t'], G)
exec('''
import numpy as np
bad = 0; nrows = 0; nhit = 0; brk = 'broken' in TESTFLAGS
for seed in range(int(TESTN)):
    r = np.random.RandomState(seed)
    W = r.rand(*(5,) * 9) * 0.3
    W[:, :, 2, :, :, :, :, :, :] += 1.0; W[:, :, 0:2, :, :, :, :, :, :] += 0.6
    LQV.clear(); LQQ.clear()
    for c, a, a2 in itertools.product((5, 6), (5, 6), LET): LQV[(c, a, a2)] = r.rand() * 2
    for c, a, m in itertools.product((5, 6), (5, 6), (31, 30, 1)): LQQ[(c, a, m)] = r.rand() * 3
    W0 = W.copy(); l3q_win(W, 7); write_l3q()
    if brk:   # control: drop the leaf correction (pass no l3q file) -> tot = window sum with the UB only
        L3FILE[0] = None
    CLSFILE[0] = os.path.join(WORK, 'clsT.bin'); class_table_R2(True).tofile(CLSFILE[0])
    rr, dt, ni = run_sep(7, W, -1e9, 300, 2, pats=False)
    for x in rr:
        if x[0] != 'V': continue
        nrows += 1; lk, sv = x[2], x[3]; w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]; tot = 0.0
        for i in range(7):
            idx = tuple(LI[w[(i + k) % 7]] for k in (-2, -1, 0, 1, 2)) + tuple(LI[s[(i + k) % 7]] for k in (-2, -1, 0, 1))
            tot += W0[idx]
        cf = l3q_terms(7, w, s); nhit += bool(cf); npay = globals().setdefault('NPAY', [0]); npay[0] += any(k[0] == 'lq' for k in cf)
        for k, v in cf.items(): tot += v * (LQV.get(k[1], 0.0) if k[0] == 'lq' else l3q_Qeff(*k[1]))
        if abs(tot - float(x[1])) > 1e-9:
            bad += 1
            if bad <= 3: print("  MISMATCH", lk, sv, x[1], tot, dict(cf))
    print('seed', seed, 'rows', nrows, 'with l3q terms', nhit, 'mismatches', bad, '%.1fs' % dt, flush=True)
print('payer-hit rows', NPAY[0] if 'NPAY' in globals() else 0); print('JSEP5 TEST%s: %d rows, %d with l3q terms, %d mismatches' % (' (BROKEN CONTROL: no leaf correction)' if brk else '', nrows, nhit, bad))
''', dict(G, TESTFLAGS=ARGV0, TESTN=os.environ.get("TESTN", "4")))
