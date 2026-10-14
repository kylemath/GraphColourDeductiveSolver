"""B8 (exploratory): WheelMain/dfast configurations from a key list.  Usage: mkconf.py KEYFILE RMIN RMAX > configs.txt
KEYFILE lines: 'ring key [count]' (as out/studio-keys.txt)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ball
lo, hi = int(sys.argv[2]), int(sys.argv[3])
for line in open(sys.argv[1]):
    f = line.split()
    if not f or f[0].startswith('#'): continue
    r = int(f[0])
    if lo <= r <= hi: print(ball.fmt_config('k' + f[1], ball.build(ball.key_from_str(f[1]))))
