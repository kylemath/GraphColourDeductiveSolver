# B3: for a window that kills the private of a link 6 (kill6 type): the kill6 key window (u if U = 7, w_{j-2..j+2},
# s_{j-2..j+1}), the key letters, and the slots read outside it (what an A' wider kill6 mask has to read); q-name.
import sys, re
def ap(nm):
    m = re.match(r'b(\d+)_([u-])([0-9.]+)_([0-9.]+)_p(\d)(\d)(\d)$', nm)
    d = int(m.group(1)); uin = m.group(2) == 'u'; lk, sv = m.group(3), m.group(4); j, k, L = int(m.group(5)), int(m.group(6)), int(m.group(7))
    U = min(d, 9)
    S = ({'u'} if uin else set()) | {'w%d' % i for i in range(d) if lk[i] != '.'} | {'s%d' % i for i in range(d) if sv[i] != '.'}
    K = ({'u'} if U == 7 else set()) | {'w%d' % ((j + o) % d) for o in (-2, -1, 0, 1, 2)} | {'s%d' % ((j + o) % d) for o in (-2, -1, 0, 1)}
    gl = lambda x: lk[int(x[1:])] if x[0] == 'w' else sv[int(x[1:])]
    ws = ''.join(lk[(j + o) % d] for o in (-2, -1, 1, 2)); ss = ''.join(sv[(j + o) % d] for o in (-2, -1, 0, 1))
    out = sorted(S - K)
    grp = [''] * d; grp[j] = str(L)
    q = 'q%d%s_%s_%s_%s' % (d, 'u' if uin else '-', lk, sv, ':'.join(grp))
    return 'U=%d w(j-2,j-1,j+1,j+2)=%s s(j-2,j-1,j,j+1)=%s private=%d' % (U, ws, ss, L), ','.join('%s=%s' % (x, gl(x)) for x in out) or '(none: plain kill6 entry)', q
if __name__ == '__main__':
    for nm in sys.argv[1:]: print(nm, '|', *ap(nm), sep=' ')
