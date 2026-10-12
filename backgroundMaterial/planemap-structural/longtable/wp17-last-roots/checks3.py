import json
from evalr import *
C = {
 "lin+L": lambda F: F['lin'] + F['L'],
 "lin": lambda F: F['lin'],
 "q": lambda F: F['q'],
 "linNoRho": lambda F: F['linNoRho'],
 "linRho": lambda F: F['linRho'],
 "lin+linNoRho": lambda F: F['lin'] + F['linNoRho'],
 "lin+2linNoRho": lambda F: F['lin'] + 2*F['linNoRho'],
 "2L-hub": lambda F: 2*F['L'] - F['hubToggles'],
 "L+links-hub": lambda F: F['L'] + F['links'] - F['hubToggles'],
 "L": lambda F: F['L'],
 "L-hub": lambda F: F['L'] - F['hubToggles'],
 "-hub": lambda F: -F['hubToggles'],
}
out = {}
for name, f in C.items():
    out[name] = {f"macro{m}": badroots(f, macro=m) for m in (1, 2, 3)}
    print(name, {k: (len(v), v[:8]) for k, v in out[name].items()}, flush=True)
json.dump(out, open('checks3.json', 'w'), indent=1)
