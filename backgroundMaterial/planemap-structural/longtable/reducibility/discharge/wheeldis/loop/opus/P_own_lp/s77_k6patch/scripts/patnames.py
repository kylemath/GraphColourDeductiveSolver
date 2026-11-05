"""s77: pattern NAMES by kind for an args file, with the pcheck.py load_patterns rules (pat=: 'D=true' lines named ^[epf]\\d+_; cpat=: C-REDUCIBLE names),
C filtered either by exname (ours: drop held-out names) or by a keep list (Studio CKEEP: keep only listed names).
usage: patnames.py ARGS (exname=FILE | ckeep=FILE) OUTPREFIX   -> OUTPREFIX_D.txt / _C.txt and counts"""
import sys, re, os
args = open(sys.argv[1]).read().split(); mode, fl = sys.argv[2].split('=', 1); out = sys.argv[3]
L = set(l.split()[0] for l in open(fl) if l.strip() and not l.startswith('#'))
D, C, Call = set(), set(), set()
for a in args:
    if not a.startswith(('pat=', 'cpat=')): continue
    p = a.split('=', 1)[1]
    if a.startswith('pat='):
        for line in open(p):
            if line.strip() and 'D=true' in line and re.match(r'^[epf]\d+_', line): D.add(line.split()[0])
    else:
        cur = None
        for line in open(p):
            if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
            elif 'C-REDUCIBLE' in line and cur and re.match(r'^[epf]\d+_', cur):
                Call.add(cur)
                if (mode == 'exname' and cur not in L) or (mode == 'ckeep' and cur in L): C.add(cur)
for k, S in (('D', D), ('C', C)): open('%s_%s.txt' % (out, k), 'w').write(''.join(n + '\n' for n in sorted(S)))
print('%s: D names %d, C-REDUCIBLE names %d, C kept (%s) %d' % (os.path.basename(out), len(D), len(Call), mode, len(C)))
