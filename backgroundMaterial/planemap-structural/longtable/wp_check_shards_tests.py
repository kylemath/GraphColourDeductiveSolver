#!/usr/bin/env python3
"""Tests for wp_check_shards.py / d1_check21.py --range.  At most 2 worker processes, order <= 23.

usage: wp_check_shards_tests.py [--plantri PATH] [--keep]
Fixture: the first K graphs of the committed order-21 exploratory output (wp20/exploratory-m5-21.json,
input wp20/input-m5-21.txt), copied to a temp dir with phase 'A' and the declaration hash re-set to
WP21-declaration.md.  The committed files are never modified.  Standard library only.
"""
import os, sys, json, hashlib, shutil, subprocess, tempfile, time, signal, argparse, copy

HERE = os.path.dirname(os.path.abspath(__file__))
CHK = os.path.join(HERE, "d1_check21.py")
DRV = os.path.join(HERE, "wp_check_shards.py")
DECL = os.path.join(HERE, "WP21-declaration.md")
K = 60          # graphs in the fixture
RS = 10         # range size
BAD_GRAPH = 37  # corrupted graph; lies in range 30..40
RESULTS = []


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def expect(name, cond, info=""):
    RESULTS.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + ((" -- " + info) if (info and not cond) else ""), flush=True)


def run(cmd, timeout=900):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def drv(out, inp, ledger, *extra, timeout=900):
    return run([sys.executable, DRV, out, inp, DECL, "--ledger-dir", ledger,
                "--range-size", str(RS), "--workers", "2"] + list(extra), timeout)


def results_state(ledger):
    st = {}
    for f in sorted(os.listdir(ledger)):
        if f.startswith("range-") and f.endswith(".json") or f == "global.json":
            p = os.path.join(ledger, f)
            st[f] = (sha(p), os.stat(p).st_mtime_ns)
    return st


