"""Long Table WP3 adversary: candidate root set in, first failing graph out.

Consumes published per-root result tables; it never re-enumerates the corpus.  Each graph
is identified by order, zero-based graph index, exact ASCII rotation and the whole-file
hash recorded by the census.  Outcomes follow JointMassMacroExecutionPlan.md:

  root      - a root in D(T) fails the named check            (refutes Good(T, r) / a (sigma,beta) win)
  set       - the candidate set S(T) contains a failing root  (refutes its every-member guarantee)
  selector  - the stated tie-break picks a failing root       (refutes that selector only)
  existential - every root in D(T) fails                      (refutes the existential claim for that check)

Checks:
  sigma-beta : bit-search-results.json, failure = losing_groups > 0.  Label-sensitive: a
               (sigma,beta) result is a fact about one labelling, not about the graph.
  mass       : mass-macro-results.json published by the corpus team (MassMacroCorpusReport.md):
               orders[].graphs_checked[].{graph_index, ascii, ascii_sha256, roots[]}, per-root
               outcome "passes" or "fails"; ascii_sha256 is UTF-8 of the line without newline.
               Its whole-file hash is checked against mass-macro-SHA256SUMS.

Reports facts only; the navigator assigns statuses.
"""
import argparse
import hashlib
import json
from pathlib import Path

from mass_core import FIXTURES, HERE, degree_five, parse_ascii


# ---------------------------------------------------------------- candidate sets
# Each rule: (description, set function rot -> set of roots, tie-break).  Rules are frozen
# here before any mass-macro table exists; see LongTableWorkPlan.md WP4.

def s0(rot):
    """S0 = D(T)."""
    return set(degree_five(rot))


def five_neighbours(rot, v):
    return sum(len(rot[w]) == 5 for w in rot[v])


def s1_max(rot):
    """S1+ = argmax over D(T) of the number of degree-five neighbours."""
    D = degree_five(rot)
    best = max(five_neighbours(rot, v) for v in D)
    return {v for v in D if five_neighbours(rot, v) == best}


def s1_min(rot):
    """S1- = argmin over D(T) of the number of degree-five neighbours."""
    D = degree_five(rot)
    best = min(five_neighbours(rot, v) for v in D)
    return {v for v in D if five_neighbours(rot, v) == best}


def exterior_of_min_anchor(rot):
    """Label-based regression rule: degree-five roots outside the closed star of vertex 0.

    Not equivariant (depends on which vertex is labelled 0).  With tie-break min it is the
    killed smallest-label exterior-root rule of AnchorRuleReport.md.
    """
    a = 0
    return {v for v in degree_five(rot) if v != a and v not in rot[a]}


RULES = {
    "S0": ("all degree-five roots", s0, True),
    "S1+": ("degree-five roots with the most degree-five neighbours", s1_max, True),
    "S1-": ("degree-five roots with the fewest degree-five neighbours", s1_min, True),
    "anchor-min": ("exterior degree-five roots of vertex 0 (label-based regression rule)",
                   exterior_of_min_anchor, False),
}


def tie_break(candidates):
    """Deterministic tie-break: smallest label.  Label-based by design (allowed by the plan)."""
    return min(candidates)


# ---------------------------------------------------------------- tables

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_corpus():
    census = json.loads((FIXTURES / "search-results.json").read_text())
    corpus = {}
    for o in census["orders"]:
        path = FIXTURES / f"triangulations-min5-{o['order']}.txt"
        assert sha(path) == o["input_sha256"], f"corpus file hash mismatch at order {o['order']}"
        lines = path.read_text().splitlines()
        assert len(lines) == o["graphs"]
        for gi, line in enumerate(lines):
            assert o["graphs_checked"][gi]["ascii"] == line
            corpus[(o["order"], gi)] = line
    return corpus


def load_table(path, failed, corpus):
    data = json.loads(Path(path).read_text())
    table = {}
    for o in data["orders"]:
        for g in o["graphs_checked"]:
            key = (o["order"], g["graph_index"])
            assert corpus[key] == g["ascii"], f"ASCII mismatch at {key}"
            if "ascii_sha256" in g:
                assert hashlib.sha256(g["ascii"].encode()).hexdigest() == g["ascii_sha256"], key
            assert not g.get("no_start_coloring_roots"), f"empty colouring family at {key}"
            table[key] = {r["root"]: failed(r) for r in g["roots"]}
    return table


