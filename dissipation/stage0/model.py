"""Stage 0: integer attention over the spokes of a hub. Who receives the forwarded units?
Features are bits (packed into Python ints / uint64 words), weights are integers, training is an
averaged structured perceptron (add/subtract only). Units of 3/60. No ML framework.
usage: python3 model.py DATA.pkl [--prune]"""
import sys, pickle, random, collections as C, numpy as np
sys.path.insert(0, '../code')
from behav import npriv

NAMES = []
def F(name):
    NAMES.append(name); return len(NAMES) - 1
VAL = [5, 6, 7, 8, 9]
B_SELF = {v: F(f'receiver is {v}{"+" if v == 9 else ""}') for v in VAL}
B_HUB8 = F('hub is 8')
B_N1 = {(v, k): F(f'ring neighbour of receiver is {v}{"+" if v==9 else ""}: {k}') for v in VAL for k in ('one', 'both')}
B_N2 = {(v, k): F(f'second ring neighbour is {v}{"+" if v==9 else ""}: {k}') for v in VAL for k in ('one', 'both')}
B_HAT = {(v, k): F(f'hat beside receiver is {v}{"+" if v==9 else ""}: {k}') for v in VAL for k in ('one', 'both')}
B_F5 = {k: F(f'receiver has {k} fans of degree 5') for k in (1, 2, 3)}
B_FB = {k: F(f'receiver has {k} fans of degree 7+') for k in (1, 2, 3)}
B_SL = {t: F(f'receiver charge after RSST below {t}') for t in (0, -12, -24, -36, -48, -60)}
B_SLU = F('receiver charge unknown (9+)')
B_OPP = F('receiver is opposite the most 5s side')  # filled below: hub ring distance to nearest 5 is >= 2
B_N5 = {k: F(f'hub has {k} neighbours of degree 5') for k in (0, 1, 2, 3, 4)}
B_SECOND = F('second unit to the same receiver')
NF = len(NAMES)

def sym(d, a, b, table):
    out = 0
    for v in VAL:
        n = (a == v) + (b == v)
        if n >= 1: out |= 1 << table[(v, 'one')]
        if n == 2: out |= 1 << table[(v, 'both')]
    return out
def feats(r):
    """bit mask per spoke."""
    d, link, asg = r['d'], r['link'], r['asg']; n5 = sum(1 for x in link if x == 5); out = []
    for i in range(d):
        m = 1 << B_SELF[link[i]]
        if d == 8: m |= 1 << B_HUB8
        m |= sym(d, link[(i - 1) % d], link[(i + 1) % d], B_N1)
        m |= sym(d, link[(i - 2) % d], link[(i + 2) % d], B_N2)
        m |= sym(d, asg[100 + (i - 1) % d], asg[100 + i], B_HAT)
        fans = [asg[200 + 3 * i + j] for j in range(npriv(link[i]))]
        k5 = sum(1 for f in fans if f == 5); kb = sum(1 for f in fans if f >= 7)
        if k5: m |= 1 << B_F5[k5]
        if kb: m |= 1 << B_FB[kb]
        e = r['et'][i]
        if e is None: m |= 1 << B_SLU
        else:
            for t in B_SL:
                if e < t: m |= 1 << B_SL[t]
        if link[(i - 1) % d] != 5 and link[(i + 1) % d] != 5: m |= 1 << B_OPP
        m |= 1 << B_N5[min(n5, 4)]
        out.append(m)
    return out
def bits(m):
    while m:
        b = m & -m; yield b.bit_length() - 1; m ^= b
def score(w, m, keep):
    m &= keep; s = 0
    while m:
        b = m & -m; s += w[b.bit_length() - 1]; m ^= b
    return s
def allocate(w, fs, units, keep):
    """greedy: each unit goes to the best spoke; a second unit to the same spoke pays the SECOND weight."""
    d = len(fs); base = [score(w, m, keep) for m in fs]; got = [0] * d
    for u in range(units):
        best = max(range(d), key=lambda i: (base[i] + (w[B_SECOND] if got[i] and (keep >> B_SECOND) & 1 else 0) * got[i], -i))
        got[best] += 1
    return got
