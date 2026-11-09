#!/bin/bash
# maclane macshim v2 install (Opus 9 Nov): replaces /tmp/maclane-k86/macshim/timeout (v1 1cefd903) with v2; v1 kept as timeout.v1.
#   bash install_macshim2.sh   (DRY=1: checks only; FORCE=1: install over another md5)
R=/tmp/maclane-k86; H=$(cd "$(dirname "$0")" && pwd -P); DST=$R/macshim/timeout
md5of() { python3 -c "import sys, hashlib; print(hashlib.md5(open(sys.argv[1], 'rb').read()).hexdigest())" "$1"; }
while read -r m f; do [ "$(md5of "$H/$f")" = "$m" ] || { echo "install_macshim2: $f md5 differs from MD5SUMS: nothing installed" >&2; exit 2; }; done < "$H/MD5SUMS"
NEW=$(md5of $H/timeout); CUR=$(md5of $DST 2>/dev/null)
[ "$CUR" = "$NEW" ] && { echo "install_macshim2: already v2 ($NEW)"; exit 0; }
[ "$CUR" = 1cefd903235ee0606aea1470a1579699 ] || [ "${FORCE:-0}" = 1 ] || { echo "install_macshim2: $DST has md5 $CUR, not v1 1cefd903 (FORCE=1 installs anyway)" >&2; exit 2; }
[ "${DRY:-0}" = 1 ] && { echo "install_macshim2: (dry) would replace $DST ($CUR -> $NEW)"; exit 0; }
[ -f $DST.v1 ] || cp -p $DST $DST.v1
cp $H/timeout $DST.v2_tmp && chmod 755 $DST.v2_tmp && mv -f $DST.v2_tmp $DST || { echo "install_macshim2: copy failed" >&2; exit 2; }
bash -n $DST && [ "$(md5of $DST)" = "$NEW" ] || { echo "install_macshim2: check after copy failed" >&2; exit 2; }
$DST 2 bash -c 'exit 3'; a=$?; $DST 1 sleep 5; b=$?
[ $a = 3 ] && [ $b = 124 ] || { echo "install_macshim2: self-test failed ($a, $b; want 3, 124): restore with cp $DST.v1 $DST" >&2; exit 2; }
echo "install_macshim2: done ($CUR -> $NEW; v1 kept as $DST.v1); self-test 3 / 124 OK"
