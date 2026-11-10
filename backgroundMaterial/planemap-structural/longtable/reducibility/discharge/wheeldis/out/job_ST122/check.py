#!/usr/bin/env python3
"""ST-122 independent check of Opus's can_leave (189) and check (2) rows.

Run:  nice -n 15 python3 -I check.py      (single process, stdlib only; reads files, writes results.tsv + check.log here)

For every row:
  1. witness literal: found in our Lean data module (the one the hC / hD theorem is about), cross-checked against kc lines
  2. isomorphism RSST config (loop/k44/rsst.txt) vs witness literal: own canonical form (ring rotations, then mirror),
     and an independent direct backtracking matcher; both must agree
  3. build status of the hC (cReducible18) / hD (dReducible) theorem: status.txt line + #print axioms in the module log
  4. occurrence glue: any .lean glue file (Occ structure / colorable_of_occ ...) naming the witness, its literal and build status
"""
import os, re, sys, random

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.normpath(os.path.join(HERE, '..', '..'))                 # .../wheeldis
R = os.path.normpath(os.path.join(W, *(['..'] * 6)))                  # worktree root
DCHECK = os.path.join(R, 'backgroundMaterial/planemap-structural/longtable/reducibility/dcheck')
IN = os.path.join(HERE, 'in')
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    LOG.append(s)
    print(s)


# ---------------------------------------------------------------- configurations
def parse_kc(r, m, ra, ia):
    r, m = int(r), int(m)
    rl = [frozenset(int(x) for x in p.split(',') if x not in ('', '-')) for p in ra.split(';')]
    il = [frozenset(int(x) for x in p.split(',') if x not in ('', '-')) for p in ia.split(';')]
    return mk(r, m, rl, il)


def mk(r, m, rl, il):
    assert len(rl) == m and len(il) == m, ('length', r, m, len(rl), len(il))
    return (r, m, tuple(frozenset(x) for x in rl), tuple(frozenset(x) for x in il))


def validate(c):
    r, m, rl, il = c
    errs = []
    for v in range(m):
        if v in il[v]:
            errs.append('loop %d' % v)
        for u in il[v]:
            if not (0 <= u < m) or v not in il[u]:
                errs.append('asym %d-%d' % (v, u))
        for t in rl[v]:
            if not (0 <= t < r):
                errs.append('ring idx %d' % t)
    return errs


LIST_RE = r'#\[((?:\s*#\[[^\]]*\]\s*,?)*)\s*\]'
CONF_RE = re.compile(r'name := "([^"]+)"[,\s]+r := (\d+)[,\s]+m := (\d+)[,\s]+ringAdj := ' + LIST_RE +
                     r'[,\s]+intAdj := ' + LIST_RE, re.S)


def parse_lean_confs(text):
    out = []
    for mo in CONF_RE.finditer(text):
        name, r, m, ra, ia = mo.groups()
        rl = [[int(x) for x in s.replace(' ', '').split(',') if x] for s in re.findall(r'#\[([^\]]*)\]', ra)]
        il = [[int(x) for x in s.replace(' ', '').split(',') if x] for s in re.findall(r'#\[([^\]]*)\]', ia)]
        out.append((name, mk(int(r), int(m), rl, il), mo.start()))
    return out


def ringmap(c, s, t):
    r, m, rl, il = c
    return (r, m, tuple(frozenset((s * j + t) % r for j in x) for x in rl), il)


def mirror(c):
    return ringmap(c, -1, 0)


def perturb(c, kind, rng):
    """flip one adjacency: kind 'int' toggles an interior pair, 'ring' toggles a ring-interior incidence"""
    r, m, rl, il = c
    rl = [set(x) for x in rl]
    il = [set(x) for x in il]
    if kind == 'int':
        a, b = rng.sample(range(m), 2)
        if b in il[a]:
            il[a].discard(b); il[b].discard(a)
        else:
            il[a].add(b); il[b].add(a)
    else:
        a = rng.randrange(m); t = rng.randrange(r)
        if t in rl[a]:
            rl[a].discard(t)
        else:
            rl[a].add(t)
    return mk(r, m, rl, il)


