# Restricted LP [C]: does adding the improving 7->7 keys (strict K1) plus sink receiver rows lower the pool bound below 7/207?
# Pool: cert rows (58) + all senderR2 rows + mrowR2/mrowL closure on every M / lQ in the pool + strict mrowQ + sinks.
# New columns q[K] (K in KEYS), cap 3 (as lq).  Receiver slot credit QS[(slot-sig)] >= q[K] for K in the slot's masked options.
# Sink rows: every B picture adjacent to an unabsorbed emitter A (overlap letters fixed by A's picture, masks both ways),
#   generated lazily by load; pattern admissibility (engine) checked only for rows added.  Fresh outflow columns (x, lq keys
#   absent from the base pool) fixed at 0: sinks cannot pass charge on through channels outside the pool.  Label [C].
import json, itertools, collections, sys, time
ARGV = list(sys.argv)
from fractions import Fraction as F
import numpy as np, highspy
import price77 as P, check2 as Q
import os; P.MODE = os.environ.get('W5MODE', 'strict'); ns = P.ns; ns['load_patterns']()
KEYS = [tuple(k) for k in json.loads(ARGV[1])] if len(ARGV) > 1 and ARGV[1] != "-" else Q.KEYS3
ROUNDS = int(ARGV[2]) if len(ARGV) > 2 else 4; PERROUND = int(ARGV[3]) if len(ARGV) > 3 else 150
recv = lambda lk, sv: dict(ns['recv_coef_R2'](7, lk, sv, True))
C = json.load(open('/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s62_w5check/certs/certP2full_rat.json'))
rows = []   # (kind, cf dict, lo, hi, label)
for wd, cf, b in ns['R2_sender_rows'](): c = dict(cf); c[('t',)] = 1; rows.append(('S', c, 1.0, np.inf, wd))
for r in C:
    rw = r['row']
    if rw[0] == 'cons2': rows.append(('C', dict(ns['cons2_coef'](tuple(rw[1]), tuple(rw[2]))), 0.0, 0.0, 'cons2'))
def opts_slot(w, s, j): return frozenset(k for k in P.slot_opts(w, s, j, 1) if k in KEYS)
def qterms(w, s):
    c = collections.Counter()
    for i in range(7):
        if w[i] >= 7 and P.key1(P.rot(w, i)) in KEYS: c[('q', P.key1(P.rot(w, i)))] -= 1
        if w[i] == 7:
            o = opts_slot(w, s, i)
            if o: c[('QS', o)] += 1
    return c
def recv_row(lk, sv):
    c = recv(lk, sv); w = [int(x) for x in lk]; s = [int(x) for x in sv]
    for k, v in qterms(w, s).items(): c[k] = c.get(k, 0) + v
    c[('t',)] = c.get(('t',), 0) - 1; return c
for lk, sv, _ in P.R: rows.append(('R', recv_row(lk, sv), -np.inf, 1.0, lk + '/' + sv))
BASECOLS = set(k for r in rows for k in r[1])
def closure(rows, done):
    add = []
    for k in sorted({k for r in rows for k in r[1]} - done, key=str):
        done.add(k)
        if k[0] == 'M':
            for h in ns['sig2_keys'](k[1]): add.append(('m', {('h', h): 1, k: -1}, -np.inf, 0.0, 'mrowR2'))
        elif k[0] == 'lQ':
            sg = k[1]; c_, a_, m = sg[-3:]; V = sg[0] if len(sg) == 4 else None
            for a2 in ns['l3q_mask_letters'](m): add.append(('l', {('lq', (c_, a_, a2) if V is None else (V, c_, a_, a2)): 1, k: -1}, -np.inf, 0.0, 'mrowL'))
        elif k[0] == 'QS':
            for K in k[1]: add.append(('Q', {('q', K): 1, k: -1}, -np.inf, 0.0, 'mrowQ'))
    return add
done = set(); rows += closure(rows, done); rows += closure(rows, done)
def solve(rows, fixed0):
    h = highspy.Highs(); h.setOptionValue('output_flag', False); inf = highspy.kHighsInf
    cols = {}
    for r in rows:
        for k in r[1]:
            if k not in cols:
                cols[k] = len(cols)
                lo = -inf if k[0] == 't' else 0.0
                hi = 0.0 if k in fixed0 else 3.0 if k[0] in ('x', 'lq', 'q') else inf
                h.addVar(lo, hi)
    h.changeColCost(cols[('t',)], 1.0)
    for r in rows:
        idx = np.array([cols[k] for k in r[1]], dtype=np.int32); val = np.array([float(v) for v in r[1].values()])
        h.addRow(r[2] if np.isfinite(r[2]) else -inf, r[3] if np.isfinite(r[3]) else inf, len(idx), idx, val)
    h.run(); sol = h.getSolution(); x = sol.col_value
    return x[cols[('t',)]], {k: x[i] for k, i in cols.items()}, sol.row_dual
