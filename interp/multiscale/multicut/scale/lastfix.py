# Final-step diagnosis for ico10:2:rand:any: the outer triangle carries t = 0 for every proper colouring, so the
# failure is properness.  Find the least ball radius R around v whose recolouring completes the sphere (pure SAT),
# and the distance from v to the nearest odd-degree vertex.  Also t of the boundary walk once all odd vertices are in.
import sys, pickle, collections
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/unbounded/')
import vr, mc
from pi import make, ball
from pysat.solvers import Cadical153
fn = sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/multiscale/multicut/unbounded/fail_ico10_2_rand_any.pkl'
D = pickle.load(open(fn, 'rb')); fl = D['fail']; name = D['spec'].split(':')[0]
adj = make(name); n = len(adj); v = fl['v']; col = dict(fl['col'])
d = ball(lambda x: adj[x], v, 50); odd = [x for x in range(n) if len(adj[x]) % 2]
print(D['spec'], 'v', v, 'deg', len(adj[v]), 'dist to nearest odd vertex', min(d[x] for x in odd), 'nbr colours', sorted(col[y] for y in adj[v]))
def fill(R):
    F = set(x for x in d if d[x] <= R); var = lambda x, c: 4*x + c + 1; S = Cadical153()
    for x in F:
        S.add_clause([var(x, c) for c in range(4)])
        for y in adj[x]:
            if y in F and y > x:
                for c in range(4): S.add_clause([-var(x, c), -var(y, c)])
            elif y not in F:
                S.add_clause([-var(x, col[y])])
    return S.solve()
for R in range(0, 12):
    ok = fill(R); print('R', R, '|ball|', sum(1 for x in d if d[x] <= R), 'odd in ball', sum(1 for x in odd if d[x] <= R), 'fill', ok, flush=True)
    if ok: break
print('t trace (last 40 recs):', [(r['n'], r['nodd'], r['t']) for r in D['recs'][-40:]])
