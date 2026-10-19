"""Stage 16 A' check 4: census of the binder row with the LOCAL filter (s16_filter.local), same forbidden set.
usage: python3 s16_check4.py EXDIR TD TC [LK=7665566] [SV=6675666]"""
import sys, itertools
sys.argv, rest = sys.argv[:5] + ['x'], sys.argv[4:]
EX, TD, TC = sys.argv[1:4]
OPT = dict(a.split('=') for a in rest)
sys.argv = [sys.argv[0], EX, TD, TC, 'unused']
exec(open(__file__.replace('s16_check4.py', 's16_filter.py')).read().split("if __name__ == '__main__':")[0])
LK = [int(c) for c in OPT.get('LK', '7665566')]; SV = [int(c) for c in OPT.get('SV', '6675666')]; D = len(LK)
C = registry(); print('forbidden', len(C))
slots = []                       # (j, k) private k of w_j, in census order (j asc, k asc)
for j in range(D):
    for k in range(1, LK[j] - 5 + 1): slots.append((j, k))
kill = {}                        # slot -> set of killed values
for j in sorted({j for j, _ in slots}):
    win = tuple(LK[(j + o) % D] for o in (-2, -1, 1, 2)); s = [SV[(j + o) % D] for o in (-2, -1, 0, 1)]
    VAR, out = local(C, D, win, LK[j], unk=int(OPT.get('unk', '99')), strict=OPT.get('strict', '1') == '1')
    for key, names in out.items():
        if all(a == 0 or a == b for a, b in zip(key[:4], s)):
            for t, val in enumerate(key[4:]):
                if val: kill.setdefault((j, t + 1), {}).setdefault(val, set()).update(names)
for sl in slots: print('slot p%d%d' % sl, {v: sorted(n)[:4] for v, n in sorted(kill.get(sl, {}).items())})
LET = (5, 6, 7, 8, 9); n = 0; import hashlib; H = hashlib.md5()
for case in itertools.product(LET, repeat=len(slots)):
    if not any(v in kill.get(sl, {}) for sl, v in zip(slots, case)): n += 1; H.update((''.join(map(str, case)) + '\n').encode())
print('survivor set md5 %s' % H.hexdigest())
print('survivors %d of %d' % (n, 5 ** len(slots)))
