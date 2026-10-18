"""Compare kc output with dfast lines field by field (classes, ext, reached, D, depth).  Usage: python3 cmp.py KC_OUT DFAST_LINES"""
import sys
def f(l):
    d = {}
    for tok in l.split()[1:]:
        if '=' in tok: k, v = tok.split('=', 1); d[k] = v
    return l.split()[0], d
A = dict(f(l) for l in open(sys.argv[1]) if ' r=' in l); B = dict(f(l) for l in open(sys.argv[2]) if ' r=' in l)
bad = 0; dmis = 0; n = 0
for nm, b in B.items():
    if nm not in A: print('MISSING', nm); bad += 1; continue
    a = A[nm]; n += 1
    for k in ('r', 'classes', 'ext', 'reached', 'D'):
        if a.get(k) != b.get(k): print('MISMATCH', nm, k, 'kc', a.get(k), 'dfast', b.get(k)); bad += 1
    if a.get('depth') != b.get('depth'): dmis += 1
print('# compared %d keys: %d field mismatches (classes/ext/reached/D); depth differs on %d' % (n, bad, dmis))
