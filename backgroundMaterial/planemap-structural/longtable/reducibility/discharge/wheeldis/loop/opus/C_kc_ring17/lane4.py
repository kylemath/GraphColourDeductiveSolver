"""C_kc_ring17 lane: pull windows from queue.txt in order (shared index under flock), run kc on each (Gauss-Seidel,
checkpointed), append 'name ring verdict-line | rss wall' to results.txt.  Usage: python3 lane.py LANE.  Touch STOP to halt."""
import sys, os, fcntl, subprocess, resource, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BUD = {6: 60, 7: 60, 8: 60, 9: 60, 10: 120, 11: 120, 12: 300, 13: 300, 14: 300, 15: 600, 16: 900, 17: 1200, 18: 1800, 19: 2700, 20: 3600}
while not os.path.exists('STOP4'):
    Q = open('queue3.txt').read().splitlines()
    with open('queue.lock', 'a+') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        i = int(open('next3.idx').read()) if os.path.exists('next3.idx') else 0
        open('next3.idx', 'w').write(str(i + 1))
    if i >= len(Q): break
    line = Q[i]; nm, r = line.split()[0], int(line.split()[1]); tag = 'y%04d' % i
    open('runs/%s.txt' % tag, 'w').write(line + '\n')
    l20 = open('r20.lock', 'a+')
    if r >= 20: fcntl.flock(l20, fcntl.LOCK_EX)
    t = time.time()
    p = subprocess.Popen(['nice', '-n', '5', './kc', '-v', '-c', 'runs/%s.ckpt' % tag, '-t', str(BUD[r]), 'runs/%s.txt' % tag],
                         stdout=open('runs/%s.out' % tag, 'w'), stderr=open('runs/%s.log' % tag, 'w'))
    _, st, ru = os.wait4(p.pid, 0)
    l20.close()
    out = open('runs/%s.out' % tag).read().strip().replace('\n', ' ; ')
    with open('results3.txt', 'a') as f:
        f.write('%s %s r=%d lane=%s | %s | rss_MB=%.0f wall_s=%.0f\n' % (tag, nm, r, sys.argv[1], out or 'NO-OUTPUT(budget?)', ru.ru_maxrss / 1024, time.time() - t))
