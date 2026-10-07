#!/usr/bin/env python3
"""[exploratory] Local compute item 8: checks C1, C2, C3, C5, C7 of MathQuarterFloorBijections.md, and the global (across-j)
collision count of Lemma A's map phi. Plain Python on ../common/kempe_py.py (states up to renaming; every map below
commutes with renaming, so it is a well-defined map on canonical states).

Notation (link x_0..x_4 in rotation order, indices mod 5):
 filled f in F_i : link (W,X,Y,X,Y) at positions i..i+4, Z = absent colour.
   M3 short: x_{i+2} !~ x_{i+4} in {Y,Z}; M3 long: x_{i+2} ~ x_{i+4}.   (C2: XOR with x_{i+3} !~ x_i in {W,X}.)
   M2 short: x_{i+1} !~ x_{i+3} in {X,Z}; M2 long: x_{i+1} ~ x_{i+3}.   (C2: XOR with x_i !~ x_{i+2} in {W,Y}.)
   L_F = number of long bits over all filled states.
 unfilled s in U_j : link (alpha,mu,alpha,A,B) at j..j+4; lock1: x_{j+1} ~ x_{j+3} in {mu,A}; lock2: x_{j+1} ~ x_{j+4} in {mu,B}.
   R+3 s = swap the {alpha,A}-component of x_{j+2} (used when lock 2 holds; C2: it misses x_j iff lock 2 holds).
   R+2 s = swap the {alpha,B}-component of x_j (used when lock 1 holds).
   Lemma A phi: lock1 fails -> swap {mu,A}-comp of x_{j+3} (lands in F_{j+4}); else lock2 fails -> swap {mu,B}-comp of x_{j+4}
   (lands in F_{j+3}).
 Gamma: s -> R+3 s. N0 = no lock, N1 = one lock, D = both. Paths start at (lock1 fails, lock2 holds); d(P) = DL states inside;
 D_cyc = DL states on cycles. Class identity: 3F - U = 2 N0 + 1.5 L_F + sum_P (1 - d(P)) - D_cyc.
 Per-j identity: F_{j+1}+F_{j+3}+F_{j+4}-U_j = L_j + |U_j^ff| + |U_{j+3}^ff| + |E_j| - |DD_j|, L_j = |F_{j+4}^{M3 long}| +
 |F_{j+3}^{M2 long}| + |F_{j+1}^{M2 long}|, E_j = {lock1 fails, lock2 holds, R+3 s not DL}, DD_j = {d in D_j : R+3 d DL}.
 C5: psi(f) = phi_B^{-1} R+3 R+3 phi_A (f) for f with M3 and M2 short (phi_A = swap {Y,Z}-comp of x_{i+2}, phi_B^{-1} = swap
 {mu,B}-comp of x_{j+4}); defined iff the intermediate locks allow; is psi(f) = f?
 C7: distance (moves) from every DL state to the nearest filled state.
usage: qf.py --orders 12 14 ... > out.jsonl   (one line per hole)
       qf.py --floor-holes ORDER > out.jsonl   (only the holes containing a 1/4 class)
       qf.py --detail ORDER GENTRI_INDEX HOLE   (every DL state: dist, whether R+3 d / R+2 d are DL)
Also per class (Intern A): R_F = phi o R+3 (= Math's rho) and R_B = phi o R+2 on DL states: both defined and equal / differ,
only one defined, neither; collisions per j; collisions of the combined rule "R_F, else R_B"; overlap with phi's image."""
import json, os, sys, itertools
from collections import Counter, defaultdict
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import Space, gentri_rotation, adj_from_rot
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri")


