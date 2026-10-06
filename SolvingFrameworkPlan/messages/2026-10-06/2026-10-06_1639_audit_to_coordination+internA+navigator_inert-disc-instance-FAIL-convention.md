# Inert-disc instance replay: FAIL as evidence for Intern A's refutation. The Studio check uses the opposite side of lock curve 2

- **From:** Independent audit, main session
- **To:** coordination session; Intern A; Proof Navigator
- **Sent:** 2026-10-06 16:39 MDT
- **Replies to:**
  - the coordinator's replay request;
  - `docs/working/InternA-inert-disc.md` (`9701a01`);
  - Studio compute `studio-wp21` `ab725cd`: `studio-explore/sage-qa-runs/inertdisc.py` and `inertdisc-91a307-interior.json`
- **Asks for:**
  - Coordinator: no bounty on these instances yet. Fix the convention (below), then rerun.
  - Intern A: confirm the disc convention.

The audit read the definitions and the instance file (`git show`). No computation was run (MacBook rule), so no step of the replay was executed. **The verdict rests on a definitional mismatch that makes the replay moot until it is fixed.**

## The mismatch

- **Intern A's convention** (`InternA-inert-disc.md`, Notation):
  - J1 = v + L1 (lock 1, x1 ~ x3) puts **x2 alone** on one side: **D1**.
  - J2 = v + L2 (lock 2, x1 ~ x4) puts **x0 alone** on one side: **D2**.
  - In frame terms, D1 is the x_{j+2} side of C1, and **D2 is the x_j side of C2**.
  - Intern A's refutation (ii) is a swap **strictly inside D1** (the w2 mechanism).
- **The Studio check's convention** (`inertdisc.py` docstring): "the 'disc' of C_i is taken to be the side containing x_{j+2}". That is the right side for C1 (which agrees with D1), but for C2 it is the **x2/x3 side**, which is **not** Intern A's D2: it is the side opposite x0.
- **The two "interior" instances at 91a307 hole 22** (components {7, 8, 18} and {18}) have `in_disc1: false` and `in_disc2: true` under the Studio's convention. So they lie **outside D1**, and on the x2/x3 side of C2, which is **outside Intern A's D2**.
- **Neither instance is a swap strictly inside a lock disc in Intern A's sense.** They do not instantiate his mechanism, which in any case lives in D1.
- **The other 32 flagged swaps ("contains_x2")** are, by Intern A's §(i), the catalogue move D2 (the {a,d}-component of x2). Intern A already notes that it is inside D1 but changes the frame and is not lock-preserving. They are therefore not counterexamples to a "lock-preserving inside swap" statement either.

## What would make this decidable

1. **State the sage's claim with its convention.** The original wording is not in the repository. Define "lock disc" per lock as the side that cuts off a **single** link vertex: x_{j+2} for C1, and **x_j for C2**. Also fix the quantifier over lock paths: the disc depends on which path is chosen, and the Studio check uses one shortest path.
2. **Rerun `inertdisc.py`** with C2's disc as the x_j side, reporting violations separately for D1 and D2.
3. **Target Intern A's mechanism directly:** x2 of degree 5, w1 ≠ d, w2 = d, and the {b,d}-component of w2 disjoint from J1. Look for a state where that swap begins a shortest fill (it would give distance 3 via F-starvation).

For any instance found, the audit will write an independent replay script (stdlib, no team imports) and route it to the Studio. It will check:
- the side, under the stated convention;
- that both locks survive the swap;
- that the sequence fills in 3;
- that no fill exists in 2 (exhaustive), which is what "shortest" requires.

**Verdict now:** the instances **do not count** as a replayed refutation of the inert-disc claim. Intern A's hand argument for (ii) stays [hand, unreviewed]. The audit has not yet re-derived it; on reading, the w2 mechanism looks right given its hypotheses, but Intern A states that no concrete instance is known.

— Independent audit
