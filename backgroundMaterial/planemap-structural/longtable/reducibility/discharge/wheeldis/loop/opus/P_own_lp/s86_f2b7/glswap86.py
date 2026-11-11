#!/usr/bin/env python3
"""glswap86.py (Opus, 10 Nov 23:45Z): pause the GL lane for the U86 check of a GS22 candidate and arm its relaunch.
usage: python3 -I glswap86.py CAND OLDNUM   (e.g. sol_k86GS22_in05 25 -> stops k86GL25, writes and starts launch_k86GL26.sh)
Snapshot eng_p8l/rows_k86GL<old>.txt -> warm/rows_k86GL<old>_snap_GL<new>.txt (whole lines), kill the old lane, write
launch_k86GL<new>.sh from launch_k86GL<old>.sh (wait for the s86U line of CAND, warm += the snapshot, new tag), start it."""
import sys, os, re, subprocess, time
N = os.path.dirname(os.path.abspath(__file__)); CAND, old = sys.argv[1], int(sys.argv[2]); new = old + 1
O, W = 'k86GL%d' % old, 'k86GL%d' % new
src = open(os.path.join(N, 'launch_%s.sh' % O)).read()
b = open(os.path.join(N, 'eng_p8l', 'rows_%s.txt' % O), 'rb').read(); b = b[:b.rfind(b'\n') + 1]
snap = 'rows_%s_snap_GL%d.txt' % (O, new); open(os.path.join(N, 'warm', snap), 'wb').write(b); nl = b.count(b'\n')
log = open(os.path.join(N, 'runK_%s' % O, 'K.log')).read(); it = re.findall(r'lext it (\d+): phase 1 \(t alone\) t1 = ([-0-9.e]+)', log)
itd = 'lext it %s, t1 = %s' % (it[-1][0], it[-1][1].replace('-0.000000000000', '0')) if it else 'in setup'
ps = subprocess.run(['ps', '-eo', 'pid,args'], capture_output=True, text=True).stdout.splitlines()[1:]
pids = [l.split()[0] for l in ps if re.search(r'(tag=%s |launch_%s\.sh| %s( |$))' % (O, O, O), l) and 'glswap86' not in l]
subprocess.run(['kill'] + pids); time.sleep(3)
t = src
prev = re.search(r'k86GL\((\d+)\|%d\) ' % old, t).group(1)
t = t.replace('k86GL(%s|%d) ' % (prev, old), 'k86GL(%d|%d) ' % (old, new)).replace('GL%s/GL%d running' % (prev, old), 'GL%d/GL%d running' % (old, new))
t = t.replace('launch_%s' % O, 'launch_%s' % W)
t = re.sub(r'sol_k86GS22_in\d\d', CAND, t)
L = t.split('\n')
for i, l in enumerate(L):
    if l.startswith('export WARM='): L[i] = l + ',$N/warm/' + snap
    elif l.startswith(('nohup ', 'cd $N', 'sleep 2; echo')): L[i] = l.replace(O, W)
t = '\n'.join(L)
t = re.sub(r'after the GS22 in\d\d check', 'after the GS22 %s check' % CAND[-4:], t)
t = re.sub(r'GL17-\d+ rows', 'GL17-%d rows' % old, t)
hdr = '# s86: %s (%s) = %s relaunched after the U86 check of %s (%s stopped at %s, for memory); warm += %s.  glswap86.py\n' % (
    W, time.strftime('%d %b %H:%MZ', time.gmtime()), O, CAND, O, itd, snap)
lf = os.path.join(N, 'launch_%s.sh' % W); open(lf, 'w').write(hdr + t)
assert subprocess.run(['bash', '-n', lf]).returncode == 0
assert t.count(W) >= 6 and snap in t and CAND in t and O not in t.split('export WARM=')[1].split('\n')[1:3][0]
open(os.path.join(N, 'run.log'), 'a').write('%s [s86G] stopped %s (%s; rows -> warm/%s, %d lines) for the U86 check of %s; launch_%s.sh armed (glswap86.py)\n' % (
    time.strftime('%H:%M:%SZ', time.gmtime()), O, itd, snap, nl, CAND, W))
subprocess.Popen('nohup bash %s > %s/logs/launch_%s.out 2>&1 &' % (lf, N, W), shell=True, cwd=N)
print('stopped', O, itd, 'pids', pids, '; armed', lf)
