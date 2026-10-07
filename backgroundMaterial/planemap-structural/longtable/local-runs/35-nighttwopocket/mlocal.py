#!/usr/bin/env python3
"""[exploratory] NightTwoPocket: the local m-neighbourhood automaton.
deg(m) = 5: m's neighbours in rotation are p, z, u1, u2, y (u1 ~ z, u2 ~ y, u1 ~ u2). Colours in the common (pulled-back) frame of NightA34Two §1.
One period G = rho^-1 pi^10 from position 9 to position 9: step 9 (pair {0,2}, component Pi contains p, m), relabel rho^-1 (1->2, 2->3, 3->1),
then steps 0..8 of the table. For each step: pair, which of p, m, y, z lie in K (pair_own / Job O). A neighbour u of a hole vertex v with c(v) in the
pair lies in K iff v does (K is a component). u1 ~ u2 propagates. Anything not forced is a free branch. Output: the transition relation on the
position-9 states (u1, u2) with the branch labels, and which branches each transition uses."""
import itertools, json, sys
# hole colours at each position (p, z, y, m) and step (pair, members among p,m,y,z) -- NightA34 §1.1
POS = {0: (3, 2, 1, 0), 1: (3, 2, 1, 0), 2: (3, 2, 1, 0), 3: (0, 2, 1, 3), 4: (0, 2, 1, 3), 5: (1, 2, 0, 3), 6: (1, 2, 3, 0),
       7: (1, 0, 3, 2), 8: (0, 1, 3, 2), 9: (0, 1, 3, 2)}
STEP = {9: ((0, 2), {'p', 'm'}), 0: ((0, 2), set()), 1: ((0, 1), set()), 2: ((0, 3), {'p', 'm'}), 3: ((0, 2), set()), 4: ((0, 1), {'p', 'y'}),
        5: ((0, 3), {'m', 'y'}), 6: ((0, 2), {'m', 'z'}), 7: ((0, 1), {'p', 'z'}), 8: ((0, 3), set())}
RHOINV = {0: 0, 1: 2, 2: 3, 3: 1}
NB = {'u1': ('m', 'z'), 'u2': ('m', 'y')}
def hole(pos):
    p, z, y, m = POS[pos]; return dict(p=p, z=z, y=y, m=m)
def ok(pos, s):
    H = hole(pos); u1, u2 = s
    return u1 != u2 and all(u1 != H[v] for v in NB['u1']) and all(u2 != H[v] for v in NB['u2'])
def step(pos, s):
    """all possible successors of state s=(u1,u2) under the swap at position pos; returns list of (s', label)"""
    (a, b), mem = STEP[pos]; H = hole(pos); us = dict(u1=s[0], u2=s[1]); out = []
    status = {}
    for u in ('u1', 'u2'):
        if us[u] not in (a, b): status[u] = 'out'; continue
        nb = [v for v in NB[u] if H[v] in (a, b)]
        if any(v in mem for v in nb): status[u] = 'in'
        elif nb: status[u] = 'out'          # adjacent to a pair-coloured hole vertex outside K
        else: status[u] = '?'
    # propagate along u1 ~ u2
    for _ in range(2):
        for u, w in (('u1', 'u2'), ('u2', 'u1')):
            if us[u] in (a, b) and us[w] in (a, b):
                if status[u] == 'in': status[w] = 'in' if status[w] != 'out' else 'CONTRA'
                if status[u] == 'out' and status[w] == 'in': status[u] = 'CONTRA'
    if 'CONTRA' in status.values(): return []
    free = [u for u in ('u1', 'u2') if status[u] == '?']
    for choice in itertools.product([False, True], repeat=len(free)):
        inK = {u: status[u] == 'in' for u in us}; inK.update(dict(zip(free, choice)))
        # adjacent pair-coloured u1, u2 must agree
        if us['u1'] in (a, b) and us['u2'] in (a, b) and inK['u1'] != inK['u2']: continue
        sw = lambda c: b if c == a else a if c == b else c
        t = tuple(sw(us[u]) if inK[u] else us[u] for u in ('u1', 'u2'))
        lab = ','.join('%s%s' % (u, '+' if inK[u] else '-') for u in free)
        out.append((t, lab))
    return out
def period(s9):
    """all runs from a position-9 state to the next position-9 state (pulled back); returns list of (end, path)"""
    runs = []
    for t, lab in step(9, s9):
        t = tuple(RHOINV[c] for c in t)
        runs.append((t, [('9', s9, lab)]))
    for pos in range(0, 9):
        new = []
        for s, path in runs:
            if not ok(pos, s): continue
            for t, lab in step(pos, s): new.append((t, path + [(str(pos), s, lab)]))
        runs = new
    return [(s, p) for s, p in runs if ok(9, s)]
if __name__ == '__main__':
    S9 = [s for s in itertools.product(range(4), repeat=2) if ok(9, s)]
    print('position-9 states (u1,u2):', S9, ' pocket-pair {0,2}; P = {m} iff neither is 0')
    rel = {}
    for s in S9:
        for e, path in period(s):
            free = [(p, l) for p, _, l in path if l]
            rel.setdefault((s, e), []).append(free)
    for (s, e), fs in sorted(rel.items()):
        print('  %s -> %s : %s' % (s, e, ' | '.join(' '.join('step%s[%s]' % f for f in fr) or 'forced' for fr in fs)))
    json.dump({'%s->%s' % k: v for k, v in rel.items()}, open('mlocal-relation.json', 'w'))
