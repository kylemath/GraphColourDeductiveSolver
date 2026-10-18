"""Job 30 F: Opus's option-F count (tcount.py, verbatim enumeration) against Studio's wlp3xt tfull keys.
The physical side is carried through the reflection (tcount.py appends it after key() may have reflected)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'tcount.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'tcount.py')), 1)
exec(src)
def rev5(r): return (r[0], r[4], r[3], r[2], r[1])
def tkey(raw, fa, fe, side):
    raw = tuple(raw); rv = rev5(raw)
    r, flip = (raw, False) if raw <= rv else (rv, True)
    if flip: fa, fe, side = fe, fa, ('e' if side == 'a' else 'a')
    if r == rev5(r) and (fe, fa, 'e' if side == 'a' else 'a') < (fa, fe, side): fa, fe, side = fe, fa, ('e' if side == 'a' else 'a')
    return (r, fa, fe, side)
def ykey(raw, fa, fe):
    return tkey(raw, fa, fe, 'a')[:3]
FL = lambda sp: (5, 6, 7, 8, 9) if sp == 6 else (0,)
Ys = {ykey(r, fa, fe) for r in roots for fa in FL(r[1]) for fe in FL(r[4])}
Ts = {tkey(r, fa, fe, sd) for r in roots for fa in FL(r[1]) for fe in FL(r[4]) for sd in ('a', 'e') if (fa if sd == 'a' else fe) >= 7}
Tok = set(); Yok = set()
for w in senders:
    x = list(w)
    for j in [j for j in range(5) if x[j] >= 7]:
        o = tuple(x[(j + k) % 5] for k in range(5)); A, E = zopts(o)
        for za in A:
            for ze in E:
                fa, fe = (0 if za is None else za), (0 if ze is None else ze)
                Yok.add(ykey(o, fa, fe))
                if fa >= 7: Tok.add(tkey(o, fa, fe, 'a'))
                if fe >= 7: Tok.add(tkey(o, fa, fe, 'e'))
print('Opus Y %d, Opus T2 %d (side slip), Opus enumeration with the physical side: Y %d, T %d' % (len(Y), len(T2), len(Yok), len(Tok)))
print('Studio Y %d, T %d; equal: Y %s, T %s' % (len(Ys), len(Ts), Yok == Ys, Tok == Ts))