def relabel(c, rng, s):
    """random interior permutation + random rotation (+ reflection if s=-1): must stay isomorphic"""
    r, m, rl, il = c
    p = list(range(m)); rng.shuffle(p)          # old v -> new p[v]
    t = rng.randrange(r)
    nrl = [None] * m; nil = [None] * m
    for v in range(m):
        nrl[p[v]] = frozenset((s * j + t) % r for j in rl[v])
        nil[p[v]] = frozenset(p[u] for u in il[v])
    return (r, m, tuple(nrl), tuple(nil))


# --- method 1: canonical form (colour refinement + individualisation), per ring map
def _refine(c, col):
    r, m, rl, il = c
    while True:
        sig = [(col[v], tuple(sorted(col[u] for u in il[v]))) for v in range(m)]
        keys = sorted(set(sig))
        new = [keys.index(sig[v]) for v in range(m)]
        if len(set(new)) == len(set(col)):
            return new
        col = new


def _leaves(c, col, acc):
    r, m, rl, il = c
    col = _refine(c, col)
    if len(set(col)) == m:
        order = sorted(range(m), key=lambda v: col[v])
        pos = {v: i for i, v in enumerate(order)}
        enc = tuple((tuple(sorted(rl[v])), tuple(sorted(pos[u] for u in il[v]))) for v in order)
        if acc[0] is None or enc < acc[0]:
            acc[0] = enc
        return
    cells = {}
    for v in range(m):
        cells.setdefault(col[v], []).append(v)
    cell = min((k for k in cells if len(cells[k]) > 1))
    for v in cells[cell]:
        nc = [2 * x + 1 for x in col]
        nc[v] = 2 * col[v]
        _leaves(c, nc, acc)


def canon_fixed_ring(c):
    r, m, rl, il = c
    init = [tuple(sorted(rl[v])) for v in range(m)]
    keys = sorted(set(init))
    acc = [None]
    _leaves(c, [keys.index(x) for x in init], acc)
    return (r, m, acc[0])


def canon_rot(c):
    return min(canon_fixed_ring(ringmap(c, 1, t)) for t in range(c[0]))


def iso_canon(a, b):
    if a[0] != b[0] or a[1] != b[1]:
        return 'no'
    cb = canon_rot(b)
    if canon_rot(a) == cb:
        return 'yes'
    if canon_rot(mirror(a)) == cb:
        return 'yes-mirror'
    return 'no'


# --- method 2: direct backtracking matcher
def _match(a, b):
    r, m, rla, ila = a
    _, _, rlb, ilb = b
    cand = []
    for v in range(m):
        cs = [u for u in range(m) if rlb[u] == rla[v] and len(ilb[u]) == len(ila[v])]
        if not cs:
            return False
        cand.append(cs)
    order = sorted(range(m), key=lambda v: len(cand[v]))
    img = {}; used = set()

    def bt(i):
        if i == m:
            return True
        v = order[i]
        for u in cand[v]:
            if u in used:
                continue
            ok = True
            for w, x in img.items():
                if (w in ila[v]) != (x in ilb[u]):
                    ok = False; break
            if ok:
                img[v] = u; used.add(u)
                if bt(i + 1):
                    return True
                del img[v]; used.discard(u)
        return False
    return bt(0)


def iso_direct(a, b):
    if a[0] != b[0] or a[1] != b[1]:
        return 'no'
    r = a[0]
    if any(_match(ringmap(a, 1, t), b) for t in range(r)):
        return 'yes'
    if any(_match(ringmap(a, -1, t), b) for t in range(r)):
        return 'yes-mirror'
    return 'no'


def iso(a, b):
    x, y = iso_canon(a, b), iso_direct(a, b)
    if x != y:
        log('!! iso methods disagree', x, y)
        return 'DISAGREE(%s/%s)' % (x, y)
    return x


# ---------------------------------------------------------------- Lean build evidence
ST_RE = re.compile(r'^(\S+) exit=(\S+) .*?sorry=(\d+) error=(\d+)')
AX_RE = re.compile(r"'([^']+)' depends on axioms: \[(.*?)\]", re.S)
_status_cache, _log_cache = {}, {}


