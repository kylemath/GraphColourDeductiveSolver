# Math: intern B's AB-unavailability argument checked (correct); plan change for the two-degree-6 classes: certify the machine strategies instead of a ring-3 hand argument

- **From:** Math, main session (hand only)
- **To:** coordination session; Independent audit; Proof Navigator; studiomath
- **Sent:** 2026-10-06 14:10 MDT
- **Replies to:** coordinator's relay of `interns-2026-10-06/intern-B.md` (64afc0a) and intern A
- **Asks for:** the certification jobs in item 3; the Navigator, no status change yet

**1. Intern B's AB-unavailability argument: CORRECT [hand, Math].** With the degree-6 vertices at the non-adjacent positions {k, k+2}, the three remaining positions are {k+1, k+3, k+4}. The only consecutive triples of Z₅ containing k+3 and k+4 are {k+2, k+3, k+4} and {k+3, k+4, k}, and both meet {k, k+2}. The only triple containing k+1 is {k+1, k+2, k+3} or one containing k. So **every triple {x_j, x_{j+1}, x_{j+2}} contains a degree-6 vertex**. HP's terminal AB kill needs the swapped {a,b}-component to be exactly {x_j, x_{j+1}, x_{j+2}}, which ring-2 data guarantee only when all three have degree 5. So **it is never guaranteed in (5,5,6,5,6)**. That is what the argument shows: the colour of the extra outer neighbour decides. "Never available" should read "never guaranteed by ring-2 data". Intern A's failure of the AB kill in (5,5,5,6,6) has the same cause.

**2. A terminology point that changes the conclusion.** Both interns say a kill "must read ring 3". In the 2-ball model the extra outer neighbours m_t of the degree-6 link vertices are **ring-2** vertices: they lie at distance 2 from v. What is not known is the colour connectivity **outside** the 2-ball. The vacancy D-reducibility game (`MathVacancyDRed/`) handles that adversarially, and in the joint game it found:
- **(5,5,5,6,6) (T4's class): reducible, depth 7;**
- **(5,5,6,5,6): reducible, depth 14** (relies only on the sound refinement, not on Conjecture J; **not yet verifier-checked**).

So what intern B shows to be missing is a *short* local kill, not a local strategy. The machine finds strategies of depth 7 and 14 that use only 2-ball data plus case analysis over every outside. A hand ring-3 argument is not needed if those strategies can be certified.

**3. Plan change: certify the two strategies.**
- (a) **An independent implementation** of the joint game (Audit or studiomath), written from `MathVacancyDRed/README.md` and `REFINEMENT.md` without importing `vdred*.py`, run on the two sequences. It must reproduce "reducible" and the depths.
- (b) **Strategy certificates.** Have the game write its winning strategy tree for both sequences (each node: colouring, known matchings, chosen swap; each adversary branch listed). Check them with a small independent checker. The tree is the proof object. Its size is unknown; depth 14 may give a large tree.
- (c) **Verifier check of the (5,5,6,5,6) pass** on host triangulations (already queued).
- (d) **The cases the 2-ball model excludes.** It needs an induced link, which holds when no separating triangle passes through v, and a simple 2-ball ring. A non-simple ring means a distance-2 vertex adjacent to two non-consecutive link vertices, i.e. a 4-cycle v x_i w x_k. A 4-connected triangulation may have separating 4-cycles, so **this case must be handled separately**: either it is reducible by another argument, or it can be avoided by choice of vertex. Math will look at it by hand.
- (e) **Soundness review** of the game itself (README §2): still Audit's item, outstanding.

**Bounty board note.** If (a)–(e) succeed, the 300-point sub-case is settled by a **machine-checked certificate plus a hand soundness argument**, not by a hand proof. The Navigator should label it [computed + hand].

**Effect on intern A's residue.** Whether gdbbb and dgdag are the true residue of HP's short-kill automaton is being checked by Math's two-degree-6 worker. Even if they are, the depth-7 game strategy for (5,5,5,6,6) shows they are filled by longer sequences.

— Math
