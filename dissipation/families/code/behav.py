"""Behavioural embedding of discharging parts.

For each receiver window (d, link word up to rotation+reflection) and each part,
the expected charge the part moves INTO the receiver (incoming from a neighbour
hub, minus outgoing when the receiver is the hub), with every unknown
second-ring degree uniform on {5,6,7,8,9+}. Semantics ported from the outside
team's verify_compact_4ct.py (Window2Ball, fit_part, build_ub_lb_terms):
a part with hub degree n moves weight w from its hub to slot 2.

usage: python3 behav.py RULES OUT.npz d [d ...] [--sample N] [--null SEED]
"""
import sys, itertools, random
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from parts import parse

FULL = (5, 9)


def npriv(letter):
    if letter == 5:
        return 0
    if letter >= 9:
        return 3
    return letter - 5


class W2B:
    def __init__(self, d, link):
        self.d = d
        self.link = list(link)
        self.rot_u = [1 + i for i in range(d)]
        self.rot_w = []
        r2 = []
        for i in range(d):
            k = npriv(self.link[i])
            s_prev = 1 + d + ((i - 1) % d)
            s_cur = 1 + d + i
            sg = [s_prev] + [1 + 2 * d + 3 * i + (j - 1) for j in range(1, k + 1)] + [s_cur]
            self.rot_w.append([0, 1 + ((i - 1) % d)] + sg + [1 + ((i + 1) % d)])
            r2.extend(sg[:-1])
        m = len(r2)
        self.r2prev = {r2[t]: r2[(t - 1) % m] for t in range(m)}
        self.r2next = {r2[t]: r2[(t + 1) % m] for t in range(m)}

    def deg_info(self, v):
        if v == -1:
            return ('open', 0)
        if v == 0:
            return ('dec', min(self.d, 9))
        if 1 <= v <= self.d:
            return ('dec', self.link[v - 1])
        if 1 + self.d <= v <= 2 * self.d:
            return ('var', 100 + (v - 1 - self.d))
        q = v - 1 - 2 * self.d
        i, j = q // 3, (q % 3) + 1
        return ('var', 200 + 3 * i + (j - 1))

    def succ(self, x, y):
        if x == -1:
            return -1
        if x == 0:
            idx = self.rot_u.index(y)
            return self.rot_u[(idx + 1) % self.d]
        if 1 <= x <= self.d:
            rw = self.rot_w[x - 1]
            idx = rw.index(y)
            return rw[(idx + 1) % len(rw)]
        prev = self.r2prev[x]
        nxt = self.r2next[x]
        if 1 + self.d <= x <= 2 * self.d:
            i = x - 1 - self.d
            w1, w0 = 1 + ((i + 1) % self.d), 1 + i
            if y == w1:
                return w0
            if y == w0:
                return prev
            if y == prev:
                return -1
            if y == nxt:
                return w1
            return -1
        q = x - 1 - 2 * self.d
        wi = 1 + (q // 3)
        if y == wi:
            return prev
        if y == prev:
            return -1
        if y == nxt:
            return wi
        return -1


def fit_part(W, h, subs, anchor):
    """Returns probability (uniform second ring) that the part fits, or 0."""
    S = W.rot_u if h == 0 else W.rot_w[h - 1]
    n = len(subs)
    if len(S) != n:
        return 0.0
    conds = {}

    def test_v(v, rng):
        if rng == FULL:
            return True
        kind, val = W.deg_info(v)
        if kind == 'dec':
            return rng[0] <= val <= rng[1]
        if kind == 'open':
            return True  # outside the 2-ball: counted as fitting (upper reading)
        lo, hi = conds.get(val, (5, 9))
        lo, hi = max(lo, rng[0]), min(hi, rng[1])
        if lo > hi:
            return False
        conds[val] = (lo, hi)
        return True

    for j in range(n):
        sp, hat, fans = subs[j]
        x = S[(anchor + j) % n]
        xp = S[(anchor + j - 1) % n]
        xn = S[(anchor + j + 1) % n]
        if not test_v(x, sp):
            return 0.0
        if hat != FULL and not test_v(W.succ(x, xp), hat):
            return 0.0
        if any(f != FULL for f in fans):
            if x == 0 or (1 <= x <= W.d):
                hv = W.succ(x, xp)
                hn = W.succ(xn, x)
                rr = W.rot_u if x == 0 else W.rot_w[x - 1]
                t = (rr.index(hv) + 1) % len(rr)
                fan_vs = []
                while rr[t] != hn:
                    fan_vs.append(rr[t])
                    t = (t + 1) % len(rr)
                    if len(fan_vs) > len(rr):
                        return 0.0
                if len(fan_vs) != len(fans):
                    return 0.0
                for fv, fr in zip(fan_vs, fans):
                    if not test_v(fv, fr):
                        return 0.0
    p = 1.0
    for lo, hi in conds.values():
        p *= (hi - lo + 1) / 5.0
    return p


def to3(slots):
    return [((s[0], s[1]), (s[2], s[3]), tuple(s[4])) for s in slots]


def canon_words(d):
    seen = set()
    out = []
    for w in itertools.product(range(5, 10), repeat=d):
        if w in seen:
            continue
        orb = set()
        for r in range(d):
            x = w[r:] + w[:r]
            orb.add(x)
            orb.add(tuple(reversed(x)))
        seen |= orb
        out.append((min(orb), len(orb)))
    return out


def sample_words(d, n, rng):
    out = {}
    while len(out) < n:
        w = tuple(rng.choice(range(5, 10)) for _ in range(d))
        orb = set()
        for r in range(d):
            x = w[r:] + w[:r]
            orb.add(x)
            orb.add(tuple(reversed(x)))
        out[min(orb)] = len(orb)
    return sorted(out.items())


def evaluate(parts, words, d):
    """matrix [n_words, n_parts] of expected net charge into receiver."""
    byhub = {}
    for k, p in enumerate(parts):
        byhub.setdefault(p['hub'], []).append(k)
    M = np.zeros((len(words), len(parts)), np.float32)
    S3 = [to3(p['slots']) for p in parts]
    for wi, (w, _) in enumerate(words):
        W = W2B(d, w)
        if 5 <= d <= 8:
            for k in byhub.get(d, []):
                p = parts[k]
                sp = [s[0:2] for s in p['slots']]
                for a in range(d):
                    if any(not (sp[j][0] <= w[(a + j) % d] <= sp[j][1]) for j in range(d)):
                        continue
                    pr = fit_part(W, 0, S3[k], a)
                    if pr:
                        M[wi, k] -= p['w'] * pr
        dd = min(d, 9)
        for i in range(d):
            L = w[i]
            if L > 8:
                continue
            for k in byhub.get(L, []):
                p = parts[k]
                s = p['slots']
                if not (s[2][0] <= dd <= s[2][1]):
                    continue
                if not (s[3 % L][0] <= w[(i - 1) % d] <= s[3 % L][1]):
                    continue
                if not (s[1][0] <= w[(i + 1) % d] <= s[1][1]):
                    continue
                pr = fit_part(W, 1 + i, S3[k], L - 2)
                if pr:
                    M[wi, k] += p['w'] * pr
    return M


def null_parts(P, seed):
    import collections as C
    rng = random.Random(seed)
    pos = C.defaultdict(list)
    for p in P:
        for r, s in enumerate(p['slots']):
            pos[(p['pre'], p['hub'], r)].append(s)
    from mir import mirror
    key = lambda p: (p['pre'], p['hub'], p['w'], p['slots'])
    idx = {}
    for k, p in enumerate(P):
        idx.setdefault(key(p), []).append(k)
    out = [None] * len(P)
    for k, p in enumerate(P):
        if out[k] is not None:
            continue
        q = dict(p, slots=tuple(p['slots'][r] if r == 2 else rng.choice(pos[(p['pre'], p['hub'], r)])
                                for r in range(p['hub'])))
        out[k] = q
        mk = [j for j in idx[(p['pre'], p['hub'], p['w'], mirror(p, 2, 1, 'with_spoke'))] if out[j] is None]
        if mk:
            out[mk[0]] = dict(P[mk[0]], slots=mirror(q, 2, 1, 'with_spoke'))
    return out


if __name__ == '__main__':
    rules, outf = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    sample = None
    seed = None
    if '--sample' in args:
        i = args.index('--sample'); sample = int(args[i + 1]); args = args[:i] + args[i + 2:]
    if '--null' in args:
        i = args.index('--null'); seed = int(args[i + 1]); args = args[:i] + args[i + 2:]
    sc, P = parse(rules)
    if seed is not None:
        P = null_parts(P, seed)
    res = {}
    for d in map(int, args):
        words = sample_words(d, sample, random.Random(d)) if sample else canon_words(d)
        M = evaluate(P, words, d)
        res[f'M{d}'] = M
        res[f'W{d}'] = np.array([w for w, _ in words], np.int8)
        res[f'O{d}'] = np.array([o for _, o in words], np.int32)
        print(d, len(words), 'nonzero', int((M != 0).sum()), flush=True)
    np.savez_compressed(outf, tags=np.array([p['tag'] for p in P]), **res)
