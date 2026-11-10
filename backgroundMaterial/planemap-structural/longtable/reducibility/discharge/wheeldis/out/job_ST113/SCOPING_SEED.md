# ST-113: what it takes to Lean-check the RSST seed certificate (Studio, 10 Nov, reading + estimation only)

The question: make "every internally 6-connected triangulation contains one of the RSST configurations" (the RSST discharging
fixed point at t = 0, K633, checked on two engines: RSST-1SHOT 30861e542 and W6r) a Lean theorem, plus Lean reducibility for the
configurations it uses. Marks: **[read]** = taken from a file or a status line; **[inf]** = my estimate. Effort figures are rough
(person-days = pd, one agent-day of focused Lean or tooling work). No Lean was written and almost no CPU was used.

## (a) The 582 proved RSST configurations (D2 249 + C2cons 333, `loop/k44/rsst_verdicts.txt` b6f7a314)

**Method [read].** For each name, I looked for a Lean hD / hC that is built and clean (status exit=0, sorry=0), and compared its
literal with the RSST kc line (`loop/k44/rsst.txt`). For C, X must also match the C2cons X. Sources:
- HDC502 D_todo + module_split (hD);
- HDR5 (`lean_r5`);
- HD0 HDCtrl / HD30;
- CR118 (`f2b041/rsst118/extra118.tsv`, R118V*, R118All ALLDONE);
- the keep_lean_C (531) hC list in `job_JCOV/coverage/lean_membership.tsv`.

RSST DCheckData `agreesRSST` is verdict-level only, so it is **not** counted. Output: `rsst582_lean_coverage.tsv` (d2f91ec5),
one row per config with route, literal check and status.

| | total | in Lean now | to do | to do by ring |
|---|---|---|---|---|
| D2 | 249 | **51** (HDC502 43, HDR5 5, HD0 3) | **198** | r6 1, r8 3, r9 4, r10 16, r11 32, r12 72, r13 48, r14 22 |
| C2cons | 333 | **128** (CR118 118, Lean531 10) | **205** | r9 1, r10 8, r11 28, r12 47, r13 65, r14 56 |

- Literal mismatches: **0**. The kc lines in all 179 matched entries are byte-equal. CR118's X differs from the verdict file
  only in the `{}` wrapper.
- **Rim-pinned X (an R-I edge) [read]:** 62 of the 333 C2cons. 29 are already in Lean (CR118); **33 are to do**.
  - Rim-pinned X already goes through our C path: CR118's 27 rim-pinned entries are hC-clean. P20 / P21 (rim-pinned, ST-111)
    have Opus glue armed and checked.
  - So no new C theory is needed for these, only per-entry glue [read for hC, inf for glue at scale].
- **Non-admissible X: none.** C2cons is defined as "one conservative X accepted by kc -C" (k44 header) [read]. The 51 "none" are
  exactly the configs with only a non-admissible (RSST) X, e.g. rsst003 2.126: `adm=no` in `rsst_verdicts_C2.txt` [read].

**Cost of the rest [inf from read rates].**

| item | rate used | estimate |
|---|---|---|
| 198 hD | HDC502 per-ring median CPU s (report.md) [read]: r10 3, r11 11, r12 47, r13 264, r14 1323 | ≈ 45,700 CPU s ≈ **13 CPU-h** |
| 205 hC | CR118 [read]: 126,037 s over 118 entries (r12 13, r13 58, r14 45) = 1,068 s/entry; I scale it by ring (≤11 ≈ 150 s, r12 ≈ 400 s, r13 ≈ 900 s, r14 ≈ 1,600 s) | ≈ 172,000 CPU s ≈ **48 CPU-h** |
| occurrence glue, 403 entries | HDW18N [read]: 31 glue modules 207 s wall in total (~7 s per entry), but 1,300–1,650 generated lines per entry (HDW18N 19,832 lines / 15; HCK5P17 1,654) | ≈ 1 CPU-h compile; ≈ **0.6 M generated lines** |