def build_fixture(d):
    o = json.load(open(os.path.join(HERE, "wp20", "exploratory-m5-21.json")))
    lines = open(os.path.join(HERE, "wp20", "input-m5-21.txt")).read().splitlines()[:K]
    inp = os.path.join(d, "in.txt")
    open(inp, "w").write("\n".join(lines) + "\n")
    o["graphs"] = o["graphs"][:K]
    for k in o["witnesses"]:
        o["witnesses"][k] = [w for w in o["witnesses"][k] if w["index"] < K]
    o["phase"] = "A"
    o["declaration_sha256"] = sha(DECL)
    o["input_sha256"] = sha(inp)
    out = os.path.join(d, "out.json")
    json.dump(o, open(out, "w"))
    return o, inp, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plantri", default="/private/tmp/claude-501/ncounter/plantri58/plantri")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    d = tempfile.mkdtemp(prefix="wpcs-")
    print("workdir", d)
    o, inp, out = build_fixture(d)
    nsep = len(o["witnesses"]["sep_bad"])
    print("fixture: %d graphs, %d SEP-bad witnesses, %d ranges of %d" % (K, nsep, (K + RS - 1) // RS, RS))
    nr = (K + RS - 1) // RS

    # ---- 0. checker flags still work
    for order in (16, 17):
        if os.path.exists(a.plantri):
            rc, txt = run([sys.executable, CHK, "--selftest", str(order), "--plantri", a.plantri,
                           "--workers", "2"])
            expect("d1_check21.py --selftest %d still passes (SELFTEST OK, exit 0)" % order,
                   rc == 0 and "SELFTEST OK" in txt, txt[-300:])
        else:
            print("SKIP selftest (no plantri at %s)" % a.plantri)

    # ---- 1. unsharded verdict == sharded verdict (clean)
    t = time.time()
    rc_u, txt_u = run([sys.executable, CHK, out, inp, DECL, "--all", "--workers", "2"])
    print("unsharded --all: exit %d in %.0fs: %s" % (rc_u, time.time() - t, txt_u.strip().splitlines()[-1]))
    L1 = os.path.join(d, "L1")
    rc_s, txt_s = drv(out, inp, L1)
    print(txt_s.strip().splitlines()[-1])
    expect("clean: unsharded --all exit 0 and sharded exit 0 with 'CHECK OK (all %d ranges)'" % nr,
           rc_u == 0 and rc_s == 0 and ("CHECK OK (all %d ranges)" % nr) in txt_s)
    led = json.load(open(os.path.join(L1, "ledger.json")))
    expect("ledger: %d jobs (global + %d ranges), all ok, each with sha256 fields" % (nr + 1, nr),
           len(led["jobs"]) == nr + 1 and all(j["status"] == "ok" and len(j["log_sha256"]) == 64 and
                                              len(j["result_sha256"]) == 64 and len(j["checker_sha256"]) == 64 and
                                              len(j["output_sha256"]) == 64 for j in led["jobs"]))
    base = results_state(L1)

    # ---- 1b. resume of a finished ledger recomputes nothing
    rc, txt = drv(out, inp, L1)
    expect("resume of a complete ledger: exit 0, nothing recomputed",
           rc == 0 and results_state(L1) == base and ("%d jobs already ok and skipped, 0 to run" % (nr + 1)) in txt, txt[-300:])

    # ---- 2. corrupted count in graph BAD_GRAPH
    bad = copy.deepcopy(o)
    bad["graphs"][BAD_GRAPH]["vertices"][0]["locked_classes"] += 1
    badout = os.path.join(d, "bad.json")
    json.dump(bad, open(badout, "w"))
    rc_u2, txt_u2 = run([sys.executable, CHK, badout, inp, DECL, "--all", "--workers", "2"])
    L2 = os.path.join(d, "L2")
    rc_s2, txt_s2 = drv(badout, inp, L2)
    led2 = json.load(open(os.path.join(L2, "ledger.json")))
    badr = [tuple(j["range"]) for j in led2["jobs"] if j["status"] == "mismatch"]
    lo = BAD_GRAPH // RS * RS
    expect("corrupted count in graph %d: unsharded exit 1, sharded exit 1 'CHECK FAILED'" % BAD_GRAPH,
           rc_u2 == 1 and rc_s2 == 1 and "CHECK FAILED" in txt_s2, txt_s2[-300:])
    expect("detected exactly in range %d..%d (mismatch ranges: %s), all other jobs ok" % (lo, lo + RS, badr),
           badr == [(lo, lo + RS)] and sum(j["status"] == "ok" for j in led2["jobs"]) == nr, str(badr))
    # direct range runs of the checker: exit codes
    rc, txt = run([sys.executable, CHK, badout, inp, DECL, "--range", str(lo), str(lo + RS), "--workers", "1"])
    expect("checker --range %d %d on corrupted file: exit 1, 'RANGE %d..%d FAILED'" % (lo, lo + RS, lo, lo + RS),
           rc == 1 and ("RANGE %d..%d FAILED" % (lo, lo + RS)) in txt)
    rc, txt = run([sys.executable, CHK, badout, inp, DECL, "--range", "0", str(RS), "--workers", "1"])
    expect("checker --range 0 %d on the same file: exit 0, 'RANGE 0..%d OK'" % (RS, RS),
           rc == 0 and ("RANGE 0..%d OK" % RS) in txt)
    rc, txt = run([sys.executable, CHK, out, inp, DECL, "--range", str(K - 5), str(K + 5), "--workers", "1"])
    expect("checker --range past the end: exit 2 'INCOMPLETE'", rc == 2 and "INCOMPLETE" in txt, txt[-200:])
    # corrupted witness total is a global fault caught by the global job only
    badw = copy.deepcopy(o)
    if badw["witnesses"]["sep_bad"]:
        badw["witnesses"]["sep_bad"].pop()
    wout = os.path.join(d, "badw.json")
    json.dump(badw, open(wout, "w"))
    rc_w, txt_w = drv(wout, inp, os.path.join(d, "L2w"))
    expect("dropped witness (global total mismatch): sharded exit 1 'CHECK FAILED'", rc_w == 1 and "CHECK FAILED" in txt_w, txt_w[-300:])

    # ---- 3. SIGKILL the driver mid-run, then resume
    L3 = os.path.join(d, "L3")
    p = subprocess.Popen([sys.executable, DRV, out, inp, DECL, "--ledger-dir", L3, "--range-size", str(RS),
                          "--workers", "2"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         start_new_session=True)
    t0 = time.time()
    while time.time() - t0 < 300:
        if os.path.isdir(L3) and len([f for f in os.listdir(L3) if f.endswith(".json") and f != "ledger.json"]) >= 2:
            break
        time.sleep(0.05)
    os.kill(p.pid, signal.SIGKILL)
    p.wait()
    time.sleep(1.5)      # orphans should die with the parent (--die-with-parent)
    left = subprocess.run(["pgrep", "-f", inp], capture_output=True, text=True).stdout.split()
    expect("after SIGKILL of the driver no checker child survives", not left, str(left))
    done = results_state(L3)
    valid = True
    for f in done:
        e = json.load(open(os.path.join(L3, f)))
        h = dict(e)
        h.pop("result_sha256")
        valid &= hashlib.sha256(json.dumps(h, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == e["result_sha256"]
    ledger_ok = True
    try:
        json.load(open(os.path.join(L3, "ledger.json")))
    except Exception:
        ledger_ok = False
    expect("after SIGKILL: %d result files recorded, all intact; ledger.json parses" % len(done),
           0 < len(done) < nr + 1 and valid and ledger_ok, "%d files" % len(done))
    rc, txt = drv(out, inp, L3)
    after = results_state(L3)
    kept = all(after.get(f) == v for f, v in done.items())
    expect("resume after SIGKILL: final 'CHECK OK (all %d ranges)', exit 0" % nr, rc == 0 and ("CHECK OK (all %d ranges)" % nr) in txt, txt[-300:])
    expect("ranges already ok before the kill (%d) were not recomputed (files byte- and mtime-identical)" % len(done), kept)
    expect("resume line reports %d skipped" % len(done), ("%d jobs already ok and skipped" % len(done)) in txt, txt[:200])

    # ---- 4. corrupted recorded result is rechecked
    victim = "range-%07d-%07d.json" % (RS, 2 * RS)
    others = {f: v for f, v in results_state(L3).items() if f != victim}
    vp = os.path.join(L3, victim)
    data = open(vp).read()
    open(vp, "w").write(data.replace('"status": "ok"', '"status": "ok" ').replace('"attempts": 1', '"attempts": 7'))
    rc, txt = drv(out, inp, L3)
    new = results_state(L3)
    expect("tampered result file (self-hash broken) is rechecked; rest untouched; verdict OK",
           rc == 0 and new[victim][0] != sha_of_text(data) and json.load(open(vp))["attempts"] == 1
           and all(new[f] == v for f, v in others.items()) and "1 to run" in txt, txt[-300:])
    # truncated result file
    open(vp, "w").write(data[:50])
    rc, txt = drv(out, inp, L3)
    expect("truncated (unparseable) result file is rechecked; verdict OK", rc == 0 and "1 to run" in txt and "CHECK OK" in txt, txt[-300:])
    # corrupted log file
    lp = os.path.join(L3, victim.replace(".json", ".log"))
    open(lp, "a").write("tamper\n")
    rc, txt = drv(out, inp, L3)
    expect("log file whose hash no longer matches the record: range rechecked; verdict OK", rc == 0 and "1 to run" in txt and "CHECK OK" in txt, txt[-300:])
    # changed output file (stale hash): same data, different bytes
    out2 = os.path.join(d, "out-reformatted.json")
    json.dump(o, open(out2, "w"), indent=0)
    rc, txt = drv(out2, inp, L3)
    expect("changed output file (stale output hash): all %d jobs rechecked, none skipped, verdict OK" % (nr + 1),
           rc == 0 and ("0 jobs already ok and skipped, %d to run" % (nr + 1)) in txt and "CHECK OK" in txt, txt[:200])
    # changed checker file (stale checker hash)
    chk2 = os.path.join(d, "d1_check21_copy.py")
    shutil.copy(CHK, chk2)
    open(chk2, "a").write("\n# changed\n")
    rc, txt = drv(out2, inp, L3, "--checker", chk2)
    expect("changed checker file: all jobs rechecked, verdict OK",
           rc == 0 and ("0 jobs already ok and skipped, %d to run" % (nr + 1)) in txt and "CHECK OK" in txt, txt[:200])

    # ---- 5. deleted range result -> partial, exit 2
    L5 = os.path.join(d, "L5")
    rc, txt = drv(out, inp, L5)
    os.unlink(os.path.join(L5, "range-%07d-%07d.json" % (3 * RS, 4 * RS)))
    rc, txt = drv(out, inp, L5, "--limit", "0")
    expect("deleted range result (not rerun): 'PARTIAL: %d of %d ranges checked', exit 2" % (nr - 1, nr),
           rc == 2 and ("PARTIAL: %d of %d ranges checked" % (nr - 1, nr)) in txt and "CHECK OK" not in txt, txt[-300:])
    rc, txt = drv(out, inp, L5)
    expect("same ledger resumed without --limit: the missing range is recomputed, 'CHECK OK', exit 0",
           rc == 0 and "1 to run" in txt and "CHECK OK" in txt, txt[-200:])

    # ---- 6. timeout: retried, then reported timeout, not a pass
    L6 = os.path.join(d, "L6")
    rc, txt = drv(out, inp, L6, "--timeout", "0.4", "--retries", "1")
    led6 = json.load(open(os.path.join(L6, "ledger.json")))
    expect("timeouts: every range retried once (2 attempts), status 'timeout', exit 2, 'PARTIAL: 0 of %d', never CHECK OK" % nr,
           rc == 2 and all(j["status"] == "timeout" and j["attempts"] == 2 for j in led6["jobs"] if j["kind"] == "range")
           and ("PARTIAL: 0 of %d ranges checked" % nr) in txt and "CHECK OK" not in txt, txt[-300:])
    # a timed-out ledger is not trusted on resume
    rc, txt = drv(out, inp, L6)
    expect("resume of a timed-out ledger with a normal timeout: all rechecked, 'CHECK OK'", rc == 0 and "CHECK OK" in txt, txt[-200:])

    # ---- 7. SIGTERM and SIGINT: clean shutdown, valid ledger
    for sig, nm in ((signal.SIGTERM, "SIGTERM"), (signal.SIGINT, "SIGINT")):
        L7 = os.path.join(d, "L7" + nm)
        p = subprocess.Popen([sys.executable, DRV, out, inp, DECL, "--ledger-dir", L7, "--range-size", str(RS),
                              "--workers", "2"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, start_new_session=True)
        t0 = time.time()
        while time.time() - t0 < 300:
            if os.path.isdir(L7) and len([f for f in os.listdir(L7) if f.endswith(".json") and f != "ledger.json"]) >= 1:
                break
            time.sleep(0.05)
        os.kill(p.pid, sig)
        try:
            txt, _ = p.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            p.kill()
            txt = "driver did not exit"
        left = subprocess.run(["pgrep", "-f", L7], capture_output=True, text=True).stdout.split()
        try:
            ledg = json.load(open(os.path.join(L7, "ledger.json")))
            body = {k: v for k, v in ledg.items() if k != "ledger_sha256"}
            lok = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == ledg["ledger_sha256"]
        except Exception:
            lok = False
        strays = [f for f in os.listdir(L7) if ".run" in f or f.startswith(".tmp-")]
        expect("%s: driver exits 2 with PARTIAL, no children left, ledger valid with matching hash, no stray temp files" % nm,
               p.returncode == 2 and "PARTIAL" in txt and not left and lok and not strays,
               "rc=%s left=%s lok=%s strays=%s %s" % (p.returncode, left, lok, strays, txt[-200:]))
        rc, txt = drv(out, inp, L7)
        expect("%s: resume completes with CHECK OK" % nm, rc == 0 and "CHECK OK" in txt, txt[-200:])

    ok = all(RESULTS)
    print("\n%d of %d checks passed" % (sum(RESULTS), len(RESULTS)))
    print("ALL TESTS PASSED" if ok else "SOME TESTS FAILED")
    if not a.keep:
        shutil.rmtree(d, ignore_errors=True)
    return 0 if ok else 1


def sha_of_text(t):
    return hashlib.sha256(t.encode()).hexdigest()


if __name__ == "__main__":
    sys.exit(main())
