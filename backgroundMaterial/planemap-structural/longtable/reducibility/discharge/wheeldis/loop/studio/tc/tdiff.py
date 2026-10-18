"""Job 30 B: diff Opus's option-B T keys (tcount_flag.py, verbatim) against Studio's wlp3xt T keys."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'tcount_flag.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'tcount_flag.py')), 1)
exec(src)
# Studio's keying (wlp3xt.tkey), flags 0/1 for small/big, side a/e; None (no 6) -> 0
def rev5(r): return (r[0], r[4], r[3], r[2], r[1])
def canon_root(raw):
    raw = tuple(raw); rv = rev5(raw); return (raw, False) if raw <= rv else (rv, True)
def tkey(raw, fa, fe, side):
    r, flip = canon_root(raw)
    if flip: fa, fe, side = fe, fa, ('e' if side == 'a' else 'a')
    if r == rev5(r) and (fe, fa, 'e' if side == 'a' else 'a') < (fa, fe, side): fa, fe, side = fe, fa, ('e' if side == 'a' else 'a')
    return (r, fa, fe, side)
TAUV = {tkey(r, fa, fe, sd) for r in roots for fa in (0, 1) for fe in (0, 1) for sd in ('a', 'e')
        if (not fa or r[1] == 6) and (not fe or r[4] == 6) and (fa if sd == 'a' else fe)}
# Opus's T with the side label recomputed from the original oriented word (the correct physical side)
Tok = set()
for w in senders:
    x = list(w)
    for j in [j for j in range(5) if x[j] >= 7]:
        o = tuple(x[(j + k) % 5] for k in range(5)); A, E = zopts(o)
        for za in A:
            for ze in E:
                fa, fe = (0 if za is None else CL(za)), (0 if ze is None else CL(ze))
                if fa: Tok.add(tkey(o, fa, fe, 'a'))
                if fe: Tok.add(tkey(o, fa, fe, 'e'))
def n0(k): return (k[0], 0 if k[1] is None else k[1], 0 if k[2] is None else k[2], k[3])
T2n = {n0(k) for k in T2}
print('Opus T2 %d, Studio %d, Opus keys with the physical side recomputed %d (equal to Studio: %s)' % (len(T2), len(TAUV), len(Tok), Tok == TAUV))
extra = sorted(T2n - TAUV)
print('Opus keys not in Studio, after Studio canonicalisation of each:', len(extra))
bad = 0
for k in extra:
    c = tkey(k[0], k[1], k[2], k[3])
    if c not in TAUV: bad += 1
    print('  ', k, '-> canonical', c, 'in Studio' if c in TAUV else 'MISSING')
# Opus's mislabel: key() may reflect o but the side is appended unreflected
mis = 0
for w in senders:
    x = list(w)
    for j in [j for j in range(5) if x[j] >= 7]:
        o = tuple(x[(j + k) % 5] for k in range(5)); r = rev5(o)
        if (r, 0, 0) < (o, 0, 0) and 6 in (o[1], o[4]): mis += 1
print('oriented roots that key() reflects and that have a 6 spoke (where the appended side label is wrong):', mis)
print('extra keys that do not canonicalise into Studio set:', bad)
# side-map check: every kept key sends across a 6 (its side's letter is 6) with that side's flag set
okside = all(k[0][1 if k[3] == 'a' else 4] == 6 and (k[1] if k[3] == 'a' else k[2]) == 1 for k in TAUV)
badO = [k for k in T2n if not (k[0][1 if k[3] == 'a' else 4] == 6 and (k[1] if k[3] == 'a' else k[2]) == 1)]
print('Studio keys: side letter 6 and side flag 1 for all %d: %s; Opus T2 keys violating it: %d' % (len(TAUV), okside, len(badO)))
# explicit merged pairs: an oriented root that reflects, its physical side, and the kept key
for o in [(7, 6, 6, 5, 5), (8, 6, 7, 5, 5), (7, 6, 5, 6, 6)]:
    if o not in [tuple(r) for r in roots] and canon_root(o)[0] not in roots: continue
    print('  oriented', o, 'T across its side-a 6 (f_a=1, f_e=0) -> kept key', tkey(o, 1, 0, 'a'))
