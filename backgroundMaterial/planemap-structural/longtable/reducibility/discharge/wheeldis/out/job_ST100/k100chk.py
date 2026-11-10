"""ST-42 second check for one K-5 hit (Studio, 9 Nov; our code + Studio engines).  usage (cwd wheeldis): python3 out/job_ST100/k5chk.py NN ID
Writes out/job_ST100/chk/hNN/: cfg.in/.x/.out, extraC.tsv, lean/CK5HNN.lean (+log), occ.txt, report.md, verdict.txt (PASS/FAIL).
C hits: iso (window K from name), kc -t 600 -C -x X, cfast --fixed X, gen_ccover3 3c9e7145 EXTRAFILE -> CK5HNN (ok/admissibleX/foldSafeX),
rim-pin info for R-I edges (I's ring neighbours, kc rotation), K3CHK occurs() on every row in the res source column.
D hits: iso, kc -C, dfast18, occurrence."""
import sys, os, re, glob, subprocess
NN, ID = sys.argv[1], sys.argv[2]
C = 'out/job_ST100/chk/h%s/' % NN; os.makedirs(C + 'lean', exist_ok=True)
row = None
for f in sorted(glob.glob('out/job_ST100/results/res_K5_*.tsv')):
    for l in open(f):
        if l.startswith(ID): row = l.rstrip('\n').split('\t'); src = f
nm, ring, m, verdict, X, srcrow, kcl = row[3], int(row[1]), int(row[2]), row[4], row[6], row[9], row[-1]
open(C + 'cfg.in', 'w').write(kcl + '\n')
rep = ['# ST-100 bind5657 hit %s second check (Studio, 9 Nov): %s %s X={%s}' % (NN, nm, verdict, X),
       'Source: %s, id %s, ring %d m %d, rows %s, lead confirm %s.' % (os.path.basename(src), ID, ring, m, srcrow, row[10])]
ok = True
sys.argv = ['x']; exec(open('out/job_HOFFC7/kccheck.py').read().split('srcs = Sources()')[0])
fname = re.sub(r'^b(\d+)_u', r'f\1_', nm)
K, why = build_K(fname, ring, m)
if why: ok = False; rep.append('- FAIL build_K(%s): %s' % (fname, why))
else:
    w = iso(K[0], K[1], kcl); ok &= w is None
    rep.append('- kc line (= res kc column) interior + degrees vs K of window %s (%s): %s' % (fname, K[3], w or 'isomorphic'))
