# s86: candidate matcher, usage: python3 patmatch.py <viol file> <pattern files...>: for each violated row (d sum excess link apex) list the patterns f<d>_<link>_<apex> ('.' wildcard) that match it under rotation / reflection. A screen only: confirm with upperR2 on the family plus the chosen file.
import sys, re, glob
# candidate matcher: pattern f<d>_<link>_<apex> vs row (link, apex); '.' wildcard; all rotations, reflections with both apex alignments
def variants(link, apex):
    d = len(link); out = set()
    for r in range(d):
        L = link[r:] + link[:r]; A = apex[r:] + apex[:r]; out.add((L, A))
        Lr = L[::-1]; Ar = A[::-1]
        out.add((Lr, Ar)); out.add((Lr, Ar[1:] + Ar[:1])); out.add((Lr, Ar[-1:] + Ar[:-1]))
    # close under rotation of reflected forms
    o2 = set()
    for L, A in out:
        for r in range(d): o2.add((L[r:] + L[:r], A[r:] + A[:r]))
    return o2
def m(p, s): return all(a == '.' or a == b for a, b in zip(p, s))
pats = []
for f in sys.argv[2:]:
    for line in open(f):
        mm = re.match(r'\s*(f(\d+)_([0-9.]+)_([0-9.]+))\s', line)
        if mm: pats.append((mm.group(1), int(mm.group(2)), mm.group(3), mm.group(4), f.split('/')[-1]))
rows = [l.split() for l in open(sys.argv[1])]
for r in rows:
    d, link, apex = int(r[0]), r[3], r[4]
    V = variants(link, apex)
    hits = sorted({(n, f) for n, dd, pl, pa, f in pats if dd == d and any(m(pl, L) and m(pa, A) for L, A in V)})
    print(d, link, apex, r[2], hits[:6])
