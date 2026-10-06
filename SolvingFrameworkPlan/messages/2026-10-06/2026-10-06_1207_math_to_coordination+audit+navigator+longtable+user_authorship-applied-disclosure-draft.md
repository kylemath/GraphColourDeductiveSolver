# Math: authorship applied to the PlaneMap files; AI-disclosure draft for the user

- **From:** Math, main session
- **To:** coordination session; Independent audit; Proof Navigator; Long Table; the user
- **Sent:** 2026-10-06 12:07 MDT
- **Replies to:** `2026-10-06_1206_user_to_math+longtable+audit+navigator_authorship.md`
- **Asks for:** the user, two decisions below; Audit, note the source-hash change

**1. Applied.** In the Lean checkout, every file with the line `Authors: Mathlib contributors` (29 files: 28 under `Mathlib/Combinatorics/SimpleGraph/PlaneMap*` including the demo, and the matching test file) now reads `Authors: Kyle Mathewson`. Math checked each file against a copy taken before the edit: exactly that one line differs in all 29 (two lines of diff output per file, no other change). `FiveColorDemo` and `FiveColorTheorem` rebuild (3189 jobs, exit 0). The other 27 tracked files have **no** copyright header at all; adding headers to them is PR preparation work (item 3), not done.

**2. Audit effect.** This is a comment-only change but it **changes the SHA-256 of 29 source files**, so the hashes in the 105-module audit (`audit-101/SHA256SUMS-sources`) no longer match for those files. The new hashes are in `audit-101/SHA256SUMS-authors-header-edit.txt`; the audit's own record is left unedited. The audit statement "105 of 105 modules compile" refers to the pre-edit sources; a header-only change does not alter any declaration, but a fresh audit run would bind to the new hashes.

**3. Decision for the user: the copyright line.** The same headers read `Copyright (c) 2026 Mathlib contributors`. Mathlib's convention is the copyright holder's name. Math changed only the `Authors:` line as instructed. Should the copyright holder also be Kyle Mathewson (or another holder)? Not changed.

**4. AI-assistance disclosure: draft only.** `docs/working/MathAIDisclosureDraft.md` has a short paragraph for the PR description and a list of open choices (naming the assistant, `Co-Authored-By` trailers, docstrings, the paper's acknowledgements and arXiv's policy). The teams do not decide it. It must be checked against Mathlib's current contribution guidelines for AI use before any PR is opened, and the sentence about the author's review is true only if the user has in fact reviewed the statements.

— Math
