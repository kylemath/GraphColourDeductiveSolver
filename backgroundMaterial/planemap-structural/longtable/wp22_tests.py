#!/usr/bin/env python3
"""wp22_tests.py -- tests of the WP22 (S2) build.  Tiny budgets, at most 2 workers.  Standard library (unittest).

  python3 wp22_tests.py            all tests (a few minutes)
  python3 wp22_tests.py -v         verbose
Regression data are read as DATA from the project (T4 faces from MathConjectureR.md, W6 from l-attack.md, the A_3
witness from explore-vhphi/lattack_witness.py, Math's certificates); no project code is imported.
"""
import hashlib
import warnings
import json
import os
import random
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

warnings.simplefilter("ignore", ResourceWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wp22_radius as R          # noqa: E402
import wp22_census as C          # noqa: E402
import wp22_search as S          # noqa: E402
import wp22_s2c as X             # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
MATH = os.path.join(ROOT, "SolvingFrameworkPlan/docs/working/MathChainSearch")
RUNNER = os.path.join(HERE, "wp22_runner.py")


def faces_T4():
    txt = open(os.path.join(ROOT, "SolvingFrameworkPlan/docs/working/MathConjectureR.md")).read()
    line = next(l for l in txt.split("\n") if l.startswith("(0,1,2) (0,1,5)"))
    tris = [tuple(map(int, m.groups())) for m in re.finditer(r"\((\d+),(\d+),(\d+)\)", line)]
    return C.orient_faces(tris)


def data_W6():
    rep = open(os.path.join(ROOT, "SolvingFrameworkPlan/docs/working/creative-intel-2026-10-05/l-attack.md")).read().split("\n")
    fl = next(l for l in rep if l.startswith("Witness W6"))
    cl = next(l for l in rep if l.startswith("Colours (vertex:colour)"))
    faces = [tuple(map(int, m.groups())) for m in re.finditer(r"\[(\d+),(\d+),(\d+)\]", fl)]
    col = {int(a): int(b) for a, b in re.findall(r"(\d+):(\d+)", cl.split("Link of v")[0].split("):")[1])}
    return faces, 16, col


def data_A3():
    src = open(os.path.join(HERE, "explore-vhphi/lattack_witness.py")).read()
    faces = eval(re.search(r"^A3_FACES\s*=\s*(.+)$", src, re.M).group(1))
    col = eval(re.search(r"^A3_COL\s*=\s*(.+)$", src, re.M).group(1))
    return faces, 0, col


def run_cmd(args, env=None, check=True):
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.run([sys.executable, RUNNER] + args, capture_output=True, text=True, env=e)
    if check and p.returncode != 0:
        raise AssertionError("runner %s failed rc=%d\n%s\n%s" % (args, p.returncode, p.stdout, p.stderr))
    return p


class TestRadiusRegression(unittest.TestCase):
    def test_T4(self):
        H = R.Hole(faces_T4(), 4)
        self.assertIsNone(H.check())
        self.assertEqual(H.n, 17)
        self.assertEqual(sorted(H.degree.values()).count(5), 12)
        self.assertEqual(sorted(H.degree.values()).count(6), 5)
        allst = R.all_states(H, need_four_link=False)
        self.assertEqual(len(allst), 68)
        dist, size = H.class_radii(allst[0])
        self.assertEqual(size, 68)                      # the whole colouring set is one class
        self.assertEqual(len(dist), 68)                 # nothing unreached
        self.assertEqual(sum(1 for s in allst if H.filled(s)), 22)
        hist = {}
        for s in allst:
            hist[dist[s]] = hist.get(dist[s], 0) + 1
        self.assertEqual(hist, {0: 22, 1: 25, 2: 15, 3: 4, 4: 2})
        dl = [s for s in allst if H.is_dl(list(s))]
        self.assertEqual(len(dl), 21)
        dh = {}
        for s in dl:
            dh[dist[s]] = dh.get(dist[s], 0) + 1
        self.assertEqual(dh, {2: 15, 3: 4, 4: 2})
        # the per-state early-exit BFS agrees with the multi-source radius on every state
        for s in allst:
            r, info = R.radius(H, s)
            self.assertEqual(r, dist[s])

    def test_W6(self):
        faces, v, col = data_W6()
        H = R.Hole(faces, v)
        self.assertIsNone(H.check())
        self.assertEqual(H.n, 20)
        self.assertEqual(H.degree[v], 5)
        base = [col[u] for u in H.labels]
        self.assertTrue(H.proper(base))
        self.assertTrue(H.is_dl(base))                  # start state doubly locked
        self.assertEqual(H.chain_len(base), 6)          # chain of length 6
        r, info = R.radius(H, R.canon(base))
        self.assertEqual(r, 2)

    def test_A3_witness_and_census_centre(self):
        faces, v, col = data_A3()
        H = R.Hole(faces, v)
        base = [col[u] for u in H.labels]
        self.assertEqual(H.chain_len(base), 40)         # infinite chain (cap)
        r, _ = R.radius(H, R.canon(base))
        self.assertIn(r, (2, 3))
        # all infinite-chain colourings at the centre of A_3 (own construction): radius 2 or 3, both occur
        recs, summ = C.census_hole("A_3", 3, 0)
        inf = [x["radius"] for x in recs if x["chain"] >= 40]
        self.assertEqual(len(inf), 20)
        self.assertTrue(set(inf) <= {2, 3})
        self.assertEqual(set(inf), {2, 3})

    def test_planted_targetless(self):
        H = R.Hole(faces_T4(), 4)
        s0 = next(s for s in R.all_states(H) if H.is_dl(list(s)))
        never = lambda st: len({st[i] for i in H.link}) <= 1     # unreachable: link always has >= 2 colours
        r, info = R.radius(H, s0, target=never)
        self.assertEqual(r, float("inf"))
        self.assertEqual(info["status"], "closed")
        self.assertEqual(info["class_size"], 68)
        # the search's kill logic on a planted unreachable target
        res = S.search_tag("planted", cpu_cap=None, max_steps=50, nlo=12, nhi=12,
                           target_factory=lambda Hh: (lambda st: len({st[i] for i in Hh.link}) <= 1))
        self.assertEqual(res["stopped"], "kill")
        self.assertEqual(len(res["kill2"]), 1)
        cert = res["kill2"][0]
        self.assertTrue(cert["claim"]["class_closed_no_filled"])
        # under the REAL definition that claim is false: the certificate checker must reject it (planted fault)
        ok, msg = R.check_cert(cert)
        self.assertFalse(ok, msg)
        # a correct radius claim is accepted by the certificate checker
        r0, _ = R.radius(H, s0)
        self.assertTrue(R.check_cert({"faces": [list(f) for f in faces_T4()], "v": 4,
                                      "colouring": {str(u): s0[i] for i, u in enumerate(H.labels)},
                                      "claim": {"radius": r0}})[0])

    def test_cap_reports_capped(self):
        H = R.Hole(faces_T4(), 4)
        s0 = next(s for s in R.all_states(H) if H.is_dl(list(s)))
        never = lambda st: False
        r, info = R.radius(H, s0, cap=10, target=never)
        self.assertIsNone(r)
        self.assertEqual(info["status"], "capped")
        r, info = R.radius(H, s0, max_depth=1, target=never)
        self.assertIsNone(r)
        self.assertEqual(info["status"], "depth")


class TestCensus(unittest.TestCase):
    def test_graphs(self):
        for r, n in ((3, 17), (4, 22), (5, 27)):
            H = C.check_A(r)
            self.assertEqual(H.n, n)
            self.assertEqual(set(H.degree.values()), {5, 6})
            self.assertEqual(sum(1 for d in H.degree.values() if d == 5), 12)
        faces, v, col = data_A3()                       # labelled graph equals the witness file's A_3
        a = {frozenset((x, y)) for f in C.build_A(3) for x, y in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0]))}
        b = {frozenset((x, y)) for f in faces for x, y in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0]))}
        self.assertEqual(a, b)

    def test_counts_vs_audit(self):
        # audit: 120, 120, 360 infinite-chain colourings with x0's colour fixed = 20, 20, 60 classes x 6
        want = {3: 20, 4: 20, 5: 60}
        for r in (3, 4, 5):
            recs, summ = C.census_hole("A_%d" % r, r, 0)
            self.assertEqual(summ["infinite_chain_classes"], want[r])
            self.assertEqual(summ["infinite_chain_classes"] * 6, {3: 120, 4: 120, 5: 360}[r])
            self.assertEqual(summ["capped"], 0)
            self.assertEqual(summ["kill2_candidates"], [])
            self.assertEqual(len(recs), summ["doubly_locked"])
            for x in recs:
                self.assertEqual(x["state"][0], -1)     # entry v is -1
                self.assertTrue(x["doubly_locked"])
        recs, summ = C.census_hole("A_3", 3, 0)
        self.assertEqual(summ["states_four_link"], 60)  # 360 raw with x0 fixed / 6
        self.assertEqual(summ["radius_hist"], {"2": 20, "3": 10})

    def test_symmetry_orbit_mates(self):
        # the 5-fold rotation: ring-0 holes (and ring r-1 holes) of A_r give identical radius multisets
        for r in (3, 4):
            hs = {}
            for h, _w in C.holes_of(r):
                _recs, s = C.census_hole("A_%d" % r, r, h)
                hs[h] = (s["doubly_locked"], tuple(sorted(s["radius_hist"].items())),
                         tuple(sorted(s["chain_hist"].items())))
            ring0 = [hs[1 + t] for t in range(5)]
            last = [hs[1 + 5 * (r - 1) + t] for t in range(5)]
            self.assertEqual(len(set(ring0)), 1)
            self.assertEqual(len(set(last)), 1)
            self.assertEqual(len(hs), 12)


