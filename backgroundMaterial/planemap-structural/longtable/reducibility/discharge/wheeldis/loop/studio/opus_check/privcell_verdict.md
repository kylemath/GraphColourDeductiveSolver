# Private-cell (q-name) guard: Studio spec-only build and check (PRIVCELL_SPEC.md, Opus s36g a9da7812, md5 ebabae02)

**Verdict: the kill line is met by one name.** Studio's own conversion agrees with `s36g/g7_q.txt` on 9 of 10. It
disagrees on #5, `g7_-..655.._..657.._...5.....5`, in the order of its ring-3 chain (Part 1.6 / 1.4, feeding G0).
Under Studio's form, the guard admits all 10 to the private-cell list (4 D, 6 C), with G5 (faces) passing 10/10.

## Independence statement
Built from PRIVCELL_SPEC.md Parts 1 and 3 only (Part 2 read for context, not used). Opus files opened: PRIVCELL_SPEC.md
and g7_q.txt (data, read only after Studio's conversion was done, for the diff). framecheck.py, privcell.py, eng/,
selftest/run_checks scripts and the logs were not opened; file names in s36g/ were seen via git ls-tree only. Inputs:
explore's g7_53_kills* at 63d8c41e (kc lines byte-identical to Studio's held53 file) and Studio's own engine verdicts
(loop/studio/sender_held/g7_53/studio_verdicts.txt, dc1ff9f9).

## Guard (out/job30/privguard.py)
- Part 1: q-name parser; well-formedness (1.5 determinacy: chain pairs fixed consecutive in ring 2, y#k needs y exact,
  private index <= n_i); the 2D images of 1.4 (rotation, reflection with L <-> R, chains reversed, y#k -> y#(m+1-k),
  R -> L(n+1-k) for exact parents) and the canonical form (bytewise min of the rendering); the containment pattern of
  1.5 (vertex list, edges, faces); the g7_ -> q converter of 1.6.
- Part 3: G0 (parses, well formed, canonical round-trip), G1 (two engines), G2 (ring-merge union-find on X), G3 (a
  degree-preserving bijection kc interior <-> constrained slots, every char exact 5..8, u = D), G4 (kc interior edges =
  pattern edges), G5 (every kc interior triangle is a frame face), G6 (arc |A| <= D - 1 for '-' names).
- G3-G5 are decided by exhaustive search over every degree-preserving bijection, so they do not depend on any frame map.
  Admitted names go to out/job30/k3p_D.out / k3p_C.cfast (never k3x); held names to out/job30/privguard_held.log. The
  guard is not wired into the LP and nothing is admitted to the registry.

## Per name (privcell/privguard_run.log)
| # | g7 name | Studio canonical q | G0-G6 | bijections G3 / G4 / G4+G5 |
|---|---|---|---|---|
| 1 | g7_-..655.._..65..._...5...... | q7-_....556_....56._::::::5 | all pass (D) | 48 / 1 / 1 |
| 2 | g7_u76.5566_6..5..._..5....... | q7u_.556676_.5...6._::::::5 | all pass (C {I0-I2}) | 1,152 / 1 / 1 |
| 3 | g7_-..655.._..65..._...5..5... | q7-_....556_....56._::::::5_s5/p6L1=5 | all pass (D) | 240 / 1 / 1 |
| 4 | g7_u..655.._..65..._...5..5... | q7u_....556_....56._::::::5_s5/p6L1=5 | all pass (D) | 240 / 1 / 1 |
| 5 | g7_-..655.._..657.._...5.....5 | **q7-_....556_...756._::::::5_p3R1/s3=5** | all pass (C {I0-I1}) | 240 / 1 / 1 |
| 6 | g7_-..655.._..657.._...5....5. | q7-_....556_...756._::::::5_s3#2=5 | all pass (C {I0-I1}) | 240 / 1 / 1 |
| 7 | g7_-.6655.._..65..._..55...... | q7-_...5566_...56.._:::::5:5 | all pass (C {I0-I1}) | 720 / 1 / 1 |
| 8 | g7_-..655.._.765..._..55...... | q7-_....556_....567_5*::::::5 | all pass (C {I0-I1}) | 240 / 1 / 1 |
| 9 | g7_-.6655.._.765..._..55...... | q7-_...5566_...567._:::::5:5 | all pass (C {I0-I1}) | 720 / 1 / 1 |
| 10 | g7_u7665566_6.65..._..5...5... | q7u_5566766_5...6.6_:::::5:_p6L1/s6=5 | all pass (D) | 172,800 / 1 / 1 |
Face counts equal the kc interior triangle counts on all 10 (4, 8, 5, 7, 5, 5, 4, 5, 7, 12). G6: '-' names |A| = 3..4;
'u' names placed at d = 7 only.

## Disagreement (kill line): #5
Opus writes the chain `s3/p3R1`; Studio writes `p3R1/s3`. Around w3, ring 2 reads s2, p3*, s3, and p3R1 is the private
next to s3, so forward order (1.5 CHAIN "forward order"; 1.4 "chains reversed, so they stay in forward ring-2 order";
1.6 "a chain in forward order") is p3R1/s3. s3's forward successor is s4 (w4 = 5), so `s3/p3R1` does not parse as a
well-formed chain under Studio's reader (G0). Likely origin: the g7 slot is spelt t(p51/s4) with p51 first, which is
not forward order (s4/p51); reflecting and reversing p5L1/s4 gives s3/p3R1. The pattern (vertices, edges, faces) is the
same either way; only the canonical string, and so name identity and dedup, differs.

## Spec ambiguities (each with the reading Studio used)
1. Chain order in 1.6 when the g7 slot is not spelt in forward order (above): Studio sorts to forward order.
2. 1.6 "L1 if it is the first private and s_{I-1} is named, **or shares a chain with a named private**": the second
   clause is not exercised by the 10 names; Studio implements only the s_{I-1} and s_I clauses.
3. Rendering a non-exact group whose R part is empty: Studio writes `L*` (agrees with #8's `5*`).
4. An exact-parent group with a constrained private is written with all n_i chars (only n_i = 1 occurs here).
5. "Interior triangle of the kc configuration" (G5) is read as a 3-cycle among the kc line's interior vertices.
6. A 'u' centre counts as a constrained slot of degree D in G3's bijection (matches every m here).
7. Part 3 says an admitted name is passed on with its Part 2 absorption class; Part 2 was out of scope here, so k3p lines
   carry no class.
