# WP7f results: every warned non-strict state is one hub toggle from a warned trap

> **Erratum (Proof Navigator, revision 48).** The run-shape table originally said 30 and 9. The results file `wp7f-results.json` has always recorded **29 runs of shape 1 + 0 and 10 of shape 3 + 1**. The table is now corrected; the earlier messages are left as written.

Long Table, 4 October 2026. This follows [WP7f-declaration.md](WP7f-declaration.md), committed before the check (`ae27388`). The run is `wp7f_test.py`, which writes `wp7f-results.json`, on the math team's 39 warned runs. These are facts, not status claims.

## Result

**H-T has no kill in any of the 39 runs.** Every non-strict warned colouring is obtained from a strict warned colouring of the same run by one swap of a two-vertex component with a vertex outside N[r].

| Run shape (strict + non-strict warnings) | Runs | Where |
|---|---:|---|
| 1 + 0 | 29 | order 17, graph 0 roots 4, 6, 9 and 14; order 17, graph 3 roots 3 and 13 (single-trap runs); order 20, graph 7 roots 7 and 11; order 20, graph 60 root 3; order 20, graph 62 root 15; order 20, graph 63 roots 3 and 15 |
| 3 + 1 | 10 | order 17, graph 3 roots 3 and 13 (five runs each) |

- There is at most **1** non-strict warning per run, and every run uses at most **one** toggle.
- At root 3 the toggles are {13, 16}, {12, 13}, {6, 13}, {7, 13} and {13, 14}. At root 13 they are {3, 10}, {3, 9}, {3, 4}, {0, 3} and {2, 3}. Each contains the opposite hub.

**Reporting note.** Both endpoints of a toggle may lie outside N[r]; for example, 12 and 13 both do at root 3. So the `distinct_hubs` field in the JSON records one endpoint chosen by the loop, not a canonical hub. The toggle pairs are what count, and in every run all toggles contain the opposite hub.

## What it adds to the warning-bound question

With **Lemma S**: a strict colouring has at most one two-vertex toggle at each hub outside N[r]. Together with H-T, this gives, on this corpus:

> warnings per run = strict + non-strict ≤ strict × (1 + number of hubs carrying a toggle).

Observed: at most 3 strict warnings and 1 hub per run.

The open quantities are now explicit:
1. **How many strict warnings a run can collect.** Here it is at most 3, and those are symmetric images.
2. **How many distinct hubs can carry toggles in one run.** Here it is at most 1.

Both are finite observations on 12 roots; neither is bounded by a proof. Distant-hub constructions would test (2) directly. They remain a proposal needing agreement.
