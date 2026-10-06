#!/usr/bin/env python3
"""studiointel search2.py -- PRODUCER for Phase C (declared in messages/2026-10-06/..._studiointel_..._declaration-phase-C-tabu.md).
Tabu search by edge flips in the core class: min degree >= 5, max degree <= 8, no separating triangle. Order is fixed by the seed graph.
Score of a graph = (#degree-5 holes with rho >= 4, #holes with rho >= 3, mean DL fraction), lexicographic; rho None (targetless) counts as infinite.
Each step: shuffle the legal flips (random.Random(seed)), evaluate the first K not previously visited (visited = all graph hashes seen, the tabu list),
move to the best of them EVEN IF it is not better (plateau / downhill allowed), keep the global best. When the current graph has no unvisited legal flip it returns to the global best; it stops at the CPU cap or when the best has none either.
Also stage X: exact analysis of one spec (radius.analyse at every degree-5 hole) with a given state cap.
Certificates (written for check.py) whenever any hole has rho >= 5 or rho None: graph, witness state, targetless class."""
import sys, json, random, time, os, argparse
import graphs, radius, search
from builders import build

def load(spec):
    if spec.startswith('json:'): return [tuple(f) for f in json.load(open(spec[5:]))['faces']]
    return build(spec)

def legal_flips(faces, rng):
    es = sorted({(min(f[i], f[(i + 1) % 3]), max(f[i], f[(i + 1) % 3])) for f in faces for i in range(3)})
    rng.shuffle(es)
    for a, b in es:
        nf = graphs.flip(faces, a, b)
        if nf is None: continue
        dg = graphs.degrees(nf)
        if min(dg.values()) < 5 or max(dg.values()) > 8: continue
        if graphs.n_separating_triangles(nf): continue
        yield nf

def score(ev):
    rs = [(10 ** 9 if r is None else r) for r in ev['rho'].values()]
    return (sum(r >= 4 for r in rs), sum(r >= 3 for r in rs), ev['mean_DL_frac'])

def certify(outdir, faces, ev):
    hot = [h for h, r in ev['per'].items() if r['rho'] is None or r['rho'] >= 5]
    if not hot: return None
    tag = radius.graph_hash(faces)[:16]; search.write_cert(outdir, tag, faces, ev)
    return tag

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('stage'); ap.add_argument('--start'); ap.add_argument('--seed', type=int, default=0); ap.add_argument('--K', type=int, default=6)
    ap.add_argument('--cpu-seconds', type=float, default=1800); ap.add_argument('--cap-states', type=int, default=400000); ap.add_argument('--out', default='out')
    a = ap.parse_args(); deadline = time.process_time() + a.cpu_seconds; os.makedirs(a.out, exist_ok=True)
    log = open(os.path.join(a.out, 'log-%s-seed%d.jsonl' % (a.stage, a.seed)), 'a')
    def record(tag, faces, ev):
        row = {'tag': tag, 'graph_sha256': radius.graph_hash(faces), 'n': len(graphs.degrees(faces)), 'cpu_s': round(time.process_time(), 1)}
        if ev is None: row['status'] = 'capped'
        elif 'inconclusive' in ev: row['status'] = 'inconclusive'; row['why'] = ev['inconclusive']
        else:
            row.update(status='done', score=list(score(ev)), F=ev['F'], rho=ev['rho'])
            c = certify(os.path.join(a.out, 'cert'), faces, ev)
            if c: row['certificate'] = c; print('CERTIFICATE', c, flush=True)
        log.write(json.dumps(row) + '\n'); log.flush(); return row
    cur = load(a.start); ev = search.evaluate(cur, a.cap_states, deadline); record('start', cur, ev)
    if a.stage == 'X' or ev is None or 'inconclusive' in ev: sys.exit(0)
    rng = random.Random(a.seed); visited = {radius.graph_hash(cur)}; best = (score(ev), cur)
    step = 0
    while time.process_time() < deadline:
        cands = []
        for nf in legal_flips(cur, rng):
            h = radius.graph_hash(nf)
            if h in visited: continue
            visited.add(h); e2 = search.evaluate(nf, a.cap_states, deadline); record('step%d' % step, nf, e2)
            if e2 is None: sys.exit(0)
            if 'inconclusive' in e2: continue
            cands.append((score(e2), nf, e2))
            if len(cands) >= a.K: break
        if not cands:
            if radius.graph_hash(cur) != radius.graph_hash(best[1]):
                cur = best[1]; print('stuck at step', step, '- back to the global best', flush=True); continue
            print('no unvisited legal flip around the global best at step', step, '- stop', flush=True); break
        s, nf, e2 = max(cands, key=lambda c: c[0]); cur, ev = nf, e2
        if s > best[0]:
            best = (s, nf); json.dump({'faces': nf, 'score': list(s)}, open(os.path.join(a.out, 'best-seed%d.json' % a.seed), 'w'))
        print('step', step, 'score', s, 'best', best[0], flush=True); step += 1
