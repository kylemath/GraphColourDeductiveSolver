# New ways to compact the 604 rule parts (FABLE, 12 Nov 2026)

Light analysis, about 4 CPU-minutes in total, Python and numpy only. Nothing here is a proof claim. Input: `swarm/outside/beat_633_588/synth_rules_588.txt` and the behaviour matrices in `results/behav/`. Code: `code/fable/` (run from a folder holding the rules file, `real58.npz`, `real911.npz` and the `code/` modules; see the last section).

Charge convention used below: a vertex of degree d starts with 60(6 − d), so a 5 has +60 and a 7 has −60, and a part moves `weight` from its hub to its target.

## Bottom line

1. **The 493 SP parts are one law: "a 7 or 8 that is exactly one unit (+6) overcharged after the RSST rules pushes that unit to its big neighbours".** On concrete hub neighbourhoods drawn inside every SP part, the hub's charge after the 71 RSST parts is exactly +6 in 89% of cases and the SP parts take it to exactly 0 in 87%. For slot-scrambled SP parts the figures are 7 to 9% and 1 to 3%. This is an explanation, not yet a replacement: the law says how much leaves the hub, not which neighbour gets it.
2. **Forgetting the target gives 221 "hub ledgers" instead of 604 parts, exactly** (null: 305). A ledger is one hub picture up to rotation and reflection, plus the list of who receives what. The SP parts are 174 ledgers: 95 send 6 to one neighbour, 74 send 3 to each of two neighbours. With exact box merges first, 192 ledgers.
3. **Exact merging of adjacent boxes gives 497 parts instead of 604** (null: 600 to 602), with the same charge on every neighbourhood by construction. It is the only result here that is directly usable in the proof, and it is modest.

What did not work: decision diagrams (canonical but larger than the part list), a "flow follows slack" rule for choosing the target, mirror symmetry as the reason for the 3 + 3 splits, and averaged transfer laws (they fit well but fit scrambled rules equally well, and they cannot see the SP parts at all).

## 1. The overflow law (approximate, explanatory)

**Object.** One sentence in place of 493 parts: *if a hub of degree 7 or 8 has charge c > 0 after the RSST rules, it sends c onward, as 6 to one neighbour of degree ≥ 7 or as 3 + 3 to two of them.*

**Test** (`overflow.py`, `overflow_null.py`). For each SP part I drew 2 concrete hub neighbourhoods inside its box (986 in all), with every spoke, hat and fan degree fixed, and computed the hub's charge after the RSST parts: 60(6 − d), minus what its own RSST parts send out, plus what its spokes' RSST parts send in. The open third ring never mattered (upper and lower readings agreed on all 986).

| measure on SP neighbourhoods | real | SP parts scrambled (3 nulls) |
|---|---|---|
| hub charge after RSST is exactly +6 | **88.6%** | 6.7 to 8.5% |
| hub charge after RSST is > 0 | 91.1% | 42 to 45% |
| hub charge after RSST and SP is exactly 0 | **86.8%** | 1.4 to 3.2% |
| total SP outflow from the hub is exactly 6 | 97.2% | not measured |

- Hub charge values seen: +6 (875), 0 (61), +12 (20), −6 (19), −12 (8), +18 (2), −18 (1). A random degree-7 hub neighbourhood has median charge −36; only 3.2% are overcharged.
- Shape of the push: 6 to one target (390 neighbourhoods), 3 + 3 to two targets (572), other (24). So the weight-3 parts are half-pushes that come in pairs.
- Targets have slack: their expected RSST charge is negative in 96% of cases (median −28).

**What each literal is for** (`literal_roles.py`). Flipping one literal of an SP part at a time: 91% of the 8,983 SP literals change the hub's RSST charge, and 94% either do that or sit on the target's own first ring. So an SP part is close to "the full description of one hub neighbourhood where the charge comes out at +6", which is why the parts look like points and resist shape-based compression (18 literals per part).

**Where it fails, candidly.**
- 13% of sampled neighbourhoods do not end at 0 (9% start at c ≤ 0). Some of this may come from my uniform draw inside interval literals; I did not separate the two causes.
- **The target choice is not explained.** The chosen target is the neighbour with the most slack in only 40% of pushes. A three-line rule on (target degree, number of 5s beside it) gets 67% of chosen/not-chosen calls right. Since the file is solver-synthesised, the choice may simply be one feasible solution among many.
- **The law over-reaches as a rule.** Among 12,000 uniform random degree-7 hub neighbourhoods, 381 are overcharged (105 at exactly +6) and no SP part fires on any of them. The SP parts cover a thin set, presumably the overcharged neighbourhoods that contain no reducible configuration. An implicit rule "every +6 hub pushes" would move charge in many more places and would have to be rechecked on the engine.

**Why it matters.** It turns the SP set from 493 opaque patterns into a checkable invariant ("SP leaves its hub at exactly 0"). The cheapest follow-up is an engine test: for each of the 174 SP ledgers, is any other choice of receiver also feasible? If yes, a canonical choice (for example "most slack, ties split") could make the SP parts derivable from the RSST rules.

## 2. Hub ledgers: quotient by the hub's dihedral group (exact regrouping)

**Object.** A hub picture is the cyclic slot sequence of a part with the target forgotten, taken up to rotation and reflection. Its ledger lists the receivers and amounts. This is the lead's "commensurate across mirror symmetry" idea applied to the whole dihedral group of the hub (`ledger.py`).

