#!/usr/bin/env python3
"""routeb/regress_kred.py -- kred.py must reproduce Math's published 2-ball table (MathVacancyDRed README sec.3 and REFINEMENT sec.3)."""
import kred
EXPECT = {  # degrees: (vdred lost or depth, joint lost or depth); ('d', k) = reducible with depth k, ('l', k) = k states lost
    (5,5,5,5,5): (('d', 3), ('d', 3)), (5,5,5,5,6): (('d', 6), ('d', 6)), (5,5,5,6,6): (('d', 7), ('d', 7)), (5,5,6,5,6): (('l', 28), ('d', 14)),
    (5,5,6,6,6): (('l', 59), ('l', 56)), (5,6,5,6,6): (('l', 56), ('l', 48)), (5,6,6,6,6): (('l', 135), ('l', 135)), (6,6,6,6,6): (('l', 370), ('l', 370))}
bad = 0
for ds, exp in EXPECT.items():
    f, v = kred.ball_from_degrees(ds)
    for mode, e in zip(('vdred', 'joint'), exp):
        r = kred.Game(kred.Config(f, v), mode).solve()
        got = ('d', r['depth']) if r['reducible'] else ('l', r['lost'])
        ok = got == e; bad += not ok
        print(ds, mode, got, 'OK' if ok else 'MISMATCH, expected %s' % (e,), flush=True)
# extra: Math's joint (6^5) decision-node count and T4 vdred histogram
f, v = kred.ball_from_degrees((6,6,6,6,6)); r = kred.Game(kred.Config(f, v), 'joint').solve()
bad += r['decision_nodes'] != 18870; print('(6^5) joint decision nodes', r['decision_nodes'], 'expected 18870')
f, v = kred.ball_from_degrees((5,5,5,6,6)); r = kred.Game(kred.Config(f, v), 'vdred').solve()
bad += r['hist'] != {1: 46, 2: 23, 3: 7, 4: 8, 5: 4, 6: 4, 7: 2}; print('T4 vdred hist', r['hist'])
print('regression passed' if bad == 0 else 'REGRESSION FAILED (%d)' % bad)
