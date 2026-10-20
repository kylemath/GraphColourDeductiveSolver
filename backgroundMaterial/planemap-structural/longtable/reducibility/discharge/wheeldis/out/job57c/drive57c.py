"""Job 57c (Long Table 20 Oct 18:54Z): the d10 binder 6565665656/6556565565 window file (win52_10_..._todo.txt, 3b6b0676,
md5 31a7d98e), ring-15 windows then ring-16 (run_r1516.txt, file order); rings 17-18 held (held_r1718.txt). Studio engines, drive45 output format, STOP=0, nice 15. A ring >= 17 dfast18 / cfast call waits for
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
for i, line in enumerate(lines):
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
