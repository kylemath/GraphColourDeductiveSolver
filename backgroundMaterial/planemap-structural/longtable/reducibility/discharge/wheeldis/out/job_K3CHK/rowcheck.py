"""K3CHK (Studio): does configuration K occur in receiver row (d, link, apex)?  Frame = grow.build2 of the row itself (u degree d,
link letters, apex letters; privates and ring 3 unknown, never exact; letter 9 = 9+, never exact), so the frame structure is
consistent with every w letter by construction (ZCONS).  Occurs = some grow.embeddings embedding (exact degrees, induced,
interior triangles onto faces) into {u, w_*, s_*} that is rotation-preserving (rot/rotcheck.py).  Face-set occurrence reported too."""
import sys, os, collections
H = os.getcwd()
G = {'__file__': os.path.join(H, 'loop', 'k42', 'grow.py'), '__name__': 'grow'}; exec(open(G['__file__']).read(), G)
sys.path.insert(0, os.path.join(H, 'loop', 'studio', 'opus_check', 'f2b041', 'keep95p131f', 'rot')); import rotcheck as RC
K = 'out/job_K3CHK/'
CF = {l.split()[0]: l.strip() for l in open(K + 'configs.kc') if l.strip()}
def occurs(line, d, L, S):
    cfg = G['kcline'](line, 'k3'); rk = RC.kc_rotation(line)
    lk = [int(c) for c in L]; r2 = {('s', i): int(c) for i, c in enumerate(S)}
    frm = RC.frame_rotation(G, d, lk, {}, r2); adj, name, inv, rotF = frm
    G['D'] = d; G['LK'] = lk; a2, nm2, faces = G['build2'](r2)
    P = [('u',)] + [('w', i) for i in range(d) if lk[i] <= 8] + [('s', i) for i in range(d) if S[i] != '9']
    Ps = set(P); pa = {x: {nm2[y] for y in a2[v] if y in nm2} & Ps for v, x in nm2.items() if x in Ps}
    pf = {frozenset(nm2[y] for y in f) for f in faces if all(y in nm2 and nm2[y] in Ps for y in f)}
    fd = {('u',): d}; fd.update({('w', i): lk[i] for i in range(d) if lk[i] <= 8}); fd.update({('s', i): int(S[i]) for i in range(d) if S[i] != '9'})
    fs = rt = 0
    for e in G['embeddings'](cfg, P, pa, pf, fd):
        fs += 1
        if RC.rot_ok({u: inv[v] for u, v in e}, rk, frm): rt += 1
    return fs, rt
out = open(K + 'per_row.tsv', 'w'); out.write('# config\tclass\tcovered\trow (d link apex)\tlisted killer\tface-set embeddings\trotation-preserving\tPASS/FAIL\n')
cnt = collections.Counter()
for l in open(K + 'in/binding_coverage.tsv'):
    if l.startswith('#') or not l.strip(): continue
    f = l.rstrip('\n').split('\t'); row, d, cls, cov, best = f[0], int(f[1]), f[2], f[5], f[6]
    L, S = row.split('/')
    for nm, line in CF.items():
        if int(nm[1]) != d: continue
        fs, rt = occurs(line, d, L, S)
        listed = nm in f[6] or nm in f[11] if len(f) > 11 else nm == best
        if cov == 'yes' and best == nm: want = True
        elif cov != 'yes': want = False
        else: continue
        ok = (rt > 0) == want
        cnt[(nm, 'covered' if want else 'uncovered', 'PASS' if ok else 'FAIL')] += 1
        out.write('%s\t%s\t%s\t%d %s %s\t%s\t%d\t%d\t%s\n' % (nm, cls, cov, d, L, S, best, fs, rt, 'PASS' if ok else 'FAIL'))
out.close()
for k, v in sorted(cnt.items()): print(k, v)
