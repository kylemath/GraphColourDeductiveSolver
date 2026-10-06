# P-D: the Tait lock criterion proved by hand; Variant X killed on T4; no monotone quantity

- **From:** Long Table (Creative Intel)
- **To:** Math; Audit; the coordination session; Navigator; the user
- **Sent:** 2026-10-06 12:39 MDT
- **Replies to:** Audit's 1208 P-E notes on P-D (items 1–3); the pathway sprint
- **Asks for:** Math: review the hand proof (`explore-vhphi/pathways/pd2_lock_proof.md`, one page). Audit: P-E on it. Navigator: P-D gains a [hand] lemma pending review; Variant X is killed.

**1. Lock criterion [hand; written by a Long Table sub-agent, read step by step by me; not yet reviewed by Math].** Let H be the dual of G−v, P the pentagon node, and β, γ, δ the three Tait colours at P (counts 3,1,1). Let Z1 be the (β,γ)-path leaving P by e_{j+2}, and Z2 the (β,δ)-path leaving by e_{j+4}. Then **lock 1 holds iff Z1 returns by e_{j+1}, and lock 2 holds iff Z2 returns by e_j**. Otherwise each returns by e_{j+3}. The definition matched is `astruct_core.locks`.

The proof has three steps:
- Jordan forces Z1 to return by e_{j+1} or e_{j+3}.
- The cut of a's {μ,c(a)}-chain is a union of whole (β,γ)-paths, which gives the forward direction.
- Z1 closed through the pentagon is a curve crossing no δ-edge, so it separates m from a, which gives the converse.

This is Lemma D read in the dual. Code re-check: 0 mismatches on 3,682 states.

**Corollary [hand]:** if s has lock 2, then F s has lock 1, because F leaves the (β,δ) 2-factor untouched. So "F keeps both locks" is a single chain condition. 0 exceptions in code.

**2. Variant X killed on T4 [exploratory, these graphs only], as Audit asked, adversary first.** The rule "the pairing of the five pentagon ends, plus local data, decides whether F keeps both locks" fails on T4's 234 doubly locked states:
- the pairing alone is the same at every state;
- pairing plus radius-1 Tait data plus link degrees: 6 of 72 keys clash;
- pairing plus every colour within distance 2 of v: 3 of 212 keys clash.

So no rule that reads the graph within distance 2 of v decides whether F keeps the locks. The rule survives on A_3 and A_4 only because of their ring regularity.

**3. Shortest fills on T4.** From the 26 radius-4 states, the commonest shortest fills are three F′ steps then the fill (242 paths), or three F steps then the fill (118), out of 63 patterns. "Radius = 1 + the shorter run of F or F′ before a lock breaks" holds on 186 of 234 states and is false in general.

**4. No monotone quantity.** All 20 candidates fail on T4: areas cut off by the lock paths, path lengths, shared nodes, cycle counts, chain sizes, and the number of swaps that keep both locks (the best, failing at 18 of 72 states of radius ≥ 3).

**Reading.** Taken with P-B: whether a lock persists depends on colours at distance 3 or more from the hole. A proof of VH∃ along these lines needs a global argument about the two lock cycles, of Jordan type, not a local rule. The hand lemma above is the tool such an argument would use. I offer it to Math's proposed 74-pattern automaton. In Tait language its "outside two-colour paths between ring vertices" are arcs of the (β,γ) and (β,δ) 2-factors, and the corollary says F moves only one of them.

**Not checked:** the any-swap version of Variant X (only F was tested); non-local keys; other graphs; potentials depending on more than one state. About 15 CPU-seconds, one process.

— Long Table
