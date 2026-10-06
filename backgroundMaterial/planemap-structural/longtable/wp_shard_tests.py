#!/usr/bin/env python3
"""Tests of wp_shard_runner.py.  Orders <= 18 only, at most 2 worker processes at any time.
usage: python3 wp_shard_tests.py [WORKDIR]      (default: a fresh temp directory; ~2-3 minutes)
Prints PASS/FAIL per check and a count; exit status 1 on any failure."""
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "wp_shard_runner.py")
DECL = os.path.join(HERE, "WP20-D1-declaration.md")
IN18 = os.path.join(HERE, "wp20", "input-m5-18.txt")
IN16, IN17 = (os.path.join(HERE, "wp20", "input-m5-%d.txt" % k) for k in (16, 17))
SEEDS17 = os.path.join(HERE, "wp21", "seeds17.txt")
W = tempfile.mkdtemp(prefix="wpshard-") if len(sys.argv) < 2 else os.path.abspath(sys.argv[1])
os.makedirs(W, exist_ok=True)
MIXED = os.path.join(W, "mixed-16-17-18.txt")        # 19 graphs, runner tests only (not for the checker)
with open(MIXED, "w") as f:
    for p in (IN16, IN17, IN18):
        f.write(open(p).read())
res = []


def check(name, ok, info=""):
    res.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + ((" -- " + str(info)) if info else ""), flush=True)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def runner(*args, env=None, check_rc=None):
    e = dict(os.environ)
    e.update(env or {})
    return subprocess.run([sys.executable, RUNNER] + [str(a) for a in args], capture_output=True, text=True, env=e)


def plan(name, inp=MIXED, size=7, order=18, **kw):
    d = os.path.join(W, name)
    shutil.rmtree(d, ignore_errors=True)
    extra = []
    for k, v in kw.items():
        extra += ["--" + k.replace("_", "-"), v]
    r = runner("plan", d, "--mode", "graphs", "--input", inp, "--decl", DECL, "--phase", "P1", "--order", order,
               "--shard-size", size, *extra)
    assert r.returncode == 0, r.stderr
    return d


def ledger(d):
    return json.load(open(os.path.join(d, "ledger.json")))


def workers_alive(d):
    out = subprocess.run(["ps", "-A", "-o", "pid=,command="], capture_output=True, text=True).stdout
    return [int(l.split()[0]) for l in out.splitlines() if "wp_shard_runner.py worker " + d in l]


def start_sched(d, workers=2, env=None, *extra):
    e = dict(os.environ)
    e.update(env or {})
    return subprocess.Popen([sys.executable, RUNNER, "run", d, "--workers", str(workers), *extra],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=e)


def wait_worker(d, timeout=30):
    t0 = time.time()
    while time.time() - t0 < timeout:
        w = workers_alive(d)
        if w:
            return w
        time.sleep(0.1)
    return []


def merge(d, out):
    return runner("merge", d, out)


# ---------------------------------------------------------------- 1. determinism
ref = None
hashes = {}
shard_hashes = {}
for workers in (1, 2):
    for size in (7, 13):
        d = plan("det-w%d-s%d" % (workers, size), size=size)
        r = runner("run", d, "--workers", workers)
        out = os.path.join(W, "det-w%d-s%d.json" % (workers, size))
        m = merge(d, out)
        hashes[(workers, size)] = sha(out) if m.returncode == 0 else None
        shard_hashes[(workers, size)] = [e["sha256"] for e in ledger(d)["shards"].values()]
        check("run w=%d shard=%d complete" % (workers, size), r.returncode == 0 and "state complete" in r.stdout,
              r.stdout.strip()[-120:])
check("merged output hash identical across workers {1,2} x shard sizes {7,13}",
      len(set(hashes.values())) == 1 and None not in hashes.values(), set(hashes.values()))
check("shard files byte-identical across worker counts (same shard size)",
      shard_hashes[(1, 7)] == shard_hashes[(2, 7)] and shard_hashes[(1, 13)] == shard_hashes[(2, 13)])
