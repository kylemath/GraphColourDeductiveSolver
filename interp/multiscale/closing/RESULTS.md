# Closing step (b) of Conjecture LML: stress test and mechanism

22 Oct 2026. Scripts and outputs are in this folder. `cl.py` is the library: CNF builder, level colourings with a forced monodromy or phase, exact closing R, chordless splits. Labels: **[P]** proved (argument given), **[M]** measured (SAT, exact for the instance), **[C]** conjecture. Notation and τ are as in `../levelling/RESULTS.md`. R = 0 means only the conflict vertices are recoloured, the same convention as `lev.merge`.

## 0. Numbers

| experiment | instances | closing R histogram | max R |
|---|---|---|---|
| E1 `e1_sample.py`: 105 chordless splits; maps ico10 (n=1002), ico20 (4002), BASE_rand22 (4842), BASE_defect_ico17 (2892), M3_ico22_hard (4842); 7 split kinds (below); up to 30 level pairs per split, forced monodromy classes included | 2110 pairs | 0: 273, 1: 731, 2: 1105, **3: 1** | 3 |
| E4 `e4_scale.py`: ico20, balanced and wiggly splits, seam L = 222–281 edges | 60 pairs | 0: 2, 1: 24, 2: 33, **3: 1** | 3 |
| E6 `e6_phase.py`: structured adversary that forces A's and B's boundary walks onto opposite sides of their centres, arc by arc; ico20 and BASE_rand22 | 80 pairs (30 more were infeasible) | 1: 18, 2: 61, **3: 1** | 3 |
| **total** | **2,250 closings** | 0: 275, 1: 773, 2: 1199, 3: 3 | **3** |

The split kinds were:
- `bal`: half balls;
- `wig`: halves grown from a random frontier;
- `third`: A of size about n/3;
- `lop`: B is a ball of radius 2–4;
- `lopA`: A is a ball of radius 1–3, down to 7 vertices;
- `dsx`: edge flips within distance 1 of the seam, giving degrees 5–9 and up to 90 vortices touching the seam;
- `dsA`: the same flips on the A side only, so the vortex charge sits on one side.

Every split was checked: A and B are both discs with induced boundary cycles.

**No counterexample to (b) was found.** The worst cases are the three R = 3 closings. All three are on the dome ico20: balanced seams of length ≈ 250 that are (nearly) Eulerian, with 0 or 1 odd vertex within distance 1 of the seam, and both sides forced to |t| = 2.
- Vortex-dense maps (random, defect, binder) never needed more than 2. That includes seams with 90 vortices on them and one-sided charge.
- Small sides (`lop`, `lopA`, down to a 7-vertex wheel) needed R ≤ 2.
- Max R was 2 on ico10 (seam length ≈ 100) and 3 on ico20 (≈ 250). Slow growth with seam length **cannot be excluded**: the ico30/ico40 scaling runs did not finish in the time box.

Other probes:
- **[M] CEGAR "window" adversary** (`e2_cegar.py`, ico6). It finds level pairs that agree across the seam except in a window and that the identity renaming cannot repair at R = 1. Another renaming then repairs them at R = 1. **The renaming is doing real work.**
- **[M] CEGAR "band" adversary** (`e3_band.py`, ∀π, recolour N_R(seam)). At R = 0 on ico4 it finds pairs (true R = 1). At R = 1 it had not converged after 15 min, so there is no exhaustive certificate.
- **[M] Torus control** (`e5_torus_closing.py`). 99 fat 6-regular tori T(p,q,r) that are 4-colourable but not 3-colourable (p ≡ 0 mod 3, q = 4–10, n ≤ 600). The two horizontal bands A and B are each 3-coloured, so they are perfectly flat with τ = √3/2.
  - In every case the conflicts fill one entire seam loop: 4p/3 vertices.
  - Recolouring exactly those vertices closes the colouring (R = 0).
  - On the 278 non-4-colourable tori of `../levelling` §4, closing fails at every R.

## 1. Mechanism

**[P] Lemma 1 (Z3 class of the seam).**
- Setting: let Ω be the band of vertices within distance 1 of ∂A ∪ ∂B, and suppose every vertex of Ω has even degree. Take the even case, where the face up/down orientation closes around the core. Let f(a e_g + b e_h) = a + b mod 3.
- Claim: there is a geometric χ(Ω) ∈ Z3 such that **every** 4-colouring that is proper on an A-collar or a B-collar of Ω has f(t) = ±χ for that collar's boundary translation. The sign is the orientation and gauge convention.
- Proof:
  1. f∘h is a proper 3-colouring wherever h is single-valued (`levelling` §4). Around the core it returns shifted by f(t).
  2. A 3-colouring of an Eulerian near-triangulation is unique up to permutation. So propagating the 3-colouring around the core of Ω gives a fixed permutation, and χ is that permutation.
  3. Both collars are homotopic sub-annuli of Ω, so they see the same χ. ∎
- Corollary: a level colouring has |t| ≤ 2τ ≤ 2 and t ∈ 2Λ, so t ∈ {0, ±2e_g, ±2e_h, ±2e_{g+h}}. Here f(t) = 0 iff t = 0, and each nonzero f-class is a single D3 orbit. Therefore **t_A = t_B = 0, or |t_A| = |t_B| = 2 and some renaming aligns them.**
  - [M] Forced-t SAT confirms this: on Eulerian-seam splits exactly one class ({0}, or one 3-element orbit) is feasible on each side.
  - [M] Across E1 and E4, the classes "zero" and "nonzero" never mix when at most 2 odd vertices lie within distance 1 of the seam (420 even/even pairs). Mixed classes, 0 against nonzero, occur only when more vortices touch the seam (270 pairs, all with R ≤ 2).

