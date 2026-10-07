#!/usr/bin/env python3
"""[exploratory] Item 17 analysis. Reads the per-class state records written by charges.py:
   raw-12-20.jsonl  (all degree-5 holes, orders 12 14 16-20)   and   raw-floor.jsonl (holes containing a 1/4 class, orders 17 21-24; orders <= 20 of this file are skipped, they are in the first file).
usage: analyze.py raw-12-20.jsonl raw-floor.jsonl > results.txt     (also writes results.json)
Everything is exact (integers / Fractions).  Gauge: see charges.py docstring; tau = eps*(W) -> (eps*W+3)/4 is gauge free."""
import json, sys, collections, os
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from fit import nullspace
from math import lcm
from fractions import Fraction

def load():
    out = []
    for k, fn in enumerate(sys.argv[1:]):
        for l in open(fn):
            r = json.loads(l)
            if k == 1 and r["order"] <= 20: continue
            out.append(r)
    return out

def Wn(s): return s["eps"] * s["W"]          # gauge-fixed signed face count of G (integer for every state)
def tau(s):                                   # folding degree times sign q(v); FILLED states only
    assert s["t"] == "F"; return (s["eps"] * s["W"] + 3) // 4

def blocks(r):
    st = r["states"]; Fs = [s for s in st if s["t"] == "F"]
    if 4 * len(Fs) != r["size"]: return None
    ks = {s["k"] for s in Fs}
    if len(ks) != 1: return None
    i = ks.pop(); B = {"F": Fs, "U1": [], "U2": [], "DL": []}
    for s in st:
        if s["t"] == "F": continue
        d = (s["k"] - i) % 5
        if s["t"] == "U" and d == 1: B["U1"].append(s)
        elif s["t"] == "U" and d == 2: B["U2"].append(s)
        elif s["t"] == "D" and d == 4: B["DL"].append(s)
        else: return None
    if any(len(v) != len(Fs) for v in B.values()): return None
    B["i"] = i
    return B

def show(v):
    L = 1
    for x in v: L = lcm(L, x.denominator)
    return tuple(int(x * L) for x in v)
def relations(rows, cols):
    ns = nullspace(rows) if rows else []
    return [dict(zip(cols, show(v))) for v in ns]
def pr(*a): print(*a, flush=True)

R = load()
nfl = [r for r in R if 4 * r["nF"] == r["size"]]
res = {"classes": len(R), "floor_classes": len(nfl), "floor_by_order": dict(sorted(collections.Counter(r["order"] for r in nfl).items()))}
pr("classes", len(R), "floor", len(nfl), res["floor_by_order"])
fourblock = [(r, blocks(r)) for r in nfl]; fourblock = [(r, B) for r, B in fourblock if B]
pr("floor classes with the exact 4-block structure (F, U at j=i+1, U at j=i+2, DL at j=i+4, each F states):", len(fourblock), "of", len(nfl))

# ------------------------------------------------------------------ Q1
pr("\n== Q1: filled states, capped charge and folding degree")
nst = nF = 0; badsig = 0
for r in R:
    for s in r["states"]:
        nst += 1
        if s["t"] == "F":
            nF += 1
            badsig += (s["eps"] != (1 if s["qv"] > 0 else -1))
            assert abs(s["qv"]) == 3 and sum(s["qLfull"]) is not None
            assert (s["eps"] * s["W"] + 3) == 4 * s["eps"] * s["deg"]
pr("states", nst, "filled", nF, "; sign q(v) = eps_F (chirality of (missing, singleton, x_{i+1}, x_{i+2})) failures:", badsig)
pr("identity eps*W_G = 4*sigma*deg - 3 (W_G = signed face count of G) holds for every filled state (asserted)")
mod4 = collections.Counter((s["t"], Wn(s) % 4) for r in R for s in r["states"])
pr("eps*W mod 4 over all states, by type (F/U/D):", dict(mod4), "=> for filled states tau = (W+3)/4 is the integer sigma*deg; unfilled states have W = 3 mod 4 (no integer degree: (W+3)/4 is a half-integer)")
split = collections.Counter(); par = collections.Counter(); bal = collections.Counter(); tau_hist_floor1 = collections.Counter()
for r in R:
    Fs = [s for s in r["states"] if s["t"] == "F"]; fl = 4 * len(Fs) == r["size"]
    plus = sum(1 for s in Fs if s["qv"] > 0)
    split[(fl, "canonical-gauge |F+ - F-|==0" if 2 * plus == len(Fs) else "canonical-gauge unbalanced")] += 1
    tp = sum(1 for s in Fs if s["deg"] * s["eps"] > 0); tn = sum(1 for s in Fs if s["deg"] * s["eps"] < 0)
    bal[(fl, "tau>0 count == tau<0 count" if tp == tn else "tau-signs unbalanced")] += 1
    par[(fl, "both degree parities in class" if len({s["deg"] % 2 for s in Fs}) == 2 else "one parity")] += 1
    if fl and len(Fs) == 1: tau_hist_floor1[tau(Fs[0])] += 1
