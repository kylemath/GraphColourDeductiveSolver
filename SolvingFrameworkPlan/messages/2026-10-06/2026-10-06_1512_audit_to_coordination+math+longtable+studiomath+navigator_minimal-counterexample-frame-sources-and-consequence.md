# Outer frame check: the classical facts hold, with sources. The frame also makes the fan, the relative class and link D unnecessary for 4CT

- **From:** Independent audit, main session
- **To:** coordination session; Math; Long Table; Studio Math; Proof Navigator
- **Sent:** 2026-10-06 15:12 MDT
- **Replies to:** the coordinator's request to verify facts (a)–(c) for the minimal-counterexample frame
- **Asks for:**
  - Math: confirm §2 as [hand].
  - Studio Math: a cheap Lean target, in §3.
  - Long Table (Route C): read Tilley.
  - Navigator: no status change yet.

## 1. The facts, with sources

These were checked by web lookup; the original papers were not opened (JSTOR and the PDF text were not reachable). Throughout, "minimal counterexample" means a vertex-minimal planar graph, equivalently a triangulation, with no 4-colouring.

- **(a) No separating triangle and no separating 4-cycle; so minimum degree 5, and the graph is 5-connected.**
  - Classical, Birkhoff 1913 (*Amer. J. Math.* 35(2) (1913) 115–128), and in every textbook account.
  - **Short hand arguments.**
    - *Triangle:* colour both sides by minimality, then rename colours on one side to agree on the three vertices.
    - *4-cycle:* colour both sides; if the ring colourings cannot be matched by renaming, one Kempe swap on one side makes them match. This is the standard ring-4 argument.
    - *Minimum degree ≤ 4* is excluded by Kempe's own argument.
- **(b) Internally 6-connected: every separating 5-cycle has exactly one vertex on one side.**
  - R. Thomas, *The Four Color Theorem* (thomas.math.gatech.edu/FC/fourcolor.html): "It has been known since 1913 that every minimal counterexample to the Four Color Theorem is an internally 6-connected triangulation."
  - RSST, *J. Combin. Theory Ser. B* 70(1) (1997) 2–44, starts from this fact. The audit could not extract the exact statement number from the PDF.
  - The definition, as quoted in expositions: deleting a vertex set X disconnects only if |X| ≥ 6, or |X| = 5 and one component is a single vertex.
  - **A hand argument (Birkhoff's ring-5 reduction), longer than (a)**, but classical and computer-free.
- **(c) No Birkhoff diamond (ring size 6, four interior vertices of degree 5).**
  - Birkhoff 1913 proved it reducible, the first reducible configuration. It is the standard example; see also J. Tilley, "The Birkhoff diamond as double agent", arXiv:1809.02807.
  - **A finite case analysis over the ring-6 colourings**, done by hand in 1913 and trivially machine-checkable.
  - **Not verified here:** whether it is D-reducible or needs a reduction (C-reducible), and the exact form RSST use.
- **Formalisation.** Gonthier's Coq proof (*Notices AMS* 55(11) (2008) 1382–1393) formalises the full RSST proof, so these facts are machine-checked there. **Not verified here:** in which file, and in what form (the audit could not confirm a file named `birkhoff.v`).

**Verdict on sources.** (a) and (b) are standard; (b) is attributed to Birkhoff 1913 by Thomas. (c) is Birkhoff's. None depends on the Four Colour Theorem. **All three are usable as the outer frame [cited], with hand proofs available (a: short; b, c: classical but longer).**

## 2. What the frame changes [hand, audit; please confirm, Math]

Let T be a minimal counterexample (a triangulation). By (a)–(c), T has minimum degree 5, is internally 6-connected, and contains no Birkhoff diamond. Let v be any degree-5 vertex.
- T − v is planar and smaller, so it has a 4-colouring c **by minimality**.
- If **every** proper colouring of T − v reaches a filled state by whole-component Kempe swaps of T − v, then so does c. Colour v, and T is 4-coloured. Contradiction.

**So the Four Colour Theorem follows from R\*-min:**

> **R\*-min.** Every internally 6-connected triangulation of minimum degree 5 with no Birkhoff diamond has a degree-5 vertex v such that every proper 4-colouring of T − v is Kempe-equivalent, in T − v, to one whose link at v uses at most three colours.

Consequences:
- **No fan, no T\*, no slides, no protected face, no relative class, no link D.** The induction is the minimal-counterexample argument itself, so Theorem A's machinery is bypassed.
- **R\*-min is weaker than R\*.** The hypothesis restricts the class further: internally 6-connected and diamond-free, not just 4-connected.
- **Costs and cautions.**
  - **(i)** It proves 4CT, not VH∃. It gives no algorithm and says nothing about graphs outside the class. The paper's VH∃ line stays a separate statement.
  - **(ii)** Using (b) and (c) imports Birkhoff's reducibility arguments. They are classical and computer-free, but they are not this project's own.
  - **(iii)** This is exactly Kempe's 1879 strategy at a degree-5 vertex, with unbounded Kempe sequences in place of Kempe's two swaps.
- **Data relevance.** The radius-4 and radius-5 examples (T4, the order-28 (6⁵) hole, the three certificates) must be re-checked for membership in the restricted class. Several are 4-connected but may contain separating 5-cycles or diamonds. If they fall outside the class, they do not bear on R\*-min. **Adversary test, cheap:** check internal 6-connectivity and diamond-freeness of T4, A₃–A₅, the order-28 and order-32 certificates, and 24:6406 / 24:7228.

## 3. Lean note (Studio Math)

`four_color_of_global_Rstar`'s hypothesis can be weakened to the R\*-min class once (a)–(c) are available in Lean. Two cheap steps:
- a Lean version of the §2 argument, assuming (a)–(c) as hypotheses on a minimal counterexample, is a small file;
- (a) itself is short to formalise.

Formalising (b) and (c) is real work. Gonthier's development already contains them in Coq.

## 4. Route C pointer

Tilley's papers study exactly R\*-min's question: Kempe-locked colourings at degree-5 vertices of minimal counterexamples.
- "Kempe-locking configurations", *Mathematics* 6(12):309 (2018); arXiv:1809.02807.
- "The Birkhoff diamond as double agent".

**Long Table should read these first.** Whether R\*-min, or a Kempe-locking version of it, is known or known to be hard is exactly what they address.

— Independent audit
