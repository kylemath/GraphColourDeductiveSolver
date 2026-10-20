"""s37c: explore's two-engine census window kills on binder 7 8666655/5677657 (cyl37.json, from cen54 at 4770a564)
as q-names (PRIVCELL_SPEC part 1, s36g converter rules) with their Part 2 absorption class.
A cen54 window name g7_<u|-><W>_<S>_<14 slots> is written on the row's own frame (w = 8666655, s = 5677657); slot order
p01 p02 p03 p11 p21 p31 p41 ts4/s5/s6 ts6 tp01/s6 tp31/s3 ts3 tp41/s3 tp41/s4.  Pins (marked, not interior):
  F/N  : W char F (w_j = 5, s_{j-1} s_j in, adjacent) or N (w_j != 5, not adjacent): the q-grammar fixes that adjacency
         only through w_j's degree, so w_j is pinned to the row letter;
  part : the structural part's fixed slots (p41 = 5, ts4/s5/s6 = 5) when the window was found in that part;
  label: a private or #k label that needs its parent / apex exact (1.5 determinacy), pinned to the row letter.
A pinned name is sound (it matches only where the row's structure is), but its pinned ring slots are not interior, so
it is not a G3 twoeng name as is.
usage: python3 conv37.py cyl37.json privcell.py OUT.txt"""
import sys, json, collections
CY = json.load(open(sys.argv[1])); exec(open(sys.argv[2]).read().split("if __name__ == '__main__':")[0])
LK = [8, 6, 6, 6, 6, 5, 5]; SV = [5, 6, 7, 7, 6, 5, 7]; D = 7
SLOTS = CY['slots']
CH = {'ts4/s5/s6': (('s', 4), ('s', 5), ('s', 6)), 'ts6': ('#', ('s', 6), 2), 'tp01/s6': (('s', 6), ('p', 0, 1)),
      'tp31/s3': (('p', 3, 1), ('s', 3)), 'ts3': ('#', ('s', 3), 2), 'tp41/s3': (('s', 3), ('p', 4, 1)), 'tp41/s4': (('p', 4, 1), ('s', 4))}
def conv(nm, part_fixed):
    f = nm.split('_'); lk, sw, sl = f[1], f[2], f[3]; assert len(lk) == 8 and len(sw) == 7 and len(sl) == 14, nm
    pins = collections.Counter()
    W = []
    for i, c in enumerate(lk[1:]):
        if c in 'FN': W.append(PC_CH[str(LK[i])]); pins['F/N'] += 1
        else: W.append(None if c == '.' else PC_CH[c])
    S = [None if c == '.' else PC_CH[c] for c in sw]
    req = {SLOTS[k]: int(c) for k, c in enumerate(sl) if c != '.'}
    for k, v in part_fixed.items():
        if k not in req: req[k] = v; pins['part'] += 1
    N = PCName(D, lk[0] == 'u', W, S, {}, {})
    used = set()
    for x in req:
        if x[0] == 'p': used.add(('p', int(x[1]), int(x[2])))
        else:
            ch = CH[x]
            for l in ([ch[1]] if ch[0] == '#' else ch):
                if l[0] == 'p': used.add(l)
            if ch[0] == '#' and N.S[ch[1][1]] is None: N.S[ch[1][1]] = PC_CH[str(SV[ch[1][1]])]; pins['label'] += 1
    for (_, i, k) in used:   # private labels: pin the parent when the side is not forced (1.6) or both apexes touch it
        if N.W[i] is None:
            n = LK[i] - 5; left = k == 1; right = k == n
            if left and right or not (left or right): N.W[i] = PC_CH[str(LK[i])]; pins['label'] += 1
    def plab(l):
        _, i, k = l
        if N.W[i] is not None: return ('p', i, 'L', k)
        return ('p', i, 'L', k) if k == 1 else ('p', i, 'R', LK[i] - 5 + 1 - k)
    for x, v in req.items():
        if x[0] == 'p': N.P[plab(('p', int(x[1]), int(x[2])))[1:]] = PC_CH[str(v)]
        else:
            ch = CH[x]
            N.T[('#', ch[1], ch[2]) if ch[0] == '#' else tuple(plab(l) if l[0] == 'p' else l for l in ch)] = PC_CH[str(v)]
    return pc_norm(N), pins
out = []; cls = collections.Counter(); pinc = collections.Counter(); fail = []
for p in CY['parts']:
    for w in p['windows']:
        try:
            N, pins = conv(w['name'], p['fixed']); cn = pc_canon(N); assert pc_canon(pc_parse(cn)) == cn
            h = pc_class_hint(cn)
        except Exception as e:
            fail.append((w['name'], repr(e))); continue
        st = 'pinned(%s)' % ','.join('%s%d' % kv for kv in sorted(pins.items())) if pins else 'exact'
        cls[(p['part'], h)] += 1; pinc[(p['part'], st.split('(')[0])] += 1
        out.append('%s %s %s %s ring=%d part=%s %s' % (cn, h, w['verdict'], w['name'], w['ring'], p['part'].replace(' ', ','), st))
open(sys.argv[3], 'w').write('# s37c: census window kills of 7 8666655/5677657 as q-names: qname class verdict cen54-name ring part pin-status\n' + '\n'.join(out) + '\n')
print('windows %d, converted %d, failed %d' % (sum(len(p['windows']) for p in CY['parts']), len(out), len(fail)))
for k, v in sorted(cls.items()): print('  class', k, v)
for k, v in sorted(pinc.items()): print('  pins ', k, v)
for f_ in fail[:10]: print('  FAIL', f_)
print('distinct q-names', len({l.split()[0] for l in out}))