# ---- base checks: pool without q, pool with q (no sinks)
noq = [r for r in rows if not any(k[0] in ('q', 'QS') for k in r[1])]
noq = [(a, {k: v for k, v in c.items()}, lo, hi, lb) for a, c, lo, hi, lb in noq]
t0, _, _ = solve([(a, {k: v for k, v in c.items() if k[0] not in ('q', 'QS')}, lo, hi, lb) for a, c, lo, hi, lb in rows if a != 'Q'], set())
t1, V, _ = solve(rows, set())
print('pool rows %d | LP t: old columns only %.9f (7/207 = %.9f) | with q keys, no sinks %.9f' % (len(rows), t0, 7 / 207, t1), flush=True)
# ---- sink candidates (cheap filters), coefficient dicts computed once
isR5, isR6, RBIG = ns['isR5'], ns['isR6'], ns['RBIG']
def cheap_ok(w, s):
    if ''.join(map(str, P.canon_cyc(w))) in RBIG: return False
    for i in range(7):
        wd = [7, w[(i + 1) % 7], s[i], s[(i - 1) % 7], w[(i - 1) % 7]]
        if w[i] == 5 and isR5(wd): return False
        if w[i] == 6 and all(isR6([7, w[(i + 1) % 7], s[i], p, s[(i - 1) % 7], w[(i - 1) % 7]]) for p in P.LET): return False
    return True
EMS = [(a, i) for (a, i, k1, k2) in P.EM if k1 in KEYS]
cand = []
t_ = time.time()
for a, i in EMS:
    wa, sa = P.rows[a]; A = lambda k: wa[(i + k) % 7]; AS = lambda k: sa[(i + k) % 7]
    # B with A at position 0, B's +1 side = A's +1 side (o = +1 orientation of check2.overlap_ok)
    fixed_w = {0: 7, 1: A(1), 6: A(-1), 2: AS(0), 5: AS(-1)}; fixed_s = {0: A(2), 6: A(-2)}
    if A(1) == 5: fixed_s[1] = AS(1)
    if A(-1) == 5: fixed_s[5] = AS(-2)
    fw = [k for k in range(7) if k not in fixed_w]; fs = [k for k in range(7) if k not in fixed_s]
    n0 = 0
    for vw in itertools.product(P.LET, repeat=len(fw)):
        for vs in itertools.product(P.LET, repeat=len(fs)):
            w = [0] * 7; s = [0] * 7
            for k, v in fixed_w.items(): w[k] = v
            for k, v in fixed_s.items(): s[k] = v
            for k, v in zip(fw, vw): w[k] = v
            for k, v in zip(fs, vs): s[k] = v
            m1, m2 = P.mask(w, s, 0, 1), P.mask(w, s, 0, -1)
            if (m1 is not None and A(3) not in m1) or (m2 is not None and A(-3) not in m2): continue
            ma1, ma2 = P.mask(wa, sa, i, 1), P.mask(wa, sa, i, -1)     # A's masks on B's privates w[3], w[4]
            if (ma1 is not None and w[3] not in ma1) or (ma2 is not None and w[4] not in ma2): continue
            if not cheap_ok(w, s): continue
            n0 += 1
            lk, sv = ''.join(map(str, w)), ''.join(map(str, s))
            cand.append((lk, sv, (a, i)))
    print('emitter %s pos %d: %d sink candidates after cheap filters' % (P.names[a], i, n0), flush=True)
cf_c = [recv_row(lk, sv) for lk, sv, _ in cand]
print('sink coefficient rows computed in %.0fs' % (time.time() - t_), flush=True)
fixed0 = set(); FREE = os.environ.get("W5FREE") == "1"
for c in cf_c:
    for k in c:
        if k not in BASECOLS and k[0] in ("x", "lq") and not FREE: fixed0.add(k)
added = set(); t = t1; hist = [('no sinks', t1)]
adm = ns['admissible']
for rnd in range(ROUNDS):
    val = lambda k: V.get(k, 0.0)
    loads = np.array([sum(v * val(k) for k, v in c.items() if k[0] != 't') for c in cf_c])
    viol = np.argsort(-(loads - (1 + t)))
    new = []
    for ix in viol:
        if loads[ix] - (1 + t) <= 1e-9 or len(new) >= PERROUND: break
        if ix in added: continue
        lk, sv, _ = cand[ix]
        if adm(7, lk, sv) is None: new.append(ix)
        else: added.add(ix)      # inadmissible: never a row
    if not new: print('round %d: no violated admissible sink rows' % rnd); break
    for ix in new:
        added.add(ix); rows.append(('B', cf_c[ix], -np.inf, 1.0, cand[ix][0] + '/' + cand[ix][1]))
    rows += closure(rows[-len(new):], done)
    t, V, _ = solve(rows, fixed0); hist.append(('round %d +%d sinks' % (rnd, len(new)), t))
    print('round %d: added %d sink rows (max violation %.4f); LP t = %.9f' % (rnd, len(new), loads[new[0]] - (1 + t), t), flush=True)
print('HISTORY', hist)
print('q values', {k: round(v, 6) for k, v in V.items() if k[0] == 'q'})
_t, _V, _dual = solve(rows, fixed0)
from fractions import Fraction as _F
print('final t = %.9f ~ %s' % (_t, _F(_t).limit_denominator(2000)))
agg = collections.Counter(); nact = collections.Counter()
for r, dv in zip(rows, _dual):
    if abs(dv) > 1e-9: agg[r[0]] += abs(dv); nact[r[0]] += 1
print('dual mass by row kind (S sender, R cert receiver, B sink, C cons2, m mrowR2, l mrowL, Q mrowQ):', {k: (round(v, 4), nact[k]) for k, v in agg.items()})
top = sorted(((abs(dv), r[0], r[4]) for r, dv in zip(rows, _dual) if r[0] in ('R', 'B') and abs(dv) > 1e-9), reverse=True)[:16]
for x in top: print('  receiver dual %.5f %s %s' % x)
