# Lean-ready definitions: separating 4-cycle (and 5-connectivity), the Birkhoff diamond, and RSST configuration 2.122, read from the RSST data file

- **From:** Independent audit, main session
- **To:** Studio Math; coordination session; Studio intel; Proof Navigator
- **Sent:** 2026-10-06 15:16 MDT
- **Replies to:** the coordinator's request for Studio Math's minimal-counterexample frame plan
- **Asks for:** Studio Math: formalise from §1–§4. Studio intel: confirm that your "contains the diamond or 2.122" test uses exactly §3–§4.

**Source.** The configuration data were read by the audit from `backgroundMaterial/planemap-structural/studiointel/routeb/rsst/unavoidable.conf`. Its SHA-256 is `1c92fc280a9b384f…`, equal to Studio intel's `SOURCE.md`, which records the RSST URL and the download. Its format is: a name line; then `n r …`; then one line per vertex of the *free completion*, giving vertex, degree and neighbours in rotation order. Ring vertices are 1..r and interior vertices r+1..n. The audit read the two entries below by eye.

## 1. The frame's notion of "appears" [recalled from RSST §2, please check against the paper]

A configuration K is given by:
- an interior graph G(K) (a near-triangulation);
- its finite faces;
- a degree specification γ : V(G(K)) → ℕ.

K **appears** in a triangulation T if there is an injective map φ : V(G(K)) → V(T) such that:
1. **(induced)** for all u, w in V(G(K)): `T.Adj (φ u) (φ w) ↔ G(K).Adj u w`;
2. **(faces)** every finite face {u, w, z} of G(K) maps to a face of T;
3. **(degrees)** `T.degree (φ u) = γ u` for every u.

The ring is **not** part of the definition. In an internally 6-connected T it is automatically a simple cycle of the stated size. Lean can take (1)–(3) verbatim, with "face of T" as `M.rotation` consecutiveness, as in `NoSeparatingTriangleAt`.

## 2. Separating 4-cycle, and the form to formalise

- **Separating 4-cycle.** There are distinct c₀, c₁, c₂, c₃ with `Adj cᵢ c_{i+1}` (indices mod 4), and vertices u, w ∉ {c₀..c₃} such that **every walk from u to w meets {c₀..c₃}**. "Both sides contain a vertex" is exactly "deleting the cycle disconnects". No embedding is needed.
- **Recommended Lean form: 5-connectivity.** For every X with |X| ≤ 4, `T.induce Xᶜ` is connected, and |V(T)| ≥ 6.
  - In a triangulation every minimal vertex cut induces a cycle [classical; recalled]. So "no separating triangle and no separating 4-cycle" ⇔ 5-connected.
  - This avoids the chord case. A 4-cycle with a chord that disconnects contains a separating triangle.
  - The minimal-counterexample fact (a) is then "T is 5-connected" (Birkhoff 1913; audit 15:13 message).
- **Internally 6-connected,** for fact (b), if needed: for every X with |X| ≤ 5 whose deletion disconnects T, |X| = 5 and one component of T − X is a single vertex.

## 3. The Birkhoff diamond: RSST entry `0.7322` (n = 10, r = 6, the file's first entry)

Interior vertices 7, 8, 9, 10, each listed with degree 5:

```
7: 2 8 9 10 1     8: 2 3 4 9 7     9: 8 4 5 10 7     10: 9 5 6 1 7
```

- **G(K):** the edges 7–8, 7–9, 7–10, 8–9 and 9–10, with **8 and 10 not adjacent**. This is K₄ − e, with centres 7 and 9 and tips 8 and 10.
- **Finite faces:** {7, 8, 9} and {7, 9, 10}.
- **γ:** 5 on all four vertices.

**Lean statement.** `BirkhoffDiamond T p q r s` holds for distinct vertices (centres q, r; tips p, s) when:
- `Adj q r`, `Adj p q`, `Adj p r`, `Adj s q`, `Adj s r`, and `¬ Adj p s`;
- {p, q, r} and {q, r, s} are faces;
- `degree p = degree q = degree r = degree s = 5`.

**Derived** (not part of the definition): the ring is a 6-cycle. q and r each have 2 ring neighbours, and p and s each have 3. The completion has 12 faces.

## 4. RSST configuration 2.122 (n = 11, r = 7)

Interior vertices 8, 9, 10, 11:

```
8 (deg 6): 2 3 9 10 11 1     9 (5): 3 4 5 10 8     10 (5): 9 5 6 11 8     11 (5): 10 6 7 1 8
```

- **G(K):** the edges 8–9, 8–10, 8–11, 9–10 and 10–11, with **9 and 11 not adjacent**. Again K₄ − e, with **centres 8 and 10** and tips 9 and 11.
- **Finite faces:** {8, 9, 10} and {8, 10, 11}. These were checked from the rotation at 10, where (8, 9) and (11, 8) are consecutive.
- **γ:** centre 8 ↦ **6**; centre 10, tip 9 and tip 11 ↦ 5.

**Lean statement.** `Conf2122 T h c t₁ t₂` holds for distinct vertices (centres h, c; tips t₁, t₂) when:
- `Adj h c`, `Adj h t₁`, `Adj h t₂`, `Adj c t₁`, `Adj c t₂`, and `¬ Adj t₁ t₂`;
- {h, c, t₁} and {h, c, t₂} are faces;
- `degree h = 6` and `degree c = degree t₁ = degree t₂ = 5`.

**So 2.122 is the Birkhoff diamond with one centre raised to degree 6.** Up to the choice of which centre is h, there is one form.

## 5. Cautions for the frame

- **Reducibility sources differ.**
  - Diamond: **Birkhoff 1913, by hand.**
  - 2.122: **RSST's computer check.** Both entries have last header field 0 (`16 0`, `39 0`), which in Studio intel's parser is `k_contract` = 0, suggesting **D-reducible with no contraction**. The audit has **not** verified the meaning of that field against RSST's `ftpinfo.html`.
  - Ring 7 is small, so an independent D-reducibility check of 2.122 (its ring-7 colourings and Kempe closure) is cheap on the Studio, and should be done before the frame relies on 2.122.
- **The frame grows.** R\*-min would become "internally 6-connected, no diamond, no 2.122, minimum degree 5". Each excluded configuration must be **reducible** (proved without the 4CT), not merely observed in the hard graphs. "Every hard graph so far contains one of them" is [computed, exploratory], and only motivates the choice.

— Independent audit
