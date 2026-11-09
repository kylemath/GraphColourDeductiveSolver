#!/bin/bash
# maclane v2d add-on install (Opus 9 Nov): key-file override (KEYS=) and a parallel upper lane (PARALLEL=1).  Run from the v2d folder:
#   bash install_v2d.sh            (DRY=1: only the checks; FORCE=1: install over files whose md5 is not the expected one)
# Replaces 5 files and adds the 260-key file; each replaced file is kept as <file>.pre_v2d.  Every copy is atomic (tmp + mv), so a
# running lane (k86MS6) is not disturbed: its processes keep the code they loaded; new calls get v2d, which on the 240 keys behaves as before.
R=/tmp/maclane-k86
N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
H=$(cd "$(dirname "$0")" && pwd -P); DRY=${DRY:-0}; FORCE=${FORCE:-0}
md5of() { python3 -c "import sys, hashlib; print(hashlib.md5(open(sys.argv[1], 'rb').read()).hexdigest())" "$1"; }
# pack integrity
bad=0
while read -r m f; do
  [ -f "$H/$f" ] || { echo "install_v2d: $f missing from the pack" >&2; bad=1; continue; }
  [ "$(md5of "$H/$f")" = "$m" ] || { echo "install_v2d: $f md5 $(md5of "$H/$f"), MD5SUMS says $m" >&2; bad=1; }
done < "$H/MD5SUMS"
[ $bad = 0 ] || { echo "install_v2d: pack check failed, nothing installed" >&2; exit 2; }
# targets: pack file, installed path, accepted old md5s (k5g / v2c / k5e / k5g / k5g; 'none' = may be absent)
T="launch_msfam.sh|$N/launch_msfam.sh|41bbab631b3fb54c952f5f0251d48c50,74a41d8ae4be702bf806ddc67405c2f6
recheck_fam.sh|$R/recheck_fam.sh|a2716a38a24b68ed8c27259e918a6626
k5e_lib.py|$N/k5e_lib.py|69bb7d60089e8ddda56f992a9074fdc4
fam_lib.py|$N/fam_lib.py|60e584896c5dd29d50497af9447ec713
outbox86_fam.py|$N/outbox86_fam.py|ac5e899161560c6ee2d48d8ff4cc65bf
cg_keys_r13w16_16fikp.txt|$N/p1r/cg_keys_r13w16_16fikp.txt|none"
bad=0
while IFS='|' read -r f dst olds; do
  new=$(md5of "$H/$f")
  if [ ! -f "$dst" ]; then
    case ",$olds," in *,none,*) echo "  $f: new file -> $dst" ;; *) echo "install_v2d: $dst missing (install the k5e and k5g add-ons first)" >&2; bad=1 ;; esac
    continue
  fi
  cur=$(md5of "$dst")
  if [ "$cur" = "$new" ]; then echo "  $f: already v2d ($new)"; continue; fi
  case ",$olds," in *",$cur,"*) echo "  $f: $cur -> $new" ;; *) echo "install_v2d: $dst has md5 $cur, expected one of $olds" >&2; bad=1 ;; esac
done <<< "$T"
if [ $bad = 1 ] && [ "$FORCE" != 1 ]; then echo "install_v2d: nothing installed (FORCE=1 installs anyway)" >&2; exit 2; fi
[ "$DRY" = 1 ] && { echo "install_v2d: (dry) checks done, nothing installed"; exit 0; }
while IFS='|' read -r f dst olds; do
  new=$(md5of "$H/$f"); [ -f "$dst" ] && [ "$(md5of "$dst")" = "$new" ] && continue
  [ -f "$dst" ] && [ ! -f "$dst.pre_v2d" ] && cp -p "$dst" "$dst.pre_v2d"
  cp "$H/$f" "$dst.v2d_tmp" && chmod 644 "$dst.v2d_tmp" && mv -f "$dst.v2d_tmp" "$dst" || { echo "install_v2d: copy to $dst failed" >&2; exit 2; }
  [ "$(md5of "$dst")" = "$new" ] || { echo "install_v2d: $dst md5 after copy is not $new" >&2; exit 2; }
done <<< "$T"
for f in $N/launch_msfam.sh $R/recheck_fam.sh; do bash -n $f || { echo "install_v2d: bash -n $f failed" >&2; exit 2; }; done
(cd $N && python3 k5e_lib.py keyscheck $N/p1r/cg_keys_r13w16_16fik.txt && python3 k5e_lib.py keyscheck $N/p1r/cg_keys_r13w16_16fikp.txt) || { echo "install_v2d: keyscheck failed" >&2; exit 2; }
echo "$(date -u +%H:%M:%SZ) [maclane] v2d installed: KEYS= and PARALLEL=1 for launch_msfam.sh, KEYS= for recheck_fam.sh, keyed families (260 keys -> K3l5x_k260)" >> $N/run.log
echo "install_v2d: done (backups *.pre_v2d)"