def status_lines(d):
    if d not in _status_cache:
        res = {}
        p = os.path.join(d, 'status.txt')
        if os.path.exists(p):
            for ln in open(p):
                mo = ST_RE.match(ln.strip())
                if mo:
                    res.setdefault(mo.group(1), []).append((mo.group(2), int(mo.group(3)), int(mo.group(4)), ln.strip()))
        _status_cache[d] = res
    return _status_cache[d]


def module_status(d, module):
    st = status_lines(d)
    keys = [k for k in st if k == module or (module.endswith(k) and module[:-len(k)].isalpha() and k.isdigit())]
    lines = [x for k in keys for x in st[k]]
    if not lines:
        return None
    last = lines[-1]
    return {'exit': last[0], 'sorry': last[1], 'error': last[2], 'n': len(lines),
            'any_bad': any(x[0] != '0' for x in lines)}


def logs_in(d):
    if d not in _log_cache:
        res = {}
        for f in sorted(os.listdir(d)):
            if f.endswith('.log'):
                t = open(os.path.join(d, f), errors='replace').read()
                for mo in AX_RE.finditer(t):
                    res.setdefault(mo.group(1), []).append((f[:-4], [a.strip() for a in mo.group(2).split(',')], t))
        _log_cache[d] = res
    return _log_cache[d]


def axioms_ok(ax):
    bad = [a for a in ax if a not in ('propext', 'Classical.choice', 'Quot.sound') and '._native.native_decide.ax_' not in a]
    return bad


def theorem_evidence(d, thm):
    """module log printing thm's axioms + that module's status line"""
    hits = logs_in(d).get(thm, [])
    if not hits:
        return {'ok': False, 'txt': 'no #print axioms for %s in %s' % (thm, os.path.relpath(d, R))}
    mod, ax, text = hits[0]
    bad = axioms_ok(ax)
    errlines = [l for l in text.splitlines() if re.search(r'\berror\b', l)]
    st = module_status(d, mod)
    ok = not bad and not errlines and st is not None and st['exit'] == '0' and st['sorry'] == 0 and st['error'] == 0
    txt = '%s in %s.log: axioms %s; status %s' % (
        thm, mod, 'std+native_decide' if not bad else 'BAD ' + ','.join(bad),
        'missing' if st is None else 'exit=%s sorry=%d error=%d' % (st['exit'], st['sorry'], st['error']))
    if errlines:
        txt += '; log error lines %d' % len(errlines)
    return {'ok': ok, 'txt': txt, 'module': mod}


# ---------------------------------------------------------------- Lean data families
FAM = {  # theorem namespace -> (data module, list name, build dir, All module)
    'CXI': (os.path.join(R, 'out/lean_cxint/95ba762d/CXInt.lean'), 'xiEntries', os.path.join(R, 'out/lean_cxint/95ba762d'), 'CXIAll'),
    'CXR': (os.path.join(DCHECK, 'CXRing.lean'), 'xrEntries', os.path.join(R, 'out/lean_cxring/2a4bc4cf'), 'CXRAll'),
    'CCV': (os.path.join(R, 'out/lean_ccover/1c56a79e/CCover.lean'), 'ccEntries', os.path.join(R, 'out/lean_ccover/1c56a79e'), 'CCAll'),
    'CC2V': (os.path.join(R, 'out/lean_ccover2/f2acc3e7/CCover2.lean'), 'cc2Entries', os.path.join(R, 'out/lean_ccover2/f2acc3e7'), 'CC2All'),
    'CC3V': (os.path.join(R, 'out/lean_ccover3/a6efb310/CCover3.lean'), 'cc3Entries', os.path.join(R, 'out/lean_ccover3/a6efb310'), 'CC3All'),
    'K108V': (os.path.join(W, 'loop/studio/opus_check/f2b041/ck108/lean/CK108.lean'), 'k108Entries',
              os.path.join(W, 'loop/studio/opus_check/f2b041/ck108/lean'), 'K108All'),
    'A5CV': (os.path.join(W, 'out/job_HA5/hc/CA5C.lean'), 'a5cEntries', os.path.join(W, 'out/job_HA5/hc'), 'A5CVAll'),
    'HDCV': (os.path.join(W, 'out/job_HDC502/lean/HDC.lean'), 'hdcConfs', os.path.join(W, 'out/job_HDC502/lean'), 'HDCAll'),
}
DATA = {}


