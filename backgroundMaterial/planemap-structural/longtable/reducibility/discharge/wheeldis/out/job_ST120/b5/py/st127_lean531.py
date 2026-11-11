#!/usr/bin/env python3
"""ST-127 (3): the 10 Lean531 configs (keep_lean_C, CCV.hC_all) marked built by name only: compare the Lean literal
(cf: r, m, ringAdj, intAdj in out/lean_ccover/1c56a79e/CCover.lean, ccEntries) with our loop/k44/rsst.txt kc line.
Exact (as per-vertex sets) first; otherwise search a ring rotation/mirror + interior relabelling (iso).
Writes st127/lean531_check.tsv and st127/lean_backing_v2.tsv (v1 + a literal column for these 10)."""
import os, re, sys, itertools
H = os.path.dirname(os.path.abspath(__file__)); B5 = os.path.normpath(os.path.join(H, '..'))
OUT = os.path.normpath(os.path.join(B5, '..', '..')); WD = os.path.normpath(os.path.join(OUT, '..'))
ROOT = os.path.normpath(os.path.join(WD, *(['..'] * 6)))
CC = os.path.join(ROOT, 'out', 'lean_ccover', '1c56a79e', 'CCover.lean')
names = ['rsst051', 'rsst072', 'rsst118', 'rsst137', 'rsst140', 'rsst148', 'rsst178', 'rsst180', 'rsst187', 'rsst217']
txt = open(CC).read()
lean = {}
for m in re.finditer(r'cf := \{\s*name := "([^"]+)", r := (\d+), m := (\d+),\s*ringAdj := #\[(.*?)\],\s*intAdj := #\[(.*?)\] \}', txt, re.S):
    nm = m.group(1)
    arr = lambda s: [sorted(int(x) for x in a.split(',') if x.strip()) for a in re.findall(r'#\[([^\]]*)\]', s)]
    lean[nm] = (int(m.group(2)), int(m.group(3)), arr(m.group(4)), arr(m.group(5)))
kc = {}
for l in open(os.path.join(WD, 'loop/k44/rsst.txt')):
    f = l.split()
    if f: kc[f[0]] = (int(f[1]), int(f[2]), [sorted(int(y) for y in x.split(',')) if x != '-' else [] for x in f[3].split(';')],
                      [sorted(int(y) for y in x.split(',')) if x != '-' else [] for x in f[4].split(';')])
def iso(a, b):
    """ring map i -> (s*i + t) mod r, interior permutation by backtracking."""
    r, m, ra, ia = a; r2, m2, rb, ib = b
    if (r, m) != (r2, m2): return None
    for t in range(r):
        for s in (1, -1):
            rm = lambda i: (s * i + t) % r
            # interior perm p: a-vertex j -> b-vertex p[j]
            p = {}
            def ok(j, q):
                if sorted(rm(x) for x in ra[j]) != rb[q] or len(ia[j]) != len(ib[q]): return False
                return all((p[k] in ib[q]) == (k in ia[j]) for k in p)
            def rec(j):
                if j == m: return True
                for q in range(m):
                    if q in p.values() or not ok(j, q): continue
                    p[j] = q
                    if rec(j + 1): return True
                    del p[j]
                return False
            if rec(0): return (t, s, dict(p))
    return None
rows = ['# rsst\tlean_name\tresult\tdetail']
res = {}
for n in names:
    full = [k for k in kc if k.startswith(n + '_')][0]
    ln = [k for k in lean if k == full]
    if not ln: rows.append('%s\t-\tNOT_FOUND\t' % full); res[full] = 'NOT_FOUND'; continue
    a = lean[full]; b = kc[full]
    if a == b: rows.append('%s\t%s\tIDENTICAL\tr=%d m=%d ringAdj/intAdj equal as sets' % (full, full, a[0], a[1])); res[full] = 'IDENTICAL'
    else:
        f = iso(a, b)
        if f: rows.append('%s\t%s\tISO\tring i->%+d*i+%d, interior %s' % (full, full, f[1], f[0], f[2])); res[full] = 'ISO'
        else: rows.append('%s\t%s\tDIFFERENT\t' % (full, full)); res[full] = 'DIFFERENT'
open(os.path.join(B5, 'st127', 'lean531_check.tsv'), 'w').write('\n'.join(rows) + '\n')
print('\n'.join(rows))
v1 = [l.rstrip('\n') for l in open(os.path.join(B5, 'st127', 'lean_backing.tsv'))]
out = [v1[0] + '\tliteral_check(v2)']
for l in v1[1:]:
    nm = l.split('\t')[0]
    out.append(l + '\t' + ('Lean531 literal vs rsst.txt: ' + res[nm] + ' (st127/lean531_check.tsv)' if nm in res else ''))
open(os.path.join(B5, 'st127', 'lean_backing_v2.tsv'), 'w').write('\n'.join(out) + '\n')
