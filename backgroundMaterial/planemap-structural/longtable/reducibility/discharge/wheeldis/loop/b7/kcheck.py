"""EXPLORE round 10 (exploratory): defect_check2 (bf) with a kill log.  For every candidate, lists the D kills (receiver-
centred 'D' and B-fixed 'bfD') with the 7 they sit at: 'centre' when it is the defect's centre u (vertex 0), plus the
centre's arrangement and S, so a centre kill can be turned into an f7_ pattern.
Usage: python3 kcheck.py CANDIDATES OUT"""
import sys, os
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAND, OUT = sys.argv[1], sys.argv[2]
src = open(os.path.join(W, 'defect_check2.py')).read()
src = src[:src.index("if __name__ == '__main__':")]
src = src.replace("                        if db == 'D': st['bfD'] += 1",
                  "                        if db == 'D': st['bfD'] += 1; KILLS.append((u == 0, 'bfD', kb, S, L_, S_, int(cb.split()[0]), Ib2 != Ib if 'Ib2' in dir() else None))")
src = src.replace("                if dv == 'D': st['D'] += 1",
                  "                if dv == 'D': st['D'] += 1; KILLS.append((u == 0, 'D', nm, S, L_, S_, r, None))")
assert src.count('KILLS.append') == 2
sys.argv = ['defect_check2.py', CAND, '/dev/null', 'bf']; KILLS = []
G = {'__file__': os.path.join(W, 'defect_check2.py'), '__name__': 'dc2', 'KILLS': KILLS}
exec(src, G); check = G['check']
import re
out = []
for line in open(CAND):
    m = re.search(r'c=(-?\d+) sig=(\S+)', line)
    if not m: continue
    KILLS.clear(); v, st, need = check(m.group(2))
    cen = [k for k in KILLS if k[0]]
    out.append('%s %s centreD=%d otherD=%d %s' % (v, m.group(2), len(cen), len(KILLS) - len(cen),
               ' '.join('%s:%s:S=%s:%s/%s:r%d' % (k[1], k[2], ','.join(map(str, k[3])), k[4], k[5], k[6]) for k in cen)))
open(OUT, 'w').write('\n'.join(out) + '\n')
import collections
print(collections.Counter((o.split()[0], 'centre' if 'centreD=0' not in o else 'other only') for o in out))
