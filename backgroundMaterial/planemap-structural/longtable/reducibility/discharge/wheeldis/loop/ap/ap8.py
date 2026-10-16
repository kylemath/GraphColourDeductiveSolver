"""EXPLORE round 21 follow-up: of the H-A' misses (fillings of v's 2-ball not killed at v) that carry an 8 on v's
link, how many are killed by a D window centred at that 8?  The 8's arrangement is read off the filling with
pairs.py view (v = 7 at one link slot); a window kills only if every slot it constrains is known and matches.
Window sets: round 16's D windows (win89.out, d = 8) and every d = 8 D/C name in the registries.
Usage: python3 ap8.py SEEDS"""
import sys, os, re
APD8 = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(APD8, 'ap.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(APD8, 'ap.py')), 1)
exec(src)
P8 = {}
for nm, (d, P) in G['PATS'].items():
    pass
# d = 8 patterns: re-parse every d = 8 D/C name with w2's parse
DV, CV, parse = G['DV'], G['CV'], G['parse']
ALL8 = {nm: parse(nm)[1] for nm in list(DV) + list(CV) if re.match(r'^[epf]8_', nm) and (DV.get(nm) == 'D' or CV.get(nm) == 'C')}
W16 = set(l.split()[0] for l in open(os.path.join(LOOP, 'w2', 'win89.out')) if 'D=true' in l and l.startswith('f8_'))
ALL8 = {k: v for k, v in ALL8.items() if v}
print('d=8 D/C names %d, of them round 16 %d' % (len(ALL8), len(W16 & set(ALL8))), flush=True)
def known_hit(P, L, S):
    d = len(L)
    for refl in (0, 1):
        for r in range(d):
            ok = True
            for p, m in P:
                q = ((-p if refl else p) + r) % d; mm = m[::-1] if refl else m
                cells = [L[q], L[(q + 1) % d], S[q], S[(q - 1) % d], L[(q - 1) % d]]
                if cells[0] != '5' or any(c == '?' or c not in st for c, st in zip(cells[1:], mm)): ok = False; break
            if ok: return True
    return False
tot = with8 = k16 = kall = 0; cache = {}
for (vL, vS), FM in MISSF:
    for row in FM:
        lk = ''.join(str(x + 5) for x in row[:7]); sv = ''.join(str(x + 5) for x in row[7:]); tot += 1
        qs = [q for q in range(7) if lk[q] == '8']
        if not qs: continue
        with8 += 1; a16 = aall = False
        for q in qs:
            key = view(lk, sv, q)
            if key not in cache:
                h = [nm for nm, P in ALL8.items() if known_hit(P, *key)]
                cache[key] = (any(nm in W16 for nm in h), bool(h))
            a16 |= cache[key][0]; aall |= cache[key][1]
        k16 += a16; kall += aall
res = 'misses %d; with a link 8 %d; killed at a link 8 by round-16 windows %d (%.1f%%), by any d=8 D/C window %d (%.1f%%); distinct 8-views %d' % (
    tot, with8, k16, 100.0 * k16 / max(with8, 1), kall, 100.0 * kall / max(with8, 1), len(cache))
print(res); open(os.path.join(APD8, 'ap8.txt'), 'w').write(res + '\n')
