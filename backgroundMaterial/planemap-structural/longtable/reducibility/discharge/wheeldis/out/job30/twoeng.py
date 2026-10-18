"""Job 30: two-engine filter for explore's window files (loop/k3*/: dfast/dfast18/cfast output, kc output = lines
with 'mode=', kc -C blocks). A window is loaded only if
- D: D=true on dfast/dfast18 and D=true on kc, or
- C: some single X (compared as an edge set) accepted by both engines under conservative admissibility (kc -C2 files are
  ignored): cfast (search, or --fixed X with leftover 0) and kc -C (search, or
  kc -C -x X with leftover 0).
Writes out/job30/k3x_D.out (dfast lines) and out/job30/k3x_C.cfast (cfast blocks), and prints a summary.
Usage: python3 out/job30/twoeng.py [glob ...]   (default loop/k[0-9]*/*: explore's round folders, and k3studio)"""
import sys, os, glob, re, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
pats = sys.argv[1:] or ['loop/k[0-9]*/*']
files = sorted(f for g in pats for f in glob.glob(os.path.join(HERE, g)) if os.path.isfile(f))
BROAD = [f for f in files if 'C2' in os.path.basename(f)]   # kc -C2 (broad admissibility) verdicts: never used (Long Table, 18 Oct)
files = [f for f in files if f not in BROAD]
def nx(x): return None if x is None else frozenset(e.strip() for e in x.strip('{}').split(','))   # X as an edge set
dD, kD, cC = {}, set(), {}; cX = collections.defaultdict(set); kC = collections.defaultdict(set)   # kc -C: every X kc accepts (search or fixed -x)
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
            x = re.search(r'X=(\{[^}]*\})', line); x = nx(x.group(1)) if x else None
            if curkc: kC[cur].add(x)
            else:
                mf = re.search(r'fixed X=(\{[^}]*\}) .*C-REDUCIBLE, leftover bad classes extending after contraction = 0$', line)
                if 'fixed X=' in line and not mf: continue
                xx = nx(mf.group(1)) if mf else x
                cX[cur].add(xx); cC.setdefault(cur, (xx, hdr, line))
        mx = re.match(r'^\s+X=(\{[^}]*\}) adm=yes leftover 0\b', line)   # kc -C -x X: fixed X accepted, leftover 0
        if cur and curkc and mx: kC[cur].add(nx(mx.group(1)))
okD = sorted(n for n in dD if n in kD)
okC = sorted(n for n in cC if cX[n] & kC.get(n, set()))
mism = sorted(n for n in cC if n in kC and not (cX[n] & kC[n]))
open(os.path.join(HERE, 'out', 'job30', 'k3x_D.out'), 'w').write(''.join(dD[n] + '\n' for n in okD))
open(os.path.join(HERE, 'out', 'job30', 'k3x_C.cfast'), 'w').write(''.join('%s\n%s\n' % (cC[n][1], cC[n][2]) for n in okC))
print('broad (kc -C2) files ignored: %s' % ' '.join(os.path.relpath(f, HERE) for f in BROAD))
print('files %d; D both engines %d (dfast-only %d, kc-only %d); C both engines same X %d (X mismatch %d: %s; one engine only %d)' % (
    len(files), len(okD), len(set(dD) - kD), len(kD - set(dD)), len(okC), len(mism), ' '.join(mism[:5]),
    len(set(cC) ^ set(kC))))