ref = hashes[(1, 7)]
# agreement with the plain producer output on the order-18 list (committed regression file)
d = plan("vs-plain", inp=IN18, size=5)
runner("run", d, "--workers", 2)
out18 = os.path.join(W, "o18.json")
merge(d, out18)
a, b = json.load(open(out18)), json.load(open(os.path.join(HERE, "wp20", "regression-m5-18.json")))
same = all(a[k] == b[k] for k in ("wp", "order", "declaration_sha256", "input_sha256", "producer_sha256",
                                  "graphs", "witnesses", "truncated"))
check("order-18 merged graphs+witnesses equal the committed plain-producer regression output", same)

# ---------------------------------------------------------------- 2. SIGKILL a worker mid-shard
d = plan("kill", size=7)
p = start_sched(d, 2, {"WP_SHARD_TEST_SLEEP": "4"})
ws = wait_worker(d)
time.sleep(0.5)
if ws:
    os.kill(ws[0], signal.SIGKILL)
out, _ = p.communicate(timeout=120)
L = ledger(d)
hist = [h for e in L["shards"].values() for h in e["history"]]
check("SIGKILLed worker: run completes", p.returncode == 0 and L["state"] == "complete", out.strip()[-100:])
check("SIGKILLed worker: shard was retried (attempts 2, history records the signal)",
      any(e["attempts"] == 2 for e in L["shards"].values()) and any("signal 9" in h for h in hist), hist)
o = os.path.join(W, "kill.json")
merge(d, o)
check("SIGKILLed worker: merged output identical to reference", os.path.exists(o) and sha(o) == ref)

# ---------------------------------------------------------------- 3. timeout, retry, failed
d = plan("timeout", size=7)
r = runner("run", d, "--workers", 2, "--timeout", 8, "--max-attempts", 2,
           env={"WP_SHARD_TEST_SLEEP": "30", "WP_SHARD_TEST_SLEEP_IDS": "1"})
L = ledger(d)
e1 = L["shards"]["1"]
check("timeout: shard 1 failed after 2 attempts, history shows timeouts",
      e1["status"] == "failed" and e1["attempts"] == 2 and all(h.startswith("timeout") for h in e1["history"]),
      (e1["status"], e1["attempts"], e1["history"]))
st = runner("status", d)
check("timeout: overall state is failed (not complete)", L["state"] == "failed" and "state failed" in st.stdout
      and st.returncode != 0, st.stdout.strip()[:100])
check("timeout: the other shards finished", L["shards"]["0"]["status"] == "done" and L["shards"]["2"]["status"] == "done")
pr = os.path.join(W, "timeout-final.json")
m = merge(d, pr)
check("timeout: merge refuses, writes nothing", m.returncode != 0 and "REFUSED" in (m.stdout + m.stderr)
      and not os.path.exists(pr), (m.stderr.strip()[:100]))
pp = os.path.join(W, "timeout-PARTIAL.json")
m = runner("merge", d, pp, "--partial")
pj = json.load(open(pp)) if os.path.exists(pp) else {}
check("timeout: --partial file has partial:true and a PARTIAL wp tag", pj.get("partial") is True
      and pj.get("wp", "").startswith("PARTIAL"), pj.get("missing_shards"))
m = runner("merge", d, os.path.join(W, "timeout-nofilename.json"), "--partial")
check("timeout: --partial refuses a name without PARTIAL", m.returncode != 0)
# checker must not accept the partial file
cp = subprocess.run([sys.executable, os.path.join(HERE, "d1_check.py"), pp, IN18, DECL, "--workers", "1"],
                    capture_output=True, text=True)
check("timeout: d1_check.py does not accept the partial file", cp.returncode != 0 and "CHECK OK" not in cp.stdout,
      (cp.stdout + cp.stderr).strip()[-120:])
r = runner("run", d, "--workers", 2, "--retry-failed")
check("timeout: --retry-failed then completes", r.returncode == 0 and ledger(d)["state"] == "complete")
o = os.path.join(W, "timeout.json")
merge(d, o)
check("timeout: merged output identical to reference after the retry", os.path.exists(o) and sha(o) == ref)

