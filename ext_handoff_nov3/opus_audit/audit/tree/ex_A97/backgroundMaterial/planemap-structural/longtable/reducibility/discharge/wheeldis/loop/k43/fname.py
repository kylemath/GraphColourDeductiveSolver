"""Round 43: f-names (gen.canon_key, dihedral-canonical f<d>_<link>_<s>) for a8_ windows, and renamed copies of kc /
cfast output blocks so that Job 30's twoeng.py (names ^[epf]<d>_) picks them up.
usage: python3 fname.py NAME [NAME ...]  -> prints 'a8name fname'; with --files writes kills.txt/kills_kc.out/kills_cf.cfast"""
import sys, os, re
H = os.path.dirname(os.path.abspath(__file__))
def canon_key(d, lk, sv):     # copy of gen.py's canon_key (s_i between w_i and w_i+1)
    best = None
    for refl in (0, 1):
        if refl: l2 = lk[::-1]; s2 = ''.join(sv[(-i - 2) % d] for i in range(d))
        else: l2, s2 = lk, sv
        for k in range(d):
            c = (l2[k:] + l2[:k], s2[k:] + s2[:k])
            if best is None or c < best: best = c
    return (d,) + best
def fname(a8):
    _, l, s = a8.split('_'); assert l[0] == 'u'
    k = canon_key(8, l[1:], s); return 'f8_%s_%s' % (k[1], k[2])
args = [a for a in sys.argv[1:] if a != '--files']
for a in args: print(a, fname(a))
if '--files' in sys.argv:
    ren = {a: fname(a) for a in args}
    def sub(text):
        for a, f in ren.items(): text = text.replace(a + ' ', f + ' ')
        return text
    def blocks(fn):
        out, cur = [], None
        for l in open(os.path.join(H, fn)):
            if l.strip() and not l.startswith(' '): cur = l.split()[0]
            if cur in ren: out.append(l)
        return ''.join(out)
    inp = ''.join(l for l in open(os.path.join(H, 'win43_A.txt')) if l.split()[0] in ren)
    open(os.path.join(H, 'kills.txt'), 'a').write(sub(inp))
    open(os.path.join(H, 'kills_kc.out'), 'a').write(sub(blocks('A_kcc.out')))
    open(os.path.join(H, 'kills_cf.cfast'), 'a').write(sub(blocks('A_cf.out')))
