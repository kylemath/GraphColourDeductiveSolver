# E1c: larger balls (r = 10..14): is tau <= 1 feasible (direct SAT), and is tau < 1 infeasible when the rule says so?
import json, random, time
from lev import *
from e1_survey import graph
rng = random.Random(7); out = open('e1c_big.jsonl', 'w')
for name in ['ico20', 'ico30', 'BASE_rand22', 'M5_ico31']:
    T = graph(name); n = len(T.adj)
    for r in [10, 12, 14]:
        for k in range(2):
            c = 0 if (k == 0 and name.startswith('ico')) else rng.randrange(n)
            cl = Cluster(T, bfs(T.adj, c, r)); t = time.time()
            ok1 = sat_level(cl, 1.0, budget=5*10**6)
            rule = (not cl.parity_odd) and sum(cl.s) % 3 == 0
            ok0 = sat_level(cl, 0.75, budget=5*10**6) if ok1 not in (None, 'UNK') else None
            rec = dict(name=name, r=r, c=c, n=len(cl.S), m=cl.m, nodd=len(cl.odd), chords=len(chords(cl)),
                       tau_le_1=(ok1 not in (None, 'UNK')) if ok1 != 'UNK' else 'UNK',
                       tau_le_0866=(ok0 not in (None, 'UNK')) if ok0 != 'UNK' else 'UNK', rule_predicts_0866=rule,
                       sec=round(time.time()-t, 1))
            out.write(json.dumps(rec)+'\n'); out.flush(); print(rec, flush=True)
