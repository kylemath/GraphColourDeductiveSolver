"""Long Table broadening search: alternative ranks under the same two-swap macro.

DECLARATION (frozen before any run; committed before results exist).
Each variant is a separately stated candidate, never a renaming of mass-macro descent.  All
use the same class, root set D(T), moves (single whole bichromatic components, components
missing B included), macro bound 2 with components recomputed, and termination at p = 0.
Every rank is computable in polynomial time with a polynomial integer range.

For a non-target colouring (four colours on the five boundary vertices B) call a boundary
vertex a *singleton* when its colour occurs once on B.  For a singleton v and another colour x,
the pair (c(v), x) is *linked* at v when v's (c(v), x)-component meets B outside v.
L(c) = number of linked (singleton, x) pairs, 0..9.  L(c) < 9 exactly when some single swap
reaches a target (a singleton freed in some pair).  L = 0 at targets by convention.

  base   lex(p, q)                          the published formula, as control
  lock   lex(p, L, q)                       unlock first, then mass
  lockq  lex(p, q + (n^2) * L)              lock as a heavy additive term (same order as lock)
  lin    lex(p, sum |K minus B|)            linear mass
  full   lex(p, sum |K|^2)                  boundary vertices counted in the mass
  rep    lex(p, q restricted to the three pairs containing the repeated boundary colour)
  Lonly  lex(p, L)                          lock count alone

ROUND 2 (declared after round-1 discovery results, before any round-2 run).  Round 1 left only
the orbit {4, 6} of order 17 graph 0 failing under lock, lockq and lin.  Round 2 variants:
  Lall    every boundary vertex v (singletons and both repeated-colour vertices) and colour
          x != c(v): count pairs where v's (c(v), x)-component meets B outside v.  0..15.
  links   number of (pair, component) with |K meet B| >= 2, i.e. boundary-linking chains.
  lockL   lex(p, L, lin)
  linq    lex(p, lin, q)
  Lallq   lex(p, Lall, q)
  linksq  lex(p, links, q)
  linksl  lex(p, links, lin)
Same protocol, run with --round 2; round-1 results are not rerun or altered.

Protocol (also frozen):
  1. Discovery: orders 12-18 only.  Report failing roots and graphs with every root failing.
  2. Any variant with zero failing roots on discovery advances to holdout orders 19-20.
     No other variant is evaluated on 19-20 in this run.
  3. Results are Long Table exploratory evidence.  A surviving variant is handed to the
     corpus team for an official, independently checked sweep; no status is claimed.
"""
import argparse
import hashlib
import json
from pathlib import Path

from mass_core import FIXTURES, HERE, PAIRS, degree_five, parse_ascii, RootState

VARIANTS = ["base", "lock", "lockq", "lin", "full", "rep", "Lonly"]
VARIANTS2 = ["base", "lockL", "linq", "Lallq", "linksq", "linksl"]


def components(state, c):
    out = []
    for a, b in PAIRS:
        pending = {i for i, x in enumerate(c) if x in (a, b)}
        while pending:
            seed = min(pending)
            pending.discard(seed)
            comp, stack = {seed}, [seed]
            while stack:
                i = stack.pop()
                for j in state.adj[i]:
                    if j in pending:
                        pending.discard(j)
                        comp.add(j)
                        stack.append(j)
            out.append(((a, b), comp))
    return out


def ranks(state, i):
    c = state.C[i]
    B = state.B
    cols = [c[j] for j in B]
    p = max(0, len(set(cols)) - 3)
    comps = components(state, c)
    Bset = state.Bset
    q = sum(len(K - Bset) ** 2 for _, K in comps if K & Bset)
    lin = sum(len(K - Bset) for _, K in comps if K & Bset)
    full = sum(len(K) ** 2 for _, K in comps if K & Bset)
    L, rep, Lall = 0, 0, 0
    links = sum(1 for _, K in comps if len(K & Bset) >= 2)
    if p == 1:
        counts = {x: cols.count(x) for x in set(cols)}
        repeated = next(x for x, k in counts.items() if k == 2)
        rep = sum(len(K - Bset) ** 2 for pr, K in comps if K & Bset and repeated in pr)
        where = {}
        for pr, K in comps:
            for j in K:
                where[(pr, j)] = K
        for j in B:
            a = c[j]
            if counts[a] != 1:
                continue
            for x in range(4):
                if x == a:
                    continue
                K = where[(tuple(sorted((a, x))), j)]
                if (K & Bset) - {j}:
                    L += 1
        for j in B:
            for x in range(4):
                if x != c[j] and (where[(tuple(sorted((c[j], x))), j)] & Bset) - {j}:
                    Lall += 1
    n2 = state.n * state.n
    return {"base": (p, q), "lock": (p, L, q), "lockq": (p, q + n2 * L), "lin": (p, lin),
            "full": (p, full), "rep": (p, rep), "Lonly": (p, L),
            "lockL": (p, L, lin), "linq": (p, lin, q), "Lallq": (p, Lall, q),
            "linksq": (p, links, q), "linksl": (p, links, lin)}


