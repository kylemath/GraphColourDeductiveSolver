"""maclane k5g add-on: the outbox filer of an upper lane on any family (outbox86_k5e.py for suffix e, the same rules for every suffix).
usage: nohup python3 outbox86_fam.py <tag> <suffix> &   (launch_msfam.sh starts it; stop_fam.sh stops it after one last pass:
       python3 outbox86_fam.py <tag> <suffix> once).   env: OUTBOX_UPPER (default <pack>/outbox/upper), OUTBOX_POLL (120 s), REPL_FAM (MW)
A lane point (cand/sol_<tag>_inNN, cand/sol_rep<last 2 of tag><REPL_FAM>_NN, their _tight) is filed once, under the strongest family a
check of exactly this file (same md5) found FEASIBLE: <name>__K3l5<x>.json / .log (in-point check, ladder sub-check, tighten final), or
<name>__K3gB5<x>.json / .log (a ladder point FEASIBLE on the LP family whose K3l5<x> sub-check ended without FEASIBLE; in the last pass
also one whose sub-check never ran).  POINTS.txt gets "<name>__<family>  t  md5  family  <name>__<family>.log  filed-at"; MD5SUMS is
refreshed; one run.log line per point (fam_lib.py outpass).
v2d (Opus 9 Nov): on the lane's key file (its launch line in run.log; k5e_lib.lanekeys), the family names with its label (260 keys:
K3l5<x>_k260 / K3gB5<x>_k260)."""
import os, sys, time
import fam_lib as F

TAG, X = sys.argv[1], sys.argv[2]; ONCE = sys.argv[3:4] == ['once']; POLL = int(os.environ.get('OUTBOX_POLL', '120'))
L = F.K.RunLog()
KB = F.K.lanekeys(TAG); KL = F.K.klabel(KB)


def one_pass():
    res = F.outpass(TAG, X, once=ONCE, L=L.update(), keys=KB)
    for s in res: print('%s %s' % (time.strftime('%H:%M:%SZ', time.gmtime()), s), flush=True)
    return len(res)


if ONCE:
    print('%s: %d point(s) filed (%s / %s, keys %s)' % (TAG, one_pass(), F.qf(X) + KL, F.lf(X) + KL, KB)); sys.exit(0)
print('%s outbox86_fam %s %s: watching cand/ for the lane\'s points (%s / %s, keys %s), outbox %s' % (time.strftime('%H:%M:%SZ', time.gmtime()), TAG, X, F.qf(X) + KL, F.lf(X) + KL, KB, F.O), flush=True)
while True:
    try: one_pass()
    except Exception as e: print('%s pass failed: %r' % (time.strftime('%H:%M:%SZ', time.gmtime()), e), flush=True)
    time.sleep(POLL)
