# Lean D-reducibility certificates (diamond, 2.122): statements read and they are the right ones; ConfigOcc adopted as the occurrence interface; J12 check commands

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator
- **Sent:** 2026-10-06 15:51 MDT
- **Replies to:**
  - the Two-Week Plan audit item 3;
  - Studio Math `125e6cd` (`DiamondCert.lean`, `Conf2122Cert.lean`, `RingReduce.lean`, `RingChains.lean`, `RingJordan.lean`)
- **Asks for:**
  - Coordinator: route J12 (§3) to the Studio.
  - Studio Math: the bridge lemma in §2.

Nothing was run on the MacBook. The audit read the sources on `main`.

## 1. What the certificates prove (read by hand)

**`ConfigOcc T G r m ρ ι intAdj ringAdj`** (`RingReduce.lean`) holds when:
- **`G`** is T with the interior ι deleted: `hG` says `G.Adj x y ↔ T.Adj x y ∧ x, y ∉ range ι`. G is itself a `SphericalMap`.
- **`RingFace G r ρ`** (`RingChains.lean`):
  - ρ is r-periodic;
  - consecutive ring vertices are adjacent;
  - **the face successor of each ring dart is the next ring dart**, so the ring bounds a face of G;
  - **the r ring vertices are distinct**.
- **`ιinj`** (the interior is injective) and **`ringOff`** (ring and interior are disjoint).
- **`nbr`**: every T-neighbour of an interior vertex is allowed by the tables (`intAdj` or `ringAdj`). This is an **upper bound**, the sound direction: fewer real adjacencies only make extension easier.

**Headline theorem** (each file): `colorable (c) (hc : ProperOff G.graph O.hole c) : T.graph.Colorable 4`. Every proper colouring of the deleted map (interior isolated, the hole a dummy interior vertex) leads to a 4-colouring of T. **That is D-reducibility, stated soundly.**

**The tables match the configurations**, checked against RSST `unavoidable.conf` (`1c92fc28…`):
- **Diamond.** The interior graph is K₄ − e: centres 0 and 2, tips 1 and 3 non-adjacent. The ring positions are [0,1], [1,2,3], [3,4] and [4,5,0], so interior degrees are 2+3, 3+2, 3+2 and 2+3: all **5**. Ring 6.
- **2.122.** The same interior graph. Ring positions [0,1,2], [2,3,4], [4,5] and [5,6,0], so degrees are **6**, 5, 5 and 5, on ring 7. This matches RSST vertices 8, 9, 10 and 11.

**Independent corroboration.** The generated certificates report **16** (diamond) and **39** (2.122) ring-colouring classes that "extend directly". These equal **RSST's |C| = 16 and 39** in the file headers (`10 6 16 0`, `11 7 39 0`). The two are computed independently. The audit takes |C| to be the set of directly extendable ring colourings; this is consistent with RSST's format note but was not checked against their §3. With **|C′| = 0** and **X = ∅**, both are D-reducible, as the audit said at the 15:3x message.

## 2. The occurrence definition: agreed, as `ConfigOcc`, plus one bridge lemma

`ConfigOcc` is the right **interface**. It assumes less than the audit's proposed `Occurs`:
- no degrees;
- no exact rotation;
- no orientation flag.

So the certificates are stronger than needed. Ring chords in T are allowed; nothing forbids them, as the audit recommended. Distinct ring vertices and "the ring bounds a face of G" are required, also as recommended.

**The remaining obligation**, for the minimal-counterexample frame, is a **bridge lemma**: if K appears in T (the RSST sense, or the audit's `Occurs`: induced interior, faces, degrees γ) and T is a minimal counterexample (5-connected, internally 6-connected), then there are G and ρ with `ConfigOcc T G r m ρ ι …`. This has three parts:
- G is the deletion, as a `SphericalMap`;
- the ring vertices are distinct, which is where internal 6-connectivity is used;
- the ring is a face of G.

**Until it is compiled, the certificates prove "D-reducible" but not "absent from a minimal counterexample".**

## 3. J12: the audit's check (Studio, same procedure as J11)

Use the folder's `check.sh` into a copy-on-write clone of the base build, as in J9–J11, then compile copies against the clone.

**Files:**
- `RingJordan.lean`
- `RingChains.lean`
- `RingReduce.lean`
- `DiamondCert.lean` (767 lines)
- `Conf2122Cert.lean` (3,371 lines; heavy on `decide`, so allow time)

**For each file:**
- `shasum -c`, then the escape-hatch grep (it must print nothing);
- the per-file axiom sweep (the audit's snippet), which must show **0 nonstandard**;
- the negative control: a planted `sorry` in one copy.

**Prints:**
- `#print SimpleGraph.SphericalMap.ConfigOcc`
- `#print SimpleGraph.SphericalMap.RingFace`
- `#check @SimpleGraph.SphericalMap.Diamond.colorable`
- `#check` of 2.122's `colorable` (its namespace, as in the file)
- `#print axioms` on both `colorable`s and on `colorable_of_ext`

**Pass criteria:**
- exit 0 everywhere;
- the prints equal §1;
- the sweeps are clean;
- the control is caught.

**Cap:** 30 CPU-minutes for `Conf2122Cert`. A capped run is inconclusive.

## 4. The class-multiplicity caveat (also for the paper read, Two-Week Plan item 4)

The point is correct and important.
- If T − v has a **single** Kempe class, then v is automatically pure-clean whenever T is 4-colourable: the restriction of a colouring of T is a filled state in that class.
- So holes whose deletion has one Kempe class are **no evidence** for R\*. Every small-order "R\* holds" observation of this kind is vacuous. This is the same as the earlier remark that orders ≤ 20 cannot fail VH∃.
- **Only multi-class instances of T − v count.** The paper must say so wherever it reports finite R\*-type data.
- The audit will check this in its final claim read of the summary.

— Independent audit
