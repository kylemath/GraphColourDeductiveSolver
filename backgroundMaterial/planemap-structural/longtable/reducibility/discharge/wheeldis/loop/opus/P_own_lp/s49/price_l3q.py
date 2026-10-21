"""s49 pricing (no solve): spare of a binder's link 7 X = w_k as a centre of its own degree-7 row, under the A83 keeppen solution.
X's row in its own frame: link L' = (u, w_{k+1}, s_k, p_{k,2}, p_{k,1}, s_{k-1}, w_{k-1}) (rotation order around X), apexes
S'_0 = w_{k+2}; S'_1 = p_{k+1,1} if w_{k+1} >= 6 else s_{k+1}; S'_2..S'_4 = ring-3 (free); S'_5 = p_{k-1,last} if w_{k-1} >= 6
else s_{k-2}; S'_6 = w_{k-2}.  Free letters 5..9.  Load = recv_coef_R2(7, L', S') . sol (y, x, M = max h over sig2 keys, r, lq,
lQ at Qeff, fb), the receiver row's own valuation; worst case over admissible fillings (engine admissible(), A83 registry + rpatN3).
Reports max load over all 25 private cells and over the surviving cells (given on the command line per X).
Also prints the binder row's own load (control: binding rows should sit at cap 1 + t) and its lQ terms.
usage: python3 price_l3q.py SPEC.json OUT.json"""
import sys, os, json, itertools, collections, time
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
SC = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad'
M = SC + '/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
E = B + '/s44/eng'; Q = B + '/s33z/reg_A83'; SOL = B + '/s44/run_A83/sol_q44fbA83.json'
opts = ['xon', 'apexcls', 'filt16', 'killtab=' + Q + '/f/kill/kill6', 'hat5', 'consall', 'l3q', 'l3qtab=' + Q + '/tab_1.json,' + Q + '/tab_-1.json',
        'lqcap=3', 'fb', 'fbdir=6', 'fbcap=3', 'rpatN=' + B + '/s39o/rpatN3.txt', 'root=' + M, 'args=' + Q + '/args_A83.txt',
        'rpat=' + B + '/rpatD.txt', 'exname=' + B + '/s40f/exname_rm128.txt', 'work=' + SC + '/P/w49p']
os.makedirs(SC + '/P/w49p', exist_ok=True)
ARGS = [os.path.abspath(a) for a in sys.argv[1:3]]; sv_ = sys.argv; sys.argv = [E + '/pcheck.py', 'none'] + opts
ns = {'__file__': sys.argv[0], '__name__': 'pcheck_lib'}
os.chdir(E)
exec(open(sys.argv[0]).read().replace("}.get(CMD, lambda: print(__doc__))()", "}.get(CMD, lambda: None)()"), ns)
sys.argv = sv_
t0 = time.time(); ns['load_patterns'](); print('patterns loaded %.0fs' % (time.time() - t0), flush=True)
Sj = json.load(open(SOL)); t = Sj['t']
ns['LQV'].clear(); ns['LQV'].update({tuple(k): v for k, v in Sj.get('lq', [])}); ns['LQQ'].clear(); ns['LQQ'].update({tuple(k): v for k, v in Sj.get('lQ', [])})
ns['l3q_load']()
Y = Sj['y']; X = {int(k): v for k, v in Sj['x'].items()}; HV2 = {tuple(k): v for k, v in Sj['h']}
FAM = {f: {tuple(k): v for k, v in Sj.get(f, [])} for f in ('r', 'fb', 'lq', 'g', 'rr', 'z', 'zr', 'D', 'q', 'v', 'f')}
unk = collections.Counter()
def val(k):
    f = k[0]
    if f == 'y': return Y.get(ns['rname'](k[1]), 0.0)
    if f == 'x': return X.get(k[1], 0.0)
    if f == 'M': ks = ns['sig2_keys'](k[1]); return max([HV2.get(h, 0.0) for h in ks] or [0.0])
    if f == 'lQ': return ns['l3q_Qeff'](*k[1])
    if f in FAM: return FAM[f].get(tuple(k[1]) if isinstance(k[1], (list, tuple)) else k[1], 0.0)
    unk[f] += 1; return 0.0
