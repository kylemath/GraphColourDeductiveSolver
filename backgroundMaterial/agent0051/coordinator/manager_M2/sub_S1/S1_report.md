# Sub-subagent 0051-M2-S1 Report

**Agent:** 0051-M2-S1
**Task:** Alternative proof via direct |V_5| descent
**Manager:** 0051-M2
**Status:** Complete — obstruction identified

---

## Work Product

### |V_5| Descent Analysis

**Question:** For every 5-colouring $c$ with $|V_5(c)| \geq 1$, does there exist a single Kempe swap reducing $|V_5|$ by 1?

**Answer: NO.** Approximately 23-30% of 5-colourings have no single-swap that reduces $|V_5|$.

| $n$ | Single-swap descent exists | No descent | Rate |
|-----|---------------------------|------------|------|
| 5   | 48/120                    | 72         | 40.0% |
| 6   | 528/720                   | 192        | 73.3% |
| 7   | 3,384/4,800               | 1,416      | 70.5% |
| 8   | 25,488/32,880             | 7,392      | 77.5% |

### Two-Step Descent Analysis

**Question:** For colourings without single-swap descent, does a 2-step sequence ({1,2,3,4}-swap then any swap) achieve descent?

| $n$ | No single descent | 2-step works | Still fails |
|-----|-------------------|-------------|-------------|
| 5   | 72                | 72          | 0           |
| 6   | 192               | 144         | 48          |
| 7   | 1,416             | 960         | 456         |
| 8   | 7,392             | 4,920       | 2,472       |

**Outcome:** At n=8, 2,472 colourings resist even 2-step descent. The direct |V_5| descent approach requires 3+ step sequences in general.

### Obstruction Analysis

The "no descent" colourings have best delta = 0: every available swap either preserves or increases $|V_5|$. The $(a,5)$-swaps that would reduce $|V_5|$ are unavailable because they would create improper colourings (colour conflicts), and the {1,2,3,4}-swaps that would free a colour at a degree-5 vertex aren't in the right configuration.

This means: a monotone $|V_5|$-descent proof is impossible with single-swap steps. The BFS shortest path must sometimes take "flat" steps (preserving $|V_5|$) before finding a descent. This is consistent with Agent 0050's monotone path analysis (only 60% have strictly monotone paths at n=8).

### Implications for Proof Architecture

1. **Pure descent doesn't work** — any proof via Kempe swaps must allow non-monotone steps
2. **Multi-step descent works** — BFS always finds a path (280K+ verified), just not always monotone
3. **The inductive approach (lifting from G-v) remains the best strategy** — it naturally handles non-monotone paths by delegating to BFS in a smaller graph

## Self-Assessment

**Craftsperson says:** Conclusive negative result that rules out the simplest proof approach.

**Skeptic says:** We only tested 2-step descent. With 3-4 steps, maybe descent always exists? But even if true, proving a bounded multi-step descent is essentially the same as proving the distance bound.

**Mover says:** The |V_5| descent bypass is dead. The inductive lift approach (M1's territory) is the only viable path. Resources should concentrate there.

---

*0051-M2-S1 — 18 Feb 2026*
