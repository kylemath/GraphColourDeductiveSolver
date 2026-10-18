"""G_ruleT_lp: count rule-T (sender-2-ball) variables and sender rows (exploratory, counts only, no LP)."""
import os, sys, itertools
WD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
src = open(os.path.join(WD, 'wlp.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(WD, 'wlp.py')))
sys.argv = ['wlp']; exec(src[:src.index('# ---- option bigw')])
def zopts(o):  # o = (B,a,b,c,e) oriented at big root; z letters for side a / side e (None if spoke not 6)
    return ([None] if o[1] != 6 else list(L)), ([None] if o[4] != 6 else list(L))
def key(o, za, ze):
    r = (o[0], o[4], o[3], o[2], o[1]); return min((tuple(o), za, ze), (r, ze, za))
Y, T, rows, rows_flag = set(), set(), 0, 0
for w in senders:
    x = list(w); bigs = [j for j in range(5) if x[j] >= 7]
    # free z slots: for each 6 at position k, its wheel (5, x[k+1], zR, q, zL, x[k-1]); zL used by root k-1 (side a), zR by root k+1 (side e)
    sixes = [k for k in range(5) if x[k] == 6]
    per6 = []
    for k in sixes:
        ok = [(zR, zL) for zR in L for q in L for zL in L if not isR6([5, x[(k + 1) % 5], zR, q, zL, x[(k - 1) % 5]])]
        per6.append(sorted(set(ok)))
    combos = 1
    for k, ok in zip(sixes, per6):
        relevant = (x[(k - 1) % 5] >= 7) or (x[(k + 1) % 5] >= 7)
        if relevant:
            proj = set((zR if x[(k + 1) % 5] >= 7 else 0, zL if x[(k - 1) % 5] >= 7 else 0) for zR, zL in ok)
            combos *= len(proj)
    rows += combos
    for j in bigs:
        o = tuple(x[(j + k) % 5] for k in range(5))
        A, E = zopts(o)
        for za in A:
            for ze in E:
                Y.add(key(o, za, ze))
                if za is not None and za >= 7: T.add(key(o, za, ze) + ('a',))
                if ze is not None and ze >= 7: T.add(key(o, za, ze) + ('e',))
T2 = set()  # canonical T: side a under reflection becomes side e
for (o, za, ze, sd) in T:
    r = (o[0], o[4], o[3], o[2], o[1]); T2.add(min((o, za, ze, sd), (r, ze, za, 'e' if sd == 'a' else 'a')))
print('non-R sender words', len(senders), ' base rooted y vars', len(roots))
print('rule-T Y vars (rooted word + own z letters)', len(Y), ' T vars', len(T2))
print('roots with a 6 spoke next to the root', sum(1 for r in roots if 6 in (r[1], r[4])))
print('sender rows (z-letter assignments consistent with non-R 6-wheels)', rows, ' (base', len(senders), ')')
