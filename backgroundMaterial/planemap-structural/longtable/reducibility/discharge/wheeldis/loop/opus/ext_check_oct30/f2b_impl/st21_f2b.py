# ext_f2b wrapper: runs Studio's st21_check.py (read unchanged from $ST21) with these source-level changes:
#  (1) recv_spec (the exact python receiver row, spec 12.5) applies the 2-ball exclusions (f2b.extra6 / f2b.extra7) to the link-6 private mask
#      and the link-7 l3q mask;  (2) the separator binary is ext_f2b/sep3r_f2b (Studio sep3r_l3q + SEP_F2B leaf correction) with a table built here;
#  (3) the VIOLATED print lists the NVIOL worst + a VIOLSUM line;  (4) DSTOP / STOPIFVIOL / THRSHIFT controls;  (5) generated .bin tables go to $OUTD.
# env: F2B_RULES=json path, F2B_MODE=on|off|half (half = drop half the rules at random, F2B_SEED), F2B_BIN=old|new (old = Studio bin/sep3r_l3q),
#      F2B_SELFTEST=1|only, OUTD=dir for tables.
import sys, os
P = os.environ['ST21']; HERE_F = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE_F)
import f2b
src = open(P).read()
def rep(old, new, cnt=1):
    global src
    assert src.count(old) == cnt, (src.count(old), old)
    src = src.replace(old, new)
MODE = os.environ.get('F2B_MODE', 'on')
if MODE == 'on': f2b.load(os.environ['F2B_RULES'])
elif MODE == 'off': f2b.load(os.environ['F2B_RULES'], off=True)
elif MODE == 'half': f2b.load(os.environ['F2B_RULES'], drop_frac=0.5, seed=int(os.environ.get('F2B_SEED', '1')))
print('F2B mode %s rule counts %s' % (MODE, f2b.STATS), flush=True)
# (1)
rep("            mk = pmask(U, W(i - 2), W(i - 1), W(i + 1), W(i + 2), S(i - 2), S(i - 1), S(i), S(i + 1))\n            sg = sig2_of(U, W(i + 1), S(i), S(i - 1), W(i - 1), ap(W(i + 2)), ap(W(i - 2))) + (mk,)\n            if cand2(sg): r[('M', sg)] += 1",
    "            mk = pmask(U, W(i - 2), W(i - 1), W(i + 1), W(i + 2), S(i - 2), S(i - 1), S(i), S(i + 1)) & ~f2b.extra6(d, w, s, i)\n            sg = sig2_of(U, W(i + 1), S(i), S(i - 1), W(i - 1), ap(W(i + 2)), ap(W(i - 2))) + (mk,)\n            if cand2(sg): r[('M', sg)] += 1")
rep("r[('lQ', (c_, a_, MASK[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)]))] += 1",
    "r[('lQ', (c_, a_, MASK[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)] & ~f2b.extra7(d, w, s, i, sg_)))] += 1")
rep("r[('lQ', (8, c_, a_, MASK8[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)]))] += 1",
    "r[('lQ', (8, c_, a_, MASK8[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)] & ~f2b.extra7(d, w, s, i, sg_)))] += 1")
