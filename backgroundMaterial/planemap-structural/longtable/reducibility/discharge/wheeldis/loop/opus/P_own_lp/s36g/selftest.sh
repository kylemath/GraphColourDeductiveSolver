# s36g selftest of the l3q and f-pattern absorption paths with two SYNTHETIC names (not kills).  bash selftest.sh
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
M=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
SW=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/s36g_work; mkdir -p $SW
S=$B/s36g; L=$S/selftest.log; cd $S/eng
printf 'q7-_755...._6......_.5::::::\n' > $SW/synthL.txt; printf 'q7u_7665566_6675676_::::::\n' > $SW/synthF.txt
python3 - > $L 2>&1 <<'PY'
import itertools, collections
exec(open('privcell.py').read().split("if __name__ == '__main__':")[0])
print('# s36g selftest. Synthetic names, NOT kills: they only exercise the l3q and f-pattern paths of pc_build.')
for nm in ['q7-_755...._6......_.5::::::', 'q7u_7665566_6675676_::::::']:
    PC_LOG.clear(); AM, L3, PT = pc_build([nm])
    print(nm, 'canon', pc_canon(pc_parse(nm)), PC_LOG[-1][3], 'l3q keys', len(L3), 'by sg', sorted(collections.Counter(k[0] for k in L3).items()), 'f-patterns', {d: len(v) for d, v in PT.items()})
for nm in [l.split()[0] for l in open('../g7_q.txt') if not l.startswith('#')]:
    N = pc_parse(nm); V, E = pc_pattern(N); print('pattern', nm, {k: ''.join(map(str, sorted(v))) for k, v in V.items()}, E, 'arc', pc_arc(N), 'cons2 sites', pc_cons2_sites(N))
PY
echo "# lowerR2 st24bL with the synthetic binder f-name (expect: the binder receiver row is no longer admissible)" >> $L
A="root=$M args=$B/s25/argsA59.txt rpat=$B/rpatD.txt threads=1 work=$SW"; F0="xon apexcls filt16 killtab=$B/s25/f/kill/kill6 hat5 consall"
nice python3 pcheck.py lowerR2 $F0 pcell=$SW/synthF.txt cert=$B/s24d/cert_st24bL.json xcap=3 $A 2>&1 | grep "pcell\|NOT ADMISS\|LOWER\|patterns:" >> $L
echo "# lowerR2 s28A60L (l3q) with the synthetic l3q name (cert has no mrowL rows, so VALID is expected; masks change)" >> $L
F="xon apexcls filt16 killtab=$B/s29/f/kill/kill6 hat5 consall l3q l3qtab=$B/s28q/tab60_1.json,$B/s28q/tab60_-1.json lqcap=3"; A6="root=$M args=$B/s29/argsA60.txt rpat=$B/rpatD.txt threads=1 work=$SW"
nice python3 pcheck.py lowerR2 $F pcell=$SW/synthL.txt cert=$B/s28q/eng/cert_s28A60L.json xcap=3 $A6 2>&1 | grep "pcell\|BAD\|negative\|LOWER" >> $L
