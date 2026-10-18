"""EXPLORE round 34 part C driver: kc over fill.txt in ring order, 3 workers, skipping any window whose fillings are
all killed already.  A kc D is re-run at once on dfast (ring <= 16) or dfast18 (17-19); a filling counts as killed
only when both engines say D.  Every 4th not-D window at ring <= 16 also gets dfast (agreement check).
usage: python3 drive.py fill.txt RMAX TSEC   -> fill_kc.out, fill_df.out, fill_state.txt"""
import sys, os, subprocess, threading, time
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__))
FN, RMAX, TSEC = sys.argv[1], int(sys.argv[2]), sys.argv[3]
lines = [l.rstrip('\n') for l in open(FN)]
cov = {}
for l in open(FN + '.cov'):
    f = l.split(); cov[f[0]] = set(f[2:])
killed, lock = set(), threading.Lock()
outk, outd = open(os.path.join(H, 'fill_kc.out'), 'a'), open(os.path.join(H, 'fill_df.out'), 'a')
done = set()
for fn in ('fill_kc.out',):                      # resume: windows already run
    for l in open(os.path.join(H, fn)):
        if ' r=' in l: done.add(l.split()[0])
for l in open(os.path.join(H, 'fill_df.out')):
    pass
def run(cmd, line):
    p = subprocess.run(cmd, input=line + '\n', capture_output=True, text=True)
    return p.stdout.strip()
nk = [0]
def work(i, line):
    nm, r = line.split()[0], int(line.split()[1])
    with lock:
        if cov[nm] <= killed: return
    t = time.time()
    o = run([os.path.join(H, '..', 'kc', 'kc', ), '-s', '60', '-t', TSEC], line)
    with lock: outk.write(o + '\n'); outk.flush()
    isD = 'D=true' in o
    if isD or (r <= 16 and i % 4 == 0):
        df = os.path.join(H, '..', '..', 'bin', 'dfast' if r <= 16 else 'dfast18')
        o2 = run([df, '/dev/stdin'], line)
        with lock:
            outd.write(o2 + '\n'); outd.flush()
            kD, dD = isD, 'D=true' in o2
            if kD != dD: outd.write('# MISMATCH ' + nm + '\n'); outd.flush()
            if kD and dD: killed.update(cov[nm])
    with lock:
        st = open(os.path.join(H, 'fill_state.txt'), 'w')
        st.write('killed %d of 25: %s\n' % (len(killed), ' '.join(sorted(killed)))); st.close()
with ThreadPoolExecutor(int(os.environ.get('NW', '3'))) as ex:
    for i, line in enumerate(lines):
        nm, r = line.split()[0], int(line.split()[1])
        if r > RMAX or nm in done: continue
        ex.submit(work, i, line)
print('killed', len(killed), sorted(killed))
