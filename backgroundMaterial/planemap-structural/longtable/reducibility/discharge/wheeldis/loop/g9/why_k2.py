"""G9 probe 2 (exploratory): for a centre degree C and ring-1 word W (ring 2.. all 6), list every wheel of the patch
that is reducible under the defect tables (9 = centre letter).  Usage: python3 why_k2.py C W [ring2word]"""
import sys, os, collections
WD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
C, W = int(sys.argv[1]), sys.argv[2]; R2 = sys.argv[3] if len(sys.argv) > 3 else None
src = open(os.path.join(WD, 'defect.py')).read().replace('HERE = os.path.dirname(os.path.abspath(__file__))', 'HERE = %r' % WD)
sys.argv = ['defect.py', '5', '1', '1', '/dev/null', 'strict7']; exec(src[:src.index("CENTRE, K, CMIN, OUT")])
sys.path.insert(0, os.path.join(os.path.dirname(WD), 'b8b')); from rings import Layered
L = Layered(C); L.add_ring([int(c) for c in W])
if R2: L.add_ring([int(c) for c in R2])
for _ in range(4): L.add_ring([6] * len(L.ring()))
nxt = collections.defaultdict(dict)
for a, b, c in L.tris: nxt[a][b] = c; nxt[b][c] = a; nxt[c][a] = b
outer = set(L.ring()); ring_of = {v: k for k, R in enumerate(L.rings) for v in R}
for u in sorted(L.deg):
    if u in outer or ring_of[u] > 3: continue
    s0 = min(nxt[u]); lk = [s0]; y = nxt[u][s0]
    while y != s0: lk.append(y); y = nxt[u][y]
    w = [min(L.deg.get(x, 6), 9) for x in lk]; d = L.deg[u]
    b = (d == 5 and isR5(w)) or (d == 6 and bad6(w)) or (d == 7 and canon(w) in D7)
    if b: print('ring', ring_of[u], 'deg', d, 'link', ''.join(map(str, w)), 'canon', ''.join(map(str, canon(w))), 'REDUCIBLE')
