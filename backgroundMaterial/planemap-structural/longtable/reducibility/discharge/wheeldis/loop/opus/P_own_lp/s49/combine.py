"""s49: combine the 2-ball kills (res_final.json), explore's pair60 grid v3 (kpriv v3) and the per-cell l3q pricing (price_final.json)
into per-row numbers.  Cell strings are 'p1p2': p1 = p_{k,1} next to s_{k-1}, p2 = p_{k,2} next to s_k (explore's priv<a><b>
is a = next to s_k, b = next to s_{k-1}, i.e. our 'ba').
(A) direct l3q: the receiver row credits +Qeff(c, a, m) per link 7 w_j and side sigma; a2 = w_j's private adjacent to a
    (sigma=+1: a = s_j, a2 = p_{j,2}; sigma=-1: a = s_{j-1}, a2 = p_{j,1}).  With the cell known, the credit can be
    q[(c, a, a2)] exactly (singleton mask, sound by RELAY_SPEC_s21 21.3).  Reduction per cell = Qeff - q(c, a, a2_cell).
    Row worst-case after split = base load - sum_j min_{surviving cells of w_j} reduction_j.
(B) payer spare: X = w_j as its own d7 centre; worst admissible load over its fillings with privates in surviving cells
    vs all cells (keeppen sol).  extra spare = worst_all - worst_surv.
usage: python3 combine.py > combine.out"""
import json, itertools, re, os
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
SOL = json.load(open(B + '/s44/run_A83/sol_q44fbA83.json')); t = SOL['t']
LQ = {tuple(k): v for k, v in SOL['lq']}; LQQ = {tuple(k): v for k, v in SOL['lQ']}
TAB = {}
for sg, fn in ((1, 'tab_1.json'), (-1, 'tab_-1.json')):
    for k, v in json.load(open(B + '/s33z/reg_A83/' + fn)).items():
        s_, wd, ao = k.split(); TAB[(int(s_),) + tuple(int(c) for c in wd) + tuple(int(c) for c in ao)] = v[0]
def letters(m): return [5 + i for i in range(5) if (m >> i) & 1]
def qeff(c, a, m): return max([LQQ.get((c, a, m), 0.0)] + [LQ.get((c, a, x), 0.0) for x in letters(m)])
ALL = [''.join(x) for x in itertools.product('56789', repeat=2)]
# pair60 grid v3 -> dead cells, our orientation
grid = {}
cur = None
for l in open('pair60_grid3.txt'):
    m = re.match(r'(\d+)/(\d+) w(\d)', l)
    if m: cur = (m.group(1), m.group(2), int(m.group(3))); grid[cur] = set(); continue
    m = re.match(r'\s+a=(\d)\s+(.*)', l)
    if m and cur:
        a = m.group(1); marks = m.group(2).split()
        for b, mk in zip('56789', marks):
            if mk != 'o': grid[cur].add(b + a)
res = {(r['link'], r['sword']): r for f in os.environ.get('RES', 'res_final.json').split(',') for r in json.load(open(f))}
pr = {(r['link'], r['sword']): r for f in os.environ.get('PRICE', 'price_final.json').split(',') for r in json.load(open(f))}
if os.environ.get('CERT'):   # weights and row order from another cert's top N receiver rows
    _rc = sorted([(c['w'], c['row']) for c in json.load(open(os.environ['CERT'])) if c['row'][0] == 'receiverR2'], key=lambda x: x[0])[:int(os.environ.get('TOPN', '5'))]
    _pr = {}
    for w_, r_ in _rc:
        k_ = (r_[2], r_[3]); assert k_ in pr, k_
        _pr[k_] = dict(pr[k_], w=w_)
    pr = _pr
