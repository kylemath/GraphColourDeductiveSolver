# Distant leverage on large-diameter spheres (exploratory)

Long Table, 2026-10-14. Follow-up to `../README.md`.

**Status: exploratory measurement.** Nothing here is a theorem or a census claim. Re-check before citing.
Labels: [data] = computed here, [hand] = short argument.

## Why

The project owner's critique of the first study:
- it used census frame graphs whose holes are only 3–5 hops from the far side;
- those graphs were built around hard holes, so the far shells were thin and undersampled;
- so the observed ~30%-per-hop decay of unlocking power might be an artefact of small map diameter.

Here the same per-swap quantities are measured on sphere maps whose holes are 5–19 hops from the far side. On the
sphere there is no real "outer face": d is the graph distance in T from the hole v to the nearest vertex of the
chain K (rim = 1).

## Setup

- `large.py` reuses `leverage.py`. The copy in this folder adds one flag: whether the chain contains an
  odd-degree vertex that is not on the rim.
- **Exact mode** (S ≤ 2·10⁵ states): the HoleGame engine, with exact dF, locks and π-orbits, as in the first study.
- **Sample mode** (larger maps):
  - Start from a random backtracking colouring of T − v.
  - Walk by random Kempe swaps (non-web chains), with a Metropolis correction (accept with probability
    min(1, deg s / deg t)). The walk is therefore uniform on the start's Kempe class. 400 burn-in steps, then every
    4th state is recorded, ≤ 15,000 states or 45 s per hole.
  - At every recorded state the single-step quantities are measured for every swap:
    - unlock (DL → not DL);
    - lock-bit changes;
    - fill;
    - for DL → DL swaps, whether the π-orbit stays the same or jumps (orbits are followed by iterating π).
  - **No dF in sample mode.** On the sphere non-DL ⇒ dF = 1, so from a DL state "unlock" equals "reduces dF" at
    every dF = 2 state. Deep states (dF ≥ 3) are 0.1–2% of DL states here.
- **Sampler validation** [data]: on the same 36 holes (tubes and Goldberg duals, n ≤ 44), with equal weight per
  hole, the sampled DL unlock rates at d = 1..6 match the exact ones to within 0.01:

  | | d=1 | d=2 | d=3 | d=4 | d=5 |
  |---|---|---|---|---|---|
  | exact | 0.758 | 0.680 | 0.439 | 0.341 | 0.198 |
  | sampled | 0.760 | 0.678 | 0.439 | 0.348 | 0.191 |

  Swaps per state at each d also match. C60 h19 agrees as well.
- **Weighting.** Exact sets pool states, so large-S holes dominate. Sample sets give each hole the same weight. The
  summary table and the plot use **equal weight per hole** for every set. The detailed tables in `TABLES.md` are
  pooled.
- **Sample counts.** The quoted sample counts are correlated walk states, not independent draws.

### Data

| set | holes | mode | n | hole ecc. |
|---|---|---|---|---|
| (a) IPR fullerene duals C60–C82 (TrackF `ipr32_52`, ≤ 3 holes per graph) | 26 | exact | 32–43 | 5–6 |
| (a) non-IPR: the same graphs after one Stone–Wales flip that makes two pentagons adjacent | 27 | exact | 32–43 | 5 |
| (a) IPR C92–C120 (`ipr32_52` n ≥ 47 and `ipr62`, 20 graphs × 2 holes) | 40 | sample | 47–62 | 6–7 |
| (a) non-IPR (SW-flipped) C92–C120 | 40 | sample | 48–62 | 5–7 |
| (a) nanotubes (5,5)/(9,0), IPR and non-IPR (`tubes.txt`, 1 cap-pentagon hole) | 57 | sample | 40–177 | 5–19 |
| (a) icosahedral Goldberg C80–C540 (flat holes) | 21 | sample | 42–272 | 6–15 |
| (a) tubes + Goldberg, n ≤ 44 | 36 | exact | 12–42 | 3–6 |
| (b) glued frame graphs (`gluing/run-tight.jsonl`, n = 42–43) | 27 | exact | 42–43 | 4–6 |
| (b) glued frame graphs (`run-tight` and `round2`, n = 42–57; plus holes above the exact cap) | 42 | sample | 42–57 | 4–6 |
| (c) padded maps: 8 game maps + 3 holes of frame-22 graphs, k = 0..4 bands | 11 per k | both | 17–46 | 3–8 |

No Studio files were found under `gluing/studio`. Only `studio-run/` exists, holding job outputs without rotations.
Padding (c) works as follows:
- choose the face (a, b, c) farthest from the hole;
- add A, B, C with edges AB, BC, CA, Aa, Ab, Bb, Bc, Cc, Ca;
- repeat, with (A, B, C) as the next outer face.

Exact pad sets for k = 3, 4 contain only the 4 base holes with S ≤ 2·10⁵, so for padding compare the sample sets across k.

## 1. Curves: DL unlock rate per swap vs d (equal weight per hole) [data]

