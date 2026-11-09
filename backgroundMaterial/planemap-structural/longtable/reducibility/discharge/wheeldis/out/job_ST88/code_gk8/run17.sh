# W17 Studio-path upper check (one Python process).  usage: SOL=sol.json TAG=name KILLDIR=dir [KS=1] [EGK=keys] [DLIST=7,8|none] [QDUMP_ONLY=1 SEPQDUMP=dir] bash run17.sh
# code_gk8 (9 Nov 2026): defaults point at code_gk8 and bin/sep3r_gk8 (payer-8/9 GK keys, PAYER8SPEC W5).
# = W15's run15.sh (stack: rules 45a4c6d1 (k95f), Studio Tier A l3q V7/V8 tables, args ARGSF (default W15's args_k95f, D 18159, C 627, RPAT 158)
# + rpatN3, HAT5=1 V6=0 FB=0 XO=0; families HATRR ZH ZR ZCAP=3 Q7 Q7M Q7CAP=3 unless FAMILIES=off) with st21_w17.py and bin/sep3r_w17.
# code_c6 (W17 round 2): C6LE=1 (cons2 as 'the 6 ends <= t'), C6_ONLY=1 (stop after the cons2 step) also come from the caller's env.
# K* / EDGE come from the caller's env (KS=1, EGK=<keys file>, KSA10, KSAMT, W17PLANT, W17PLANT_SEP, W17ST, W17GRAM, KSDUMP).
R=/home/user/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; S=$R/out/job31/f2bA
T=/mnt/project-files/swarm/round6/W1-minimal-set/k95f
# W17 round 6 (macpack): outside the swarm container the Studio repo and /mnt are absent; use the bundle's copies
[ -f $S/studio_l3qtab_+1.json ] || { R=/tmp/swarm-W17/wd; S=$R/out/job31/f2bA; }
[ -f $T/tab/rules_studio_keep95p131f.json ] || T=/tmp/swarm-W17/ext/k95f
# W17 round 6 (22:28Z): the default rule file is the proof stack's rules_zcons_minus_W18rejects (2b362955, 6,016 rules) = Studio
# rules_zcons (DERIVE Z-consistency fix, e6c496a1, 6,290) minus W18's 274 strict-audit rejects; a subset of zcons, f7s 704c371f and
# 45a4c6d1 in every group. Used for F2B7=1 and F2B7=0 alike; F2BRULES=<file> names another (zcons / f7s / 45a4c6d1: comparison only).
F2BRULES=${F2BRULES:-/tmp/swarm-W17/tab/rules_zcons_minus_W18rejects.json}
[ -f "$F2BRULES" ] || { echo "VERDICT: FAIL (rule file $F2BRULES missing)"; exit 2; }
# W17 round 6 (7 Nov, Opus OP-16 growpy audit + lead 02:15Z): rpatN is OFF by default (no rpatN pattern loaded: rpatN3 e153fc41 has 46
# face-set-only patterns, the Studio's rotation rerun drops 15 more). RPATN=<file> loads one, e.g. tab/rpatN3_rotation_justified.txt
# (8b90a842, 2,241 = e153fc41 minus the 46); RPATN=off|none or a header-only file (no pattern line) = off. The old Studio copy
# out/job31/s39o_rpatN3_studio.txt (= e153fc41 as a set) is not sound.
RPATN=${RPATN:-off}
case $RPATN in off|none) RPATN=;; esac
if [ -n "$RPATN" ]; then
  _RF=$RPATN; [ -f "$_RF" ] || _RF=/tmp/swarm-W17/wd/$RPATN
  [ -f "$_RF" ] || { echo "VERDICT: FAIL (rpatN file $RPATN missing)"; exit 2; }
  grep -v '^#' "$_RF" | grep -q '[^[:space:]]' || { echo "rpatN: $RPATN has no pattern line: rpatN off"; RPATN=; }
fi
[ -n "$RPATN" ] && echo "rpatN: $RPATN (md5 $(md5sum < $_RF | cut -c1-8))" || echo "rpatN: off (no rpatN pattern loaded)"
: ${SOL:?SOL=} ${TAG:?TAG=} ${KILLDIR:?KILLDIR=}
if [ "${FAMILIES:-on}" = on ]; then FAM="HATRR=1 ZH=1 ZR=1 ZCAP=3 Q7=1 Q7M=1 Q7CAP=3"; else FAM="HATRR=0"; fi
cd /tmp/swarm-W17/wd && env $FAM SEPTAG=$TAG SEPBIN=${SEPBIN:-sep3r_gk8} F2B=$F2BRULES L3Q=1 L3TAB=$S/studio_l3qtab_+1.json,$S/studio_l3qtab_-1.json \
  L3Q8=1 L3TAB8=$S/V8/studio_l3qtabV8_+1.json,$S/V8/studio_l3qtabV8_-1.json KILLDIR=$KILLDIR RPATN=$RPATN \
  HAT5=1 V6=0 FB=0 XO=0 SKIP_LOWER=1 EXPECT_T=${EXPECT_T:-0.041565} EXPECT_PAT=${EXPECT_PAT:-18159,627,158} WLP3X_DEF=1 WLP_SEPF=1 DMAXP=${DMAXP:-17} \
  W10_HERE=/tmp/swarm-W17/wd W10_ST16=/tmp/swarm-W17/st16 \
  nice -n 15 python3 ${W17CODE:-/tmp/swarm-W17/code_gk8}/st21_w17.py $SOL $SOL ${ARGSF:-/tmp/swarm-W17/args_k95f.txt}
