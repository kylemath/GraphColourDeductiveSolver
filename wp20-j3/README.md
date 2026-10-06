# WP20 P1 replay J3 (audit, route A): run record

Committed by Studio intel at the coordinator's request, as a handover for the audit after the Studio compute session stopped. **Not interpreted by Studio intel:** the audit writes the verdict. The files are copied byte for byte from `~/studio-scratch/p1audit/` on the Mac Studio.

- **Route:** A (audit message `2026-10-06_1340`). Script: `run_j3.sh`, launched detached under `caffeinate -ims` (`j3p1audit.pid`).
- **Worktree:** `~/studio-scratch/main-wt`, at commit `46c843e` (checked by `git log -1` in that worktree at handover).
- **Inputs:** sha256 lines as recorded at setup in `shasums.txt`:
  - P1 merged output `P1-m5-25.json`: `e68c44a32e277a59ed73b0c656436b4d6e43d4cb22387159d4f517930fc4793e` (agrees with `TRANSFER-README.txt`);
  - `longtable/wp20/input-m5-25.txt`: `92e482edefb9ff4c5fbb77b2121366b2c3a88cf8001fecafa1ae29025e60d989`;
  - code: `audit/wp20-replay/wp20_audit.py` `d0fc8759…63cc`, `audit/wp20-replay/compare_p1.py` `511cf77e…1c1e`, `WP20-D1-declaration.md` `8758a9f8…2fef`, `d1_confirm.py` `bb350d3b…d0b5`, `d1_check.py` `98c6bcf7…ab12` (full lines in `shasums.txt`).
- **Times** (`out/times.txt`): start 2026-10-06 14:14:44 MDT, end 14:53:25 MDT, exit 0.
- **Outputs:** `out/compare-result.json` and `out/run.log`, unmodified. The 117 MB `P1-m5-25.json` is not committed; its hash is above.
