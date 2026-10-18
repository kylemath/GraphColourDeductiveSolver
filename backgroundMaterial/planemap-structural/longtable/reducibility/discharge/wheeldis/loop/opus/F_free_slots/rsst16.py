"""RSST 633 in each free filling of the binder (B's rsst_rows.py, relaxed mode = every exact slot may host interior).
9 is run as exact 9 (a superset of what >= 9 allows), so 'free' at 9 implies free at 9+."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'B_rsst_rows'))
import rsst_rows as R
w = [int(c) for c in '5675765']; s0 = [int(c) for c in '6577575']
for a in range(6, 10):
    for b in range(6, 10):
        s = list(s0); s[1], s[4] = a, b
        h = R.hits(7, w, s, 'relaxed')
        print('s1=%d s4=%d: %s' % (a, b, ' '.join(R.P[i]['name'] for i in h) or 'RSST-free'), flush=True)
