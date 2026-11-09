#!/bin/bash
# maclane v2d1 add-on install (Opus 9 Nov): side-lane tags k86MK<n> for launch_msfam.sh / stop_fam.sh / status_fam.sh, on top of v2d.
#   bash install_v2d1.sh           (DRY=1: only the checks; FORCE=1: install over files whose md5 is not the expected one)
# Needs v2d installed (k5e_lib.py 839623aa, fam_lib.py 67daca90).  Replaces 3 files; each is kept as <file>.pre_v2d1.  Every copy is atomic (tmp + mv), so a
# running lane (k86MS6) is not disturbed: its processes keep the code they loaded; new calls get v2d, which on the 240 keys behaves as before.
R=/tmp/maclane-k86
N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
H=$(cd "$(dirname "$0")" && pwd -P); DRY=${DRY:-0}; FORCE=${FORCE:-0}
md5of() { python3 -c "import sys, hashlib; print(hashlib.md5(open(sys.argv[1], 'rb').read()).hexdigest())" "$1"; }
# pack integrity
bad=0
while read -r m f; do
  [ -f "$H/$f" ] || { echo "install_v2d1: $f missing from the pack" >&2; bad=1; continue; }
  [ "$(md5of "$H/$f")" = "$m" ] || { echo "install_v2d1: $f md5 $(md5of "$H/$f"), MD5SUMS says $m" >&2; bad=1; }
done < "$H/MD5SUMS"
[ $bad = 0 ] || { echo "install_v2d1: pack check failed, nothing installed" >&2; exit 2; }
for f in k5e_lib.py:839623aa2967ba1baa5e23bc20b1127b fam_lib.py:67daca90f9d2393c0f9795493b790093; do
  [ "$(md5of $N/${f%%:*})" = "${f#*:}" ] || { echo "install_v2d1: $N/${f%%:*} is not the v2d one (${f#*:}): install v2d first (bash install_v2d.sh)" >&2; exit 2; }
done
# targets: pack file, installed path, accepted old md5s (v2d / k5g / k5g)
T="launch_msfam.sh|$N/launch_msfam.sh|91af83c35e6d28f8335d9dcc2fe1733c
stop_fam.sh|$R/stop_fam.sh|8de63ed3f89511354e1af576c5916179
status_fam.sh|$R/status_fam.sh|31eae46fa2cd932dec38268a92770286"
bad=0
while IFS='|' read -r f dst olds; do
  new=$(md5of "$H/$f")
  if [ ! -f "$dst" ]; then
    case ",$olds," in *,none,*) echo "  $f: new file -> $dst" ;; *) echo "install_v2d1: $dst missing (install the k5e and k5g add-ons first)" >&2; bad=1 ;; esac
    continue
  fi
  cur=$(md5of "$dst")
  if [ "$cur" = "$new" ]; then echo "  $f: already v2d1 ($new)"; continue; fi
  case ",$olds," in *",$cur,"*) echo "  $f: $cur -> $new" ;; *) echo "install_v2d1: $dst has md5 $cur, expected one of $olds" >&2; bad=1 ;; esac
done <<< "$T"
if [ $bad = 1 ] && [ "$FORCE" != 1 ]; then echo "install_v2d1: nothing installed (FORCE=1 installs anyway)" >&2; exit 2; fi
[ "$DRY" = 1 ] && { echo "install_v2d1: (dry) checks done, nothing installed"; exit 0; }
while IFS='|' read -r f dst olds; do
  new=$(md5of "$H/$f"); [ -f "$dst" ] && [ "$(md5of "$dst")" = "$new" ] && continue
  [ -f "$dst" ] && [ ! -f "$dst.pre_v2d1" ] && cp -p "$dst" "$dst.pre_v2d1"
  cp "$H/$f" "$dst.v2d1_tmp" && chmod 644 "$dst.v2d1_tmp" && mv -f "$dst.v2d1_tmp" "$dst" || { echo "install_v2d1: copy to $dst failed" >&2; exit 2; }
  [ "$(md5of "$dst")" = "$new" ] || { echo "install_v2d1: $dst md5 after copy is not $new" >&2; exit 2; }
done <<< "$T"
for f in $N/launch_msfam.sh $R/stop_fam.sh $R/status_fam.sh; do bash -n $f || { echo "install_v2d1: bash -n $f failed" >&2; exit 2; }; done
echo "$(date -u +%H:%M:%SZ) [maclane] v2d1 installed: side-lane tags k86MK<n> (launch_msfam.sh, stop_fam.sh, status_fam.sh)" >> $N/run.log
echo "install_v2d1: done (backups *.pre_v2d1)"