| set | d=1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | fitted factor/hop (d ≥ 2) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IPR C60–C82 exact | .733 | .655 | .452 | .349 | .271 | | | | | | | | 0.75 |
| non-IPR C60–C82 exact | .701 | .602 | .421 | .314 | .253 | | | | | | | | 0.75 |
| IPR C92–C120 | .659 | .567 | .355 | .233 | .175 | .142 | .112 | | | | | | 0.73 |
| non-IPR C92–C120 | .664 | .567 | .349 | .247 | .171 | .133 | .078 | | | | | | 0.69 |
| Goldberg C80–C540 | .685 | .466 | .267 | .192 | .149 | .098 | .077 | .056 | .061 | .021 | .018 | .030 | 0.74 |
| tubes n ≤ 92 | .672 | .593 | .265 | .165 | .073 | .020 | .006 | .002 | .000 | .000 | | | 0.36 |
| tubes n > 92 | .618 | .580 | .225 | .130 | .042 | .007 | .002 | .001 | .000 | .000 | .000 | .000 | 0.32 |
| glued n = 42–43 exact | .667 | .427 | .222 | .114 | .065 | .037 | | | | | | | 0.54 |
| glued n = 42–57 | .628 | .468 | .196 | .067 | .038 | .031 | | | | | | | 0.49 |
| *small maps (first study, D2):* frame 30–33 | .711 | .489 | .338 | .240 | | | | | | | | | ≈0.70 |
| *small:* random plantri24 | .743 | .563 | .320 | .145 | | | | | | | | | ≈0.56 |

Tube rows are 0.000 out to d = 18, on 40,000+ swaps per bin. Plot: `plots/DL_unlock_large.png` (log scale).

### Per-shell normalisation (DL source)

Far shells are now well populated. On Goldberg maps the shells hold 15–20 vertices at d = 3–8; on tubes, about 10
vertices per ring out to d = 19.

| set | | d=2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Goldberg | swaps / state / shell vertex | .27 | .23 | .20 | .20 | .19 | .19 | .17 |
| Goldberg | unlocks / state / shell vertex | .127 | .055 | .038 | .025 | .018 | .015 | .011 |
| tubes n > 92 | swaps / state / shell vertex | .17 | .25 | .30 | .33 | .34 | .35 | .34 |
| tubes n > 92 | unlocks / state / shell vertex | .088 | .051 | .032 | .011 | .002 | .0005 | .0002 |

Far swaps are **not** scarce on large maps:
- the number of available swaps per shell vertex is flat, or even rises in tubes;
- each Goldberg DL state has 3–4 swaps at every d = 3..7.

So the decay is a decay of **power per swap**, not of availability. That rules out the undersampling explanation
[data].

### Exact: states whose only dF-reducing swaps are far (d ≥ 2) [data]

| set | DL/D2 states with a dF-reducing swap | only far | fraction | deep (dF ≥ 3): only far |
|---|---|---|---|---|
| IPR C60–C82 | 96,947 | 240 | 0.25% | 0 of 211 |
| non-IPR C60–C82 | 129,315 | 359 | 0.28% | 0 of 267 |
| tubes + Goldberg n ≤ 44 | 79,249 | 77 | 0.10% | 0 of 82 |
| glued n = 42–43 | 295,588 | 742 | 0.25% | 0 of 1,091 |
| pad k = 0 / 1 / 2 | 5,729 / 22,916 / 91,664 | 22 / 88 / 352 | 0.38% each | 0 |

In sample mode, the share of DL states whose only unlocking swaps are far:
- 0.17–0.23% for fullerenes C92–C120 and for glued maps;
- 0.02–0.03% for tubes;
- 0 of 3,189 for Goldberg;
- 0.20–0.28% for padded maps at every k.

A far unlocking swap is **available** at 95–97% of round-fullerene DL states, 85% of glued ones and 70% of tube ones.

## 2. Answers

**Does the decay survive large diameter?** Yes. [data]
- **Round maps** (fullerene duals C60–C120, IPR and non-IPR alike, and icosahedral Goldberg duals to C540, hole
  eccentricity up to 15):
  - the per-hop factor is 0.69–0.75, the same as in the small census maps (≈ 0.70);
  - it is constant from eccentricity 5 to 15;
  - at a fixed d, the large maps are **at or below** the small-map rates (d = 3: 0.27–0.36 against 0.34; d = 4:
    0.19–0.25 against 0.24).
- **Thin or separated maps** decay faster:
  - glued frame graphs, which have a separating 5-cycle: about 0.5 per hop;
  - nanotubes: about 0.3 per hop beyond d = 2, falling to ≤ 0.002 by d = 7–8 and to 0 (in ≥ 40,000 swaps per bin)
    out to d = 18;
  - the far cap's pentagons do not revive leverage.

**Is there a characteristic radius?** Yes, once the diameter is large, but it depends on the geometry. [data]
- **Round maps:** the decay is exponential with length ξ = −1/ln f ≈ 3 hops (2.7–3.5). There is no cutoff, and no
  plateau out to d = 11–12 on Goldberg maps (rate ≈ 0.02–0.03 there).
