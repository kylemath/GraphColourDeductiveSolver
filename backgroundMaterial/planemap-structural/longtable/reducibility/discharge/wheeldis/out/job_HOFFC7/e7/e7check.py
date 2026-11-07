"""HOFFC7-D addendum (Studio, 7 Nov): re-check the 13 e7 kc lines (e7/e13.kc: 12 extracted by us from eq_D7_k3.txt.gz 2732ad76,
1 rebuilt by Opus from the name) like kccheck.py: registry D entry (d7_lines FILE md5 + NAME D=true, r, m), kc r/m equal, kc interior
graph + degrees isomorphic to K from the name; prints the registry classes/ext/reached for comparison with our dfast18 run."""
import sys, re, collections
sys.argv = ["x"]; exec(open("out/job_HOFFC7/kccheck.py").read().split("srcs = Sources()")[0])
J = "out/job_HOFFC7/"
kcs = {l.split()[0]: l.rstrip("\n") for l in open(J + "e7/e13.kc") if l.strip()}
srcs = Sources(); hdr = None; n = 0
for l in open(J + "in/d7_lines.tsv"):
    f = l.rstrip("\n").split("\t")
    if hdr is None: hdr = f; continue
    R = dict(zip(hdr, f)); nm = R["NAME"]
    if nm not in kcs: continue
    n += 1; ev, why = srcs.lookup(R["file"], R["md5"], nm, "D")
    if why: print(nm, "FAIL registry", why); continue
    r, m, _ = ev; g = kcs[nm].split()
    reg = [x for x in srcs.cache[srcs.path(R["file"])][1] if x.startswith(nm + " ") and "D=true" in x][0]
    st = " ".join(re.findall(r"(?:classes|ext|reached)=\d+", reg))
    if (int(g[1]), int(g[2])) != (r, m): print(nm, "FAIL r,m"); continue
    K, why = build_K(nm, r, m)
    print(nm, "FAIL build_K " + why if why else (iso(K[0], K[1], kcs[nm]) or "ok"), "r=%d m=%d" % (r, m), "| registry:", st)
print(n, "of", len(kcs))