**[P] Lemma 2 (bounded mismatch on the closing seam).**
- The closing seam is one loop. A renaming acts on heights as h ↦ P h + c, and c is free because each disc's height is defined only up to a constant.
- Choose P as in Lemma 1. The offset o(i) = H_A(i) − P H_B(i) − c is then periodic around the loop, so its diameter is at most 2τ_A + 2τ_B ≤ 4.
- This is `levelling` (i), now justified for a *closed* seam. Without Lemma 1, o would wind by t_A − P t_B around the loop and nothing would bound it.

**[P] Lemma 3 (what the torus lacks).**
- Claim: when A and B are annuli whose seam has two components, the relative constant can be gauged away on one component only. On the other, the offset jumps by the period t_γ of a loop that crosses both seams. Neither τ_A nor τ_B sees t_γ.
- Proof: the loop γ lies in neither side, so neither boundary walk measures its period, while each extra seam component carries its own offset constant and a single renaming has only one c to spend. ∎
- Consequences:
  - On non-3-colourable 6-regular tori, |t_γ| ≥ 2 is forced (`levelling` §4).
  - On fat tori the jump is a uniform shift along a whole seam loop. It is cheap: [M] R = 0, but recolouring O(L) vertices.
  - On the thin non-4-colourable tori no closing exists.
- So the clean contrast is the following. **On the sphere the only seam invariants are the monodromies, and they are matched (Lemma 1) and bounded by τ (Lemma 2). On a handle-seam there is one extra, ungaugeable offset per extra seam component, and τ does not control it.**
- Lemma 1 also fails on the torus in the sense that matters: t_γ is not a boundary monodromy of either side.

**[M] Where R comes from.**
- Eulerian seams (no odd vertex within distance 1), E1 + E4:
  - t = 0 on both sides: 240 pairs, R ≤ 1 (208 of them R = 0);
  - |t| = 2 on both sides: 50 pairs, R histogram {1: 28, 2: 21, 3: 1}.
  All three R = 3 cases have |t| = 2 on both sides.
  - A plausible reason [C]: with |t| = 2 the walk must cross the whole unit disc in one lap. The offset then sweeps a diameter-2 segment, so M is about 4, against M ≤ 2 to 3 when t = 0.
- Localisation (`loc.py`). Starting from radius R − 1 everywhere, does adding radius R inside one ball of radius ρ around a single seam spot suffice?
  - Instance e4_R3: 4 of 44 spots suffice with ρ = 4. The spots are clustered at distance 8–9 from every odd vertex, so the obstruction is **local**.
  - Instance e6_R3: no single spot suffices, even with ρ = 14. The obstruction needs at least two separated spots, or a long stretch.
- Vortices near the seam cap R at 2: dense maps have R ≤ 2, and so do the mixed-class pairs. This fits the picture that vortices are where mismatch is absorbed. They do not make R = 0 common, though: 0 occurred in about 2% of the 1,566 pairs with more than 2 vortices at the seam.

## 2. Status of (b)

- **[C] Band-filling form of (b).** On a planar closing seam with level sides, Lemmas 1 and 2 give matched monodromy and offset diameter M ≤ 4. The conjecture is that an annular band with matched monodromy and offset diameter M can always be filled with width c(M), with c(4) ≤ 3 + O(1) independent of the seam length.
  - Together with Lemmas 1 and 2, this would imply (b) with R = c(4).
  - It is a Lipschitz-extension statement for Kondev–Henley heights. It is the missing piece and is **not proved**. Note that the (T) family of `seam_lemma.md` needs M ∝ L, which τ ≤ 1 rules out.
- **Calibration.**
  - The adversaries are sampling-based plus structured (forced t, forced phases, window CEGAR). The only exhaustive certificate is the trivial R = 0 band case on ico4.
  - Max R rose from 2 (ico10) to 3 (ico20). Three R = 3 cases in about 650 ico20 closings is compatible either with a bounded constant or with slow extreme-value growth in L.
  - The decisive missing measurement is the R distribution on Eulerian |t| = 2 seams of length 400–1000 (ico30–ico50). The `e4_scale.py ico30,ico40` run was stopped before any result: level SAT on 4500-vertex sides is slow.
- **Note on the definition.** R counts from the conflicts, and conflicts can be dense. On the torus they fill a whole seam loop, so R = 0 can mean recolouring O(L) vertices. Any finite-check reduction of (b) should bound the *number* of recoloured vertices per unit length of seam, or use the band form above.

Files:
- `e1.jsonl`, `e4_scale.jsonl`, `e6_phase.jsonl`, `e5_torus_closing.jsonl`: results;
- `e4_R3_*.pkl`, `e6_R3_*.pkl`: the worst instances (adjacency, A, c_A, c_B);
- `e2_found_*.pkl`, `e3_found_*.pkl`: the CEGAR witnesses.

In E1 the "t(..)" labels are unreliable: the first forced-t encoding allowed a spurious end point and was fixed mid-run. The measured `tvec` fields, and all R values, are correct.
