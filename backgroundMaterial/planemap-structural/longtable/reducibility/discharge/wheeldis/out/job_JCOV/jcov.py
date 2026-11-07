"""JCOV (Studio, ST-5): Lean / engine coverage of every justifier in keep95p131f/rule_provenance.tsv (45a4c6d1).
Identity: a justifier's own kc line (name r m ringadj intadj, from the forbidden-set sources f2b_rulecheck reads) is matched
against every Conf literal in our Lean files (jcov_index.py JSON) by (r, m, sorted ring lists, sorted interior lists);
RSST justifiers rsstNNN are matched to DCheckData cfg_NNN (unavoidable.conf order) and checked by interior degrees.
A literal counts as Lean-backed through: a `get` theorem (hD_k / hC_k on list[k]), an `all` theorem (Fin n), a `run`
theorem with reached = classes (D), a `dred` theorem, or an agreesRSST theorem (explicit list, or rsst.filter by r) for an
RSST D2 entry (rsstContract = 0, so agreesRSST asserts reached = classes).
Engine evidence (no Lean): nl51 from explore round 54d (6368d2f5: loop/k53/nl54d_verdicts.txt, per-config kc / dfast lines
in loop/k5x/*_kcc.out / *_df.out) and Studio job54d / job54e (8fd249f6: A_kcc.out kc, A_df.out dfast18); k3x / k3p from
their registry files (tierA/k3x_D_A100.out kc lines with D=true, k3p_D.out 'two engines'); RSST from loop/k44/rsst_verdicts.txt.
usage: python3 jcov.py INDEX.json OUTDIR"""
import sys, os, json, re, collections, subprocess
IDX, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
WD = os.getcwd()   # wheeldis
ROOT = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
F = 'loop/studio/opus_check/f2b041/'; K = F + 'keep95p131f/'
def gshow(c, p):
    return subprocess.run(['git', 'show', '%s:%s' % (c, os.path.relpath(os.path.join(WD, p), ROOT))], capture_output=True, text=True).stdout
# ---- justifiers ----
cite = collections.Counter(); sole = collections.Counter()
for l in open(K + 'rule_provenance.tsv'):
    if l.startswith('#'): continue
    f = l.rstrip('\n').split('\t'); ns = [n for n in f[4].split(',') if n]
    for n in ns: cite[n] += 1
    if len(ns) == 1: sole[ns[0]] += 1
W18 = json.load(open(K + 'rot/in/rules_zcons_minus_W18rejects.json'))
inW18 = set()
W18set = set()
for g, v in W18.items():
    for sg, L in ([('0', v)] if isinstance(v, list) else v.items()):
        for r in L: W18set.add((g, sg, json.dumps(r)))
for l in open(K + 'rule_provenance.tsv'):
    if l.startswith('#'): continue
    f = l.rstrip('\n').split('\t')
    if (f[0], f[2], json.dumps(json.loads(f[1]))) in W18set:
        for n in f[4].split(','):
            if n: inW18.add(n)
# ---- source classes (as PROV5F) ----
rd = lambda fn: {l.split()[0] for l in open(fn) if l.strip() and not l.startswith('#')}
lean531 = rd(F + 'keep/keep_lean_C.txt'); r118 = rd(F + 'rsst118/names118.txt'); ck108 = rd(F + 'ck108/names.txt'); q5 = rd(F + 'ckq5/names.txt')
core = rd(F + 'keep95/core95.txt'); k13 = {n for n in rd(F + 'keep95/dropnames_cover.txt') if not n.startswith('rsst')}
nl51 = {}; [nl51.setdefault(l.split()[0], l.strip()) for l in open(F + 'tierA/nl51_kc.txt') if l.strip()]
k3pD = {}; [k3pD.setdefault(l.split()[0], l) for l in open(F + 'tierA/k3p_D.out') if l.strip() and not l[0].isspace()]
k3xD = {}
for l in open(F + 'tierA/k3x_D_A100.out'):
    m = re.match(r'^(\S+) r=\d+ .*D=true', l)
    if m: k3xD[m[1]] = l.strip()
leanR = {x.split('_')[0] for x in lean531 if x.startswith('rsst')}
def src(n):
    if n.startswith('rsst'):
        return 'C rsst118' if n in r118 else ('C Lean531 (RSST)' if n in leanR else 'D RSST')
    if n in lean531: return 'C Lean531'
    if n in core: return 'C core95'
    if n in k13: return 'C k3x13'
    if n in nl51: return 'D nl51'
    if n in k3pD: return 'D k3p'
    if n in k3xD: return 'D k3x'
    return 'other'
