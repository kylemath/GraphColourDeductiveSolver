"""s52c final C-cover for A83 l3q + rpatN3 + fb6 (fbdir=6 fbcap=3) with the 128 exname hold-outs (s44 sol_q44fbA83, upper FEASIBLE at
0.105883918328). Copy of s46c/final46.py, parameterised: tables s52c_tab, ex_A83, reg_A83 k3x_C, J from j_A83.txt, exname s40f/exname_rm128.txt,
Lean status adds CCover2 (origin/main out/lean_ccover2/f2acc3e7/entries.txt: the 6 s46c not-in-Lean k3x_C names; format idx name X, name = field 2).
Inputs: cc/vrows_cover.txt.gz (ccover52.py), SC/s52c_tab/v_<name>.txt (batch2), the conservation cells of upper_noC.log.
Outputs: ccover_A83.txt, sole_A83.txt, vrows_cover_A83.txt.gz, entries_A83.txt, ckeep_A83.txt, ccover_A83_summary.txt."""
import gzip, os, re, collections
O = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(O)
SC = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad'; T = SC + '/s52c_tab'
EX = SC + '/ex_A83/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/k44/rsst_verdicts.txt'
# ---- metadata: ring size, Lean status, source
RING, SRC = {}, {}
for l in open(O + '/cc/entries_used.txt'):
    if l.startswith('#'): continue
    f = l.split(); RING[f[0]] = f[1]; SRC[f[0]] = f[5]
for l in open(EX):
    m = re.match(r'^(rsst\S+) r=(\d+)', l)
    if m: RING[m.group(1)] = m.group(2); SRC[m.group(1)] = 'RSST C2cons (k44/rsst_verdicts)'
for l in open(os.path.join(B, '..', '..', '..', '..', 'studio17', 'wheels17_verdicts.txt')):
    f = l.split()
    if f and f[0].startswith('c6_') and len(f) > 2 and f[2] == 'C': RING[f[0]] = f[1]; SRC[f[0]] = 'studio17 C 6-wheel'
LEAN = {}
for fn, tag, col in (('lean_CXRing_entries.txt', 'CXRing', 2), ('lean_CXInt_entries.txt', 'CXInt', 2), ('lean_CCover_entries.txt', 'CCover', 2), ('lean_CCover2_entries.txt', 'CCover2', 1)):
    for l in open(os.path.join(O, fn)):
        f = l.split()
        if len(f) >= 3: LEAN.setdefault(f[col], tag)   # s46c: first list wins (CXRing, CXInt, CCover); s52c: then CCover2 (name in field 2)
for w in ('c6_556577', 'c6_566577'): LEAN[w] = 'CWheels'   # dcheck/CWheels.lean (Studio Job 21): exactly these two wheels
for n, s_ in list(SRC.items()):
    if s_ == 'k42map_C_cons.cfast' and RING.get(n) == '0': RING[n] = 'derived'   # r=0 placeholder in k42map_C_cons.cfast (C patterns derived from RSST / explore C configurations)
def lean(n): return LEAN.get(n, 'notLean')
# k3x_C names: everything in the A83 registry
K3X = set(l.split()[0] for l in open(B + '/s33z/reg_A83/k3x_C_A83.cfast') if ' r=' in l and not l.startswith(' '))
EXN = set(l.split()[0] for l in open(B + '/s40f/exname_rm128.txt') if l.strip() and not l.startswith('#'))
# ---- rows and covers
rows, cov = [], []
for l in gzip.open(O + '/cc/vrows_cover.txt.gz', 'rt'):
    a, b = l.split('|'); f = a.split(); rows.append((f[0], f[1], f[2], f[3])); cov.append(set(b.split()))
idx = {(r[0], r[1], r[2]): i for i, r in enumerate(rows)}
tabn = [l.split()[0] for l in open(O + '/tabnames.txt') if not l.startswith('#')]
for n in tabn:
    still = set()
    for l in open('%s/v_%s.txt' % (T, n)):
        f = l.split(); still.add((f[0], f[3], f[4]))
    assert still <= set(idx), n
    for k, i in idx.items():
        if k not in still: cov[i].add(n)
# conservation cells (reported in upper_noC.log; covered by the studio17 C wheel with that canonical link)
def canon(w):
    w = tuple(w); n = len(w)
    return min(min(s[k:] + s[:k] for k in range(n)) for s in (w, w[::-1]))
CONS = []
for l in open(O + '/upper_noC.log'):
    m = re.match(r'^\s+cons off: L=\(([\d, ]+)\) five=\S+ worst (\S+)', l)
    if m:
        L = ''.join(map(str, canon(int(x) for x in m.group(1).split(',')))); w = 'c%d_%s' % (len(L), L)
        assert w in SRC and SRC[w] == 'studio17 C 6-wheel' or w.startswith('c5_'), (w, l)
        rows.append(('cons', L, '-', m.group(2))); cov.append({w}); CONS.append(w)
