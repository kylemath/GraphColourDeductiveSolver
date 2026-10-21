"""EXPLORE round 60: the pair-census grid per receiver row and link 7, from pair60's containment table and kpriv's engine
kills.  Cell (a, b) = w_k's privates p_k_1 (next to s_k) and p_k_2 (next to s_(k-1)), 9 = >= 9.  R = a registry
configuration inside the split row's closed vertices, X = a 2026 one, E = a two-engine kpriv window matches, o = open.
usage: python3 grid60.py PAIR60OUT KPRIV"""
import sys, re
P, K = sys.argv[1:3]
st = {}
for l in open(P):
    m = re.match(r'^(\S+) w(\d) priv(\d)(\d): (.*)$', l.strip())
    if not m: continue
    row, k, a, b, rest = m.group(1), int(m.group(2)), m.group(3), m.group(4), m.group(5)
    st[(row, k, a, b)] = 'R' if 'registry inside' in rest else 'X' if '2026 set inside' in rest else 'o'
eng = []
for l in open(K):
    if not l.startswith('g') or 'tag=D2' not in l and 'tag=C2' not in l: continue
    m = re.match(r'^g(\d+)_(-?)([0-9.]+)_([0-9.]+)_w(\d):([0-9.]{2}) ', l); eng.append((m.group(3), m.group(4), int(m.group(5)), m.group(6), m.group(2)))
def match(p, w): return all(x == '.' or x == y for x, y in zip(p, w))
rows = sorted({(r, k) for r, k, a, b in st}, key=lambda t: (list(dict.fromkeys(r for r, k, a, b in st)).index(t[0]), t[1]))
for row, k in rows:
    lk, sv = row.split('/')
    print('%s w%d   b=5 6 7 8 9   (a = private next to s%d, b = next to s%d)' % (row, k, k, (k - 1) % len(lk)))
    cnt = {}
    for a in '56789':
        line = []
        for b in '56789':
            s = st.get((row, k, a, b), '?')
            if s == 'o' and any(kk == k and match(pl, lk) and match(ps, sv) and match(pp, a + b) for pl, ps, kk, pp, mk in eng): s = 'E'
            line.append(s); cnt[s] = cnt.get(s, 0) + 1
        print('   a=%s       %s' % (a, ' '.join(line)))
    print('   dead %d of 25 (R %d, X %d, E %d), open %d' % (25 - cnt.get('o', 0) - cnt.get('?', 0), cnt.get('R', 0), cnt.get('X', 0), cnt.get('E', 0), cnt.get('o', 0)))
