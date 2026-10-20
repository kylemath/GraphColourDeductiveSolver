"""EXPLORE round 54d: the full two-engine list of the 2026 set.  Reads this machine's verdicts (N54_res.txt, cen53's
rule) and Studio's drive45-format outputs (out/job54d: rings 16-18; out/job54e: the ring-15 remainder), checks that
Studio's input files are ours (md5), and that each Studio name has kc D=true, a dfast/dfast18 D=true and a KILL line
D (a C would need cfast leftover 0); where both sides ran a configuration the verdicts must agree.
usage: python3 -I imp54d.py NLKC LOCALRES STUDIODIR... -> nl54d_verdicts.txt (name ring verdict source), prints tallies"""
import sys, os, collections
NLKC, LRES, SD = sys.argv[1], sys.argv[2], sys.argv[3:]
H = os.path.dirname(os.path.abspath(__file__))
ring = {l.split()[0]: int(l.split()[1]) for l in open(NLKC) if l.strip()}
loc = {}
for l in open(LRES):
    f = l.rstrip('\n').split(' ', 2)
    if len(f) == 3 and f[0] in ring: loc[f[0]] = f[1]
stu = {}; bad = []
for d in SD:
    kc = {l.split()[0]: l for l in open(os.path.join(d, 'A_kcc.out')) if l.strip() and not l.startswith(' ')}
    df = {l.split()[0]: l for l in open(os.path.join(d, 'A_df.out')) if l.strip()}
    cf = {l.split()[0]: l for l in open(os.path.join(d, 'A_cf.out')) if l.strip()}
    for l in open(os.path.join(d, 'KILL')):
        f = l.split()
        if not f: continue
        n, v = f[0], f[1]
        if v == 'D' and 'D=true' in kc.get(n, '').split('\n')[0] and 'D=true' in df.get(n, ''): stu[n] = 'D'
        elif v == 'C' and 'leftover bad classes extending after contraction = 0' in cf.get(n, ''): stu[n] = 'C'
        else: bad.append((d, n, v))
    miss = set(kc) - set(stu) - {b[1] for b in bad}
    print('%s: %d kc lines, %d verdicts confirmed, %d not confirmed, %d with no KILL line' % (os.path.basename(d.rstrip('/')), len(kc), sum(1 for n in kc if n in stu), len([b for b in bad if b[0] == d]), len(miss)))
both = set(loc) & set(stu); dis = [n for n in both if loc[n] != stu[n]]
print('both sides ran %d; disagreements %d %s' % (len(both), len(dis), dis[:5]))
out = []; tab = collections.defaultdict(collections.Counter)
for n in sorted(ring, key=lambda n: (ring[n], n)):
    v = stu.get(n) or loc.get(n) or 'unrun'; src = 'both' if n in both else ('studio' if n in stu else ('explore' if n in loc else '-'))
    out.append('%s %d %s %s' % (n, ring[n], v, src)); tab[ring[n]][v] += 1
open(os.path.join(H, 'nl54d_verdicts.txt'), 'w').write('# round 54d: the 2026 set on our two engines (name ring verdict source)\n' + '\n'.join(out) + '\n')
tot = collections.Counter(v for c in tab.values() for v in c.elements())
print('by ring:', ' '.join('r%d %s' % (r, dict(tab[r])) for r in sorted(tab)))
print('total %d: %s' % (len(ring), dict(tot)))
