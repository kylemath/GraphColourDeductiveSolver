# J4: digest of the transferred first-Mac P1 output, computed on the Studio

- Route: digest of the transferred first-Mac file (origin/transfer-p1 wp20/P1-m5-25.json.gz, gunzipped) computed on the Studio.
- Machine: Kyles-Mac-Studio.local, Apple M4 Max, Python 3.9.6.
- Tool: wp_compare_outputs.py from a detached worktree of origin/main at 46c843e (~/studio-scratch/main-wt), sha256 6d62589fe3b73c0e63d9ed557ec33ba72392015ad05120f42dae68dde87c8a2e (equal to the wp21/PACKAGE-SHA256SUMS entry).
- Input: P1-m5-25.json sha256 e68c44a32e277a59ed73b0c656436b4d6e43d4cb22387159d4f517930fc4793e.
- Commands (nice -n 10, 2026-10-06 14:15:37-14:15:44 MDT):
  - `python3 wp_compare_outputs.py digest P1-m5-25.json > P1-DIGEST.json`
  - `python3 wp_compare_outputs.py compare P1-m5-25.json wp20/replay-P1-m5-25.json` -> `IDENTICAL`, exit 0
- P1-DIGEST.json is equal, as JSON, to wp20/replay/DIGEST.json (the Studio T2 replay): overall_sha256 39f1396ee1988d38e94d4252e45170521259b8d9fc27dbb11ed241bb4e4723d7.
