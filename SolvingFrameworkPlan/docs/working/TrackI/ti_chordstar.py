#!/usr/bin/env python3
"""Track I: identity (*) and rigid isolation in the planar chord model (TrackH model, independent code in ti_lib).
For every DL instance with N <= NMAX cubic vertices:
   (*) kH + k12 + kHX + k12X + [pHX == (e1e4)(e2e3)] == 0 (mod 2),   X = F13-trail through e1,e3;
and for rigid instances the image type (kHX, k12X, pHX).
usage: ti_chordstar.py NMAX"""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ti_lib import chord_instances, analyse
for N in range(3, int(sys.argv[1]) + 1, 2):
    st = Counter()
    for E, meta in chord_instances(N):
        r = analyse(E)
        if r is None: continue
        kH, k12, k13 = r['k']
        star = (kH + k12 + r['kHX'] + r['kF12X'] + (1 if r['img_dl'] else 0)) % 2
        st['DL'] += 1; st['star_fail'] += star
        if r['rigid']:
            st['rigid'] += 1; st['rigid_to_rigid'] += r['img_rigid']
            st[('rigid_img', r['kHX'], r['kF12X'], 'DL' if r['img_dl'] else 'nDL')] += 1
    print('N', N, dict(sorted(st.items(), key=str)), flush=True)
