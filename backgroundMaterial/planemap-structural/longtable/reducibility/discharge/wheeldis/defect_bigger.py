"""Larger configurations around a defect (README §7, test G follow-up; exploratory).  From the explicit patch
(b8b/rings.py), for every vertex of the cluster Y writes (dfast format):
  K5_<v>   : the 5-centred 2-ball of each 5 (v + link + second ring, exact degrees; ring = third ring) -- the K-key family;
  R2_<u>   : the exact-degree 2-ball of each 7 (u + link + second ring; ring = third ring);
  BF_<u>_S : u + S + every link vertex of S at its exact degree, B included (the "B fixed" family), for every S, |S| >= 1
             (|S| = 1 included: a sender with its big neighbours fixed);
  Y1       : the cluster plus its 6-neighbours (N_1(Y), exact degrees; ring = N_2(Y) minus N_1(Y)).
Prints ring sizes.  Usage: python3 defect_bigger.py SIG OUT.cfg"""
import sys, os, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
SIG, BIGOUT = sys.argv[1], sys.argv[2]
src = open(os.path.join(HERE, 'defect_verify.py')).read()
src = src.replace("HERE = os.path.dirname(os.path.abspath(__file__))", "HERE = %r" % HERE)
pre = src[:src.index('c = sum(6 - deg[v] for v in Y)')]
post = src[src.index('def extract_cfg'):src.index('lines = []; nonsimple')]
sys.argv = ['v', SIG, '/dev/null']; exec(pre); exec(post)
lines = []; rings_ = collections.defaultdict(list)
def add(nm, I):
    cfg = extract_cfg(sorted(I))
    if cfg is None:
        RS = set(y for x in I for y in adj[x]) - set(I); I2 = set(I) | {y for y in RS if adj[y] <= (set(I) | RS)}
        cfg = extract_cfg(sorted(I2)) if I2 != set(I) else None; nm += '+'
    if cfg is None: rings_[nm.split('_')[0]].append('nosimple'); return
    lines.append('%s %s' % (nm, cfg)); rings_[nm.split('_')[0]].append(int(cfg.split()[0]))
for v in Y:
    N2 = {v} | adj[v] | {z for y in adj[v] for z in adj[y]}
    if deg[v] == 5: add('K5_%d' % v, N2)
    else:
        add('R2_%d' % v, N2)
        S5 = [x for x in rot(v) if deg[x] == 5]
        for k in range(1, len(S5) + 1):
            for S in itertools.combinations(S5, k):
                I = {v} | set(S)
                for s in S: I |= adj[s]
                add('BF_%d_%s' % (v, '-'.join(map(str, S))), I)
add('Y1_all', set(Y) | {y for x in Y for y in adj[x]})
open(BIGOUT, "w").write("\n".join(lines) + "\n")
for k, v in sorted(rings_.items()): print(k, len(v), 'rings', sorted(collections.Counter(v).items(), key=str))
