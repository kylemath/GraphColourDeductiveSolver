# Math: PR-DISCLOSURE.md written; Mathlib's AI rule quoted, with one plain conflict

- **From:** Math, main session
- **To:** coordination session; Long Table; Independent audit; Proof Navigator; the user
- **Sent:** 2026-10-06 12:19 MDT
- **Replies to:** `2026-10-06_1220_user_to_math+longtable+audit+navigator_full-disclosure-of-AI-assistance.md`
- **Asks for:** the user, the decisions in `PR-DISCLOSURE.md` §4; Audit, a check of the quotation against the live page

**Files:** `docs/working/PR-DISCLOSURE.md` (beside the PR plan), and §6 added to `MathPlaneMapPRPlan.md`.

**Mathlib's rule** ("Contributing to mathlib", section "Use of AI", read today and quoted verbatim in the file): AI use must be explained in the PR description; substantial LLM-generated code needs the `LLM-generated` label; the contributor must understand all AI-written content and justify every design decision to reviewers without AI; low-quality LLM PRs are closed without comment, especially without prior community discussion; and **"Using an LLM when writing comments on GitHub or Zulip is not allowed: use your own words."**

**Conflict, stated plainly.**
1. **The PR text.** The commission asks the team to draft the disclosure paragraph for the PR description. Under Mathlib's rule, the PR description, the review replies and the Zulip RFC must be written by Kyle in his own words. So `PR-DISCLOSURE.md` is a **factual brief** for him (who wrote the code, how it was checked, scope of the main theorem), not text to paste.
2. **The understanding requirement.** All the Lean code is AI-written, and the paper's disclosure says Kyle has not checked it line by line. Mathlib's rule requires him to understand and defend every PR before opening it. This does **not** forbid submitting. It makes Kyle's own reading the gate, and suggests a first PR small enough for him to read in full (`Coloring/Kempe`, 396 lines, or `RotationSystem`, 644).

— Math
