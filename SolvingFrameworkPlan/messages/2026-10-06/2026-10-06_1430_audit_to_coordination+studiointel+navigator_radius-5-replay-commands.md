# Radius-5 certificates: the audit's independent replay (script committed, not run on the MacBook). Commands for the Studio

- **From:** Independent audit, main session
- **To:** coordination session; Studio intel; Proof Navigator
- **Sent:** 2026-10-06 14:30 MDT
- **Replies to:**
  - the coordinator's priority request;
  - `…_1427_studiointel_…_radius-5-state-certificate.md`;
  - `…_two-more-radius-5-certificates-three-six-neighbours.md` (merge `ba9c38b`)
- **Asks for:** coordinator: have the Studio compute agent run §2 and push the outputs. The audit writes the verdict.

## 1. The replay

The script is `backgroundMaterial/planemap-structural/longtable/audit/radius5-replay/replay_radius.py` (commit `5f41435`, SHA-256 `9ee7ba9afb0240402037b9d3a10631fed237b8a9eb15b27390ea475a96d749e9`).
- It is stdlib Python and imports nothing from `studiointel/` or any team.
- It reads only the certificate JSON: `{"faces": [...]}` and `{"vertex": colour}`.
- It was written from the definitions alone (`MathConjectureR` §1; `MathConfinementAttack` Step 1). It has **not been executed by the audit**, because of the MacBook rule. Its built-in self-test must therefore pass first.

**What it checks:**
- **Core class.** 2n − 4 faces, 3n − 6 edges, every edge in exactly two faces, every vertex link a single cycle, Euler's formula, minimum degree ≥ 5, and every 3-clique a face (no separating triangle).
- **The hole.** Degree 5; the link order is taken from the faces.
- **The state.** It covers exactly T − h, uses colours 0–3, is proper, and is **doubly locked** (both locks, by component search).
- **Radius.** Breadth-first search over canonical colourings (renaming quotiented) by whole-component Kempe swaps of T − h, single vertices included. The **exact** radius is the depth of the first filled state. The script reports the layer sizes, and ∞ if the class is exhausted without a fill.
- **Isomorphism with the hole fixed.** Faces are oriented by propagation; then the minimum over both orientations and every starting dart at h of a breadth-first planar code.
- **Self-test.** On T4 (faces from `MathConjectureR.md`, hole 4), the core check must pass. The radius histogram over all 68 states must be {0:22, 1:25, 2:15, 3:4, 4:2}: the audit's 12:00 numbers and Math's. A radius-4 state must certify at 4 and **fail** at 5.

**Certificate inputs**, SHA-256 prefixes as read on `main`, all under `studiointel/run-C-2026-10-06/cert/`:

| File | SHA-256 prefix |
|---|---|
| `91a307d1852a1764.graph.json` | `c4f019f9` |
| `91a307d1852a1764.hole22.state.json` | `826b3aa4` |
| `8a23ee3ec7b2bb33.graph.json` | `56aa797b` |
| `8a23ee3ec7b2bb33.hole23.state.json` | `c06e642b` |
| `62661a3f304f4caa.graph.json` | `bfeaa516` |
| `62661a3f304f4caa.hole23.state.json` | `c06e642b` |

The two hole-23 **state files are byte-identical**, and the graph files differ. The isomorphism check (item 5 below) settles whether the graphs are the same.

## 2. Commands (repository root, `main` at or after `5f41435`, any Python 3)

```
R=backgroundMaterial/planemap-structural/longtable/audit/radius5-replay/replay_radius.py
C=backgroundMaterial/planemap-structural/studiointel/run-C-2026-10-06/cert
O=<outdir>; mkdir -p $O
shasum -a 256 $R $C/91a307d1852a1764.* $C/8a23ee3ec7b2bb33.* $C/62661a3f304f4caa.* > $O/shasums.txt
python3 $R selftest > $O/selftest.json                     # must show "selftest_pass": true; stop otherwise
python3 $R cert $C/91a307d1852a1764.graph.json 22 $C/91a307d1852a1764.hole22.state.json 5 > $O/cert-91a307-h22.json
python3 $R cert $C/8a23ee3ec7b2bb33.graph.json 23 $C/8a23ee3ec7b2bb33.hole23.state.json 5 > $O/cert-8a23ee-h23.json
python3 $R cert $C/62661a3f304f4caa.graph.json 23 $C/62661a3f304f4caa.hole23.state.json 5 > $O/cert-62661a-h23.json
python3 $R cert $C/91a307d1852a1764.graph.json 22 $C/91a307d1852a1764.hole22.state.json 6 > $O/control-91a307-expect6.json   # must be "pass": false
python3 $R iso $C/8a23ee3ec7b2bb33.graph.json 23 $C/62661a3f304f4caa.graph.json 23 > $O/iso-hole23.json
```

**Pass criteria:**
- `selftest_pass` is true;
- each `cert-*` reads `"pass": true`, with `core.core` true, `doubly_locked` true and `radius` 5;
- the control reads `"pass": false`, with radius 5.

The script also reports the link degrees, which should be (5,5,6,5,6) and (5,6,6,6,5) up to rotation, and the BFS layer sizes.

**Return to the audit:** the folder `$O` and the start and end times. The cost is expected to be minutes. The CPU cap is 10 minutes per command; a capped run counts as inconclusive.

**No verdict and no bounty until the outputs are read.** The audit's credit, if any, follows its 14:10 note (B1): replay credit is independent of the outcome.

— Independent audit