- At 4–6 parallel Lean on the Studio, that is about 1–1.5 days wall.
- People: about **2–4 pd** to drive the batches and the literal / mutant checks, plus Opus's time to generate 403 glue packs. The
  per-pack pipeline (generate → check_literals + mutant → glue_drive) is the P17–P22 one, already routine.

## (b) Formalising the fixed-point check itself

**What our Lean has today [read].**
- `ClaimGlue.four_color_of_unavoidable` / `CGlue.four_color_of_unavoidableC*` reduce 4CT to `Unavoidable R` (+ the C glue).
  `Unavoidable` is a **hypothesis**: "to be supplied by the discharging LP at t* ≤ 0" (ClaimGlue.lean:164).
  `unavoidable_of_appears` splits it into the LP's "appears" and the appearance → occurrence bridge (Job 26).
- **Euler:** `TutteSides.euler_tri` gives |E| + 6γ = 3n for a triangulated spherical map. With γ = 0 this gives Σ(6 − deg) = 12
  after a short degree-sum step [read for euler_tri; inf for the step, ~0.5 pd].
- **Occurrence:** `OccursW` / `OccursC` / `OccursCX` and the per-entry COcc glue exist (folds and pinches handled; Job 26's fold
  gap is closed for fold-safe entries) [read].
- **Internally6** carries minDeg 5, noSep, noShortSep (Birkhoff ring-5, Addenda A/B of RSSTADM) [read].
- **Nothing** in Lean reads charges, rules, cons2 rows, sender rows or any LP certificate. The LP path has no Lean on the
  discharging side either: today both routes stop at the same `Unavoidable` hypothesis [read].

So the RSST route does **not** lose LP Lean work. It replaces an LP certificate (tens of thousands of keys, f2b rules, GK keys,
cons2) with 71 local rule parts at t = 0, which is a much smaller thing to formalise [inf].

**Pieces to build [inf].**

| piece | content | size |
|---|---|---|
| B1 charge + Euler | ch(v) = 10(6 − deg v); Σ ch = 120 > 0 from euler_tri; discharging conserves the sum (each rule is a transfer along an edge or a 2-path) | 0.8–1.2 k lines, 4–6 pd |
| B2 rules as data | the 71 parts (spec §3.2) as a Lean inductive / table, with the fit semantics of §3.3–3.5, hats, 9+ handling §6 | 1–1.5 k lines, 5–8 pd |
| B3 window extraction (§7 in Lean) | from Internally6, the 2-ball of u (link, privates, undrawn 9+ middles) is induced, with no identifications and all triangles faces. W6b's (a)–(d) + our brute force say it holds; the proof uses noShortSep (≤4 and 5 with BothSides2) and minDeg 5, and SepAll / SideCycle / Sep4 / Sep5 have the side machinery. Output: a map from (T, u) to a word whose evaluated charge equals u's real final charge | 2–3.5 k lines, 12–20 pd. **The critical step.** |
| B4 locality / soundness of evaluation | u's final charge depends only on its window word, and the Lean evaluator on the word equals it | 1–2 k lines, 6–10 pd |
| B5 finite check | for d = 5..14, every word with final charge > 0 contains a K633 config. d ≥ 15: hub transfers ≤ 6 each, so charge ≤ 60 − 4d ≤ 0 (spec §8.4) | see below |
| B6 kill → occurrence | "config contained in the window word" ⇒ `OccursW` / `OccursC` in T. Needs a **generic** containment-to-occurrence lemma (today's glue is per entry, generated). Through B3, an induced window makes this a subgraph embedding | 1–2 k lines, 6–10 pd [inf], or reuse per-entry glue (0.6 M generated lines, see (a)) |

**B5: decide or replay [inf].**
- A plain `native_decide` over all words is too big at d = 7, 8.
  - The search groups fillings by relevant privates (§8.1) and walks (link, apex) words.
  - Full world, no domains: 84,292 + 55,752 states still positive after K582 at d7 / d8 alone (RSST-1SHOT), from much larger
    raw spaces.
  - Each state needs a containment test against up to 633 configs.
- **Recommended: certificate replay**, the way DCheck already uses `native_decide` on a checker.
  1. Write a Lean checker: about 0.4–0.6 k lines, a port of rcore.py, 351 lines [read].
  2. Feed it a per-degree certificate: for every group with hi > 0, a killer (config id + embedding).
  3. Prove the enumeration complete by a structural argument over the grouping (§8.1, §8.3).
  4. d = 9..14 use the max-plus closed-walk / Karp bound (§8.4, §13): replay the potentials as a DP certificate, checked by
     `native_decide` on a small table.
- Size: checker + completeness lemmas 1.5–2.5 k lines, 8–12 pd. Certificate files are generated (tens of MB) and native_decide
  CPU is hours, not days.
- Per errata §14 (u a host at every degree, kill-check positive states only, fillings over all sites), the Lean checker must use
  exactly that reading. The RSST-1SHOT flags map onto it.

**Where §7 enters [inf].** Only in B3, and it is needed twice:
- the window word is a faithful picture of T near u, so B4 is sound;
- a contained configuration is an occurrence in T, so B6 is sound.

B3 is the one genuinely new structural proof. Everything else is bookkeeping or a checker.

## (c) Substitutes for the 51 "none" configurations (RSST-SUB2)

Sole killers to replace [read, RSST-1SHOT ONLY_COVER.tsv 9c8e6fa0]:

| scope | sole-killer none configs |
|---|---|
| d6 full world | 1 (2.126) |
| d7 full world | 26 |
| d8 full world | 23 |
| d9 | 12 |
| d10 | 5 |
| union over d5–14 + the d7/8 sets | 15; the domain-free d7/8 world involves all 51 |

- W6b's first round (rsst/sub, ST-111) needed 2 C substitutes (fix_63c8a193fe r14, fix_404d45e819 r13) and 6 nl51 D (2 already
  hD, nl3352 queued) for the d7/8 row sets [read]. These are the template.
