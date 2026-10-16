"""EXPLORE round 12 (exploratory): H-AV probe.  Can the receivers of a wlp3 certificate sit next to each other?
For receiver arrangements A, B (d = 7 here, any d works) and a link big w_i of A whose degree equals B's degree, the
arrangement of v = w_i is partly fixed by A's letters:
  v's link (cyclic): u, w_i+1, s_i, (deg v - 5 free p slots of A), s_i-1, w_i-1;
  v's s word: w_i+2 (between u and w_i+1); s_i+1 if w_i+1 = 5 else free; free x (deg v - 4);
              s_i-2 if w_i-1 = 5 else free; w_i-2 (between w_i-1 and u).
B fits at v if some dihedral image of B agrees with every fixed letter.  If the certificate's receivers can be paired
this way (with matching dual weights), the same dual combination is a certificate for the pair-averaging model
charge(u) + charge(v) <= 2t, so that model cannot go below the certificate's t.
Usage: python3 pairs.py 'linkA sA' 'linkB sB' ..."""
import sys
def images(lk, sv):
    d = len(lk)
    for r in range(d):
        yield lk[r:] + lk[:r], sv[r:] + sv[:r]
        yield ''.join(lk[(r - i) % d] for i in range(d)), ''.join(sv[(r - i - 1) % d] for i in range(d))
def view(lk, sv, i):
    d = len(lk); dv = int(lk[i]); w = lambda k: lk[(i + k) % d]; s = lambda k: sv[(i + k) % d]
    L = [str(d), w(1), s(0)] + ['?'] * (dv - 5) + [s(-1), w(-1)]
    S = [w(2), s(1) if w(1) == '5' else '?'] + ['?'] * (dv - 4) + [s(-2) if w(-1) == '5' else '?', w(-2)]
    return ''.join(L), ''.join(S)
def fits(view_, B):
    L, S = view_
    if len(L) != len(B[0]): return []
    out = []
    for lk, sv in images(*B):
        if all(a == '?' or a == b for a, b in zip(L, lk)) and all(a == '?' or a == b for a, b in zip(S, sv)): out.append((lk, sv))
    return out
arrs = [tuple(a.split()) for a in sys.argv[1:]]
for A in arrs:
    for i, ch in enumerate(A[0]):
        if ch not in '789': continue
        vw = view(A[0], A[1], i)
        for B in arrs:
            f = fits(vw, B)
            print('%s/%s at w%d (view link %s s %s) <- %s/%s: %s' % (A[0], A[1], i, vw[0], vw[1], B[0], B[1], ('FITS ' + ' '.join('%s/%s' % x for x in sorted(set(f)))) if f else 'no'))
