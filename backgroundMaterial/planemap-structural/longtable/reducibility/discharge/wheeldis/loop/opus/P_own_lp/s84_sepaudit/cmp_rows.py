"""s84_sepaudit: compare the reported rows ("V load link apexes") of two jsepf runs, row by row.
usage: python3 cmp_rows.py A.out B.out [rot]
  default: rows are compared as (link, apexes) exactly as printed, with their loads (|diff| <= 1e-11);
  rot    : rows are first reduced to their rotation class (P_0 = max P_i representative is not assumed: min over the d rotations),
           and loads must agree within each class (for a sym-on vs sym-off comparison)."""
import sys
def rows(fn):
    R = []; end = None
    for l in open(fn):
        f = l.split()
        if f and f[0] == 'V': R.append((f[2], f[3], float(f[1])))
        elif f and f[0] == 'END': end = (int(f[1]), int(f[2]))
    return R, end
def rot(w, s):
    d = len(w); return min((w[r:] + w[:r], s[r:] + s[:r]) for r in range(d))
ra, ea = rows(sys.argv[1]); rb, eb = rows(sys.argv[2]); R = len(sys.argv) > 3 and sys.argv[3] == 'rot'
print('A: %s  %d rows, END %s' % (sys.argv[1].split('/')[-1], len(ra), ea)); print('B: %s  %d rows, END %s' % (sys.argv[2].split('/')[-1], len(rb), eb))
def key(r): return rot(r[0], r[1]) if R else (r[0], r[1])
da, db = {}, {}
for D, rr in ((da, ra), (db, rb)):
    for r in rr:
        k = key(r)
        if k in D and abs(D[k] - r[2]) > 1e-11: print('  load differs inside one key %s: %.12f vs %.12f' % (k, D[k], r[2]))
        D[k] = r[2]
dupA = len(ra) - len(da) if not R else 0; dupB = len(rb) - len(db) if not R else 0
onlyA = sorted(set(da) - set(db)); onlyB = sorted(set(db) - set(da))
bad = [(k, da[k], db[k]) for k in set(da) & set(db) if abs(da[k] - db[k]) > 1e-11]
print('distinct keys: A %d, B %d (duplicates A %d, B %d); only in A: %d; only in B: %d; common with different load: %d' % (len(da), len(db), dupA, dupB, len(onlyA), len(onlyB), len(bad)))
for k in onlyA[:5]: print('  only A:', k, '%.12f' % da[k])
for k in onlyB[:5]: print('  only B:', k, '%.12f' % db[k])
for k in bad[:5]: print('  load differs:', k)
if not R:
    sa = sorted(ra); sb = sorted(rb)
    print('row-by-row (sorted, as printed): %s' % ('IDENTICAL' if [(a, b, '%.12f' % c) for a, b, c in sa] == [(a, b, '%.12f' % c) for a, b, c in sb] else 'DIFFERENT'))
    print('row-by-row (in output order): %s' % ('IDENTICAL' if ra == rb else 'DIFFERENT'))
if ra or rb:
    allv = [r[2] for r in ra + rb]; print('load range of reported rows: %.12f .. %.12f' % (min(allv), max(allv)))
print('VERDICT: %s' % ('SAME ROW SET' if not onlyA and not onlyB and not bad else 'ROW SETS DIFFER'))
