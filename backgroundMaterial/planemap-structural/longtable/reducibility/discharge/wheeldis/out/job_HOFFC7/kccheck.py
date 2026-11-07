"""HOFFC7-D (Studio, 7 Nov): re-check each kc line of in/in/kc55.tsv against its d7 D kill (d7_lines.tsv) with our own code:
kc line present verbatim in kc_src; (r, m) equal to the registry D entry (FILE md5 + NAME with D=true, via ST-32 Sources.lookup);
kc interior graph + degrees isomorphic to K rebuilt from the name (OFFC_SPEC section 2, ST-32 build_K). Engines run separately.
usage: python3 kccheck.py  (cwd wheeldis)"""
import sys, collections
sys.argv = ["x"]; exec(open("out/job_ST32/offc_verify.py").read().split("if __name__ ==")[0])
J = "out/job_HOFFC7/"
kc = {}
for l in open(J + "in/in/kc55.tsv"):
    g = l.rstrip("\n").split("\t")
    if len(g) >= 3: kc[g[0]] = (g[1], g[2])
def iso(V, E, kcl):
    g = kcl.split(); m = int(g[2]); rp = g[3].split(";"); ip = g[4].split(";")
    IE = {u: (set() if ip[u] == "-" else {int(x) for x in ip[u].split(",")}) for u in range(m)}
    deg = {u: len(IE[u]) + (0 if rp[u] == "-" else len(rp[u].split(","))) for u in range(m)}
    if any(u in IE[w] for w in IE for u in IE[w] if w not in IE[u]): return "intAdj not symmetric"
    if len(V) != m: return "m=%d != |K|=%d" % (m, len(V))
    Kv = sorted(V); Ka = {x: {y for y in Kv if frozenset((x, y)) in E} for x in Kv}
    order = sorted(range(m), key=lambda u: -len(IE[u]))
    def rec(i, mp):
        if i == m: return True
        u = order[i]
        for x in Kv:
            if x in mp.values() or V[x] != deg[u] or len(Ka[x]) != len(IE[u]): continue
            if any((w in IE[u]) != (mp[w] in Ka[x]) for w in mp): continue
            mp[u] = x
            if rec(i + 1, mp): return True
            del mp[u]
        return False
    return None if rec(0, {}) else "kc interior not isomorphic to K"
srcs = Sources(); hdr = None; out = []; seen = set()
for l in open(J + "in/d7_lines.tsv"):
    f = l.rstrip("\n").split("\t")
    if hdr is None: hdr = f; continue
    R = dict(zip(hdr, f))
    if R["SRC"] != "D": continue
    nm = R["NAME"]
    if nm in seen: out.append((nm, "dup", "-")); continue
    seen.add(nm)
    ev, why = srcs.lookup(R["file"], R["md5"], nm, "D")
    if why: out.append((nm, "FAIL registry: " + why, "-")); continue
    r, m, _ = ev
    if nm not in kc: out.append((nm, "NO-KC (registry r=%d m=%d, %s)" % (r, m, R["file"]), "-")); continue
    ksrc, kcl = kc[nm]
    p = ksrc[2:] if ksrc.startswith("./") else ksrc
    try: verb = kcl in open(p).read().splitlines()
    except Exception as e: verb = False
    g = kcl.split()
    if g[0] != nm: out.append((nm, "FAIL kc name", kcl)); continue
    if (int(g[1]), int(g[2])) != (r, m): out.append((nm, "FAIL kc r,m %s,%s != registry %d,%d" % (g[1], g[2], r, m), kcl)); continue
    K, why = build_K(nm, r, m)
    if why: out.append((nm, "FAIL build_K: " + why, kcl)); continue
    why = iso(K[0], K[1], kcl)
    out.append((nm, ("FAIL " + why) if why else ("ok%s" % ("" if verb else " (kc line not verbatim in " + ksrc + ")")), kcl))
with open(J + "kccheck.tsv", "w") as fo:
    fo.write("name\tverdict\tkc\n")
    for t in out: fo.write("\t".join(t) + "\n")
print(collections.Counter(v.split(" (")[0] if not v.startswith("NO-KC") else "NO-KC" for _, v, _ in out))
for nm, v, _ in out:
    if not v.startswith("ok"): print(nm, v)
