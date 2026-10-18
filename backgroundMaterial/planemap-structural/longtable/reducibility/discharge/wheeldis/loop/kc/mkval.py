"""Round 33 validation set: config lines joined with their dfast verdicts, by a fixed rule (every k-th config line).
Usage: python3 mkval.py > val.txt ; writes val.txt (configs) and val_dfast.txt (dfast lines, same order)."""
import os
H = os.path.dirname(os.path.abspath(__file__)); L = os.path.dirname(H); DIS = os.path.dirname(os.path.dirname(L))
SRC = [  # (config file, dfast output, every k-th line)
    (os.path.join(L, 'n9', 'win9_r14.txt'), os.path.join(L, 'n9', 'win9.out'), 10),
    (os.path.join(L, 'n9', 'win25.txt'), os.path.join(L, 'n9', 'win25.out'), 5),
    (os.path.join(L, 'n9', 'win27.txt'), os.path.join(L, 'n9', 'win27.out'), 2),
    (os.path.join(L, 'n9', 'win31.txt'), os.path.join(L, 'n9', 'win31.out'), 3),
]
conf, ver = [], []
for cf, of, k in SRC:
    V = {l.split()[0]: l.strip() for l in open(of) if ' r=' in l}
    lines = [l.strip() for l in open(cf) if l.strip()]
    for i, l in enumerate(lines):
        if i % k == 0 and l.split()[0] in V: conf.append(l); ver.append(V[l.split()[0]])
open(os.path.join(H, 'val.txt'), 'w').write('\n'.join(conf) + '\n')
open(os.path.join(H, 'val_dfast.txt'), 'w').write('\n'.join(ver) + '\n')
nd = sum('D=false' in v for v in ver)
rings = sorted(set(int(v.split()[1][2:]) for v in ver))
print('validation keys %d (not D %d), rings %s' % (len(ver), nd, rings))
