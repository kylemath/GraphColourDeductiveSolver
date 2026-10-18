"""Job 26 step (iii) (exploratory): the face-walk form of a per-key occurrence module.
Wraps gen_occ_key.gen_key and rewrites its output:
- `Occ` drops `ring_inj` and gets `ring_dinj` (dart injectivity of the ring walk, below the period). The ring
  vertices may repeat (pinches and folds of the third ring).
- `configOcc` builds `FaceWalk.mk_lt` instead of `RingFace.mk_lt` and returns a `ConfigOccW`.
- `colorable_of_occ_dred` concludes through `ConfigOccW.colorable_of_dReducible18` (DCheckOccWalk).
Usage: python3 gen_occ_walk.py KEYFILE LINENO NAMESPACE OUTDIR"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_occ_key as G

def walk(occ, r):
    def rep(a, b):
        nonlocal occ
        assert occ.count(a) == 1, (occ.count(a), a[:60]); occ = occ.replace(a, b)
    rep('import DCheckMirror', 'import DCheckMirror\nimport DCheckOccWalk')
    rep('  ring_inj : Function.Injective ring\n',
        '  ring_dinj : ∀ s t, s < %d → t < %d → ρOf ring s = ρOf ring t → ρOf ring (s + 1) = ρOf ring (t + 1) → s = t\n' % (r, r))
    m = re.search(r'  have hinj : .*?\n    omega\n', occ, re.S); assert m
    occ = occ[:m.start()] + occ[m.end():]
    rep('  have hring : RingFace G %d (ρOf ring) := RingFace.mk_lt (by norm_num) hper hadj hstep hinj' % r,
        '  have hring : FaceWalk G %d (ρOf ring) := FaceWalk.mk_lt (by norm_num) hper hadj hstep h.ring_dinj' % r)
    occ = occ.replace('ConfigOcc T G %d' % r, 'ConfigOccW T G %d' % r)
    rep('ConfigOcc.colorable_of_dReducible18', 'ConfigOccW.colorable_of_dReducible18')
    occ = occ.replace('injective ring (`ring k` is RSST ring', 'ring with distinct darts, vertices may repeat (`ring k` is RSST ring')
    return occ

if __name__ == '__main__':
    keyfile, lineno, ns, outdir = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    line = [l for l in open(keyfile) if l.strip()][lineno]
    r = int(line.split()[1])
    open('%s/%s.lean' % (outdir, ns), 'w').write(walk(G.gen_key(line, ns), r))