class TestSearch(unittest.TestCase):
    def test_initial_states_and_moves(self):
        rng = random.Random("wp22-test-moves")
        nmoves = 0
        for _ in range(12):
            faces, v, col = S.init_state(rng)
            H = R.Hole(faces, v)
            self.assertIsNone(H.check())
            self.assertGreaterEqual(min(H.degree.values()), 4)
            self.assertTrue(12 <= H.n <= 30)
            self.assertEqual(H.degree[v], 5)
            self.assertTrue(H.proper([col[u] for u in H.labels]))
            self.assertTrue(H.is_dl([col[u] for u in H.labels]))
            for _k in range(250):
                mv = S.move(rng, faces, v, col)
                if mv is None:
                    continue
                faces, col = mv
                nmoves += 1
                H = R.Hole(faces, v)
                self.assertIsNone(H.check())
                self.assertGreaterEqual(min(H.degree.values()), 4)   # EVERY visited triangulation
                self.assertEqual(H.degree[v], 5)
                self.assertTrue(H.proper([col[u] for u in H.labels]))
        self.assertGreater(nmoves, 1000)

    def test_deterministic_tag(self):
        a = S.dumps(S.search_tag("t007", cpu_cap=None, max_steps=400))
        b = S.dumps(S.search_tag("t007", cpu_cap=None, max_steps=400))
        self.assertEqual(a, b)
        c = S.dumps(S.search_tag("t008", cpu_cap=None, max_steps=400))
        self.assertNotEqual(a, c)
        # a run stopped by the CPU cap is reproduced exactly by a replay with its recorded number of steps
        r1 = S.search_tag("t009", cpu_cap=1.5, max_steps=None)
        self.assertTrue(r1["capped"])
        r2 = S.search_tag("t009", cpu_cap=None, max_steps=r1["steps"])
        for r in (r1, r2):
            r.pop("stopped"), r.pop("capped")
        self.assertEqual(S.dumps(r1), S.dumps(r2))

    def test_result_content(self):
        r = S.search_tag("t010", cpu_cap=None, max_steps=300)
        self.assertEqual(r["seed"], "wp22|s2a|t010")
        self.assertEqual(r["stopped"], "max_steps")
        self.assertGreaterEqual(r["best"]["r"], 2)
        ok, msg = R.check_cert({"faces": r["best"]["cert"]["faces"], "v": r["best"]["cert"]["v"],
                                "colouring": r["best"]["cert"]["colouring"],
                                "claim": {"radius": r["best"]["r"]}})
        self.assertTrue(ok, msg)


