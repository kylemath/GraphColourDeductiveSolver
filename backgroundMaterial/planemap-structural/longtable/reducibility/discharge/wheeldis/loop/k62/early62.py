"""EXPLORE round 62: early close for loop/k56/q56.py (rule of 11:26Z).  Watches the queue log; when the running row has a
two-engine kill in loop/k47/KILL and every one of its ring <= 13 windows is done, stops the queue's session, runs minkill47
on what is done, marks the row closed (R56_<P>.DONE) and restarts the queue, which skips closed rows.  Leaves the queue
alone while a row is closing by itself.
usage: python3 early62.py QLOG ROWS SID   (QLOG, ROWS relative to loop/k62; SID = the running queue's session id)"""
import sys, os, re, time, subprocess, signal
H = os.path.dirname(os.path.abspath(__file__)); K47 = os.path.join(H, '..', 'k47')
QLOG, ROWS, SID = os.path.join(H, sys.argv[1]), sys.argv[2], int(sys.argv[3])
now = lambda: time.strftime('%H:%MZ', time.gmtime())
def say(s):
    with open(QLOG, 'a') as f: f.write('%s %s\n' % (now(), s))
def alive(sid):
    ps = subprocess.run(['ps', '-eo', 'sid'], capture_output=True, text=True).stdout.split()
    return str(sid) in ps
while alive(SID):
    time.sleep(60)
    lines = open(QLOG).read().splitlines()
    rows = [l for l in lines if re.match(r'^\d\d:\d\dZ row \S+ \d+ \d+ \d+ - ', l)]
    if not rows: continue
    f = rows[-1].split(); P, D, LK, SV = f[2], f[3], f[4], f[5]
    i0 = max(i for i, l in enumerate(lines) if l == rows[-1])
    if any(l.endswith('row %s closed' % P) for l in lines) or any(' drive ended;' in l for l in lines[i0:]):
        continue
    WL = os.path.join(K47, 'win56_%s_%s_%s_A15.txt' % (D, LK, SV))
    if not os.path.exists(WL): continue
    W = {l.split()[0]: int(l.split()[1]) for l in open(WL) if l.strip()}
    done = {l.split()[0] for l in open(os.path.join(K47, 'A_kcc.out')) if l.strip() and not l.startswith(' ')}
    kills = [l.split()[0] for l in open(os.path.join(K47, 'KILL')) if l.split() and l.split()[0] in W and not l.split()[1].startswith('MISMATCH')]
    low = [n for n, r in W.items() if r <= 13]
    if not kills or not all(n in done for n in low): continue
    subprocess.run(['pkill', '-s', str(SID)]); time.sleep(3)
    nd = sum(1 for n in W if n in done)
    say('drive stopped by early62.py: the row has %d kills and its %d ring <= 13 windows are done; ring <= 15 done %d of %d' % (len(kills), len(low), nd, len(W)))
    W16 = 'win45_%s_%s_%s_A16.txt' % (D, LK, SV)
    out = subprocess.run(['python3', 'minkill47.py', W16, LK, P], cwd=K47, capture_output=True, text=True).stdout
    with open(QLOG, 'a') as fl: fl.write(out)
    say('row %s closed' % P); open(os.path.join(K47, 'R56_%s.DONE' % P), 'w').close()
    pr = subprocess.Popen('DNW=3 setsid nohup python3 ../k56/q56.py %s 15 7000 >> %s 2>&1 < /dev/null & echo $!' % (ROWS, QLOG),
                          shell=True, cwd=H, stdout=subprocess.PIPE, text=True)
    pr.stdout.read(); time.sleep(5)
    ps = subprocess.run(['ps', '-eo', 'sid,args'], capture_output=True, text=True).stdout.splitlines()
    q = [int(l.split()[0]) for l in ps if 'q56.py %s ' % ROWS in l and 'python3' in l]
    if not q: say('early62.py: restart failed, no queue found'); break
    SID = q[0]
    say('early62.py: queue restarted, session %d' % SID)
