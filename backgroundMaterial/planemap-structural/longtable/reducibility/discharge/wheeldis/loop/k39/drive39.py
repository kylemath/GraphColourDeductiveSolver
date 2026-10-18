"""EXPLORE round 39 driver (copy of round 37 drive37.py; targets = open fillings from the .cov file): kc -C over p5.txt in
ring order, NW workers, skipping any window whose targets are all killed already.  Per window: D-closure, then (if not D) the round-35 C stage.
- A kc D is re-run at once on dfast (ring <= 16) or dfast18 (17-19); the filling is killed 'D2' only if both say D.
- A kc-C C kills its fillings as 'C1' (one engine; cfast at Studio is the second).
- Every 4th not-D window at ring <= 16 also gets dfast (agreement check).
Per-target table: targets.txt (target x2x3x4, status, window).  Resumes from fill_kcc.out.
usage: NW=1 python3 drive39.py p5.txt RMAX TSEC"""
import sys, os, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__))
FN, RMAX, TSEC = sys.argv[1], int(sys.argv[2]), sys.argv[3]
lines = [l.rstrip('\n') for l in open(FN)]
cov = {}
for l in open(FN + '.cov'):
    f = l.split(); cov[f[0]] = f[2:]
FILL = sorted({t for v in cov.values() for t in v})
status, lock = {}, threading.Lock()          # filling -> (status, window)
KO, DO = os.path.join(H, 'fill_kcc.out'), os.path.join(H, 'fill_df.out')
done, blocks, cur = set(), {}, None
if os.path.exists(KO):
    for l in open(KO):
        if not l.startswith(' '): cur = l.split()[0]; done.add(cur); blocks[cur] = [l]
        elif cur: blocks[cur].append(l)
dfD = {}
if os.path.exists(DO):
    for l in open(DO):
        if ' r=' in l: dfD[l.split()[0]] = 'D=true' in l
def mark(nm, st):
    for f in cov[nm]:
        old = status.get(f)
        if old is None or (old[0] == 'C1' and st == 'D2'): status[f] = (st, nm)
for nm, b in blocks.items():                 # rebuild state from a resumed run
    if 'D=true' in b[0] and dfD.get(nm): mark(nm, 'D2')
    if any('C-REDUCIBLE' in x for x in b): mark(nm, 'C1')
outk, outd = open(KO, 'a'), open(DO, 'a')
def table():
    with open(os.path.join(H, 'targets.txt'), 'w') as t:
        t.write('# R* + p5 = 7: open fillings (s1 s4): D2 = D on kc and dfast/dfast18, C1 = C on kc-C only, open\n')
        for f in FILL:
            s = status.get(f); t.write('%s %s %s\n' % (f, s[0] if s else 'open', s[1] if s else '-'))
        t.write('# killed %d of %d (D2 %d, C1 %d)\n' % (len(status), len(FILL), sum(1 for v in status.values() if v[0] == 'D2'),
                                                       sum(1 for v in status.values() if v[0] == 'C1')))
def run(cmd, line):
    return subprocess.run(cmd, input=line + '\n', capture_output=True, text=True).stdout.rstrip('\n')
def work(i, line):
    nm, r = line.split()[0], int(line.split()[1])
    with lock:
        if all(f in status for f in cov[nm]): return
    o = run([os.path.join(H, '..', 'kc', 'kcc'), '-C', '-s', '60', '-t', TSEC], line)
    with lock: outk.write(o + '\n'); outk.flush()
    isD = 'D=true' in o.split('\n')[0]
    if isD or (r <= 16 and i % 4 == 0):
        df = os.path.join(H, '..', '..', 'bin', 'dfast' if r <= 16 else 'dfast18')
        o2 = run([df, '/dev/stdin'], line)
        with lock:
            outd.write(o2 + '\n'); outd.flush()
            if isD != ('D=true' in o2): outd.write('# MISMATCH ' + nm + '\n'); outd.flush()
            if isD and 'D=true' in o2: mark(nm, 'D2')
    if 'C-REDUCIBLE' in o:
        with lock: mark(nm, 'C1')
    with lock: table()
table()
with ThreadPoolExecutor(int(os.environ.get('NW', '3'))) as ex:
    for i, line in enumerate(lines):
        nm, r = line.split()[0], int(line.split()[1])
        if r > RMAX or nm in done: continue
        ex.submit(work, i, line)
print('killed', len(status), sorted(status.items()))
