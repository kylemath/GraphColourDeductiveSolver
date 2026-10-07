"""[exploratory] NightA34Two §7: is the {c(p),c(m)}-graph connected at the R3k4 visits?  Compare Job AV's Kpm_at_k4
(|K_{c(p),c(m)}(p)| at the two R3k4 states) with the number of vertices coloured c(p) or c(m) there."""
import json
from collections import Counter
st = Counter()
for l in open('../27-studio-positive-config/jobav/jobav-cycles.jsonl'):
    r = json.loads(l)
    if r['L'] != 20: continue
    N = r['names']; V = r['vertices']; ix = {v: i for i, v in enumerate(V)}; C = r['colourings']
    a = (r['K8'][0]['pos'] - 8) % 20
    for b in range(2):
        t = (a + 10 * b) % 20; col = C[t]
        pm = {col[ix[N['p']]], col[ix[N['m']]]}
        tot = sum(1 for x in col if x in pm)
        fail = r['breaks']['k4fail'][b] if 'k4fail' in r['breaks'] else None
        st[('k4fail' if fail else 'k4ok', 'pm-graph connected at R3k4', r['Kpm_at_k4'][b] == tot)] += 1
for k in sorted(st, key=str): print(st[k], k)
