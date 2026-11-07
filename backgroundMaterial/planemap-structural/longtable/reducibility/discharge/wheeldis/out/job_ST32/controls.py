"""ST-32 controls. (1) the two OFFC_SPEC test rows, matched against the kill file with Studio's own st21 rpatN loader + patmatch (out/job31/
st21_check_f2b.py:542-552 and :586-597, copied verbatim below) and the W17 harness's st21_w17.py (same loader; checked separately);
(2) mutation controls through offc_verify.check_line: LINK letter flip, phi image swap, and an entry whose K fails section R."""
import sys, os, collections, random
sys.argv = ['x']; exec(open('out/job_ST32/offc_verify.py').read().split("if __name__ == '__main__':")[0])
KF = 'out/job_ST32/in/offc_K3g_2f4f0f02.txt'
PAT = collections.defaultdict(set)
NSET = {'5': {5}, '6': {6}, '7': {7}, '8': {8}, 'N': {6, 7, 8, 9}}
lines = [l.rstrip('\n') for l in open(KF) if l.strip() and not l.startswith('#')]
for line in lines:
    f = line.split('#')[0].split(); d = int(f[0]); lk, sw = f[1], f[2]
    P = frozenset([('w', i, frozenset(NSET[ch])) for i, ch in enumerate(lk) if ch != '.'] + [('s', i, frozenset(NSET[ch])) for i, ch in enumerate(sw) if ch != '.'])
    PAT[d].add((P, line))
def patmatch(d, w, s):
    hits = []
    for P, line in PAT.get(d, ()):
        for r in range(d):
            for refl in (False, True):
                ok = True
                for kd, i, S in P:
                    if kd == 'w': x_ = w[(r - i) % d] if refl else w[(i + r) % d]
                    else: x_ = s[(r - i - 1) % d] if refl else s[(i + r) % d]
                    if x_ not in S: ok = False; break
                if ok: hits.append(line); break
            else: continue
            break
    return hits
print('== control 1: spec test rows (Studio st21 rpatN semantics)')
for d, L, S, want in ((7, '7567675', '6666655', 'f7_..55756_..5766.'), (7, '8567565', '6678565', 'f8_...55756_...6666.')):
    h = patmatch(d, [int(c) for c in L], [int(c) for c in S])
    names = sorted({x.split('#')[1].split()[1] for x in h})
    print('%d/%s/%s killed by %d line(s): %s; expected entry %s present: %s' % (d, L, S, len(h), names, want, want in names))
    for x in h:
        if want in x: print('   ', x[:160])
print('== control 2: mutations (each must FAIL)')
srcs = Sources(); random.seed(7)
L0 = lines[0]
f = L0.split('#', 1); pat = f[0].split(); meta = f[1]
lk = list(pat[1]); i = next(k for k, c in enumerate(lk) if c in '5678'); lk[i] = '6' if lk[i] != '6' else '7'
mut1 = '%s %s %s #%s' % (pat[0], ''.join(lk), pat[2], meta)
print('LINK flip  ->', check_line(mut1, srcs))
ph = meta.split('phi=')[1].split(); items = ph[0].split(','); a, b = items[0].split('>'), items[1].split('>')
items[0], items[1] = '%s>%s' % (a[0], b[1]), '%s>%s' % (b[0], a[1])
mut2 = '%s #%s' % (f[0].rstrip(), meta.split('phi=')[0] + 'phi=' + ','.join(items))
print('phi swap   ->', check_line(mut2, srcs))
# entry failing section R: search eq_D7_dfast.out for a D entry whose rebuilt K has an edge in no triangle
found = None
for l in open('out/eq_D7_dfast.out'):
    g = l.split()
    if not g or 'D=true' not in l: continue
    mm = re.search(r' r=(\d+) m=(\d+)', l)
    if not mm: continue
    K, why = build_K(g[0], int(mm[1]), int(mm[2]))
    if K and section_R(K[0], K[1]):
        found = (g[0], K, section_R(K[0], K[1])); break
nm, K, rwhy = found
V = K[0]; phi = ','.join('%s>%s' % (('u' if x == ('u',) else '%s%d' % x), ('w%d' % k)) for k, x in enumerate(sorted(V)))
mut3 = '7 ....... ....... # D %s d0=7 file=out/eq_D7_dfast.out md5=8d5e826a phi=%s' % (nm, phi)
print('R-failing entry %s (%s) ->' % (nm, rwhy), check_line(mut3, srcs))
