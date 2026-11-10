#!/bin/bash
# s86 (10 Nov 14:55Z): one-shot inject of the Studio's Mac-lane point sol_k86MK6_in04_tight__K3l5r_k260 (0.013846086 [E2], gk7 52acce6b0)
# into the running k86GS22 (K3gB5r + 365 keys + HATBB on eng_p8h).  K3gB5r is not a file-level superset of K3l5r (K3d/K3f/K3i/K3j
# files are only in K3l5r), so the point is checked here first on GS22's own family + keys + flags (U86); FEASIBLE -> eng_p8h/inject_k86GS22.json.
N=$(cd $(dirname $0) && pwd); S=/mnt/project-files/swarm/round6/W17-studio-kstar/from_studio/sol_k86MK6_in04_tight__K3l5r_k260/in
b=sol_k86MK6_in04_tight__K3l5r_k260; tg=MI_k86MK6_in04_k86GS22
[ "$(md5sum < $S/$b.json | cut -c1-8)" = b32f09f5 ] || { echo "$(date -u +%H:%M:%SZ) [s86MI-k86GS22] $b md5 mismatch, not checked" >> $N/run.log; exit 2; }
cp $S/$b.json $N/cand/$b.json
E86OVR=$N/eng_p8h STACK=s77 ARGS=$N/args_A97_F_W13K3gB5r.txt KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstwb.txt bash $N/U86.sh $tg $N/cand/$b.json 2 $XF > /dev/null 2>&1
v=$(grep "\[s86U-$tg\] STACK" $N/run.log | tail -1 | grep -o "UPPER-R2: [A-Z]*")
if [ "$v" = "UPPER-R2: FEASIBLE" ]; then
  cp $N/cand/$b.json $N/eng_p8h/inject_k86GS22.json.tmp && mv $N/eng_p8h/inject_k86GS22.json.tmp $N/eng_p8h/inject_k86GS22.json
  echo "$(date -u +%H:%M:%SZ) [s86MI-k86GS22] $b (t 0.013846086) FEASIBLE on K3gB5r + 365 + HATBB -> eng_p8h/inject_k86GS22.json" >> $N/run.log
else echo "$(date -u +%H:%M:%SZ) [s86MI-k86GS22] $b (t 0.013846086) '${v:-no verdict}' on K3gB5r + 365 + HATBB; not injected" >> $N/run.log; fi
