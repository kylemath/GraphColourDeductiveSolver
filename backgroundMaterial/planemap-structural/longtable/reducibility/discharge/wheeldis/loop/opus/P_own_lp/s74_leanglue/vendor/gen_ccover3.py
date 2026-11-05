"""Studio CCover generator (out/lean_ccover/gen_ccover.py, Long Table 20 Oct 20:42Z): the A74 C-cover entries not yet in Lean.
k3x_C names in ONLY use the twoeng source rule of gen_cxring.py; EXTRAFILE lines "name<TAB>r m ringadj intadj<TAB>X" (RSST with
RSST's contract X; the two cpat entries with Studio's two-engine X) are taken verbatim. Output CCover.lean (ccEntries).
Based on: Studio variant (out/lean_cxint/gen_cxint.py) of dcheck/gen_cxring.py: the interior-only C entries (no ring vertex
in X) with r <= RMAX (default 13), written as CXInt.lean (imports CXRing for XRData; ccEntries, ccEntries_ok,
ccEntries_length). Only the selection and the output wrapper differ from gen_cxring.py.
Generate CXRing.lean (Long Table, 19 Oct 2026): every ring-X C entry of discharge/wheeldis/out/job30/k3x_C.cfast,
with the configuration its C verdict was computed on and one label per X-component.
Source of each configuration: as twoeng.py, the first loop/k*/ cfast block (sorted file order, C2 files and teamB
skipped) with an accepted C line for the name; its input line is read from the sibling .txt/.in (stem without
_cf.cfast/_cf.out/_fixedX.cfast), else from any .txt/.in in that folder, and must match the block header's r and m
exactly once.
Usage: python3 gen_cxring.py CXRing.lean > CXRing.new   (replaces the xrEntries block; header and theorems kept)"""
import os, re, sys, glob
W = os.environ['WHEELDIS']
RMAX = int(os.environ.get('RMAX', '13'))
names = {}; cur = None
for l in open(os.path.join(W, 'out', 'job30', 'k3x_C.cfast')):
    if not l.startswith(' '): cur = l.split()[0]; hdr = l
    elif 'C-REDUCIBLE' in l:
        m = re.search(r'X=\{([^}]*)\}', l)
        names.setdefault(cur, (m.group(1).split(','), re.search(r' r=(\d+) m=(\d+)', hdr).groups()))
files = sorted(f for f in glob.glob(os.path.join(W, 'loop', 'k[0-9]*', '*')) if os.path.isfile(f))
files = [f for f in files if 'C2' not in os.path.basename(f) and os.sep + 'teamB' not in f]
src = {}
for fn in files:
    cur = None; curkc = False
    try: lines = open(fn).read().splitlines()
    except UnicodeDecodeError: continue
    for line in lines:
        m = re.match(r'^([A-Za-z]\w*_\S+) r=\d+ ', line)
        if m: cur, curkc = m.group(1), 'mode=' in line; continue
        if cur and 'C-REDUCIBLE' in line and not curkc:
            mf = re.search(r'fixed X=(\{[^}]*\}) .*C-REDUCIBLE, leftover bad classes extending after contraction = 0$', line)
            if 'fixed X=' in line and not mf: continue
            if cur in names and cur not in src: src[cur] = fn
def confs_in(p, n):
    out = set()
    for line in open(p, errors='ignore'):
        t = line.split()
        if len(t) == 5 and t[0] == n and t[1].isdigit(): out.add(' '.join(t[1:]))
    return out
def isring(x): return any(e.startswith('R') or '-R' in e for e in x)
listed = []
EXTRA = [x for x in os.environ.get('EXTRA', '').split(',') if x]   # Long Table 20 Oct 14:17Z: always included
ONLY = [x for x in os.environ.get('ONLY', '').split(',') if x]
order = sorted(n for n in names if n in ONLY)
assert len(order) == len(ONLY), ('ONLY names not in k3x_C', set(ONLY) - set(order))
def parse(s):
    r, m, ra, ia = s.split(); r = int(r); m = int(m)
    ra = [[] if g == '-' else list(map(int, g.split(','))) for g in ra.split(';')]
    ia = [[] if g == '-' else list(map(int, g.split(','))) for g in ia.split(';')]
    return r, m, ra, ia
