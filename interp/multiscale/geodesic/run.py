# Usage: python run.py out.jsonl maps modes seeds.  modes: plain,refl,deep,refldeep,refldeep3,harm,vor_any,vor_max
import sys, json, time, random, collections
sys.path.insert(0, '/mnt/project-files/multiscale/geodesic'); sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy/weak')
from geo import *
from e1_hier import make
from multiprocessing import Pool

def vor_tree(g, seed, pick):
    """run_vor.py merge order without colouring; returns list of (U, A, B)."""
    from e4_recursion import voronoi_cells
    from wk import Disc
    rng = random.Random(seed); cells = voronoi_cells(g, 3, rng); clusters = [set(c) for c in cells]; merges = []
    while sum(1 for c in clusters if c) > 2:
        alive = [i for i, c in enumerate(clusters) if c]; own = {v: i for i in alive for v in clusters[i]}
        nb = {i: set(own[w] for v in clusters[i] for w in g.adj[v] if own[w] != i) for i in alive}
        order = sorted(alive, key=lambda i: (len(clusters[i]), rng.random())); used = set(); merged = 0
        for i in order:
            if i in used or sum(1 for c in clusters if c) <= 2: continue
            opts = []
            for j in [j for j in nb[i] if j not in used]:
                if check(g, clusters[i] | clusters[j])[0] == 'nodisc': continue
                nch = len(Disc(g, clusters[i] | clusters[j]).chords) if pick == 'max' else 0
                opts.append(((-nch, len(clusters[j]), rng.random()), j))
            if not opts: continue
            opts.sort(); j = opts[0][1]
            merges.append((clusters[i] | clusters[j], clusters[i], clusters[j]))
            clusters[i] = clusters[i] | clusters[j]; clusters[j] = None; used |= {i, j}; merged += 1
        if not merged: break
    last = [c for c in clusters if c]
    merges.append((set(range(g.n)), last[0], last[1]))
    leaves = [len(c) for c in cells]
    return merges, leaves

def job(a):
    name, mode, seed, L = a; t = time.time(); g = G(make(name)); rec = dict(name=name, mode=mode, seed=seed, L=L, n=g.n)
    try:
        if mode.startswith('vor'):
            merges, leaves = vor_tree(g, seed, mode[4:])
            ss = [dict(seam_stats(g, U, A, B), root=(len(U) == g.n)) for U, A, B in merges]
            rec.update(leafmax=max(leaves), nleaves=len(leaves))
        else:
            if mode == 'harm':
                from wk import build_tree
                nodes = build_tree(g, L=L, seed=seed)
                spl = []
                for nd in nodes:
                    if len(nd['kids']) == 2:
                        A, B = nodes[nd['kids'][0]]['S'], nodes[nd['kids'][1]]['S']
                        sU, sa, sb = check(g, nd['S']) if len(nd['S']) < g.n else ('ok',), check(g, A), check(g, B)
                        spl.append(dict(parentCL=(sU[0] == 'ok'), stA=sa[0], stB=sb[0], chA=sa[2], chB=sb[2], chinfo=[]))
            else:
                nodes = build_geo(g, L, seed, mode)
                rec['root'] = nodes[0]['info']
                spl = []
                for nd in nodes[1:]:
                    i = nd['info']
                    if not i or i.get('fail'): continue
                    spl.append(dict(parentCL=nd['chordless'], stA=i['stA'], stB=i['stB'], chA=i['chA'], chB=i['chB'], chinfo=i['chinfo'],
                                    used_refl=i['used_refl'], nrefl=i['nrefl'], deep_fb=i.get('deep_fallback', False), anyCL=i['any_chordless'],
                                    nodisc=i.get('leaf_nodisc', False), n=len(nd['S'])))
                rec['fails'] = sum(1 for nd in nodes if nd['info'] and nd['info'].get('fail'))
            ss = tree_seams(g, nodes)
            lv = [len(nd['S']) for nd in nodes if not nd['kids']]
            rec.update(leafmax=max(lv), nleaves=len(lv), nleaves_gtL=sum(x > L for x in lv))
            cl = [s for s in spl if s['parentCL']]
            def ch(s): return [s[k] or 0 for k in ('chA', 'chB')]
            rec.update(splits=len(spl), splits_from_CL=len(cl),
                       fully_CL_from_CL=sum(s['stA'] == 'ok' and s['stB'] == 'ok' for s in cl),
                       fully_CL_all=sum(s['stA'] == 'ok' and s['stB'] == 'ok' for s in spl),
                       nodisc=sum('nodisc' in (s['stA'], s['stB']) for s in spl),
                       chords_child_fromCL=dict(sorted(collections.Counter(c for s in cl for c in ch(s)).items())),
                       chords_child_all=dict(sorted(collections.Counter(c for s in spl for c in ch(s)).items())),
                       chord_type_fromCL=dict(collections.Counter(c['type'] for s in cl for c in s['chinfo'])),
                       chord_d_fromCL=dict(sorted(collections.Counter(min(c['d'], 9) for s in cl for c in s['chinfo']).items())),
                       chord_d_all=dict(sorted(collections.Counter(min(c['d'], 9) for s in spl for c in s['chinfo']).items())),
                       chord_type_all=dict(collections.Counter(c['type'] for s in spl for c in s['chinfo'])))
            if mode != 'harm':
                rec.update(refl_used=sum(s['used_refl'] for s in spl), deep_fb=sum(s['deep_fb'] for s in spl),
                           anyCL_avail=sum(s['anyCL'] for s in spl), nrefl0=sum(s['nrefl'] == 0 for s in spl))
        nr = [s for s in ss if not s['root']]
        rec.update(merges=len(ss), S0=max(s['j'] for s in ss), S0_nonroot=max([s['j'] for s in nr], default=0),
                   j_hist=dict(sorted(collections.Counter(s['j'] for s in ss).items())),
                   s_max=max(s['s'] for s in ss), root_j=[s['j'] for s in ss if s['root']],
                   j_by_size={k: max([s['j'] for s in ss if lo <= s['nU'] < hi], default=None) for k, (lo, hi) in
                              {'<100': (0, 100), '100-1k': (100, 1000), '>=1k': (1000, 10**9)}.items()},
                   kid_chords_max=max(s['chA']+s['chB'] for s in ss))
    except Exception as e:
        import traceback; rec['err'] = traceback.format_exc()[-600:]
    rec['sec'] = round(time.time()-t); return rec

if __name__ == '__main__':
    out, maps, modes, seeds = sys.argv[1], sys.argv[2].split(','), sys.argv[3].split(','), int(sys.argv[4])
    L = int(sys.argv[5]) if len(sys.argv) > 5 else 40
    jobs = [(m, mo, s, L) for m in maps for mo in modes for s in range(seeds)]
    jobs.sort(key=lambda j: 0 if j[0] in ('ico10', 'flip10_1') else 1)
    f = open(out, 'a')
    with Pool(4) as p:
        for r in p.imap_unordered(job, jobs):
            f.write(json.dumps(r)+'\n'); f.flush()
            print({k: r.get(k) for k in ('name', 'mode', 'seed', 'splits', 'splits_from_CL', 'fully_CL_from_CL', 'chords_child_fromCL', 'S0', 'S0_nonroot', 'leafmax', 'err', 'sec')}, flush=True)