out = []
for (LK, SV), P in pr.items():
    d = P['d']; lk = [int(c) for c in LK]; sv = [int(c) for c in SV]; n = d
    R = res.get((LK, SV)); w = P['w']
    row = {'link': LK, 'sword': SV, 'w': w, 'base': P['load'], 'cap': P['cap'], 'X': {}}
    for js, X in P['X'].items():
        j = int(js)
        mine = set(c for c, v in R['single'][js].items() if v) if R else set()
        g = grid.get((LK, SV, j), set())
        dead = mine | g
        # the l3q kill table itself (strict 1.5-ball + a2 containment, RELAY_SPEC_s21 21.4) kills a2 letters outside its mask
        mk = set()
        for sgm in (1, -1):
            c = lk[(j + sgm) % n]; a = sv[j] if sgm == 1 else sv[(j - 1) % n]
            if d != 7 or c > 6 or a > 6: continue
            o = sv[(j - 1) % n] if sgm == 1 else sv[j]
            m = TAB[(sgm, c, lk[(j + 2 * sgm) % n], lk[(j + 3 * sgm) % n], lk[(j + 4 * sgm) % n], a, o)]
            pos = 1 if sgm == 1 else 0
            mk |= set(cc for cc in ALL if int(cc[pos]) not in letters(m))
        tabdead = mk - dead; dead = dead | mk
        surv = [c for c in ALL if c not in dead]
        # (A) l3q payee terms at w_j
        terms = []
        for sgm in (1, -1):
            c = lk[(j + sgm) % n]; a = sv[j] if sgm == 1 else sv[(j - 1) % n]
            if d != 7 or c > 6 or a > 6: continue
            o = sv[(j - 1) % n] if sgm == 1 else sv[j]
            m = TAB[(sgm, c, lk[(j + 2 * sgm) % n], lk[(j + 3 * sgm) % n], lk[(j + 4 * sgm) % n], a, o)]
            pos = 1 if sgm == 1 else 0   # index in 'p1p2' of a2
            Qe = qeff(c, a, m)
            red = {cc: Qe - LQ.get((c, a, int(cc[pos])), 0.0) for cc in ALL}
            terms.append({'side': sgm, 'c': c, 'a': a, 'mask': letters(m), 'a2': 'p%d,%d' % (j, pos + 1), 'Qeff': Qe,
                          'a2_5_dead': all(cc in dead for cc in ALL if cc[pos] == '5'), 'red_min_surv': min(red[cc] for cc in surv) if surv else None})
        pc = X['percell']
        def wl(cs):
            v = [pc[c][0] for c in cs if pc.get(c)]
            return max(v) if v else None
        wa, ws = wl(ALL), wl(surv)
        worst_cell = max((c for c in surv if pc.get(c)), key=lambda c: pc[c][0]) if surv else None
        five_dead = all(c in dead for c in ALL if '5' in c)
        row['X'][j] = {'mine': sorted(mine), 'grid': sorted(g), 'tab': sorted(tabdead), 'dead': sorted(dead), 'surv': surv, 'five_cells_all_dead': five_dead,
                       'l3q': terms, 'worst_all': wa, 'worst_surv': ws, 'extra_spare': (wa - ws) if ws is not None else None,
                       'spare_surv': (1 + t - ws) if ws is not None else None, 'worst_surv_cell': worst_cell,
                       'worst_surv_row': pc[worst_cell][1:4] if worst_cell else None, 'worst_all_row': [x for x in max((pc[c] for c in ALL if pc.get(c)), key=lambda x: x[0])[1:4]]}
    A = sum(tm['red_min_surv'] or 0 for X in row['X'].values() for tm in X['l3q'])
    Aall = sum(tm['red_min_surv'] or 0 for X in row['X'].values() for tm in X['l3q'] if tm['a2_5_dead'])
    Bx = sum(X['extra_spare'] or 0 for X in row['X'].values())
    row.update({'A_red': A, 'A_red_nosplit': Aall, 'B_extra': Bx, 'gainA': abs(w) * A, 'gainB': abs(w) * Bx})
    out.append(row)
json.dump(out, open(os.environ.get('OUT', 'combine.json'), 'w'), indent=1)
for r in out:
    print('%s/%s w %.6f base %.9f cap %.9f: A red %.6f (of which row-mask only %.6f) gainA %.6f; B extra %.6f gainB %.6f' % (
        r['link'], r['sword'], r['w'], r['base'], r['cap'], r['A_red'], r['A_red_nosplit'], r['gainA'], r['B_extra'], r['gainB']))
    for j, X in r['X'].items():
        print('   w%d: dead %d (mine %d, grid %d, l3q-table extra %d) five-all-dead %s; surv %s' % (j, len(X['dead']), len(X['mine']), len(X['grid']), len(X['tab']), X['five_cells_all_dead'], ' '.join(X['surv'])))
        for tm in X['l3q']: print('      l3q side %+d c%d a%d mask %s a2 %s Qeff %.6f red_min surv %s; all a2=5 cells dead %s' % (tm['side'], tm['c'], tm['a'], tm['mask'], tm['a2'], tm['Qeff'], tm['red_min_surv'], tm['a2_5_dead']))
        print('      X worst all %.6f %s; surv %s cell %s %s; extra %s; spare_surv %s' % (X['worst_all'], X['worst_all_row'], X['worst_surv'], X['worst_surv_cell'], X['worst_surv_row'], X['extra_spare'], X['spare_surv']))