def fam_data(ns):
    if ns not in DATA:
        path, lst, d, allm = FAM[ns]
        text = open(path).read()
        i = text.index('def %s' % lst)
        confs = parse_lean_confs(text[i:])
        xs = [None] * len(confs)
        if ns != 'HDCV':   # XRData: X := "..." precedes cf
            for k, (nm, c, pos) in enumerate(confs):
                seg = text[i:i + pos]
                mx = list(re.finditer(r'X := "([^"]*)"', seg))
                xs[k] = mx[-1].group(1) if mx else None
        DATA[ns] = (confs, xs)
    return DATA[ns]


def all_evidence(ns):
    path, lst, d, allm = FAM[ns]
    hits = [h for thm, hs in logs_in(d).items() for h in hs if h[0] == allm and thm.endswith('.hC_all') or
            (h[0] == allm and thm.endswith('.hD_all'))]
    st = module_status(d, allm)
    if not hits:
        return 'All module %s: no axioms print' % allm
    bad = axioms_ok(hits[0][1])
    return '%s: axioms %s; status %s' % (allm, 'std+native_decide' if not bad else 'BAD',
                                         'none in status.txt (log only)' if st is None else 'exit=%s' % st['exit'])


def lookup_entry(ns, name):
    confs, xs = fam_data(ns)
    ks = [k for k, (nm, c, p) in enumerate(confs) if nm == name]
    return [(k, confs[k][1], xs[k]) for k in ks]


# ---------------------------------------------------------------- glue scan
GLUE_MARK = re.compile(r'colorable_of_occ|colorable_of_mirror_occ|occursCXF_of_occ|occursW_of_occ|structure Occ\b')


def scan_glue(names):
    """name -> list of (path, literal-or-None)"""
    names = set(names)
    out = {n: [] for n in names}
    nfiles = 0
    for root, dirs, files in os.walk(R):
        dirs[:] = [x for x in dirs if x not in ('.lake', '.git', 'node_modules')]
        for f in files:
            if not f.endswith('.lean'):
                continue
            p = os.path.join(root, f)
            try:
                t = open(p, errors='replace').read()
            except OSError:
                continue
            if not GLUE_MARK.search(t):
                continue
            nfiles += 1
            found = set(re.findall(r'"([^"\s]+)"', t)) | set(re.findall(r'`([^`\s]+)`', t))
            hit = found & names
            if hit:
                lits = {nm: c for nm, c, _ in parse_lean_confs(t)}
                for n in hit:
                    out[n].append((p, lits.get(n)))
    return out, nfiles


