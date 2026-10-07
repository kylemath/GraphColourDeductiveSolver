"""[exploratory] NightTwoPocket: the Job AW counterexample A7f2-A34-w5-it918 (mirror). Both runs break: pockets of c_9 and d_9, m's far neighbours."""
import sys, os, json, time
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../27-studio-positive-config')
for d in ('jobaw', 'jobax', 'jobav', 'jobuv', 'jobay'): sys.path.insert(0, os.path.join(B, d))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../27-studio-positive-config/jobas'))
for d in ('../26-transport-adversarial', '../25-transport', '../common', '../22-winding-escape'): sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), d))
from flipsearch import rotation
from uv_lib import Hole
from jobav import Frame, trace
from mdata import tabcol, HN
r = json.load(open(os.path.join(B, 'jobaw/hits/A7f2-A34-w5-it918.json'))); h = int(r['hole'])
rot = rotation([tuple(t) for t in r['faces']]); t0 = time.time()
H = Hole('aw', h, True, rot=rot); print('states', H.S, 'time', round(time.time() - t0, 1))
adj = {v: set(x) - {h} for v, x in enumerate(H.rot) if v != h}
F = Frame(adj, H.L, H.w); N = F.names; print('names', N, 'deg m', len(adj[N['m']]))
for z in H.cycles:
    if len(z) != 20 or not all(H.DL[x] for x in z): continue
    cyc = [{v: H.col(x, v) for v in H.sp.order} for x in z]
    T = trace(F, cyc)
    if 'error' in T: print(T['error']); continue
    if not all(b for b in T['breaks']['step8break']): continue
    V = sorted(adj); cols = []
    for t, cl in enumerate(T['colourings']):
        col = dict(zip(V, cl)); Tc = tabcol(t % 10); phi = {col[N[k]]: Tc[k] for k in HN}; cols.append({v: phi[c] for v, c in col.items()})
    c9, d9 = cols[9], cols[19]
    X9 = sorted(v for v in V if c9[v] != d9[v])
    far = sorted(adj[N['m']] - {N['p'], N['y'], N['z']})
    def pk(col):
        P = {N['m']}; st = [N['m']]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in P and w not in (N['p'], N['xp']) and col[w] in (0, 2): P.add(w); st.append(w)
        return P
    Pc, Pd = pk(c9), pk(d9)
    print('cycle: breaks', T['breaks'])
    print(' far nbrs of m', far, 'adj z:', [u for u in far if N['z'] in adj[u]], 'adj y:', [u for u in far if N['y'] in adj[u]])
    print(' c9 colours', [c9[u] for u in far], ' d9 colours', [d9[u] for u in far])
    print(' Pc', sorted(Pc), 'reaches w+', N['wp'] in Pc); print(' Pd', sorted(Pd), 'reaches w+', N['wp'] in Pd)
    print(' Pc&Pd', sorted(Pc & Pd), ' X9', X9, ' X9&Pc', sorted(set(X9) & Pc), ' X9&Pd', sorted(set(X9) & Pd))
    print(' hole vertices in Pc', [k for k in HN if N[k] in Pc], 'in Pd', [k for k in HN if N[k] in Pd])
    print(' colours (c9,d9) on X9', [(v, c9[v], d9[v]) for v in X9])
    break
