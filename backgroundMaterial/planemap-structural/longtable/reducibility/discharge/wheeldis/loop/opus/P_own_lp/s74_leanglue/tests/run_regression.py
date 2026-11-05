#!/usr/bin/env python3
"""Regression tests for gen_occ_kc.py that need no Lean (s74_leanglue, Team C, 5 Nov 2026).

  python3 tests/run_regression.py [--rev origin/main] [--ref-root DIR] [--big] [--keep DIR]

Committed reference files are read with `git show REV:path` (default origin/main); --ref-root reads them from a directory
laid out like the repository instead. Exit status 0 iff every test passes. Tests:
  T1  the 49 K=1 keys (discharge/studio14b/k1_r17_19.txt): gen_occ_kc --form ring == committed dcheck/occ24/Kxx.lean, byte
      for byte, through both the `one` and the legacy gen_occ_key argument order.
  T2  bridge: gen_occ_kc's bridge (no registry) for K41 == committed dcheck/COccK41.lean; for all 49 keys == the vendored
      occ24/gen_rotbridge.py run as a program on the regenerated Kxx.lean.
  T3  e66666F: the kc line of CGlue.cf66666 -> the rotation literal == COccBridge.lean's rot66666 (raw orientation of
      gen_occ_key.rotation), and the bridge's `rot` is its global reversal (Occ's orientation; documented, neutral).
  T4  walk form: gen_occ_kc --form walk (default) == the vendored occ24/gen_occ_walk.py program, all 49 keys (D00..D48 were
      compiled by Studio, walkD_results.txt, but are not committed), WALK_ASSUME on and off.
  T5  independent rotation: validate_rotation + derive_rotation agree with gen_occ_key.rotation on every kc line of the
      reference sets (49 keys, 2,855 Studio-D keys, CK108/CKQ5/CR118 extras, the CXRing/CCover*/CKQ5/CR118 Conf
      literals, RSST 633, nl51 8,200, the XR configs.in 12,700; --big adds the 23,721 loop/k* input lines); forcing the
      fallback (old routine disabled) gives the same modules up to the documented list-start / reversal normal form.
  T6  Conf literal: for every C/D registry entry (CCover3, CKQ5, CR118 XRData `cf`; gen_hd.py on the same kc lines) the
      generated `def cf` has the same name, r, m, ringAdj, intAdj, so `registry_cf = <NS>.cf` is `rfl`; gen_ccover3.py's
      EXTRAFILE branch regenerates the committed CKQ5 / CR118 entry blocks byte for byte (shared Conf path not regressed).
  T7  registry glue text: every generated COcc module has the eight registry theorems, balanced brackets, and the
      Python prechecks (rotOK, cf_sym, cf_loop, ring range, degrees) pass for every generated key.
  T8  fallback and refusal on synthetic kc lines (a link that is not an induced cycle; a ring position with no interior
      neighbour)."""
import sys, os, re, subprocess, argparse, tempfile, shutil, collections

HERE = os.path.dirname(os.path.abspath(__file__)); TOP = os.path.dirname(HERE)
sys.path.insert(0, TOP)
sys.argv, ARGS = sys.argv[:1], sys.argv[1:]
import gen_occ_kc as K   # noqa: E402

