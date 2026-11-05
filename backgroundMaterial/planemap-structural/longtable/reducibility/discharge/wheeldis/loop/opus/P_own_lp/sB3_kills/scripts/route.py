# B3 route mapper: every two-engine D window (kcc D + dfast D + dfast18 D) in the given res files ->
#   LP route (F: u-centred receiver pattern / A: kill6 entry / L: l3q mask entry / X: cell kill needing a new key)
#   and the rows it touches among ROWS files (exact: the same slot set, placed by every rotation/reflection, rebuilds a
#   window with the same canonical code in that row, with the private / ring-3 vertex at the same letter).
# usage: python3 route.py OUT.tsv ROWSFILE[,ROWSFILE..] res1.tsv [res2.tsv ...]
import sys, re, collections
from gen3 import build, ringcycle, kcline, ring3_candidates
from kcanon import code
OUT, RF = sys.argv[1], sys.argv[2].split(','); RES = sys.argv[3:]
ROWS = []
for fn in RF:
    for l in open(fn):
        if not l.strip() or l.startswith('#'): continue
        f = l.split(); ROWS.append((f[1], f[2], f[3] if len(f) > 3 else '', fn.split('/')[-1]))
def parse_name(nm):
    m = re.match(r'b(\d+)_([u-])([0-9.]+)_([0-9.]+)((?:_[pt]\d+)*)$', nm)
    d = int(m.group(1)); uin = m.group(2) == 'u'; lk, sv = m.group(3), m.group(4); ex = []
    for e in m.group(5).split('_')[1:]:
        if e[0] == 'p': ex.append((('p', int(e[1]), int(e[2])), int(e[3])))
        else: ex.append((('t', int(e[1:-1])), int(e[-1])))
    assert len(lk) == d and len(sv) == d
    return d, uin, lk, sv, ex
def slots_of(d, uin, lk, sv):
    return ({('u',)} if uin else set()) | {('w', j) for j in range(d) if lk[j] != '.'} | {('s', j) for j in range(d) if sv[j] != '.'}
def placements(d):
    for r in range(d):
        yield (lambda j, r=r: (j + r) % d), (lambda j, r=r: (j + r) % d), False
        yield (lambda j, r=r: (r - j) % d), (lambda j, r=r: (r - j - 1) % d), True
def window_code(LK, SV, S, pdeg, tdeg):
    try: adj, rot, name, deg, Z3, inv = build(LK, SV, pdeg=pdeg, tdeg=tdeg)
    except (AssertionError, ValueError): return None
    if any(x not in inv for x in S): return None
    if any(deg.get(x, 9) >= 9 for x in S if x[0] in 'uws'): return None
    Is = set(inv[x] for x in S); order = ringcycle(adj, Is)
    if order is None: return None
    return code(kcline('x', adj, Is, order))
def nbnames(LK, SV, k):
    for kk, nb in ring3_candidates(LK, SV):
        if kk == k: return nb
def touches(nm, kl):
    d, uin, lk, sv, ex = parse_name(nm); S0 = slots_of(d, uin, lk, sv); target = code(kl); hits = []
    srcLK = srcSV = None
    for LK, SV, tag, src in ROWS:
        if len(LK) != d: continue
        found = False
        for pw, ps, refl in placements(d):
            S = set()
            for x in S0: S.add(x if x[0] == 'u' else (('w', pw(x[1])) if x[0] == 'w' else ('s', ps(x[1]))))
            if any(LK[x[1]] != lk[[j for j in range(d) if pw(j) == x[1]][0]] for x in S if x[0] == 'w'): continue
            if any(SV[x[1]] != sv[[j for j in range(d) if ps(j) == x[1]][0]] for x in S if x[0] == 's'): continue
            pdeg = {}; tdeg = {}; ok = True
            for (e, dg) in ex:
                if e[0] == 'p':
                    j = pw(e[1]); n = int(LK[j]) - 5 if LK[j] != '9' else None
                    if n is None: ok = False; break
                    k = e[2] if not refl else n + 1 - e[2]
                    if not 1 <= k <= n: ok = False; break
                    pdeg[('p', j, k)] = dg; S.add(('p', j, k))
                else:
                    ok = False   # ring-3 extras: mapped only onto the source row (identity placement below)
            if not ok: continue
            c = window_code(LK, SV, S, pdeg or None, None)
            if c == target: found = True; break
        if not found and any(e[0] == 't' for e, _ in ex):
            S = set(S0) | {e for e, _ in ex}; pdeg = {e: dg for e, dg in ex if e[0] == 'p'}; tdeg = {e[1]: dg for e, dg in ex if e[0] == 't'}
            if all(LK[x[1]] == lk[x[1]] for x in S0 if x[0] == 'w') and all(SV[x[1]] == sv[x[1]] for x in S0 if x[0] == 's'):
                c = window_code(LK, SV, S, pdeg or None, tdeg or None)
                if c == target: found = True
        if found: hits.append('%s/%s%s' % (LK, SV, ('[' + tag.split('_')[0] + ']') if tag else ''))
    return hits
