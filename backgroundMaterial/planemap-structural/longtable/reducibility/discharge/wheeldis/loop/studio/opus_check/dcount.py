"""Distinct parsed D patterns per pat= file, Studio loader semantics (wlp3.py parse/fullparse/dropped), in args order.
Columns as Opus's dcount.txt: file names newnames newpat newpat_by_d. A pattern key is (d, sorted parse) or, for
names with dropped letters, ('full', d, sorted fullparse).
Usage: WLP_SEPF=1 python3 dcount.py ARGSFILE"""
import sys, os, re, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
args = open(sys.argv[1]).read().split()
src = open(os.path.join(HERE, 'wlp3.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3.py')), 1)
sys.argv = ['wlp3'] + args
exec(src[:src.index('PATS = []; FULLP = []')])
SEEN, SEENP = set(), set(); tot = 0; out = []
for a in args:
    if not a.startswith('pat='): continue
    fn = a[4:]; allf = fn.endswith(':all'); fn = fn[:-4] if allf else fn
    p = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
    if not os.path.exists(p): out.append('%s MISSING' % os.path.basename(fn)); continue
    nm_n = new_n = 0; newp = 0; byd = collections.Counter()
    for line in open(p):
        if line.strip() and (allf or 'D=true' in line) and re.match(r'^[epf]\d+_', line):
            nm = line.split()[0]; nm_n += 1
            if nm in SEEN: continue
            SEEN.add(nm); new_n += 1
            if dropped(nm): d, F = fullparse(nm); key = ('full', d, tuple(sorted(F)))
            else: d, P = parse(nm); key = (d, tuple(sorted(P)))
            if key in SEENP: continue
            SEENP.add(key); newp += 1; byd[d] += 1
    tot += newp
    out.append('%s %d %d %d %s' % (os.path.basename(fn), nm_n, new_n, newp, ' '.join('%d:%d' % kv for kv in sorted(byd.items()))))
print('\n'.join(out)); print('# TOTAL distinct parsed D patterns %d (names %d)' % (tot, len(SEEN)))
