"""Run a command, report its peak RSS (MB) and wall time on stderr.  Usage: python3 runrss.py OUT ERR cmd args..."""
import sys, subprocess, resource, time
t = time.time()
with open(sys.argv[1], 'w') as o, open(sys.argv[2], 'w') as e:
    rc = subprocess.call(sys.argv[3:], stdout=o, stderr=e)
    e.write('# rc=%d peak_rss_MB=%.0f wall_s=%.0f\n' % (rc, resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024, time.time() - t))
sys.exit(rc)
