"""configs for cfast: every notD candidate K(S) with ring <= RC of the MISS situations of a res file.
Usage: python3 clist.py RESFILE RC OUT"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RES, RC, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
sys.argv = ['inst.py', '/dev/null', '0', 'clist']
import inst
seen = {}
for line in open(RES):
    f = line.split()
    if f[2] != 'MISS': continue
    for r, mk, S, kb, cb in inst.cands(tuple(map(int, f[0])), tuple(map(int, f[1]))):
        if kb and r <= RC and inst.V.get(kb) == 'notD' and kb + 'C' not in inst.V: seen[kb] = (r, cb)
with open(OUT, 'w') as fo:
    for kb, (r, cb) in sorted(seen.items(), key=lambda x: x[1][0]): fo.write('%s %s\n' % (kb, cb))
print(len(seen), 'configs')
