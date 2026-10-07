"""[exploratory] NightSigmaImage summary over simg.py outputs (args: jsonl files)."""
import json, sys
from collections import Counter
R = [json.loads(l) for f in sys.argv[1:] for l in open(f)]
def lt(x): return 'fix' if x['fixed'] else ('DL' if x['l1'] and x['l2'] else 'L2' if x['l2'] else 'L1' if x['l1'] else 'no')
print('Gamma-cycles:', len(R), 'lengths', dict(Counter(z['L'] for z in R)))
A = Counter(); per = Counter(); cr = Counter(); pat = Counter(); exc = Counter(); tgt = Counter(); minr = []
for z in R:
    rows = z['rows']; L = z['L']; P = L // 10
    c = Counter(); credit = 0
    for x in rows:
        A[(x['ty'], x['k'], lt(x))] += 1
        if x['ty'] == 3:
            t = lt(x); c[(x['k'], t)] += 1
            if t == 'no': credit += 3 * x['f'] - 1
            if t in ('L1', 'L2', 'no'): exc[(x['k'], t, x['i'], x['u'], x['f'])] += 1; tgt[(x['k'], t, 'Tgamma' if x['Tgamma'] else ('Tneg' if x['TW'] < 0 else 'T0' if x['TW'] == 0 else 'Tpos'))] += 1
    nf = sum(v for (k, t), v in c.items() if t == 'fix'); f34 = c[(4, 'L2')] + c[(3, 'L1')]
    per[(L, nf, f34)] += 1; minr.append((credit / L, z['tag'], z['hole'], z['cyc']))
    # period pattern of fixed points at positions 1,4,6,8 and failures at 0,2
    byp = {}
    for n, x in enumerate(rows): byp.setdefault(n // 10 if False else None, None)
    for b in range(P):
        rr = rows  # rows start anywhere; find pos-0 index
    s0 = next(n for n, x in enumerate(rows) if x['pos'] == 0)
    rows2 = rows[s0:] + rows[:s0]
    for b in range(P):
        w = rows2[10 * b:10 * b + 10]
        pat[tuple(lt(w[p]) for p in (0, 1, 2, 4, 6, 8))] += 1
print('\n(ty,k,image type) counts:'); [print('  ', k, v) for k, v in sorted(A.items())]
print('\nper cycle (L, #fixed among R3 k<=2, #failures k=3,4):'); [print('  ', k, v) for k, v in sorted(per.items())]
print('\nper period pattern of image types at positions (0,1,2,4,6,8):'); [print('  ', k, v) for k, v in pat.most_common()]
print('\nexcursion placement of non-fixed R3 images (k,type,i,u,f):'); [print('  ', k, v) for k, v in sorted(exc.items())]
print('\ntarget cycle sign (k,type,T):'); [print('  ', k, v) for k, v in sorted(tgt.items())]
minr.sort(); print('\nmin lockless credit / L:', minr[:3])
