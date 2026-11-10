#!/bin/bash
# maclane v2e build (Opus 10 Nov): compile the separators of the engine dir eng_p8 (made by install_v2e.sh), about 20 s.
#   bash build_v2e.sh        [env as build.sh: CXX (default clang++, else c++ / g++), CXXFLAGS, ARCHFLAG]
# eng_p8/bin/jsepf_gk_k192 <- eng_p8/jsepf_gk_k192s_p8.cpp (the container's p8 leaf: the gkin payer mask takes letters 5..9, um <= 31,
#   and the d = 7 leaf credits payer letters 8 / 9 as well); eng_p8/bin/jsepf_gk = the same binary (as in the container's eng_p8/bin,
#   where jsepf_gk, jsepf_gk_k192 and jsepf_gk_k192s are one build); eng_p8/bin/jsep3 <- eng_p8/jsep3.cpp (= eng_p1r's).
# Same compiler line as the pack's build.sh.  Each binary is written to <bin>.v2e_tmp and moved into place, so a running check keeps its
# binary.  Exit 0 = all built.
R=/tmp/maclane-k86
N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
E=$N/eng_p8
md5of() { python3 -c "import sys, hashlib; print(hashlib.md5(open(sys.argv[1], 'rb').read()).hexdigest())" "$1"; }
[ -f $E/jsepf_gk_k192s_p8.cpp ] && [ -f $E/jsep3.cpp ] || { echo "build_v2e: $E is not there or incomplete: bash install_v2e.sh first" >&2; exit 2; }
[ "$(md5of $E/jsepf_gk_k192s_p8.cpp)" = 17307d6be6de7b8de9956a5a9fccdf10 ] || { echo "build_v2e: $E/jsepf_gk_k192s_p8.cpp is not the v2e one (17307d6b)" >&2; exit 2; }
if [ -z "$CXX" ]; then for c in clang++ c++ g++; do command -v $c > /dev/null 2>&1 && { CXX=$c; break; }; done; fi
CXXFLAGS=${CXXFLAGS:--std=c++17 -O3 -pthread -ffp-contract=off -include cstdint}
if [ -z "${ARCHFLAG+x}" ]; then
  T=${TMPDIR:-/tmp}/maclane_arch_$$; echo 'int main(){return 0;}' > $T.cpp
  if $CXX -mcpu=native -o $T $T.cpp > /dev/null 2>&1; then ARCHFLAG=-mcpu=native; else ARCHFLAG=""; fi; rm -f $T $T.cpp
fi
echo "build_v2e: $($CXX --version 2>&1 | head -1); flags $CXXFLAGS $ARCHFLAG"
FAIL=0; T0=$(date +%s); mkdir -p $E/bin
b() {   # b <source> <binary>
  if $CXX $CXXFLAGS $ARCHFLAG -o $E/bin/$2.v2e_tmp $E/$1 2> $E/bin/$2.build.log && mv -f $E/bin/$2.v2e_tmp $E/bin/$2; then
    echo "  ok   eng_p8/bin/$2  <- $1 $( [ -s $E/bin/$2.build.log ] && echo "(warnings: $E/bin/$2.build.log)")"
  else echo "  FAIL eng_p8/bin/$2  <- $1: see $E/bin/$2.build.log"; rm -f $E/bin/$2.v2e_tmp; FAIL=1; fi
  [ -s $E/bin/$2.build.log ] || rm -f $E/bin/$2.build.log
}
b jsepf_gk_k192s_p8.cpp jsepf_gk_k192
if [ $FAIL = 0 ]; then
  cp $E/bin/jsepf_gk_k192 $E/bin/jsepf_gk.v2e_tmp && chmod 755 $E/bin/jsepf_gk.v2e_tmp && mv -f $E/bin/jsepf_gk.v2e_tmp $E/bin/jsepf_gk && echo "  ok   eng_p8/bin/jsepf_gk  = eng_p8/bin/jsepf_gk_k192 (one p8 build, as in the container)" || FAIL=1
fi
b jsep3.cpp jsep3
echo "build_v2e: $([ $FAIL = 0 ] && echo OK || echo FAILED) in $(( $(date +%s) - T0 )) s"
[ $FAIL = 0 ] && echo "$(date -u +%H:%M:%SZ) [maclane] v2e build: eng_p8/bin/{jsepf_gk_k192,jsepf_gk} <- jsepf_gk_k192s_p8.cpp, jsep3 ($CXX)" >> $N/run.log
exit $FAIL
