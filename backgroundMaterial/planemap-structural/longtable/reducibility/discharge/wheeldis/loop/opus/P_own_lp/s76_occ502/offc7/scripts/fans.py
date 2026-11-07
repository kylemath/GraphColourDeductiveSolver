"""Lean-form RingLinked (with fan lists) on the 55 kc keys: compute fan t as a path in the seesFace graph and
check RingLinked exactly as OffcOcc.lean states it."""
import sys, os, itertools
P = sys.argv[1]; kcf = sys.argv[2]; out = sys.argv[3]
sys.path.insert(0, os.path.join(P, 's74_leanglue'))
import gen_occ_kc as K

def kc_rot(canon):
    rot = K.bridge_rot(K.G.gen_key(canon, 'X'))
    return {a: [(('l', i) if k == 'inl' else ('r', i)) for k, i in rot[a]] for a in rot}

def sl(rot, x, k): L = len(rot[x]); return rot[x][k % L]

def sees(rot, a, b, t):
    ra = range(len(rot[a])); rb = range(len(rot[b]))
    return any((sl(rot, a, k + 1) == ('l', b) and sl(rot, a, k) == ('r', t) and
                any(sl(rot, b, j) == ('l', a) and sl(rot, b, j + 1) == ('r', t) for j in rb)) or
               (sl(rot, a, k + 1) == ('r', t) and sl(rot, a, k) == ('l', b) and
                any(sl(rot, b, j) == ('r', t) and sl(rot, b, j + 1) == ('l', a) for j in rb)) for k in ra)

def ring_linked(r, rot, fan):
    m = len(rot)
    if not 0 < r: return False
    for a in range(m):
        if len(set(rot[a])) != len(rot[a]): return False
        if any(x[0] == 'r' and not x[1] < r for x in rot[a]): return False
    for t in range(r):
        f = fan[t]
        if not f: return False
        if any((('r', t) in rot[a]) != (a in f) for a in range(m)): return False
        if not all(sees(rot, p, q, t) for p, q in zip(f, f[1:])): return False
    return True

def find_fan(rot, t):
    occ = [a for a in rot if ('r', t) in rot[a]]
    for perm in itertools.permutations(occ):
        if all(sees(rot, p, q, t) for p, q in zip(perm, perm[1:])): return list(perm)
    return None

res = []
for l in open(kcf):
    name, _, canon = l.rstrip('\n').split('\t')
    r = int(canon.split()[1]); rot = kc_rot(canon)
    fan = {t: find_fan(rot, t) for t in range(r)}
    ok = all(fan[t] is not None for t in range(r)) and ring_linked(r, rot, fan)
    # control: reversing one fan of length >= 3 keeps it a path; dropping a member must fail
    t3 = [t for t in range(r) if fan[t] and len(fan[t]) >= 2]
    ctrl = None
    if t3:
        f2 = dict(fan); f2[t3[0]] = fan[t3[0]][1:]; ctrl = ring_linked(r, rot, f2)
    res.append((name, r, ok, ctrl, ';'.join(','.join(map(str, fan[t] or [])) for t in range(r))))
with open(out, 'w') as o:
    o.write('name\tr\tRingLinked\tfan (t = 0..r-1, ;-separated)\n')
    for name, r, ok, ctrl, fs in res: o.write('%s\t%d\t%s\t%s\n' % (name, r, ok, fs))
print('RingLinked true:', sum(x[2] for x in res), 'of', len(res), '; drop-a-member controls failing:',
      sum(1 for x in res if x[3] is False), 'of', sum(1 for x in res if x[3] is not None))
