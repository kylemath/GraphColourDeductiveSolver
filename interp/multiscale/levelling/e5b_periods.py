# E5b (corrected encoding): for 4-colourable 6-regular tori, can both height periods vanish?  If not, the minimum
# |t1|^2, |t2|^2 (separately) and the minimum of max(|t1|^2,|t2|^2) over colourings.
import json, sys
import e5_torus as E
NORMS = [0, 1, 3, 4, 7, 9, 12, 13, 16, 19, 21, 25, 27, 28, 31, 36, 37, 39, 43, 48, 49, 52, 57, 61, 63, 64, 100, 10**4]
R = [json.loads(l) for l in open('e5_torus.jsonl')]
out = open('e5b_periods.jsonl', 'w')
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 36
for x in R:
    if not x['col4'] or x['n'] > NMAX: continue
    p, q, r = x['p'], x['q'], x['r']
    rec = dict(p=p, q=q, r=r, n=x['n'], col3=x['col3'])
    rec['zero'] = E.solve(p, q, r, target=('zero', 'zero'))
    if not rec['zero']:
        rec['min_t1sq'] = next(t for t in NORMS if E.solve(p, q, r, target=(t, None)))
        rec['min_t2sq'] = next(t for t in NORMS if E.solve(p, q, r, target=(None, t)))
        rec['min_maxsq'] = next(t for t in NORMS if t >= max(rec['min_t1sq'], rec['min_t2sq']) and E.solve(p, q, r, target=(t, t)))
    out.write(json.dumps(rec)+'\n'); out.flush()
