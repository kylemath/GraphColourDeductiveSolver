# Job 21: C-candidate wheels not certified [exploratory]

`dcheck/CWheels.lean` (built 14 Oct 2026 22:41, `lake build CWheels` rc=0, 34 theorems, 0 sorry, native_decide) certifies
the computational half for **17** of the 23 C-candidate wheels (66666 is separate, `dcheck/C66666.lean`):
11 5-wheels (55558, 55568, 55577, 55578, 55588, 55658, 56568, 56577, 56578, 56588, 56658) and
6 6-wheels (555577, 555677, 555767, 555777, 556577, 566577), each with X = {I0-I1}.

**Not certified (6):** the 6-wheels `565667`, `565676`, `565677`, `565757`, `565767`, `565777`.
For each, every working contraction found by cfast (listed in `cwheels21.json`, e.g.
X = {I0-I4, I0-I6, R0-I2, R2-I2}, components {I0,I4,I6} and {I2,R0,R2}) has a component containing two ring
vertices (R0, R2). Merging two ring vertices can create a loop if the outside has a chord or path joining them, so
these contractions are not admissible without an extra argument about the outside. They stay out of R in Job 22.
