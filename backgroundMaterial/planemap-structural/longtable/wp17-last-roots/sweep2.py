"""Grid: a*linRho + b*linNoRho + c*L + d*links + e*hubToggles (e may be negative), macro 2, all 1586 roots."""
import json, itertools
from evalr import *
out = []
for a, b, c, d, e in itertools.product(range(0, 4), range(0, 4), range(0, 3), range(0, 2), (-1, 0)):
    if a == b == c == d == 0: continue
    f = lambda F, a=a, b=b, c=c, d=d, e=e: a*F['linRho'] + b*F['linNoRho'] + c*F['L'] + d*F['links'] + e*F['hubToggles']
    br = badroots(f)
    out.append({"linRho": a, "linNoRho": b, "L": c, "links": d, "hub": e, "bad": br})
    if len(br) <= 2: print(a, b, c, d, e, br, flush=True)
json.dump(out, open('sweep2.json', 'w'))
