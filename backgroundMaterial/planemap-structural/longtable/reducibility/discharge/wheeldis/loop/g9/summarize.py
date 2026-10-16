"""G9 (exploratory): summarise defect_check2_8.py .status files: which families kill each candidate.
Usage: python3 summarize.py STATUS [STATUS ...]"""
import sys, ast, collections
tot = collections.Counter(); unt = collections.Counter()
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.strip(): continue
        v = line.split()[0]; st = ast.literal_eval(line[line.index('{'):])
        fams = sorted(k for k in st if st[k] and (k[:2] in ('W7', 'W8') or k.startswith(('rcD@', 'rcC@', 'bfD@', 'bfC@', 'nosimple@', 'bf_nosimple@'))))
        wheel = any(k.startswith('W') for k in fams); rc = any(k.startswith(('rcD', 'rcC')) for k in fams)
        bfk = any(k.startswith(('bfD', 'bfC')) for k in fams); ns = any('nosimple' in k for k in fams)
        at8 = any(k.endswith('@8') or k.startswith('W8') for k in fams)
        if v != 'killed': cls = v
        elif wheel: cls = 'killed: 7/8-wheel (D or C-cand)'
        elif rc: cls = 'killed: receiver-centred B-free (D/C)'
        elif bfk: cls = 'killed: B-fixed only'
        elif ns: cls = 'killed: nosimple only'
        else: cls = 'killed: ?'
        tot[cls] += 1; tot['kill uses a config at an 8' if at8 else 'kill only at 7s'] += (v == 'killed')
        tot['rc-kill available (any)'] += rc; tot['bf-kill available (any)'] += bfk
        for k in st:
            if k.startswith('unt8_'): unt[k[5:]] += 1
        if v != 'killed': print(line.strip())
for k, n in sorted(tot.items()): print('%-45s %d' % (k, n))
print('untested wheels with a letter 8 / centre 8 appearing (counted not reducible), #candidates containing each:')
for k, n in sorted(unt.items(), key=lambda x: -x[1]): print('  %s-wheel %s: %d' % (k.split('_')[0], k.split('_')[1], n))
