# s86 (10 Nov 01:20Z, disk full at 01:13Z killed GS18): every 10 min remove scratchpad sD/wr86u_* and wr86K_* work dirs that no live
# pcheck process uses and that have not changed for 15 min (U86/K runs never delete their work dirs; 221 MB per K run).
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/sD
while true; do
  R=$(for p in $(pgrep -f 'pcheck.py'); do tr '\0' '\n' < /proc/$p/cmdline 2>/dev/null | grep '^work=' | sed 's|work=||'; done)
  for d in $(find $S -maxdepth 1 -type d \( -name 'wr86u_*' -o -name 'wr86K_*' \) -mmin +15 2>/dev/null); do
    echo "$R" | grep -qx "$d" && continue
    [ -n "$(find $d -mmin -15 2>/dev/null | head -1)" ] && continue
    rm -rf "$d"
  done
  sleep 600
done