def analyse(rot, hole, detail=False):
    adj = adj_from_rot(rot); S = Space(adj, hole, link=rot[hole]); S.build_graph(); cl, ncl = S.classes()
    dist = S.dist_to_filled(); L = S.linki; NS = len(S.states)
    bit = lambda i: 1 << i

    def joined(c, cm, u, w, p, q):
        return bool(S.flood(bit(u), cm[p] | cm[q]) >> w & 1)

    def sw(c, cm, x, p, q):
        K = S.flood(bit(x), cm[p] | cm[q]); return S.index[S.swap(c, K, p, q)], K
    info = [None] * NS; c2bad = Counter()
    for s in range(NS):
        c = S.states[s]; cm = S.cmasks(c); lc = [c[x] for x in L]
        if len(set(lc)) <= 3:
            i = [t for t in range(5) if lc.count(lc[t]) == 1][0]; x = [L[(i + t) % 5] for t in range(5)]
            W, X, Y = lc[i], lc[(i + 1) % 5], lc[(i + 2) % 5]; Z = ({0, 1, 2, 3} - {W, X, Y}).pop()
            m3long = joined(c, cm, x[2], x[4], Y, Z); m3alt = not joined(c, cm, x[3], x[0], W, X)
            m2long = joined(c, cm, x[1], x[3], X, Z); m2alt = not joined(c, cm, x[0], x[2], W, Y)
            if m3long != m3alt: c2bad["M3"] += 1
            if m2long != m2alt: c2bad["M2"] += 1
            info[s] = {"F": True, "i": i, "m3long": m3long, "m2long": m2long, "W": W, "X": X, "Y": Y, "Z": Z}
        else:
            j = [t for t in range(5) if lc[t] == lc[(t + 2) % 5]][0]; x = [L[(j + t) % 5] for t in range(5)]
            al, mu, A, B = lc[j], lc[(j + 1) % 5], lc[(j + 3) % 5], lc[(j + 4) % 5]
            l1 = joined(c, cm, x[1], x[3], mu, A); l2 = joined(c, cm, x[1], x[4], mu, B)
            d = {"F": False, "j": j, "l1": l1, "l2": l2}
            r3, K3 = sw(c, cm, x[2], al, A)
            if (not (K3 >> x[0] & 1)) != l2: c2bad["R+3"] += 1
            r2, K2 = sw(c, cm, x[0], al, B)
            if (not (K2 >> x[2] & 1)) != l1: c2bad["R+2"] += 1
            d["R3"] = r3 if l2 else None; d["R2"] = r2 if l1 else None
            if not l1: d["phi"] = sw(c, cm, x[3], mu, A)[0]; d["phi_case"] = 1
            elif not l2: d["phi"] = sw(c, cm, x[4], mu, B)[0]; d["phi_case"] = 2
            info[s] = d
    # checks on R+3 image: lands in U_{j+3} with lock 1
    for s in range(NS):
        d = info[s]
        if not d["F"] and d["R3"] is not None:
            t = info[d["R3"]]
            if t["F"] or t["j"] != (d["j"] + 3) % 5 or not t["l1"]: c2bad["R+3_image"] += 1
            if t["R2"] != s: c2bad["R+3_inverse"] += 1
    # global collision count for phi (across j and cases)
    pre = defaultdict(list)
    for s in range(NS):
        d = info[s]
        if not d["F"] and "phi" in d: pre[d["phi"]].append((d["j"], d["phi_case"], s))
    coll_same_j = sum(1 for t, P in pre.items() if len(P) != len({(a, b) for a, b, _ in P}))
    coll_cross_j = sum(1 for t, P in pre.items() if len({a for a, _, _ in P}) >= 2)
    maxpre = max((len(P) for P in pre.values()), default=0)
    first_cross = None
    for t, P in pre.items():
        if len({a for a, _, _ in P}) >= 2:
            first_cross = {"filled": {str(u): S.states[t][S.idx[u]] for u in S.order}, "preimages": [{"j": a, "case": b} for a, b, _ in P]}; break
    out = {"states": NS, "C2_bad": dict(c2bad), "phi_preimage_max": maxpre, "phi_collisions_same_j": coll_same_j,
           "phi_collisions_cross_j": coll_cross_j, "first_cross_j": first_cross, "classes": []}
    members = defaultdict(list)
    for s in range(NS): members[cl[s]].append(s)
    for k, C in members.items():
        F = [s for s in C if info[s]["F"]]; U = [s for s in C if not info[s]["F"]]
        isDL = lambda s: (not info[s]["F"]) and info[s]["l1"] and info[s]["l2"]
        N0 = sum(1 for s in U if not info[s]["l1"] and not info[s]["l2"]); N1 = sum(1 for s in U if info[s]["l1"] != info[s]["l2"])
        Dn = sum(1 for s in U if isDL(s)); LF = sum(info[s]["m3long"] + info[s]["m2long"] for s in F)
        # Gamma paths
        dP = []; onpath = set(); bad_path = 0
        for s in U:
            if not info[s]["l1"] and info[s]["l2"]:
                cnt = 0; t = info[s]["R3"]; steps = 0
                while True:
                    steps += 1
                    if steps > len(C) + 2: bad_path += 1; break
                    if isDL(t): cnt += 1; onpath.add(t); t = info[t]["R3"]; continue
                    if not info[t]["l2"] and info[t]["l1"]: break
                    bad_path += 1; break
                dP.append(cnt)
        Dcyc = Dn - len(onpath)
        lhs = 3 * len(F) - len(U); rhs = 2 * N0 + 1.5 * LF + sum(1 - d for d in dP) - Dcyc
        # per-j identity
        cntF = Counter(info[s]["i"] for s in F); cntU = Counter(info[s]["j"] for s in U)
        m3l = Counter(info[s]["i"] for s in F if info[s]["m3long"]); m2l = Counter(info[s]["i"] for s in F if info[s]["m2long"])
        ff = Counter(info[s]["j"] for s in U if not info[s]["l1"] and not info[s]["l2"])
        E = Counter(info[s]["j"] for s in U if not info[s]["l1"] and info[s]["l2"] and not isDL(info[s]["R3"]))
        DD = Counter(info[s]["j"] for s in U if isDL(s) and isDL(info[s]["R3"]))
        DDp = Counter(info[s]["j"] for s in U if isDL(s) and isDL(info[s]["R2"]))
        DDboth = Counter(info[s]["j"] for s in U if isDL(s) and isDL(info[s]["R3"]) and isDL(info[s]["R2"]))
        perj_bad = 0; perj = []
        for j in range(5):
            l = cntF[(j + 1) % 5] + cntF[(j + 3) % 5] + cntF[(j + 4) % 5] - cntU[j]
            Lj = m3l[(j + 4) % 5] + m2l[(j + 3) % 5] + m2l[(j + 1) % 5]
            r = Lj + ff[j] + ff[(j + 3) % 5] + E[j] - DD[j]
            perj_bad += l != r; perj.append([l, Lj, ff[j], ff[(j + 3) % 5], E[j], DD[j]])
        # C5
        c5 = Counter()
        for f in F:
            d = info[f]
            if d["m3long"] or d["m2long"]: continue
            c = S.states[f]; cm = S.cmasks(c); x = [L[(d["i"] + t) % 5] for t in range(5)]
            s1, _ = sw(c, cm, x[2], d["Y"], d["Z"])           # phi_A
            if info[s1]["R3"] is None: c5["stop_after_phiA_no_lock2"] += 1; continue
            s2 = info[s1]["R3"]
            if info[s2]["R3"] is None: c5["stop_after_R3_no_lock2"] += 1; continue
            s3 = info[s2]["R3"]; e = info[s3]
            if e["l2"]: c5["stop_s3_lock2_holds"] += 1; continue
            cc = S.states[s3]; ccm = S.cmasks(cc); jj = e["j"]; xx = [L[(jj + t) % 5] for t in range(5)]
            g, _ = sw(cc, ccm, xx[4], cc[xx[1]], cc[xx[4]])  # phi_B^{-1}: {mu,B}-comp of b
            c5["defined"] += 1; c5["returns_to_f" if g == f else "other_filled" if info[g]["F"] else "BAD_not_filled"] += 1
        dl_dist = Counter(dist[s] for s in U if isDL(s))
        # Intern A: R_F = phi o R+3 (Math's rho) and R_B = phi o R+2 (rho') on DL states
        rr = Counter(); imgF = defaultdict(list); imgB = defaultdict(list); imgComb = defaultdict(list)
        for s in U:
            if not isDL(s): continue
            a = info[s]["R3"]; b = info[s]["R2"]
            fF = info[a]["phi"] if not isDL(a) else None; fB = info[b]["phi"] if not isDL(b) else None
            if fF is not None: imgF[(info[s]["j"], fF)].append(s)
            if fB is not None: imgB[(info[s]["j"], fB)].append(s)
            comb = fF if fF is not None else fB
            if comb is not None: imgComb[comb].append(s)
            if fF is not None and fB is not None: rr["both_equal" if fF == fB else "both_differ"] += 1
            elif fF is not None: rr["only_RF"] += 1
            elif fB is not None: rr["only_RB_covers_DD"] += 1
            else: rr["neither_in_DD_and_DDprime"] += 1
            if fF is not None and (not info[fF]["F"] or info[fF]["i"] != (info[s]["j"] + 1) % 5): rr["RF_image_BAD"] += 1
            if fB is not None and (not info[fB]["F"] or info[fB]["i"] != (info[s]["j"] + 1) % 5): rr["RB_image_BAD"] += 1
        rr["RF_collisions_per_j"] = sum(len(v) - 1 for v in imgF.values()); rr["RB_collisions_per_j"] = sum(len(v) - 1 for v in imgB.values())
        rr["RF_else_RB_collisions"] = sum(len(v) - 1 for v in imgComb.values())
        phi_imgs = {info[s]["phi"] for s in U if "phi" in info[s]}
        rr["RF_else_RB_hits_phi_image"] = sum(1 for f in imgComb if f in phi_imgs)
        rec = {"size": len(C), "F": len(F), "U": len(U), "N0": N0, "N1": N1, "D": Dn, "L_F": LF, "paths": len(dP),
               "dP_hist": dict(Counter(dP)), "D_cyc": Dcyc, "bad_path": bad_path, "identity_lhs": lhs, "identity_rhs": rhs,
               "identity_ok": lhs == rhs, "perj_bad": perj_bad, "perj": perj, "DD": [DD[j] for j in range(5)],
               "DDprime": [DDp[j] for j in range(5)], "DDboth": [DDboth[j] for j in range(5)],
               "F_i": [cntF[i] for i in range(5)], "C5": dict(c5), "RF_RB": dict(rr), "DL_dist_hist": {str(a): b for a, b in sorted(dl_dist.items())}}
        out["classes"].append(rec)
    return out