# (2)
OLDP = "    SEPX = _sp.Popen([os.path.join(HERE, 'bin', 'sep3r_l3q' if L3Q else 'sep3r_ak'), NS_['SF']], stdin=_sp.PIPE, stdout=_sp.PIPE, text=True, env=SEPENV)"
rep(OLDP, "    SEPENV_, SEPBIN_ = F2B_SETUP(SEPENV)\n    SEPX = _sp.Popen([SEPBIN_, NS_['SF']], stdin=_sp.PIPE, stdout=_sp.PIPE, text=True, env=SEPENV_)")
rep("sys.argv = ['wlp3r6', 'tag=", "OUTD = os.environ['OUTD']; os.makedirs(OUTD, exist_ok=True)\nsys.argv = ['wlp3r6', 'tag=")
rep("os.path.join(HERE, 'out', 'job31', 'st16',", "os.path.join(OUTD,", cnt=src.count("os.path.join(HERE, 'out', 'job31', 'st16',"))
SETUP = '''
def F2B_SETUP(SEPENV):
    import f2b as _f
    env = dict(SEPENV)
    if os.environ.get('F2B_BIN', 'new') == 'old':
        print('F2B: using Studio bin/sep3r_l3q (no 2-ball leaf correction)', flush=True); return env, os.path.join(HERE, 'bin', 'sep3r_l3q')
    assert L3Q and not V6
    tf = os.path.join(OUTD, 'f2b_tab.bin')
    _f.build_tables(tf, None, KT, MASK, MASK8 if L3Q8 else {}, Mval, Qeff, Qeff8 if L3Q8 else Qeff, sig2_of, ap, V6)
    if os.environ.get('F2B_MODE', 'on') != 'off': env['SEP_F2B'] = tf
    print('F2B: sep3r_f2b table %s (%s)' % (tf, os.environ.get('F2B_MODE', 'on')), flush=True)
    return env, os.path.join('@@HERE@@', 'sep3r_f2b')
'''.replace('@@HERE@@', HERE_F)
rep("import subprocess as _sp\n", "import subprocess as _sp\n" + SETUP)
rep("def rrel_row(d, lk, sv):", "if os.environ.get('F2B_SELFTEST'):\n    exec(open(os.path.join(%r, os.environ.get('F2B_SELFTEST_FILE', 'f2b_selftest.py'))).read(), globals())\n    if os.environ['F2B_SELFTEST'] == 'only': sys.exit(0)\ndef rrel_row(d, lk, sv):" % HERE_F)
# (3)(4)
old = "    for v_, lk, sv in exact_bad[:5]: print('VIOLATED receiverR2 d=%d exact load %.12f link %s s %s' % (d, v_, lk, sv))"
rep(old, "    for v_, lk, sv in sorted(exact_bad, reverse=True)[:int(os.environ.get('NVIOL', '20'))]: print('VIOLATED receiverR2 d=%d exact load %.12f excess %.12f link %s s %s' % (d, v_, v_ - (d - 6 + T), lk, sv))\n"
        "    if exact_bad: print('VIOLSUM d=%d count %d worst_excess %.12f' % (d, len(exact_bad), max(v_ for v_, _, _ in exact_bad) - (d - 6 + T)), flush=True)")
SH = "float(os.environ.get('THRSHIFT', '0'))"
rep("out = sepx(d, yv, xv, d - 6 + T + EPS, CAP)", "out = sepx(d, yv, xv, d - 6 + T + EPS + %s, CAP)" % SH)
rep("if spec_val(d, lk, sv) > d - 6 + T + EPS]", "if spec_val(d, lk, sv) > d - 6 + T + EPS + %s]" % SH)
i0 = src.index("    print('receivers d=%d: relaxation reports")
i1 = src.index('\n', i0)
src = src[:i1 + 1] + "    if os.environ.get('STOPIFVIOL') and (rbad or not full):\n        print('STOPIFVIOL: stopped after d=%d (violations or incomplete); later degrees NOT run' % d, flush=True); sys.exit(0)\n" + src[i1 + 1:]
rep("for d in range(7, DMAXP + 1):\n    _t0 = _tm.time()", "for d in range(int(os.environ.get('DSTART', '7')), min(DMAXP, int(os.environ.get('DSTOP', '99'))) + 1):\n    _t0 = _tm.time()")
if os.environ.get('DSTOP'):
    o3 = "z9 = max([v for tq, v in X.items()"
    rep(o3, "print('PARTIAL RUN (DSTART=%s DSTOP=%s): stopped after the receivers; FAIL so far: %s' % (os.environ.get('DSTART', '7'), os.environ['DSTOP'], FAIL), flush=True); sys.exit(0)\n" + o3)
sys.argv = [P] + sys.argv[1:]
g = {'__file__': P, '__name__': '__main__', 'f2b': f2b}
exec(compile(src, P, 'exec'), g)
