# W16: Team C targets (C-tight-in10/targets_v1.txt) vs world rows and t = 0 implicit equalities
import sys, json, pickle, glob, os; sys.path.insert(0, '/tmp/swarm-W16/code')
import torus as TT
from lp_patterns import lab_str
def canon_lab(d, lk, sv):
    w = tuple(int(c) for c in lk); s = tuple(int(c) for c in sv); c = TT.canon_ws(w, s); return 'R%d %s/%s' % (d, ''.join(map(str, c[0])), ''.join(map(str, c[1])))
T = []
for l in open('/mnt/project-files/swarm/round6/C-tight-in10/targets_v1.txt'):
    if l.startswith('R '): f = l.split(); T.append((canon_lab(int(f[1]), f[2], f[3]), f[1] + ' ' + f[2] + '/' + f[3], f[4][:40]))
worlds = {}
for f in sorted(glob.glob('/tmp/swarm-W16/data/world*.pkl')):
    try: labs = pickle.load(open(f, 'rb'))
    except Exception: continue
    worlds[os.path.basename(f)] = {lab_str(l) for l in labs if l[0] == 'R'}
imps = {}
for f in sorted(glob.glob('/tmp/swarm-W16/data/imp*.json')):
    J = json.load(open(f)); imps[os.path.basename(f)] = {r[1] for r in J.get('rows', [])}
for c, orig, tag in T:
    inw = [w for w, S in worlds.items() if c in S]; ini = [w for w, S in imps.items() if c in S]
    print('%-26s %-22s canon %-24s in worlds: %s | implicit-eq in: %s' % (orig, tag[:22], c, ','.join(inw) or '-', ','.join(ini) or '-'))
