"""Run a command and kill its whole process tree if the summed CPU time of the tree exceeds a cap.
usage: wp_cpucap.py CAP_CPU_SECONDS -- COMMAND ...   Exit codes: the command's, or 3 if capped."""
import subprocess, sys, time
cap = float(sys.argv[1]); cmd = sys.argv[sys.argv.index("--") + 1:]
def cpu_s(t):
    s = 0.0
    for x in [float(y) for y in t.replace("-", ":").split(":")]: s = s * 60 + x
    return s
def tree_cpu(root):
    rows = subprocess.run(["ps", "-A", "-o", "pid=,ppid=,time="], capture_output=True, text=True).stdout.split("\n")
    kids, cpu = {}, {}
    for r in rows:
        p = r.split()
        if len(p) == 3: kids.setdefault(int(p[1]), []).append(int(p[0])); cpu[int(p[0])] = cpu_s(p[2])
    tot, stack, pids = 0.0, [root], []
    while stack:
        q = stack.pop(); tot += cpu.get(q, 0.0); pids.append(q); stack.extend(kids.get(q, []))
    return tot, pids
proc = subprocess.Popen(cmd)
while proc.poll() is None:
    time.sleep(30)
    tot, pids = tree_cpu(proc.pid)
    if tot > cap:
        print(f"CAPPED: tree CPU {tot:.0f}s exceeds cap {cap:.0f}s; killing", flush=True)
        for q in pids[::-1]:
            try: subprocess.run(["kill", "-9", str(q)])
            except Exception: pass
        sys.exit(3)
sys.exit(proc.returncode)
