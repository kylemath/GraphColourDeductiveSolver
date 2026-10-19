"""Round 47 (from minkill45.py): round 43's minkill.py for any row.  From KILL (two-engine kills): inclusion-minimal windows, dihedral-canonical
f-names, twoeng-ready kills.txt / kills_kc.out / kills_cf.cfast / kills_df.out, and kills_min.txt.  A window name's F/N
(w_i outside the window, s_(i-1) and s_i inside) becomes w_i's own letter in the row, so the f-name keeps the s-s
adjacency the window has.  usage: python3 minkill47.py WINFILE LK PREFIX   (kills restricted to WINFILE's windows; files PREFIX_kills*.txt/.out)"""
import os, sys, collections
H = os.path.dirname(os.path.abspath(__file__)); WF, LK, PF = sys.argv[1], sys.argv[2], sys.argv[3]
def canon_key(d, lk, sv):     # gen.canon_key (s_i between w_i and w_i+1), as k43/fname.py
    best = None
    for refl in (0, 1):
        if refl: l2 = lk[::-1]; s2 = ''.join(sv[(-i - 2) % d] for i in range(d))
        else: l2, s2 = lk, sv
        for k in range(d):
            c = (l2[k:] + l2[:k], s2[k:] + s2[:k])
            if best is None or c < best: best = c
    return best
def fname(a):
    h, l, s = a.split('_'); d = int(h[1:]); l = ''.join(LK[j] if c in 'FN' else c for j, c in enumerate(l[1:]))
    k = canon_key(d, l, s); return 'f%d_%s_%s' % (d, k[0], k[1])
inw = {l.split()[0] for l in open(os.path.join(H, WF))}
kills = {}
for l in open(os.path.join(H, 'KILL')):
    nm, why = l.split(' ', 1)
    if nm in inw: kills.setdefault(nm, why.strip())
def vs(nm):
    _, l, s = nm.split('_')
    return frozenset([('u',)] * (l[0] == 'u') + [('w', j) for j, c in enumerate(l[1:]) if c not in '.FN'] + [('s', j) for j, c in enumerate(s) if c != '.'])
V = {k: vs(k) for k in kills}
mins = [k for k in kills if not any(V[o] < V[k] for o in kills if o != k)]
inp = {l.split()[0]: l for l in open(os.path.join(H, WF))}
fn = {k: fname(k) for k in kills}
def blocks(f):
    out, cur = {}, None
    for l in open(os.path.join(H, f)):
        if l.strip() and not l.startswith(' ') and not l.startswith('#'): cur = l.split()[0]
        if cur in kills and not l.startswith('#'): out.setdefault(cur, []).append(l)
    return out
kb, cb, db = blocks('A_kcc.out'), blocks('A_cf.out'), blocks('A_df.out')
ren = lambda k, ls: ''.join(x.replace(k + ' ', fn[k] + ' ', 1) for x in ls)
seen = set(); order = sorted(kills, key=lambda k: (int(inp[k].split()[1]), fn[k]))
with open(os.path.join(H, PF + '_' + 'kills.txt'), 'w') as a, open(os.path.join(H, PF + '_' + 'kills_kc.out'), 'w') as b, \
     open(os.path.join(H, PF + '_' + 'kills_cf.cfast'), 'w') as c, open(os.path.join(H, PF + '_' + 'kills_df.out'), 'w') as d:
    for k in order:
        if fn[k] in seen: continue
        seen.add(fn[k]); a.write(inp[k].replace(k + ' ', fn[k] + ' ', 1)); b.write(ren(k, kb.get(k, [])))
        if kills[k].startswith('C'): c.write(ren(k, cb.get(k, [])))
        else: d.write(ren(k, db.get(k, [])))
ms = sorted({fn[k]: k for k in mins}.items(), key=lambda t: (int(inp[t[1]].split()[1]), t[0]))
with open(os.path.join(H, PF + '_' + 'kills_min.txt'), 'w') as o:
    o.write('# round 47: inclusion-minimal two-engine kills (f-name, window name, ring, m, verdict)\n')
    for f, k in ms: o.write('%s %s %s %s %s\n' % (f, k, inp[k].split()[1], inp[k].split()[2], kills[k]))
print('kills', len(kills), 'distinct f-names', len(seen), 'minimal', len(mins), 'minimal f-names', len(ms))
print(collections.Counter((inp[k].split()[1], kills[k][0]) for k in mins))
