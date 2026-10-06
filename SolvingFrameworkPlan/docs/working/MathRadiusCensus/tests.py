#!/usr/bin/env python3
"""MathRadiusCensus / tests.py: regression, mutation, resume and verifier-fault tests. Usage: python3 tests.py  (about 20 s)
Regression targets are the tables of MathConjectureR.md section 3 (A_2..A_6 centre holes, all holes of A_3 and A_4, T4)."""
import json, os, subprocess, sys, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); TMP = tempfile.mkdtemp(prefix="mrc_")
fails = []
def check(name, cond, info=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else "  " + str(info)))
    if not cond: fails.append(name)

def A(r):
    """stacked pentagonal antiprism A_r: pole 0, rings 1..r of 5 vertices, pole 5r+1; n = 5r+2"""
    R = lambda i, k: 1 + 5 * (i - 1) + (k % 5)
    q = 5 * r + 1; F = []
    for k in range(5): F.append((0, R(1, k), R(1, k + 1)))
    for i in range(1, r):
        for k in range(5): F.append((R(i, k), R(i, k + 1), R(i + 1, k))); F.append((R(i, k + 1), R(i + 1, k), R(i + 1, k + 1)))
    for k in range(5): F.append((q, R(r, k), R(r, k + 1)))
    return 5 * r + 2, F
T4F = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]
def line(n, F): return f"G {n} {'0'*4} {len(F)} " + " ".join(f"{a} {b} {c}" for a, b, c in F) + "\n"
gpath = os.path.join(TMP, "reg.txt")
graphs = [A(r) for r in (2, 3, 4, 5, 6)] + [(17, T4F)]
open(gpath, "w").write("".join(line(n, F) for n, F in graphs))

def run(binary, extra=()):
    p = subprocess.run([binary, gpath, *extra], capture_output=True, text=True)
    return p.returncode, [json.loads(l) for l in p.stdout.splitlines() if l.strip()]
def trim(h):
    h = list(h)
    while len(h) > 1 and h[-1] == 0: h.pop()
    return h
def by(recs, g, v): return [r for r in recs if r["g"] == g and r["v"] == v][0]

def regression(binary, quiet=False):
    """returns list of failed names"""
    rc, recs = run(binary); bad = []
    def chk(name, cond):
        if not cond: bad.append(name)
        if not quiet: check(name, cond)
    chk("exit code 0", rc == 0)
    if rc != 0: return bad + ["crash"]
    exp = {2: (20, 10, 0, [0, 0]), 3: (100, 40, 30, [0, 0, 20, 10]), 4: (520, 200, 80, [0, 0, 80]), 5: (2720, 1040, 530, [0, 0, 530]), 6: (14240, 5440, 2450, [0, 0, 2450])}
    for gi, r in enumerate((2, 3, 4, 5, 6)):
        x = by(recs, gi, 0); e = exp[r]
        chk(f"A_{r} centre: ncol/filled/DL", (x["ncol"], x["nfilled"], x["ndl"]) == e[:3])
        chk(f"A_{r} centre: DL radius histogram", trim(x["hist_dl"]) == trim(e[3]))
        chk(f"A_{r} centre: nothing unreached", x["unreached"] == 0)
    chk("A_2 icosahedron: no DL, not-DL unfilled radius 1", trim(by(recs, 0, 0)["hist_all"]) == [10, 10])
    chk("A_4 centre: max radius over all states 2", len(trim(by(recs, 2, 0)["hist_all"])) == 3)
    chk("A_5 centre: max radius over all states 2", len(trim(by(recs, 3, 0)["hist_all"])) == 3)
    # all holes of A_3 (n=17, poles 0 and 16): DL counts and radii
    for v in [r["v"] for r in recs if r["g"] == 1]:
        x = by(recs, 1, v)
        if v in (0, 16): chk(f"A_3 pole {v}: DL radii {{2:20,3:10}}", trim(x["hist_dl"]) == [0, 0, 20, 10])
        else: chk(f"A_3 hole {v}: 14 DL, all radius 2", trim(x["hist_dl"]) == [0, 0, 14])
    for v in [r["v"] for r in recs if r["g"] == 2]:
        x = by(recs, 2, v)
        if v in (0, 21): chk(f"A_4 pole {v}: 80 DL, radius 2", trim(x["hist_dl"]) == [0, 0, 80])
        else: chk(f"A_4 hole {v}: 28 DL, all radius 2", trim(x["hist_dl"]) == [0, 0, 28])
    t = by(recs, 5, 4)
    chk("T4 hole 4: 68 colourings, 22 filled", (t["ncol"], t["nfilled"]) == (68, 22))
    chk("T4 hole 4: radius table {0:22,1:25,2:15,3:4,4:2}", trim(t["hist_all"]) == [22, 25, 15, 4, 2])
    chk("T4 hole 4: 21 DL, radii {2:15,3:4,4:2}", t["ndl"] == 21 and trim(t["hist_dl"]) == [0, 0, 15, 4, 2])
    chk("T4: nothing unreached", t["unreached"] == 0)
    return bad

