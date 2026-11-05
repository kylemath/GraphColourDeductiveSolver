Studio-side C pattern files as loaded by the swarm's Studio frozen checks (W7 lowerchk.sh / args_k95f.txt; 42 cpat files).
With the Studio D files and RPAT this stack reports "patterns distinct by kind: D 18159, C 627, RPAT 158" (EXPECT_PAT=18159,627,158).
The two C patterns that excuse receiverR2 7/7577575/7555755 are in loop__studio__opus_check__f2b041__tierA__k3x_C_A111.cfast:
  f7_..57575_...55.. (r11, X={I0-I3}) and f7_.575757_..55... (r13, X={I0-I4}); both non-Lean per c_lean_status_pass1.txt.
args_cpat.txt: the cpat= arguments with absolute paths into this folder. MD5SUMS: per-file md5.
Note: the Studio checker applies its own admissibility (R5/R6/RBIG + patmatch); the C count 627 is after its dedupe.
