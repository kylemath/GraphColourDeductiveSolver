"""B8 (exploratory): out-of-sample test of the 2-ball family.

A census 2-ball key is "in R" iff it is W12 (wheel), S66 (66666 with flat second ring), J9 (Job 9 D-reducible 66666)
or D=true in some out/dres-*.txt.  The family R_train is built from census orders TRAIN only (several recipes below),
and tested on census orders TEST and on witness files (constructed graphs, never in the census).

Recipes for R_train (all include W12 + S66 + J9, which were fixed before any census data was seen):
  all    : every D-reducible key that occurs anywhere in a TRAIN-order census graph
  fail   : every D-reducible key that occurs in an H1-failing TRAIN graph (the procedure that built EXT, restricted)
  cover  : a greedy minimum set of D-reducible keys hitting every H1-failing TRAIN graph (the 'cover.txt' procedure)
Usage: oos.py TRAIN_MAX [WITFILE...]    (TRAIN = orders <= TRAIN_MAX, TEST = orders > TRAIN_MAX)"""
import sys, os, gzip, json, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ball, h0

TMAX = int(sys.argv[1]); WIT = sys.argv[2:]
ext = h0.load_ext(); j9 = h0.load_j9()


def base(ws, ks):
    if ws in h0.W12: return True
    if ks is None: return False
    key = ball.key_from_str(ks)
    if ws == '66666':
        if all(d <= 6 for b in key for d in b[1] + (b[2],)): return True
        nm = ball.key_to_66666_name(key)
        if j9.get(nm): return True
    return False


def dstat(ks):
    """True/False if tested, None if untested"""
    if ks in ext: return ext[ks]
    nm = ball.key_to_66666_name(ball.key_from_str(ks))
    if nm in j9: return j9[nm]
    return None


graphs = []   # (name, n, [(ws, ks)])
for fn in sorted(glob.glob(os.path.join(HERE, 'out/scan-*.jsonl.gz'))):
    for line in gzip.open(fn, 'rt'):
        g = json.loads(line)
        graphs.append((g['g'], g['n'], [(w, ks) for v, w, ks, st in g['h']]))

untested = collections.Counter()
for name, n, H in graphs:
    for w, ks in H:
        if not base(w, ks) and ks is not None and dstat(ks) is None: untested[ball.ring_size(ball.key_from_str(ks))] += 1
print('census holes with untested key (not W12/S66/J9), by ring:', sorted(untested.items()))

train = [g for g in graphs if g[1] <= TMAX]; test = [g for g in graphs if g[1] > TMAX]
h1fail_train = [g for g in train if not any(base(w, ks) for w, ks in g[2])]
fam = {}
fam['all'] = {ks for _, _, H in train for w, ks in H if ks and not base(w, ks) and dstat(ks)}
fam['fail'] = {ks for _, _, H in h1fail_train for w, ks in H if ks and dstat(ks)}
left = {g[0]: {ks for w, ks in g[2] if ks and dstat(ks)} for g in h1fail_train}; cov = set()
while left:
    c = collections.Counter(k for s in left.values() for k in s)
    if not c: break
    k = c.most_common(1)[0][0]; cov.add(k); left = {a: s for a, s in left.items() if k not in s}
fam['cover'] = cov
fam['none(H1)'] = set()


def hit(H, F):
    return any(base(w, ks) or (ks in F) for w, ks in H)


print('TRAIN orders <= %d: %d graphs, %d H1-failing' % (TMAX, len(train), len(h1fail_train)))
print('%-9s %7s | %s' % ('recipe', '|EXT|', 'test failures by order (test orders > %d)' % TMAX))
for r, F in fam.items():
    per = collections.defaultdict(lambda: [0, 0]); ex = None
    for name, n, H in test:
        per[n][0] += 1
        if not hit(H, F):
            per[n][1] += 1; ex = ex or name
    tot = [sum(a for a, b in per.values()), sum(b for a, b in per.values())]
    print('%-9s %7d | %s | total %d/%d = %.4f  first %s' % (r, len(F), '  '.join('%d:%d/%d' % (n, per[n][1], per[n][0])
          for n in sorted(per)), tot[1], tot[0], tot[1] / max(tot[0], 1), ex))
    # train-sample check (in-sample)
    tf = sum(1 for name, n, H in train if not hit(H, F))
    print('%-9s         in-sample (train) failures %d/%d' % ('', tf, len(train)))
    # failure decomposition: test graphs missed by recipe but hit by a D-reducible key not in F (new key) or untested
    if r != 'none(H1)':
        why = collections.Counter()
        for name, n, H in test:
            if hit(H, F): continue
            if any(ks and dstat(ks) for w, ks in H): why['has a D-reducible key not in R_train'] += 1
            elif any(ks and dstat(ks) is None and not base(w, ks) for w, ks in H): why['only untested keys could help'] += 1
            else: why['no D-reducible 2-ball at all'] += 1
        print('%-9s         why test graphs fail: %s' % ('', dict(why)))

for fn in WIT:
    print('== witnesses', os.path.basename(fn))
    for r, F in fam.items():
        tot = 0; miss = 0; truew = 0; inclass = 0
        for line in open(fn):
            if not line.strip(): continue
            name, rot = ball.parse_line(line); tot += 1
            H = []
            for v in range(len(rot)):
                if len(rot[v]) != 5: continue
                w, key, st = ball.ball_at(rot, v)
                H.append((''.join(map(str, ball.wheel_canon(w))), ball.key_str(key) if key else None))
            if not hit(H, F):
                miss += 1
                if not any(ks and dstat(ks) is not False and not base(w, ks) for w, ks in H): truew += 1
        print('  %-9s |EXT|=%6d  R_train-free %d/%d   (of which every hole tested non-D-reducible: %d)' % (
            r, len(F), miss, tot, truew))
