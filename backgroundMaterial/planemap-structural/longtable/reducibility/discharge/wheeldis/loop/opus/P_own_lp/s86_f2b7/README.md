# s86_f2b7 (Opus, 6 Nov 2026): q7m masks on 7-sides (f2b7)

- eng/ = s85_edge56/eng plus two changes, both behind flag `f2b7` (needs q7m + f2b):
  - f2bglue.py: q7m side with c or apex >= 7 gets mask 31 & ~extra7 (was 31).
  - jsepf_gk.cpp / bin/jsepf_gk: the same at the q7m leaf, when env JSEPF_F2B7=1 (set by f2bglue).
  - `f2b7ctl` = negative control (python on, C++ off).
- Spec: /mnt/project-files/swarm/round6/W12-studio-K/from_opus/f2b7/SPEC.md.
- Selftest (`upperR2 ... f2b7 f2bself=3000 q7force` on k85C in03): PASS, max |python - C++| <= 5e-13 at d = 7, 8 and 9 (logs/f2bself7.log). The control fails at d = 7 (0.0147).
- Evidence: s85_edge56/l3t7 and from_opus/s85_k85CL/README.md. The rule file's 7-side kills reproduce all 183 of our own full 2-ball kills
  (f2ball7.py, A97 donly registry minus exname) and add 176. The relief is 14.5% of the d = 7 q7 payee weight in the k85CL dual.
- k86A = k85C + f2b7 (launch_k86A.sh), from k85C in03; points are filed by watch86/file86 to from_opus/s86_k86A/.

## k86B / k86L (13:11Z)

The family is f2b7 + `s85_edge56/keys/cg_keys_r12.txt` (140 keys: cg_keys_124 plus the 16 keys W6 r12 priced as improving on the k85CL dual). gkwintest and gkselftest both PASS on it. `launch_k86B.sh` starts:

- k86B, the in-out upper from k85C in03;
- k86L, a lext lower run, with `watchL86.sh` checking each phase-1 cert by lowerR2 exactbasis (f2b7 on).

k86A (124 keys) and k85CL were stopped.