# ---- kc lines of the justifiers (the forbidden-set sources) ----
sys.argv = ['f2b_rulecheck.py', 'x', 'y']
for k_, v_ in (('EXTRA_KC', F + 'tierA/nl51_kc.txt,' + F + 'tierA/k3p_D.out,' + K + 'k3p_C_keep95p131f.cfast'),
               ('K3X', F + 'tierA/k3x_D_A100.out,' + K + 'k3x_C_A100_keep95p131f.cfast'), ('RSSTC_KEEP', K + 'keep95p131f_C.txt')):
    os.environ[k_] = v_
M = {'__name__': 'jcov', '__file__': os.path.abspath('out/job31/f2b_rulecheck.py')}
exec(open('out/job31/f2b_rulecheck.py').read(), M)
RAW = M['RAWKC']
def key(r, m, ra, ia):
    return (int(r), int(m), tuple(tuple(sorted(x)) for x in ra), tuple(tuple(sorted(x)) for x in ia))
def kckey(line):
    f = line.split(); r, m = f[1], f[2]
    p = lambda s: [[] if g == '-' else [int(x) for x in g.split(',')] for g in s.split(';')]
    return key(r, m, p(f[3]), p(f[4]))
# ---- Lean index ----
J = json.load(open(IDX)); ents = J['ents']; thms = J['thms']
byget = collections.defaultdict(list); bydef = collections.defaultdict(list); agree_cfg = collections.defaultdict(list); agreeR = []
for t in thms:
    if t['how'] in ('get', 'all'): byget[(t['defn'], t['idx'])].append(t)
    elif t['how'] in ('run', 'dred'):
        if t['kind'] == 'D': bydef[t['defn']].append(t)
    elif t['how'] == 'agree': agree_cfg[t['defn']].append(t)
    elif t['how'].startswith('agreeR'): agreeR.append(t)
ekey = collections.defaultdict(list)
for e in ents: ekey[key(e['r'], e['m'], e['ra'], e['ia'])].append(e)
def lean_of(e, kind):
    out = []
    for t in byget.get((e['defn'], e['idx']), []):
        if t['kind'] == kind: out.append(t)
    if kind == 'D' and e['defn'] and e['defn'].startswith('cfg_'):
        out += bydef.get(e['defn'], [])
    return out
# RSST: DCheckData cfg_i <-> rsst%03d
dd = [e for e in ents if e['file'].endswith('dcheck/DCheckData.lean') and e['defn'] and re.match(r'cfg_\d+$', e['defn'])]
ddm = {int(e['defn'][4:]): e for e in dd}
contract0 = set()
for l in open(os.path.join(ROOT, 'backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/DCheckData.lean')):
    m = re.match(r'def (cfg_\d+) : Conf := .*rsstContract := 0 \}', l)
    if m: contract0.add(m[1])
rsstcfg = {c[0]: c for c in M['FORB'] if c[0].startswith('rsst')}
ver = {}
for l in open('loop/k44/rsst_verdicts.txt'):
    if l.startswith('#') or not l.strip(): continue
    f = l.split(); v = [x for x in f if x.startswith('verdict=')]; ver[f[0].split('_')[0]] = v[0][8:] if v else None
def rsst_lean(n):
    i = int(n[4:]); e = ddm.get(i)
    if e is None: return [], 'no DCheckData cfg_%d' % i
    c = rsstcfg.get(n)
    if c and sorted(c[3].values()) != sorted(len(a) + len(b) for a, b in zip(e['ra'], e['ia'])): return [], 'degree mismatch cfg_%d' % i
    t = list(agree_cfg.get('cfg_%d' % i, []))
    for a in agreeR:
        cond = a['how'].split(':', 1)[1]; r = e['r']
        if ('≤ 9' in cond and '10 ≤' not in cond and r <= 9) or ('10 ≤ c.r && c.r ≤ 11' in cond and 10 <= r <= 11): t.append(a)
    t += bydef.get('cfg_%d' % i, [])
    return (t if 'cfg_%d' % i in contract0 else []), ('cfg_%d contract0=%s' % (i, 'cfg_%d' % i in contract0))
