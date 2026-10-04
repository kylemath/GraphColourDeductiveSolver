# WP9 results: the good-root property is not determined at radius 2

Long Table, 4 October 2026. This follows [WP9-local-determinacy-declaration.md](WP9-local-determinacy-declaration.md), committed before any run (`5bf8a98`). The discovery report was posted (`9f8832c`) before the pooled run. Outputs are `wp9-orders-12-18.json` and `wp9-orders-12-20.json`. These are facts, not status claims.

**Sanity checks on the ball code:**
- symmetric roots get equal codes (order 17, graph 3, roots 3 and 13);
- codes are unchanged under random relabelling at k = 1, 2 and 3.

## Results

| Radius | Orders 12–18 (279 roots, 6 failing) | Orders 12–20 pooled (1,586 roots, 12 failing) |
|---|---|---|
| 1 | **Killed** (3 mixed codes) | **Killed** (5 mixed codes) |
| 2 | Survives, **vacuously**: 0 of 6 failing roots share a code with a passing root | **Killed** (1 mixed code) |
| 3 | Survives, vacuously | Survives, **vacuously**: 0 of 12 failing roots share a code with a passing root |

**The radius-2 kill witness, independently recomputed with `mass_core`:**

| Root | Radius-2 ball | Outcome | Colouring orbits | Two-swap stuck |
|---|---|---|---:|---:|
| Order 19, graph 20, root 3 | 11 vertices, same code | **passes** | 200 | 0 |
| Order 20, graph 60, root 3 | 11 vertices, same code | **fails** | 224 | 2 |

Their radius-3 balls differ.

## Reading

- **No radius-1 or radius-2 catalogue can work.** The mass-macro good-root property is **not** a function of the radius-2 rooted neighbourhood, even with full T-degrees and the rotation recorded. No catalogue of radius ≤ 2 root shapes can decide goodness by itself, and route A at radius ≤ 2 is closed.
- **Radius 3 cannot be tested on this corpus.** At orders 19–20 a radius-3 ball already contains 17 of 19–20 vertices: almost the whole graph. Its survival is vacuous and also uninformative about locality. Testing k = 3 meaningfully needs graphs much larger than radius 3, so orders well beyond 20, which are not released.
- **Consistent with the Proof Navigator's prior** (radius 2 to 3: Low). Combined with WP7, this is further evidence that the obstruction is not local at small radius. The empty-region hypothesis may still hold globally; the corpus has a good root in every graph.

## Consequences for the plan (for joint decision)

1. **Route A is closed at radius ≤ 2.** Radius ≥ 3 is untestable without larger graphs.
2. **Route B (descent-reducibility)** was to wait for a non-vacuous surviving radius, and none exists. It could still be attempted directly, as a claim about *configurations whose ring colourings all descend*. That is a different statement from local determinacy, and it would need its own declaration.
3. **The stitch and the contact theorem (Track 1)** are unaffected. They make the hypothesis exact, whatever its proof turns out to be.
4. **Larger graphs** become the only way to test locality at radius 3. That is the same release question as the distant-hub search, and both could be declared together.
