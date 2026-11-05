"""s80 Team E: dump receiver-row coefficients (recv_coef_R2, the exact Python row of the engine) for a row list, with any engine.
usage: python3 rowdump.py ENGDIR ROWS OUT.jsonl [sol=SOL.json] -- <pcheck options (FAM flags, tables, f2b=, f2bx=...)>
  ROWS: lines 'R d link sword' (K row-file format) or 'link/sword'.
  OUT lines: {"row": [d, lk, sv], "cf": [[repr(key), coef], ...] sorted, "val": value at SOL (if given)}
  With f2bx in the options (s80 engine only) each line also carries "cf0" / "val0" = the same row with the extra rules removed."""
import sys, os, json, collections
ENG, ROWS, OUT = sys.argv[1:4]; rest = sys.argv[4:]
SOL = None
if rest and rest[0].startswith('sol='): SOL = rest[0][4:]; rest = rest[1:]
if rest and rest[0] == '--': rest = rest[1:]
sys.argv = [os.path.join(ENG, 'pcheck.py'), 'none'] + rest
G = {'__file__': os.path.join(ENG, 'pcheck.py'), '__name__': '__main__'}
exec(compile(open(G['__file__']).read(), G['__file__'], 'exec'), G)
rows = []
for l in open(ROWS):
    f = l.split()
    if not f or l.startswith('#'): continue
    if f[0] == 'R': rows.append((int(f[1]), f[2], f[3]))
    else: lk, sv = f[0].split('/'); rows.append((len(lk), lk, sv))
xon = 'xon' in G['FLAGS']
val = None
if SOL:
    Sj = json.load(open(SOL)); y = {}
    for k, v in Sj['y'].items():
        u, r_ = k.split('|'); y[G['root'](list((int(u),) + tuple(int(c) for c in r_)), 0)] = v
    HV2 = {tuple(k): v for k, v in Sj['h']}; D = {}
    for nm in ('z', 'zr', 'r', 'rr', 'q', 'lq', 'lQ'): D[nm] = {tuple(k): v for k, v in Sj.get(nm, [])}
    xd = {int(k): v for k, v in Sj.get('x', {}).items()}
    G['LQV'].clear(); G['LQV'].update(D['lq']); G['LQQ'].clear(); G['LQQ'].update(D['lQ']); G['QV'].clear(); G['QV'].update(D['q'])
    def MV(sg):
        ks = G['sig2_keys'](sg); return max(HV2.get(k, 0.0) for k in ks) if ks else 0.0
    def val(cf):
        t = 0.0
        for k, c in cf.items():
            if k[0] == 'y': v = y.get(k[1], 0.0)
            elif k[0] == 'x': v = xd.get(k[1], 0.0)
            elif k[0] == 'M': v = MV(k[1])
            elif k[0] in ('z', 'zr', 'r', 'rr', 'q', 'lq'): v = D[k[0]].get(k[1], 0.0)
            elif k[0] == 'Q': v = max([G['QV'].get(kk, 0.0) for kk in G['q7keys'](k[1])] or [0.0])
            elif k[0] == 'lQ': v = G['l3q_Qeff'](*k[1]) if len(k[1]) == 3 else G['l3q_QeffV'](*k[1])
            else: raise Exception('key %s' % (k,))
            t += c * v
        return t
fx = 'f2bx' in G['OPT']
if fx:
    f2bm = G['f2bm']; XR = {g: set(f2bm.XRULES.get(g, ())) for g in f2bm.GROUPS}
    def setrules(on):
        for g in f2bm.GROUPS:
            if not hasattr(setrules, 'full'): setrules.full = {g_: list(f2bm._R[g_]) for g_ in f2bm.GROUPS}
            f2bm._R[g] = list(setrules.full[g]) if on else [r for r in setrules.full[g] if r not in XR[g]]
            idx = {}
            for p, wr, sr in f2bm._R[g]:
                sd = dict(sr); idx.setdefault((sd.get(-1), sd.get(0)), []).append((wr, tuple((o, v) for o, v in sr), 1 << (p - 5)))
            f2bm._IDX[g] = idx
    setrules(False)
    CF0 = [G['recv_coef_R2'](d, lk, sv, xon) for d, lk, sv in rows]
    setrules(True)
with open(OUT, 'w') as o:
    for n, (d, lk, sv) in enumerate(rows):
        cf = G['recv_coef_R2'](d, lk, sv, xon)
        rec = {'row': [d, lk, sv], 'cf': sorted([repr(k), c] for k, c in cf.items() if c)}
        if val: rec['val'] = val(cf)
        if fx:
            rec['cf0'] = sorted([repr(k), c] for k, c in CF0[n].items() if c)
            if val: rec['val0'] = val(CF0[n])
        o.write(json.dumps(rec) + '\n')
print('rowdump: %d rows -> %s' % (len(rows), OUT), flush=True)
