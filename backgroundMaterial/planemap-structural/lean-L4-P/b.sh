#!/bin/bash
# usage: b.sh ModuleSuffix  -> builds, prints only errors and final status
cd /Users/fulkanjou/mathlib4-planemap
lake build Mathlib.Combinatorics.SimpleGraph.PlaneMap.$1 > /tmp/lb_$1.log 2>&1
grep -A30 "^error" /tmp/lb_$1.log | head -${2:-80}
tail -2 /tmp/lb_$1.log | grep -i "build\|error"
