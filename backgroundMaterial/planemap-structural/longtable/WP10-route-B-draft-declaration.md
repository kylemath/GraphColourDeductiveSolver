# WP10 DRAFT declaration: route B, configuration reducibility for degree-five roots

Long Table, 4 October 2026. **This is a draft for review. It is not released, and nothing will be run** until the Proof Navigator, the math team and the user agree on a final form. These are statements and analysis only.

## Why route B is needed

WP9 killed local determinacy at radius ≤ 2, and radius 3 cannot be tested at orders ≤ 20. The empty-region hypothesis (mass-macro existence) survives. Route B asks for a *sufficient* local condition, not a characterisation: a short list of configurations K, each guaranteeing that its central root can be made to work whatever the rest of the map looks like, together with a proof that some K always occurs.

## A structural obstacle, stated first

The mass-macro rank R = (6n² + 1)p + q includes q, a sum of squared **exterior** chain masses. Chains leave any finite configuration, so neither R nor "descent within two swaps" is determined by data on the configuration's boundary ring. Consequently, **"K is descent-reducible for R" cannot be decided by a finite ring computation.**

There are two honest ways around this, and we propose to choose between them before anything runs:

- **B1, classical reducibility at a degree-five root.** Drop R and ask the classical question. For every proper colouring of the ring of K, and every pattern of Kempe-chain connections outside the ring consistent with planarity, can Kempe moves reach a colouring that extends into K?
  - This is Birkhoff's D-reducibility and C-reducibility.
  - It is finitely checkable per K.
  - It decides *reachability*, and descent rank and complexity are separate.
  - The project already computed that the Birkhoff diamond is D-reducible and that the plain degree-five hub is not.
  - Taking B1 means accepting that the proof's local layer has the Appel–Haken / RSST shape. The hoped-for contrast would then rest on a **much smaller** configuration list, made possible by the global information that mass-macro descent and breadcrumb runs supply.
- **B2, a ring-local rank.** Find a rank computable from the ring colouring and the chain-connection partition on the ring alone, which descends within a bounded macro for every completion.
  - WP7 and the earlier Kittell experiment show that boundary-only observations (σ, and σ plus one bit) do not support a robust common-action rank. That is direct evidence against B2.
  - We would declare B2 only together with a specific candidate rank, and expect it to fail.

## Proposed claim, B1 form, if chosen

For a rooted configuration K (a near-triangulated disc around a degree-five root r, with ring ∂K):

> **C-red(K).** For every proper four-colouring of ∂K and every planar chain-connection pattern outside ∂K, some sequence of single-component Kempe swaps, realised on the ring and its outside pattern, reaches a ring colouring that extends to a colouring of K − r together with r.

**Combined target.** If a finite list 𝒦 of configurations satisfies C-red, and 𝒦 is unavoidable in minimum-degree-five triangulations (for example by a stated discharging rule), then every such T has a root inside some K ∈ 𝒦 whose recursive colouring extends. That suffices for the contact implication's *existential reachability* form. It does not give an empty dead-end region (mass-macro) or a polynomial bound; those stay separate.

**Kill conditions.**
- For each K: a ring colouring and outside pattern with no extending reachable colouring. That makes K not C-reducible.
- For 𝒦 as a whole: a minimum-degree-five triangulation avoiding every K ∈ 𝒦. For finite enumerated orders, the corpus serves as a falsifier.

**First candidates, small.**
- the radius-1 and radius-2 neighbourhoods of the corpus's *passing* roots, grouped by WP9 code;
- the WP9 radius-2 witness pair, which shows that radius-2 shape alone cannot be the criterion for mass-macro descent. Under the weaker C-red criterion, it may still be decisive.

## Questions for review

1. B1 or B2? We recommend **B1**, with the explicit acknowledgement that its local layer is classical. The project's distinctive contribution would then be the size of 𝒦 and the global descent and recursion around it.
2. Who owns the ring-colouring and chain-pattern enumerator? It is new code; an independent second implementation is strongly advisable.
3. Is a run limited to configurations drawn from the existing corpus (orders ≤ 20) acceptable as the first stage, with no new graphs needed?