for nm, c in (("canonical-gauge split by sign q(v)", split), ("gauge-free split by sign of tau = sigma*deg", bal), ("degree parity", par)):
    pr(nm, {("floor" if k[0] else "non-floor") + ": " + k[1]: v for k, v in sorted(c.items())})
pr("tau of the single filled state in the", sum(tau_hist_floor1.values()), "floor classes with F=1:", dict(sorted(tau_hist_floor1.items())))
res["q1"] = {"sign_qv_equals_eps_failures": badsig, "tau_single_filled_floor": dict(sorted(tau_hist_floor1.items()))}
# Sum over filled of sigma*deg etc, per order, floor vs nonfloor
for fl in (True, False):
    c = collections.Counter(); 
    for r in R:
        if (4 * r["nF"] == r["size"]) != fl: continue
        Fs = [s for s in r["states"] if s["t"] == "F"]
        c["classes"] += 1; c["deg0_somewhere"] += any(s["deg"] == 0 for s in Fs)
        c["all_tau_equal"] += len({tau(s) for s in Fs}) == 1
    pr("floor" if fl else "non-floor", dict(c))

# ------------------------------------------------------------------ Q3a/Q4 : tau balance
pr("\n== block sums of W = eps*W_G (gauge free, integer for every state; for filled states W = 4*tau - 3)")
rows = []; info = []
for r in R:
    T = collections.Counter(); N = collections.Counter()
    for s in r["states"]: T[s["t"]] += Wn(s); N[s["t"]] += 1
    rows.append((T["F"], T["U"], T["D"], N["F"], N["U"], N["D"])); info.append(r)
cols = ["sumW_F", "sumW_U", "sumW_D", "nF", "nU", "nD"]
pr("relations among (class sums of W over F, over non-DL unfilled, over DL; counts F, U, D) -- all classes:", relations(rows, cols))
pr("   floor classes only:", relations([x for x, r in zip(rows, info) if 4 * r["nF"] == r["size"]], cols))
d0 = collections.Counter()
for x, r in zip(rows, info):
    fl = 4 * r["nF"] == r["size"]; d0[(fl, x[1] + x[2] - x[0] == 0)] += 1
pr("  [sum_U W + sum_D W == sum_F W] by (is floor class, holds):", dict(sorted(d0.items())))
res["tau_balance"] = {str(k): v for k, v in d0.items()}
pr("  floor classes where it fails:")
for x, r in zip(rows, info):
    if 4 * r["nF"] == r["size"] and x[1] + x[2] != x[0]: pr("    order", r["order"], "gentri", r["gentri_index"], "hole", r["hole"], "size", r["size"], "F", r["nF"], "(sumW_F,sumW_U,sumW_D)", x[:3], "defect", x[1] + x[2] - x[0])
pr("  non-floor classes where it holds:")
for x, r in zip(rows, info):
    if 4 * r["nF"] != r["size"] and x[1] + x[2] == x[0]: pr("    order", r["order"], "gentri", r["gentri_index"], "hole", r["hole"], "size", r["size"], "F", r["nF"], "fraction", Fraction(r["nF"], r["size"]))
reg = [(r, B) for r, B in fourblock if sum(Wn(s) for s in B["F"]) == sum(Wn(s) for n in ("U1", "U2", "DL") for s in B[n])]
pr("  4-block floor classes obeying it:", len(reg), "of", len(fourblock))
single = [(r, B) for r, B in fourblock if len(B["F"]) == 1]
pr("  of the", len(single), "classes with F=1 (4 states): W_F = W_U1+W_U2+W_DL in", sum(1 for r, B in single if Wn(B['F'][0]) == sum(Wn(B[n][0]) for n in ('U1', 'U2', 'DL'))))

# ------------------------------------------------------------------ Q2 block relations
def stat_pos(s, i):
    e = s["eps"]; q = s["qL"]; Q = [e * q[(i + k) % 5] for k in range(5)]
    d = {"W": Wn(s), "sumL": sum(Q), "posn": (s["pos"] if e > 0 else s["ntouch"] - s["pos"]), "sqL": sum(x * x for x in Q), "one": 1}
    for k in range(5): d["Q%d" % k] = Q[k]; d["Q%d^2" % k] = Q[k] ** 2; d["Q%dQ%d" % (k, (k + 1) % 5)] = Q[k] * Q[(k + 1) % 5]
    return d
