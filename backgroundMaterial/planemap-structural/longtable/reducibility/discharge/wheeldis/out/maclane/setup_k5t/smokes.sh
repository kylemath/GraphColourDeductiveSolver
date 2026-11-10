#!/bin/bash
S=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/maclane/setup_k5t
bash $S/smoke_harness.sh > $S/smoke_harness.log 2>&1
cd $HOME/maclane/maclane-k86 && nice -n 15 bash smoke_fam.sh t > $S/smoke_fam_t.out 2>&1 < /dev/null; echo "smoke_fam exit $?" >> $S/smoke_harness.log
