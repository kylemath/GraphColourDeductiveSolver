"""HOFFC7: the d = 7 line table. Usage: make_table.py OFFC KCMAP FANS OUT
OFFC = offc_K3g_2f4f0f02.txt; KCMAP = kcmap.py's output; FANS = fans.py's output."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import offc_model as M
offc, kcmap, fans, out = sys.argv[1:5]
kc = {}
for l in list(open(kcmap))[1:]:
    f = l.rstrip('\n').split('\t'); kc[f[0]] = f
fn = {}
for l in list(open(fans))[1:]:
    f = l.rstrip('\n').split('\t'); fn[f[0]] = f
C_HC = {'f7_...5576_...665.': 'hC: CK108.k108Entries[14] (X I0-I1), K108All, main 0d86ecb0',
        'f7_..56756_....66.': 'hC: CK108.k108Entries[19] (X I3-I4), K108All, main 0d86ecb0'}
rows = []
for no, l in enumerate(open(offc), 1):
    if l.startswith('#') or not l.strip(): continue
    head, _, tail = l.rstrip('\n').partition(' # ')
    d, link, sword = head.split()
    if d != '7': continue
    src, name = tail.split()[:2]
    kv = dict(t.split('=', 1) for t in tail.split()[2:])
    phi = {M.slot_parse(x): M.slot_parse(y) for x, y in (p.split('>') for p in kv['phi'].split(','))}
    orot, deg, adj = M.own_rot(name, set(phi))
    pat = M.pat_of(link, sword)
    eo = [e for e in (1, -1) if not M.offc_ok(7, orot, phi, pat, e)]
    assert len(eo) == 1, (name, eo)
    lean = C_HC.get(name, 'no hD/hC module on main (name in no .lean file)')
    k = kc.get(name); f = fn.get(name)
    rows.append([str(no), d, link, sword, src, name, kv['d0'], kv['file'], kv['md5'], kv['phi'],
                 '+' if eo == [1] else '-', lean,
                 k[1] if k else 'none in tree', k[5] if k else '', k[6] if k else '', k[7] if k else '',
                 k[8] if k else '', f[2] if f else '', k[10] if k else ''])
hdr = ['line', 'd', 'LINK', 'SWORD', 'SRC', 'NAME', 'd0', 'file', 'md5', 'phi', 'eps_own', 'lean',
       'kc_src', 'r', 'm', 'phi_kc', 'eps_kc', 'RingLinked', 'kc_check']
with open(out, 'w') as o:
    o.write('\t'.join(hdr) + '\n')
    for r in rows: o.write('\t'.join(r) + '\n')
print(len(rows), 'rows;', sum(1 for r in rows if r[12] != 'none in tree'), 'with kc lines;',
      sum(1 for r in rows if r[18] == 'ok'), 'kc-order OffcOK ok;', sum(1 for r in rows if r[17] == 'True'), 'RingLinked')
