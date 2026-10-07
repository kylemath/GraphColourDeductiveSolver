#!/usr/bin/env python3
"""w2trace.py (NightW2): ranks of the three pair-graphs avoiding colour 1 (= alpha at every state of positions 4..8) along positions 4..8 of each period,
from Job AH (jobuv/jobah.json). Colours named at R3k2: alpha=1, mu=2, A=3, B=4. Frame pairs by position:
 pos4 R3k2 (mu,A,B)=(2,3,4); pos5 R1k4 (4,2,3); pos6 R3k1 (3,4,2); pos7 R1k3 (2,3,4); pos8 R3k0 (4,2,3).  Single core, < 1 s."""
import json, ast
from collections import Counter
d = json.load(open('../jobuv/jobah.json'))
FR = {4: (2, 3, 4), 5: (4, 2, 3), 6: (3, 4, 2), 7: (2, 3, 4), 8: (4, 2, 3)}
def ranks(row, pos):
    mu, A, B = FR[pos]; return {frozenset((A, B)): row['AB'], frozenset((mu, A)): row['muA'], frozenset((mu, B)): row['muB']}
P34, P24, P23 = frozenset((3, 4)), frozenset((2, 4)), frozenset((2, 3))
tr = {P34: Counter(), P24: Counter(), P23: Counter()}; tot = Counter(); n = 0; chk = Counter(); fixedtrace = Counter(); w2s = Counter()
for r in d:
    if r['deg'] != 6: continue
    rows = r['rows'] if isinstance(r['rows'], list) else ast.literal_eval(r['rows']); L = len(rows)
    s0 = next(i for i, x in enumerate(rows) if x['ty'] == 3 and x['k'] == 4); rows = rows[s0:] + rows[:s0]
    for b in range(0, L, 10):
        per = rows[b:b + 10]; n += 1
        assert [(per[i]['ty'], per[i]['k']) for i in range(4, 9)] == [(3, 2), (1, 4), (3, 1), (1, 3), (3, 0)]
        R = {pos: ranks(per[pos], pos) for pos in range(4, 9)}
        for P in tr: tr[P][tuple(min(R[pos][P], 3) for pos in range(4, 9))] += 1
        tot[tuple(sum(R[pos].values()) for pos in range(4, 9))] += 1
        chk[(per[4]['fixed'] == (R[4][P34] == 0), per[6]['fixed'] == (R[6][P24] == 0), per[8]['fixed'] == (R[8][P23] == 0))] += 1
        if R[4][P34] == 0: fixedtrace[('F4: {2,3} ranks pos4..8', tuple(R[pos][P23] for pos in range(4, 9)))] += 1
        if R[8][P23] == 0: fixedtrace[('F8: {3,4} ranks pos4..8', tuple(R[pos][P34] for pos in range(4, 9)))] += 1
        w2s[(R[4][P34] + R[8][P23] >= 1)] += 1
print('deg-6 periods', n, ' Lemma Fix consistency (fixed <-> own-pair rank 0) at pos 4,6,8:', dict(chk))
print('W2* (rank34@4 + rank23@8 >= 1):', dict(w2s))
for P, nm in ((P34, '{3,4} (F4 pair)'), (P24, '{2,4} (F6 pair)'), (P23, '{2,3} (F8 pair)')):
    print('rank of', nm, 'at pos 4,5,6,7,8 (capped 3):'); [print('   ', v, k) for k, v in tr[P].most_common()]
print('sum of the three ranks at pos 4..8:'); [print('   ', v, k) for k, v in tot.most_common(15)]
print('traces at fixed points:'); [print('   ', v, k) for k, v in sorted(fixedtrace.items())]
