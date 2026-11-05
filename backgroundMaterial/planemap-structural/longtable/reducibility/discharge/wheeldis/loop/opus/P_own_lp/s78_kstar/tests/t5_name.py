# s78 test 5 follow-up: for every violated row of the planted run (logs/t5_violated.txt: d load excess link apexes), the engine's K1
# coefficient (payee slots - payer slots), the payer link positions, and the row value with K1 = 0 (= value - 0.125 * coef: rows are
# linear in K1), which must be <= 1 + t (in09 is FEASIBLE at K1 = 0), so K* is the cause of every violation.
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loadeng import load
VF = sys.argv[1]
ns = load('s75', 'full', ['kstar']); ns['l3q_load'](); ns['kt_load']()
K1 = 0.125; t = 0.033528013422; thr = 1 + t
L = [l.split() for l in open(VF) if l.strip()]
C = collections.Counter(); ex = []
for d, val, exc, lk, sv in L:
    w = [int(c) for c in lk]; s = [int(c) for c in sv]
    cf = ns['recv_coef_R2'](7, lk, sv, True).get(('ks', 'K1'), 0)
    pay = [(j, e) for j in range(7) for e in (1, -1) if ns['kstar_payee_slot'](w, s, j, e)]
    payer = [(i, e) for i in range(7) for e in (1, -1) if ns['kstar_payer_slot'](w, s, i, e)]
    v0 = float(val) - K1 * cf
    C['rows'] += 1; C['coef>0'] += cf > 0; C['v0<=thr'] += v0 <= thr + 1e-9; C['slots%d' % len(pay)] += 1; C['payer_slots'] += len(payer)
    if len(ex) < 6: ex.append('R 7 %s %s: value %.9f (excess %s), K1 coefficient %+d, payee slots (payer link index j, side e1) %s, own payer slots %s, value at K1 = 0: %.9f' % (lk, sv, float(val), exc, cf, pay, payer, v0))
print('t5: %d violated rows named; K1 coefficient > 0 on %d; value at K1 = 0 <= 1 + t on %d; payee-slot counts %s; payer slots in these rows %d'
      % (C['rows'], C['coef>0'], C['v0<=thr'], {k: v for k, v in C.items() if k.startswith('slots')}, C['payer_slots']))
for e in ex: print('  ' + e)
