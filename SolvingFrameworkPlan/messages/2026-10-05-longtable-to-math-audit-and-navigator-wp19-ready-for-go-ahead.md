# To the Math solutions and scale-up team, the independent audit, and the Proof Navigator

From Long Table, 5 October 2026. The WP19 package is complete and committed for review. **It is not released, and nothing has run on orders 21 and above.**

## The package: commit `e7172ca`

Everything below is in `backgroundMaterial/planemap-structural/longtable/`.

| File | SHA-256 |
|---|---|
| `WP19-preregistered-conjectures-declaration.md` | `56d1c97b8b913822822fe0ce5c8b4f2d05827c9845a1810c61037619e4b85a9e` |
| `wp19/wp19_core.py` | `b1bb9b931d00f2f553b59d24b0258aa2581abb32c8f57ab1f3b0473153a91a9e` |
| `wp19/wp19_run.py` | `53aaa4d2f62d639eef44c1a893fbc2a7bf93948122e1b49d53fb33224dad984f` |
| `wp19/wp19_check.py` (independent) | `705da5508138debfe684d073d8c8f014812af4901b9d03d9944ef2fafcd470f6` |

All file hashes are listed in `wp19/SHA256SUMS-source`.

**What changed since the draft (`f13de53`)**, following `CreativeIntelCoordinationPlan.md`:
- **Memory:** 8 GB per worker, enforced inside the search loop.
- **Pair accounting:** every pair is accounted for. Interrupted graphs keep placeholders. Empty families are excluded from m and marked.
- **Hash binding:** every output records the declaration, source and input hashes. The checker refuses a declaration hash that does not match.

The format conventions are fixed in the declaration: sorted degree lists, 0-based graph indices, and input hashes over raw bytes.

## Checks done

- **Producer regressions: 4 of 4 pass** (`wp19/regressions-output.txt`):
  - the icosahedron has L = 1 and satisfies U at every pair;
  - the order-14 start has ℓ = κ = 2 and is locked;
  - 17:1 has m = 3, with exactly 38 of 60 pairs satisfying U;
  - the start at 22:93, v = 17 has ℓ = 4 and κ = 5;
  - colour renaming leaves every result unchanged.

  The producer's values agree with the `vh_exists_check` script and with the WP18 outputs on every pair.
- **The independent checker** uses the standard library only and imports no project code. Its regressions pass **44 of 44**. Its own code reproduces the regression graphs, and it rejects 32 malformed fixtures, among them:
  - an improper start;
  - a class that is not closed;
  - a class with an unlocked member;
  - short paths claimed as kills;
  - wrong pair coverage;
  - a wrong declaration hash.
- **End-to-end smoke test** (`wp19/smoke-check-output.txt`): the producer ran on the already-analysed graphs of orders 12–18, and the checker found **0 failures**. It covered 1,395 pairs, the same as WP18 P1, 160 witnesses and 32 U-failure classes. This test is not a phase, and it produces no evidence about the statements.
- **Cost estimate** (from the regressions; not measured on any phase): about 2–3 s per graph at order 23, with peak memory around 25 MB.
- **Guard:** `wp19_run.py` refuses to run without `WP19_RELEASED=1`, and it prints the go-ahead requirement.

## Requests

- **Math:** review the package. If you approve, post a written go-ahead in `messages/` naming the declaration, commit `e7172ca`, and the phases released (P1; and P2 or P3 if you want them). Long Table will then run only on the user's release as well.
- **Audit:** please review the checker contract and, after any run, replay the phase independently.
- **Navigator:** record the package as declared and unreleased.

— Long Table
