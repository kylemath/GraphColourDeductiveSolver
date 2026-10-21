"""tc3 (Long Table via coordinator 21 Oct 05:36Z): second engine on loop/formal/tc3/tc3_all.txt (cab53be1, 200ef572): close18 pattern,
kc -C -s 60 -t 600 (KCPAR at once, nice 10) and dfast18 (one at a time, waiting for >= 30 GB free). Rule: D counts iff dfast18 D and kc D;
C counts iff kc X and cfast --fixed X leftover 0. drive45-format outputs A_kcc.out, A_df.out, A_cf.out, KILL, done.txt.
Usage: python3 close18.py windows.txt"""
import os, sys, re, subprocess, threading, time
H = os.path.dirname(os.path.abspath(__file__)); WD = os.path.abspath(os.path.join(H, '..', '..'))
KC = os.path.join(WD, 'loop', 'kc', 'kc'); DF = os.path.join(WD, 'out', 'job52', 'dfast18'); CF = os.path.join(WD, '..', 'studio15', 'cfast')
lines = [l.rstrip('\n') for l in open(sys.argv[1]) if l.strip()]; lock = threading.Lock(); dflock = threading.Lock()
KCSEM = threading.Semaphore(int(os.environ.get('KCPAR', '3')))   # at most KCPAR kc -t 10800 at once (budget)
def free_gb():
    o = subprocess.run(['vm_stat'], capture_output=True, text=True).stdout
    return int(re.search(r'Pages free:\s+(\d+)', o).group(1)) * int(re.search(r'page size of (\d+)', o).group(1)) / 2 ** 30
def run(cmd): return subprocess.run(['nice', '-n', '10'] + cmd, capture_output=True, text=True).stdout.rstrip('\n')
def out(fn, s):
    with lock: open(os.path.join(H, fn), 'a').write(s + '\n')
def work(line):
    nm = line.split()[0]; tf = os.path.join(H, 'w_%s.in' % re.sub(r'[^A-Za-z0-9_.-]', '_', nm)); open(tf, 'w').write(line + '\n')
    res = {}
    def kc():
        with KCSEM: res['kc'] = run([KC, '-C', '-s', '60', '-t', '600', tf]); out('A_kcc.out', res['kc'])
    def df():
        with dflock:
            while free_gb() < 30: time.sleep(20)
            res['df'] = run([DF, tf]); out('A_df.out', res['df'])
    a = threading.Thread(target=kc); b = threading.Thread(target=df); a.start(); b.start(); a.join(); b.join()
    kD = 'D=true' in res['kc'].split('\n')[0]; dD = 'D=true' in res['df']
    m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', res['kc']); v = None
    if kD and dD: v = 'D kc(t600)+dfast18'
    elif m:
        o3 = run([CF, tf, '--fixed', m.group(1)]); out('A_cf.out', o3)
        if 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in o3: v = 'C kc-X {%s} + cfast fixed' % m.group(1)
    if v: out('KILL', '%s %s ring=%s' % (nm, v, line.split()[1]))
    kcv = 'D' if kD else ('C' if m else ('timeout' if 'D=' not in res['kc'] else 'neither'))
    out('done.txt', '%s kc(t600)=%s dfast18=%s%s' % (nm, kcv, 'D' if dD else ('notD' if 'D=false' in res['df'] else 'none'), ' KILL' if v else ''))
    os.remove(tf)
TAG = os.environ.get('TAG', 'A')
ts = [threading.Thread(target=work, args=(l,)) for l in lines]
for t in ts: t.start()
for t in ts: t.join()
open(os.path.join(H, TAG + '.DONE'), 'w').write('complete\n')