def detail(rot, hole):
    """per DL state of every class: dist to filled, whether R+3 d and R+2 d are DL (Intern B's order-17 request)."""
    adj = adj_from_rot(rot); S = Space(adj, hole, link=rot[hole]); S.build_graph(); cl, _ = S.classes(); dist = S.dist_to_filled()
    out = []
    for s in range(len(S.states)):
        c = S.states[s]; cm = S.cmasks(c); lc = [c[x] for x in S.linki]
        if len(set(lc)) <= 3: continue
        L = S.linki; j = [t for t in range(5) if lc[t] == lc[(t + 2) % 5]][0]; x = [L[(j + t) % 5] for t in range(5)]
        al, mu, A, B = lc[j], lc[(j + 1) % 5], lc[(j + 3) % 5], lc[(j + 4) % 5]
        lk = lambda cc, cmm, xx: (bool(S.flood(1 << xx[1], cmm[cc[xx[1]]] | cmm[cc[xx[3]]]) >> xx[3] & 1), bool(S.flood(1 << xx[1], cmm[cc[xx[1]]] | cmm[cc[xx[4]]]) >> xx[4] & 1))
        if not all(lk(c, cm, x)): continue
        def isdl(t):
            cc = S.states[t]; l2 = [cc[y] for y in L]
            if len(set(l2)) <= 3: return False
            jj = [u for u in range(5) if l2[u] == l2[(u + 2) % 5]][0]; return all(lk(cc, S.cmasks(cc), [L[(jj + u) % 5] for u in range(5)]))
        K3 = S.flood(1 << x[2], cm[al] | cm[A]); K2 = S.flood(1 << x[0], cm[al] | cm[B])
        r3 = S.index[S.swap(c, K3, al, A)]; r2 = S.index[S.swap(c, K2, al, B)]
        out.append({"class": cl[s], "j": j, "dist": dist[s], "R+3_is_DL": isdl(r3), "R+2_is_DL": isdl(r2),
                    "colouring": {str(u): c[S.idx[u]] for u in S.order}})
    return out