def route(nm):
    d, uin, lk, sv, ex = parse_name(nm); S = slots_of(d, uin, lk, sv); U = min(d, 9)
    if not ex:
        return 'F', 'f%d_%s_%s  (q%d%s_%s_%s_%s)' % (d, lk, sv, d, 'u' if uin else '-', lk, sv, ':' * (d - 1))
    if len(ex) == 1 and ex[0][0][0] == 'p':
        (p, L), = ex; j = p[1]
        if lk[j] == '6':
            key = {('w', (j + o) % d) for o in (-2, -1, 0, 1, 2)} | {('s', (j + o) % d) for o in (-2, -1, 0, 1)} | ({('u',)} if U == 7 else set())
            if S <= key:
                ws = ''.join(lk[(j + o) % d] for o in (-2, -1, 1, 2)); ss = ''.join(sv[(j + o) % d] for o in (-2, -1, 0, 1))
                return 'A', 'KILL6 U=%s w(j-2,j-1,j+1,j+2)=%s s(j-2,j-1,j,j+1)=%s private=%d' % ('7' if uin else ('7,8,9' if U == 7 else '8,9'), ws, ss, L)
            return 'A\'', 'kill6-type private of the 6 at w%d, window leaves the key: %s' % (j, sorted(S - key))
        if lk[j] == '7' and d in (7, 8):
            n = 2
            for sg in (1, -1):
                if (sg == 1 and p[2] != 2) or (sg == -1 and p[2] != 1): continue
                ap = ('s', j) if sg == 1 else ('s', (j - 1) % d); o = ('s', (j - 1) % d) if sg == 1 else ('s', j)
                R = {('u',), ('w', j), ap, o} | {('w', (j + k * sg) % d) for k in (1, 2, 3, 4)}
                if S <= R:
                    gl = lambda x: (lk[x[1]] if x[0] == 'w' else sv[x[1]])
                    c, w2, w3, w4 = (gl(('w', (j + k * sg) % d)) for k in (1, 2, 3, 4))
                    return 'L', 'L3Q sigma=%+d c,w2,w3,w4=%s%s%s%s a,o=%s%s a2=%d (c,a must be <=6; . = any letter)' % (sg, c, w2, w3, w4, gl(ap), gl(o), L)
            return 'X7', 'private of the 7 at w%d: window not inside an l3q payee window (needs a wider key)' % j
    return 'X', 'cell kill (%s): needs a new key / cluster row' % ','.join('%s=%d' % (''.join(map(str, e)), dg) for e, dg in ex)
seen = {}
for fn in RES:
    for l in open(fn):
        g = l.rstrip('\n').split('\t')
        if len(g) < 12: continue
        isD = g[4] == 'D' and 'noD' not in g[10]; isC = g[4] == 'C' and 'C-REDUCIBLE' in g[10].upper()
        if not (isD or isC): continue
        if g[0] in seen: continue
        seen[g[0]] = (int(g[1]), int(g[2]), g[3], g[9], ('kcc:D ' + g[10]) if isD else ('kcc:C X={%s} ' % g[6] + g[10][:60]), g[11])
with open(OUT, 'w') as f:
    f.write('# code\tring\tm\tname\tfamily\tengines\troute\tentry\trows_touched\tkcline\n')
    for c, (r, m, nm, fam, conf, kl) in sorted(seen.items(), key=lambda kv: kv[1][:2]):
        rt, ent = route(nm); h = touches(nm, kl)
        f.write('\t'.join([c, str(r), str(m), nm, fam, conf, rt, ent, ' '.join(h), kl]) + '\n')
        print(r, m, nm, fam, conf[:40], rt, ent, '| rows', len(h), ' '.join(h[:6]), flush=True)
print('D/C windows', len(seen))