# ---------------------------------------------------------------- 4. SIGTERM the scheduler, resume
d = plan("sigterm", size=3)
p = start_sched(d, 2, {"WP_SHARD_TEST_SLEEP": "2"})
ws = wait_worker(d)
time.sleep(3.5)                       # some shards done, some running
p.send_signal(signal.SIGTERM)
out, _ = p.communicate(timeout=60)
time.sleep(0.5)
L = ledger(d)
nd = sum(1 for e in L["shards"].values() if e["status"] == "done")
check("SIGTERM: scheduler exited 143, no worker left alive, ledger has no running shard",
      p.returncode == 143 and not workers_alive(d) and not any(e["status"] == "running" for e in L["shards"].values()),
      (p.returncode, workers_alive(d)))
check("SIGTERM: interrupted mid-run (0 < done < total)", 0 < nd < len(L["shards"]), "%d/%d" % (nd, len(L["shards"])))
r = runner("run", d, "--workers", 2)
check("SIGTERM: resume completes", r.returncode == 0 and ledger(d)["state"] == "complete")
o = os.path.join(W, "sigterm.json")
merge(d, o)
check("SIGTERM: merged output identical to reference after interrupt+resume", sha(o) == ref)
check("SIGTERM: finished shards were not recomputed (attempts 1 for all done-before shards)",
      sum(1 for e in ledger(d)["shards"].values() if e["attempts"] == 1) >= nd)

# ---------------------------------------------------------------- 5. stale 'running' entry of a dead scheduler
d = plan("stale", size=7)
L = ledger(d)
L["shards"]["0"]["status"] = "running"
L["scheduler_pid"] = 2 ** 22 + 12345
json.dump(L, open(os.path.join(d, "ledger.json"), "w"))
st = runner("status", d)
check("stale running: status shows it as pending", '"pending": 3' in st.stdout, st.stdout.strip()[:100])
r = runner("run", d, "--workers", 2)
o = os.path.join(W, "stale.json")
merge(d, o)
check("stale running: resume completes, identical output", r.returncode == 0 and sha(o) == ref)

