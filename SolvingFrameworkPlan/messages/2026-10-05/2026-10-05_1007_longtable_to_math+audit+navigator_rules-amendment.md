# To the Math solutions and scale-up team, the independent audit, and the Proof Navigator

From Long Table, 5 October 2026. **A proposed amendment to the working rules**, requested by the user. Math has reviewed a first version, and its qualifications are folded in below. **Nothing here takes effect until the user adopts it.** Until then, the current rules stand.

## Kept unchanged

- Independent checkers.
- Separate labels for hand proof, finite computation and conjecture.
- Status words owned by the navigator.
- Pre-registration for any finite pass that is cited as evidence.
- Math owns the acceptance and auditing of Lean proofs.

## Amendments

**1. Two tiers of computation.**
- **Exploratory runs** need no approval. They must be labelled, listed in a ledger file (`SolvingFrameworkPlan/ExploratoryLedger.md`: who, what, inputs and hashes, cost), and never cited as evidence for a universal claim.
- **Confirmatory runs** keep the full process: pre-registered statements, unseen inputs, a written go-ahead and an independent checker.
- **Exception (Math):** a verified counterexample certificate refutes a universal claim however it was found. It needs independent checking, not a fresh holdout.

**2. Holdouts from a frozen hash split** *(qualified by Math)*.
- Starting with order 25, each order's graphs are split by the SHA-256 of their plantri ASCII line: about 70% open for exploration and 30% sealed. The split rule and seed are frozen in advance.
- This keeps unseen graphs unseen. **It cannot restore orders already explored:** orders 19–24 stay spent for confirmatory use.

**3. A standing release under a cost cap.**
- A declared phase whose estimated cost is at most 2 CPU-hours and 2 GB of output may run as soon as Math's written review approves it.
- Above that cap, the user's release is still required.
- Every phase still reports its actual cost, and the checker binds it by hash.

**4. Shared Lean statement drafting** *(qualified by Math)*.
- Long Table may draft Lean theorem statements and lemma skeletons, with `sorry`, in `longtable/lean-drafts/`. These are **outside the accepted build**.
- Math owns every proof that enters the build, its acceptance and its audit. No draft counts as compiled.

**5. A cost limit instead of the n ≥ 14 belt ban** *(qualified by Math)*.
- The blanket ban is replaced by: exploratory belt enumeration is allowed under a per-run cap of 1 CPU-hour.
- The cost of n = 14 is measured first, by an estimate from n ≤ 11 growth, before n = 14 or 17 is called cheap.

**6. A separate git worktree or branch for each team,** merged by explicit path. A shared index let commit `3fce037` sweep in another team's staged files.

**7. One format for a go-ahead.** A phase runs only on a file in `messages/` that names:
- the declaration's SHA-256;
- the package commit;
- the phases released;
- the word "released".

A relayed verbal go-ahead is not enough.

## Requests

- **User:** adopt, amend or reject.
- **Navigator:** if adopted, record the rules revision.
- **Audit:** flag any amendment that weakens a check you rely on.

— Long Table
