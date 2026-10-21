"""s52c copy of s46c/tabname.py for A83 (FULL = s33z/reg_A83, DONLY = s52c/noC).
s41c: per-C-name table variants. FULL = s33z/reg_A74 tables (D + every C: k3x_C + RSST C2cons); DONLY = s41c/noC.
A kill6 key / l3q killed value present in FULL but not in DONLY is a C kill; its name list (all C) is read from FULL.
usage: python3 tabname.py list                -> every C name behind a table kill (tabnames.txt)
       python3 tabname.py build OUTDIR N1[,N2..] -> tables = DONLY + the C kills of the names given (kill6 json + npy, l3q json)"""
import sys, os, json, subprocess, shutil
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FULL = B + '/s33z/reg_A83'; DON = B + '/s52c/noC'
def kill6(U):
    a = json.load(open('%s/f/kill/kill6_U%d.json' % (FULL, U))); b = json.load(open('%s/f/kill/kill6_U%d.json' % (DON, U)))
    return a, b, {(w, k): ns for w, ks in a['kills'].items() for k, ns in ks.items() if k not in b['kills'].get(w, {})}
def l3q(sg):
    a = json.load(open('%s/tab_%s.json' % (FULL, sg))); b = json.load(open('%s/tab_%s.json' % (DON, sg)))
    return a, b, {(k, v): ns for k in a for v, ns in a[k][1].items() if v not in b[k][1]}
if sys.argv[1] == 'list':
    import collections; c = collections.Counter(); where = collections.defaultdict(set)
    for U in (7, 8, 9):
        for key, ns in kill6(U)[2].items(): c.update(ns); [where[n].add('kill6_U%d' % U) for n in ns]
    for sg in ('1', '-1'):
        for key, ns in l3q(sg)[2].items():
            assert len(ns) < 3, ns   # why lists are cut at 3: a cut list could hide a name
            c.update(ns); [where[n].add('l3q%s' % sg) for n in ns]
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tabnames.txt'), 'w') as f:
        f.write('# C names behind a table kill (FULL reg_A83 minus D-only): name #kills tables\n')
        for n, k in c.most_common(): f.write('%s %d %s\n' % (n, k, ','.join(sorted(where[n]))))
    print(len(c), 'names')
else:
    OUT, NM = sys.argv[2], set(sys.argv[3].split(','))
    os.makedirs(OUT + '/f/kill', exist_ok=True)
    for U in (7, 8, 9):
        a, b, d = kill6(U)
        for (w, k), ns in d.items():
            if NM & set(ns): b['kills'].setdefault(w, {})[k] = ns
        json.dump(b, open('%s/f/kill/kill6_U%d.json' % (OUT, U), 'w'))
    for sg in ('1', '-1'):
        a, b, d = l3q(sg)
        LET = (5, 6, 7, 8, 9)
        for (k, v), ns in d.items():
            if NM & set(ns): b[k][0] &= ~(1 << LET.index(int(v))); b[k][1][v] = ns
        json.dump(b, open('%s/tab_%s.json' % (OUT, sg), 'w'))
    subprocess.run(['python3', B + '/s30t/f/s16_killnpy.py', OUT + '/f/kill'], check=True, stdout=open(OUT + '/f/kill/killnpy.log', 'w'))