names = ["F", "U1", "U2", "DL"]
def block_sums(Bset):
    out = []
    for r, B in Bset:
        i = B["i"]; S = {n: collections.Counter() for n in names}
        for n in names:
            for s in B[n]:
                for k, v in stat_pos(s, i).items(): S[n][k] += v
        out.append((len(B["F"]), S))
    return out
pr("\n== Q2: block sums of gauge-fixed charges in the four floor blocks (position frame: Qk = eps*q_G(x_{i+k}), i = singleton position of the filled block)")
pr("   roles: block U1 has repeat pair {i+1,i+3}: m=x_{i+2}, a=x_{i+4}, b=x_i; block U2 pair {i+2,i+4}: m=x_{i+3}, a=x_i, b=x_{i+1}; DL pair {i+4,i+1}: m=x_i, a=x_{i+2}, b=x_{i+3}.")
BS = block_sums(fourblock); BSreg = block_sums(reg)
res["block_relations"] = {}
for X in BS[0][1]["F"]:
    for tag, data in (("all 4-block classes", BS), ("regular (W-balanced) 4-block classes", BSreg)):
        rows = [tuple(S[n][X] for n in names) + (F,) for F, S in data]
        rel = relations(rows, ["S_F", "S_U1", "S_U2", "S_DL", "#F"])
        res["block_relations"].setdefault(X, {})[tag] = rel
        if tag.startswith("regular") or rel: pr("  %-8s %-40s null-space dim %d: %s" % (X, tag, len(rel), rel))
# nonzero-ness of the sign-flip relations
nz = collections.Counter()
for F, S in BS:
    for X in ("Q1", "Q4", "Q2", "Q3"): nz[X] += (S["F"][X] != 0)
pr("  classes (of %d) where the filled-block sum of Qk is nonzero (so the sign-flip relations are not vacuous):" % len(BS), dict(nz))
sg = collections.Counter()
for F, S in BS:
    sg[("S_F(Q1) sign", (S["F"]["Q1"] > 0) - (S["F"]["Q1"] < 0))] += 1; sg[("S_F(Q4) sign", (S["F"]["Q4"] > 0) - (S["F"]["Q4"] < 0))] += 1
    sg[("S_F(Q2) sign", (S["F"]["Q2"] > 0) - (S["F"]["Q2"] < 0))] += 1; sg[("S_F(Q3) sign", (S["F"]["Q3"] > 0) - (S["F"]["Q3"] < 0))] += 1
    sg[("S_DL(Q0) sign", (S["DL"]["Q0"] > 0) - (S["DL"]["Q0"] < 0))] += 1; sg[("S_F(Q0) sign", (S["F"]["Q0"] > 0) - (S["F"]["Q0"] < 0))] += 1
pr("  signs of block sums (gauge-fixed, so meaningful):", dict(sorted(sg.items())))
# per-state constancy inside blocks, and the state-wise sign pattern
pr("  per-state: Q_k constant inside a block (fraction of classes):")
const = collections.Counter()
for r, B in fourblock:
    for n in names:
        for k in range(5):
            const[(n, k)] += len({s["eps"] * s["qL"][(B["i"] + k) % 5] for s in B[n]}) == 1
pr("   ", {"%s Q%d" % key: "%d/%d" % (v, len(fourblock)) for key, v in sorted(const.items())})
# statewise: for classes where both are constant, compare value in block pairs
pat = collections.Counter()
for r, B in fourblock:
    for k in range(5):
        vals = {}
        for n in names:
            S = {s["eps"] * s["qL"][(B["i"] + k) % 5] for s in B[n]}
            if len(S) == 1: vals[n] = next(iter(S))
        if len(vals) == 4:
            F, U1, U2, DL = (vals[n] for n in names)
            pat[(k, "U1=F" if U1 == F else "U1=-F" if U1 == -F else "-", "U2=F" if U2 == F else "U2=-F" if U2 == -F else "-", "DL=F" if DL == F else "DL=-F" if DL == -F else "-")] += 1
pr("  value relations (block-constant cases): ", dict(sorted(pat.items(), key=lambda kv: (-kv[1]))[:20]))

