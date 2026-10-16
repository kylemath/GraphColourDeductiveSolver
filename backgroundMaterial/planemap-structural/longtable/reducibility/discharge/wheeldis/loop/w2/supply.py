"""EXPLORE (coordinator ask, 16 Oct 14:20Z): supply of B-fixed configurations for the d = 7 tight family.
For each family row: is it forbidden (by Studio's r_*.out/.cfast only, and by the whole registry incl. explore windows)?
If free under the whole registry, classify its B-fixed sender sets S (any |S| >= 2, gen28 variants) at ring <= 16:
  supply   some S at ring <= 16 untested (or in Studio's pending batch)
  pendC    all tested, some notD with no cfast verdict yet
  hard     all S at ring <= 16 tested, none D/C (HARD28-like; includes rows with no S at ring <= 16)
Usage: python3 supply.py FAMILY..."""
import sys, os, re, glob, collections
FILES = sys.argv[1:]; sys.argv = ['w2.py', 'build', '/dev/null', '30']
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'w2.py')).read(); src = src[:src.index("if mode in ('build', 'build8'):")]
exec(src)

W_ = os.path.dirname(os.path.dirname(HERE))
NEITHER = set()
for fn in glob.glob(os.path.join(W_, '**', '*.cfast'), recursive=True):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
        elif 'search |X|' in line and cur and cur not in CV: NEITHER.add(cur)
# Studio-only patterns: names with D in out/job28/r_*.out or C in out/job28/r_*.cfast
ST = set()
for fn in glob.glob(os.path.join(W_, 'out', 'job28', 'r_*.out')):
    for line in open(fn):
        if 'D=true' in line: ST.add(line.split()[0])
for fn in glob.glob(os.path.join(W_, 'out', 'job28', 'r_*.cfast')):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
        elif 'C-REDUCIBLE' in line and cur: ST.add(cur)
PST = {n: v for n, v in PATS.items() if n in ST}
FAM = family(FILES)
cnt = collections.Counter(); rings = collections.Counter(); sup = {}; rowsup = collections.Counter(); out = []
for lk, sv, s_ in FAM:
    a = any(hits(P, lk, sv) for d, P in PST.values() if d == 7)
    b = a or any(hits(P, lk, sv) for d, P in PATS.values() if d == 7)
    if b:
        cnt['forbidden (Studio r_*)' if a else 'forbidden (explore windows)'] += 1; out.append((lk, sv, s_, 'forbidden')); continue
    vs = G['variants'](7, lk, sv)
    low = [x for x in vs if x[0] <= 16]
    un = [x for x in low if x[5] not in DV and x[5] not in CV]
    pc = [x for x in low if DV.get(x[5]) == 'notD' and x[5] not in CV and x[5] not in NEITHER]
    ne = [x for x in low if x[5] in NEITHER]
    if un: k = 'supply'
    elif pc: k = 'pendC'
    else: k = 'hard'
    cnt[k] += 1
    if ne: cnt['  (free rows with an S tested neither)'] += 1
    if not low: cnt['  (hard rows with no S at ring <= 16)'] += 1
    for x in un: sup[x[5]] = x[0]; rowsup[(lk, sv)] += 1
    if k == 'supply': rings[min(x[0] for x in un)] += 1
    out.append((lk, sv, s_, k))
print('family', len(FAM))
for k in sorted(cnt): print('  %-40s %d' % (k, cnt[k]))
print('supply rows by smallest untested ring:', sorted(rings.items()))
print('distinct untested configs at ring <= 16:', len(sup), sorted(collections.Counter(sup.values()).items()),
      'in Studio pending batch:', sum(1 for n in sup if n in PEND))
open(os.path.join(HERE, 'supply_rows.txt'), 'w').write(''.join('%s %s %s %s\n' % r for r in out))
open(os.path.join(HERE, 'supply_cfg.txt'), 'w').write(''.join('%s %d\n' % (n, r) for n, r in sorted(sup.items(), key=lambda x: x[1])))
