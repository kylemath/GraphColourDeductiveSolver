# s51 control (c) helper: an old-x solution -> the xo solution with the same x on every outer-letter completion
# (xo constant in ea, eb = the old x as a subfamily of xo).  usage: python3 conv51.py SOL_IN SOL_OUT
import json, sys, itertools
LI = {l: l - 5 for l in range(5, 10)}
def dg(S): return (5 + S // 25, 5 + (S // 5) % 5, 5 + S % 5)
def sidex(c, a, b, ea, eb): return (((LI[c] * 5 + LI[a]) * 5 + LI[b]) * 5 + LI[ea]) * 5 + LI[eb]
def tauo(fl, tl, s1, s2): lo, hi = min(s1, s2), max(s1, s2); return (((LI[fl] - 2) * 3 + (LI[tl] - 2)) * 3125 + lo) * 3125 + hi
S = json.load(open(sys.argv[1])); xo = {}
for k, v in S['x'].items():
    t = int(k); hi = t % 125; lo = (t // 125) % 125; fi, ti = divmod(t // 15625, 3)
    for e in itertools.product(range(5, 10), repeat=4):
        xo[str(tauo(7 + fi, 7 + ti, sidex(*dg(lo), e[0], e[1]), sidex(*dg(hi), e[2], e[3])))] = v
print('old x %d values -> xo %d values' % (len(S['x']), len(xo)))
S['x'] = {}; S['xo'] = xo; S['xoflag'] = True
json.dump(S, open(sys.argv[2], 'w'))
