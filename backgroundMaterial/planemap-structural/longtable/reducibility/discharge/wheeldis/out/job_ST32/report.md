# ST-32: independent verification of Opus's off-centre kill file offc_K3g_2f4f0f02.txt (Studio, 7 Nov)
Spec-only: OFFC_SPEC.md (7a5650b3) was read; Opus's offc2.py / offc.py / pcheck code was NOT read. Verifier: offc_verify.py (our own code), per-line table per_line.tsv, controls controls.py / controls.txt.

## Result: **250 / 250 lines PASS** (d7 68, d8 23, d9 13, d10 13, d11 13, d12..17 20 each — as expected); 246 D, 4 C.
Per line: (0) FILE exists, its md5 starts with md5= (all 12 files: eq_D7_dfast 8d5e826a, k3x_D_A97 d76bc52f, win89 82ebc23f, lp_dfast 6b95208f, win14 808e7be9,
r_2 a9fff70a, r_12 176fd929, r_1 eac8f47e, k3x_C_A97 9f8cfe39, win8 007b46db, r_hr1 d9cd53f6, r_9 c5bea47b), NAME is in it with D=true (D) or a C-REDUCIBLE
X line (C), and r=, m= are read from that line; (1) K rebuilt per section 2 (EX = singleton 5..8 slots; s–s ambiguity skip; Ku iff m = |EX|+1 and r(Ku)=r, K0 iff
m = |EX| and r(K0)=r, r(K) = Σ − E − 3n + 3, connected); (2) section R conditions 1–5; (3) phi has domain V(K), injective, no u>u (section U), x>u only if
deg_K(x) = d, every other image's letter = deg_K(x) ∈ 5..8; (4) induced on the section 1 window (s_{i-1}s_i from w_i's image letter or the 5/N condition);
(5) every 3-clique of K onto a window face; (6) LINK/SWORD equal exactly the image letters plus the w_i conditions. C lines: X edges checked against the entry's
kc line (first match in loop/k*/): every interior X edge is an interior edge, and the kc interior graph is isomorphic to K with degrees.

**Note (C, rim-pinned):** f8_...65856_...6556. (cpat k3x_C_A97) has an X containing the ring edge R8-I1. A ring vertex is not in K, so "all X edges lie in K"
cannot hold literally; I check instead that I1 is a K vertex with R8 among its kc ring neighbours (true) and that the X's interior edges lie in K (true).
The line passes all six checks; it is listed as PASS with NOTE-RIM in per_line.tsv.

## Controls (controls.txt)
1. **Spec test rows**, matched with Studio's own st21 rpatN loader + patmatch (out/job31/st21_check_f2b.py), which are byte-identical to the W17 harness's
   (code_gk7/st21_w17.py:805-815, patmatch :852; its admissible() = not patmatch(...), :863-869): 7/7567675/6666655 is killed by exactly one line,
   `7 757..65 55...66 # D f7_..55756_..5766.` (phi u>w0); 7/8567565/6678565 by exactly one line, `7 856..65 56...66 # D f8_...55756_...6666.` (phi u>w0).
   Both rows are therefore inadmissible once the file is loaded.
2. **Mutations (each FAILS):** LINK letter flip -> "LINK/SWORD … != expected"; swap of two phi images -> "not induced: (s,3) (w,3)"; a registry entry whose K fails
   section R (e7_B55655._5B.66.._1111110 from eq_D7_dfast, an edge s0-w1 in no triangle) -> "section R: R1".

## Spec points I had to resolve
- **Name format:** e7 names carry a third block (e.g. `_1111110`) the spec does not describe; I read every name as `<letter><d0>_LINK_SWORD`, ignoring later
  blocks (the LINK/SWORD lengths equal d0 for all 250 entries).
- **k3x file paths:** the lines give the container path /home/claude/…/s33z/reg_A97/k3x_*; I read them from /tmp/swarm-W17/pat/A97/ (md5s match).
- **Rim-pinned C X** (above): checked as "interior part of X in K, R–I edges attached to a K vertex".
