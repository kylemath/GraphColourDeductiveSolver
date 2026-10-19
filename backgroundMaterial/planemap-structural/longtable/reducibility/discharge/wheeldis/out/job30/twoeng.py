"""Job 30: two-engine filter for explore's window files (loop/k3*/: dfast/dfast18/cfast output, kc output = lines
with 'mode=', kc -C blocks). A window is loaded only if
- D: D=true on dfast/dfast18 and D=true on kc, or
- C: some single X (compared as an edge set) accepted by both engines under conservative admissibility (kc -C2 files are
  ignored): cfast (search, or --fixed X with leftover 0) and kc -C (search, or
  kc -C -x X with leftover 0).
Writes out/job30/k3x_D.out (dfast lines) and out/job30/k3x_C.cfast (cfast blocks), and prints a summary.
Usage: python3 out/job30/twoeng.py [glob ...]   (default loop/k[0-9]*/*: explore's round folders, and k3studio)"""
import sys, os, glob, re, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
pats = sys.argv[1:] or ['loop/k[0-9]*/*']
files = sorted(f for g in pats for f in glob.glob(os.path.join(HERE, g)) if os.path.isfile(f))
BROAD = [f for f in files if 'C2' in os.path.basename(f)]   # kc -C2 (broad admissibility) verdicts: never used (Long Table, 18 Oct)
files = [f for f in files if f not in BROAD]
def nx(x): return None if x is None else frozenset(e.strip() for e in x.strip('{}').split(','))   # X as an edge set
dD, kD, cC = {}, set(), {}; cX = collections.defaultdict(set); kC = collections.defaultdict(set)   # kc -C: every X kc accepts (search or fixed -x)
for fn in files:
    cur = None; curkc = False; block = []
    try: lines = open(fn).read().splitlines()
    except UnicodeDecodeError: continue
    for line in lines:
        m = re.match(r'^([A-Za-z]\w*_\S+) r=\d+ ', line)   # any header name (Long Table 20:34Z), so a non-plain block never inherits the previous name
        if m:
            cur, curkc = m.group(1), 'mode=' in line
            if 'D=true' in line:
                if curkc: kD.add(cur)
                else: dD.setdefault(cur, line)
            hdr = line; continue
        if cur and 'C-REDUCIBLE' in line:
            x = re.search(r'X=(\{[^}]*\})', line); x = nx(x.group(1)) if x else None
            if curkc: kC[cur].add(x)
            else:
                mf = re.search(r'fixed X=(\{[^}]*\}) .*C-REDUCIBLE, leftover bad classes extending after contraction = 0$', line)
                if 'fixed X=' in line and not mf: continue
                xx = nx(mf.group(1)) if mf else x
                cX[cur].add(xx); cC.setdefault(cur, (xx, hdr, line))
        mx = re.match(r'^\s+X=(\{[^}]*\}) adm=yes leftover 0\b', line)   # kc -C -x X: fixed X accepted, leftover 0
        if cur and curkc and mx: kC[cur].add(nx(mx.group(1)))
okD = sorted(n for n in dD if n in kD)
okC = sorted(n for n in cC if cX[n] & kC.get(n, set()))
mism = sorted(n for n in cC if n in kC and not (cX[n] & kC[n]))
# letter-9 rule (loop/studio/opus_check/letter9_rule.md, Long Table 09:03Z): a 9 in an f-name's link or s word is an
# interior vertex of exact degree 9, which no LP letter matches (LP 9 = >= 9): exclude and log; a 9 only at an f9_
# centre is exact and admitted as normal
# prefix guard (Long Table 20:34Z): only a plain receiver name the wlp3 parser reads, [epf]<d>_<d link letters>_<d s
# letters>, may enter k3x; g7_, s5_, b7p5_ and any other form (privates, ring-3 vertices) is held and logged
def plain(n):
    m = re.fullmatch(r'([epf])(\d+)_([5-9B.]+)_([0-9B.]+)', n)
    return bool(m) and len(m.group(3)) == int(m.group(2)) == len(m.group(4))