ap = argparse.ArgumentParser(); ap.add_argument('--rev', default='origin/main'); ap.add_argument('--ref-root')
ap.add_argument('--big', action='store_true'); ap.add_argument('--keep')
A = ap.parse_args(ARGS)
GITTOP = subprocess.run(['git', '-C', TOP, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
RB = 'backgroundMaterial/planemap-structural/longtable/reducibility/'
WD = RB + 'discharge/wheeldis/'
F2 = WD + 'loop/studio/opus_check/f2b041/'


def ref(path):
    if A.ref_root:
        return open(os.path.join(A.ref_root, path)).read()
    p = subprocess.run(['git', '-C', GITTOP, 'show', '%s:%s' % (A.rev, path)], capture_output=True)
    if p.returncode: raise FileNotFoundError('%s:%s' % (A.rev, path))
    return p.stdout.decode()


RES = []
def report(tid, ok, msg):
    RES.append((tid, ok)); print('%s %s  %s' % (tid, 'PASS' if ok else 'FAIL', msg)); sys.stdout.flush()


WORK = A.keep or tempfile.mkdtemp(prefix='s74reg_')
os.makedirs(WORK, exist_ok=True)
VEND = os.path.join(TOP, 'vendor')
print('occ24 generators imported from', K.OCC24, '; reference', A.ref_root or A.rev, '; work dir', WORK)
keys = [l for l in ref(RB + 'discharge/studio14b/k1_r17_19.txt').splitlines(True) if l.strip()]
assert len(keys) == 49

# ---------------------------------------------------------------------------------------------------------- T1
bad = []
for i, l in enumerate(keys):
    ns = 'K%02d' % i
    name, r, m, files = K.gen_one(l, ns, WORK, form='ring', bridge=False, write=False)
    if files[ns + '.lean'] != ref(RB + 'dcheck/occ24/%s.lean' % ns): bad.append(ns)
kf = os.path.join(WORK, 'k1_r17_19.txt'); open(kf, 'w').write(''.join(keys))
d1 = os.path.join(WORK, 'legacy'); os.makedirs(d1, exist_ok=True)
for i in (0, 41, 48):
    subprocess.run([sys.executable, os.path.join(TOP, 'gen_occ_kc.py'), kf, str(i), 'K%02d' % i, d1, '--no-bridge'], check=True,
                   capture_output=True)
    if open(os.path.join(d1, 'K%02d.lean' % i)).read() != ref(RB + 'dcheck/occ24/K%02d.lean' % i): bad.append('legacy K%02d' % i)
report('T1', not bad, '49 K=1 keys, ring form vs committed occ24/Kxx.lean: %d/49 byte-identical%s' % (49 - len([b for b in bad if not b.startswith('legacy')]),
       '' if not bad else ' differ: %s' % bad))

# ---------------------------------------------------------------------------------------------------------- T2
bad = []
d2 = os.path.join(WORK, 'ring'); os.makedirs(d2, exist_ok=True)
for i, l in enumerate(keys):
    ns = 'K%02d' % i
    name, r, m, files = K.gen_one(l, ns, d2, form='ring', bridge=True, registry=False)
    p = subprocess.run([sys.executable, os.path.join(VEND, 'gen_rotbridge.py'), os.path.join(d2, ns + '.lean'), ns, ns],
                       capture_output=True, text=True, check=True)
    if p.stdout != files['COcc%s.lean' % ns]: bad.append(ns)
    if i == 41:
        k41 = files['COcc%s.lean' % ns] == ref(RB + 'dcheck/COccK41.lean')
report('T2', k41 and not bad, 'bridge: COccK41 byte-identical=%s; 49/49 equal to vendored gen_rotbridge.py: %s' % (k41, not bad))

# ---------------------------------------------------------------------------------------------------------- T3
cg = ref(RB + 'dcheck/CGlue.lean'); cb = ref(RB + 'dcheck/COccBridge.lean')
mm = re.search(r'def cf66666 : DCheck18\.Conf :=\s*\{ name := "66666", r := (\d+), m := (\d+),\s*ringAdj := (#\[.*?\]\]),\s*'
               r'intAdj := (#\[.*?\]\]) \}', cg, re.S)
conv = lambda s: ';'.join(x.replace(' ', '') or '-' for x in re.findall(r'#\[([^\[\]]*)\]', s[2:-1]))
kc6 = '66666 %s %s %s %s' % (mm.group(1), mm.group(2), conv(mm.group(3)), conv(mm.group(4)))
name, r, m, ra, ia, canon = K.parse_kc(kc6)
raw = K.rotation_kc(r, m, ra, ia)
S = lambda u: '.inr %d' % (u - 1) if u <= r else '.inl %d' % (u - r - 1)
lit = lambda R: '[' + ', '.join('[' + ', '.join(R[v]) + ']' for v in sorted(R)) + ']'
want = re.search(r'def rot66666 : Fin 6 → List \(Fin 6 ⊕ ℕ\) :=\s*!(\[.*?\]\])\n', cb, re.S).group(1)
want = re.sub(r'\s+', ' ', want)
got_raw = lit({v: [S(u) for u in raw[v]] for v in raw})
_, _, _, f6 = K.gen_one(kc6, 'E66666', WORK, form='walk')
br = K.bridge_rot(f6['E66666.lean'])
brL = {a: ['.%s %d' % x for x in br[a]] for a in br}
rev_ok = all(K._cyc_eq(brL[a], [S(u) for u in raw[a + r + 1]][::-1]) for a in brL)
report('T3', got_raw == want and rev_ok, 'e66666F: kc line `%s` -> rotation literal == COccBridge rot66666: %s; generated bridge `rot` '
       '= its global reversal (Occ orientation): %s' % (kc6, got_raw == want, rev_ok))

# ---------------------------------------------------------------------------------------------------------- T4
bad = []
d4 = os.path.join(WORK, 'walk'); os.makedirs(d4, exist_ok=True)
for assume in (False, True):
    for i, l in enumerate(keys):
        ns = 'D%02d' % i
        name, r, m, files = K.gen_one(l, ns, d4, form='walk', walk_assume=assume, bridge=False, write=False)
        env = dict(os.environ); env['PYTHONPATH'] = VEND
        if assume: env['WALK_ASSUME'] = '1'
        else: env.pop('WALK_ASSUME', None)
        subprocess.run([sys.executable, os.path.join(VEND, 'gen_occ_walk.py'), kf, str(i), ns, d4], check=True, env=env)
        if open(os.path.join(d4, ns + '.lean')).read() != files[ns + '.lean']: bad.append((ns, assume))
report('T4', not bad, 'walk form == vendored gen_occ_walk.py, 49 keys x {derived dinj, WALK_ASSUME=1}: %d/98%s' % (98 - len(bad), '' if not bad else ' %s' % bad[:5]))

# ---------------------------------------------------------------------------------------------------------- T5
def kc_lines():
    yield 'k1_r17_19', keys
    yield 'k1_studioD', ref(RB + 'dcheck/occ24/k1_studioD.txt').splitlines(True)
    out = []
    for l in ref(F2 + 'ck108/names.txt').splitlines():
        n, tag, lines = l.split('\t')
        for k, x in enumerate(lines.split('|')): out.append('%s%s %s\n' % (n, '#%d' % k if '|' in lines else '', x.split(' @ ')[0]))
    for fn in ('ckq5/extra5.tsv', 'rsst118/extra118.tsv'):
        out += [l for l in ref(F2 + fn).splitlines(True) if l.strip()]
    yield 'ck108+ckq5+cr118', out
    lits = []
    pat = re.compile(r'name := "([^"]+)", r := (\d+), m := (\d+),\s*ringAdj := (#\[[^\n]*\]),\s*intAdj := (#\[[^\n]*\]) \}')
    for fn in (RB + 'dcheck/CXRing.lean', 'out/lean_ccover3/a6efb310/CCover3.lean', 'out/lean_ccover/1c56a79e/CCover.lean',
               'out/lean_ccover2/f2acc3e7/CCover2.lean', F2 + 'rsst118/lean/CR118.lean', F2 + 'ckq5/lean/CKQ5.lean'):
        for g in pat.finditer(ref(fn)):
            lits.append('%s %s %s %s %s\n' % (g.group(1), g.group(2), g.group(3), conv(g.group(4)), conv(g.group(5))))
    yield 'CXRing/CCover*/CR118/CKQ5 literals', lits
    rs = []
    for g in re.finditer(r'def cfg_(\d+) : Conf := \{ name := "([^"]+)", r := (\d+), m := (\d+), ringAdj := #\[(.*?)\], intAdj := #\[(.*?)\], rsst',
                         ref(RB + 'dcheck/DCheckData.lean')):
        c2 = lambda s: ';'.join(x.replace(' ', '') or '-' for x in re.findall(r'#\[([^\]]*)\]', s))
        rs.append('rsst%03d %s %s %s %s\n' % (int(g.group(1)), g.group(3), g.group(4), c2(g.group(5)), c2(g.group(6))))
    yield 'RSST DCheckData', rs
    yield 'nl51', ref(WD + 'loop/studio/opus_check/s39o/nl51_kc.txt').splitlines(True)
    yield 'XR configs.in', ref(WD + 'out/ext_reruns_a1d1317/in/configs.in').splitlines(True)
    if A.big:
        ls = subprocess.run(['git', '-C', GITTOP, 'ls-tree', '-r', '--name-only', A.rev, WD + 'loop'], capture_output=True, text=True).stdout.split()
        big = set()
        for fn in ls:
            if re.search(r'/k[0-9]+[^/]*/[^/ ]*\.(in|txt)$', fn):
                for l in ref(fn).splitlines(True):
                    f = l.split()
                    if len(f) == 5 and f[1].isdigit() and f[2].isdigit(): big.add(l)
        yield 'loop/k* inputs', sorted(big)

tot = 0; bad = []; per = []
K.STATS.clear()
for lab, lines in kc_lines():
    n = 0
    for l in lines:
        if not l.strip(): continue
        n += 1
        try:
            name, r, m, ra, ia, canon = K.parse_kc(l)
            old = K._orig_rotation(r, m, ra, ia)
            s, P = K.validate_rotation(r, m, ra, ia, old)
            new = K.derive_rotation(r, m, ra, ia)
            s2, P2 = K.validate_rotation(r, m, ra, ia, new)
            if P or P2 or not K.same_rotation(old, new) or s2 != 1: bad.append((lab, name, P[:1], P2[:1]))
        except Exception as e:
            bad.append((lab, l.split()[0], repr(e)[:80]))
    per.append('%s %d' % (lab, n)); tot += n
report('T5a', not bad, 'rotation: %d kc lines (%s): old routine valid, independent derivation valid, equal up to reversal; '
       'interior links that are not induced cycles: %d, with several Hamiltonian cycles: %d (so the rotation is forced)%s' % (
       tot, ', '.join(per), K.STATS['links_not_induced_cycle'], K.STATS['links_several_ham_cycles'], '' if not bad else ' FAILS %s' % bad[:5]))

# fallback path: the derivation alone (old routine disabled). Its lists start at the smallest label and read the ring
# forwards; aligning each list's start with the committed module's makes the output byte-identical again.
def _raise(*a): raise ValueError('disabled for the fallback test')
saved = K._orig_rotation; K._orig_rotation = _raise
same = 0; aligned = 0; badf = []
for i, l in enumerate(keys):
    ns = 'K%02d' % i
    try:
        name, r, m, files = K.gen_one(l, ns, WORK, form='ring', bridge=False, write=False)
    except Exception as e:
        badf.append((ns, repr(e)[:80])); continue
    old = ref(RB + 'dcheck/occ24/%s.lean' % ns)
    if files[ns + '.lean'] == old: same += 1; continue
    nm, r, m, ra, ia, canon = K.parse_kc(l)
    raw = saved(r, m, ra, ia)
    try: K.G.gen_occ(nm, r, raw, 'X'); E = raw
    except (KeyError, AssertionError): E = {v: c[::-1] for v, c in raw.items()}
    D = K.derive_rotation(r, m, ra, ia)
    Da = {}
    for v in D:
        j = D[v].index(E[v][0]); Da[v] = D[v][j:] + D[v][:j]
    K.G.rotation = lambda *a: {v: list(c) for v, c in Da.items()}
    try:
        _, _, _, f2 = K.gen_one(l, ns, WORK, form='ring', bridge=False, write=False)
        if f2[ns + '.lean'] == old: aligned += 1
        else: badf.append((ns, 'not equal after aligning list starts'))
    finally:
        K.G.rotation = K.rotation_kc
K._orig_rotation = saved
report('T5b', not badf and same + aligned == 49, 'fallback (derive_rotation only), 49 keys: %d byte-identical as is, %d byte-identical '
       'once each per-vertex list starts where the committed one starts (the only difference: list start)%s' % (same, aligned, '' if not badf else ' FAILS %s' % badf[:5]))

# ---------------------------------------------------------------------------------------------------------- T6
def cf_fields(text):
    out = {}
    for g in re.finditer(r'name := "([^"]+)", r := (\d+), m := (\d+),\s*ringAdj := (#\[[^\n]*\]),\s*intAdj := (#\[[^\n]*\]) \}', text):
        out.setdefault(g.group(1), set()).add((int(g.group(2)), int(g.group(3)), g.group(4), g.group(5)))
    return out
def gen_cf(kcline):
    name, r, m, ra, ia, canon = K.parse_kc(kcline)
    occ = K.occ_text(canon, 'X', 'walk')
    g = re.search(r'def cf : DCheck18\.Conf where\n  name := "(.*)"\n  r := (\d+)\n  m := (\d+)\n  ringAdj := (.*)\n  intAdj := (.*)\n', occ)
    return g.group(1), (int(g.group(2)), int(g.group(3)), g.group(4), g.group(5))
tot = 0; bad = []
for fn, ext in ((F2 + 'ckq5/lean/CKQ5.lean', F2 + 'ckq5/extra5.tsv'), (F2 + 'rsst118/lean/CR118.lean', F2 + 'rsst118/extra118.tsv')):
    reg = cf_fields(ref(fn))
    for l in ref(ext).splitlines():
        if not l.strip(): continue
        nm, fl = gen_cf(l); tot += 1
        if reg.get(nm) != {fl}: bad.append(nm)
cc3 = cf_fields(ref('out/lean_ccover3/a6efb310/CCover3.lean'))
# CCover3 entries were read from loop/k* inputs (name lookup); take their kc line from the committed literal itself
for nm, s in cc3.items():
    (r, m, ra, ia), = s
    l = '%s %d %d %s %s' % (nm, r, m, conv(ra), conv(ia)); n2, fl = gen_cf(l); tot += 1
    if fl != (r, m, ra, ia): bad.append(nm)
# gen_hd.py (Studio's D template) on the same kc lines writes the same literal
hd = os.path.join(WORK, 'hd'); os.makedirs(hd, exist_ok=True)
ef = os.path.join(hd, 'extra.tsv')
open(ef, 'w').write(ref(F2 + 'ckq5/extra5.tsv') + ref(F2 + 'rsst118/extra118.tsv'))
subprocess.run([sys.executable, os.path.join(VEND, 'gen_hd.py'), ef, hd, 'HDT', 'hdt', '50'], check=True, capture_output=True)
hdl = cf_fields(open(os.path.join(hd, 'HDT.lean')).read().replace('\n    ringAdj', ' ringAdj').replace('\n    intAdj', ' intAdj'))
for l in open(ef):
    if not l.strip(): continue
    nm, fl = gen_cf(l); tot += 1
    if hdl.get(nm) != {fl}: bad.append('hd:' + nm)
# gen_ccover3.py's EXTRAFILE branch regenerates the committed CKQ5 / CR118 entry blocks (shared Conf path)
fake = os.path.join(WORK, 'fakeW'); os.makedirs(os.path.join(fake, 'out', 'job30'), exist_ok=True)
open(os.path.join(fake, 'out', 'job30', 'k3x_C.cfast'), 'w').close()
blk = lambda t: re.search(r'(?s) := \[\n(.*?)\]\n\ntheorem', t).group(1)
regen = []
for fn, ext in ((F2 + 'ckq5/lean/CKQ5.lean', F2 + 'ckq5/extra5.tsv'), (F2 + 'rsst118/lean/CR118.lean', F2 + 'rsst118/extra118.tsv')):
    e2 = os.path.join(WORK, os.path.basename(ext)); open(e2, 'w').write(ref(ext))
    p = subprocess.run([sys.executable, os.path.join(VEND, 'gen_ccover3.py')], capture_output=True, text=True,
                       env=dict(os.environ, WHEELDIS=fake, EXTRAFILE=e2, ONLY=''))
    regen.append((os.path.basename(fn), p.returncode == 0 and blk(p.stdout) == blk(ref(fn))))
report('T6', not bad and all(x for _, x in regen), 'Conf literal: %d registry entries (CKQ5, CR118, CCover3, gen_hd.py) give the same '
       'name/r/m/ringAdj/intAdj as the generated `cf` (=> `rfl`)%s; gen_ccover3.py EXTRAFILE regenerates the committed entry '
       'blocks: %s' % (tot, '' if not bad else ' MISMATCH %s' % bad[:5], regen))

# ---------------------------------------------------------------------------------------------------------- T7
bad = []; n = 0
lines = list(keys) + [l for l in ref(F2 + 'ckq5/extra5.tsv').splitlines(True) if l.strip()] + [kc6]
for i, l in enumerate(lines):
    for form in ('walk', 'ring'):
        try:
            name, r, m, files = K.gen_one(l, 'Z%02d' % i, WORK, form=form, write=False)
        except Exception as e:
            bad.append((i, form, repr(e)[:80])); continue
        t = files['COccZ%02d.lean' % i]; n += 1
        ok = all(('theorem %s ' % x in t or 'def %s ' % x in t) and ('#print axioms SimpleGraph.SphericalMap.Z%02d.%s\n' % (i, x)) in t
                 for x in K.REG_NAMES)
        body = re.sub(r'/-.*?-/', '', t, flags=re.S)
        ok = ok and all(body.count(a) == body.count(b) for a, b in ('()', '[]', '{}', '⟨⟩'))
        ok = ok and ('ConfigOccW' in files['Z%02d.lean' % i]) == (form == 'walk')
        if not ok: bad.append((i, form))
report('T7', not bad, 'registry glue: %d COcc modules (49 keys, 5 CKQ5 entries, 66666; walk and ring), 8 registry declarations '
       'each, brackets balanced, prechecks pass%s' % (n, '' if not bad else ' FAILS %s' % bad[:5]))

# ---------------------------------------------------------------------------------------------------------- T8
# synthetic kc lines: syn1 has a degree-3 interior vertex inside the triangle (I0, R0, R1), so the link of I0 is not an
# induced cycle and gen_occ_key.rotation raises; the derivation must take over. syn2 leaves ring position 4 with no
# interior neighbour and must be refused before any Lean is written.
K.STATS.clear(); ok = True; msg = []
try:
    name, r, m, files = K.gen_one('syn1 5 2 0,1,2,3,4;0,1 1;0', 'SYN1', WORK, form='walk', write=False)
    ok = ok and K.STATS['old_rotation_raised'] > 0 and K.STATS['rotation_derived'] > 0 and 'COccSYN1.lean' in files
    msg.append('syn1 generated through the fallback (%s)' % dict(K.STATS))
except Exception as e:
    ok = False; msg.append('syn1 failed: %r' % e)
try:
    K.gen_one('syn2 5 1 0,1,2,3 -', 'SYN2', WORK, write=False); ok = False; msg.append('syn2 NOT refused')
except K.KcError as e:
    msg.append('syn2 refused: %s' % str(e)[:70])
report('T8', ok, '; '.join(msg))

if not A.keep: shutil.rmtree(WORK, ignore_errors=True)
print('ALL PASS' if all(ok for _, ok in RES) else 'SOME FAILED: %s' % [t for t, ok in RES if not ok])
sys.exit(0 if all(ok for _, ok in RES) else 1)
