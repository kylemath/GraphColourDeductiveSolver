import json, sys, os, time
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace'); sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill')
from kt import *; from collar import *; from minbad import *; from t2_tubes import annulus
os.makedirs('minimal_bad', exist_ok=True)
found = {}
def record(name, adj, S, col, bd, w, k0, coord, L):
    t0 = time.time(); S0 = len(S)
    Sm = shrink(adj, S, col, bd, w, k0)
    cf = canon(Sm, col, bd, coord, L); h = hashlib.md5(str(cf).encode()).hexdigest()[:10]
    d = depth_in(adj, Sm, bd)
    rec = dict(name=name, L=L, w=w, k0=k0, size_before=S0, size=len(Sm), rows_used=sorted(set(coord[v][0] for v in Sm)),
               cells=sorted((coord[v][0], coord[v][1], col[v]) for v in Sm), canon_hash=h, sec=round(time.time()-t0))
    json.dump(rec, open(f'minimal_bad/{name}.json', 'w'), indent=1)
    found.setdefault(h, []).append(name)
    print(name, 'size', S0, '->', len(Sm), 'rows', rec['rows_used'], 'hash', h, f'{rec["sec"]}s', flush=True)
    # picture
    rows = sorted(set(coord[v][0] for v in Sm)); pic = []
    for r in rows:
        line = ['.'] * L
        for v in Sm:
            if coord[v][0] == r: line[coord[v][1]] = str(col[v])
        pic.append(f'{r:2d} ' + ''.join(line))
    print('\n'.join(pic), flush=True)
    return rec
ce = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/counterexamples.json'))
tk = {(r['L'], r['side']): r for r in json.load(open('t3_tubes.json'))} if os.path.exists('t3_tubes.json') else {}
for c in sorted(ce, key=lambda c: c['L']):
    L, w0 = c['L'], c['w']
    for side in 'AB':
        rows = c['A_rows_depth_w_to_seam'] if side == 'A' else [r[::-1] for r in reversed(c['B_rows_seam_to_depth_w'])]
        rows = extend_below(rows[0], EXT) + rows
        adj, col = annulus(rows); n = len(col); seam = len(rows)-1; bd = [seam*L + i for i in range(L)]; S = set(range(n))
        coord = {v: (seam - v // L, v % L) for v in range(n)}
        w = w0
        k, _, _ = min_window(adj, S, col, bd, w); k0 = k - 1
        record(f'tube_L{L}_{side}_w{w}_k{k0}', adj, S, col, bd, w, k0, coord, L)
d = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/sphere_L18_w4.json'))
adj = [set(a) for a in d['adj']]; L = 18; n = len(adj); A = set(d['A']); B = set(range(n)) - A; m = d['seam_row_A']
colA = {int(k): v for k, v in d['colA'].items()}; colB = {int(k): v for k, v in d['colB'].items()}
bdA = [m*L + i for i in range(L)]; bdB = [(m+1)*L + i for i in range(L)]
ntube = 26*L
coordA = {v: ((m - v // L, v % L) if v < ntube else (99, v)) for v in range(n)}
coordB = {v: ((v // L - (m+1), v % L) if v < ntube else (99, v)) for v in range(n)}
record('opus_A_w4_k10', adj, A, colA, bdA, 4, 10, coordA, L)
record('opus_B_w4_k8', adj, B, colB, bdB, 4, 8, coordB, L)
print('DISTINCT', len(found), {h: v for h, v in found.items()})
json.dump(found, open('minimal_bad/index.json', 'w'), indent=1)