def load(d, lk, sv, detail=False):
    cf = ns['recv_coef_R2'](d, lk, sv, True)
    tot = 0.0; parts = []
    for k, c in cf.items():
        v = val(k); tot += c * v
        if detail and abs(c * v) > 1e-12: parts.append((round(c * v, 9), k))
    return (tot, sorted(parts, key=lambda x: -abs(x[0]))) if detail else tot
def adm(d, lk, sv):
    r = ns['admissible'](d, lk, sv); return not r
spec = json.load(open(ARGS[0])); out = []
for row in spec:
    d, LK, SV = row['d'], row['link'], row['sword']; lk = [int(c) for c in LK]; sv = [int(c) for c in SV]
    bl, parts = load(d, LK, SV, True)
    print('binder %d %s/%s w %.9f: load %.9f cap %.9f slack %.3g' % (d, LK, SV, row['w'], bl, d - 6 + t, d - 6 + t - bl), flush=True)
    lQt = [(v, k) for v, k in parts if k[0] in ('lQ', 'lq')]
    print('   l3q terms:', lQt)
    rr = {'d': d, 'link': LK, 'sword': SV, 'w': row['w'], 'load': bl, 'cap': d - 6 + t, 'l3q_terms': [[v, repr(k)] for v, k in lQt],
          'top_terms': [[v, repr(k)] for v, k in parts[:12]], 'X': {}}
    for k_s, surv in row['X'].items():
        k = int(k_s); n = d
        if lk[k] != 7: continue
        wp, wm = lk[(k + 1) % n], lk[(k - 1) % n]
        rows = []
        for p1, p2 in itertools.product((5, 6, 7, 8, 9), repeat=2):
            for ra, rb, rc in itertools.product((5, 6, 7, 8, 9), repeat=3):
                for a1 in ((5, 6, 7, 8, 9) if wp >= 6 else (sv[(k + 1) % n],)):
                    for a5 in ((5, 6, 7, 8, 9) if wm >= 6 else (sv[(k - 2) % n],)):
                        L2 = '%d%d%d%d%d%d%d' % (d if d <= 9 else 9, wp, sv[k], p2, p1, sv[(k - 1) % n], wm)
                        S2 = '%d%d%d%d%d%d%d' % (lk[(k + 2) % n], a1, ra, rb, rc, a5, lk[(k - 2) % n])
                        rows.append((load(7, L2, S2), '%d%d' % (p1, p2), L2, S2))
        rows.sort(key=lambda x: -x[0])
        def worst(cellset):
            nchk = 0
            for ld, c, L2, S2 in rows:
                if c not in cellset: continue
                nchk += 1
                if adm(7, L2, S2): return ld, c, L2, S2, nchk
            return None
        allc = set('%d%d' % x for x in itertools.product((5, 6, 7, 8, 9), repeat=2))
        wa = worst(allc); ws = worst(set(surv)) if surv else None
        no5 = set(c for c in allc if '5' not in c); wn = worst(no5)
        percell = {c: worst({c}) for c in sorted(allc)}
        rec = {'cells_surv': sorted(surv), 'worst_all': wa, 'worst_surv': ws, 'worst_no5': wn, 'cap': 1 + t, 'percell': percell}
        rr['X'][k] = rec
        print('  X = w%d: worst load all cells %s; surviving %s; no-5 cells %s; cap %.9f (%.0fs)' % (k, wa, ws, wn, 1 + t, time.time() - t0), flush=True)
    out.append(rr); json.dump(out, open(ARGS[1], "w"), indent=1, default=str)
print('unknown families valued 0:', dict(unk))
