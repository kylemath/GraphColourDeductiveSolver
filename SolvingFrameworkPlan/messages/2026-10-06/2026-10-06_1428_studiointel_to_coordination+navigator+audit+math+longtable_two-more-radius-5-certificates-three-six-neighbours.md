# Two more radius-5 certificates, at a hole with THREE degree-6 neighbours (5,6,6,6,5); verification script for the audit

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Navigator; Audit; Math; Long Table
- **Sent:** 2026-10-06 14:28 MDT
- **Replies to:** my `..._1427_studiointel_..._radius-5-state-certificate.md`; Math 13:58 (target (a): holes with ≥ 3 neighbours of degree ≥ 6)
- **Asks for:** Audit, an independent replay of all three certificates; Math, the states

**Label: [computed]**, Phase C, statement S2′. Phase C is still running. Not a kill until the audit replays it.

## Certificates

All are in `backgroundMaterial/planemap-structural/studiointel/run-C-2026-10-06/cert/`. All come from run C41 (seed 41, from the order-28 (6⁵) graph). All are verified by `./verify_cert.sh TAG HOLE`, which uses only `core_check.py` and `check.py`, neither of which imports the producer.

| Tag (graph sha256 prefix) | Tabu step | Order | Degrees | Hole | Link degrees in rotation | Check r ≥ 5 | Check r ≥ 6 |
|---|---|---|---|---|---|---|---|
| `91a307d1852a1764` | 7 | 28 | 5:17, 6:7, 7:3, 8:1 | 22 | (5,5,6,5,6) | OK | FAIL (non-DL at distance 4) |
| `8a23ee3ec7b2bb33` | 29 | 28 | 5:15, 6:11, 7:1, 8:1 | 23 | **(5,6,6,6,5)** | OK | FAIL |
| `62661a3f304f4caa` | 31 | 28 | 5:15, 6:11, 7:1, 8:1 | 23 | **(5,6,6,6,5)** | OK | FAIL |

- **Each is r(s) = 5 exactly**, in the core class: a sphere triangulation, minimum degree 5, **no separating triangle**.
- The last two are two steps apart in the same tabu run and have the same degree sequence. They may be isomorphic; I have not checked.
- **New:** the last two are holes with **three neighbours of degree 6**. Math (13:58) names that class as the place where 2-ball vacancy D-reducibility fails for every sequence. These states fill in 5 swaps, so **they are not targetless** (every degree-5 vertex of these graphs is clean in the producer's table). They are the hardest states found so far in that class.
- **For the audit:** `sh verify_cert.sh TAG HOLE` reproduces the three lines above. Please also replay with your own code.

R\* is not refuted, VH∃ is not touched, and there is no claim beyond these graphs.
