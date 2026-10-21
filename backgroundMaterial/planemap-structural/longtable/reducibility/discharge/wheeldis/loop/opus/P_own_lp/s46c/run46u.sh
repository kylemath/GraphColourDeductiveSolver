# s46c generic upper on sol_q42aA78 with the s46c engine copy (s39o/eng + exname + ckeep=).  usage: bash run46u.sh TAG TABLEDIR "EXTRA FLAGS" [VFILE]
# TABLEDIR: dir holding f/kill/kill6_U*.npy and tab_{1,-1}.json (reg_A78 = full tables; s46c/noC = D-only).  Log: s46c/upper_TAG.log
. $(dirname $0)/env.sh; cd $E
TAG=$1; TD=$2; XF=$3; VF=$4
a=$(df -BG --output=avail $SC | tail -1 | tr -dc 0-9); [ "$a" -gt 10 ] || { echo "df ${a}G, not run" > $O/upper_$TAG.log; exit 5; }
[ -n "$VF" ] && : > $VF && XF="$XF vK=1e12 vfile=$VF"
nice -n 10 python3 pcheck.py upperR2 $(fq $TD) $X $XF nomax sol=$SOL $A threads=1 work=$SC/P/wr46c_$TAG > $O/upper_$TAG.log 2>&1 || echo "upper exit $?" >> $O/upper_$TAG.log
echo "$(date -u +%H:%M:%SZ) [$TAG] tables=$(basename $TD) flags='$XF': $(grep UPPER-R2 $O/upper_$TAG.log)${VF:+ ; vrows $(wc -l < $VF)}" >> $O/s46c.log
rm -rf $SC/P/wr46c_$TAG
