"""Row 12 addendum (Long Table 20:38Z), the row10_open.py method: the 11 ring-18 windows where kc timed out at -t 600 go
to dfast18 (6 h limit per window). A dfast18 D=true is confirmed by kc -C -s 60 -t 10800 on the same window (a kill
needs both engines). A dfast18 D=false is recorded; no cfast (no kc X). Heavy-slot locks shared with job52.py (poll
5 s, ahead of the 30 s-poll rows 4-9 and 13; slots 0-9); 20 GB memory floor.
Usage: python3 out/job52/row12_open.py NAME [NAME ...]"""
import os, sys, re, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); WD = os.path.abspath(os.path.join(HERE, '..', '..'))
KC = os.path.join(WD, 'loop', 'kc', 'kc'); DF = os.path.join(HERE, 'dfast18')
RD = os.path.join(HERE, 'row_7_7766556_6576576'); SRC = os.path.join(HERE, 'win52_7_7766556_6576576_todo.txt')
LIM = 6 * 3600
def free_gb():
    out = subprocess.run(['vm_stat'], capture_output=True, text=True).stdout
    return int(re.search(r'Pages free:\s+(\d+)', out).group(1)) * int(re.search(r'page size of (\d+)', out).group(1)) / 2 ** 30
def slot():
    os.makedirs(os.path.join(HERE, '.heavy'), exist_ok=True)
    while True:
        for k in range(10):
            p = os.path.join(HERE, '.heavy', 'slot%d' % k)
            try: os.mkdir(p)
            except FileExistsError: continue
            if free_gb() >= 20: return p
            os.rmdir(p)
        time.sleep(5)
lines = {l.split()[0]: l.rstrip('\n') for l in open(SRC) if l.strip()}
out = open(os.path.join(RD, 'open11_results.txt'), 'a')
for nm in sys.argv[1:]:
    safe = re.sub(r'[^A-Za-z0-9_.-]', '_', nm); wf = os.path.join(RD, 'o_%s.in' % safe); open(wf, 'w').write(lines[nm] + '\n')
    t0 = time.time(); lock = slot()
    try:
        with open(os.path.join(RD, 'o_%s.df' % safe), 'w') as fo:
            subprocess.run(['nice', '-n', '10', 'perl', '-e', 'alarm shift; exec @ARGV', str(LIM), DF, wf], stdout=fo, stderr=subprocess.STDOUT)
    finally: os.rmdir(lock)
    d = open(os.path.join(RD, 'o_%s.df' % safe)).read(); dt = time.time() - t0
    v = 'D' if 'D=true' in d else ('notD' if 'D=false' in d else 'timeout')
    line = '%s ring=18 dfast18=%s(%.0fs)' % (nm, v, dt)
    if v == 'D':
        left = max(60, LIM - dt)
        with open(os.path.join(RD, 'o_%s.kc10800' % safe), 'w') as fo:
            subprocess.run(['nice', '-n', '10', 'perl', '-e', 'alarm shift; exec @ARGV', str(int(left)), KC, '-C', '-s', '60', '-t', '10800', wf], stdout=fo, stderr=subprocess.STDOUT)
        k = open(os.path.join(RD, 'o_%s.kc10800' % safe)).read()
        line += ' kc_t10800=%s' % ('D' if 'D=true' in k else ('neither' if 'D=false' in k else 'timeout'))
        if 'D=true' in k: open(os.path.join(RD, 'kills.txt'), 'a').write('%s D dfast18+kc(t10800) ring=18\n' % nm)
    out.write(line + '\n'); out.flush()