E8 = lambda c: subprocess.run(c, capture_output=True, text=True).stdout + subprocess.run(['true']).stdout
if verdict == 'C':
    open(C + 'cfg.x', 'w').write('%s {%s}\n' % (nm, X))
    a = subprocess.run(['nice', '-n', '10', 'loop/kc/kc', '-t', '600', '-C', '-x', C + 'cfg.x', C + 'cfg.in'], capture_output=True, text=True).stdout
    b = subprocess.run(['nice', '-n', '10', '../studio15/cfast', C + 'cfg.in', '--fixed', X], capture_output=True, text=True).stdout
    open(C + 'cfg.out', 'w').write('== kc -C -x X\n' + a + '== cfast --fixed X\n' + b)
    ka = 'adm=yes leftover 0' in a and 'C-REDUCIBLE' in a; cb = 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in b
    ok &= ka and cb
    rep.append('- kc -t 600 -C -x {%s}: %s; cfast --fixed %s: %s' % (X, 'adm=yes leftover 0 C-REDUCIBLE' if ka else 'FAIL', X, 'C-REDUCIBLE leftover 0' if cb else 'FAIL'))
    open(C + 'extraC.tsv', 'w').write('%s\t%s\t%s\n' % (nm, ' '.join(kcl.split()[1:]), X))
    env = dict(os.environ, WHEELDIS=os.getcwd(), RMAX='16', ONLY='', EXTRAFILE=C + 'extraC.tsv')
    g = subprocess.run(['python3', 'out/job_OCC13/in/vendor/gen_ccover3.py'], capture_output=True, text=True, env=env).stdout
    open(C + 'lean/gen_raw.lean.txt', 'w').write(g); g = g.split('\n')
    a_ = [k for k, l in enumerate(g) if l.startswith('def ccEntries')][0]; b_ = [k for k, l in enumerate(g) if l.startswith('    lbl :=')][0]
    ck = open('out/job_HCK3k/lean/CK3K.lean').read().split('\n')
    a2 = [k for k, l in enumerate(ck) if l.startswith('def k3kEntries')][0]; b2 = [k for k, l in enumerate(ck) if l.startswith('    lbl :=')][0]
    t = '\n'.join(ck[:a2 + 1] + g[a_ + 1:b_ + 1] + ck[b2 + 1:])
    t = t.replace('CK3K (Studio, HCK3k, 8 Nov): the K3k C kill b8_u...56556_.....66. = f8_...56556_.....66. of pat_K3g2_C.cfast 6f6dce95 (same literal and X as in CK3C7)',
                  'CK5P%s (Studio, ST-100 bind5657 hit %s, 9 Nov): %s X={%s} (%s, gen_ccover3 3c9e7145 EXTRAFILE literal)' % (NN, NN, nm, X, os.path.basename(src))).replace('k3k', 'k5p%s' % NN)
    open(C + 'lean/CK5P%s.lean' % NN, 'w').write(t)
    rs = open('out/job_HCK3k/lean/run.sh').read().replace('hck3k', 'k5chk').replace('job_HCK3k/lean', 'job_ST100/chk/h%s/lean' % NN)
    open(C + 'lean/run.sh', 'w').write(rs); os.chmod(C + 'lean/run.sh', 0o755)
    subprocess.run(['./run.sh', 'CK5P%s' % NN], cwd=C + 'lean')
    st = open(C + 'lean/status.txt').read().strip().split('\n')[-1]
    lk = 'exit=0' in st and 'sorry=0 error=0' in st; ok &= lk
    rep.append('- Lean lean/CK5P%s.lean (XRData.ok, admissibleX, foldSafeX): %s' % (NN, st))
    rim = [e for e in X.split(',') if 'R' in e]
    if rim:
        RC = {'__name__': 'rc'}; exec(open('loop/studio/opus_check/f2b041/keep95p131f/rot/rotcheck.py').read(), RC)
        rot = RC['kc_rotation'](kcl); f = kcl.split(); rp = f[3].split(';')
        for e in rim:
            p, q = e.split('-'); r_, i_ = (p, q) if p[0] == 'R' else (q, p); ii = int(i_[1:]); rr = int(r_[1:])
            on = rp[ii] != '-' and rr in map(int, rp[ii].split(','))
            ro = rot[ii]; k = ro.index(('R', rr)) if ('R', rr) in ro else -1
            fl = (ro[k - 1], ro[(k + 1) % len(ro)]) if k >= 0 else None
            ok &= on
            rep.append('- rim pin %s: %s is %sa ring neighbour of %s (ring nbrs %s); rotation of %s %s; flanked by %s' % (e, r_, '' if on else 'NOT ', i_, rp[ii], i_, ro, fl))
    else: rep.append('- X interior only: no rim pin.')
else:
    a = subprocess.run(['nice', '-n', '10', 'loop/kc/kc', '-t', '600', '-C', C + 'cfg.in'], capture_output=True, text=True).stdout
    b = subprocess.run(['nice', '-n', '10', 'out/job52/dfast18', C + 'cfg.in'], capture_output=True, text=True).stdout
    open(C + 'cfg.out', 'w').write('== kc -C\n' + a + '== dfast18\n' + b)
    dd = 'D=true' in a and 'D=true' in b; ok &= dd
    rep.append('- kc -C: %s; dfast18: %s' % ('D' if 'D=true' in a else 'not D', 'D' if 'D=true' in b else 'not D'))
src0 = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = '%s'" % C).replace("open(K + 'configs.kc')", "open(K + 'cfg.in')")
exec(src0)
occ = []
for rw in srcrow.split(':', 1)[1].split(','):
    L, S = rw.split('/'); fs, rt = occurs(kcl, len(L), L, S); occ.append('%d/%s/%s face-set %d rotation-preserving %d %s' % (len(L), L, S, fs, rt, 'OCCURS' if rt else 'NO'))
    ok &= rt > 0
open(C + 'occ.txt', 'w').write('\n'.join(occ) + '\n')
rep.append('- Occurrence (K3CHK occurs, rotation-preserving): ' + '; '.join(occ))
rep.append('- **Result: %s**' % ('PASS' if ok else 'FAIL'))
open(C + 'report.md', 'w').write('\n'.join(rep) + '\n'); open(C + 'verdict.txt', 'w').write('PASS\n' if ok else 'FAIL\n')
print('\n'.join(rep))