# 1. regression with the real binary
build = lambda out, *flags: subprocess.run(["g++", "-O2", *flags, "-o", out, os.path.join(HERE, "census.cpp")], check=True)
good = os.path.join(TMP, "census_good"); build(good)
b = regression(good); check("regression suite on the real census", not b, b)
# 2. mutation tests: each mutated binary must fail at least one regression check
for k, desc in ((1, "DL needs only the beta-gamma lock"), (2, "DL needs only one of the two locks (OR)"), (3, "colour pair (0,1) never swapped"),
                (4, "no canonical colour renaming"), (5, "BFS sources include non-DL unfilled states")):
    out = os.path.join(TMP, f"census_m{k}"); build(out, f"-DMUT={k}")
    bad = regression(out, quiet=True); check(f"mutation {k} ({desc}) is detected", len(bad) > 0)
# 3. verifier on the regression output, then verifier fault injection
rc, recs = run(good); jl = os.path.join(TMP, "reg.jsonl")
open(jl, "w").write("".join(json.dumps(r) + "\n" for r in recs))
# regression graph file has dummy hex; verifier checks hex equality against the file, which we wrote identically ("0000") -- fine
v = subprocess.run([sys.executable, os.path.join(HERE, "verify_census.py"), gpath, jl, "--every", "7"], capture_output=True, text=True)
check("independent verifier agrees on a sample of regression records", v.returncode == 0, v.stdout[-300:])
for field, fn in (("hist_dl", lambda r: r.__setitem__("hist_dl", [0, 0, r["hist_dl"][2] + 1] + r["hist_dl"][3:])), ("ndl", lambda r: r.__setitem__("ndl", r["ndl"] + 1)),
                  ("wit", lambda r: r["wit"].__setitem__(1, r["wit"][2]))):
    rr = [json.loads(json.dumps(r)) for r in recs if r["g"] == 1 and r["v"] == 0]; fn(rr[0])
    p2 = os.path.join(TMP, "bad.jsonl"); open(p2, "w").write("".join(json.dumps(r) + "\n" for r in rr))
    v = subprocess.run([sys.executable, os.path.join(HERE, "verify_census.py"), gpath, p2], capture_output=True, text=True)
    check(f"verifier detects a planted fault in {field}", v.returncode != 0)
# 4. generator: counts, validity, shard completeness, determinism
gen = os.path.join(HERE, "gen_tri")
if not os.path.exists(os.path.join(HERE, "census")): subprocess.run(["g++", "-O2", "-o", os.path.join(HERE, "census"), os.path.join(HERE, "census.cpp")], check=True)
if not os.path.exists(gen): subprocess.run(["g++", "-O2", "-o", gen, os.path.join(HERE, "gen_tri.cpp")], check=True)
for n in (12, 13, 14, 15, 16, 17, 18):
    out = subprocess.run([gen, str(n), "--all"], capture_output=True, text=True).stdout
    p = os.path.join(TMP, f"g{n}.txt"); open(p, "w").write(out)
    if n == 13: check("n=13: no graphs", out.strip() == ""); continue
    v = subprocess.run([sys.executable, os.path.join(HERE, "verify_census.py"), "--gen", p], capture_output=True, text=True)
    check(f"generator n={n}: valid, pairwise non-isomorphic, known count (verifier)", v.returncode == 0, v.stdout)
a = subprocess.run([gen, "16", "--all"], capture_output=True, text=True).stdout; b2 = subprocess.run([gen, "16", "--all"], capture_output=True, text=True).stdout
check("generator deterministic across reruns", a == b2)
sh = set()
for i in range(4): sh |= {l.split()[2] for l in subprocess.run([gen, "17", "--all", "--part", str(i), "4"], capture_output=True, text=True).stdout.splitlines()}
check("4 generator shards of n=17 together give all 4 classes", len(sh) == 4, len(sh))
# 5. resumability of the driver
od = os.path.join(TMP, "run16"); cmd = [sys.executable, os.path.join(HERE, "run_census.py"), "16", "--gen-parts", "2", "--block", "1", "--workers", "2", "--outdir", od]
subprocess.run(cmd, capture_output=True); m = json.load(open(od + "/manifest.json"))
os.remove(od + "/cen_16_b1.jsonl"); m["b1"] = {"status": "failed"}; json.dump(m, open(od + "/manifest.json", "w"))
r = subprocess.run(cmd, capture_output=True, text=True)
check("driver redoes only the interrupted shard and reports COMPLETE", "COMPLETE" in r.stdout and os.path.exists(od + "/cen_16_b1.jsonl"), r.stdout[-300:])
m = json.load(open(od + "/manifest.json")); m["b0"] = {"status": "failed"}; json.dump(m, open(od + "/manifest.json", "w"))
r = subprocess.run(cmd + ["--report"], capture_output=True, text=True)
check("report says PARTIAL when a shard is unfinished", "PARTIAL" in r.stdout, r.stdout[-300:])
shutil.rmtree(TMP)
print("ALL PASS" if not fails else f"FAILED: {fails}"); sys.exit(1 if fails else 0)
