"""ST-10 follow-up: test W18's witness for each of the 14 patterns with Studio's rpatN builder (face-set and RPATN_ROT), every centre and
placement, and decide whether the witness's rotation-preserving pattern MATCHES the target window: a witness pattern Q justifies a
target pattern P when, under one of the 2d rotations / reflections, every fixed position of Q is satisfied by P
(digit = same digit; N = P's letter in {6,7,8,N}; '5' on a non-image w between images = P has 5 there).  Our full-pool comparison
only looked for EQUAL patterns (Q == P), which is the restriction this test removes."""
import os, sys, collections
os.environ['RPATN_ROT'] = '1'; sys.argv = ['rpatN_studio.py']
M = {'__name__': 'w14', '__file__': os.path.abspath('out/job31/rpatN_studio.py')}
exec(open('out/job31/rpatN_studio.py').read().split("if __name__ == '__main__':")[0], M)
R = 'loop/studio/opus_check/f2b041/keep95p131f/rpatN3_rot/'
pool = {l.split()[0]: l.strip() for fn in (R + 'keeppool_kc.txt', R + 'rsst_kc.txt') for l in open(fn) if l.strip()}
def pats(line, rot):
    M['ROT'] = rot; nm, m, g, E, tri = M['parse'](line)
    if rot: M['CUR']['rot'] = M['RC'].kc_rotation(line)
    out = set()
    for c in [c for c in range(m) if 7 <= g[c] <= 17]:
        for d, L, S in M['embeddings'](m, g, E, tri, c): out.add((d, ''.join(L), ''.join(S)))
    return out
def sat(q, p):
    if q == '.': return True
    if q == 'N': return p in '678N'
    return q == p
def justifies(Q, P):
    d, L, S = P; dq, Lq, Sq = Q
    if dq != d: return False
    for refl in (False, True):
        for r in range(d):
            if refl: L2 = [Lq[(r - i) % d] for i in range(d)]; S2 = [Sq[(r - i - 1) % d] for i in range(d)]
            else: L2 = [Lq[(i + r) % d] for i in range(d)]; S2 = [Sq[(i + r) % d] for i in range(d)]
            if all(sat(a, b) for a, b in zip(L2, L)) and all(sat(a, b) for a, b in zip(S2, S)): return True
    return False
rows = [l.rstrip('\n').split('\t') for l in open(R + 'in/rpatN3_extra14_W18witness.tsv') if l.strip() and not l.startswith('#')]
with open(R + 'extra14_W18witness_rot.tsv', 'w') as f:
    f.write('# pattern\tsource\tW18 witness\tface-set: equal / matching\trotation-preserving: equal / matching\tmatching rotation-preserving witness pattern(s)\tverdict\n')
    for p, srcn, w in rows:
        t = p.split(); P = (int(t[0]), t[1], t[2]); line = pool.get(w)
        if not line: f.write('%s\t%s\t%s\tnot in pool\t\t\t-\n' % (p, srcn, w)); continue
        F = pats(line, False); Rr = pats(line, True)
        fe = any(q == P or justifies(q, P) and justifies(P, q) for q in F); fm = [q for q in F if justifies(q, P)]
        re_ = any(justifies(q, P) and justifies(P, q) for q in Rr); rm = [q for q in Rr if justifies(q, P)]
        v = '(a) rotation-preserving witness exists (matching, not equal)' if rm and not re_ else ('(a) equal pattern' if re_ else '(b) rejected: ' + ('face-set only' if fm else 'no matching embedding even face-set'))
        f.write('%s\t%s\t%s\t%s / %d\t%s / %d\t%s\t%s\n' % (p, srcn, w, fe, len(fm), re_, len(rm), ' ; '.join('%d %s %s' % q for q in sorted(rm)[:3]) or '-', v))
        print(p, w, v)
