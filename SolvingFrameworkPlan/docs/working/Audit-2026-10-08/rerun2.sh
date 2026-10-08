#!/bin/zsh
# rerun the two copies whose appended print lines had wrong namespaces, plus the challenge non-vacuity file
source <(sed -n '/^SP=/,/^esac; }/p' run_audit.sh)
run() { local cp=$OUT/audit_$2.lean
  cp "$P/$1.lean" "$cp"; printf '%s\n' "$3" >> "$cp"; printf '%s\n' "$SWEEP" >> "$cp"
  local s=$(date +%s)
  ( ulimit -t 1800; nice -n 10 env LEAN_PATH="$LP" $LEAN "$cp" ) > "$OUT/audit_$2.out" 2>&1; echo "exit $?" >> "$OUT/audit_$2.out"
  echo "$2 wall $(( $(date +%s) - s ))s (rerun)" >> "$OUT/times.txt"; }
run QuarterLockParity QuarterLockParity "$(pr QuarterLockParity)"
run ChainMod4 ChainMod4 "$(pr ChainMod4)"
( ulimit -t 1800; nice -n 10 env LEAN_PATH="$LP" $LEAN $SP/audit/ChallengeNonVacuity.lean ) > $OUT/ChallengeNonVacuity.out 2>&1; echo "exit $?" >> $OUT/ChallengeNonVacuity.out
