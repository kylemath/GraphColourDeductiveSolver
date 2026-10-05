# To the Math solutions and scale-up team (copy to the audit chat and the Proof Navigator)

From Long Table, 5 October 2026. **At the user's request, we are handing the WP19 run to you.** Long Table is pausing for capacity. The package is committed as `e7172ca`, and the go-ahead request is in `12cc070`.

## Before running

1. Post your written go-ahead in `messages/`. Name `WP19-preregistered-conjectures-declaration.md` (SHA-256 `56d1c97b…a9e`), commit `e7172ca`, and the phases released.
2. Confirm the user's release.
3. Check that the source is unchanged:

```bash
cd backgroundMaterial/planemap-structural/longtable/wp19 && shasum -a 256 -c SHA256SUMS-source
```

## Running

plantri 5.8 reproduces the recorded hashes. A built binary is at `/private/tmp/planemap-next/plantri58/plantri`, from source tarball `e78a9441…29b8`.

```bash
cd backgroundMaterial/planemap-structural/longtable/wp19 && python3 wp19_regressions.py && python3 wp19_check_regressions.py
```

```bash
cd backgroundMaterial/planemap-structural/longtable/wp19 && WP19_RELEASED=1 PLANTRI=/private/tmp/planemap-next/plantri58/plantri python3 wp19_run.py P1 --procs 12
```

- P1 is order 23: 2,070 graphs, an estimated 2–3 s per graph. The plantri output must hash to `d233b4ef…afa`, and the script asserts this.
- P2 (U∃ only, orders 21–22) and P3 (order 24) are optional. They run with the same command, using `P2` or `P3`.

## Checking

```bash
cd backgroundMaterial/planemap-structural/longtable/wp19 && python3 wp19_check.py wp19-P1.json
```

The checker refuses the file if the declaration hash differs. It verifies every certificate:
- witnesses, by complete layer exclusion;
- U-failure classes, by closure and by every member being locked;
- M1–M3 and C1–C3 kills, and the U∃ kill.

Histograms and upper bounds are producer claims. We ask the audit chat to replay the phase independently.

## Reporting

Report per statement (M1, M2, M3, C1, C2, C3, U∃) as one of:
- **killed**, with its certificate;
- **passed on these graphs**, which is not evidence of truth beyond them;
- **unresolved**.

Also report m and the histograms, cost, peak memory, interruptions and the output digests. Every statement is a post hoc candidate. Order 23 is new for these statistics but was exposed to the night swarm's q/lin sweeps.

## Other open items Long Table leaves with you

- Written acceptance or refusal of the finite WP18 statement (independently replayed in full).
- Review of `swarm/belt-joined.md`, which passed the audit's hand review. Its dependencies are cited: Florek's Theorem 3.1 (checked against the primary paper) and the family identification.
- Review of `swarm/vh-exists.md`: VH∃ implies 4-colourability, containment, apex singleton, and the candidate U∃. The audit's adversarial review is in progress.

— Long Table
