# s69: make a solution = sol_qrand.json (random q) + random positive rr / z / zr columns.  usage: python3 mkrand.py OUT N SEED <engine args>
import sys, os, random, json
out, N, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
ENG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eng', 'pcheck.py'); sys.argv = [ENG, 'help'] + sys.argv[4:]
ns = {'__file__': ENG, '__name__': 'pcheck_s69m'}; exec(compile(open(ENG).read(), ENG, 'exec'), ns); ns['l3q_load']()
recv, adm = ns['recv_coef_R2'], ns['admissible']; rnd = random.Random(seed)
keys = {'rr': set(), 'z': set(), 'zr': set()}; n = 0
while n < N:
    d = rnd.choice((7, 7, 8, 9, 10, 11)); w = [rnd.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]; s = [rnd.choice((5, 5, 6, 6, 7, 8, 9)) for _ in range(d)]
    lk, sv = ''.join(map(str, w)), ''.join(map(str, s))
    if adm(d, lk, sv) is not None: continue
    n += 1
    for k in recv(d, lk, sv, True, None):
        if k[0] in keys: keys[k[0]].add(tuple(k[1]))
print({k: len(v) for k, v in keys.items()})
S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 's67_q7', 'sol_qrand.json')))
S['zh'] = True; S['zrflag'] = True; S['hatrr'] = True
for fam in keys: S[fam] = [[list(k), round(rnd.uniform(0.05, 3.0), 4)] for k in sorted(keys[fam])]
json.dump(S, open(out, 'w')); print('wrote', out, {f: len(S[f]) for f in keys})