def phi(fs, got):
    v = C.Counter()
    for i, g in enumerate(got):
        if not g: continue
        for b in bits(fs[i]): v[b] += g
        if g > 1: v[B_SECOND] += g * (g - 1) // 2
    return v
def prep(rows):
    X = []
    for r in rows:
        tot = sum(r['spo'])
        if tot <= 0 or tot % 3 or any(x % 3 for x in r['spo']): continue
        X.append((r['tag'].rstrip('m'), feats(r), [x // 3 for x in r['spo']], r))
    return X
def train(X, keep, epochs=30, seed=0):
    w = [0] * NF; acc = [0] * NF; rng = random.Random(seed); n = 0
    for ep in range(epochs):
        rng.shuffle(X)
        for _, fs, y, _r in X:
            p = allocate(w, fs, sum(y), keep)
            if p != y:
                a, b = phi(fs, y), phi(fs, p)
                for k in set(a) | set(b):
                    if (keep >> k) & 1: w[k] += a[k] - b[k]
            n += 1
            for k in range(NF): acc[k] += w[k]
    # averaged weights, rounded to integers on a common scale (keep 6 bits of mantissa)
    mx = max(abs(a) for a in acc) or 1
    return [int(round(63 * a / mx)) for a in acc]
def evalu(w, X, keep):
    ok = 0
    for _, fs, y, _r in X:
        ok += allocate(w, fs, sum(y), keep) == y
    return ok / max(1, len(X))
def folds(X, k=5):
    fam = sorted({x[0] for x in X}); random.Random(1).shuffle(fam); f = {t: i % k for i, t in enumerate(fam)}
    for j in range(k):
        yield [x for x in X if f[x[0]] != j], [x for x in X if f[x[0]] == j]
def cv(X, keep):
    return float(np.mean([evalu(train(list(tr), keep), te, keep) for tr, te in folds(X)]))
def baseline(X):
    """most slack takes everything; and most slack two share."""
    a = b = 0
    for _, fs, y, r in X:
        d = r['d']; sl = [(r['et'][i] if r['et'][i] is not None else -999) if r['link'][i] >= 7 else 999 for i in range(d)]
        o = sorted(range(d), key=lambda i: sl[i]); u = sum(y)
        g = [0] * d; g[o[0]] = u; a += g == y
        g = [0] * d
        for t in range(u): g[o[t % 2]] += 1
        b += g == y
    return a / len(X), b / len(X)
if __name__ == '__main__':
    rows = pickle.load(open(sys.argv[1], 'rb')); X = prep(rows)
    ALL = (1 << NF) - 1
    print(sys.argv[1], 'balls', len(rows), 'usable', len(X), 'families', len({x[0] for x in X}), 'features', NF)
    print(' units:', sorted(C.Counter(sum(x[2]) for x in X).items()), ' shapes:', C.Counter(tuple(sorted(v for v in x[2] if v)) for x in X).most_common(5))
    print(' baseline most-slack-all %.3f  most-slack-two %.3f' % baseline(X))
    print(' held-out exact match, all features: %.3f' % cv(X, ALL))
    if '--prune' in sys.argv:
        keep = ALL; w = train(list(X), keep); hist = []
        while bin(keep).count('1') > 1:
            # drop the live feature with the smallest rounded weight (never the SECOND bit first)
            live = [k for k in range(NF) if (keep >> k) & 1]
            k = min(live, key=lambda k: (abs(w[k]), k)); keep &= ~(1 << k)
            w = train(list(X), keep, epochs=15); n = bin(keep).count('1')
            if n in (40, 30, 24, 20, 16, 12, 10, 8, 6, 4, 3, 2, 1):
                a = cv(X, keep); hist.append((n, a)); print('  features %2d  held-out %.3f' % (n, a), flush=True)
                if n in (12, 8):
                    for k2 in sorted(live, key=lambda k: -abs(w[k])):
                        if (keep >> k2) & 1: print('      %+3d  %s' % (w[k2], NAMES[k2]))
