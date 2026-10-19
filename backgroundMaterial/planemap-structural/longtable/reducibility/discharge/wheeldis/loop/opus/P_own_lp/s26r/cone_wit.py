import sys, cone_search as cs, cone
from ball import *
def test(lk, sv, r2, r3):
    LK = [int(c) for c in lk]; SV = [int(c) for c in sv]; D = len(LK)
    P2, pa2, pf2, order2, _, _ = frame(D, LK)
    free2 = [x for x in order2 if x[0] == 'p']
    R2 = {('s', i): SV[i] for i in range(D)}; R2.update(dict(zip(free2, [int(c) for c in r2])))
    rings = [LK, [R2[x] for x in order2], [int(c) for c in r3]]
    tot = 6 - D + sum(6 - l for r in rings for l in r)
    try: st, lens = cs.stable(None, D, rings, 8)
    except AssertionError as e: return dict(tot=tot, geom='fail')
    B = cs.mkcone(D, rings, 7); L, Pc, pac, pfc, fdc = B
    h = cone.contains(cs.C, Pc, pac, pfc, fdc, stop=False)
    return dict(tot=tot, stable=st, lens=lens, hits=sorted({x[0] for x in h})[:8], nhits=len(h))
if __name__ == '__main__':
    print(test(*sys.argv[1:5]))
