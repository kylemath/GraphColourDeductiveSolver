"""EXPLORE round 44: per-configuration verdict table for RSST's 633 on our engines.
Registry-eligible (rsst_verdicts.txt): D2 = D on kc and dfast; C2cons = C on kc -C (conservative admissibility) and cfast
--fixed with the same X, leftover 0.  Anything else is listed with verdict 'none' there, and its diagnostics (RSST's
own X scored by kc, kc -C2 broad search, cfast with RSST's X, cfast --search) go to rsst_verdicts_C2.txt, which stays
out of the registry (Long Table, 20:00Z).  usage: python3 verdict44.py"""
import os, re, collections
H = os.path.dirname(os.path.abspath(__file__))
names = [l.split()[0] for l in open(os.path.join(H, 'rsst.txt')) if l.strip()]
ring = {l.split()[0]: int(l.split()[1]) for l in open(os.path.join(H, 'rsst.txt')) if l.strip()}
rx = dict(l.split() for l in open(os.path.join(H, 'rsst_x.txt')) if l.strip())
def blocks(fn):
    out = collections.defaultdict(list); cur = None
    if not os.path.exists(os.path.join(H, fn)): return out
    for l in open(os.path.join(H, fn)):
        l = l.rstrip('\n')
        if l.startswith('rsst'): cur = l.split()[0]
        if cur: out[cur].append(l)
    return out
kc = blocks('s0_kcc.out'); kc.update(blocks('s1_kcc.out'))
df = blocks('rsst_dfast.out'); cf = blocks('kc_cf.cfast')
xk = blocks('rsst_x_kc.out'); c2 = blocks('rsst_C2.out'); cx = blocks('rsst_C2_cf.cfast'); cs = blocks('rsst_C2_cfsearch.cfast')
rows = []; broad = []; cnt = collections.Counter(); mism = []
for n in names:
    k = kc[n]; kD = 'D=true' in k[0]
    m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', '\n'.join(k)); kX = m.group(1) if m else None
    dD = ('D=true' in df[n][0]) if n in df else None
    lab = 'D' if rx[n] == '-' else 'C'
    if dD is not None and dD != kD: mism.append(n)
    if lab == 'D' and not kD: mism.append(n)
    if kD and dD: v, x = 'D2', '-'
    elif kD: v, x = 'Dkc-only' if dD is False else 'Dkc(dfast pending)', '-'
    elif kX:
        ok = any('fixed X={%s}' % kX in l and l.endswith('leftover bad classes extending after contraction = 0') for l in cf.get(n, []))
        v, x = ('C2cons' if ok else ('C-kc-only' if n in cf else 'C(cfast pending)')), '{%s}' % kX
    else: v, x = 'none', '-'
    cnt[v] += 1
    rows.append('%s r=%d RSST=%s kcD=%s dfastD=%s verdict=%s X=%s' % (n, ring[n], lab, kD, dD, v, x))
    if v == 'none':
        ad = next((l.strip() for l in xk.get(n, []) if 'X=' in l), 'n/a (RSST label D)' if lab == 'D' else 'pending')
        b = next((l.strip() for l in c2.get(n, []) if 'C-REDUCIBLE' in l or 'C=false' in l), 'pending')
        f1 = next((l.strip() for l in cx.get(n, []) if 'fixed X=' in l), 'n/a' if lab == 'D' else 'pending')
        f2 = next((l.strip() for l in cs.get(n, []) if 'C-REDUCIBLE' in l or 'no output' in l or 'not' in l.lower()), 'pending')
        broad.append('%s r=%d RSST X=%s\n  kc -x RSST X (conservative): %s\n  kc -C2 broad: %s\n  cfast fixed RSST X: %s\n  cfast --search: %s'
                     % (n, ring[n], rx[n], ad, b, f1, f2))
hdr = ('# EXPLORE round 44: RSST unavoidable.conf (633) on kc and dfast/cfast.  verdict D2 = D on both engines; C2cons = C\n'
       '# with one conservative X accepted by kc -C and cfast --fixed (leftover 0); none = neither (see rsst_verdicts_C2.txt,\n'
       '# not registry).  Counts: %s.  kc/dfast or RSST-label mismatches: %d %s\n' % (dict(cnt), len(mism), ' '.join(mism[:10])))
open(os.path.join(H, 'rsst_verdicts.txt'), 'w').write(hdr + '\n'.join(rows) + '\n')
open(os.path.join(H, 'rsst_verdicts_C2.txt'), 'w').write(
    '# EXPLORE round 44: RSST configurations that are neither D2 nor C2cons on our engines.  Diagnostics only, NOT for the\n'
    '# registry (broad admissibility or RSST\'s own X).\n' + '\n'.join(broad) + '\n')
print(hdr)
