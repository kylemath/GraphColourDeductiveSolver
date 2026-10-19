"""P2 s13: per-file D counts for an args file with pcheck's own pat= loader rules (D=true line, name ^[epf]\\d+_).
Columns: names = accepted lines; newnames = names not seen in an earlier file (Studio's SEEN rule); newpat = pattern
tuples new to PATS (what pcheck actually adds; distinct (d, slot->letter-set) after parsing). usage: dcount.py ARGS ROOT"""
import sys, re, os, runpy, io, contextlib, collections
args, root = sys.argv[1], sys.argv[2]
sys.argv = ['pcheck.py', 'none', 'root=' + root]
with contextlib.redirect_stdout(io.StringIO()): G = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pcheck.py'))
pname = G['pname']; seen = set(); pats = set(); tot = collections.Counter()
print('# file names newnames newpat newpat_by_d  (pat= files only; missing files marked MISSING)')
for a in open(args).read().split():
    if not a.startswith('pat='): continue
    fn = a[4:]; p = fn if os.path.isabs(fn) else os.path.join(root, fn)
    if not os.path.exists(p): print(os.path.basename(fn), 'MISSING'); continue
    n = nn = npat = 0; byd = collections.Counter()
    for line in open(p):
        if line.strip() and 'D=true' in line and re.match(r'^[epf]\d+_', line):
            nm = line.split()[0]; n += 1
            if nm not in seen: seen.add(nm); nn += 1
            d, P = pname(nm)
            if (d, P) not in pats: pats.add((d, P)); npat += 1; byd[d] += 1
    tot['names'] += n; tot['newnames'] += nn; tot['newpat'] += npat
    print(os.path.basename(fn), n, nn, npat, ' '.join('%d:%d' % kv for kv in sorted(byd.items())))
print('# TOTAL', dict(tot))
