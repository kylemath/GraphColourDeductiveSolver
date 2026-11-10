#!/bin/bash
# maclane v2e add-on install (Opus 10 Nov): the engine dir eng_p8 (payer-8/9 EDGE keys, PAYER8SPEC W5), an ENG=eng_p8 knob for the upper
# lane and its checks, and the 268-key file.  Run from the v2e folder, on top of v2d1:
#   bash install_v2e.sh            (DRY=1: only the checks; FORCE=1: install over files whose md5 is not the expected one)
#   then bash build_v2e.sh         (compiles eng_p8/bin; launch_msfam.sh / recheck_fam.sh with ENG=eng_p8 need it)
# Replaces 4 files (each kept as <file>.pre_v2e), adds the 268-key file and makes eng_p8 = a copy of the installed eng_p1r (*.py, *.cpp)
# with eng_p8/{edge56.py, p1r.py, pcheck.py, w6b_p8_ref.py, jsepf_gk_k192s_p8.cpp} from this folder and prelay2.py from eng_p1t (the
# k5e copy with the tighten line).  eng_p1r, eng_p1t and every running lane are untouched: copies are atomic (tmp + mv), and with ENG
# unset every command runs on eng_p1r exactly as before.
R=/tmp/maclane-k86
N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
H=$(cd "$(dirname "$0")" && pwd -P); DRY=${DRY:-0}; FORCE=${FORCE:-0}
md5of() { python3 -c "import sys, hashlib; print(hashlib.md5(open(sys.argv[1], 'rb').read()).hexdigest())" "$1"; }
# pack integrity
bad=0
while read -r m f; do
  [ -f "$H/$f" ] || { echo "install_v2e: $f missing from the pack" >&2; bad=1; continue; }
  [ "$(md5of "$H/$f")" = "$m" ] || { echo "install_v2e: $f md5 $(md5of "$H/$f"), MD5SUMS says $m" >&2; bad=1; }
done < "$H/MD5SUMS"
[ $bad = 0 ] || { echo "install_v2e: pack check failed, nothing installed" >&2; exit 2; }
# v2d1 must be installed (files v2e does not replace; launch_msfam.sh is checked with the targets below)
for f in $R/stop_fam.sh:7d1a090f5cb9379dc7dad615ab850260 $R/status_fam.sh:c0966049dda2cc11a0d7f7acdc566eff $N/fam_lib.py:67daca90f9d2393c0f9795493b790093; do
  [ "$(md5of ${f%%:*} 2>/dev/null)" = "${f#*:}" ] || { echo "install_v2e: ${f%%:*} is not the v2d / v2d1 one (${f#*:}): install v2d and v2d1 first" >&2; exit 2; }
done
# targets: pack file, installed path, accepted old md5s (v2d1 / v2d / k5e / v2d; 'none' = may be absent)
T="launch_msfam.sh|$N/launch_msfam.sh|0158680c883cf7aaaacd08f7a33e677b
recheck_fam.sh|$R/recheck_fam.sh|1bcbc07b8c4ed260034c956086c03481
runK86p.sh|$N/p1r/runK86p.sh|6b3c9734e2cf91ec57942fc2e02c73bc
k5e_lib.py|$N/k5e_lib.py|839623aa2967ba1baa5e23bc20b1127b
cg_keys_r13w16_16fikp_p8bb.txt|$N/p1r/cg_keys_r13w16_16fikp_p8bb.txt|none"
bad=0
while IFS='|' read -r f dst olds; do
  new=$(md5of "$H/$f")
  if [ ! -f "$dst" ]; then
    case ",$olds," in *,none,*) echo "  $f: new file -> $dst" ;; *) echo "install_v2e: $dst missing (install v2d and v2d1 first)" >&2; bad=1 ;; esac
    continue
  fi
  cur=$(md5of "$dst")
  if [ "$cur" = "$new" ]; then echo "  $f: already v2e ($new)"; continue; fi
  case ",$olds," in *",$cur,"*) echo "  $f: $cur -> $new" ;; *) echo "install_v2e: $dst has md5 $cur, expected one of $olds" >&2; bad=1 ;; esac
done <<< "$T"
# eng_p8: the base files the overrides were made against (the pack's eng_p1r, the k5e eng_p1t/prelay2.py)
for f in eng_p1r/edge56.py:1095b49c5562c7fbe4076cb36354eab6 eng_p1r/p1r.py:8f5d2e7e1181750b50e7086bdfec8fdb eng_p1r/pcheck.py:2dbeadf5bebe61579d3c300e493229a6 eng_p1t/prelay2.py:c4c95ae9ac0360ce9f98935db2b83c2c; do
  [ "$(md5of $N/${f%%:*} 2>/dev/null)" = "${f#*:}" ] || { echo "install_v2e: $N/${f%%:*} is not the pack's (${f#*:}); eng_p8 is made from it" >&2; bad=1; }
