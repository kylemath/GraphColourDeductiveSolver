# s41c batch 1: engine-copy controls, then attribution probes for the rows no cpat / C 7-wheel covers
O=$(cd $(dirname $0) && pwd); R=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s33z/reg_A74
: bash $O/run41u.sh ctl_base $R ""
bash $O/run41u.sh ctl_noC $O/noC "noC noCw"
: bash $O/run41u.sh a_noC_fulltab $R "noC noCw" /tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/s41c_v_a.txt
bash $O/run41u.sh b_noCcpat_Dtab $O/noC "noC" /tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/s41c_v_b.txt
echo DONE > $O/batch1.done
