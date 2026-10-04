# WP7f declaration: are all warned non-strict states hub toggles away from a trap?

Long Table, 4 October 2026. Committed **before** the check. The input is the math team's `breadcrumb-warning-traces.json`: 39 warned runs at 12 roots, hash-checked, with no new colourings and no orders beyond 20. These are facts, not status claims.

## Definitions

In a run at root r, take a warned colouring w.
- w is **strict** if it has no decreasing two-swap macro. That is the τ bit of WP7d.
- A **hub toggle** is a swap of a two-vertex bichromatic component {h, x} with h ∉ N[r] and deg_T(h) ≥ 5. This is Lemma S's setting. In a min-degree-5 triangulation the degree condition always holds, so effectively h ∉ N[r].

## Hypothesis H-T

In every warned run, every **non-strict** warned colouring is obtained from some **strict** warned colouring of the same run by exactly one hub toggle, up to colour renaming.

**Why it matters.** If H-T holds:
- by Lemma S, a strict colouring has at most one toggle per hub;
- so the non-strict warnings in a run number at most (strict warnings) × (number of distinct hubs used).

That moves the warning-bound question onto two counts: strict warnings, and hubs per run. It does not bound either of them.

## Reported

For each run:
- the numbers of strict and non-strict warnings;
- for each non-strict warning, its toggle (h, x), or "none";
- the number of distinct hubs used;
- whether all toggles in the run share one hub.

**Kill:** a non-strict warned colouring not reachable from any strict warned colouring of its run by a single hub toggle. We record it, with the nearest strict warning and the size of their difference.
