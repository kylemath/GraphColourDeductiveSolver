#!/usr/bin/env python3
"""Census34 job queue with load-aware parallelism.
usage: runq.py JOBS.txt PROGRESS.log [--max 12] [--low 6]
Each line of JOBS.txt is "ID<TAB>shell command". A job is skipped if ID appears as done in PROGRESS.log (restartable).
Commands run under `nice -n 10` (each command is responsible for its own nice). Target parallelism is --max, dropped to
--low once the 1-min load average has been > 30 for more than 10 minutes, raised again after 10 minutes below 30."""
import sys, os, time, subprocess
jobs_f, prog = sys.argv[1], sys.argv[2]
MAX = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 12
LOW = int(sys.argv[sys.argv.index('--low') + 1]) if '--low' in sys.argv else 6
done = set()
if os.path.exists(prog):
    for l in open(prog):
        p = l.split()
        if len(p) >= 4 and p[2] == 'done': done.add(p[3])
jobs = [l.rstrip('\n').split('\t', 1) for l in open(jobs_f) if l.strip()]
jobs = [j for j in jobs if j[0] not in done]
log = open(prog, 'a', buffering=1)
def say(*a): log.write(time.strftime('%m-%d %H:%M:%S') + ' ' + ' '.join(map(str, a)) + '\n')
target = LOW if os.getloadavg()[0] > 30 else MAX   # load already > 30 at start -> start low
hi_since = lo_since = None
running = {}
say('start', len(jobs), 'jobs; target', target, 'load', round(os.getloadavg()[0], 1))
t0 = time.time(); ndone = 0
while jobs or running:
    la = os.getloadavg()[0]; now = time.time()
    if la > 30: hi_since = hi_since or now; lo_since = None
    else: lo_since = lo_since or now; hi_since = None
    if target == MAX and hi_since and now - hi_since > 600: target = LOW; say('target', LOW, 'load', round(la, 1))
    if target == LOW and lo_since and now - lo_since > 600: target = MAX; say('target', MAX, 'load', round(la, 1))
    for jid, p in list(running.items()):
        rc = p.poll()
        if rc is not None:
            del running[jid]; ndone += 1
            say('done' if rc == 0 else 'FAIL', jid, 'rc=%d' % rc, '%.0fs' % (now - p.t0), 'n=%d left=%d run=%d' % (ndone, len(jobs), len(running)))
    while jobs and len(running) < target:
        jid, cmd = jobs.pop(0); p = subprocess.Popen(cmd, shell=True, executable='/bin/bash'); p.t0 = time.time(); running[jid] = p
    time.sleep(2)
say('ALLDONE', '%.0fs' % (time.time() - t0))