def work(t):
    n, gi, line, v = t
    r = analyse(gentri_rotation(line), v)
    return {"order": n, "gentri_index": gi, "hole": v, **r}


def main():
    if "--detail" in sys.argv:
        n, gi, h = [int(x) for x in sys.argv[sys.argv.index("--detail") + 1:][:3]]
        l = [x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip()][gi]
        for r in detail(gentri_rotation(l), h): print(json.dumps(r))
        return
    tasks = []
    if "--floor-holes" in sys.argv:  # only holes that contain a 1/4 class (from ../6-quarter-floor/quarter-classes.jsonl)
        n0 = int(sys.argv[sys.argv.index("--floor-holes") + 1]); lines = [x for x in open(os.path.join(GENTRI, "tri%d.txt" % n0)) if x.strip()]
        for l in open(os.path.join(H, "..", "6-quarter-floor", "quarter-classes.jsonl")):
            r = json.loads(l)
            if r["order"] == n0 and r["deg"] == 5: tasks.append((n0, r["gentri_index"], lines[r["gentri_index"]], r["hole"]))
    orders = [int(x) for x in sys.argv[sys.argv.index("--orders") + 1:] if x.isdigit()] if "--orders" in sys.argv else []
    for n in orders:
        for gi, l in enumerate(x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip()):
            rot = gentri_rotation(l); tasks += [(n, gi, l, v) for v in range(len(rot)) if len(rot[v]) == 5]
    with Pool(6) as pool:
        for r in pool.imap(work, tasks, chunksize=4): print(json.dumps(r), flush=True)


if __name__ == "__main__":
    main()
