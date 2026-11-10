# s86 (9 Nov 23:10Z, Lead 22:59Z option A): trimmed warm pool for the GS run after GS16, so a GL run and one check fit beside it.
# Keeps (1) the dual support (receiverR2 -> 'R d link apex', cons2 -> 'C L s') of every given lpdual JSON, and (2) every row of the given
# GS-lineage row files (rows the GS separation itself found); drops the older s44..s79 pools.  usage:
#   python3 -I mkwarmtrim.py <out> --dual f1.json,f2.json,... --rows r1.txt,r2.txt,...
import json, re, sys
out = sys.argv[1]; a = dict(zip(sys.argv[2::2], sys.argv[3::2]))
seen, lines, nd, nr = set(), [], 0, 0
def add(l):
    if l not in seen: seen.add(l); lines.append(l); return 1
    return 0
for f in filter(None, a.get('--dual', '').split(',')):
    for e in json.load(open(f)):
        r = e['row']
        if r[0] == 'receiverR2': nd += add('R %d %s %s' % (r[1], r[2], r[3]))
        elif r[0] == 'cons2': nd += add('C %s %s' % (''.join(map(str, r[1])), ''.join(map(str, r[2]))))
for f in filter(None, a.get('--rows', '').split(',')):
    for l in open(f):
        l = l.rstrip('\n')
        if re.match(r'^R \d+ \d+ \d+\s*$', l) or re.match(r'^C [5-9]{6} [5-9]{6}\s*$', l): nr += add(l.strip())
open(out, 'w').write(''.join(l + '\n' for l in lines))
print('mkwarmtrim: %d lines (%d from dual support, %d more from row files) -> %s' % (len(lines), nd, nr, out))