# ---------------------------------------------------------------- 6. corrupted shard, deleted shard
d = plan("corrupt", size=7)
runner("run", d, "--workers", 2)
sp0 = os.path.join(d, "shards", "shard-00001.json")
data = bytearray(open(sp0, "rb").read())
data[len(data) // 2] ^= 0x01
open(sp0, "wb").write(bytes(data))
st = runner("status", d, "--verify")
check("corrupt: status --verify reports the damaged shard", "damaged [1]" in st.stdout and "state partial" in st.stdout,
      st.stdout.strip()[:140])
o = os.path.join(W, "corrupt.json")
m = merge(d, o)
check("corrupt: merge refuses", m.returncode != 0 and not os.path.exists(o))
r = runner("run", d, "--workers", 2)
L = ledger(d)
check("corrupt: run recomputes only that shard", r.returncode == 0 and L["shards"]["1"]["attempts"] == 2
      and L["shards"]["0"]["attempts"] == 1 and L["shards"]["2"]["attempts"] == 1)
merge(d, o)
check("corrupt: merged output identical to reference", sha(o) == ref)
os.remove(os.path.join(d, "shards", "shard-00002.json"))
m = merge(d, o + ".2")
check("deleted shard: merge refuses and writes nothing", m.returncode != 0 and not os.path.exists(o + ".2"),
      m.stderr.strip()[:100])
st = runner("status", d)
check("deleted shard: status is not complete", "state complete" not in st.stdout and st.returncode != 0)
runner("run", d, "--workers", 2)
merge(d, o)
check("deleted shard: rerun restores it, identical output", sha(o) == ref)

# ---------------------------------------------------------------- 7. CPU cap
d = plan("cap", inp=IN18, size=2, cpu_cap=1.0)
r = runner("run", d, "--workers", 2)
L = ledger(d)
o = os.path.join(W, "cap.json")
m = merge(d, o)
check("CPU cap 1s: exit 3, state capped, some shards capped", r.returncode == 3 and L["state"] == "capped"
      and any(e["status"] == "capped" for e in L["shards"].values()), r.stdout.strip()[-120:])
check("CPU cap: no worker left, merge refuses", not workers_alive(d) and m.returncode != 0 and not os.path.exists(o))
r = runner("run", d, "--workers", 2, "--cpu-cap", 10000)
merge(d, o)
check("CPU cap: rerun with a larger cap completes (resumed)", r.returncode == 0 and ledger(d)["state"] == "complete"
      and os.path.exists(o))

# ---------------------------------------------------------------- 8. existing checkers
cp = subprocess.run([sys.executable, os.path.join(HERE, "d1_check.py"), out18, IN18, DECL, "--all", "--workers", "2"],
                    capture_output=True, text=True)
check("d1_check.py --all --workers 2 accepts the merged order-18 output", cp.returncode == 0 and "CHECK OK" in cp.stdout,
      (cp.stdout.strip().splitlines() or [""])[-1][:120])
d = os.path.join(W, "phaseA18")
shutil.rmtree(d, ignore_errors=True)
D21 = os.path.join(HERE, "WP21-declaration.md")
runner("plan", d, "--mode", "graphs", "--input", IN18, "--decl", D21, "--phase", "A", "--order", 18, "--shard-size", 5)
runner("run", d, "--workers", 2)
oA = os.path.join(W, "A18.json")
merge(d, oA)
cp = subprocess.run([sys.executable, os.path.join(HERE, "d1_check21.py"), oA, IN18, D21, "--all", "--workers", "2"],
                    capture_output=True, text=True)
check("d1_check21.py --all accepts the merged phase-A style output (wp WP20, phase A, WP21 declaration, order 18)",
      cp.returncode == 0 and "CHECK OK" in cp.stdout, (cp.stdout.strip().splitlines() or [""])[-1][:120])

# ---------------------------------------------------------------- 9. phase B (chains)
old = os.path.join(W, "B-old")
subprocess.run([sys.executable, os.path.join(HERE, "wp21_search.py"), "--seeds", SEEDS17, "--out-prefix", old,
                "--chains", "4", "--steps", "6", "--workers", "2"], capture_output=True)
d = os.path.join(W, "chains")
shutil.rmtree(d, ignore_errors=True)
runner("plan", d, "--mode", "chains", "--seeds", SEEDS17, "--chains", 4, "--steps", 6, "--seed-tag", "WP21")
p = start_sched(d, 2, {"WP_SHARD_TEST_SLEEP": "2"})
ws = wait_worker(d)
time.sleep(0.4)
if ws:
    os.kill(ws[0], signal.SIGKILL)
out, _ = p.communicate(timeout=120)
new = os.path.join(W, "B-new")
m = runner("merge", d, new)
files = ["-evaluated.txt", ".json", "-log.json"]
check("phase B runner (with a SIGKILLed chain worker): complete", p.returncode == 0 and ledger(d)["state"] == "complete")
check("phase B: runner outputs byte-identical to the old wp21_search.py CLI (3 files)",
      all(os.path.exists(new + f) and sha(new + f) == sha(old + f) for f in files))
check("phase B: -evaluated.txt and -log.json byte-identical to committed wp21/reg17-run1*",
      all(sha(new + f) == sha(os.path.join(HERE, "wp21", "reg17-run1" + f)) for f in ("-evaluated.txt", "-log.json")))
nj, rj = json.load(open(new + ".json")), json.load(open(os.path.join(HERE, "wp21", "reg17-run1.json")))
nj["producer_sha256"]["wp21_search.py"] = rj["producer_sha256"]["wp21_search.py"]
check("phase B: .json equals committed reg17-run1.json except its own wp21_search.py hash (v2 file)", nj == rj)

n, f = sum(res), len(res) - sum(res)
print("\n%d checks, %d passed, %d failed (workdir %s)" % (len(res), n, f, W))
sys.exit(1 if f else 0)