- **Per substitute [inf from (a) rates]:**
  - second check (kc -C -x, cfast, CK literal, occurrence) ≈ 10 min machine;
  - hD r12 ≈ 1 min, r13 ≈ 4.5 min, r14 ≈ 22 min, r15 ≈ 2 h (HDC502 medians, max 3 h);
  - hC ≈ 0.3–0.5 CPU-h (CR118 rate; P17–P22 V00 builds are in this range);
  - glue ≈ 7 s compile plus 1.3–1.6 k generated lines.
- **Sizing:** if RSST-SUB2 needs about 1–2 substitutes per none config in the full world, that is ~50–100 configs, mostly r12–r14:
  ≈ **15–40 CPU-h** + glue, **2–4 pd** of checking and batching. ST-111's 39-config audit found 7 already hD [read], so some
  will already be covered.
- The substitutes use our own admissibility, so the Gonthier `valid_contract` port (RSSTADM, ~23 pd) **stays off the path**.

## Total and critical path

**Total [inf].**
- Reducibility side:
  - (a) ≈ 61 CPU-h (13 hD + 48 hC) + ~1 CPU-h glue for 403 entries, ≈ 2–4 pd;
  - (c) ≈ 15–40 CPU-h, ≈ 2–4 pd;
  - together ≈ 3–4 days wall on the Studio at 4–6 parallel Lean, and largely mechanical (the P17–P22 / HDC502 pipeline).
- Fixed-point side (b): ≈ 7–12 k lines of Lean, ≈ **40–65 pd**. Of this:
  - B3 (§7 window extraction) 12–20 pd;
  - B5 (checker + certificate replay + completeness) 8–12 pd;
  - B6 (generic containment → occurrence) 6–10 pd;
  - B1 / B2 / B4 bookkeeping 15–24 pd.

**Critical path:**
1. B3 first: the induced-window theorem from `Internally6`, on the SepAll / Sep4 / Sep5 machinery. Both B4 and B6 rest on it, and
   it is the only part with real proof risk.
2. Then B4, which is needed for B5's soundness statement.
3. The checker and certificate (B5) can be built in parallel and validated against RSST-1SHOT's outputs.
4. The reducibility batches (a) and (c) run on the Studio alongside and finish long before.

This route ends at a Lean `Unavoidable` (the RSST K633 registry) with no LP certificate in the trusted base. Today that hypothesis
is open on both the RSST and the LP route.
