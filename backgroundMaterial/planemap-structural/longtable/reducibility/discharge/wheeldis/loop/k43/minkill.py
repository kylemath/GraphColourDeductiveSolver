"""Round 43: from KILL (two-engine kills), the inclusion-minimal windows (no other kill's vertex set inside them, same
orientation), their dihedral-canonical f-names, and twoeng-ready files for all kills (kills.txt, kills_kc.out,
kills_cf.cfast, kills_df.out) plus kills_min.txt (minimal ones, f-name order by ring).  usage: python3 minkill.py"""
import os, collections
H = os.path.dirname(os.path.abspath(__file__))
G = {'__file__': os.path.join(H, 'fname.py'), '__name__': 'x'}
src = open(G['__file__']).read(); exec(src[:src.index('args = ')], G)
kills = {}
for l in open(os.path.join(H, 'KILL')):
    nm, why = l.split(' ', 1); kills.setdefault(nm, why.strip())
def vs(nm):
    _, l, s = nm.split('_'); return frozenset([('u',)] * (l[0] == 'u') + [('w', j) for j, c in enumerate(l[1:]) if c != '.'] + [('s', j) for j, c in enumerate(s) if c != '.'])
V = {k: vs(k) for k in kills}
mins = [k for k in kills if not any(V[o] < V[k] for o in kills if o != k)]
inp = {l.split()[0]: l for l in open(os.path.join(H, 'win43_A.txt'))}
fn = {k: G['fname'](k) for k in kills}
def blocks(f):
    out, cur = {}, None
    for l in open(os.path.join(H, f)):
        if l.strip() and not l.startswith(' ') and not l.startswith('#'): cur = l.split()[0]
        if cur in kills and not l.startswith('#'): out.setdefault(cur, []).append(l)
    return out
kb, cb, db = blocks('A_kcc.out'), blocks('A_cf.out'), blocks('A_df.out')
ren = lambda k, ls: ''.join(x.replace(k + ' ', fn[k] + ' ', 1) for x in ls)
seen = set(); order = sorted(kills, key=lambda k: (int(inp[k].split()[1]), fn[k]))
with open(os.path.join(H, 'kills.txt'), 'w') as a, open(os.path.join(H, 'kills_kc.out'), 'w') as b, \
     open(os.path.join(H, 'kills_cf.cfast'), 'w') as c, open(os.path.join(H, 'kills_df.out'), 'w') as d:
    for k in order:
        if fn[k] in seen: continue
        seen.add(fn[k]); a.write(inp[k].replace(k + ' ', fn[k] + ' ', 1)); b.write(ren(k, kb.get(k, [])))
        if kills[k].startswith('C'): c.write(ren(k, cb.get(k, [])))
        else: d.write(ren(k, db.get(k, [])))
ms = sorted({fn[k]: k for k in mins}.items(), key=lambda t: (int(inp[t[1]].split()[1]), t[0]))
with open(os.path.join(H, 'kills_min.txt'), 'w') as o:
    o.write('# round 43: inclusion-minimal two-engine kills of d = 8 85556565/65866655 (f-name, a8 name, ring, m, verdict)\n')
    for f, k in ms: o.write('%s %s %s %s %s\n' % (f, k, inp[k].split()[1], inp[k].split()[2], kills[k]))
print('kills', len(kills), 'distinct f-names', len(seen), 'minimal', len(mins), 'minimal f-names', len(ms))
print(collections.Counter((inp[k].split()[1], kills[k][0]) for k in mins))
