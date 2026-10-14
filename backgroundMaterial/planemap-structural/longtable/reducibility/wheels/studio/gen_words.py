"""Studio Job 8 (exploratory): the hole-wheel configurations to test.  Words = Track B's 59 + 19 hole types
(discharge2-frameonly.json) and every link word at a degree-5 hole of the order-33 frame census (eval-33 field w).
Words are cyclic, up to rotation and reflection; a letter '8+' (degree >= 8) is instantiated as 8 and as 9.
Writes words.json (canonical word -> sources) and configs_wheels.txt (WheelMain format), using wheels.py's wheel()."""
import json, gzip, re, itertools, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
W = '/Users/kylemathewson/GraphColourDeductiveSolver/SolvingFrameworkPlan/docs/working'

def letters(w): return re.findall(r'8\+|\d', w)
def canon(L):
    c = [tuple(L[i:] + L[:i]) for i in range(len(L))]; L2 = L[::-1]
    c += [tuple(L2[i:] + L2[:i]) for i in range(len(L))]
    return min(c)

src = {}
d = json.load(open(W + '/TrackB/out/discharge2-frameonly.json'))
for w in d['S_allowed']: src.setdefault(canon(letters(w)), set()).add('TrackB-S')
for w in d['S_forbidden']: src.setdefault(canon(letters(w)), set()).add('TrackB-555/565')
cnt = {}
for l in gzip.open(W + '/Census33/out/eval-33.jsonl.gz', 'rt'):
    r = json.loads(l)
    for h, v in r['holes'].items():
        k = canon(letters(v['w'])); src.setdefault(k, set()).add('census33'); cnt[k] = cnt.get(k, 0) + 1

def wheel(word):   # identical to ../wheels.py wheel()
    ring = []
    for i, dd in enumerate(word):
        for p in range(dd - 5): ring.append(('p', i, p))
        ring.append(('s', i))
    pos = {v: k for k, v in enumerate(ring)}
    ringadj = [[] for _ in range(6)]; intadj = [[] for _ in range(6)]
    for i, dd in enumerate(word):
        a = 1 + i
        ringadj[a] = [pos[('s', (i - 1) % 5)]] + [pos[('p', i, p)] for p in range(dd - 5)] + [pos[('s', i)]]
        intadj[a] = [0, 1 + (i + 1) % 5, 1 + (i - 1) % 5]
    intadj[0] = [1, 2, 3, 4, 5]
    return len(ring), ringadj, intadj, 6

inst = {}
for k in src:
    opts = [[8, 9] if x == '8+' else [int(x)] for x in k]
    for c in itertools.product(*opts):
        cw = canon([str(x) for x in c]); inst.setdefault(''.join(cw), set()).add(''.join(k))
out = open(os.path.join(HERE, 'configs_wheels.txt'), 'w')
for w in sorted(inst, key=lambda w: (sum(map(int, w)), w)):
    r, ra, ia, m = wheel([int(c) for c in w])
    fmt = lambda L: ';'.join(','.join(map(str, x)) if x else '-' for x in L)
    out.write('w%s %d %d %s %s\n' % (w, r, m, fmt(ra), fmt(ia)))
json.dump({''.join(k): dict(sources=sorted(v), census33_holes=cnt.get(k, 0)) for k, v in src.items()}, open(os.path.join(HERE, 'words.json'), 'w'), indent=0)
json.dump({w: sorted(v) for w, v in inst.items()}, open(os.path.join(HERE, 'instances.json'), 'w'), indent=0)
import collections
print('words', len(src), 'instances', len(inst), 'by ring', sorted(collections.Counter(sum(map(int, w)) - 20 for w in inst).items()))
