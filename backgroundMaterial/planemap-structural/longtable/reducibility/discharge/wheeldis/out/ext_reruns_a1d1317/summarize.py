# out/ext_reruns_a1d1317 summary: pass = D=true (kcD/cfD), or C-REDUCIBLE with leftover 0 under the listed X (kcC/cfC)
import glob, collections, re, sys, hashlib
X = 'out/ext_reruns_a1d1317/'
R = {l.split()[0]: int(l.split()[1]) for l in open(X + 'in/configs.in')}
J = {p: [tuple(l.split()) for l in open(X + 'jobs_p%d.txt' % p)] for p in (1, 2, 3)}
def ok(e, o):
    if e.endswith('D'): return 'D=true' in o
    return 'C-REDUCIBLE' in o and re.search(r'leftover[^=\d]*(=\s*)?0(\D|$)', o) is not None and 'INCOMPLETE' not in o
for p in (1, 2, 3):
    C = collections.Counter(); bad = []; seen = set(); fs = sorted(glob.glob(X + 'p%d_s*.tsv' % p))
    for f in fs:
        for l in open(f):
            n, e, t, o = l.rstrip('\n').split('\t', 3); seen.add((n, e))
            v = ok(e, o); C[(e, R[n], 'PASS' if v else 'FAIL')] += 1
            if not v: bad.append((n, e, o))
    miss = [j for j in J[p] if j not in seen]
    print('P%d: %d of %d jobs done, %d missing; PASS %d, FAIL %d' % (p, len(seen), len(J[p]), len(miss), sum(v for k, v in C.items() if k[2] == 'PASS'), len(bad)))
    for k in sorted(C): print('   %s ring %d %s: %d' % (k[0], k[1], k[2], C[k]))
    for b in bad: print('   FAIL %s %s: %s' % b)
    for f in fs: print('   md5 %s %s' % (hashlib.md5(open(f, 'rb').read()).hexdigest(), f.split('/')[-1]))
