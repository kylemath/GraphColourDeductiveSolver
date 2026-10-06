# PR-DISCLOSURE: AI assistance in the PlaneMap pull requests

Math team, 6 October 2026. **Draft for Kyle Mathewson. Nothing here is posted, and no pull request is opened, without his approval of the final wording at that moment.** The user's decision (12:20) is full disclosure.

## 1. Mathlib's current rule, quoted

From "Contributing to mathlib", section "Use of AI" (<https://leanprover-community.github.io/contribute/index.html>, read 6 October 2026):

> "Using an LLM when writing comments on GitHub or Zulip is not allowed: use your own words."

> "As of mid-2026, code written by an AI without the supervision of a Lean subject expert fails to meet that bar by a large margin."

> "Members of the review team will summarily close without comment any low quality PR produced using LLMs, especially if the author has made little effort to directly engage in the community in a discussion about its merits before opening the PR."

> "If you use artificial intelligence (such as, by using GitHub's copilot mode, asking an LLM like ChatGPT or using an agent like Codex, Claude, Gemini, or even Lean-dedicated agents like Aristotle), you must explain this in the PR description."

> "If your PR contains a substantial amount of LLM-generated code, add the `LLM-generated` label by adding the comment `LLM-generated`."

> "It is essential that you understand all the content written by an AI. This includes understanding any design decisions made for the formalization and being able to justify each decision to reviewers without the use of an AI."

The same section also says AI use raises "ethical, ecological, legal and social concerns", and that reviewers worry that "the pedagogical value of the reviewers work is wasted if there is not a human contributor actively learning."

## 2. Where this conflicts with the plan, stated plainly

1. **We cannot write the PR text for Kyle.** Mathlib forbids LLM-written comments on GitHub and Zulip. A pull request description, every reply to a reviewer, and the Zulip RFC are all such text. **Kyle must write them himself, in his own words.** This file is therefore a factual brief for him to draw on, not a paragraph to paste. The commission asked for a disclosure paragraph for the PR description; under Mathlib's rule, the team should not supply that wording.
2. **The understanding requirement is not met today.** The policy requires the person opening the PR to understand all of it and justify every design decision to reviewers without AI. All 13,336 lines of the tracked library, and all 7,479 lines of the Five Colour path, were written by AI sessions. The paper's own disclosure says Kyle has not checked them line by line. **Until Kyle has read and can defend a PR's contents himself, Mathlib's policy says such a PR is likely to have negative value and may be closed without comment.** This does not forbid submitting; it makes Kyle's own review the gate.
3. **Supervision by a Lean expert.** The policy says AI code without supervision by a Lean subject expert falls short "by a large margin". No human Lean expert has reviewed this code. Kyle would need either to act as that expert or to find one.
4. **Engagement first.** The policy weighs discussion on Zulip before the PR. The plan already recommends an RFC before PRs 3 and 6; under this rule it should come before PR 1, written by Kyle.
5. **Label.** Every PR in the series contains substantial LLM-generated code, so each needs the `LLM-generated` label.

**Bottom line.** Mathlib does not ban AI-written code, but it requires a human contributor who understands the code, writes all communication himself, labels the PR, and discusses it first. The series can go ahead only on those terms, and the realistic first step is one small PR (for example `Coloring/Kempe`, 396 lines, or `RotationSystem`, 644 lines) that Kyle has read and can defend.

## 3. Facts Kyle can use in his own description

- **Who wrote it.** The Lean code was written by AI agents (Claude models made by Anthropic, run in Claude Code, plus short-lived sub-agents) under Kyle Mathewson's direction. Commits carry Kyle as git author; the `Co-Authored-By` trailers name the models (Claude Sonnet 5.5 and Claude Opus 5.5).
- **How it was checked.**
  - Lean 4 kernel: every module compiles.
  - Module audit by a separate AI worker: 105 modules rebuilt from source, no `sorry`, `admit`, `native_decide`, `unsafe` or `axiom` declarations. All 1,778 non-internal constants in the 71 audited `Mathlib.*` modules use only `propext`, `Classical.choice` and `Quot.sound`.
  - An independent rebuild and lint replay by a second AI session (Audit) on a second machine is planned before submission.
  - **No human** has checked that the formal statements say what their docstrings say.
- **Responsibility.** Kyle Mathewson is responsible for the PR and will answer review himself, in his own words.
- **Scope of the main theorem.** `PlaneMap.five_color_theorem` is about graphs presented as a plane map (a rotation system built by leaf and edge insertions); it does not prove that an abstractly planar graph admits such a map.

## 4. Decisions for Kyle

1. Whether to submit at all under these terms.
2. If so, which first PR he will read in full himself.
3. Whether he writes the Zulip RFC before PR 1.
4. Whether the module docstrings also mention AI authorship (Mathlib's rule concerns the PR description; docstrings are optional).
