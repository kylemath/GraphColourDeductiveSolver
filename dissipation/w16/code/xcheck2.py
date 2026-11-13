# W16: Team C targets v2 vs (a) world rows (5/7, 5/6/7), (b) Opus admissibility seen in row generation, (c) weights in the exact
# 5/6/7 certificates (base / rrz / all, S-and-O stack), (d) t = 0 implicit equalities of the 5/7 world.
import sys, json, pickle, glob, os; sys.path.insert(0, '/tmp/swarm-W16/code')
import torus as TT
from lp_patterns import lab_str
D = '/tmp/swarm-W16/data/'
def canon_lab(d, lk, sv):
    w = tuple(int(c) for c in lk); s = tuple(int(c) for c in sv); c = TT.canon_ws(w, s); return 'R%d %s/%s' % (d, ''.join(map(str, c[0])), ''.join(map(str, c[1])))
T = []
for l in open('/mnt/project-files/swarm/round6/C-tight-in10/targets_v2.txt'):
    if l.startswith('R '): f = l.split(); T.append((canon_lab(int(f[1]), f[2], f[3]), f[1] + ' ' + f[2] + '/' + f[3], f[4].split('_')[0]))
W = {}
for nm in ['world57.pkl', 'world57_SO.pkl', 'world57_noA111b.pkl', 'world_567_7_std.pkl']:
    W[nm.replace('.pkl', '')] = {lab_str(l) for l in pickle.load(open(D + nm, 'rb')) if l[0] == 'R'}
rej = set()
for f in glob.glob(D + 'rg567_SO_*.pkl'):
    rej |= {lab_str(l) for l in pickle.load(open(f, 'rb')).get('opus_rejected', [])}
CW = {}
for f in sorted(glob.glob(D + 'x567*_summary.json')):
    J = json.load(open(f)); tot = sum(abs(v) for v, k in J['support'] if k.startswith('R')) or 1
    CW[os.path.basename(f).replace('_summary.json', '')] = {k: v / tot for v, k in J['support'] if k.startswith('R')}
IMP = {}
for f in sorted(glob.glob(D + 'imp*.json')):
    IMP[os.path.basename(f).replace('.json', '')] = {r[1] for r in json.load(open(f)).get('rows', [])}
print('target | canonical | worlds containing it | Opus-rejected in 567 rowgen | share of receiver |w| in 5/6/7 certs | 5/7 implicit-eq sets')
for c, orig, tag in T:
    print('%-6s %-20s %-24s | %-48s | %s | %s | %s' % (tag, orig, c, ','.join(k for k, S in W.items() if c in S) or '-', 'REJ' if c in rej else '-',
          ' '.join('%s=%.1f%%' % (k.replace('x567', ''), 100 * v[c]) for k, v in CW.items() if c in v) or '-', ','.join(k for k, S in IMP.items() if c in S) or '-'))
