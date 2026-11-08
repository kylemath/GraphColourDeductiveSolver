# maclane v2b: IPM time cap for the v2 lower lane (k86GV1), and its restart on K3gB5g

**Why.** On 8 Nov k86GV1 (K3gB5d) spent 9.8 h at 99% CPU in one scipy `highs-ipm` solve: hshim run 3, the cold re-solve
after `v2inner it 0.1`, about 496k rows by 90k columns. Runs 1 and 2 (311k and 406k rows) took 216 s and 635 s. There
was no swap. hshim solves every LP from scratch with no time limit, so one stalled IPM or crossover holds the whole lane.

**What changes.** Only `eng_v2/hshim.py` (the v2 lane's scipy stand-in for highspy). eng/ and eng_p1r/ (the upper
lane MS3) are untouched.
- `HSHIM_TMAX_IPM=<s>`: a first-try `highs-ipm` gets `time_limit=<s>`. When it stops on the cap, the shim's existing
  retry runs `highs-ds` (dual simplex) on the same model with no cap. The model, and so the optimum and every cert, is
  unchanged; only which HiGHS solver returns it changes. The hshim run line then ends
  `[highs-ipm: status 1 (HSHIM_TMAX_IPM 2400s cap); highs-ds: status 0]`.
- `HSHIM_DISP=1`: the HiGHS log goes to stdout. It is for diagnosis only and is noisy, so leave it off in runs.
- Unset (the default), the shim behaves exactly as v2a.

**Container tests (scipy 1.18.1, HiGHS 1.12).**
- On an 80k x 20k LP, IPM with a 20 s cap stopped at 34 s with "time limit" (IPX checks the limit between
  iterations; crossover not run).
- A tiny LP with cap 1e-6 returned through the highs-ds retry, Optimal, same objective.
- Uncapped and capped runs gave identical optima.
- A cap shorter than presolve is ignored by HiGHS (IPX treats a negative remaining time as no limit), so use a cap of
  minutes, not seconds.
- On that random LP, dual simplex was slower than IPM (>10 min against 330 s), so the cap is a backstop, not a
  replacement.

**Files.** `hshim.py` md5 0a74a7b9eee502cb50582978c371017f; it replaces v2a `eng_v2/hshim.py` md5 9ba488536f9adaf4c07d36ff2a48eb3d.

**Studio commands.** P = the pack's s86_f2b7 directory (…/maclane-k86/fs/home/claude/…/P_own_lp/s86_f2b7).
```
cd ~/maclane/maclane-k86
md5 -q $P/eng_v2/hshim.py                       # must print 9ba488536f9adaf4c07d36ff2a48eb3d
md5 -q <shared>/v2b/hshim.py                     # must print 0a74a7b9eee502cb50582978c371017f
bash stop_v2.sh                                   # stops k86GV1 (stalled in run 3); its rows file is kept
cp $P/eng_v2/hshim.py $P/eng_v2/hshim_v2a.py
cp <shared>/v2b/hshim.py $P/eng_v2/hshim.py
HSHIM_TMAX_IPM=2400 ARGSV=$P/args_A97_F_W13K3gB5g.txt bash launch_v2d.sh
```
launch_v2d.sh keeps tag k86GV1 and its knobs (V2INNER 4, V2_WARM_PREV 1). With V2_WARM_PREV=1 the realisation rows that GV1
logged (eng_v2/rows_k86GV1.txt) become warm rows. The family only adds kills, and rows K3gB5g does not admit are dropped on
admission. FAMILY.txt records that certs from the next number on are K3gB5g certs. A K3gB5g lower holds for K3l5g, the
upper family; a K3gB5d lower did not. The environment variable reaches the engine through nohup (the launcher does
not clear the environment). Check it with `ps eww <pid> | tr ' ' '\n' | grep HSHIM` on the new solveR2 process.
