# near-tight receiver rows from a vfile (d load excess link sv): canonical class, LP-row dedup, family split at the sol, motif, extended-family touch.
# usage: python3 tight.py <flags> sol=FILE vfile=FILE out=PREFIX
import sys, os, collections, json
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ana.py')).read())
ns['load_patterns']()
S = Sol(OPT['sol']); P = OPT['out']
def feats(d, w, s):
    f = []
    if any(w[i] == '5' and w[(i + 1) % d] == '5' and s[i] == '5' for i in range(d)): f.append('555-face')
    elif any(w[i] == '5' and w[(i + 1) % d] == '5' for i in range(d)): f.append('55-pair')
    n5 = w.count('5')
    if n5 == 0: f.append('relay(no 5)')
    elif set(w) <= {'5', '7'} and n5 >= 3 and not f: f.append('5-7 mesh')
    elif n5 == 1: f.append('lone-5')
    return ','.join(f) or 'mixed 5-6-7'
EXT = ('rr', 'z', 'zr', 'q7')
def touch(cf):
    out = {}
    for k, c in cf.items():
        fam = GRP.get(k[0], k[0])
        if fam not in EXT or not c: continue
        if k[0] == 'Q' and not ns['q7keys'](k[1]): continue
        a = out.setdefault(fam, [0, 0]); a[0] += 1; a[1] += int(abs(S.val(k)) > 1e-12)
    return out
rows = {}
for line in open(OPT['vfile']):
    p = line.split()
    if len(p) < 5: continue
    d, load, exc, lk, sv = int(p[0]), float(p[1]), float(p[2]), p[3], p[4]
    key = (d,) + ns['_canon_row'](d, lk, sv)
    if key not in rows: rows[key] = (load, -exc, lk, sv)
print('distinct classes', len(rows), 'by d', dict(sorted(collections.Counter(k[0] for k in rows).items())))
lp = {}; bad = []; R = []
for key, (load, sl, lk, sv) in rows.items():
    d = key[0]
    tot, sl2, g, fams, cf = S.row(d, lk, sv)
    if abs(sl2 - sl) > 1e-7: bad.append((d, lk, sv, sl, sl2))
    ck = (d, tuple(sorted(((k, c) for k, c in cf.items() if c), key=str)))
    if ck in lp: lp[ck]['n'] += 1; lp[ck]['alts'].append(lk + '/' + sv); continue
    r = {'sl': sl, 'd': d, 'lk': lk, 'sv': sv, 'g': g, 'tch': touch(cf), 'mot': feats(d, lk, sv), 'n': 1, 'alts': [], 'adm': ns['admissible'](d, lk, sv)}
    lp[ck] = r; R.append(r)
print('python vs jsepf slack mismatches > 1e-7: %d %s' % (len(bad), bad[:5]))
print('distinct LP rows', len(R), 'not admissible as written:', sum(1 for r in R if r['adm']))
R.sort(key=lambda r: r['sl'])
with open(P + '_rows.txt', 'w') as f:
    f.write('# near-tight receiver rows at %s (t = %.12f); slack = d - 6 + t - load [M]; one line per distinct LP row (n = classes with identical coefficients)\n' % (OPT['sol'], S.t))
    f.write('# R d link sv tag | slack n motif | load split by family | extended-family keys in the row: fam=keys/positive-at-sol\n')
    for r in R:
        f.write('R %d %s %s sl%.5f | %.9f n=%d %s | %s | %s\n' % (r['d'], r['lk'], r['sv'], r['sl'], r['sl'], r['n'], r['mot'],
            ' '.join('%s=%+.5f' % kv for kv in sorted(r['g'].items())), ' '.join('%s=%d/%d' % (k, v[0], v[1]) for k, v in sorted(r['tch'].items())) or 'none'))
for th in (1e-6, 0.001, 0.003, 0.005, 0.01):
    sub = [r for r in R if r['sl'] < th]
    c = collections.Counter(r['d'] for r in sub); m = collections.Counter(r['mot'] for r in sub if r['d'] == 7)
    print('slack < %-6g: %5d LP rows, by d %s; d=7 motifs %s' % (th, len(sub), dict(sorted(c.items())), dict(m.most_common())))
    sub7 = [r for r in sub if r['d'] == 7]
    for fam in EXT:
        print('    d=7 rows with %s keys: %d, with a positive %s column: %d' % (fam, sum(1 for r in sub7 if fam in r['tch']), fam, sum(1 for r in sub7 if fam in r['tch'] and r['tch'][fam][1])))
    print('    d=7 rows with no rr/z/zr/q7 key at all: %d' % sum(1 for r in sub7 if not r['tch']))
json.dump([[r['sl'], r['d'], r['lk'], r['sv'], r['n'], r['mot'], r['g'], r['tch']] for r in R], open(P + '_rows.json', 'w'))
