"""Per-binder B-fixed status (ring <= 16): D / C / neither / untested, and HARD28. Usage: python3 binder_report.py ROWS"""
import sys, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROWS = sys.argv[1]
src = open(os.path.join(HERE, 'gen28.py')).read()
sys.argv = ['gen28.py', '/dev/null', '16', '/dev/null', 'all']
exec(src[:src.index('\narrs = []')])
for line in open(ROWS):
    m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line)
    if not m: continue
    d, lk, sv = int(m.group(1)), m.group(2), m.group(3)
    vs = variants(d, lk, sv); st = collections.Counter(); kil = []
    for x in vs:
        nm = x[5]
        if DV.get(nm) == 'D': st['D'] += 1; kil.append(nm)
        elif CV.get(nm) == 'C': st['C'] += 1; kil.append(nm)
        elif DV.get(nm) == 'notD' and CV.get(nm) == 'neither': st['neither'] += 1
        elif DV.get(nm) == 'notD': st['notD, C untested'] += 1
        else: st['untested'] += 1
    hard = not kil and not st['untested'] and not st['notD, C untested']
    print('%s/%s: %d B-fixed S at ring<=16 %s%s%s' % (lk, sv, len(vs), dict(st), ' HARD28' if hard else '',
          (' killed by ' + kil[0]) if kil else ''))
