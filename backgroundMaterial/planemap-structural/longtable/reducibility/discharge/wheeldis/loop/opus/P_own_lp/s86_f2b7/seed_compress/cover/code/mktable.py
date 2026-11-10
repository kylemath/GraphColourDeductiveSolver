#!/usr/bin/env python3
"""seed_compress Stage B: merge cover.py / statecount.py outputs into the per-config table (Opus, 10 Nov 2026).
usage: python3 -I mktable.py <out dir>"""
import sys, os, collections, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('cover', os.path.join(HERE, 'cover.py')); cv = importlib.util.module_from_spec(spec); spec.loader.exec_module(cv)
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
RF = '/mnt/project-files/swarm/round6/W6r-replay'
VER = RF + '/rsst_closure/inputs/rsst_verdicts.txt'; LC = RF + '/rsst_fp/from_studio_ST113/rsst582_lean_coverage.tsv'

def rd(fn, key=0, skip=2):
    out = {}
    for l in open(os.path.join(HERE, fn)):
        if l.startswith('#') or not l.strip(): continue
        f = l.rstrip('\n').split('\t')
        if f[0] in ('idx', 'config', 'none_config'): continue
        out[f[key]] = f
    return out
confs = cv.parse_conf(cv.CONF)
ver = {}
for l in open(VER):
    if l.startswith('rsst'):
        f = l.split(); ver[int(f[0][4:7])] = (f[0], dict(x.split('=', 1) for x in f[1:] if '=' in x))
lean = {}
for l in open(LC):
    if l.startswith('rsst'):
        f = l.rstrip('\n').split('\t'); lean[f[0]] = (f[5], f[6])
CU, CR = rd('cover_union_u.tsv'), rd('cover_union_r.tsv')
SU, SR = rd('sc_u_sets.tsv'), rd('sc_r_sets.tsv')
NU, NR = rd('sc_u_needsnone.tsv'), rd('sc_r_needsnone.tsv')
alive = {}
for l in open(os.path.join(HERE, 'cover_union_u.tsv.leaves')):
    idx, nm, z, kind, lab = l.rstrip('\n').split('\t')
    if kind == 'adm' and idx not in alive: alive[idx] = 'z=%s %s' % (z, lab)

def zlabel(c, z):
    L = c['adj'][z]; d = len(L); w = []; s = []
    for i in range(d):
        a = L[i]; w.append(str(cv.letter(c, a)) if cv.letter(c, a) else '.')
        sv = cv.apex(c, z, a, L[(i + 1) % d]); s.append(str(cv.letter(c, sv)) if cv.letter(c, sv) else '.')
    return '%d %s %s' % (d, ''.join(w), ''.join(s))
def nine_plus(c, z):   # a link / apex vertex of degree >= 10 read as letter 9
    L = c['adj'][z]; d = len(L); big = []
    for i in range(d):
        for v, nm in ((L[i], 'w%d' % i), (cv.apex(c, z, L[i], L[(i + 1) % d]), 's%d' % i)):
            if v is not None and v > c['r'] and len(c['adj'][v]) >= 10: big.append('%s=%d' % (nm, len(c['adj'][v])))
    return ','.join(big)

H = ['idx', 'rsst_id', 'name', 'verdict', 'ring', 'interior', 'lean_queue', 'covered_u', 'covered_r', 'witness_vertex', 'witness_kind',
     'witness', 'witness_zlabel', 'deg10plus_read_as_9', 'n_killed_vertices_u',
     'sets_groups', 'sets_groups_not_rejected_u', 'sets_groups_not_rejected_r',
     'fw_needsnone_states', 'fw_needsnone_not_rejected_u', 'fw_needsnone_not_rejected_r', 'fw_sole_states', 'fw_sole_not_rejected_u', 'fw_sole_not_rejected_r',
     'example_alive_label_u']
rows = []; tab = collections.Counter(); wit = collections.defaultdict(list)
for idx, c in enumerate(confs):
    rid, vv = ver[idx]; v = vv['verdict']; cu = CU[str(idx)]; cr = CR[str(idx)]
    assert cu[1] == c['name'] == cr[1] and rid.split('_', 1)[1].replace('o', '.', 1) == c['name']
    if v == 'none': q = 'none (not in the 582)'
    else: q = {'covered': 'in Lean (179)', 'todo': 'to prove (403)'}[lean[rid][0]]
    z = cu[4].split()[0] if cu[2] == 'yes' else '-'
    zl = zlabel(c, int(z)) if z != '-' and len(c['adj'][int(z)]) >= 7 else ('-' if z == '-' else 'wheel ' + ''.join(str(cv.letter(c, a) or '.') for a in c['adj'][int(z)]))
    nb = nine_plus(c, int(z)) if z != '-' else ''
    su = SU.get(c['name']); sr = SR.get(c['name']); nu = NU.get(c['name']); nr = NR.get(c['name'])
    r = [idx, rid, c['name'], v, c['r'], c['n'] - c['r'], q, cu[2], cr[2], cu[4], cu[5], cu[6], zl, nb or '-', cu[3],
         su[1] if su else 0, su[3] if su else 0, sr[3] if sr else 0,
         nu[1] if nu else '-', nu[2] if nu else '-', nr[2] if nr else '-', nu[3] if nu else '-', nu[4] if nu else '-', nr[4] if nr else '-',
         alive.get(str(idx), '-') if cu[2] == 'no' else '-']
    rows.append(r); tab[(q, cu[2], cr[2])] += 1
    if cu[2] == 'yes': wit[cu[6]].append(c['name'])
with open(os.path.join(OUT, 'cover_table.tsv'), 'w') as g:
    g.write('# Stage B cover test, all 633 RSST configs (unavoidable.conf 26aeba66); u = K3l5u + K3gB5u patterns + engine wheel kills, r = K3l5r + K3gB5r likewise. See README.md.\n')
    g.write('\t'.join(H) + '\n')
    for r in rows: g.write('\t'.join(map(str, r)) + '\n')
for fn, sel in (('drop_candidates_403.tsv', lambda r: r[6].startswith('to prove') and r[7] == 'yes'),
                ('uncovered_403.tsv', lambda r: r[6].startswith('to prove') and r[7] == 'no')):
    with open(os.path.join(OUT, fn), 'w') as g:
        g.write('\t'.join(H) + '\n')
        for r in rows:
            if sel(r): g.write('\t'.join(map(str, r)) + '\n')
with open(os.path.join(OUT, 'witness_patterns.tsv'), 'w') as g:
    g.write('# distinct witness kills used by covered configs (first killed vertex of each config): for the Studio Lean-membership check\nwitness\tconfigs\tnames\n')
    for w_, ns in sorted(wit.items(), key=lambda x: -len(x[1])): g.write('%s\t%d\t%s\n' % (w_, len(ns), ','.join(ns)))
with open(os.path.join(OUT, 'summary.tsv'), 'w') as g:
    g.write('lean_queue\tcovered_u\tcovered_r\tconfigs\n')
    for k, n in sorted(tab.items()): g.write('\t'.join(k) + '\t%d\n' % n)
for k, n in sorted(tab.items()): print(k, n)
print('distinct witnesses', len(wit))
