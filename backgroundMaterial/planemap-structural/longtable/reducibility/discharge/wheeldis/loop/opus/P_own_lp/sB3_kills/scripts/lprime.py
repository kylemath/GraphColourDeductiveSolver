# B3: for a window that kills one private of a link 7: the l3q side it serves (sigma), the l3q payee window R (RELAY_SPEC 21.4)
# and the slots it reads outside R (the extra key an L' row-level mask needs); plus a q-name (PRIVCELL grammar, not canonicalised).
import sys, re
def lp(nm):
    m = re.match(r'b7_([u-])([0-9.]{7})_([0-9.]{7})_p(\d)(\d)(\d)$', nm)
    uin, lk, sv, j, k, L = m.group(1) == 'u', m.group(2), m.group(3), int(m.group(4)), int(m.group(5)), int(m.group(6))
    S = ({'u'} if uin else set()) | {'w%d' % i for i in range(7) if lk[i] != '.'} | {'s%d' % i for i in range(7) if sv[i] != '.'}
    sg = 1 if k == 2 else -1
    ap = 's%d' % (j if sg == 1 else (j - 1) % 7); o = 's%d' % ((j - 1) % 7 if sg == 1 else j)
    R = {'u', 'w%d' % j, ap, o} | {'w%d' % ((j + i * sg) % 7) for i in (1, 2, 3, 4)}
    grp = [''] * 7; grp[j] = ''.join(str(L) if kk == k else '.' for kk in (1, 2))
    q = 'q7%s_%s_%s_%s' % ('u' if uin else '-', lk, sv, ':'.join(grp))
    gl = lambda x: lk[int(x[1])] if x[0] == 'w' else sv[int(x[1])]
    key = '(sigma=%+d, c,w2,w3,w4=%s, a=%s, o=%s)' % (sg, ''.join(gl('w%d' % ((j + i * sg) % 7)) for i in (1, 2, 3, 4)), gl(ap), gl(o))
    extra = sorted(S - R)
    return sg, key, extra, ','.join('%s=%s' % (x, gl(x)) for x in extra), q
if __name__ == '__main__':
    for nm in sys.argv[1:]:
        sg, key, extra, ex, q = lp(nm); print(nm, '| side', key, '| outside R:', ex, '|', q)
