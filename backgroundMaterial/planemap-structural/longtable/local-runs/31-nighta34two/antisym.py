"""[exploratory] NightA34Two §5: search for an antisymmetric pair quantity Delta_i(c,d) = f(c_i) - f(d_i) with
B(c) => Delta > 0 on all 19 breaking L = 20 cycles (B = step-8 break of the run).  Any such f closes A34' on L = 20
(both breaks would give Delta > 0 and Delta < 0).  f ranges over: colour-class sizes by role letter (frame of position i,
roles from the hole: alpha = c(x_j) etc. via the named vertices), |K_i| (the step-i swapped component)."""
import json
from collections import Counter, defaultdict
F = '../27-studio-positive-config/jobav/jobav-cycles.jsonl'
res = defaultdict(Counter)
for l in open(F):
    r = json.loads(l)
    if r['L'] != 20: continue
    V = r['vertices']; N = r['names']; C = r['colourings']; a = (r['K8'][0]['pos'] - 8) % 20
    tau = {int(k): v for k, v in r['closing_colour_map'].items()}
    def CC(t): return C[t] if t < 20 else [tau[x] for x in CC(t - 20)]
    c = [dict(zip(V, CC(a + i))) for i in range(21)]
    rho = {c[0][v]: c[10][v] for v in N.values()}; ri = {b: x for x, b in rho.items()}
    d = [{v: ri[x] for v, x in c[10 + i].items()} for i in range(10)]
    S = {s['pos']: s for s in r['steps']}
    br = r['breaks']['step8break']
    if not sum(br): continue
    b = br.index(True); runs = (c, d) if b == 0 else (d, c)   # (breaking run, other run), same frame
    for i in range(10):
        ub, uo = runs[0][i], runs[1][i]
        for nm in ('p', 'm', 'y', 'z'):
            col = ub[N[nm]]   # same in both runs (hole-sync)
            f = lambda u: sum(1 for v in V if u[v] == col)
            res[(i, 'class of c(%s)' % nm)][(f(ub) > f(uo)) - (f(ub) < f(uo))] += 1
        Kb = len(S[(a + i + 10 * b) % 20]['K']); Ko = len(S[(a + i + 10 * (1 - b)) % 20]['K'])
        res[(i, '|K_i|')][(Kb > Ko) - (Kb < Ko)] += 1
good = [(k, v) for k, v in res.items() if set(v) == {1} or set(v) == {-1}]
for k in sorted(res): print(k, dict(res[k]))
print('SIGN-CONSISTENT on 19/19:', good)
