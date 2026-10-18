"""EXPLORE round 43 part A driver: kc -C over FILE in file order (ring order) on NW workers, resuming from A_kcc.out.
A kc D is re-run on dfast (ring <= 16) or dfast18; a kc C goes to cfast --fixed with kc's conservative X.  The first
window that is D on both engines, or C with kc's X accepted by cfast (leftover 0), is written to KILL and no new
window starts (STOP=0: record every kill and go on; a mismatch still stops).  Every 4th not-D window at ring <= 14 also gets dfast (agreement).  usage: NW=3 python3 drive43.py FILE TSEC"""
import sys, os, re, subprocess, threading, tempfile
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(H, '..', '..', 'bin')
FN, TSEC = sys.argv[1], sys.argv[2]
lines = [l.rstrip('\n') for l in open(FN) if l.strip()]
KO, DO, CO = (os.path.join(H, x) for x in ('A_kcc.out', 'A_df.out', 'A_cf.out'))
done = {l.split()[0] for l in open(KO) if l.strip() and not l.startswith(' ')} if os.path.exists(KO) else set()
lock = threading.Lock(); stop = threading.Event()
outk, outd, outc = open(KO, 'a'), open(DO, 'a'), open(CO, 'a')
def run(cmd, inp=None):
    return subprocess.run(cmd, input=inp, capture_output=True, text=True).stdout.rstrip('\n')
def kill(nm, why):
    with lock:
        open(os.path.join(H, 'KILL'), 'a').write('%s %s\n' % (nm, why))
        if os.environ.get('STOP', '1') == '1' or why.startswith('MISMATCH'): stop.set()
def work(i, line):
    if stop.is_set(): return
    nm, r = line.split()[0], int(line.split()[1])
    o = run([os.path.join(H, '..', 'kc', 'kcc'), '-C', '-s', '60', '-t', TSEC], line + '\n')
    with lock: outk.write(o + '\n'); outk.flush()
    isD = 'D=true' in o.split('\n')[0]
    if isD or (r <= 14 and i % 4 == 0):
        o2 = run([os.path.join(B, 'dfast' if r <= 16 else 'dfast18'), '/dev/stdin'], line + '\n')
        with lock:
            outd.write(o2 + '\n'); outd.flush()
            if isD != ('D=true' in o2): outd.write('# MISMATCH ' + nm + '\n'); outd.flush(); kill(nm, 'MISMATCH kc/dfast')
        if isD and 'D=true' in o2: kill(nm, 'D kc+dfast')
    m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', o)
    if m:
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as t: t.write(line + '\n')
        o3 = run([os.path.join(B, 'cfast'), t.name, '--fixed', m.group(1)]); os.unlink(t.name)
        with lock: outc.write(o3 + '\n'); outc.flush()
        if 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in o3: kill(nm, 'C kc-X {%s} + cfast fixed' % m.group(1))
        else:
            with lock: outc.write('# CFAST REJECTS kc X for ' + nm + '\n'); outc.flush()
with ThreadPoolExecutor(int(os.environ.get('NW', '3'))) as ex:
    for i, line in enumerate(lines):
        if line.split()[0] in done: continue
        ex.submit(work, i, line)
open(os.path.join(H, 'A.DONE'), 'w').write('stopped' if stop.is_set() else 'complete')
