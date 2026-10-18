"""EXPLORE round 35: compare kc-C (valc_kcc.txt) with cfast (valc_ref.txt)."""
import re, collections
ref = {}
for l in open('valc_ref.txt'):
    f = l.split(); nm = f[0]
    d = dict(x.split('=', 1) for x in f[2:])
    ref[nm] = d
kc = {}; cur = None
import sys
KF = sys.argv[1] if len(sys.argv) > 1 else 'valc_kcc.txt'
for l in open(KF):
    if not l.startswith(' '): cur = l.split()[0]; kc[cur] = {'x': {}, 'C': None, 'D': 'D=true' in l}; continue
    m = re.match(r'\s+X=(\{[^}]*\}) adm=(\w+)(?: leftover (\d+))?', l)
    if m: kc[cur]['x'][m.group(1)] = (m.group(2), m.group(3)); continue
    if 'C-REDUCIBLE' in l: kc[cur]['C'] = True; kc[cur]['X'] = re.search(r'X=(\{[^}]*\})', l).group(1)
    elif 'C=false' in l: kc[cur]['C'] = False
st = collections.Counter(); bad = []
def norm(x): return x   # kc prints edges in its own order; compare as sets
def eset(x): return frozenset(e if e.startswith('R') else '-'.join(sorted(e.split('-'), key=lambda v: int(v[1:]))) for e in x.strip('{}').split(','))
for nm, r in ref.items():
    k = kc.get(nm)
    if not k: st['missing'] += 1; continue
    if k['D']: st['kcD?'] += 1; bad.append(('D', nm)); continue
    for key in ('X', 'best'):
        x = r[key]
        if x == 'None': continue
        hit = [v for xx, v in k['x'].items() if eset(xx) == eset(x)]
        if not hit: st['x_not_evaluated'] += 1; continue
        adm, L = hit[0]
        want = 0 if key == 'X' else int(r['leftover'])
        if adm == 'no': st['cfastX_inadmissible_for_kc'] += 1; continue
        if int(L) == want: st['leftover_equal'] += 1
        else: st['leftover_MISMATCH'] += 1; bad.append(('L', nm, x, L, want))
    cC, kC = r['C'] == 'True', k['C']
    st['cfastC=%s kcC=%s' % (cC, kC)] += 1
    if kC and not cC: bad.append(('C', nm))
print(dict(st)); print('problems', bad[:20])
