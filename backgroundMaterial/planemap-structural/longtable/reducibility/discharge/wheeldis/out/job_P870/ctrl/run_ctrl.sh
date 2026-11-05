#!/bin/zsh
# one P870 control: the 870 rules minus one binding rule; receivers only at the rule's degree (d7_* -> 7, d8_* -> 8)
cd "$(dirname $0)/../../.."   # wheeldis
j=$1; P=out/job_P870; g=$(cut -f1 $P/ctrl/drop$j.txt); d=${g:1:1}
EXPECT_PAT=18159,608,158 $P/run_p870.sh c$j F2B=$P/ctrl/drop$j.json DLIST=$d CALD=7 SEPTAG_SUFFIX=c$j
