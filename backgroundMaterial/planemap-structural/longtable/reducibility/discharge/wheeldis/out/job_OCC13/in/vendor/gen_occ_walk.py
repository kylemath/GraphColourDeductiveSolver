"""Job 26 step (iii) (exploratory): the face-walk form of a per-key occurrence module.
Wraps gen_occ_key.gen_key and rewrites its output:
- `Occ` drops `ring_inj` and gets `ring_dinj` (dart injectivity of the ring walk, below the period). The ring
  vertices may repeat (pinches and folds of the third ring).
- `configOcc` builds `FaceWalk.mk_lt` instead of `RingFace.mk_lt` and returns a `ConfigOccW`.
- `colorable_of_occ_dred` concludes through `ConfigOccW.colorable_of_dReducible18` (DCheckOccWalk).
Default: `ring_dinj` is derived per key (`ring_dinj_of`); WALK_ASSUME=1 keeps it as an Occ field instead.
Usage: python3 gen_occ_walk.py KEYFILE LINENO NAMESPACE OUTDIR"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_occ_key as G

def dinj_proof(line, ns):
    """The per-key proof that the ring walk has distinct darts, from the other Occ fields: equal ring darts have the
    same inner apex (the rotation step at the dart's head is a function); different apex labels contradict int_inj;
    one apex label puts two different ring positions at two indices of its full rotation chain (chain_inj)."""
    name, r, m, ra, ia = G.parse(line)
    rot = G.rotation(r, m, ra, ia)
    try: G.gen_occ(name, r, rot, ns)
    except (KeyError, AssertionError): rot = {v: c[::-1] for v, c in rot.items()}
    labels = sorted(rot); idx = {v: i for i, v in enumerate(labels)}
    lab_of = lambda t: t % r + 1
    facts = {}
    for a in labels:
        L = rot[a]; d = len(L)
        for k in range(d): facts[(a, k)] = (L[(k + 1) % d], L[k])
    steps = {}
    for (a, k), (u, y) in facts.items():
        f = "h.r%d_%d" % (idx[a], k)
        steps.setdefault(y, {})[a] = (u, "(nx_tri htri %s).1" % f)
        steps.setdefault(u, {})[y] = (a, "(nx_tri htri %s).2" % f)
    apex = {}
    for t in range(r):
        q, term = steps[lab_of(t + 1)][lab_of(t)]
        assert q > r, (name, t, 'ring chord: apex is a ring vertex')
        apex[t] = (q, term)
    V = lambda u: G.V(u, r, idx)
    A = []; ap = A.append
    ap('/-- The ring walk has distinct darts (derived; replaces `ring_inj`). -/')
    ap('theorem ring_dinj_of {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin %d → Fin n}' % r)
    ap('    {int : Fin %d → Fin n} (h : Occ T ring int) :' % m)
    ap('    ∀ s t, s < %d → t < %d → ρOf ring s = ρOf ring t → ρOf ring (s + 1) = ρOf ring (t + 1) → s = t := by' % (r, r))
    ap('  have key : ∀ s t, s < t → t < %d → ρOf ring s = ρOf ring t → ρOf ring (s + 1) = ρOf ring (t + 1) → False := by' % r)
    ap('    intro s t hst ht e0 e1')
    ap('    have hs : s < %d := by omega' % r)
    ap('    interval_cases s')
    for s_ in range(r):
        ap('    · interval_cases t')
        for t_ in range(s_ + 1, r):
            (qs, Ts), (qt, Tt) = apex[s_], apex[t_]
            ap('      · have fs : Nx T (ρOf ring (%d + 1)) (ρOf ring %d) %s := %s' % (s_, s_, V(qs), Ts))
            ap('        have ft : Nx T (ρOf ring (%d + 1)) (ρOf ring %d) %s := %s' % (t_, t_, V(qt), Tt))
            ap('        rw [e1, e0] at fs')
            ap('        have ea := h.int_inj (nx_func fs ft)')
            if qs != qt:
                ap('        exact absurd ea (by decide)')
            else:
                L = rot[qs]; d = len(L); order = [L[(-j) % d] for j in range(d)]
                I, J = order.index(s_ + 1), order.index(t_ + 1)
                xs = ", ".join(V(u) for u in order)
                ap('        let X : ℕ → Fin n := fun j => ([%s] : List (Fin n)).getD j (ring 0)' % xs)
                ap('        have hc : ∀ j, j + 1 < %d → Nx T (int %d) (X j) (X (j + 1)) := by' % (d, idx[qs]))
                ap('          intro j hj; have hj\' : j < %d := by omega' % (d - 1))
                ap('          interval_cases j')
                ap('          exacts [%s]' % ", ".join("h.r%d_%d" % (idx[qs], (-j - 1) % d) for j in range(d - 1)))
                ap('        exact absurd (chain_inj (by simpa using h.deg %d) (nx_adj_left (hc 0 (by norm_num))) hc %d %d' % (idx[qs], I, J))
                ap('          (by norm_num) (by norm_num) e0) (by norm_num)')
    ap('  intro s t hs ht e0 e1')
    ap('  rcases Nat.lt_trichotomy s t with h\' | h\' | h\'')
    ap('  · exact (key s t h\' ht e0 e1).elim')
    ap('  · exact h\'')
    ap('  · exact (key t s h\' hs e0.symm e1.symm).elim')
    return '\n'.join(A) + '\n\n'

def walk(occ, r, derive=None):
    def rep(a, b):
        nonlocal occ
        assert occ.count(a) == 1, (occ.count(a), a[:60]); occ = occ.replace(a, b)
    rep('import DCheckMirror', 'import DCheckMirror\nimport DCheckOccWalk')
    if derive is None:
        rep('  ring_inj : Function.Injective ring\n',
            '  ring_dinj : ∀ s t, s < %d → t < %d → ρOf ring s = ρOf ring t → ρOf ring (s + 1) = ρOf ring (t + 1) → s = t\n' % (r, r))
    else:   # nothing assumed about the ring beyond the Nx facts: dart injectivity is derived
        rep('  ring_inj : Function.Injective ring\n', '')
        i = occ.index('theorem configOcc'); occ = occ[:i] + derive + occ[i:]
    m = re.search(r'  have hinj : .*?\n    omega\n', occ, re.S); assert m
    occ = occ[:m.start()] + occ[m.end():]
    rep('  have hring : RingFace G %d (ρOf ring) := RingFace.mk_lt (by norm_num) hper hadj hstep hinj' % r,
        '  have hring : FaceWalk G %d (ρOf ring) := FaceWalk.mk_lt (by norm_num) hper hadj hstep %s' % (r, 'h.ring_dinj' if derive is None else '(ring_dinj_of htri h)'))
    occ = occ.replace('ConfigOcc T G %d' % r, 'ConfigOccW T G %d' % r)
    rep('ConfigOcc.colorable_of_dReducible18', 'ConfigOccW.colorable_of_dReducible18')
    occ = occ.replace('injective ring (`ring k` is RSST ring', 'ring with distinct darts, vertices may repeat (`ring k` is RSST ring')
    return occ

if __name__ == '__main__':
    keyfile, lineno, ns, outdir = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    line = [l for l in open(keyfile) if l.strip()][lineno]
    r = int(line.split()[1])
    derive = None if os.environ.get('WALK_ASSUME') == '1' else dinj_proof(line, ns)   # default: derive ring_dinj
    open('%s/%s.lean' % (outdir, ns), 'w').write(walk(G.gen_key(line, ns), r, derive))
