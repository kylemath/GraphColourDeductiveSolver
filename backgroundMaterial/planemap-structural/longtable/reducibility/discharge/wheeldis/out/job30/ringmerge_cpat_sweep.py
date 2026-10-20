"""Ring-merge sweep over every C entry the k3x guard never covered (Long Table 20 Oct 20:49Z): every cpat= file of the A74
args (loop/studio/opus_check/s39o/argsA74_local_rpat.txt) except the k3x_C file. An entry is a cfast block whose name the
wlp3 loader takes (header '<name> r=..' followed by a C-REDUCIBLE line). Its recorded Xs are every 'C-REDUCIBLE with X={..}'
and every 'fixed X={..}: C-REDUCIBLE, leftover .. = 0' in the block. Guard (twoeng ringmerge): union-find on X, a
component with >= 2 ring vertices R* merges ring vertices. Status: PASS if some recorded X passes; FAIL if every recorded
X merges; NOX if no X is recorded. Usage: python3 out/job30/ringmerge_cpat_sweep.py ARGS > out/job30/ringmerge_cpat_sweep.out"""
import sys, os, re, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
def ringmerge(x):
    par = {}
    def fd(a):
        while par.setdefault(a, a) != a: a = par[a]
        return a
    for e in x:
        a, b = e.strip().split('-'); par[fd(a)] = fd(b)
    comp = collections.Counter(fd(v) for v in par if v.startswith('R'))
    return max(comp.values(), default=0) >= 2
args = open(sys.argv[1]).read().split()
files = [a[5:] for a in args if a.startswith('cpat=') and 'k3x_C' not in a]
tot = collections.Counter(); fails = []; seen = {}
for fn in files:
    p = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
    if not os.path.exists(p): print('# missing %s' % fn); continue
    cur = None; xs = collections.defaultdict(list); ok = set()
    for line in open(p):
        if ' r=' in line and not line.startswith(' '): cur = line.split()[0]; continue
        if cur and 'C-REDUCIBLE' in line and re.match(r'^[epf]\d+_', cur):
            ok.add(cur)
            mm = re.search(r'X = ([A-Z0-9,-]+)\)', line)   # k42map_C_cons form: '(cfast --fixed and kc -C, X = I0-I1)'
            if mm: xs[cur].append(mm.group(1))
            for m in re.finditer(r'X=\{([^}]*)\}', line):
                if 'fixed X=' in line and not re.search(r'leftover bad classes extending after contraction = 0', line): continue
                xs[cur].append(m.group(1))
    for n in sorted(ok):
        X = xs.get(n, [])
        if not X: st = 'NOX'
        elif any(not ringmerge(x.split(',')) for x in X): st = 'PASS'
        else: st = 'FAIL'
        tot[st] += 1; tot['entries'] += 1
        if n in seen: tot['also in an earlier file'] += 1
        seen.setdefault(n, fn)
        if st != 'PASS': fails.append((st, n, fn, X))
print('# ring-merge sweep: %d cpat files (k3x_C excluded); totals %s' % (len(files), dict(tot)))
for st, n, fn, X in fails: print('%s %s %s X=%s' % (st, n, fn, ' | '.join('{%s}' % x for x in X) or '-'))
