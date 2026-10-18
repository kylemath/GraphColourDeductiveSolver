"""Round 38 kills: rebuild each window's input line (frame coordinates from greedy.out), then evaluate cfast's X on kc
(kc -C -x) so both engines are checked on one X.  Writes kills.txt (input lines), kills_x.txt, kills_cfastX.kc."""
import os, re, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.normpath(os.path.join(H, '..', '..'))
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
sys.argv = ['gen28.py', '/dev/null', '24']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
txt = open(os.path.join(H, 'greedy.out')).read()
kills = re.findall(r'^  C2 (\S+) ring (\d+) \(link (\S+) s (\S+)\)', txt, re.M)
cx = dict(re.findall(r'^     cfast: (\S+) r=.*\n     cfast:   C-REDUCIBLE with X=(\{[^}]*\})', txt, re.M))
lines, xs = [], []
for nm, r, L, S in kills:
    w = [int(c) if c != '.' else None for c in L]; s = [int(c) if c != '.' else None for c in S]
    line = G['make'](7, int(r), None, w, s, nm); assert line and line.split()[0] == nm, (nm, line)
    lines.append(line); xs.append('%s %s' % (nm, cx[nm]))
open(os.path.join(H, 'kills.txt'), 'w').write('\n'.join(lines) + '\n')
open(os.path.join(H, 'kills_x.txt'), 'w').write('\n'.join(xs) + '\n')
o = subprocess.run([os.path.join(H, '..', 'kc', 'kcc'), '-C', '-x', os.path.join(H, 'kills_x.txt')], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout
open(os.path.join(H, 'kills_cfastX.kc'), 'w').write(o); print(o)
