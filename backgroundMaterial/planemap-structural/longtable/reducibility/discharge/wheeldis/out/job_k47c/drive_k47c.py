"""Job k47 (explore / Long Table via coordinator 21 Oct 07:30Z): row 7676655/6667656 (k47c, explore via coordinator 21 Oct 09:02Z, low priority),
win52_7_7676655_6667656_todo.txt (4360edda, md5 6794f7c7; 622 kc lines: 304 r16, 189 r17, 129 r18; file order), stop at the first
two-engine kill (STOPKILL=1). dfast18 confirms every kc D (rings 16-18; it is the only dfast build here, ring <= 19). twoeng
ring-merge guard on C: a kc X whose union-find component holds >= 2 ring vertices is HELD (not a kill), cfast not called.
From job57e: Copied from nl54e: Job nl54e (Long Table 20 Oct 08:46Z): the ring-15 remainder of the 2026 8,202 set (nl54d_r15rest_rev.txt, 2e2081df,
md5 4c5cd863, 1,535 kc lines, run in file order), Studio engines, drive45 output format, STOP=0, nice 15. A ring >= 17 dfast18 / cfast call waits for
>= 30 GB free (20 GB floor + one heavy call). NW.txt may be 0 (wait for a slot).
Copied from out/job54s/drive54s.py: Per window in file order: loop/kc/kc -C -s 60 -t 600 -> A_kcc.out; kc D ->
out/job52/dfast18 -> A_df.out (kill if D); kc C X -> studio15/cfast --fixed X -> A_cf.out (kill if leftover 0, else a
'# CFAST REJECTS' line). Kills -> KILL ('name D kc+dfast18' / 'name C kc-X {X} + cfast fixed'). No other engine runs.
Resumes from A_kcc.out. The number of concurrent windows is read from NW.txt before each window starts (default 3), so
slots can be added as other jobs finish. Usage: python3 out/job54s/drive54s.py FILE"""
import sys, os, re, subprocess, threading, tempfile, time
H = os.path.dirname(os.path.abspath(__file__)); WD = os.path.abspath(os.path.join(H, '..', '..'))
KC = os.path.join(WD, 'loop', 'kc', 'kc'); DF = os.path.join(WD, 'out', 'job52', 'dfast18'); CF = os.path.join(WD, '..', 'studio15', 'cfast')
FN = sys.argv[1]; lines = [l.rstrip('\n') for l in open(FN) if l.strip()]
KO, DO, CO = (os.path.join(H, x) for x in ('A_kcc.out', 'A_df.out', 'A_cf.out'))
done = {l.split()[0] for l in open(KO) if l.strip() and not l.startswith(' ') and ' r=' in l} if os.path.exists(KO) else set()
lock = threading.Lock(); outk, outd, outc = open(KO, 'a'), open(DO, 'a'), open(CO, 'a'); active = [0]
def nw():
    try: return max(0, int(open(os.path.join(H, 'NW.txt')).read().strip()))
    except Exception: return 0
def run(cmd):
    return subprocess.run(['nice', '-n', '15'] + cmd, capture_output=True, text=True).stdout.rstrip('\n')
def free_gb():
    o = subprocess.run(['vm_stat'], capture_output=True, text=True).stdout
    return int(re.search(r'Pages free:\s+(\d+)', o).group(1)) * int(re.search(r'page size of (\d+)', o).group(1)) / 2 ** 30
def memgate(ring):
    while ring >= 17 and free_gb() < 30: time.sleep(20)
def ringmerge(x):   # twoeng guard: union-find on X; a component with >= 2 ring vertices merges ring vertices
    par = {}
    def fd(a):
        while par.setdefault(a, a) != a: a = par[a]
        return a
    for e in x:
        a, b = e.strip().split('-'); par[fd(a)] = fd(b)
    import collections as _c
    return max(_c.Counter(fd(v) for v in par if v.startswith('R')).values(), default=0) >= 2
def kill(nm, why):
    with lock: open(os.path.join(H, 'KILL'), 'a').write('%s %s\n' % (nm, why))
def work(i, line):
    try:
        nm = line.split()[0]
        with tempfile.NamedTemporaryFile('w', suffix='.in', dir=H, delete=False) as t: t.write(line + '\n'); tf = t.name
        o = run([KC, '-C', '-s', '60', '-t', '600', tf])
        with lock: outk.write(o + '\n'); outk.flush()
        if 'D=true' in o.split('\n')[0]:
            memgate(int(line.split()[1])); o2 = run([DF, tf])
            with lock: outd.write(o2 + '\n'); outd.flush()
            if 'D=true' in o2: kill(nm, 'D kc+dfast18')
        else:
            m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', o)
            if m and ringmerge(m.group(1).split(',')):
                with lock: outc.write('# RINGMERGE HOLD kc X {%s} for %s\n' % (m.group(1), nm)); outc.flush()
                m = None
            if m:
                memgate(int(line.split()[1])); o3 = run([CF, tf, '--fixed', m.group(1)])
                with lock: outc.write(o3 + '\n'); outc.flush()
                if 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in o3: kill(nm, 'C kc-X {%s} + cfast fixed' % m.group(1))
                else:
                    with lock: outc.write('# CFAST REJECTS kc X for ' + nm + '\n'); outc.flush()
        os.unlink(tf)
        with lock: open(os.path.join(H, 'progress.txt'), 'a').write('%d %s\n' % (i + 1, nm))
    finally:
        with lock: active[0] -= 1
STOPKILL = os.environ.get('STOPKILL') == '1'   # stop starting windows at the first two-engine kill
for i, line in enumerate(lines):
    if STOPKILL and os.path.exists(os.path.join(H, 'KILL')) and os.path.getsize(os.path.join(H, 'KILL')) > 0: break
    if line.split()[0] in done: continue
    while True:
        with lock:
            if active[0] < nw(): active[0] += 1; break
        time.sleep(2)
    threading.Thread(target=work, args=(i, line), daemon=False).start()
while True:
    with lock:
        if active[0] == 0: break
    time.sleep(5)
open(os.path.join(H, 'A.DONE'), 'w').write('complete\n')
