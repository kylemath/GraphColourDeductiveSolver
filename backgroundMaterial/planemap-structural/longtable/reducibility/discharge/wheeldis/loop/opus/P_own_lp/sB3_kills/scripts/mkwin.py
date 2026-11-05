# B3: kc line of a named window on a given row.  usage: python3 mkwin.py LK SV WLK WSV [pJK=L ...]
#   WLK / WSV: the window's link / apex masks over the row ('.' = not in the window; a letter must equal the row's);
#   u is always in the window; pJK=L puts private k of w_j at letter L into the window.
import sys
from gen3 import build, ringcycle, kcline, wname
from kcanon import code
LK, SV, WL, WS = sys.argv[1:5]; ex = sys.argv[5:]
pdeg = {('p', int(e[1]), int(e[2])): int(e.split('=')[1]) for e in ex}
adj, rot, name, deg, Z3, inv = build(LK, SV, pdeg=pdeg or None)
S = {('u',)} | {('w', j) for j in range(len(LK)) if WL[j] != '.'} | {('s', j) for j in range(len(LK)) if WS[j] != '.'} | set(pdeg)
assert all(WL[j] in '.' + LK[j] for j in range(len(LK))) and all(WS[j] in '.' + SV[j] for j in range(len(LK)))
Is = set(inv[x] for x in S); order = ringcycle(adj, Is)
nm = wname(LK, SV, S, [(k, v) for k, v in pdeg.items()])
kl = kcline(nm, adj, Is, order); print(code(kl), kl)
