"""Job 30 audit: which loaded registry patterns (wlp3 parse) carry a letter on a slot no 5-sender reads?
parse() keeps only fives whose four slots are all specified, plus those slots; any other specified letter is
dropped, which makes the encoded pattern weaker than the configuration (it would forbid more than is reducible).
Usage: python3 out/job30/audit_drop.py <pattern args as for wlp3>   (WLP3X_DEF=1 keeps out/def_*)"""
import sys, os, re, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
EXCL = ('hr1_or1',) if os.environ.get('WLP3X_DEF') == '1' else ('out/def_', 'hr1_or1')
names = {}
for a in sys.argv[1:]:
    if not a.startswith(('pat=', 'cpat=')) or any(e in a for e in EXCL): continue
    kind, fn = a.split('=', 1); allf = fn.endswith(':all'); fn = fn[:-4] if allf else fn
    p = os.path.join(HERE, fn)
    if not os.path.exists(p): continue
    if kind == 'pat':
        for line in open(p):
            if line.strip() and (allf or 'D=true' in line) and re.match(r'^[epf]\d+_', line): names.setdefault(line.split()[0], fn)
    else:
        cur = None
        for line in open(p):
            if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
            elif 'C-REDUCIBLE' in line and cur and re.match(r'^[epf]\d+_', cur): names.setdefault(cur, 'C:' + fn)
bad = collections.Counter(); ex = collections.defaultdict(list)
for nm, fn in names.items():
    f = nm.split('_'); d = int(f[0][1:]); lk, sv = f[1], f[2]; k0 = f[0][0]
    def spec(ch, kind):
        if ch == '.': return False
        if k0 == 'p' and ((kind == 'w' and ch == '9') or (kind == 's' and ch == '0')): return False
        return True
    sp = lambda ch, kind: spec(ch, kind)
    cw = lambda i: sp(lk[i % d], 'w'); cs = lambda i: sp(sv[i % d], 's')
    full5 = [lk[i] == '5' and cw(i + 1) and cw(i - 1) and cs(i) and cs(i - 1) for i in range(d)]   # parse() keeps these
    rw = [full5[i] or full5[(i - 1) % d] or full5[(i + 1) % d] for i in range(d)]
    rs = [full5[i] or full5[(i + 1) % d] for i in range(d)]
    drop = [('w', i, lk[i]) for i in range(d) if spec(lk[i], 'w') and not rw[i]] + \
           [('s', i, sv[i]) for i in range(d) if spec(sv[i], 's') and not rs[i]]
    if drop: bad[fn] += 1; ex[fn].append((nm, drop))
print('patterns loaded %d; with a dropped letter %d' % (len(names), sum(bad.values())))
for fn, k in bad.most_common():
    print('  %-44s %d   e.g. %s' % (fn, k, '; '.join('%s %s' % (n, ''.join('%s%d=%s' % x for x in dr)) for n, dr in ex[fn][:3])))