N = len(rows); unc = [i for i in range(N) if not cov[i]]
byent = collections.Counter(n for c in cov for n in c)
sole = collections.Counter(next(iter(c)) for c in cov if len(c) == 1)
S = set(sole)
left = [i for i in range(N) if cov[i] and not (cov[i] & S)]
G = []; rem = set(left)
while rem:
    t = collections.Counter(n for i in rem for n in cov[i])
    n, k = max(t.items(), key=lambda x: (x[1], lean(x[0]) != 'notLean', x[0] in K3X, x[0]))   # ties: Lean-proved first, then registry k3x_C
    G.append((n, k)); rem = {i for i in rem if n not in cov[i]}
# J: rows no single C entry kills (unc) can be killed only by several kill6/l3q table kills together; j_A83.txt lists the table names
# aug52.sh rounds (one table name added at a time to S + G) found to complete the cover (empty if the S + G check is FEASIBLE).
J = [l.split()[0] for l in open(O + '/j_A83.txt') if l.strip() and not l.startswith('#')] if os.path.exists(O + '/j_A83.txt') else []
J = [n for n in J if n not in S and n not in {g for g, k in G}]
cover = [n for n in sorted(S, key=lambda n: (-sole[n], n))] + [n for n, k in G] + J
assert not (set(cover) & EXN), set(cover) & EXN   # held-out names never in the cover
def kind(n):
    return 'k3x_C' if n in K3X else ('RSST' if n.startswith('rsst') else ('C6wheel' if n.startswith('c6_') else ('C7wheel' if n.startswith('c7_') else 'cpat-other')))
with gzip.open(O + '/vrows_cover_A83.txt.gz', 'wt') as f:
    f.write('# every violated receiver row (d link sv excess) or conservation cell with all C out, and the C entries covering it\n')
    for r, c in zip(rows, cov): f.write('%s %s %s %s | %s\n' % (r + (' '.join(sorted(c)) if c else 'JOINT (no single C entry; killed only by several kill6/l3q table kills together)',)))
with open(O + '/entries_A83.txt', 'w') as f:
    f.write('# every C entry covering >= 1 violated row: name ring lean kind #covered #sole source\n')
    for n, k in byent.most_common(): f.write('%s %s %s %s %d %d %s\n' % (n, RING.get(n, '?'), lean(n), kind(n), k, sole.get(n, 0), SRC.get(n, '?')))
with open(O + '/sole_A83.txt', 'w') as f:
    f.write('# sole-cover C entries (the only cover of >= 1 violated row): name ring lean kind #rows-it-alone-covers #rows-covered\n')
    for n in cover[:len(S)]: f.write('%s %s %s %s %d %d\n' % (n, RING.get(n, '?'), lean(n), kind(n), sole[n], byent[n]))
with open(O + '/ccover_A83.txt', 'w') as f:
    f.write('# greedy minimum C cover, A83 l3q + rpatN3 + fb6 + 128 exname upper (sol_q44fbA83): sole entries (S) first, then greedy (G<k>, #new rows)\n# name ring lean kind role\n')
    for n in cover[:len(S)]: f.write('%s %s %s %s S\n' % (n, RING.get(n, '?'), lean(n), kind(n)))
    for i, (n, k) in enumerate(G): f.write('%s %s %s %s G%d new=%d\n' % (n, RING.get(n, '?'), lean(n), kind(n), i + 1, k))
    for n in J: f.write('%s %s %s %s J (joint table kills)\n' % (n, RING.get(n, '?'), lean(n), kind(n)))
with open(O + '/ckeep_A83.txt', 'w') as f:
    for n in cover: f.write(n + '\n')
rg = collections.defaultdict(collections.Counter)
for n in cover: rg[RING.get(n, '?')][lean(n)] += 1
with open(O + '/ccover_A83_summary.txt', 'w') as f:
    f.write('violated rows/cells with all C out: %d (%s)\n' % (N, dict(collections.Counter(r[0] for r in rows))))
    f.write('uncovered by any C entry: %d\n' % len(unc))
    f.write('C entries covering >= 1 row: %d\n' % len(byent))
    f.write('sole-cover entries: %d; rows left after the sole set: %d; greedy adds %d; joint-table additions %d; cover total %d\n' % (len(S), len(left), len(G), len(J), len(cover)))
    f.write('cover by kind: %s\n' % dict(collections.Counter(kind(n) for n in cover)))
    f.write('cover by Lean status: %s\n' % dict(collections.Counter(lean(n) for n in cover)))
    f.write('sole by Lean status: %s\n' % dict(collections.Counter(lean(n) for n in S)))
    f.write('cover by ring (lean status counts):\n')
    for r in sorted(rg, key=lambda x: int(x) if x.isdigit() else 0): f.write('  ring %s: %d  %s\n' % (r, sum(rg[r].values()), dict(rg[r])))
    f.write('ring 14-16 cover entries:\n')
    for n in cover:
        if RING.get(n, '?') in ('14', '15', '16'): f.write('  %s r=%s %s %s %s sole=%d cov=%d\n' % (n, RING[n], lean(n), kind(n), 'S' if n in S else ('J' if n in J else 'G'), sole.get(n, 0), byent[n]))
print(open(O + '/ccover_A83_summary.txt').read())
