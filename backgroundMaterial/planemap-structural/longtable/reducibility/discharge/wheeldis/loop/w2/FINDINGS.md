# Round 14: small B-fixed windows across the d = 7 tight family (16 Oct 2026) [exploratory, dfast only]

**Windows** (`w2.py build`): gen28's B-fixed configuration with |S| = 2 or 3. u is at exact degree 7, S is a set of
link fives, and every neighbour of S is at its exact letter (9 becomes B, a free ring vertex). The f7_ name has '.'
outside S's letters, so one D verdict forbids every d = 7 arrangement containing the window. A window over the two
fives flanking a link 7 is the edge-centred configuration (u, the 7, their common fives, all at exact degree).

**Family**: 617 distinct d = 7 arrangements. 471 are from `loop/e7/tight7.txt` (my round-9 tight rows and Studio's
round 9-11 certificates). 146 more are from Studio's round 12 (`out/job28/tight7_12.txt`), which also holds its
certificate receivers and the 15 HARD28 rows.

**Run**: 2,032 windows at ring <= 14. 839 were already tested, 9 are in Studio's pending batch, and 636 were new
(`win14.txt`). dfast found **178 D of 636** (`win14.out`):

| ring | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|
| D / tested | 0/1 | 2/8 | 16/33 | 39/104 | 58/189 | 63/301 |

**Coverage** (`w2.py cover`, the same matcher as sep3: rooted words of S, dihedral; it reports 0 hits on Studio's 227
round-12 tight rows with Studio's own pattern list):
- Before: 73 of 617 forbidden (11.8%), all by Studio's round-12 partial verdicts (`r_12.partial.out`).
- After: **190 of 617 (30.8%)**. H-W2 survives, just over its 30% bar. The guess was 20%.
- Studio's own tight rows: 48 of 146 forbidden (21 before).

| rows | letters 5-7 only | with an 8 or 9 |
|---|---|---|
| only shared fives | **20 / 21** | 61 / 126 |
| with a lone five | 18 / 28 | 91 / 442 |

**Reading.**
- The 7-5-7 family with letters 5-7 is gone: 20 of 21 rows die to windows at ring <= 14.
- What survives has an 8 next to S. An 8 at exact degree adds ring vertices, so these windows reach ring 15-21.
- All 4 receivers of the 13/49 certificate were already forbidden by Studio's round-12 verdicts. The new windows do
  not touch the current certificate. They forbid 117 other rows ahead of the LP.

**Shared fives drive 13/49** (`out/wlp3_j28_12.txt`). 81% of the sender dual weight (0.51 of 0.63) is on
shared-five senders (55677, 55767, 56677, 56776, 66677, 66777). The lone sender 55667 carries 0.12. The heaviest
receiver, 5756756/6565665 (0.163), has three fives and each one sits next to a link 7.

**HARD28** (Studio's 15 rows, all with an 8 or 9; each has 3 fives, a 5-5 pair and a five between bigs):
- Each row's only window at ring <= 16 is the 5-5 pair (ring 11, not D). Its other windows are at ring 17-21.
- So exact windows cannot cover them below ring 17.
- One row, 5576576/5658856, now dies anyway. The killer is `f7_5567567_56.BB.6`, a window built from a sibling row
  with 9s, where B (free, 7/8/9) also matches the 8s.
- That points at **8-relaxed windows**: the same S, with the 8s left free. For the HARD28 rows these are at ring
  10-16 and almost all untested. That is round 15.

## Supply count for the K = 2 gate (coordinator ask, 14:20Z) [`supply.py`; the estimate at the end is inferred]

All B-fixed sender sets S (any |S| >= 2, gen28 variants) of the 617 distinct d = 7 tight rows, at ring <= 16, against
the registry after round 14 (round 15 not included):

| class | rows | meaning |
|---|---|---|
| forbidden by Studio's r_1..r_12 | 71 | |
| forbidden by explore windows (round 14) | 119 | |
| supply | 318 | some S at ring <= 16 untested (106 of these configs are in Studio's pending batch) |
| pendC | 61 | every S at ring <= 16 tested, a notD one still waits for cfast |
| hard (HARD28-like) | 48 | every S at ring <= 16 tested, none D/C; 4 have no S at ring <= 16 at all |

- 303 of the 427 free rows have at least one S that cfast called neither.
- The supply is expensive: for 300 of the 318 supply rows the smallest untested S is at ring 15-16. There are 564
  distinct untested configurations, 549 of them at ring 15-16.
- Rows that first appeared in round 12 (146): 48 forbidden, 76 supply, 14 pendC, 8 hard.

**Estimate (inferred).** At Studio's ~200 configurations a round, today's supply lasts about 3 rounds. dfast D rates at
ring 14-15 are 20-25% (round 14; Studio's round 12), so roughly a third of the supply rows should die. The rest go to
pendC and then mostly to hard. After those rounds about two thirds of today's free rows would be HARD28-like. t* fell
0.029 in 12 rounds (5/17 to 13/49), so the ring <= 16 supply runs out long before t* nears 0. At the 24 Oct gate the
choice between bigger configurations (ring 17+, or configurations not centred at u) and a new rule class is real.
