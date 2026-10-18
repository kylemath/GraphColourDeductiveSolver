"""Sequential kc driver over win.txt (ring order), one core. Skips windows whose fillings are all killed or whose
verdict is known (known.txt). kc D at ring <= 16 is re-checked with A's dfast. usage: python3 drive.py RMAX"""
import sys, os, subprocess, time
H = os.path.dirname(os.path.abspath(__file__)); RMAX = int(sys.argv[1])
DF = os.path.join(H, '..', 'A_rsst_defects', 'bin', 'dfast')
lines = [l.rstrip('\n') for l in open(os.path.join(H, 'win.txt'))]
cov = {l.split()[0]: set(l.split()[2:]) for l in open(os.path.join(H, 'win.txt.cov'))}
known = {}
for fn in ('known.txt', 'win_kc.out'):
    p = os.path.join(H, fn)
    if os.path.exists(p):
        for l in open(p):
            if 'D=' in l: known[l.split()[0]] = 'D=true' in l
killed = set().union(*[cov[n] for n, v in known.items() if v and n in cov]) if any(known.values()) else set()
out = open(os.path.join(H, 'win_kc.out'), 'a'); dfo = open(os.path.join(H, 'win_dfast.out'), 'a')
for line in lines:
    nm, r = line.split()[0], int(line.split()[1])
    if r > RMAX or nm in known or cov[nm] <= killed: continue
    o = subprocess.run([os.path.join(H, 'kc'), '/dev/stdin'], input=line + '\n', capture_output=True, text=True).stdout.strip()
    out.write(o + '\n'); out.flush()
    if 'D=true' in o:
        if r <= 16:
            o2 = subprocess.run([DF, '/dev/stdin'], input=line + '\n', capture_output=True, text=True).stdout.strip()
            dfo.write(o2 + '\n'); dfo.flush()
            if 'D=true' not in o2: dfo.write('# MISMATCH %s\n' % nm); continue
        killed |= cov[nm]
    open(os.path.join(H, 'state.txt'), 'w').write('%s last=%s r=%d killed %d/16: %s\n' % (time.strftime('%H:%M:%S'), nm, r, len(killed), ' '.join(sorted(killed))))
print('done killed', sorted(killed))