class TestS2c(unittest.TestCase):
    def test_math_certificates(self):
        dirs = [os.path.join(MATH, "certs_len_ge6"), os.path.join(MATH, "lt_certs")]
        files = X.list_certs(dirs)
        self.assertEqual(len(files), 24)
        nstates = 0
        hist = {}
        for f in files:
            recs, summ = X.cert_records(f)
            cert = X.load_cert(f)
            if cert.get("claimed_length") is not None:     # same chain length as Math's checker
                self.assertEqual(summ["doubly_locked_states"], cert["claimed_length"], f)
            self.assertEqual(summ["capped"], 0)
            self.assertEqual(summ["kill2_candidates"], [])
            for k, v in summ["radius_hist_dl"].items():
                hist[k] = hist.get(k, 0) + v
            nstates += summ["states"]
        self.assertEqual(hist.get("inf", 0), 0)
        self.assertTrue(set(hist) <= {"2", "3", "4", "5", "6"}, hist)


class TestRunner(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="wp22test-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def d(self, name):
        return os.path.join(self.tmp, name)

    def plan_s2a(self, name, tags=4, steps=120, **kw):
        args = ["plan", self.d(name), "--mode", "s2a", "--tags", str(tags), "--tag-cpu", "30",
                "--max-steps", str(steps)]
        for k, v in kw.items():
            args += ["--" + k.replace("_", "-"), str(v)]
        run_cmd(args)

    def merged(self, name):
        out = self.d(name + "-m")
        run_cmd(["merge", self.d(name), out])
        return open(out + "-summary.json", "rb").read()

    def test_worker_counts_and_interrupt_resume(self):
        self.plan_s2a("w1")
        run_cmd(["run", self.d("w1"), "--workers", "1"])
        m1 = self.merged("w1")
        self.plan_s2a("w2")
        run_cmd(["run", self.d("w2"), "--workers", "2"])
        m2 = self.merged("w2")
        self.assertEqual(hashlib.sha256(m1).hexdigest(), hashlib.sha256(m2).hexdigest())
        # shard files are byte-identical across runs (determinism of a tag rerun through the runner)
        for i in range(4):
            a = open(os.path.join(self.d("w1"), "shards", "shard-%05d.json" % i), "rb").read()
            b = open(os.path.join(self.d("w2"), "shards", "shard-%05d.json" % i), "rb").read()
            self.assertEqual(a, b)
        # interrupt (SIGTERM to the scheduler while workers sleep) and resume
        self.plan_s2a("ir")
        env = {"WP22_TEST_SLEEP": "2.5", "WP22_TEST_SLEEP_IDS": "2,3"}
        e = dict(os.environ)
        e.update(env)
        p = subprocess.Popen([sys.executable, RUNNER, "run", self.d("ir"), "--workers", "2"], env=e,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        t0 = time.time()
        while time.time() - t0 < 30:
            led = json.load(open(os.path.join(self.d("ir"), "ledger.json")))
            if any(x["status"] == "done" for x in led["shards"].values()) and \
                    any(x["status"] == "running" for x in led["shards"].values()):
                break
            time.sleep(0.2)
        p.send_signal(signal.SIGTERM)
        self.assertEqual(p.wait(timeout=30), 128 + signal.SIGTERM)
        st = run_cmd(["status", self.d("ir")], check=False)
        self.assertEqual(st.returncode, 1)               # not complete
        self.assertIn("partial", st.stdout)
        refuse = run_cmd(["merge", self.d("ir"), self.d("ir-m")], check=False)
        self.assertNotEqual(refuse.returncode, 0)
        self.assertIn("MERGE REFUSED", refuse.stderr + refuse.stdout)
        run_cmd(["run", self.d("ir"), "--workers", "2"])
        self.assertEqual(hashlib.sha256(self.merged("ir")).hexdigest(), hashlib.sha256(m1).hexdigest())

    def test_sigkilled_worker_retried(self):
        self.plan_s2a("k", tags=2)
        e = dict(os.environ)
        e.update({"WP22_TEST_SLEEP": "4", "WP22_TEST_SLEEP_IDS": "0"})
        p = subprocess.Popen([sys.executable, RUNNER, "run", self.d("k"), "--workers", "2"], env=e,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        t0 = time.time()
        pid = None
        while time.time() - t0 < 30 and pid is None:
            try:
                led = json.load(open(os.path.join(self.d("k"), "ledger.json")))
                pid = led["shards"]["0"]["pid"] if led["shards"]["0"]["status"] == "running" else None
            except (ValueError, OSError):
                pass
            time.sleep(0.1)
        self.assertIsNotNone(pid)
        os.kill(pid, signal.SIGKILL)
        self.assertEqual(p.wait(timeout=60), 0)
        led = json.load(open(os.path.join(self.d("k"), "ledger.json")))
        self.assertEqual(led["shards"]["0"]["status"], "done")
        self.assertGreaterEqual(led["shards"]["0"]["attempts"], 2)
        self.assertTrue(any("killed by signal 9" in h for h in led["shards"]["0"]["history"]), led["shards"]["0"])
        self.merged("k")

    def test_deleted_and_corrupted_shards(self):
        self.plan_s2a("c", tags=3)
        run_cmd(["run", self.d("c"), "--workers", "2"])
        ref = self.merged("c")
        sh = lambda i: os.path.join(self.d("c"), "shards", "shard-%05d.json" % i)
        os.remove(sh(0))
        with open(sh(1), "r+b") as f:
            f.seek(10)
            f.write(b"X")                                # corrupt one byte
        st = run_cmd(["status", self.d("c"), "--verify"], check=False)
        self.assertEqual(st.returncode, 1)
        self.assertIn("damaged", st.stdout)
        refuse = run_cmd(["merge", self.d("c"), self.d("c-m2")], check=False)
        self.assertNotEqual(refuse.returncode, 0)
        run_cmd(["run", self.d("c"), "--workers", "2"])  # recomputes both
        self.assertEqual(self.merged("c"), ref)
        # truncated ledger hash is not trusted either: edit a recorded hash
        led = json.load(open(os.path.join(self.d("c"), "ledger.json")))
        led["shards"]["2"]["sha256"] = "0" * 64
        json.dump(led, open(os.path.join(self.d("c"), "ledger.json"), "w"))
        refuse = run_cmd(["merge", self.d("c"), self.d("c-m3")], check=False)
        self.assertNotEqual(refuse.returncode, 0)
        run_cmd(["run", self.d("c"), "--workers", "1"])
        self.assertEqual(self.merged("c"), ref)

    def test_tiny_cpu_cap(self):
        run_cmd(["plan", self.d("cap"), "--mode", "s2a", "--tags", "4", "--tag-cpu", "2", "--cpu-cap", "3"])
        p = run_cmd(["run", self.d("cap"), "--workers", "2"], check=False)
        self.assertEqual(p.returncode, 3)
        self.assertIn("capped", p.stdout)
        led = json.load(open(os.path.join(self.d("cap"), "ledger.json")))
        self.assertTrue(led["capped"])
        self.assertTrue(any(x["status"] == "capped" for x in led["shards"].values()))
        refuse = run_cmd(["merge", self.d("cap"), self.d("cap-m")], check=False)
        self.assertNotEqual(refuse.returncode, 0)
        self.assertIn("MERGE REFUSED", refuse.stderr + refuse.stdout)
        self.assertFalse(os.path.exists(self.d("cap-m-summary.json")))

    def test_s2b_s2c_modes(self):
        run_cmd(["plan", self.d("b"), "--mode", "s2b", "--orders", "3"])
        run_cmd(["run", self.d("b"), "--workers", "2"])
        out = self.d("b-m")
        run_cmd(["merge", self.d("b"), out])
        summ = json.load(open(out + "-summary.json"))
        self.assertEqual(summ["holes"], 12)
        self.assertEqual(summ["radius_hist_by_graph"]["A_3"], {"2": 180, "3": 20})
        lines = open(out + ".jsonl").read().splitlines()
        self.assertEqual(len(lines), summ["doubly_locked_states"])
        rec = json.loads(lines[0])
        for k in ("graph", "v", "faces_sha256", "state", "doubly_locked", "radius"):
            self.assertIn(k, rec)
        run_cmd(["plan", self.d("x"), "--mode", "s2c"])
        run_cmd(["run", self.d("x"), "--workers", "2"])
        run_cmd(["merge", self.d("x"), self.d("x-m")])
        sc = json.load(open(self.d("x-m-summary.json")))
        self.assertEqual(sc["certificates"], 24)
        self.assertEqual(sc["capped_states"], 0)

    def test_package_hash_mismatch_refused(self):
        self.plan_s2a("h", tags=1)
        plan_p = os.path.join(self.d("h"), "plan.json")
        plan = json.load(open(plan_p))
        plan["producer_sha256"]["wp22_radius.py"] = "0" * 64
        json.dump(plan, open(plan_p, "w"))
        p = run_cmd(["run", self.d("h")], check=False)
        self.assertNotEqual(p.returncode, 0)
        p = run_cmd(["merge", self.d("h"), self.d("h-m")], check=False)
        self.assertNotEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
