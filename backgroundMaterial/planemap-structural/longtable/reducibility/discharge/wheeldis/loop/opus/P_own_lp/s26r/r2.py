"""radius-2 census of receiver rows: free = privates of the <=8 link vertices; s and w fixed by the row."""
import sys, itertools, collections, json, time
from ball import *
C = registry(); print('forbidden set', len(C), flush=True)
LET = (5, 6, 7, 8, NEVER)
def ch(l): return 6 - (9 if l == NEVER else l)
def census(D, LK, SV, dump=None):
    LK = [int(c) for c in LK]; SV = [int(c) for c in SV]
    P, pa, pf, order2, _, _ = frame(D, LK)
    fd = {('u',): D if D <= 8 else D}       # receiver degree is exact in the row
    for i in range(D): fd[('w', i)] = LK[i] if LK[i] < 9 else NEVER; fd[('s', i)] = SV[i] if SV[i] < 9 else NEVER
    free = [x for x in order2 if x[0] == 'p' and LK[x[1]] < 9]
    for x in order2:
        if x[0] == 'p' and LK[x[1]] >= 9: fd[x] = NEVER
    R = reqsets(C, P, pa, pf, fd, set(free))
    if frozenset() in R: return dict(row='%d %s/%s' % (D, ''.join(map(str, LK)), ''.join(map(str, SV))), dead_fixed=R[frozenset()])
    base = sum(ch(fd[x]) for x in fd if x[0] in 'uws' and x not in free)  # fixed part (>=9 counted as 9)
    # all fixed vertices: u, w, s, unknown privates (each >=9 private counted as 9 -> charge <= -3)
    Rl = [(tuple(r), n) for r, n in R.items()]
    surv = []; used = collections.Counter()
    for vals in itertools.product(LET, repeat=len(free)):
        a = dict(zip(free, vals)); hit = None
        for r, n in Rl:
            if all(a[v] == d for v, d in r): hit = n; break
        if hit is None: surv.append(vals)
        else: used[hit] += 1
    unkp = [x for x in fd if x[0] == 'p']
    fixedc = sum(ch(fd[x]) for x in fd if x[0] in ('u', 'w', 's')) + sum(ch(NEVER) for x in unkp)
    tot = [fixedc + sum(ch(v) for v in s) for s in surv]
    res = dict(row='%d %s/%s' % (D, ''.join(map(str, LK)), ''.join(map(str, SV))), nfree=len(free), free=[''.join(map(str, f)) for f in free],
               domain=5 ** len(free), survivors=len(surv), fixed_charge=fixedc, nunk_priv=len(unkp),
               allsmall=sum(1 for s in surv if all(v in (5, 6) for v in s)), all6=(tuple([6] * len(free)) in set(surv)),
               max_ball=max(tot) if tot else None, min_ball_no9=min([t for t, s in zip(tot, surv) if NEVER not in s], default=None),
               killers=used.most_common(6), nreq=len(R))
    if tot:
        mx = max(tot); res['argmax'] = [''.join('9' if v == NEVER else str(v) for v in s) for t, s in zip(tot, surv) if t == mx][:12]
        res['n_argmax'] = sum(1 for t in tot if t == mx)
        res['hist'] = sorted(collections.Counter(tot).items())
        res['private5_allowed'] = {''.join(map(str, f)): sorted({s[k] for s in surv}) for k, f in enumerate(free)}
    if dump: open(dump, 'w').write(''.join(''.join('9' if v == NEVER else str(v) for v in s) + '\n' for s in surv))
    return res
if __name__ == '__main__':
    rows = [a.split('/') for a in sys.argv[1:]]
    for lk, sv in rows:
        t0 = time.time(); r = census(len(lk), lk, sv, dump='surv2_%s_%s.txt' % (lk, sv)); r['sec'] = round(time.time() - t0, 1)
        print(json.dumps(r), flush=True)
