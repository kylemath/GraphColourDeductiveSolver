# s78 test 3b: how tight is the K* window bound?  For random and planted d = 7 arrangements: per (window k, side) the exact payee slot
# (masks with the f2b extras, as the C++ leaf) against KUB (python kstar_kub, as WIN), asserting exact <= KUB on every slot.
# usage: python3 kub_gap.py [N] [stack]
import sys, os, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loadeng import load
NARR = int(sys.argv[1]) if len(sys.argv) > 1 else 20000; STACK = sys.argv[2] if len(sys.argv) > 2 else 's75'
ns = load(STACK, 'full', ['kstar']); ns['l3q_load'](); ns['kt_load']()
K0, K1 = ns['kstar_kub']()
def widx(w, s, k):
    n = 7; L = [w[(k + o) % n] - 5 for o in (-2, -1, 0, 1, 2)] + [s[(k + o) % n] - 5 for o in (-2, -1, 0, 1)]
    ix = 0
    for v in L: ix = ix * 5 + v
    return ix
rng = random.Random(7802); C = collections.Counter()
for it in range(NARR):
    if it % 2: w, s = ns['kstar_force'](rng, 7)
    else: w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(7)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(7)]
    tub = tex = 0
    for k in range(7):
        ix = widx(w, s, k)
        for sgi, e1 in ((0, 1), (1, -1)):
            ub = int((K0 if sgi == 0 else K1)[ix]); ex = ns['kstar_payee_slot'](w, s, (k - e1) % 7, e1)
            assert ex <= ub, (w, s, k, e1)
            tub += ub; tex += ex
    C['arr'] += 1; C['ub_slots'] += tub; C['ex_slots'] += tex
    if tub: C['arr_ub'] += 1
    if tub > tex: C['arr_gap'] += 1
print('kub_gap (%s): %d d=7 arrangements (half planted): window-bound slots %d, exact payee slots %d (bound tight on %.1f%% of bound slots); %d arrangements with a bound slot, %d with a bound above exact; exact <= KUB on every slot: PASS'
      % (STACK, C['arr'], C['ub_slots'], C['ex_slots'], 100.0 * C['ex_slots'] / max(1, C['ub_slots']), C['arr_ub'], C['arr_gap']))
