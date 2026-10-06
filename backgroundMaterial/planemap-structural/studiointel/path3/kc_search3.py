#!/usr/bin/env python3
"""studiointel path3/kc_search.py -- [exploratory] Path 3: tabu search for a STUCK Kempe class of T - v (a class with no filled state).
Core class kept: min degree >= 5, max degree <= MAXDEG, no separating triangle. Each graph: at every degree-5 hole, the Kempe classes of
T - v (fast/kempe_classes: per class size, #filled, #DL). OBJECTIVE v3 (coordinator, after v2 drifted to tiny classes): lowest filled FRACTION among classes of size >= LMIN = 40.
Score = (1 if a class of size >= 40 exists [2 if any class has no filled state], -min filled/size over such classes, far of that class, max kappa).
Old v2 text: Score (lexicographic, larger is better):
  ( - min #filled over holes and classes,  far = max distance (pure swaps) from a state of that minimal class to its filled states,
    max kappa(T - v),  number of holes with kappa >= 2 ).  Classes with exactly 1 filled state are saved to onefill/.
A class with 0 filled states is a counterexample to R* at that hole: written to cert/ immediately (graph + hole), for independent replay.
Moves as search2.py: seeded shuffle of legal flips, evaluate K unvisited, move to the best even if worse, return to best when stuck."""
import sys, os, json, random, time, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
import graphs, radius
BIN = os.path.join(HERE, '..', 'fast', 'kempe_classes3'); LMIN = 40

def kclasses(F, h):
    labels = sorted({x for f in F for x in f}); m = {u: i for i, u in enumerate(labels)}
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
        fh.write('%d %d\n' % (len(labels), len(F)))
        for f in F: fh.write('%d %d %d\n' % tuple(m[x] for x in f))
    out = subprocess.run([BIN, fh.name, str(m[h]), '300000000', str(LMIN)], capture_output=True, text=True).stdout; os.unlink(fh.name)
    return json.loads(out)

def evaluate(F):
    dg = graphs.degrees(F); per = {}
    for h in sorted(v for v in dg if dg[v] == 5): per[h] = kclasses(F, h)
    if any('inconclusive' in r for r in per.values()): return None
    large = [(c[1] / c[0], c[0], c[1], c[2], h) for h, r in per.items() for c in r['classes'] if c[0] >= LMIN]
    large.sort()
    kmax = max(r['n_classes'] for r in per.values()); nmulti = sum(r['n_classes'] >= 2 for r in per.values())
    stuck = [h for h, r in per.items() if r['classes_without_filled_state'] > 0]
    if large:
        hmin = large[0][4]; mc = per[hmin]['min_class']
        score = (1, -large[0][0], mc['far'], kmax)
    else:
        hmin = min(per, key=lambda h: per[h]['min_class']['filled']); mc = per[hmin]['min_class']; score = (0, 0.0, 0, kmax)
    if stuck: score = (2, 0.0, 0, kmax)
    return {'score': score, 'hole_min': hmin, 'min_class': mc, 'stuck_holes': stuck, 'lowest10': [list(x) for x in large[:10]],
            'per': {str(h): {'kappa': r['n_classes'], 'classes': r['classes'], 'min_class': {k: r['min_class'][k] for k in ('size', 'filled', 'DL', 'far')}} for h, r in per.items()}}

def legal(F, maxdeg):
    dg = graphs.degrees(F)
    return min(dg.values()) >= 5 and max(dg.values()) <= maxdeg and graphs.n_separating_triangles(F) == 0

if __name__ == '__main__':
    start, seed, K, cpu, out, maxdeg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5], int(sys.argv[6])
    os.makedirs(os.path.join(out, 'cert'), exist_ok=True); log = open(os.path.join(out, 'log-seed%d.jsonl' % seed), 'a')
    t_end = time.time() + cpu; rng = random.Random(seed)
    cur = [tuple(f) for f in json.load(open(start))['faces']]; ev = evaluate(cur); visited = {radius.graph_hash(cur)}; best = (ev['score'], cur)
    def rec(tag, F, e):
        row = {'tag': tag, 'sha': radius.graph_hash(F), 'n': len(graphs.degrees(F)), 'score': e['score'] if e else None,
               'kappa': {h: p['kappa'] for h, p in e['per'].items()} if e else None}
        log.write(json.dumps(row) + '\n'); log.flush()
        if e: row['min_class'] = {'hole': e['hole_min'], **{k: e['min_class'][k] for k in ('size', 'filled', 'DL', 'far')}}; row['lowest10'] = e['lowest10']
        if e and e['score'][0] == 2:
            json.dump({'faces': [list(f) for f in F], 'per': e['per']}, open(os.path.join(out, 'cert', row['sha'][:16] + '.json'), 'w'))
            print('STUCK CLASS', row['sha'][:16], flush=True)
    rec('start', cur, ev); step = 0
    while time.time() < t_end:
        es = sorted({(min(f[i], f[(i + 1) % 3]), max(f[i], f[(i + 1) % 3])) for f in cur for i in range(3)}); rng.shuffle(es); cands = []
        for a, b in es:
            nf = graphs.flip(cur, a, b)
            if nf is None or not legal(nf, maxdeg): continue
            h = radius.graph_hash(nf)
            if h in visited: continue
            visited.add(h); e = evaluate(nf); rec('step%d' % step, nf, e)
            if e: cands.append((e['score'], nf, e))
            if len(cands) >= K: break
        if not cands:
            if radius.graph_hash(cur) != radius.graph_hash(best[1]): cur = best[1]; continue
            break
        s, nf, e = max(cands, key=lambda c: c[0]); cur = nf
        if s > best[0]: best = (s, nf); json.dump({'faces': [list(f) for f in nf], 'score': list(s)}, open(os.path.join(out, 'best-seed%d.json' % seed), 'w'))
        print('step', step, 'score', s, 'best', best[0], flush=True); step += 1