def root_failures(rot, r, variants):
    s = RootState(rot, r)
    rk = [ranks(s, i) for i in range(len(s.C))]
    nxt = [[t for _, _, t in s.info[i]["moves"]] for i in range(len(s.C))]
    out = {}
    for v in variants:
        stuck = []
        for i in range(len(s.C)):
            if rk[i][v][0] != 1:
                continue
            start = rk[i][v]
            if any(rk[t][v] < start for t in nxt[i]):
                continue
            if any(rk[u][v] < start for t in nxt[i] for u in nxt[t]):
                continue
            stuck.append(i)
        out[v] = {"stuck": len(stuck), "first": list(s.C[stuck[0]]) if stuck else None}
    return out, s.V


def run(orders, variants):
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    result = {v: {"failing_roots": [], "graphs_all_fail": []} for v in variants}
    for o in table["orders"]:
        if o["order"] not in orders:
            continue
        for g in o["graphs_checked"]:
            rot = parse_ascii(g["ascii"])
            per = {}
            for r in degree_five(rot):
                f, V = root_failures(rot, r, variants)
                per[r] = f
                if "base" in variants:
                    published = next(x for x in g["roots"] if x["root"] == r)
                    assert (f["base"]["stuck"] > 0) == (published["outcome"] == "fails"), (o["order"], g["graph_index"], r)
                for v in variants:
                    if f[v]["stuck"]:
                        result[v]["failing_roots"].append({"order": o["order"], "graph_index": g["graph_index"],
                                                           "root": r, "stuck": f[v]["stuck"], "vertex_order": V,
                                                           "first_stuck": f[v]["first"]})
            for v in variants:
                if all(per[r][v]["stuck"] for r in per):
                    result[v]["graphs_all_fail"].append((o["order"], g["graph_index"]))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stage", choices=["discovery", "holdout"], required=True)
    ap.add_argument("--round", type=int, choices=[1, 2], default=1)
    args = ap.parse_args()
    variants = VARIANTS if args.round == 1 else VARIANTS2
    tag = "" if args.round == 1 else "-round2"
    disc_path = HERE / f"broaden-discovery{tag}.json"
    if args.stage == "discovery":
        res = run(set(range(12, 19)), variants)
        out = {"stage": "discovery", "round": args.round, "orders": "12-18", "variants": variants, "results": res}
        path = disc_path
    else:
        disc = json.loads(disc_path.read_text())
        advancing = [v for v in variants if v != "base" and not disc["results"][v]["failing_roots"]]
        res = run({19, 20}, advancing) if advancing else {}
        out = {"stage": "holdout", "round": args.round, "orders": "19-20", "advancing": advancing, "results": res}
        path = HERE / f"broaden-holdout{tag}.json"
    out["scope"] = ("Long Table exploratory screen of predeclared alternative ranks under the two-swap macro. "
                    "Finite evidence only; no status claims; survivors go to the corpus team.")
    out["checkers"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (HERE / "broaden_variants.py", HERE / "mass_core.py")}
    path.write_text(json.dumps(out, indent=1) + "\n")
    for v, r in out["results"].items():
        roots = sorted({(x["order"], x["graph_index"], x["root"]) for x in r["failing_roots"]})
        print(f"{v:<6} failing roots {len(roots):>3}  graphs with all roots failing {len(r['graphs_all_fail'])}"
              f"  {roots[:8]}{' ...' if len(roots) > 8 else ''}")
    if args.stage == "holdout":
        print("advancing:", out["advancing"])


if __name__ == "__main__":
    main()
