# Dissipation network: Stage 1 brief (13 Nov 2026)

Written by the cloud thread "families" for a session running on the Mac Studio in this repository.
k's instruction (12 Nov, 18:21 Edmonton): "run them here on my computer", after asking for the method to be run
"on bare metal with speedups in training from using bit control and rounding and ranking based on mantissa, then
post attention and selection pruning of ignored features to reduce compute", and "add any other efficiencies or
speedups you can think of".

Proposal document (k has it): https://claude.ai/artifact/K7kVZV2BdxaqriaGcywmgW
Background measurements: `FABLE_IDEAS.md`, `OPERATIONS_IDEAS.md`, `stage0/RESULT.md` in this folder.

## The idea in one paragraph

Discharging is treated as a small network that runs on the map for two or three rounds and is trained by descent,
instead of solving a linear programme for the amounts of a fixed list of rule pictures. Each round every vertex
looks only at its direct neighbours and at the charge it holds so far, then sends charge along its edges. The loss
is the largest charge left on any neighbourhood that contains no reducible configuration (no kill). Loss 0 is a
candidate proof; it is then rounded to exact fractions, unrolled into ordinary rule parts and checked by the
existing exact engines. What is new is that round 2 reads the charge so far ("forward your surplus"), which a
linear programme cannot express.

## Model (charge unit = 1/60 of a degree-5 vertex's 60; a vertex of degree d starts with 60(6 - d))

1. Round 1, push. Every vertex u of degree 5 or 6 sends a(u -> v) to each neighbour v. a is an integer table
   lookup (multiples of 3) indexed by threshold bits: deg(v) >= 6, >= 7, >= 8, >= 9; the same bits for the two
   common neighbours of u and v; the count of 5s around u (bucketed). Mirror positions share entries.
2. Round 2, forward. Every vertex u of degree >= 7 computes its charge c1(u) after round 1. If c1(u) > theta
   it sends s = c1(u) - theta onward, split over its neighbours by attention with a budget of exactly 1:
   share(u -> v) = sparse-normalise_v( score(v | u) ), score = integer weights over bits of: deg(v) thresholds,
   the degrees of v's two ring neighbours around u and the two hats beside v (pooled one/both for mirror symmetry),
   v's fans (count of 5s, count of 7+), thresholds on c1(v), and pair conjunctions of these bits (Stage 0 showed
   single bits are too weak: 44% vs 72% with pairs). Attention is masked to edges. Use a normalisation that gives
   exact zeros (sparsemax or top-1 / top-2 with a learned margin) so shares harden to 1 or 1/2 + 1/2.
3. Optional round 3: a second forward step (covers the tunnel moves).
4. Mask: a neighbourhood that contains a kill (a reducible configuration from the proof stack) is excused.
   Stage 1 keeps the kill list fixed. Stage 2 adds a dial in [0, 1] per configuration with a price.
5. Loss: smooth maximum (log-sum-exp with rising temperature, or CVaR of the top rows) of the final charge over
   all unexcused neighbourhoods, plus an L1 price on non-zero table entries and score weights.

Charge is conserved by construction: every transfer is on an edge, and the shares of a vertex sum to 1.

## Stage 1 task

World: degrees 5, 6 and 7 only (the W16 "5/6/7 world", report in `w16/REPORT.md`; its code and data are copied in
`w16/` but the code has cloud-container paths hard-wired: `/home/user/...`, `/tmp/swarm-W10`, `/mnt/project-files`.
Re-point them at this checkout or re-derive the rows with the Studio's own engine). Known facts for that world:
110,087 admissible degree-7 receivers on the Studio-full stack; no existing single-round family reaches t = 0 there
(floor about 0.0058 to 0.0072 with full q7). So a result of 0 here would be something the linear programme
families could not do, and a result stuck above that floor is a failure of this idea at Stage 1.

Steps:
1. Build the row set: every admissible neighbourhood needed to evaluate the final charge of a degree-7 vertex
   (and the 5 and 6 conservation rows) in the 5/6/7 world, with the kill mask from the current sound stack
   (use whatever the Studio's engines treat as current; record which stack and its hashes).
   NOTE the reach: a forward step makes a vertex's final charge depend on its neighbours' round-1 charge, i.e.
   one ring further than the rows the LP uses. Decide how to handle it and write it down: either enumerate the
   wider neighbourhood, or bound the unknown outer ring conservatively (worst case over the outer letters, as the
   LP's realisation rows do). A conservative bound keeps soundness; say which you used.
2. Implement the network evaluation on all rows as tensor operations. Use the Mac's GPU if a framework with Metal
   support is installed (PyTorch MPS or MLX); otherwise NumPy/Accelerate. Do not install system-wide packages
   without need; a local virtual environment inside `dissipation/` is fine.
3. Train. Then harden (snap amounts to multiples of 3, shares to 1 or 1/2 + 1/2, retrain the rest), prune
   features by rounded weight size and retrain (Stage 0: pruning 1,151 -> 200 features improved held-out accuracy).
4. Evaluate the hardened network EXACTLY (integers) on every row. Report max final charge, the binding rows, and
   the number of non-zero parameters.
5. If max final charge <= 0: unroll to rule parts and hand to the exact two-engine check. Do not claim a proof
   from this code alone; label results [P] one engine until a second engine agrees.

Speedups k asked for, apply where they help and say which were used:
- bit-packed features (uint64 words) and integer or fixed-point weights; mistake-driven or sign updates where possible;
- round weights to a few bits of mantissa and rank by that magnitude for pruning;
- after training attention, drop the features and rows it ignores (rows far below the maximum can be sampled or
  dropped with periodic full re-checks: active-set / hard-negative mining, like the LP's row generation);
- merge duplicate rows (mirror-canonical form), drop never-set feature columns, early stopping;
- anything else that is sound (cache round-1 charges per neighbourhood class, batch by hub degree).

Pass / fail for Stage 1:
- PASS: exact max final charge <= 0 on the 5/6/7 world after hardening.
- INFORMATIVE: below the LP floor for that world (about 0.0058 in t units; convert units and say how).
- FAIL: stuck at or above the LP floor after a reasonable effort (a few hours of compute).

## Ground rules on this machine

- k stopped all proof jobs on 11 Nov ("stop everything for now while i regroup"); see `out/STOP_20261111.md` if
  present. Do NOT restart, kill or modify any of those jobs, queues or their files. This task is separate.
- Work only inside `dissipation/` (new files) unless reading. Do not push to any branch other than
  `claude/project-thread-mmceyr`. Commit results there (code, a RESULT.md, small data; no large binaries).
- Keep runs bounded: note wall time and core use; leave the machine usable.
- Report back plainly: what ran, numbers with units, what failed, what you could not find. No claims beyond
  what the exact integer evaluation shows.

## Stage 0 (already done in the cloud, for reference)

Imitating the outside team's receiver choice on 4,928 neighbourhoods: best 76% exact on held-out rule families
with 200 pair features (pass line was 95%). See `stage0/RESULT.md`. `stage0/gen.py` needs the outside team's rule
file, which is in this repository as `dissipation/data/synth_rules_588.txt` (an earlier version of this brief said otherwise, wrongly); Stage 1 does not need it.
