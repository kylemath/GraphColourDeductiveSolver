# Independent validation of Math's disc generator, and of the order-24 (G*) certificates

Independent audit, 6 October 2026. This is an exploratory validation. Orders 18–24 are spent, and are used here only to test a tool. The audit's code imports and reads no Math or Long Table code:
- `rigid_census.py`
- `case_walk_check.py`
- `chord_states.py`

Definitions are taken from the written pages (`MathNDiscSearch/README.md`, `MathNAttack.md`, `MathNCaseI.md` §1 and §3, `MathNIaIb.md`).

## 1. plantri

- The tarball on disk (`/private/tmp/claude-501/ncounter/plantri58.tar.gz`) has SHA-256 `e78a9441…29b8`, the hash declared in WP20.
- The audit built its own binary from it in the audit scratchpad.
- `plantri -m5 -a n` for n = 16–22 and 24 hashes identically to `longtable/wp20/input-m5-n.txt`.

## 2. The disc generator against an independent census

**Object.**
- A tuple (T, x, labelled ring u0..u4, proper 4-colouring of T − x).
- T is a minimum-degree-5 triangulation from plantri, and x has degree 5.
- The ring is either direction and any start of the rotation at x.
- The ring word is D α D β γ.
- The object is **rigid**: all six two-colour subgraphs of T − x are forests, with components (1,2,2,1,1,1).
- The object is **legal**: no ring chord.

**Canonical form.** A breadth-first planar code from the dart x → u0, with the orientation fixed by u0 → u1. This identifies mirror embeddings and graph isomorphisms that preserve the labels. The audit re-derives faces and orientation from the edge list on both sides, so both sides go through the same code path.

**Result.** At every order the generator's DISC lines are exactly the audit's set of rigid classes:
- no line is rejected (every line is a valid minimum-degree-5 triangulation, proper, rigid, chord-free);
- no class is missing;
- no class is extra;
- no class appears twice.

| Order | plantri graphs | Audit classes | Generator lines | Missing | Extra | Rigid labelled states with a ring chord (excluded by design) |
|---|---|---|---|---|---|---|
| 12–16 | 1, 0, 1, 1, 3 | 0 | 0 (12, 14, 16; 15 not run) | 0 | 0 | 0 |
| 17 | 4 | 75 | 75 | 0 | 0 | 0 |
| 18 | 12 | 74 | 74 | 0 | 0 | 0 |
| 19 | 23 | 170 | 170 | 0 | 0 | 0 |
| 20 | 73 | 1,565 | 1,565 | 0 | 0 | 0 |
| 21 | 192 | 5,146 | 5,146 | 0 | 0 | 0 |
| 22 | 651 | 15,840 | 15,840 | 0 | 0 | 0 |
| 23 | 2,070 | 78,005 | 78,005 | 0 | 0 | 120 |
| 24 | 7,290 | *running* | 313,493 | | | |

**Generator convention.** One line per class of labelled ring, with mirror images identified and the ring direction kept. It is not "up to reversed labelling": that would halve the counts, which the audit computes as `classes_mirror_identified` (38, 37, 85, 784, 2,573, …).

**Negative control.** The audit dropped one order-17 line, deleted an edge in a second and recoloured a third. The comparison then reports 3 classes missing and rejects the two corrupted lines ("not a triangulation", "improper"/"not rigid").

**Scope.** This validates the generator's completeness and soundness for the stated object class at orders ≤ 23. It does not test the Prop 3 size targets as a separate claim. They are, however, tested implicitly: the audit's census does not use Prop 3, and finds no rigid disc that Prop 3 pruning would have lost.

**Ring-chord states (scope note).**
- The generator forbids ring chords, so rigid states with an illegal fan are outside its object class by design.
- At order 23 there are 120 such labelled states; at orders ≤ 22 there are none.
- `chord_states.py` tests whether any of them is locked at every *legal* admitting fan. That would be a D1-relevant state that the (N) setup never sees. *Running; result to follow.*

## 3. The four order-24 certificates and the Case table

The audit re-derived the walk and the predicate from the written definitions (`case_walk_check.py`):
- c′ = ν_γ c, the swap of the [D,γ]-component of u2;
- c1 is the swap of the [α,γ]-component of u4;
- c2 is the swap of the [α,β]-component of u4;
- Case I ⇔ u2 ~ u4 in [β,γ]₂;
- c3 is the swap of the [β,γ]-component of u4;
- (G*) ⇔ u1 ~ u3 or u1 ~ u4 in [α,γ]₃;
- c″ is computed as c′ of the reversed labelling.

Locks are complete Kempe-class searches in G = T − x u_i; no cap was hit.

- **Reproduces Math's tables exactly.**
  - The order-17 pair (one Case II and one Case I neighbour each).
  - The order-23 table of `MathNCaseI.md` §2, disc by disc.
  - Order 24, all 26 locked discs (`locked24.txt`):
    - every disc is triply locked, and (N) holds on all of them;
    - case pairs: II×II 10, I×II 10, I×I 6;
    - neighbour types: II 30, Ia 18, Ib 4;
    - no disc has both neighbours Ib.
- **The four certificates `cert24/bad_24_{p0_8, p1_2, p3_3, p3_4}.txt`.**
  - Each is a valid rigid minimum-degree-5 triangulation, and appears in `out2_24_*`.
  - Each is triply locked, and (N) holds on it.
  - Each has **exactly one Ib neighbour**: (G*) fails, and the chain {D,β} at c3 is intact:

    | Certificate | Ib neighbour |
    |---|---|
    | p0_8 | c″ |
    | p1_2 | c″ |
    | p3_3 | c′ |
    | p3_4 | c′ |

  - So **(G*) and T3\* are refuted at order 24, confirmed independently.**
- **Naming.** The certificate file suffix is the 0-based line in `res2_24_<part>.txt`. Math's 08:31 message cites the 1-based line: p0 line 9 = `bad_24_p0_8`, and so on. These are consistent.
- **A side observation, in the data.** In every Ia case the chain {D,β} at c3 is broken, and in every Ib case it is intact. This is Lemma D's equivalence, as Math states it.

## Files

- `rigid_census.py`, `case_walk_check.py`, `chord_states.py`
- `out/census-compare.jsonl`
- `out/census-19-23-timing.txt`
- `out/census-small-orders.txt`
- `out/negative-control-17.txt`
- `out/case-walk-17-23.jsonl`
- `out/case-walk-locked24.jsonl`
- `out/case-walk-cert24.jsonl`

Cost so far: about 30 CPU-minutes, single process.
