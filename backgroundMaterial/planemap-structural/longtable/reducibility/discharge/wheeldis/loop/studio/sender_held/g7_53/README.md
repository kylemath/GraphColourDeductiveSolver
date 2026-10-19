# g7_53: explore's round-53 held set on binder 7 7665566/6765766 (held, not admitted)

Source: branch claude/project-thread-nh6pv2 at **c9cb6184**, loop/k53/{held53_7_7665566_6765766.txt, G_kcc.out,
G_df.out, G_cf.out}, fetched by path, byte-identical (sha1 040d598d92 / 9e9003c525 / 1b9062cb92 / 56d10254e5).

**Independence.** Studio checked this set from the spec header of held53_7_7665566_6765766.txt and the data files
only. deliv53.py and cen53's builder were not read. The engines are Studio's own runs: loop/kc/kc -C -s 60 -t 600,
out/job52/dfast18 (from wheels/studio/dfast18.cpp), studio15/cfast --fixed. The frame check is Studio's g7_check.py
on grow.kcline (degrees from the kc line).

**Verdict (studio_verdicts.txt): 10/10 agree with explore, 0 problems.**
- 4 D: kc D + dfast18 D (rings 8, 8, 9, 15).
- 6 C: kc X + cfast --fixed X with leftover 0 (X = {I0-I2} once, {I0-I1} five times; rings 11-14); ring-merge
  guard pass on all 6 (all X interior-only).
- Frame: each frame has m vertices with degrees equal to the kc line's, its letters equal the name's (v iff u,
  wI / sI / slots in the header's slot order), and every spec-forced adjacency with both ends in the window is
  present (v-wI, wI-w(I+1), sI-wI, sI-w(I+1), pIK-wI, the ring-2 order s(I-1)-pI1-..-sI, t(a/b/..)-a, b, ..).

**Not admitted.** These names carry privates and ring-3 vertices; the wlp3 parser cannot read them. The twoeng prefix
guard (0339586b) holds all 10: a test run with this folder in the glob gave k3x_D / k3x_C byte-identical and 10 g7_
names held (the test's log lines were not kept).
