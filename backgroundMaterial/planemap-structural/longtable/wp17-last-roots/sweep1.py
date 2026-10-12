"""Tie-break and small-weight additions on top of lin+L, all 1586 roots, macro 2."""
import json
from evalr import *
NEW = ['q','Lall','links','shortLinks','repMass','hubToggles','maxK','touched','nComp','distSum','dist2',
       'singLinks','rhoLinks','linRho','linNoRho','lin_int','allComps']
res = {}
for x in NEW:
    for sgn in (1, -1):
        name = f"(lin+L, {'+' if sgn>0 else '-'}{x}) lex"
        res[name] = badroots(lambda f, x=x, s=sgn: (f['lin'] + f['L'], s * f[x]))
        print(name, res[name], flush=True)
for x in ['linNoRho','lin_int','allComps','hubToggles']:
    for sgn in (1, -1):
        for W in (2, 3, 5, 10, 50):
            name = f"{W}(lin+L) {'+' if sgn>0 else '-'} {x}"
            res[name] = badroots(lambda f, x=x, s=sgn, W=W: W * (f['lin'] + f['L']) + s * f[x])
            print(name, res[name], flush=True)
json.dump({k: v for k, v in res.items()}, open('sweep1.json', 'w'), indent=0)
