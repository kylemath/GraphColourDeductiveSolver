# Team onboarding: start here after a restart

Last updated 5 October 2026 by Long Table. Read this page first, then the latest messages. Every claim below points to its source. If this page disagrees with a newer message, the message wins: update this page.

## 1. The goal

We want a **structural, executable proof of the Four Colour Theorem**: a rule-based argument without the large configuration census of the classical proofs. After that come a proof of termination and a polynomial algorithm, each justified separately. Finite computations are adversarial tests, not proofs. Lean compilation is the bar for "compiled".

The current proof route is the **vacancy induction** (`longtable/swarm/hole-induction.md`, `longtable/swarm/vh-exists.md`):
1. Delete a degree-5 vertex v.
2. Add a legal fan of two chords to get the smaller triangulation T\*.
3. Colour T\* by induction and restrict the colouring to T − v.
4. Fill the hole using singleton slides and Kempe swaps. This last step is the open hypothesis, **VH∃**: some vertex and fan work for every start.

Math has accepted VH∃ ⇒ 4-colourability as a hand argument. VH∃ itself is **open**.

## 2. Who is who

| Team | Also called | Owns | Does not own |
|---|---|---|---|
| **Long Table** | Creative Intel; "longtable" in filenames | Hand proof pages and structural ideas; adversary tooling; declarations and producers for experiments (WP-numbers); its own errata; Lean **drafts** with `sorry`, outside the build (if the rules amendment is adopted) | Lean proofs in the accepted build; acceptance; status words |
| **Math** | Math solutions and scale-up team; "math superintel" | Acceptance or refusal of results; proof review; Lean formalisation and the module audit (83 custom modules); written go-aheads for experiment phases; executing released phases; corpus sweeps | Long Table's source pages (it reports corrections instead of editing them) |
| **Proof Navigator** | Navigator; ledger; the swarm web frontend | The status ledger and the web app `docs/navigator/` (`planning.json`, revision numbers, journal); status words (proved / compiled / exploring / killed) | Running experiments; editing proof pages |
| **Independent audit** | The audit chat; Teams A and B | Independent replays and checkers that import no team code; adversarial review; `longtable/audit/` | Producers; the source pages of other teams |
| **Night swarm** | "Gremlins" | Overnight exploratory agents run by the user. Fast, less careful. Wrote `SolvingFrameworkPlan/NightHandoff.md` and `longtable/swarm/*` notes. | Their outputs are **leads, not evidence**. Re-check before citing. Their runs on orders 20–26 are disclosed in `longtable/night-swarm-outputs.sha256`. |

The user is the final authority, and releases computations.

## 3. Where things live

| What | Path |
|---|---|
| Messages between teams | `SolvingFrameworkPlan/messages/` |
| Plans and reports | `SolvingFrameworkPlan/*.md` |
| Long Table's code, proofs and data | `backgroundMaterial/planemap-structural/longtable/`, with its own `SHA256SUMS` |
| Swarm and proof notes | `longtable/swarm/` (e.g. `belt-joined.md`, `vh-exists.md`, `hole-induction.md`, `fan-link.md`) |
| WP18 (fan-selection length m(T)) | `longtable/WP18-*`, `longtable/wp18/` |
| WP19 (pre-registered conjectures) | `longtable/WP19-*`, `longtable/wp19/` |
| Audit checkers and reviews | `longtable/audit/` |
| Lean | `lean4/FourColor`, `lean4/KempeReconfiguration`; Math's overlays in `backgroundMaterial/planemap-structural/short-fill-lean/` and `belt-lean-preparation/` |
| Long Table Lean drafts (outside the build) | `longtable/lean-drafts/` |
| Navigator web app | `docs/navigator/` |
| Plays and stories (fiction about the project) | `docs/play/`, `docs/story/` |

## 4. Communication protocol

- **One message is one new file** in `SolvingFrameworkPlan/messages/`. Never edit another team's message; reply in a new file.
- **Filename:** `YYYY-MM-DD-<from>-to-<to>[-and-<to>]-<subject>.md`. The team tokens are `longtable`, `math`, `navigator` and `audit`.
- **Headings** name the recipients, e.g. "To the Math solutions and scale-up team" or "To the Proof Navigator".
- **Silence is not acceptance.** A relayed verbal go-ahead is not a go-ahead.
- **Corrections** to another team's page go in a message. The owner edits the page.
- **Commits:** commit only your own files, by explicit path. Run `git diff --cached --name-only` first: other chats may have staged files in the shared index. Use the attribution line the harness requires.

## 5. Conventions

**Claim labels.** Every claim carries one of these labels:
- **[hand]**: a complete argument is written out.
- **[compiled]**: Lean, with no `sorry`, the standard axioms only, and in the audit.
- **[computed]**: finite, with its inputs named.
- **[cited]**: an external theorem.
- **[post hoc]**: a pattern seen after looking at the data.
- **[open]**.

Never write "proved" for computation. Never generalise a finite pass.

**Status words** (proved, compiled, exploring, killed) are the **navigator's** to record. Other teams report facts.

**Experiments follow the WP-number process:**
1. **Declare and commit** the statements, kill certificates, inputs and hashes, caps, resource limits and phases. Commit the producer, an independent checker (one that imports no producer code) and regressions **before** any run.
2. **Get a written go-ahead** in `messages/` that names the declaration's SHA-256, the package commit and the phases. Then get the user's release.
3. **Run and verify.** Each phase is one pass, with no tuning between phases. Successful paths prove upper bounds only. Exact distances need complete enumeration of the earlier layers. Interrupted or capped results are inconclusive, never passes.
4. **Report** per statement: killed (with its certificate), passed *on these graphs*, or unresolved. The output is bound to its code by hash.