# ------------------------------------------------------------------ Q3 identities over all classes
pr("\n== Q3: exact identities  sum_states(stat) = linear combination of F, U (non-DL unfilled), D (DL) counts")
def stats_all(s):
    e = s["eps"]; Q = [e * x for x in s["qL"]]
    d = {"W_gauge": e * s["W"], "sumL_partial": sum(Q), "pos_faces_at_link": (s["pos"] if e > 0 else s["ntouch"] - s["pos"]), "sumL_sq": sum(x * x for x in Q),
         "sum_adjacent_products": sum(Q[k] * Q[(k + 1) % 5] for k in range(5)), "W_sq": s["W"] ** 2}
    # raw (gauge dependent) versions as asked in the task
    d["RAW_sumL_partial"] = sum(s["qL"]); d["RAW_pos_faces_at_link"] = s["pos"]
    return d
def stats_roles(s):
    # unfilled only
    e = s["eps"]; j = s["k"]; Q = [e * s["qL"][(j + k) % 5] for k in range(5)]   # alpha, m, alpha, a, b
    d = {"Q_m": Q[1], "Q_a": Q[3], "Q_b": Q[4], "Q_alpha1": Q[0], "Q_alpha2": Q[2], "Qm^2": Q[1] ** 2, "Qa^2": Q[3] ** 2, "Qb^2": Q[4] ** 2, "QmQa": Q[1] * Q[3], "QmQb": Q[1] * Q[4], "QaQb": Q[3] * Q[4],
         "RAW_q_m": s["qL"][(j + 1) % 5], "RAW_q_a": s["qL"][(j + 3) % 5], "RAW_q_b": s["qL"][(j + 4) % 5]}
    return d
def stats_filled(s):
    e = s["eps"]; i = s["k"]; Q = [e * s["qL"][(i + k) % 5] for k in range(5)]; QF = [e * s["qLfull"][(i + k) % 5] for k in range(5)]
    d = {"tau=deg*sigma": tau(s)}
    for k in range(5): d["Q%d_partial" % k] = Q[k]; d["Q%d_full" % k] = QF[k]
    d["Qv(=3)"] = 3
    return d
def per_class(r, fn, types):
    S = collections.Counter(); N = collections.Counter()
    for s in r["states"]:
        N[s["t"]] += 1
        if s["t"] in types:
            for k, v in fn(s).items(): S[(s["t"], k)] += v
    return S, N
res["identities"] = {}
def scan(label, fn, types, subset):
    keys = None; table = []
    for r in subset:
        S, N = per_class(r, fn, types); table.append((S, N))
        if keys is None: keys = sorted({k for (t, k) in S}) if S else None
    if keys is None: return
    # re-collect keys over all
    keys = sorted({k for S, N in table for (t, k) in S})
    for X in keys:
        rows = []
        for S, N in table:
            rows.append(tuple(S[(t, X)] for t in types) + (N["F"], N["U"], N["D"]))
        cols = ["S_" + t for t in types] + ["#F", "#U", "#D"]
        rel = relations(rows, cols); res["identities"].setdefault(label, {})[X] = rel
        pr("  [%s] %-24s null-space dim %d %s" % (label, X, len(rel), rel))
def tau_balanced(r):
    T = collections.Counter()
    for s in r["states"]: T[s["t"]] += Wn(s)
    return T["U"] + T["D"] == T["F"]
regfloor = [r for r in nfl if tau_balanced(r)]
for lab, subset in (("all classes", R), ("floor classes", nfl), ("floor classes with W balance (%d)" % len(regfloor), regfloor), ("4-block classes", [r for r, B in fourblock])):
    pr(" -- subset:", lab, len(subset))
    scan(lab + " / all states", stats_all, ("F", "U", "D"), subset)
    scan(lab + " / unfilled roles", stats_roles, ("U", "D"), subset)
    scan(lab + " / filled positions", stats_filled, ("F",), subset)

# ------------------------------------------------------------------ Q4
pr("\n== Q4: does a charge quantity predict the filled fraction?")
sl = []
for x, r in zip(rows if False else [None] * len(R), R): pass
tot = 0
cl = collections.Counter()
for r in R:
    Ff = r["nF"]; slack = r["size"] - 4 * Ff   # >= 0 by the floor; unfilled - 3F
    T = collections.Counter()
    for s in r["states"]: T[s["t"]] += Wn(s)
    d = T["U"] + T["D"] - T["F"]
    cl[(slack == 0, d == 0)] += 1
pr("(is floor class, defect sum_U W + sum_D W - sum_F W == 0):", dict(sorted(cl.items())))
json.dump(res, open(os.path.join(H, "results.json"), "w"), indent=1, default=str)
