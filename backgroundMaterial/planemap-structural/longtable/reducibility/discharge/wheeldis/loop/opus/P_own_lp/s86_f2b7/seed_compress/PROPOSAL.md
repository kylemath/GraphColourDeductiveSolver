# Compressing the RSST seed with our LP engines: proposal (Opus, 10 Nov 2026 16:05Z)

**Goal.** Start from the seed certificate: RSST's 71 parts as our rules, the 633 configurations as kills, every realisation state ending ≤ 0 [E2].
Find the fewest rules and configurations that still give t = 0 on realisation rows. No CPU has been used for this page.

**Principle.** The LP only *proposes* drops. A drop counts only when an exhaustive fixed-point check passes over all fillings, at every degree, on two engines:
* W6r fp_exact (RSSTFP_SPEC), then the Studio one-shot.

## 1. Rules: which parts to drop or merge into our keys

* **Expressible parts.** 52 parts map to 27 EDGE keys (`cg_keys_rsst.txt` cba3c43c, `rsst_amounts.json` f836a669; rsst_closure §1).
  * In the LP, make their amounts free columns, with caps at the RSST value or a small multiple of it.
  * Add our own columns beside them: the 365 keys plus HATBB, so the LP can substitute.
  * Objective: reweighted L1 at t = 0. First Σ a_k / a_k^RSST, then two or three rounds with weights 1/(a_k + ε). That approximates "fewest parts".
  * A part whose amount goes to 0 is a drop candidate. Two parts whose coefficient vectors are identical on all tight states merge into one key.
  * The chirality pairs are already merged (one key at 0.1 covers a part and its mirror).
* **The 19 non-expressible parts stay fixed at RSST amounts** as constants until our grammar can price them:
  * fan conditions: drule5/7/25/27 (8 parts);
  * payer-8 with S.L±3: drule28/30/31/31' (7 parts);
  * S.L±4: drule29/32 (4 parts).
* **Making some of them compressible.** Lifting W5 to exact S.L±3 at d = 8 in the upper OUT is an eng_p8 change, and it makes drule28/30/31/31' compressible. The fans and S.L±4 need IN read as "possible" (the middle private of an 8), so W6r's engine should price those.
* **Expected outcome.** Our keys already carry most d7/d8 load (5/6/7 world at t = 0 with 87 generic keys, 6 Nov). Likely drops are the hub-7 EDGE parts that our 6-relay or q7 columns duplicate. The likely keepers are the big-pays-big parts (drule8/9/21/28/29), which none of our keys reproduces (closing-review, 9 Nov).

## 2. Configurations: which of the 633 our family u kills already cover

* **Free substitutions.** Using `fam_args/u/patterns_K3gB5u.tsv` (fbc6aaf5; drop the 5 lines from pat_K5[stu] for the Lean-only set):
  * Call an RSST config c *covered* when every state it kills, in the seed's state list, has a row label that admissible() rejects on family u.
  * Our kills act on the whole label class, so covering is sound for every filling.
  * Covered configs are dropped with no LP. W6b runs the cover test, and our engine checks admissible() on the label list it sends.
* **Remaining configs: greedy drop.**
  * Order by how many states only that config kills, fewest first.
  * For each config, take the states it alone kills and compute the max final charge there at the current LP amounts. If it is ≤ 0, the config is a candidate drop.
  * Drops interact, so re-solve the rule LP after every batch.
* **Configs that need private letters (242).** Our pattern kills cannot replace them: our patterns read only link and apex letters. They can only become unnecessary through slack in the rules.
* **The 51 "none" configs.** These come first: each one dropped removes a Lean port (valid_contract). The RSST-SUB substitutes (nl2837_r11, nl3352_r13, the ring-14 and ring-13 C windows, P20 / P21, 37 2026-set D for d9/d10) go into the same greedy pass.

## 3. Row model the LP needs

* **d7/d8.** v2 realisation rows (eng_v2 `upperR2 v2r`, V2ROW_SPEC, gate PASS 9 Nov), with the domains of RSSTFP_SPEC §5.
  * Needed: kills that tie adjacent privates (W2p), entered as forbidden transitions in the max-plus over Q_j (rsst_closure §4 item 5).
* **d6 (cons2).** Two changes:
  * Add a private dimension.
  * Add a kill mask on (link, apex): flag `k6pat`. This is the path we held this morning for P21. In the K582 run, all 3,917 d6 survivors are 2.126 alone.
  * The mask goes into cons2 separation, the warm and initial cons2 rows, the upperR2 conservation loop and the lower exact check, and the Studio harness needs the same change.
* **d5.** Sender rows per filling. There are no domains at d = 5, 6 (spec §5).
* **d ≥ 9.** Our window reading (U = min(d,9), wildcard privates at d ≥ 10) is conservative and would block t = 0 at d9..14, where the seed needs kills. Two options:
  * use exact rows to d = 14 (words searched 2,905 / 1,911 / 949 / 266 / 30 / 2);
  * or take W6r's exact d9..14 states as separated rows.
  * d ≥ 15 closes with no kills, so a DP tail bound suffices there.
* **Size.** The full realisation space is too large for one LP (d7/d8 sets alone are 541.6M fillings).
  * Use cutting planes: start from the seed's states with hi > −ε.
  * W6r's engine is the separation oracle: it returns the violated states at the current amounts, and we add them as rows.
  * GV1 showed about 90k realisation rows per round is our practical LP size.

## 4. Risk: compression reintroduces the private-letter gap

* **Wrong direction.** If the LP sees a subset of states (cutting planes) or masked rows, it can accept a drop that fails on an unseen filling.
  * This is the 10 Nov 06Z gap: 21.2% of d7 rows are positive for *some* private filling.
  * Guard: no drop stands on LP evidence. Each batch is re-run exhaustively (fp_exact + Studio one-shot, all degrees). A failure returns its states as new rows.
* **Masked rows.** Running compression on p1r or masked rows only makes the LP stricter: it fails to compress but stays sound. So masked rows are a fast pre-screen, never the acceptance test.
* **Kills on label classes.** Replacing a private-reading RSST config with one of our label kills is always sound. The reverse, dropping our kills and keeping RSST's, never happens here.

## 5. Where W6r's fixed-point engine is needed instead of ours

* Every acceptance check: exhaustive over fillings at d5..14+, with section 7 (induced window).
* The 19 non-expressible parts, both as fixed contributions and as the oracle when we test dropping them.
* The separation oracle for the realisation LP, and per-filling kill coverage, including W2p adjacent-private kills.

## What I would build first (when the seed is in Lean)

1. **Stage A** (no engine change). An LP over the 27 RSST keys plus our 365 + HATBB on W6r's tight d7/d8 states: an L1 drop list for the expressible parts, then a W6r re-check.
   * First, a cheap test of how far rules alone compress: replay the outside team's exact primals (swarm/outside/outside-argon-7nov/: certs/primal_t0_16rules_84conds_exact.json, 16 rules on the 5/6/7 world; certs/primal_d8_studio_17rules_exact.json, 17 rules on the Studio d8 receivers) on our W16-world rows.
2. **Stage B.** Cover test of the 633 against family u (W6b list, our admissible()), then the greedy config pass. Cover test done 10 Nov: cover/README.md (every cover is the config itself; 189 of the 403 already have a Lean copy).
3. **Stage C** (engine work, only if A and B leave large sets). Add `k6pat` and d6 privates, exact d9..14 rows, and W5 S.L±3.