done
p8chk() {   # p8chk <dir>: the dir's *.py / *.cpp are exactly ENG_P8.md5 (prints the first difference; a python -c, no here-document)
  python3 -c "
import sys, os, hashlib
d, mf = sys.argv[1], sys.argv[2]
want = dict(l.split()[::-1] for l in open(mf) if l.strip())
have = dict((f, hashlib.md5(open(os.path.join(d, f), 'rb').read()).hexdigest()) for f in os.listdir(d) if f.endswith(('.py', '.cpp')) and os.path.isfile(os.path.join(d, f)))
for f in sorted(set(want) | set(have)):
    if want.get(f) != have.get(f): print('%s: %s, ENG_P8.md5 says %s' % (f, have.get(f, 'missing'), want.get(f, 'absent'))); sys.exit(1)
" "$1" "$H/ENG_P8.md5"
}
P8=new
if [ -e $N/eng_p8 ]; then
  if D=$(p8chk $N/eng_p8); then P8=same; echo "  eng_p8: already v2e ($(wc -l < $H/ENG_P8.md5 | tr -d ' ') files)"
  else echo "install_v2e: $N/eng_p8 exists and differs from ENG_P8.md5 ($D)$( [ "$FORCE" = 1 ] && echo '; FORCE=1: it is moved to eng_p8.pre_v2e_<UTC>')" >&2; bad=1; P8=replace; fi
else echo "  eng_p8: new engine dir -> $N/eng_p8 (eng_p1r copy + 5 v2e files + eng_p1t/prelay2.py)"; fi
if [ $bad = 1 ] && [ "$FORCE" != 1 ]; then echo "install_v2e: nothing installed (FORCE=1 installs anyway)" >&2; exit 2; fi
[ "$DRY" = 1 ] && { echo "install_v2e: (dry) checks done, nothing installed"; exit 0; }
while IFS='|' read -r f dst olds; do
  new=$(md5of "$H/$f"); [ -f "$dst" ] && [ "$(md5of "$dst")" = "$new" ] && continue
  [ -f "$dst" ] && [ ! -f "$dst.pre_v2e" ] && cp -p "$dst" "$dst.pre_v2e"
  cp "$H/$f" "$dst.v2e_tmp" && chmod 644 "$dst.v2e_tmp" && mv -f "$dst.v2e_tmp" "$dst" || { echo "install_v2e: copy to $dst failed" >&2; exit 2; }
  [ "$(md5of "$dst")" = "$new" ] || { echo "install_v2e: $dst md5 after copy is not $new" >&2; exit 2; }
done <<< "$T"
if [ $P8 != same ]; then
  W=$N/eng_p8.v2e_tmp; rm -rf $W; mkdir -p $W/bin || { echo "install_v2e: cannot make $W" >&2; exit 2; }
  for f in $N/eng_p1r/*.py $N/eng_p1r/*.cpp; do cp -p $f $W/ || { echo "install_v2e: copy of $f failed" >&2; exit 2; }; done
  for f in edge56.py p1r.py pcheck.py w6b_p8_ref.py jsepf_gk_k192s_p8.cpp; do cp $H/eng_p8/$f $W/$f && chmod 644 $W/$f || { echo "install_v2e: copy of eng_p8/$f failed" >&2; exit 2; }; done
  cp $N/eng_p1t/prelay2.py $W/prelay2.py && chmod 644 $W/prelay2.py || { echo "install_v2e: copy of eng_p1t/prelay2.py failed" >&2; exit 2; }
  D=$(p8chk $W) || { echo "install_v2e: the new eng_p8 differs from ENG_P8.md5 ($D); left in $W" >&2; exit 2; }
  if [ -e $N/eng_p8 ]; then mv $N/eng_p8 $N/eng_p8.pre_v2e_$(date -u +%Y%m%dT%H%M%SZ) || exit 2; fi
  mv $W $N/eng_p8 || { echo "install_v2e: mv $W $N/eng_p8 failed" >&2; exit 2; }
fi
for f in $N/launch_msfam.sh $R/recheck_fam.sh $N/p1r/runK86p.sh; do bash -n $f || { echo "install_v2e: bash -n $f failed" >&2; exit 2; }; done
(cd $N && python3 k5e_lib.py keyscheck $N/p1r/cg_keys_r13w16_16fik.txt && python3 k5e_lib.py keyscheck $N/p1r/cg_keys_r13w16_16fikp.txt \
  && python3 k5e_lib.py keyscheck $N/p1r/cg_keys_r13w16_16fikp_p8bb.txt && [ "$(python3 k5e_lib.py keyseng $N/p1r/cg_keys_r13w16_16fikp.txt)" = eng_p1r ] \
  && [ "$(python3 k5e_lib.py keyseng $N/p1r/cg_keys_r13w16_16fikp_p8bb.txt)" = eng_p8 ]) || { echo "install_v2e: keyscheck / keyseng failed" >&2; exit 2; }
echo "$(date -u +%H:%M:%SZ) [maclane] v2e installed: engine dir eng_p8 (payer-8/9 keys, PAYER8SPEC W5), ENG=eng_p8 for launch_msfam.sh / recheck_fam.sh / p1r/runK86p.sh, 268 keys cg_keys_r13w16_16fikp_p8bb.txt (b5875bfe -> K3l5x_k268)" >> $N/run.log
echo "install_v2e: done (backups *.pre_v2e).  Next: bash $H/build_v2e.sh"
