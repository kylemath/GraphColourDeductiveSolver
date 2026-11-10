# W6b round 14b: an independent reference for key coefficients, written from the TEXT of KEYSPEC section 5, DUAL_EXPORT
# (gkwin) and PAYER8SPEC.md, with Python sets of letters (no grammar.match, no edge_vec, no slot tables, no win_vecs).
# coef(row, key) = the key's integer coefficient in the row: receiver / cons2 IN - OUT, sender OUT - IN; IN counts slots that
# POSSIBLY match, OUT slots that SURELY match; every oriented pair with both chiralities.
# A row is given as a dict:
#   window receiver (d >= 8): {'kind': 'W', 'd', 'w', 's'} (exact letters 5..9, 9 = 9+), privates from the gkwin window rule;
#   picture row: {'kind': 'S' | 'C' | 'R', 'd', 'w', 's': apex letter sets, 'priv': [ [set, ...] per link vertex ], 'c': centre}
#     (privates ordered from the s_{j-1} side to the s_j side, as grammar.build), built by the caller from the engine's masks.
# A key: (U set of payer letters, V set of payee letters, {position name: letter set}); unlisted positions = all letters.
import itertools
LET = (5, 6, 7, 8, 9); ALLS = frozenset(LET)
def letters(m): return frozenset(l for l in LET if m >> (l - 5) & 1)
def sure(pos, key):
    return all(pos[p] <= key[2].get(p, ALLS) for p in pos)
def poss(pos, key):
    return all(pos[p] & key[2].get(p, ALLS) for p in pos)
def mirror(pos):
    sw = {'S.L+1': 'S.L-1', 'S.L+2': 'S.L-2', 'S.L+3': 'S.L-3', 'S.A+1': 'S.A-1', 'R.L+2': 'R.L-2'}
    sw.update({b: a for a, b in list(sw.items())})
    return {sw[p]: v for p, v in pos.items()}

def window_slots(d, w, s, pmask, mode='W5'):
    """(role, payer letter, payee letter, positions) of a d >= 8 window row, text of DUAL_EXPORT (IN) and PAYER8SPEC (OUT)"""
    n = d; U = min(d, 9); out = []
    W = lambda k: w[k % n]; S = lambda k: s[k % n]
    one = lambda x: frozenset([x])
    def am(k, outside=()):   # amask of link 6 at k: pmask(U, w_{k-2}, w_{k-1}, w_{k+1}, w_{k+2}, s_{k-2}, s_{k-1}, s_k, s_{k+1})
        args = [W(k - 2), W(k - 1), W(k + 1), W(k + 2), S(k - 2), S(k - 1), S(k), S(k + 1)]
        r = set()
        for sub in itertools.product(*[LET if i in outside else (args[i],) for i in range(8)]): r |= letters(pmask(U, *sub))
        return frozenset(r)
    # IN: payer w_j -> centre; chirality +1 has S.L+1 = w_{j-1}
    for j in range(n):
        x = W(j)
        p = {'S.L+1': one(W(j - 1)), 'S.L-1': one(W(j + 1)), 'S.L+2': one(S(j - 1)), 'S.L-2': one(S(j)),
             'R.L+2': one(W(j - 2)), 'R.L-2': one(W(j + 2))}
        if x == 5: p['S.L+3'] = one(S(j)); p['S.L-3'] = one(S(j - 1))
        elif x == 6: p['S.L+3'] = p['S.L-3'] = am(j)
        else: p['S.L+3'] = p['S.L-3'] = ALLS                 # payer 7, 8, 9+: own privates unknown
        # S.A+1: w_{j-1}'s private next to s_{j-1}; S.A-1: w_{j+1}'s private next to s_j
        y = W(j - 1)
        p['S.A+1'] = one(S(j - 2)) if y == 5 else am(j - 1, outside=(0, 4)) if y == 6 else ALLS   # w_{j-3}, s_{j-3} outside
        y = W(j + 1)
        p['S.A-1'] = one(S(j + 1)) if y == 5 else am(j + 1, outside=(3, 7)) if y == 6 else ALLS   # w_{j+3}, s_{j+2} outside
        out.append(('in', x, U, p)); out.append(('in', x, U, mirror(p)))
    # OUT: centre (letter U) -> w_i; chirality +1 has S.L+1 = w_{i+1}
    for i in range(n):
        p = {'S.L+1': one(W(i + 1)), 'S.L+2': one(W(i + 2)), 'S.L-1': one(W(i - 1)), 'S.L-2': one(W(i - 2)),
             'S.A+1': one(S(i + 1)), 'S.A-1': one(S(i - 2)), 'R.L+2': one(S(i)), 'R.L-2': one(S(i - 1))}
        if mode == 'W7': p['S.L+3'] = one(W(i + 3)); p['S.L-3'] = one(W(i - 3))
        else: p['S.L+3'] = p['S.L-3'] = ALLS
        out.append(('out', U, W(i), p)); out.append(('out', U, W(i), mirror(p)))
    return out

def picture_in_slots(row):
    """IN slots (link payer w_j -> centre) of a picture row (sender / cons2 / d = 7 receiver), KEYSPEC section 5 IN formula"""
    d, w, s, priv = row['d'], row['w'], row['s'], row['priv']; n = d; out = []
    W = lambda k: w[k % n]; S = lambda k: s[k % n]; PV = lambda k: priv[k % n]
    one = lambda x: frozenset([x])
    for j in range(n):
        x = W(j)
        p = {'S.L+1': one(W(j - 1)), 'S.L-1': one(W(j + 1)), 'S.L+2': S(j - 1), 'S.L-2': S(j), 'R.L+2': one(W(j - 2)), 'R.L-2': one(W(j + 2))}
        if x == 5: p['S.L+3'] = S(j); p['S.L-3'] = S(j - 1)
        else: p['S.L+3'] = PV(j)[0]; p['S.L-3'] = PV(j)[-1]   # private next to s_{j-1} / next to s_j (a 6: the same one)
        p['S.A+1'] = S(j - 2) if W(j - 1) == 5 else PV(j - 1)[-1]   # w_{j-1}'s private next to s_{j-1}
        p['S.A-1'] = S(j + 1) if W(j + 1) == 5 else PV(j + 1)[0]    # w_{j+1}'s private next to s_j
        out.append(('in', x, row['c'], p)); out.append(('in', x, row['c'], mirror(p)))
    return out

def picture_out_slots(row):
    """OUT slots (centre -> link w_i) of a picture row, KEYSPEC section 5 OUT formula (indices mod d)"""
    d, w, s = row['d'], row['w'], row['s']; n = d; out = []
    W = lambda k: frozenset([w[k % n]]); S = lambda k: s[k % n]
    for i in range(n):
        p = {'S.L+1': W(i + 1), 'S.L+2': W(i + 2), 'S.L+3': W(i + 3), 'S.L-1': W(i - 1), 'S.L-2': W(i - 2), 'S.L-3': W(i - 3),
             'S.A+1': S(i + 1), 'S.A-1': S(i - 2), 'R.L+2': S(i), 'R.L-2': S(i - 1)}
        out.append(('out', row['c'], w[i], p)); out.append(('out', row['c'], w[i], mirror(p)))
    return out

def coef(slots, key, kind):
    """kind 'S' (sender: OUT - IN) or other (IN - OUT)"""
    U, V = key[0], key[1]; c = 0
    for role, a, b, p in slots:
        if role == 'out':
            if a in U and b in V and sure(p, key): c += 1 if kind == 'S' else -1
        else:
            if a in U and b in V and poss(p, key): c += -1 if kind == 'S' else 1
    return c
