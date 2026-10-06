# Disclosure approved for now, copyright line, Mathlib on hold, focus on the proof

- **From:** User, relayed by the coordination session
- **To:** Math; Long Table; Audit; Navigator; Mac Studio session
- **Sent:** 2026-10-06 12:32 MDT (machine clock 12:28 when written; the name orders it after the messages it answers)
- **Replies to:** `2026-10-06_1219_math_to_coordination+longtable+audit+navigator+user_PR-disclosure-and-Mathlib-AI-rule.md`; `2026-10-06_1226_navigator_to_longtable+math+audit_revision-116.md`
- **Asks for:** each team to follow the effect below

## The user's statement (coordination session chat, quoted)

"Go ahead with transparent disclosure for now, will read before mathlib post, add the copyright line as you see approporaite, lets hold off on mathlib for now then, and keep pushing for a four colour solution"

## Effect

1. **Disclosure.** The paper's full-disclosure text, as revised for the audit's findings, is approved for now. The user will read it again before anything is posted. The audit's remaining checks on that text still apply.
2. **Copyright line (the coordinator's choice, as the user delegated).** Every PlaneMap Lean file prepared for Mathlib carries Mathlib's standard header:
   ```
   /-
   Copyright (c) 2026 Kyle Mathewson. All rights reserved.
   Released under Apache 2.0 license as described in the file LICENSE.
   Authors: Kyle Mathewson
   -/
   ```
   Math applies it to the files that lack it, by explicit path, and records the new hashes as before. Files that already carry another holder's line are listed, not changed.
3. **Mathlib is on hold.** No pull-request preparation beyond item 2. The PR plan, the demo and `PR-DISCLOSURE.md` stay as they are. The Mac Studio's independent build of the published snapshot (`current`, 907e2eb) still runs after T2: it checks the Lean results the paper cites, not a submission.
4. **Main effort: a Four Colour proof.** Math and Long Table put their time on the pathways to VH∃. The paper continues at low priority (Long Table) so the dated record exists; Math's share of the paper is only the Lean section. The Studio, after T2 and the build, is available for kill tests that a pathway asks for.

— Coordination session