**Holdouts.** Orders 19–24 are spent for confirmatory use. A frozen hash split from order 25 onward is proposed.

**Counterexample certificates** refute a universal claim however they were found. They need independent checking, not a holdout.

**Other conventions.**
- Graphs come from plantri 5.8 with `-m5 -a n`. Graph indices are 0-based in plantri output order. A graph is named `order:index`, e.g. 17:1.
- States: hole = 4, and colours are canonical by first occurrence.
- Moves: whole-component Kempe swaps (singletons allowed) and singleton slides. A state is filled when the hole's link uses at most 3 colours.

**Pending rules amendment** (`messages/2026-10-05-longtable-to-math-audit-and-navigator-rules-amendment.md`, awaiting the user):
- exploratory and confirmatory tiers;
- a standing release under a 2 CPU-hour cap;
- shared Lean statement drafting;
- a cost limit replacing the n ≥ 14 belt ban;
- separate worktrees for each team;
- a single format for go-aheads.

**Until it is adopted, the current rules apply.**

## 6. Where things stand (5 October 2026)

**Compiled (Lean):**
- The pre-existing foundation: Five Colour, spherical degree-4 extension, the 11-vertex result, the icosahedron, six exterior degree-5 roots, and the conditional ranked-contact theorems.
- **Short-fill theorem (M3):** on any simple graph, a mixed fill of length ≤ 2 gives a pure-Kempe fill of length ≤ the same length. `SimpleGraph.VacancyShortFill`, theorems `short_fill` and `optimal_short`; see `ShortFillLeanReport.md`.
- Belt helpers: the 14 opening words, and the potential/budget lemma.

**Accepted hand proofs:**
- **Belt theorem** (`longtable/swarm/belt-joined.md`): the vacancy hypothesis holds at every hole of Florek's two-pole graphs Gₙ, for every n ≥ 5. Unequal poles fill by slides alone within 2n moves. The no-singleton pole-hole case **cites Florek's Theorem 3.1**, and the identification with Florek's graph family is also cited.
- **VH∃ ⇒ 4-colourability**, with the containment and apex-singleton lemmas (`vh-exists.md`).
- **Diagonal reduction:** with all five fans legal, a vertex is bad exactly when its far diagonals cross (`wp18/analysis-17-1.md`).
- **Lemma A** and the one-way Lemma E (`wp18/mechanism.md`).
- **An infinite family with m = 3** (`TriangleSumM3Family.md`, order 14k+3).
- **Lemma L3** is submitted and awaiting review (`wp19/counterexample-analysis.md`).

**Finite results, accepted on their stated inputs:**
- WP11 discovery and validation.
- **WP18:** orders 12–22. m = 3 only on 17:1, m ≤ 2 elsewhere, every start fills within ≤ 4 moves.
- **WP19:**
  - Orders 23–24: m = 3 only on 24:6406. Maximum ℓ is 4. κ − ℓ = 2 on 4 starts, all at order 24.
  - Orders 21–24: U∃ holds on every graph.

**Killed:**
- Every fixed Kempe-swap budget at a frozen hole.
- Fitted ranks: q, lin and others.
- m ≤ 2 (17:1; C1 by 24:6406).
- C3: m ≥ 3 only with degrees 5 and 6.
- M2: κ ≤ ℓ + 1 (24:7228).
- The cascade claim "fails exactly in configuration X".

**Open:**
- VH∃ itself, and U∃.
- Whether m(T) is bounded (no graph with m ≥ 4 is known; C2, m ≤ 3, passed every tested graph).
- M1 (ℓ ≤ 4) as a universal statement.
- A Florek-free proof of the belt's pole case.
- Lean for the belt walk.

## 7. Active work

| Owner | Task |
|---|---|
| Math | **Task B:** compile the unequal-pole belt walk in Lean (Φ induction, caps, the n = 5 case). It is slow at the graph transitions and the termination proof. |
| Long Table | Lean skeleton drafts for Task B (`longtable/lean-drafts/`); a Florek-free proof of the pole case (`swarm/pole-hole-noflorek.md`); short-fill theory beyond length 2 (`wp19/beyond-short-fill.md`); structure of 24:6406 and 24:7228 |
| Audit | Adversarial review of U∃, the diagonal reduction and the mechanism lemmas; independent replay of any new phase |
| Navigator | Record the actual decisions. No upgrade from finite checks. |
| Stopped | WP12, new rank fitting, and any new census without a declaration |

## 8. Restart checklist

1. Read this page, then `ls -t SolvingFrameworkPlan/messages | head -20`, and read every message addressed to your team that is newer than this page.
2. Read your team's plan: Long Table uses `LongTableWorkPlan.md`, `LongTableNextAttack.md` and `CreativeIntelCoordinationPlan.md`. Math and the audit have their own reports.
3. Check `git status` and `git log --oneline -15`. Do not commit files you did not write.
4. Verify hashes before relying on outputs: `shasum -a 256 -c SHA256SUMS` in `longtable/`.
5. Before running anything: is there a declaration, a written go-ahead naming its commit, and a user release (or, if adopted, the cost-capped standing release)?
6. Update §6 and §7 of this page when you change the state of things.
