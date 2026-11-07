"""K3CHK7 (ST-26): per-config reducibility of the 174 K-3/K-4 hits. Parse check: the kc line's name = config name and its r, m = listed
ring, m. D: kc -C -s 60 -t 600 + dfast18; C: kc -t 600 -C -x X + cfast --fixed X. Reuse: identical (name, kc line[, X]) already run
on the same engines in out/job_K3/results (K-3 pack: kc -C D + dfast18 D) or out/job_K3CHK..K3CHK6 (D: kc+dfast18; C: kc -x + cfast)."""
import os, re, json, subprocess, glob
from concurrent.futures import ThreadPoolExecutor
K = 'out/job_K3CHK7/'
rows = []
for l in open(K + 'in/all_K3_K4_hits_kc.tsv'):
    if l.startswith('#') or not l.strip(): continue
    f = l.rstrip('\n').split('\t'); rows.append(dict(name=f[0], v=f[1], X=f[2], ring=f[3], m=f[4], src=f[6], kc=' '.join(f[7].split()[:5])))
reuse = {}
for fn in glob.glob('out/job_K3/results/res_K3_*.tsv'):
    for l in open(fn):
        g = l.rstrip('\n').split('\t')
        if len(g) >= 12 and g[4] == 'D' and 'dfast18:D' in g[10]: reuse[(g[3], ' '.join(g[11].split()[:5]), 'D')] = 'K-3 pack ' + os.path.basename(fn) + ' (kc -C D + dfast18 D)'
for j, kcf, kind, x in (('K3CHK', 'configs.kc', 'D', None), ('K3CHK2', 'D3.kc', 'D', None), ('K3CHK2', 'C1.kc', 'C', 'I5-I6'), ('K3CHK3', 'D1.kc', 'D', None), ('K3CHK3', 'C1.kc', 'C', 'I0-I5'),
                        ('K3CHK4', 'D1.kc', 'D', None), ('K3CHK4', 'C1.kc', 'C', 'I2-I3'), ('K3CHK5', 'D1.kc', 'D', None), ('K3CHK5', 'C1.kc', 'C', 'I0-I3')):
    for l in open('out/job_%s/%s' % (j, kcf)):
        if l.strip(): reuse[(l.split()[0], ' '.join(l.split()[:5]), kind if x is None else 'C:' + x)] = 'out/job_%s (%s)' % (j, 'kc -C + dfast18' if kind == 'D' else 'kc -x + cfast --fixed')
sh = lambda c: subprocess.run(['nice', '-n', '10'] + c, capture_output=True, text=True).stdout
def one(r):
    kc = r['kc'].split(); parse = kc[0] == r['name'] and kc[1] == r['ring'] and kc[2] == r['m']
    key = (r['name'], r['kc'], 'D' if r['v'] == 'D' else 'C:' + r['X'])
    if key in reuse: return r, parse, 'reused: ' + reuse[key], True
    f = K + 'eng/' + re.sub(r'[^A-Za-z0-9_.-]', '_', r['name']); open(f + '.in', 'w').write(r['kc'] + '\n')
    if r['v'] == 'D':
        a = sh(['loop/kc/kc', '-C', '-s', '60', '-t', '600', f + '.in']); b = sh(['out/job52/dfast18', f + '.in'])
        open(f + '.out', 'w').write('== kc -C\n' + a + '== dfast18\n' + b); ok = 'D=true' in a and 'D=true' in b
        return r, parse, 'kc:%s dfast18:%s' % ('D' if 'D=true' in a else 'noD', 'D' if 'D=true' in b else 'noD'), ok
    open(f + '.x', 'w').write('%s {%s}\n' % (r['name'], r['X']))
    a = sh(['loop/kc/kc', '-t', '600', '-C', '-x', f + '.x', f + '.in']); b = sh(['../studio15/cfast', f + '.in', '--fixed', r['X']])
    open(f + '.out', 'w').write('== kc -C -x X\n' + a + '== cfast --fixed X\n' + b)
    adm = 'adm=yes' in a and 'leftover 0' in a; cf = 'leftover bad classes extending after contraction = 0' in b
    return r, parse, 'kc-x:%s cfast:%s' % ('adm=yes,leftover0' if adm else 'FAIL', 'C' if cf else 'noC'), adm and cf
with ThreadPoolExecutor(4) as ex: R = list(ex.map(one, rows))
with open(K + 'eng/results.tsv', 'w') as f:
    f.write('# name\tverdict\tX\tring\tm\tkc line parses to name/ring/m\tengines\tPASS\n')
    for r, p, e, ok in R: f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (r['name'], r['v'], r['X'], r['ring'], r['m'], 'yes' if p else 'NO', e, 'PASS' if (ok and p) else 'FAIL'))
print('done', sum(1 for _, p, _, ok in R if ok and p), '/', len(R), 'PASS; reused', sum(1 for _, _, e, _ in R if e.startswith('reused')))
