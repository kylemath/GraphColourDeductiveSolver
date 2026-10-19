"""Stage 16 A' check 4 with the FULL 3-ball test (s16_filter.fullrow).  usage: python3 s16_check4full.py EXDIR TD TC [LK=] [SV=]"""
import sys, itertools
EX, TD, TC = sys.argv[1:4]; OPT = dict(a.split('=') for a in sys.argv[4:])
sys.argv = [sys.argv[0], EX, TD, TC, 'unused']
exec(open(__file__.replace('s16_check4full.py', 's16_filter.py')).read().replace("if __name__ == '__main__':", "if False:"))
LK = [int(c) for c in OPT.get('LK', '7665566')]; SV = [int(c) for c in OPT.get('SV', '6675666')]; D = len(LK)
C = registry(); print('forbidden', len(C)); K = fullrow(C, D, LK, SV)
slots = [(j, k) for j in range(D) for k in range(1, LK[j] - 4)]
for sl in slots: print('slot p%d%d' % sl, {v: sorted(n)[:4] for v, n in sorted(K.get(sl, {}).items())})
n = sum(1 for case in itertools.product((5, 6, 7, 8, 9), repeat=len(slots)) if not any(v in K.get(sl, {}) for sl, v in zip(slots, case)))
print('survivors %d of %d' % (n, 5 ** len(slots)))