def manifest_hash(manifest, name):
    for line in Path(manifest).read_text().splitlines():
        digest, _, file = line.partition("  ")
        if Path(file).name == name:
            return digest
    raise KeyError(name)


def mass_outcome(r):
    assert r["outcome"] in ("passes", "fails"), r["outcome"]
    return r["outcome"] == "fails"


# ---------------------------------------------------------------- adversary

def evaluate(rule_name, corpus, table, source):
    desc, fn, equivariant = RULES[rule_name]
    rows, first = [], {"set": None, "selector": None, "existential": None}
    counts = {"graphs": 0, "set": 0, "selector": 0, "existential": 0, "empty_set": 0}
    for key in sorted(table):
        rot = parse_ascii(corpus[key])
        D = set(degree_five(rot))
        fails = table[key]
        assert set(fails) == D, f"table roots differ from D(T) at {key}"
        S = fn(rot)
        assert S <= D
        counts["graphs"] += 1
        if not S:
            counts["empty_set"] += 1
            continue
        bad_in_set = sorted(v for v in S if fails[v])
        pick = tie_break(S)
        row = {"order": key[0], "graph_index": key[1], "D_size": len(D), "set": sorted(S),
               "failing_roots": sorted(v for v in D if fails[v]), "failing_in_set": bad_in_set,
               "selected": pick, "selected_fails": fails[pick],
               "existential": all(fails.values())}
        rows.append(row)
        for kind, hit in (("set", bad_in_set), ("selector", fails[pick]), ("existential", row["existential"])):
            if hit:
                counts[kind] += 1
                if first[kind] is None:
                    first[kind] = {"order": key[0], "graph_index": key[1], "ascii": corpus[key],
                                   "roots": bad_in_set if kind == "set" else [pick] if kind == "selector"
                                   else sorted(D), "witness_source": source}
    return {"rule": rule_name, "description": desc, "equivariant_set": equivariant,
            "tie_break": "smallest label", "counts": counts, "first_failures": first, "per_graph": rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", choices=["sigma-beta", "mass"], default="sigma-beta")
    ap.add_argument("--mass-table", type=Path, default=FIXTURES / "mass-macro-results.json",
                    help="Published per-root mass-macro table (corpus team).")
    ap.add_argument("--rules", nargs="*", default=list(RULES))
    ap.add_argument("--max-order", type=int, default=20,
                    help="Evaluate only orders <= this (holdout: discovery uses <= 18).")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    corpus = load_corpus()
    if args.check == "sigma-beta":
        source = FIXTURES / "bit-search-results.json"
        table = load_table(source, lambda r: r["losing_groups"] > 0, corpus)
        note = "(sigma,beta) is label-sensitive; results describe the Plantri labelling only."
    else:
        source = args.mass_table
        assert sha(source) == manifest_hash(FIXTURES / "mass-macro-SHA256SUMS", Path(source).name), \
            "mass table does not match mass-macro-SHA256SUMS"
        table = load_table(source, mass_outcome, corpus)
        note = "Mass-macro goodness is isomorphism-invariant (InvarianceNote.md)."
    table = {k: v for k, v in table.items() if k[0] <= args.max_order}
    results = [evaluate(name, corpus, table, Path(source).name) for name in args.rules]
    out = {"scope": "Finite adversarial evaluation of predeclared candidate sets against a published "
                    "per-root table. Passing is evidence, not coverage; no status claims.",
           "check": args.check, "note": note, "max_order": args.max_order,
           "inputs": {Path(source).name: sha(source), "search-results.json": sha(FIXTURES / "search-results.json")},
           "checkers": {p.name: sha(p) for p in (HERE / "adversary.py", HERE / "mass_core.py")},
           "results": results}
    suffix = "" if args.max_order == 20 else f"-max{args.max_order}"
    output = args.output or HERE / f"adversary-{args.check}{suffix}.json"
    output.write_text(json.dumps(out, indent=1) + "\n")
    for res in results:
        c, f = res["counts"], res["first_failures"]
        def at(x):
            return "none" if x is None else f"order {x['order']} graph {x['graph_index']} roots {x['roots']}"
        print(f"{res['rule']:<10} graphs {c['graphs']:>3}  set-fail {c['set']:>3}  selector-fail {c['selector']:>3}"
              f"  existential {c['existential']:>3}  | first selector failure: {at(f['selector'])}")
    print("existential failures (all roots fail):", results[0]["counts"]["existential"] if results else "n/a")


if __name__ == "__main__":
    main()
