"""Job 30: two-engine filter for explore's window files (loop/k3*/: dfast/dfast18/cfast output, kc output = lines
with 'mode=', kc -C blocks). A window is loaded only if
- D: D=true on dfast/dfast18 and D=true on kc, or
- C: C-REDUCIBLE on cfast and C-REDUCIBLE on kc -C, with the same X.
Writes out/job30/k3x_D.out (dfast lines) and out/job30/k3x_C.cfast (cfast blocks), and prints a summary.
Usage: python3 out/job30/twoeng.py [glob ...]   (default loop/k3*/*)"""
import sys, os, glob, re, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
pats = sys.argv[1:] or ['loop/k3*/*']
files = sorted(f for g in pats for f in glob.glob(os.path.join(HERE, g)) if os.path.isfile(f))
dD, kD, cC, kC = {}, set(), {}, {}
for fn in files:
    cur = None; curkc = False; block = []
    try: lines = open(fn).read().splitlines()
    except UnicodeDecodeError: continue
    for line in lines:
        m = re.match(r'^([epf]\d+_\S+) r=\d+ ', line)
        if m:
            cur, curkc = m.group(1), 'mode=' in line
            if 'D=true' in line:
                if curkc: kD.add(cur)
                else: dD.setdefault(cur, line)
            hdr = line; continue
        if cur and 'C-REDUCIBLE' in line:
            x = re.search(r'X=(\{[^}]*\})', line); x = x.group(1) if x else None
            if curkc: kC[cur] = x
            else: cC.setdefault(cur, (x, hdr, line))
okD = sorted(n for n in dD if n in kD)
okC = sorted(n for n in cC if n in kC and kC[n] == cC[n][0])
mism = sorted(n for n in cC if n in kC and kC[n] != cC[n][0])
open(os.path.join(HERE, 'out', 'job30', 'k3x_D.out'), 'w').write(''.join(dD[n] + '\n' for n in okD))
open(os.path.join(HERE, 'out', 'job30', 'k3x_C.cfast'), 'w').write(''.join('%s\n%s\n' % (cC[n][1], cC[n][2]) for n in okC))
print('files %d; D both engines %d (dfast-only %d, kc-only %d); C both engines same X %d (X mismatch %d: %s; one engine only %d)' % (
    len(files), len(okD), len(set(dD) - kD), len(kD - set(dD)), len(okC), len(mism), ' '.join(mism[:5]),
    len(set(cC) ^ set(kC))))
