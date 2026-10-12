"""Stream all cached roots (orders 12-22) and evaluate candidate ranks at macro 2."""
import json, pickle, sys
from multiprocessing import Pool
from collections import Counter
from engine import *

CANDS = {
 "const": lambda F: 0,
 "q": lambda F: F['q'],
 "lin": lambda F: F['lin'],
 "L": lambda F: F['L'],
 "lin+L": lambda F: F['lin'] + F['L'],
 "lin+2links": lambda F: F['lin'] + 2*F['links'],
 "lin+Lall+links": lambda F: F['lin'] + F['Lall'] + F['links'],
 "lin+linNoRho": lambda F: F['lin'] + F['linNoRho'],
 "lin+linNoRho+L": lambda F: F['lin'] + F['linNoRho'] + F['L'],
 "2lin+2L+linNoRho": lambda F: 2*F['lin'] + 2*F['L'] + F['linNoRho'],
 "lex(lin+L,linNoRho)": lambda F: (F['lin'] + F['L'], F['linNoRho']),
 "lex(lin+L,-hub)": lambda F: (F['lin'] + F['L'], -F['hubToggles']),
 "lex(lin+L,-distSum)": lambda F: (F['lin'] + F['L'], -F['distSum']),
 "2(lin+L)-hub": lambda F: 2*(F['lin'] + F['L']) - F['hubToggles'],
 "2L-hub": lambda F: 2*F['L'] - F['hubToggles'],
 "L+links-hub": lambda F: F['L'] + F['links'] - F['hubToggles'],
 "lex(2L-hub,lin)": lambda F: (2*F['L'] - F['hubToggles'], F['lin']),
 "lex(lin+linNoRho,L)": lambda F: (F['lin'] + F['linNoRho'], F['L']),
 "kd": lambda F: F['kd'],
}

def job(fn):
    g = pickle.loads(fn.read_bytes())
    order, gi = map(int, fn.stem.split('-'))
    res = []
    for r, R in g["roots"].items():
        mk = max(R['F'][i]['kd'] for i in range(len(R['P'])))
        bad = [name for name, f in CANDS.items() if stuck_states(R, f)]
        res.append((order, gi, r, mk, bad, [len(g['rot'][b]) for b in R['B']]))
    return res

if __name__ == "__main__":
    files = sorted(CACHE.glob("*.pkl"))
    allres = []
    with Pool(12) as p:
        for res in p.imap_unordered(job, files):
            allres.extend(res)
    allres.sort()
    json.dump(allres, open("holdout_eval.json", "w"))
    for lo, hi in ((12, 18), (19, 20), (21, 21), (22, 22)):
        sub = [x for x in allres if lo <= x[0] <= hi]
        print(f"orders {lo}-{hi}: roots {len(sub)}, maxkd dist {sorted(Counter(x[3] for x in sub).items())}")
        for name in CANDS:
            b = [x[:3] for x in sub if name in x[4]]
            print(f"   {name:24s} bad {len(b):4d}  {b[:6]}")
