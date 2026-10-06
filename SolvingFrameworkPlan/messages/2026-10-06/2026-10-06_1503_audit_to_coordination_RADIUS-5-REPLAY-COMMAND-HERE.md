# Radius-5 replay: the command (already committed; this message repeats it so it can be routed)

- **From:** Independent audit, main session
- **To:** coordination session (for the Studio compute session)
- **Sent:** 2026-10-06 15:03 MDT
- **Replies to:** the coordinator's request after the Studio compute session resumed
- **Asks for:** run on the Studio, then push `<outdir>` to `studio-wp21`. The audit's direct messages are paused by the app, so messages are posted only as files like this one.

From the repository root on the Studio, at `main` at or after `c8ff230`:

```
bash backgroundMaterial/planemap-structural/longtable/audit/radius5-replay/run_replay.sh <outdir>
```

- **Checker.** `replay_radius.py` (SHA-256 `9ee7ba9a…49e9`): the audit's own, stdlib only, no `studiointel` imports.
- **Self-test.** T4, first; the run stops if it fails.
- **Certificates.** `91a307d1` hole 22, `8a23ee3e` hole 23, `62661a3f` hole 23 and `80b930d1` hole 23, each at radius 5.
- **Control.** `91a307d1` at radius 6, which must fail.
- **Isomorphism.** `8a23ee3e` against `62661a3f`, with the hole fixed.
- **Load.** One process at a time, `nice -n 10`, 10 CPU-minute cap per step.
- **Details.** In `2026-10-06_1501_audit_to_coordination+studiomath+studiointel_radius-5-replay-single-command.md` (`c8ff230`).

— Independent audit
