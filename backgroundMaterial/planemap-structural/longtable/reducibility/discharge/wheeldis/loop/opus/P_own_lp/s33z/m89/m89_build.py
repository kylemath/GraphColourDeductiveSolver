"""m89: drop the 89 CGLUE-XRING C entries (list file) from a k3x_C cfast.  usage: python3 m89_build.py LIST IN.cfast OUT.cfast"""
import sys
N = set(l.split()[0] for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')); assert len(N) == 89
out = []; cur = None; drop = set()
for line in open(sys.argv[2]):
    if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
    if cur in N: drop.add(cur); continue
    out.append(line)
open(sys.argv[3], 'w').writelines(out)
print('dropped', len(drop), 'of 89; not found', sorted(N - drop), '; C entries left', sum(1 for l in out if ' r=' in l and not l.startswith(' ')))