- **Tubes:** ξ ≈ 0.9–1 hop beyond d = 2. Leverage is effectively confined to d ≤ 5–6.
- **Beyond a separating triangle:** ξ = 0, exactly (see below).

So "about 30% loss per hop" is a real property of round sphere maps, not a small-diameter artefact. Where the map
narrows (tube belts, short separating cycles), the loss is much larger.

**Padded maps (c).** The added bands carry 1.4–1.5 swaps per DL state per band, and those swaps **never unlock**. The
unlock rate is 0.000 at every d ≥ ecc₀ + 2, in both modes. [data]

- Exactly, the DL counts and the only-far counts multiply by exactly 4^k, and the only-far fraction is identical for
  k = 0, 1, 2.
- [hand] The innermost padding triangle abc separates the hole from the bands, and a, b, c are pairwise adjacent. Any
  bichromatic path between two inside vertices that leaves through one triangle vertex and comes back through
  another can be shortcut by the triangle edge. So whether two inside vertices are connected, and in particular every
  lock bit, depends only on the colouring of the closed inside region. A chain lying strictly outside abc therefore
  never changes a lock bit, never fills, and never unlocks.
- At d ≤ ecc₀ the rates are unchanged by padding (d = 2, 3: 0.50–0.51 and 0.36–0.39 for k = 0..4). The d = 4 bin
  drops (0.18 → 0.07–0.10) because inert band chains enter it.
- So padding measures the separating-triangle effect, not a diameter effect.

**Odd-degree vertices.** Far chains that contain an odd-degree vertex (rim excluded) are somewhat stronger at
d = 2–3: for fullerenes C92–C120 the rates are 0.61 / 0.41 against 0.53 / 0.33 for all-even chains. Beyond d = 3 the
difference vanishes, and all-even chains do unlock (on C60 h19 all 80 swaps at d = 4 are all-even, and 40 of them
unlock). So
"a far swap must move a pentagon" is **not** the mechanism. [data]

**π-orbits.** As in the first study, far DL → DL swaps essentially always jump to another π-orbit: unlock rate +
π-jump rate = 1.00 at every d ≥ 2 in every set, so pi_same ≈ 0, and the π-jump rate is 0.65–1.0 at d ≥ 3 (TABLES.md).
[data]

## 3. Reading [hand, interpretation]

The first study's conclusion survives and gets sharper:
- leverage decays exponentially with distance on every sphere family tried;
- the near swap is essentially never missing: only-far states are ≤ 0.4% and deep states have 0 only-far;
- the decay length is set by how much "room" the lock chains have to route around the hole region. It is about 3
  hops in round maps, about 1 hop in tubes, and 0 across a separating triangle.

The last case is a clean statement worth recording: **a Kempe swap outside a separating triangle that has the hole
inside is inert for locks.** It follows directly from the triangle being a clique. Separating 4- and 5-cycles are
not cliques, and on the glued maps they show finite but steeper decay. This fits the reading that lock status is a
connectivity fact local to the region around the rim, and that far swaps act through re-routing of the lock chains,
whose reach is limited by the narrowest separating cycle.

## Caveats

- Sample mode gives single-step quantities only. "Only far" is "only far unlocking swaps", which equals dF-reducing
  at dF = 2 states.
- The sampler covers the start's Kempe class only. Frame graphs and fullerenes almost always have one class per hole.
- Goldberg holes are all equivalent within a graph (icosahedral symmetry), so 21 holes means 5 graphs (C80, C180, C240,
  C320, C540) with repeated samples. DL states are rare there (3,190 samples), so the d = 9–12 rates (0.02–0.06) are
  noisy.
- Glued exact holes are those with S ≤ 2·10⁵. Pad exact k = 3, 4 covers only the 4 small base holes.
- Non-IPR graphs are synthetic: one Stone–Wales flip of an IPR dual. This is not a census of non-IPR fullerenes.
- The C92–C120 fullerene samples are 20 random graphs per family.

## Files

- `large.py`: driver (graph sources rot / sw / glued / pad; exact or sample mode per hole). It needs
  `~/4square/kempe_engine.py`.
- `leverage.py`: copy of `../leverage.py` with the odd-degree-chain flag (`odd`, `unlock_odd`).
- `analyse_large.py` → `TABLES.md` (full tables: per-d swaps per state, per shell vertex, chain size, π-jump,
  e-stratified, odd split, padding by k) and `plots/DL_unlock_large.png`.
- `run_large.sh` (first pass), `run_large2.sh` (tubes/Goldberg and padding re-run with the odd flag, exact tubes,
  extra Goldberg and glued holes, sampler validation). Inputs are read in place; `out/in_frame22_4.txt` is rebuilt.
- `out/*.jsonl.gz`: one record per hole, with histograms keyed `src|d` as in the first study. Sample records carry
  `samples`, `acc` and `steps`.

Runs: 2026-10-14 00:26–01:06, MacBook on AC power (100%), ≤ 3 processes, nice 10, each run ≤ 14 min.
