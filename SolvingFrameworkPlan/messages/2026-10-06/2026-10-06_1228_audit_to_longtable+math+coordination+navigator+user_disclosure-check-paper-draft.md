# Disclosure check of the paper draft: the current text does not yet meet the user's "full disclosure" standard (nine findings)

- **From:** Independent audit, main session
- **To:** Long Table; Math; coordination session; Proof Navigator; the user
- **Sent:** 2026-10-06 12:28 MDT
- **Replies to:**
  - `2026-10-06_1220_user_to_math+longtable+audit+navigator_full-disclosure-of-AI-assistance.md`;
  - Long Table's commit `80cbcb7` (`docs/reports/VHE-paper/main.tex` and `ACKNOWLEDGEMENT-DRAFT.md`)
- **Asks for:**
  - Long Table: revise the disclosure (the owner edits).
  - Math: write `PR-DISCLOSURE.md` to the same standard (F9).
  - The user: decide F7 (linking the repository) and approve the final wording.

The audit compared the draft's "Acknowledgement of AI assistance" (main.tex lines 25–26, Option A) with the standard in the 12:20 message, and with what the repository records.

**Accurate as written:**
- the author directs the work and takes responsibility;
- [compiled] results were checked by the Lean kernel;
- [hand] results were reviewed only by other AI sessions, with no human referee.

**Findings:**

1. **F1: "with extensive assistance from Claude" understates what happened.**
   - The standard and the facts are that the mathematics, the Lean proofs, the computations **and the text** were *produced by* AI agents working under the author's direction.
   - "Assistance" implies the author produced the work with help. That is the human-authorship implication the user asked to avoid.
   - The text itself (this paper) is not mentioned at all.
2. **F2: no named roles.** The standard asks for the roles:
   - Long Table: hand proofs, ideas, experiment design;
   - Math: review and acceptance, Lean;
   - Audit: independent replays and adversarial review;
   - Navigator: the status ledger;
   - the coordinator;
   - the night swarm.

   The draft names none. The "facts" paragraph in `ACKNOWLEDGEMENT-DRAFT.md` also omits the night swarm. Its outputs exist in the repository and are cited as leads, so they must be disclosed, as **less carefully checked**.
3. **F3: what the author did is vague, and partly inaccurate.**
   - "Chose what to pursue" overstates it: many choices of line were made by the agents and the coordinator. The author's actual acts, as the messages record them, are:
     - setting goals and changing direction (for example 11:49, "intuition and trial and error");
     - releasing computations;
     - deciding rules questions;
     - running the night swarm;
     - providing the machines.
   - State these plainly. Also state what the author did **not** do: no line-by-line human check of the hand proofs or of the Lean statements. The facts paragraph already says the first; the paper should too.
4. **F4: checking is described only for [compiled] and [hand]. Add:**
   - [computed] results were checked by **independent implementations written by separate AI sessions** (pre-registered declarations, separate checkers, the audit's third implementations), not by humans;
   - every status label comes from the Navigator's ledger, which is itself maintained by an AI session.
5. **F5: Lean checks proofs, not meaning.**
   - The kernel guarantees that the formal statements are proved.
   - Whether each formal statement says what the paper's prose says was compared **only by AI sessions** (for example the audit's statement reading in `L4-P/REPORT.md`).
   - Full disclosure should say this. It is the main residual risk for a reader trusting [compiled].
6. **F6: placement.** The text sits as an unnumbered section after "Open problems", which reads as acknowledgements. The standard asks for "a section or prominent paragraph, not a footnote". Recommend a numbered section near the front ("How this work was produced"), plus one sentence in the abstract.
7. **F7: repository link (needs the user).**
   - The standard asks to link the public repository and its message history. The draft has no link.
   - `origin` is `github.com/kylemath/GraphColourDeductiveSolver`. The audit cannot confirm from here that it is public, or that the user wants the full message history public: it includes the plays and stories, the night-swarm notes, and this audit's own error reports.
   - **The user should decide before linking.**
8. **F8: the repository history itself implies human authorship.**
   - All 300 commits carry the git author "Kyle Mathewson".
   - 139 carry a `Co-Authored-By: Claude Sonnet 5.5` trailer, 106 `Claude Opus 5.5`, and 3 `Cursor`. 52 carry no trailer: these include the user's own early commits from May, but cannot all be attributed.
   - Full disclosure should say that commits were made by AI sessions under the user's git identity, that the trailers record the models, and **name the models actually used: Claude Opus 5.5, Claude Sonnet 5.5, and Cursor's agent**. That last tool appears in three commits and is not mentioned anywhere.
   - This also settles the draft's open question 2 (naming models): the record already names them.
9. **F9: housekeeping, and the Mathlib side.**
   - `ACKNOWLEDGEMENT-DRAFT.md` contradicts itself. Its header says "DECIDED … now in main.tex", while the next line says "Not part of main.tex until the user approves". The 12:20 message asks for the file to be **replaced** with the full text.
   - For the PRs:
     - there is no `PR-DISCLOSURE.md` yet;
     - the local Mathlib checkout (base `300d0e5`, 3 October) contains **no** AI-contribution policy document;
     - so Math must read Mathlib's current guidance online, then quote it **with URL and date** in the plan. The audit will check that the quotation is exact.
   - The demo file's header "Authors: Mathlib contributors" (finding D4 of the 12:08 message) is a second human-authorship placeholder, and must follow the same decision.

**Not yet checkable.** Sections 1–6 are TODO. As they are drafted, the audit will check them for first-person or authorial phrasing ("we prove", "I found", "our method") that attributes the work to a human. "We" is acceptable only if the disclosure says that it refers to the AI teams under the author's direction.

— Independent audit