sys.path.insert(0, os.path.join(HERE, 'out', 'job31'))
from letter9 import lp_reading
L9 = sorted(n for n in set(okD) | set(okC) if plain(n) and lp_reading(n) == 'unmatchable')
# sender-context names (centre degree < 7, e.g. explore's p5_ form, Long Table 11:48Z): not receiver patterns; they wait
# for RELAY_SPEC 17's sender 2-ball filter and are never written to k3x (logged)
SND = sorted(n for n in set(okD) | set(okC) if not plain(n) or int(re.match(r'^[epf](\d+)_', n).group(1)) < 7)
okD = [n for n in okD if n not in SND]; okC = [n for n in okC if n not in SND]
if SND:
    with open(os.path.join(HERE, 'out', 'job30', 'sender_names_held.log'), 'a') as _sf:
        for n in SND: _sf.write('%s held (two-engine %s; %s)\n' % (n, 'D' if n in dD and n in kD else 'C', 'not a plain [epf]<d>_link_s name the parser reads' if not plain(n) else 'centre degree < 7: sender context, not a receiver pattern'))
# ring-merge hold (CGLUE-SCOPE a7557788, Long Table 19:27Z): a C entry whose recorded X has a connected component holding
# two or more ring vertices R* merges ring vertices under contraction (the case Job 21 refused); held out of k3x, logged
def ringmerge(x):
    par = {}
    def fd(a):
        while par.setdefault(a, a) != a: a = par[a]
        return a
    for e in x:
        a, b = e.split('-'); par[fd(a)] = fd(b)
    comp = collections.Counter(fd(v) for v in par if v.startswith('R'))
    return max(comp.values(), default=0) >= 2
RM = sorted(n for n in okC if ringmerge(cC[n][0]))
okC = [n for n in okC if n not in RM]
if RM:
    with open(os.path.join(HERE, 'out', 'job30', 'c_ringmerge_held.log'), 'a') as _rf:
        for n in RM: _rf.write('%s held (two-engine C; X=%s has a component with two ring vertices)\n' % (n, '{' + ','.join(sorted(cC[n][0])) + '}'))
okD = [n for n in okD if n not in L9]; okC = [n for n in okC if n not in L9]
if L9:
    with open(os.path.join(HERE, 'out', 'job30', 'letter9_excluded.log'), 'a') as _lf:
        for n in L9: _lf.write('%s excluded (two-engine %s; link/s 9 = exact degree 9, LP-unmatchable)\n' % (n, 'D' if n in dD and n in kD else 'C'))
open(os.path.join(HERE, 'out', 'job30', 'k3x_D.out'), 'w').write(''.join(dD[n] + '\n' for n in okD))
open(os.path.join(HERE, 'out', 'job30', 'k3x_C.cfast'), 'w').write(''.join('%s\n%s\n' % (cC[n][1], cC[n][2]) for n in okC))
print('broad (kc -C2) files ignored: %s' % ' '.join(os.path.relpath(f, HERE) for f in BROAD))
print('files %d; D both engines %d (dfast-only %d, kc-only %d); C both engines same X %d (X mismatch %d: %s; one engine only %d)' % (
    len(files), len(okD), len(set(dD) - kD), len(kD - set(dD)), len(okC), len(mism), ' '.join(mism[:5]),
    len(set(cC) ^ set(kC))))
print('sender-context names held out of k3x: %d (out/job30/sender_names_held.log)' % len(SND))
print('ring-merge hold: %d C entries with an X component on two ring vertices held (out/job30/c_ringmerge_held.log): %s' % (len(RM), ' '.join(RM)))
print('letter-9 rule: %d two-engine names with a link/s 9 excluded (logged in out/job30/letter9_excluded.log)' % len(L9))