# ---------------------------------------------------------------- main
def main():
    rng = random.Random(122)
    # RSST kc lines
    rsst = {}
    for ln in open(os.path.join(W, 'loop/k44/rsst.txt')):
        p = ln.split()
        if len(p) == 5:
            rsst[p[0]] = parse_kc(*p[1:])
    verd = {}
    for ln in open(os.path.join(W, 'loop/k44/rsst_verdicts.txt')):
        mo = re.match(r'(rsst\S+) .*verdict=(\S+)(?: X=(\S+))?', ln)
        if mo:
            verd[mo.group(1)] = (mo.group(2), mo.group(3) or '-')
    log('rsst.txt configs:', len(rsst), '; verdicts:', len(verd))

    # our records
    memb = {}
    for ln in open(os.path.join(W, 'out/job_JCOV/coverage/lean_membership.tsv')):
        if ln.startswith('#'):
            continue
        p = ln.rstrip('\n').split('\t')
        if len(p) >= 3:
            memb.setdefault(p[0], []).append((p[1], p[2]))
    dtodo = {}
    for ln in open(os.path.join(W, 'out/job_HDC502/D_todo.tsv')):
        p = ln.rstrip('\n').split('\t')
        if len(p) == 2:
            dtodo[p[0]] = parse_kc(*p[1].split())
    a5extra = {}
    for ln in open(os.path.join(W, 'out/job_HA5/hc/in/glue/extraC.tsv')):
        p = ln.rstrip('\n').split('\t')
        if len(p) >= 2:
            a5extra[p[0]] = parse_kc(*p[1].split())
    kcfiles = [os.path.join(W, 'loop/k44/pats44_f.txt')]
    kcidx = {}
    for f in kcfiles:
        for ln in open(f):
            p = ln.split()
            if len(p) == 5 and p[1].isdigit():
                kcidx.setdefault(p[0], (os.path.relpath(f, W), parse_kc(*p[1:])))

    # rows
    rows = []
    for fn, cls in (('queue403_can_leave.tsv', None), ('queue403_check.tsv', 'check')):
        lines = [l.rstrip('\n').split('\t') for l in open(os.path.join(IN, fn))]
        hdr = lines[0]
        for p in lines[1:]:
            d = dict(zip(hdr, p))
            d['cls'] = cls or d['verdict']
            rows.append(d)
    log('rows:', len(rows), {c: sum(1 for d in rows if d['cls'] == c) for c in ('C2cons', 'D2', 'check')})

    results = []
    for d in rows:
        rid, cls = d['rsst_id'], d['cls']
        cfg = rsst.get(rid)
        res = {'idx': d['idx'], 'rsst_id': rid, 'name': d['name'], 'verdict': d['verdict'], 'class': cls}
        notes = []
        v = verd.get(rid, ('?', '?'))
        res['rsst_X'] = v[1]
        if v[0] != d['verdict']:
            notes.append('verdict mismatch vs rsst_verdicts.txt (%s)' % v[0])
        if cfg is None:
            res.update(witness='-', literal='-', iso='-', build='-', glue='-', final='FAILED', reason='rsst config not in rsst.txt')
            results.append(res); continue
        if validate(cfg):
            notes.append('rsst literal invalid: ' + ';'.join(validate(cfg)))
        # witness name + theorem
        ev = d['lean_copy_evidence']
        if cls == 'C2cons':
            mo = re.match(r'pattern C (\S+) \(', d['witness'])
            w = mo.group(1) if mo else None
            mo2 = re.match(r'witness (\S+) has ', ev)
            if not mo2 or mo2.group(1) != w:
                notes.append('witness column and lean_copy_evidence disagree')
        else:
            mo = re.search(r'isomorphic to (\S+) ', ev)
            w = mo.group(1) if mo else None
        res['witness'] = w or '-'
        cands = []   # (ns, k, conf, X, thm)
        if cls == 'C2cons':
            ms = memb.get(w, [])
            res['membership'] = ' | '.join('%s: %s' % m for m in ms) or '-'
            for lst, txt in ms:
                for mo in re.finditer(r'\b(CXI|CXR|CCV|CC2V|CC3V|K108V)\.hC_(\d+|all)\b', txt):
                    ns, kk = mo.group(1), mo.group(2)
                    for k, c, X in lookup_entry(ns, w):
                        if kk == 'all' or int(kk) == k:
                            if (ns, k) not in [(x[0], x[1]) for x in cands]:
                                cands.append((ns, k, c, X, '%s.hC_%d' % (ns, k)))
            if not ms:
                notes.append('witness not in lean_membership.tsv')
        elif cls == 'D2':
            res['membership'] = 'D_todo.tsv' if w in dtodo else '-'
            for k, c, X in lookup_entry('HDCV', w):
                cands.append(('HDCV', k, c, None, 'HDCV.hD_%d' % k))
        else:
            res['membership'] = 'HA5 extraC.tsv' if w in a5extra else '-'
            for k, c, X in lookup_entry('A5CV', w):
                cands.append(('A5CV', k, c, X, 'A5CV.hC_%d' % k))
        if not cands:
            res.update(literal='NOT FOUND', iso='-', build='-', glue='-', final='FAILED', reason='witness literal not found in a built Lean data module; ' + '; '.join(notes))
            results.append(res); continue
        ns, k, wc, X, thm = cands[0]
        if len(cands) > 1:
            notes.append('%d Lean copies; first used' % len(cands))
        res['witness_X'] = X or '-'
        src = '%s %s[%d] (%s)' % (os.path.relpath(FAM[ns][0], R), FAM[ns][1], k, ns)
        cross = []
        if validate(wc):
            notes.append('witness literal invalid: ' + ';'.join(validate(wc)))
        if w in kcidx:
            cross.append('kc %s: %s' % (kcidx[w][0], 'identical' if kcidx[w][1] == wc else 'iso=' + iso(kcidx[w][1], wc)))
        if cls == 'D2' and w in dtodo:
            cross.append('D_todo kc: %s' % ('identical' if dtodo[w] == wc else 'iso=' + iso(dtodo[w], wc)))
        if cls == 'check' and w in a5extra:
            cross.append('extraC kc: %s' % ('identical' if a5extra[w] == wc else 'iso=' + iso(a5extra[w], wc)))
        for ns2, k2, c2, X2, thm2 in cands[1:]:
            cross.append('%s[%d]: %s' % (ns2, k2, 'identical' if c2 == wc else 'iso=' + iso(c2, wc)))
        res['literal'] = src + ('; ' + '; '.join(cross) if cross else '')
        if any(('iso=no' in x or 'DISAGREE' in x) for x in cross):
            notes.append('a second copy of the witness literal differs')
        # iso
        res['iso'] = iso(cfg, wc)
        res['_wc'] = wc
        # build
        be = theorem_evidence(FAM[ns][2], thm)
        res['build'] = ('OK ' if be['ok'] else 'NOT OK ') + be['txt'] + '; ' + all_evidence(ns)
        res['_build_ok'] = be['ok']
        res['_notes'] = notes
        res['_ns'] = ns
        results.append(res)

    # glue
    wit = sorted({r['witness'] for r in results if r.get('witness', '-') != '-'})
    log('scanning .lean files for occurrence glue on %d witness names ...' % len(wit))
    glue, nfiles = scan_glue(wit)
    log('glue-type .lean files scanned:', nfiles)
    for r in results:
        if 'iso' not in r or r.get('literal') == 'NOT FOUND':
            continue
        g = glue.get(r['witness'], [])
        det = []
        okg = False
        for p, lit in g:
            rp = os.path.relpath(p, W if p.startswith(W) else R)
            mod = os.path.basename(p)[:-5]
            st = module_status(os.path.dirname(p), mod)
            stt = 'no status' if st is None else 'exit=%s sorry=%d' % (st['exit'], st['sorry'])
            lt = '-' if lit is None else ('identical' if lit == r['_wc'] else 'iso=' + iso(lit, r['_wc']))
            if '/in/' not in p:
                det.append('%s [%s; literal %s]' % (rp, stt, lt))
                if st is not None and st['exit'] == '0' and st['sorry'] == 0 and lt in ('identical', '-', 'iso=yes', 'iso=yes-mirror'):
                    okg = True
        r['glue'] = 'yes' if okg else ('listed-unbuilt' if det else 'no')
        r['glue_detail'] = ' ; '.join(det) if det else '-'

    # verdicts
    for r in results:
        if 'final' in r:
            continue
        notes = r['_notes']
        why = []
        if r['iso'] not in ('yes', 'yes-mirror'):
            why.append('witness NOT isomorphic to the RSST config (iso=%s)' % r['iso'])
        if not r['_build_ok']:
            why.append('build evidence incomplete')
        if any('differs' in n or 'invalid' in n for n in notes):
            why.append('; '.join(notes))
        if why:
            r['final'] = 'FAILED'; r['reason'] = '; '.join(why)
        else:
            r['final'] = 'CONFIRMED'
            rs = ['iso %s' % r['iso'], '%s built' % r['build'].split(' in ')[0].replace('OK ', '')]
            if r['class'] == 'C2cons':
                rs.append('witness X %s vs RSST X %s' % (r.get('witness_X'), r.get('rsst_X')))
            rs.append('glue ' + r['glue'])
            rs += notes
            r['reason'] = '; '.join(rs)

    # alternative Lean copies for non-iso rows
    bad = [r for r in results if r.get('iso') == 'no']
    if bad:
        idx = {}
        for ns in FAM:
            for k, (nm, c, p) in enumerate(fam_data(ns)[0]):
                idx.setdefault((c[0], c[1]), []).append((ns, k, nm, c))
        for r in bad:
            cfg = rsst[r['rsst_id']]
            alts = [(ns, k, nm) for ns, k, nm, c in idx.get((cfg[0], cfg[1]), []) if iso(cfg, c) != 'no']
            r['reason'] += '; iso Lean copies elsewhere: ' + (', '.join('%s[%d]=%s' % a for a in alts) or 'none')

    # controls
    log('--- controls')
    ctl = {'self': [0, 0], 'relabel_rot': [0, 0], 'relabel_mirror': [0, 0], 'perturb_int': [0, 0], 'perturb_ring': [0, 0],
           'perturb_int_vs_witness': [0, 0], 'perturb_ring_vs_witness': [0, 0], 'mirror_only_detected': [0, 0]}
    for r in results:
        if 'iso' not in r or r.get('literal') == 'NOT FOUND':
            continue
        cfg = rsst[r['rsst_id']]; wc = r['_wc']
        for c in (cfg, wc):
            ctl['self'][0] += 1; ctl['self'][1] += iso(c, c) == 'yes'
            x = relabel(c, rng, 1)
            ctl['relabel_rot'][0] += 1; ctl['relabel_rot'][1] += iso(c, x) == 'yes'
            x = relabel(c, rng, -1)
            ctl['relabel_mirror'][0] += 1; ctl['relabel_mirror'][1] += iso(c, x) in ('yes', 'yes-mirror')
        for kind in ('int', 'ring'):
            p = perturb(cfg, kind, rng)
            ctl['perturb_' + kind][0] += 1; ctl['perturb_' + kind][1] += iso(cfg, p) == 'no'
            ctl['perturb_%s_vs_witness' % kind][0] += 1; ctl['perturb_%s_vs_witness' % kind][1] += iso(p, wc) == 'no'
    # a chiral control: find a config not iso to its own mirror under rotation; iso(c, mirror c) must say yes-mirror
    for r in results:
        if r.get('iso') in ('yes', 'yes-mirror'):
            c = rsst[r['rsst_id']]
            if iso_canon(c, mirror(c)) == 'yes-mirror':
                ctl['mirror_only_detected'][0] += 1
                ctl['mirror_only_detected'][1] += iso_direct(c, mirror(c)) == 'yes-mirror'
    for k, (n, ok) in ctl.items():
        log('control %-24s %d / %d as expected' % (k, ok, n))

    # write
    cols = ['idx', 'rsst_id', 'name', 'verdict', 'class', 'witness', 'literal', 'iso', 'build', 'glue', 'glue_detail',
            'membership', 'witness_X', 'rsst_X', 'final', 'reason']
    with open(os.path.join(HERE, 'results.tsv'), 'w') as f:
        f.write('# ST-122 check (check.py). class: C2cons / D2 = queue403_can_leave rows, check = queue403_check rows.\n')
        f.write('\t'.join(cols) + '\n')
        for r in results:
            f.write('\t'.join(str(r.get(c, '-')).replace('\t', ' ') for c in cols) + '\n')
    log('--- summary')
    for cls in ('C2cons', 'D2', 'check'):
        rs = [r for r in results if r['class'] == cls]
        log('%-7s rows %3d  CONFIRMED %3d  FAILED %3d  iso yes %3d  yes-mirror %3d  no %d  glue yes %3d  no %3d  other %d' % (
            cls, len(rs), sum(r['final'] == 'CONFIRMED' for r in rs), sum(r['final'] == 'FAILED' for r in rs),
            sum(r.get('iso') == 'yes' for r in rs), sum(r.get('iso') == 'yes-mirror' for r in rs), sum(r.get('iso') == 'no' for r in rs),
            sum(r.get('glue') == 'yes' for r in rs), sum(r.get('glue') == 'no' for r in rs),
            sum(r.get('glue') not in ('yes', 'no') for r in rs)))
    for r in results:
        if r['final'] == 'FAILED':
            log('FAILED', r['idx'], r['name'], r['witness'], r['reason'])
    by_ns = {}
    for r in results:
        k = (r['class'], r.get('_ns', '-'), r.get('glue', '-'))
        by_ns[k] = by_ns.get(k, 0) + 1
    for k in sorted(by_ns):
        log('family', k, by_ns[k])
    with open(os.path.join(HERE, 'check.log'), 'w') as f:
        f.write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    main()
