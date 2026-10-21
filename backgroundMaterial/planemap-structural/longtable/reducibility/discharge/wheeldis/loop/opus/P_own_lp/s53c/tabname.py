"""s53c copy of s52c/tabname.py for A97 (FULL = s33z/reg_A97 + s47/tabV8_A97 for the V = 8 tables, DONLY = s53c/noC), + the V = 8 l3q tables
(tabV8_{1,-1}.json, same layout as tab_*.json: key -> [mask, {letter: names[:3]}]).
s41c: per-C-name table variants. A kill6 key / l3q (V = 7 or V = 8) killed value present in FULL but not in DONLY is a C kill; its name list
(all C) is read from FULL.
usage: python3 tabname.py list                -> every C name behind a table kill (tabnames.txt)
       python3 tabname.py build OUTDIR N1[,N2..] -> tables = DONLY + the C kills of the names given (kill6 json + npy, l3q json, V8 json)"""
import sys, os, json, subprocess, shutil
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FULL = B + '/s33z/reg_A97'; FULLV8 = B + '/s47/tabV8_A97'; DON = B + '/s53c/noC'
def kill6(U):
    a = json.load(open('%s/f/kill/kill6_U%d.json' % (FULL, U))); b = json.load(open('%s/f/kill/kill6_U%d.json' % (DON, U)))
    return a, b, {(w, k): ns for w, ks in a['kills'].items() for k, ns in ks.items() if k not in b['kills'].get(w, {})}
def l3q(sg, v8=False):
    a = json.load(open(('%s/tabV8_%s.json' % (FULLV8, sg)) if v8 else ('%s/tab_%s.json' % (FULL, sg))))
    b = json.load(open('%s/tab%s_%s.json' % (DON, 'V8' if v8 else '', sg)))
    assert set(a) == set(b) and len(a) == 2500, (sg, v8)
    for k in a:   # D-only kills must be a subset of the full kills (mask bits: full clears every bit D-only clears)
        assert set(b[k][1]) <= set(a[k][1]) and (a[k][0] & ~b[k][0]) == 0, (sg, v8, k)
    return a, b, {(k, v): ns for k in a for v, ns in a[k][1].items() if v not in b[k][1]}
if sys.argv[1] == 'list':
    import collections; c = collections.Counter(); where = collections.defaultdict(set)
    for U in (7, 8, 9):
        for key, ns in kill6(U)[2].items(): c.update(ns); [where[n].add('kill6_U%d' % U) for n in ns]
    for v8 in (False, True):
        for sg in ('1', '-1'):
            for key, ns in l3q(sg, v8)[2].items():
                assert len(ns) < 3, ns   # why lists are cut at 3: a cut list could hide a name
                c.update(ns); [where[n].add('l3q%s%s' % ('V8' if v8 else '', sg)) for n in ns]
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tabnames.txt'), 'w') as f:
        f.write('# C names behind a table kill (FULL reg_A97 + tabV8_A97 minus D-only): name #kills tables\n')
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
    LET = (5, 6, 7, 8, 9)
    for v8 in (False, True):
        for sg in ('1', '-1'):
            a, b, d = l3q(sg, v8)
            for (k, v), ns in d.items():
                if NM & set(ns): b[k][0] &= ~(1 << LET.index(int(v))); b[k][1][v] = ns
            json.dump(b, open('%s/tab%s_%s.json' % (OUT, 'V8' if v8 else '', sg), 'w'))
    subprocess.run(['python3', B + '/s30t/f/s16_killnpy.py', OUT + '/f/kill'], check=True, stdout=open(OUT + '/f/kill/killnpy.log', 'w'))
