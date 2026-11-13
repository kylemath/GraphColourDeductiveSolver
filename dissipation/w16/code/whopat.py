# which named patterns (D / C files of the args) match a given receiver row
import sys, os, re; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W
ARGV = list(sys.argv); W.init(); ns = W.NS
rows = [(int(a.split('/')[0]), a.split('/')[1], a.split('/')[2]) for a in ARGV[1:]]
HERE = '/tmp/swarm-W10/wd'
for a in open('/tmp/swarm-W10/args_k95f.txt').read().split():
    if not a.startswith(('pat=', 'cpat=')): continue
    fn = a.split('=', 1)[1]; allf = fn.endswith(':all'); fn = fn[:-4] if allf else fn
    p = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
    if not os.path.exists(p): continue
    lines = open(p).read().splitlines()
    if a.startswith('pat='): names = [(l.split()[0], 'D') for l in lines if l.strip() and (allf or 'D=true' in l)]
    else:
        names = []
        for k, l in enumerate(lines):
            if ' r=' in l and not l.startswith(' '):
                for l2 in lines[k + 1:]:
                    if ' r=' in l2 and not l2.startswith(' '): break
                    if 'C-REDUCIBLE' in l2: names.append((l.split()[0], 'C')); break
    for nm, kind in names:
        if not re.match(r'^[epf]\d+_', nm): continue
        d, P = ns['parse_name'](nm)
        for (dd, lk, sv) in rows:
            if dd == d and ns['_pm1'](d, [int(c) for c in lk], [int(c) for c in sv], tuple(P)):
                print('%d/%s/%s matched by %s %s (%s)' % (dd, lk, sv, kind, nm, os.path.basename(p)), flush=True)