# ---- engine evidence for nl51 ----
NLE = collections.defaultdict(dict)   # name -> {engine: (verdict, file@sha)}
P54 = 'loop/k5%s/%s'
for fn in ('k51/F', 'k53/G', 'k53/N54', 'k53/T', 'k54/A'):
    for suf, eng in (('_kcc.out', 'kc'), ('_df.out', 'dfast')):
        txt = gshow('6368d2f5', 'loop/%s%s' % (fn, suf))
        for l in txt.splitlines():
            if not l.strip() or l[0].isspace(): continue
            n = l.split()[0]
            if n in nl51 and eng not in NLE[n]: NLE[n][eng] = ('D' if 'D=true' in l else 'notD', 'loop/%s%s@6368d2f5' % (fn, suf))
for jd in ('job54d', 'job54e'):
    for suf, eng in (('A_kcc.out', 'kc'), ('A_df.out', 'dfast18')):
        for l in gshow('8fd249f6', 'out/%s/%s' % (jd, suf)).splitlines():
            if not l.strip() or l[0].isspace(): continue
            n = l.split()[0]
            if n in nl51 and eng not in NLE[n]: NLE[n][eng] = ('D' if 'D=true' in l else 'notD', 'out/%s/%s@8fd249f6' % (jd, suf))
V54 = {}
for l in gshow('6368d2f5', 'loop/k53/nl54d_verdicts.txt').splitlines():
    f = l.split()
    if len(f) == 4 and not l.startswith('#'): V54[f[0]] = (f[2], f[3])
# ---- rows ----
rows = []; stat = collections.Counter(); single_noLean = 0; single_noLean_W18 = 0
for n in sorted(cite):
    s = src(n); kind = s[0]; lean = []; how = ''
    if s == 'D RSST' or (s.startswith('C') and n.startswith('rsst') and False):
        lean, how = rsst_lean(n)
    else:
        line = RAW.get(n)
        if line is None and n in rsstcfg: line = None
        if line:
            for e in ekey.get(kckey(line), []): lean += lean_of(e, kind)
            if not lean:   # same name, same r and m (relabelled literal)
                f_ = line.split()
                for e in ents:
                    if e['name'] == n and e['r'] == int(f_[1]) and e['m'] == int(f_[2]): lean += lean_of(e, kind); how = 'name'
        elif n.startswith('rsst'):
            # RSST C (rsst118 / Lean531 RSST): XRData literals named rsstNNN_*
            for e in ents:
                if e['name'].split('_')[0] == n or e['name'] == n: lean += lean_of(e, 'C')
            how = 'RSST C by name'
    mods = sorted({'%s (%s%s)' % (t['thm'], os.path.basename(t['file']), '' if t.get('tracked', True) else ', local only') for t in lean})
    eng = []; ev = []
    if s == 'D nl51':
        for k_, (v, p) in sorted(NLE.get(n, {}).items()): eng.append('%s:%s' % (k_, v)); ev.append(p)
        if n in V54: eng.append('nl54d:%s(%s)' % V54[n]); ev.append('loop/k53/nl54d_verdicts.txt@6368d2f5')
    elif s == 'D k3x': eng.append('kc:D (registry line)'); ev.append(F + 'tierA/k3x_D_A100.out')
    elif s == 'D k3p': eng.append('two engines (registry line)'); ev.append(F + 'tierA/k3p_D.out')
    elif s == 'D RSST': eng.append('rsst_verdicts:%s' % ver.get(n)); ev.append('loop/k44/rsst_verdicts.txt')
    elif s.startswith('C'): eng.append('C keep list'); ev.append(K + 'keep95p131f_C.txt')
    cls = 'Lean' if mods else ('engine-only' if eng else 'none')
    stat[(s, cls)] += 1
    if not mods and sole[n]: single_noLean += sole[n]; single_noLean_W18 += sole[n] if n in inW18 else 0
    rows.append((n, kind, s, cite[n], sole[n], 'yes' if n in inW18 else 'no', '; '.join(mods) or '-', ' '.join(eng) or '-', ' '.join(ev) or '-', how))
with open(os.path.join(OUT, 'justifier_coverage.tsv'), 'w') as f:
    f.write('# name\tkind\tsource\tn_rules_citing\tn_single_justifier_rules\tcited_by_a_2b362955_rule\tlean_module\tengines\tevidence\tmatch_note\n')
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
summ = collections.defaultdict(collections.Counter)
for (s, c), v in stat.items(): summ[s][c] += v
json.dump({'by_source': {k: dict(v) for k, v in summ.items()}, 'single_justifier_rules_on_noLean_justifier': single_noLean,
           'of_them_on_justifiers_cited_by_2b362955': single_noLean_W18}, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1)
print(json.dumps({k: dict(v) for k, v in summ.items()}), 'single-justifier rules resting on a no-Lean justifier:', single_noLean, '(W18-cited justifiers:', single_noLean_W18, ')')
