# s86 tighten: lower t on a FEASIBLE upper point with its weights fixed (the repair ladder keeps a feasible blend's own t, so points carry slack).
# usage: [ARGS=<args file, default K3j>] [KEYS=...] bash tighten.sh <cand/sol_X.json> [probe drop, default 0.003]
# 1. probe: upperR2 at t_p = t - drop with every violated receiver listed (vfile); every row family is linear in t with coefficient 1,
#    so the floor = max(t_p + max receiver excess, t_p + cons worst excess, senders' 1 - min value).
# 2. final: upperR2 at ceil(floor, 1e-9) + 1e-9; writes cand/sol_<X>_tight.json and logs/upper_F_<X>_tight.log.  Any tail / pattern-free
#    failure at the probe stops it (not linear-checked here).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; B=$(dirname $N)
SOL=$1; DROP=${2:-0.003}; X=$(basename $SOL .json); X=${X#sol_}
export STACK=s77 ARGS=${ARGS:-$N/args_A97_F_W13K3l.txt} KEYS=${KEYS:-$B/s85_edge56/keys/cg_keys_r13w16.txt}
FAMX="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt"
P=$N/cand/sol_${X}_probe.json
T0=$(python3 -c "
import json,sys; S=json.load(open('$SOL')); t=S['t']; S['t']=t-$DROP; S['note']=S.get('note','')+' | s86 tighten probe at t - $DROP'; json.dump(S,open('$P','w')); print(t)")
bash $N/U86.sh F_${X}_probe $P 1 $FAMX vK=1000000 vfile=$N/logs/viol_F_${X}_probe.txt
L=$N/logs/upper_F_${X}_probe.log
if grep -q "Traceback" $L || ! grep -q "UPPER-R2" $L; then echo "tighten $X: probe failed to run" >&2; exit 3; fi
if grep -qE "exact pattern-free: [1-9]" $L; then echo "tighten $X: tail fails at the probe; not handled" >&2; exit 4; fi
FL=$(python3 - $SOL $L $N/logs/viol_F_${X}_probe.txt <<'PY'
import sys, re, json
t0 = json.load(open(sys.argv[1]))['t']; L = open(sys.argv[2]).read()
tp = float(re.search(r'at t = ([0-9.e-]+)', L).group(1))
sf = float(re.search(r'senders need t >= ([0-9.e+-]+)', L).group(1))
m = re.search(r'links with in - out > t \+ 1e-9: (\d+) \(worst excess ([0-9.e+-]+)\)', L); ce = float(m.group(2)) if m and int(m.group(1)) else None
rx = [float(l.split()[2]) for l in open(sys.argv[3]) if l.strip()]
fl = max([sf] + ([tp + max(rx)] if rx else []) + ([tp + ce] if ce is not None else []))
src = {'senders': sf, 'receivers': tp + max(rx) if rx else None, 'cons': tp + ce if ce is not None else None}
print('%.12f %.12f %s' % (fl, t0, json.dumps(src)))
PY
)
read FLOOR TOLD SRC <<< "$FL"
if [ -z "$FLOOR" ]; then echo "tighten $X: could not read the floor" >&2; exit 5; fi
TT=$(python3 -c "import math; f=$FLOOR; print('%.9f' % (math.ceil(f*1e9)/1e9 + 1e-9))")
if python3 -c "import sys; sys.exit(0 if $TT < $TOLD else 1)"; then :; else echo "tighten $X: floor $FLOOR not below t $TOLD" >&2; exit 6; fi
O=$N/cand/sol_${X}_tight.json
python3 -c "
import json; S=json.load(open('$SOL')); S['t']=$TT; S['note']=S.get('note','')+' | s86 tighten: same weights, t = $TT (floor $FLOOR)'; json.dump(S,open('$O','w'))"
bash $N/U86.sh F_${X}_tight $O 1 $FAMX vK=1000000 vfile=$N/logs/viol_F_${X}_tight.txt
echo "$(date -u +%H:%M:%SZ) [s86T] tighten $X ($(basename $ARGS)): t $TOLD -> $TT (floor $FLOOR; sources $SRC): $(grep 'UPPER-R2' $N/logs/upper_F_${X}_tight.log | tail -1)" >> $N/run.log
rm -f $P
