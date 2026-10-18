"""Q_rule_class/capcheck.py: first-order slack ("cap") of a big z in a partial frame, at a given y solution (x=0, T=0).
cap = (d - 6 + t) - max admissible y-load over arrangements of z agreeing with the frame (+ extra 6-wheel filters).
usage: python3 -I capcheck.py ROOT SOL ARGS     (frames are defined below; uses ../J_lp_checker/jcheck2.py machinery)"""
import sys, os, re, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT, SOL, ARGS = sys.argv[1:4]
J = os.path.join(HERE, '..', 'J_lp_checker', 'jcheck2.py')
sys.argv = [J, 'help', 'root=' + ROOT, 'args=' + ARGS]
g = {'__file__': J, '__name__': 'jc'}
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(open(J).read(), g)
g['load_patterns'](); t, y, x, S = g['load_solution'](SOL)
LET = (5, 6, 7, 8, 9); LI = g['LI']; isR6 = g['isR6']
def cap(d, W, S_, extra=(), top=None, name=''):
    """max admissible y-load of a frame via jsep2 (mode 1, no symmetry break): fixed letters and extra joint conditions
    are added as forbidden pattern instances. W, S_: letter or None per position; extra: list of (slots, pred) with
    slots a list of ('w'|'s', i) and pred(letters) -> True if allowed."""
    U = min(d, 9); WT = g['window_table'](U, y, {})
    inst = list(g['instances'](d))
    sl = lambda typ, i: 2 * i + (typ == 's')
    for i in range(d):
        for typ, v in (('w', W[i]), ('s', S_[i])):
            if v is not None: inst.append(((sl(typ, i), 31 & ~(1 << LI[v])),))
    for slots, pred in extra:
        for combo in itertools.product(range(5), repeat=len(slots)):
            if not pred([LET[c] for c in combo]): inst.append(tuple(sorted((sl(t_, i_), 1 << c) for (t_, i_), c in zip(slots, combo))))
    hdr = os.path.join(HERE, 'work', 'hdr_%s_%d.txt' % (re.sub(r'\W', '', name), d)); os.makedirs(os.path.dirname(hdr), exist_ok=True)
    big = sorted(b for b in g['RBIG'] if len(b) == d) if d in (7, 8) else []
    with open(hdr, 'w') as f:
        f.write('%d %.15f %d %d\n%d\n%s\n%d\n' % (d, 0.0, 1, 1, len(big), '\n'.join(big), len(inst)))
        for I in inst: f.write('%d %s\n' % (len(I), ' '.join('%d %d' % sk for sk in I)))
    wp = os.path.join(HERE, 'work', 'win_q%d.bin' % d)
    np.ascontiguousarray(np.where(np.isfinite(WT), WT, -1e300), dtype=np.float64).tofile(wp)
    import subprocess
    out = subprocess.run([g['BIN'], hdr, wp, '1', '0'], capture_output=True, text=True, check=True).stdout.split()
    v = float(out[1]); c = d - 6 + t - v
    print('%-30s d=%d max load %.6f  cap = %.6f  at link %s s %s' % (name, d, v, c, out[2], out[3]), flush=True)
    return c
def nonR6(*wd): return lambda w, s: not isR6([v(w, s) if callable(v) else v for v in wd])
if __name__ == '__main__':
    F = None
    for d in (7, 8):
        # p1 at R*(6,6): link [o1, s0=6, w1=6, s1=6, q, ...], s(o1,s0)=o2, s(s0,w1)=w0=5, s(w1,s1)=w2=7
        # extras: s0's wheel (U, w1=6, w0=5, s6=5, o2, o1) non-R6; s1's wheel (U, q, s(s1,q), p2a, w2=7, w1=6) non-R6 for some p2a>=6
        Wf = [F, 6, 6, 6] + [F] * (d - 4); Sf = [F, 5, 7] + [F] * (d - 3)
        ex = [([('s', 0), ('w', 0)], lambda L, d=d: not isR6([min(d, 9), 6, 5, 5, L[0], L[1]])),
              ([('w', 4), ('s', 3)], lambda L, d=d: any(not isR6([min(d, 9), L[0], L[1], p, 7, 6]) for p in (6, 7, 8, 9)))]
        cap(d, Wf, Sf, ex, name='p1 (H/S target) at (6,6)')
        cap(d, Wf, Sf, [], name='p1 frame, no extras')
        # p5 at (6,6): link [a, s4=6, w5=6, s5=7, ...], s(s4,w5)=w4=7, s(w5,s5)=w6=5; w5 private (rel p5) = u=7
        Wf = [F, 6, 6, 7] + [F] * (d - 4); Sf = [F, 7, 5] + [F] * (d - 3)
        cap(d, Wf, Sf, [], name='p5 (T from s5-root) (6,6)')
    # w2 at (6,6): link (u7, w1 6, s1 6, p2a, p2b, s2 7, w3 5), s (w0 5, p1 B, x, x, x, s3 7, w4 7), p2a>=6
    for p1 in (7, 8, 9):
        cap(7, [7, 6, 6, F, F, 7, 5], [5, p1, F, F, F, 7, 7], [([('w', 3), ('w', 4)], lambda L: L[0] >= 6 and not (L[0] == 6 and L[1] == 5))], name='w2 (T target) p1=%d' % p1)
    # s1 big (S-opp target of w0 through w1) for s1 = 7, 8: link of s1 (w1 6, w2 7, p2a, ..., p1); s(w1? ) : s1's arrangement
    # s1 link: [p1, w1=6, w2=7, p2a, ..., ]  s(p1,w1)=s0=6, s(w1,w2)=u=7 ; w1's private rel s1 = w0 = 5
    for d in (7, 8):
        cap(d, [F, 6, 7] + [F] * (d - 3), [6, 7] + [F] * (d - 2), [], name='s1 (S-opp target) s1=%d' % d)
