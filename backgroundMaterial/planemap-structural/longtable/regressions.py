"""Long Table WP2: named regression fixtures for mass-macro descent and (sigma, beta).

Fixtures (JointMassMacroExecutionPlan.md, section 2): graph 36 of order 20 (zero-based) with
its eight exterior degree-five roots; its root-8 one-swap local minima and two-swap escapes;
the spherical icosahedron.  Plus permutation regressions on graph 36 root 8.  No corpus-wide
enumeration.  Standard library only.  Reports facts, not statuses.
"""
import argparse
import hashlib
import json
import random
from pathlib import Path

from mass_core import (FIXTURES, HERE, PAIRS, RootState, degree_five, parse_ascii, relabel,
                       rotation_from_fixture, sigma_beta)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def raw_rank(rot, r, colouring):
    """R evaluated directly on an arbitrary (non-canonical) colouring dict v -> colour."""
    n, B = len(rot), set(rot[r])
    q = 0
    for a, b in PAIRS:
        pending = {v for v, x in colouring.items() if x in (a, b)}
        while pending:
            seed = pending.pop()
            comp, stack = {seed}, [seed]
            while stack:
                v = stack.pop()
                for w in rot[v]:
                    if w in pending:
                        pending.discard(w)
                        comp.add(w)
                        stack.append(w)
            if comp & B:
                q += len(comp - B) ** 2
    p = max(0, len({colouring[v] for v in B}) - 3)
    return (6 * n * n + 1) * p + q


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=HERE / "regressions.json")
    ap.add_argument("--seed", type=int, default=20261004)
    ap.add_argument("--relabellings", type=int, default=6)
    args = ap.parse_args()
    checks, out = [], {}

    def check(name, ok, detail=None):
        checks.append({"check": name, "ok": bool(ok), **({"detail": detail} if detail is not None else {})})
        print(("PASS " if ok else "FAIL ") + name + ("" if detail is None else f"  {detail}"))

    # ---- inputs and hashes
    corpus = FIXTURES / "triangulations-min5-20.txt"
    census = json.loads((FIXTURES / "search-results.json").read_text())
    recorded20 = next(o for o in census["orders"] if o["order"] == 20)
    check("order-20 corpus file hash equals census input_sha256",
          sha(corpus) == recorded20["input_sha256"], sha(corpus))
    line = corpus.read_text().splitlines()[36]
    afternoon = json.loads((FIXTURES / "afternoon-checks.json").read_text())
    component = json.loads((FIXTURES / "component-mass-results.json").read_text())
    check("graph 36 ASCII equals afternoon-checks record", line == afternoon["ascii"])
    check("graph 36 ASCII equals component-mass record", line == component["ascii"])
    check("graph 36 ASCII equals census record",
          line == recorded20["graphs_checked"][36]["ascii"])
    rot = parse_ascii(line)

    # ---- fixture 1: eight exterior roots, (sigma, beta)
    anchor = 0
    eligible = [r for r in degree_five(rot) if r != anchor and r not in rot[anchor]]
    check("exterior degree-five roots of anchor 0", eligible == afternoon["eligible_roots"], eligible)
    sb_rows = []
    for r in eligible:
        got = sigma_beta(rot, r)
        want = next(row for row in afternoon["root_replays"] if row["root"] == r)
        same = all(got[k] == want[k] for k in ("boundary", "coloring_orbits", "groups",
                                               "losing_groups", "winning_rounds"))
        check(f"(sigma,beta) root {r} matches afternoon-checks", same,
              {k: got[k] for k in ("coloring_orbits", "groups", "losing_groups", "winning_rounds")})
        sb_rows.append(got)
    check("only root 8 loses (sigma,beta) among exterior roots",
          [row["root"] for row in sb_rows if row["losing_groups"]] == [8])
    out["graph36_sigma_beta"] = sb_rows

    # ---- fixture 2: root 8 mass macro
    state = RootState(rot, 8)
    state.check_closure()
    m = state.mass_summary()
    check("root 8 orbit and non-target counts", (m["coloring_orbits"], m["non_target"]) == (198, 131),
          (m["coloring_orbits"], m["non_target"]))
    check("root 8 vertex order matches component-mass", state.V == component["vertex_order"])
    check("root 8 one-swap stuck orbits = 3", m["one_swap_stuck"] == 3, m["one_swap_stuck"])
    published_min = {tuple(c) for c in component["all_local_minimum_colorings"]}
    check("root 8 one-swap stuck colourings identical to published",
          set(map(tuple, m["one_swap_stuck_colorings"])) == published_min)
    w = m["one_swap_first_stuck"]
    succ = sorted({tuple(x["rank"]) for x in w["one_step"]})
    check("first stuck rank (1,190) with successor ranks as published",
          tuple(w["rank"]) == tuple(component["witness"]["potential"]) and
          succ == sorted(tuple(x) for x in component["witness"]["successor_potentials"]),
          {"rank": w["rank"], "successors": succ})
    check("root 8 two-swap stuck orbits = 0", m["two_swap_stuck"] == 0, m["two_swap_stuck"])
    published_escapes = {tuple(row["start"]): row["two_swap_decrease"]
                         for row in afternoon["component_mass_two_swap_checks"]}
    replayed = True
    for row_start, esc in published_escapes.items():
        i = state.index[row_start]
        first = next(t for mv, k, t in state.info[i]["moves"]
                     if state.C[t] == tuple(esc["intermediate"]))
        end_ok = any(state.C[u] == tuple(esc["end"]) for _, _, u in state.info[first]["moves"])
        replayed &= end_ok and state.info[state.index[tuple(esc["end"])]]["R"] < state.info[i]["R"]
    check("published two-swap escapes replay as legal decreasing macros", replayed)
    out["graph36_root8_mass"] = m

    # ---- permutation regressions (implementation checks, not proofs)
    rng = random.Random(args.seed)
    base = (m["coloring_orbits"], m["non_target"], m["one_swap_stuck"], m["two_swap_stuck"])
    base_ranks = sorted(info["R"] for info in state.info)
    perm_rows = []
    for k in range(args.relabellings):
        perm = list(range(len(rot)))
        rng.shuffle(perm)
        rrot = relabel(rot, perm)
        img = RootState(rrot, perm[8])
        mm = img.mass_summary(keep_witness=False)
        got = (mm["coloring_orbits"], mm["non_target"], mm["one_swap_stuck"], mm["two_swap_stuck"])
        ranks = sorted(info["R"] for info in img.info)
        sb = {perm[r]: sigma_beta(rrot, perm[r])["losing_groups"] for r in eligible}
        perm_rows.append({"perm": perm, "image_root": perm[8], "mass_counts": got,
                          "rank_multiset_equal": ranks == base_ranks,
                          "sigma_beta_losing_by_image_root": sb})
        check(f"relabelling {k}: mass counts and rank multiset invariant",
              got == base and ranks == base_ranks, got)
    colour_ok = True
    for i in rng.sample(range(len(state.C)), 25):
        col = dict(zip(state.V, state.C[i]))
        for sigma in ([1, 0, 2, 3], [3, 2, 1, 0], [2, 3, 0, 1], [1, 2, 3, 0]):
            colour_ok &= raw_rank(rot, 8, {v: sigma[x] for v, x in col.items()}) == state.info[i]["R"]
    check("colour permutations leave R unchanged (25 states x 4 permutations)", colour_ok)
    out["permutation_regressions"] = perm_rows
    changed = sum(any(sb_row["losing_groups"] != row["sigma_beta_losing_by_image_root"][row["perm"][sb_row["root"]]]
                      for sb_row in sb_rows) for row in perm_rows)
    out["sigma_beta_relabelling_diagnostic"] = {
        "relabellings_changing_some_exterior_root_outcome": changed,
        "note": "Diagnostic only. (sigma,beta) is label-sensitive by construction; a change is expected behaviour, not an implementation error."}
    print(f"diagnostic: (sigma,beta) outcome changed under {changed}/{len(perm_rows)} relabellings")

    # ---- fixture 3: icosahedron
    ico_path = FIXTURES / "icosahedron-fixture.json"
    irot = rotation_from_fixture(ico_path)
    ico = []
    for r in range(12):
        s = RootState(irot, r)
        s.check_closure()
        mm = s.mass_summary(keep_witness=False)
        mm["max_target_distance"] = s.target_distance_max()
        ico.append(mm)
    check("icosahedron: 20 orbits at every root", all(x["coloring_orbits"] == 20 for x in ico))
    check("icosahedron: target within one swap at every root",
          all(x["max_target_distance"] <= 1 for x in ico))
    check("icosahedron: every root good under the two-swap mass macro",
          all(x["good_macro2"] for x in ico),
          {"one_swap_stuck_by_root": [x["one_swap_stuck"] for x in ico]})
    out["icosahedron"] = ico

    out = {"scope": "Named regression fixtures only (graph 36 order 20, icosahedron). Not a corpus "
                    "result, not coverage, no status claims.",
           "formula_version": "mass-macro v1: R=(6n^2+1)p+q, macro<=2, components recomputed",
           "inputs": {p.name: sha(p) for p in (corpus, FIXTURES / "search-results.json",
                                               FIXTURES / "afternoon-checks.json",
                                               FIXTURES / "component-mass-results.json", ico_path)},
           "checkers": {p.name: sha(p) for p in (HERE / "mass_core.py", HERE / "regressions.py")},
           "seed": args.seed, "all_passed": all(c["ok"] for c in checks), "checks": checks, **out}
    args.output.write_text(json.dumps(out, indent=1) + "\n")
    print("all passed:", out["all_passed"])


if __name__ == "__main__":
    main()