| set | parts | ledgers | null ledgers | ledger types |
|---|---|---|---|---|
| all | 604 | **221** | 305 | |
| SP | 493 | **174** | 248 | 95 send 6 to one spoke; 74 send 3 + 3; 5 other |
| RSST | 71 | 37 | 37 | 34 mirror pairs, 3 self-mirror |
| ST | 40 | 10 | 20 | 10 "take 6 back from one spoke, give 6 to another" |

- It is exact: the 221 ledgers regenerate the 604 parts. The null (305) is just the mirror quotient, so the real gain over mirror symmetry is 303 → 221.
- After the exact merges of section 3, 497 boxes fall into 192 ledgers.
- **Negative result for the symmetry idea:** only 2 of the 76 split ledgers are mirror-symmetric pictures. The 3 + 3 split is not a symmetrisation of a 6; the two receivers are usually inequivalent (adjacent in 256 of 596 sampled cases, three apart in 224).
- I found no odd/even structure: hub-7 and hub-8 SP pictures share no pattern beyond the overflow law.

## 3. Exact box merges (exact, proof-usable)

**Object.** The charge a hub sends a target is F = Σ weight × [part fits]. Any part list with the same F is the same discharging procedure. Two exact moves: identical boxes add their weights; two boxes of equal weight that differ in one coordinate by adjacent intervals become one box (`merge.py`, greedy to a fixpoint, best of 8 orders).

| set | parts | after merges | literals before → after |
|---|---|---|---|
| real | 604 | **497** | 9,829 → 8,125 |
| null (3) | 604 | 600 to 602 | no change to speak of |
| SP / RSST / ST | 493 / 71 / 40 | 394 / 64 / 40 | |

- 5 parts are exact duplicates of another part (for example `drule1` and `drule1#2`), so their weights add.
- Caveat: on the engine's "upper reading", a third-ring vertex fits every split box but is not tested by a merged full-range box, so merged parts can only tighten the bound. This should still be confirmed with one engine run.

## 4. What failed or gave nothing new

**Decision diagram of F** (`dd.py`). One reduced multi-valued diagram per hub degree, variables read outward from the target. It is canonical, but not small: 4,607 nodes and 12,241 interval edges, against 9,829 literals in the part list (null: 8,100 to 8,600 nodes). The 1.8× gap to the null confirms real prefix sharing, but as a description it is worse than the parts. Side fact: F is never negative, so every ST "take back" cancels an RSST unit on the same edge; the maximum on one edge is 36.

**Averaged transfer laws** (`laws.py`, `laws_null.py`). I fitted the total expected charge into a receiver by per-edge laws.

| law | parameters | fit, real (all degrees) | fit, real / two nulls (d = 5..8) |
|---|---|---|---|
| degree potential: flow depends on the two end degrees | 10 | 95.8% | 94.6% / 61.4%, 96.9% |
| diamond: also on the two common neighbours, antisymmetric | 150 | 99.3% | 98.5% / 99.5%, 99.4% |
| diamond, not antisymmetric | 375 | 99.96% | 99.9% / 99.7%, 99.8% |

These fit scrambled rule sets just as well, so they describe the template ("5s pay big neighbours") and not this rule set. They are approximate and cannot serve the proof. Degree-6 receivers are the weak spot of the two antisymmetric laws.

**A warning about the behaviour matrix.** In raw units the SP parts carry about 10⁻⁹ of the matrix's energy and the ST parts about 10⁻⁶, because each one fits a tiny fraction of second rings. The earlier factor analysis normalised each column, so it compared directions only. Any law fitted to the averaged matrix is a law about the 71 RSST parts.

**Relaxation at receiver level** (`relax.py`). Averaged over second rings, SP inflow shows no usable relation to the receiver's RSST charge (correlation 0.1 to 0.3). The overflow law only appears on concrete hub neighbourhoods.

## Ideas not tested

- **Level sets.** Write F / 3 as a sum of indicator sets {F ≥ 3k} and cover each by overlapping boxes. Overlap is allowed there, so it may beat the 497 of section 3. Exact.
- **Grammar with a description-length score** for the cyclic slot words. The slot-scrambled null has the same per-position statistics, so only a context model (neighbouring slots) could show a gain.
- **Derive SP from RSST.** Enumerate hub neighbourhoods with RSST charge +6 that contain no reducible configuration and compare with the 174 SP ledgers. This needs the configuration matcher and is the real test of section 1.

## Files

- `code/fable/common.py`, `ball.py`: loaders and the concrete hub-neighbourhood evaluator (built on the validated `behav.py` matcher).
- `code/fable/overflow.py`, `overflow2.py`, `overflow_null.py`, `surplus.py`, `literal_roles.py`: section 1.
- `code/fable/ledger.py`: section 2. `merge.py`: section 3. `dd.py`, `laws.py`, `laws_null.py`, `relax.py`: section 4.
- To rerun: put `synth_rules_588.txt`, `real58.npz`, `real911.npz` and `code/*.py` in one folder with `code/fable/` as a subfolder, then from inside `fable/` run `RULES=../synth_rules_588.txt python3 merge.py` first (it writes `merged_real.pkl`), then `overflow.py` (writes `overflow_rows.pkl`), then the others. `laws_null.py` needs null matrices made with `python3 behav.py synth_rules_588.txt null58_1.npz 5 6 7 8 --null 1`.