arr = lambda L: "#[" + ", ".join("#[" + ", ".join(map(str, g)) + "]" for g in L) + "]"
items = []; AMB = []
for n in order:
    fn = src[n]; d = os.path.dirname(fn)
    stem = re.sub(r'_(cf\.cfast|cf\.out|fixedX\.cfast)$', '', os.path.basename(fn))
    got = set()
    for e in ('.txt', '.in'):
        if os.path.exists(os.path.join(d, stem + e)): got |= confs_in(os.path.join(d, stem + e), n)
    if not got:
        for f in os.listdir(d):
            if f.endswith('.txt') or f.endswith('.in'): got |= confs_in(os.path.join(d, f), n)
    got = sorted(g for g in got if g.split()[:2] == list(names[n][1]))
    if len(got) != 1: AMB.append((n, fn, got))   # several input lines with the block's r and m: every one is written
    for gi, g in enumerate(got):
      nm2 = n if len(got) == 1 else '%s#%s' % (n, 'abcdefgh'[gi])
      r, m, ra, ia = parse(g)
      par = {}
      def f(x):
          par.setdefault(x, x)
          while par[x] != x: x = par[x]
          return x
      eqR = []; eqI = []
      for e in names[n][0]:
          p, q = e.split('-'); P = (p[0], int(p[1:])); Q = (q[0], int(q[1:]))
          par[f(P)] = f(Q)
          if P[0] == 'R': eqR.append((P[1], Q[1]))
          elif Q[0] == 'R': eqR.append((Q[1], P[1]))
          else: eqI.append((Q[1], P[1]))
      ids = {}
      lab = lambda v: ids.setdefault(f(v), len(ids))
      lbl = [lab(('I', a)) for a in range(m)] + [lab(('R', t)) for t in range(r)]
      items.append('  { name := "%s", src := "%s", X := "%s",\n    cf := {\n      name := "%s", r := %d, m := %d,\n'
                   '      ringAdj := %s,\n      intAdj := %s },\n    eqR := %s, eqI := %s,\n    lbl := %s }' % (
          nm2, os.path.relpath(fn, W), ','.join(names[n][0]), nm2, r, m, arr(ra), arr(ia),
          "[" + ", ".join("(%d, %d)" % p for p in eqR) + "]", "[" + ", ".join("(%d, %d)" % p for p in eqI) + "]", lbl))
for line in open(os.environ['EXTRAFILE']):
    if not line.strip(): continue
    n, kcf, xs = line.rstrip('\n').split('\t')
    r, m, ra, ia = parse(kcf)
    par = {}
    def f(x):
        par.setdefault(x, x)
        while par[x] != x: x = par[x]
        return x
    eqR = []; eqI = []
    for e in xs.split(','):
        p, q = e.split('-'); P = (p[0], int(p[1:])); Q = (q[0], int(q[1:]))
        par[f(P)] = f(Q)
        if P[0] == 'R': eqR.append((P[1], Q[1]))
        elif Q[0] == 'R': eqR.append((Q[1], P[1]))
        else: eqI.append((Q[1], P[1]))
    ids = {}
    lab = lambda v: ids.setdefault(f(v), len(ids))
    lbl = [lab(('I', a)) for a in range(m)] + [lab(('R', t)) for t in range(r)]
    items.append('  { name := "%s", src := "%s", X := "%s",\n    cf := {\n      name := "%s", r := %d, m := %d,\n'
                 '      ringAdj := %s,\n      intAdj := %s },\n    eqR := %s, eqI := %s,\n    lbl := %s }' % (
        n, 'EXTRAFILE', xs, n, r, m, arr(ra), arr(ia),
        "[" + ", ".join("(%d, %d)" % p for p in eqR) + "]", "[" + ", ".join("(%d, %d)" % p for p in eqI) + "]", lbl))
sys.stdout.write("""import CXRing

/-! # CCover (Studio, Long Table 20 Oct 20:42Z): the A74 C-cover entries not yet in Lean (ring <= %d unused here), as
`XRData` (from CXRing), generated by out/lean_ccover/gen_ccover.py (a variant of dcheck/gen_cxring.py). -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def ccEntries : List XRData := [
""" % RMAX + ",\n".join(items) + """]

theorem ccEntries_ok : ccEntries.all XRData.ok = true := by
  native_decide

theorem ccEntries_length : ccEntries.length = %d := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.ccEntries_ok
""" % len(items))
sys.stderr.write('interior-only entries with r <= %d: %d written, %d with several matching input lines (all written, suffix #a, #b): %s\n' % (RMAX, len(items), len(AMB), [(a, os.path.relpath(b, W), len(c)) for a, b, c in AMB]))
