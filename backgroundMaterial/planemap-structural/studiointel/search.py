#!/usr/bin/env python3
"""studiointel search.py -- PRODUCER for the R* adversary search (pre-registered in messages/2026-10-06/..._studiointel_..._preregistration-Rstar-adversary-search.md).
 stage A: deterministic list of graphs, every degree-5 hole analysed exactly (radius.analyse).
 stage B: seeded hill-climb by edge flips, degrees kept in [5,7], no separating triangle.
Fitness of a graph T: F(T) = max over faces phi of min over degree-5 v not on phi of rho(v)  (rho None = infinity), primary;
 tie-break mean over degree-5 holes of n_DL/n_states.  Every evaluated graph is logged as one JSON line.
Writes certificates (inputs for check.py) whenever F(T) >= 5 or a targetless class exists at all holes off some face.
CPU cap: --cpu-seconds, measured by time.process_time(); the run stops cleanly when reached (result: capped, never a pass)."""
import sys, json, random, time, os, hashlib, argparse
import graphs, radius
from builders import build

def evaluate(faces, cap_states, deadline):
    dg = graphs.degrees(faces); fives = sorted(v for v in dg if dg[v] == 5); per = {}
    for h in fives:
        if time.process_time() > deadline: return None
        r = radius.analyse(faces, h, cap_states)
        if 'inconclusive' in r: return {'inconclusive': r['inconclusive'], 'hole': h}
        per[h] = r
    INF = 10 ** 9; rho = {h: (INF if per[h]['rho'] is None else per[h]['rho']) for h in fives}
    best = -1; best_phi = None
    for f in faces:
        off = [h for h in fives if h not in f]
        m = min((rho[h] for h in off), default=INF)
        if m > best: best, best_phi = m, f
    frac = sum(per[h]['n_DL'] / per[h]['n_states'] for h in fives) / len(fives)
    return {'F': best, 'phi': list(best_phi), 'mean_DL_frac': round(frac, 6), 'rho': {str(h): (None if rho[h] == INF else rho[h]) for h in fives}, 'per': per}

def write_cert(outdir, tag, faces, ev):
    os.makedirs(outdir, exist_ok=True)
    json.dump({'faces': faces}, open(os.path.join(outdir, tag + '.graph.json'), 'w'))
    json.dump({'phi': ev['phi'], 'rho': ev['rho']}, open(os.path.join(outdir, tag + '.meta.json'), 'w'))
    for h, r in ev['per'].items():
        if 'witness' in r:
            w = r['witness']; json.dump({str(u): c for u, c in zip(w['order'], w['state'])}, open(os.path.join(outdir, '%s.hole%d.state.json' % (tag, h)), 'w'))
            if 'targetless' in r:
                json.dump([{str(u): c for u, c in zip(w['order'], st)} for st in r['targetless']], open(os.path.join(outdir, '%s.hole%d.class.json' % (tag, h)), 'w'))

def neighbours_flip(faces, rng):
    es = sorted({(min(f[i], f[(i + 1) % 3]), max(f[i], f[(i + 1) % 3])) for f in faces for i in range(3)})
    rng.shuffle(es)
    for a, b in es:
        nf = graphs.flip(faces, a, b)
        if nf is None: continue
        dg = graphs.degrees(nf)
        if min(dg.values()) < 5 or max(dg.values()) > 7: continue
        if graphs.n_separating_triangles(nf): continue
        yield nf

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('stage'); ap.add_argument('--specs', default=''); ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--cpu-seconds', type=float, default=1800); ap.add_argument('--cap-states', type=int, default=400000)
    ap.add_argument('--steps', type=int, default=10 ** 6); ap.add_argument('--out', default='out'); ap.add_argument('--start', default='A:5')
    a = ap.parse_args(); deadline = time.process_time() + a.cpu_seconds; os.makedirs(a.out, exist_ok=True)
    log = open(os.path.join(a.out, 'log-%s-seed%d.jsonl' % (a.stage, a.seed)), 'a')
    def record(spec, faces, ev):
        row = {'spec': spec, 'graph_sha256': radius.graph_hash(faces), 'n': len(graphs.degrees(faces)), 'cpu_s': round(time.process_time(), 1)}
        if ev is None: row['status'] = 'capped'
        elif 'inconclusive' in ev: row['status'] = 'inconclusive'; row['why'] = ev['inconclusive']
        else:
            row.update(status='done', F=ev['F'], mean_DL_frac=ev['mean_DL_frac'], rho=ev['rho'])
            if ev['F'] >= 5: write_cert(os.path.join(a.out, 'cert'), row['graph_sha256'][:16], faces, ev); row['certificate'] = row['graph_sha256'][:16]
        log.write(json.dumps(row) + '\n'); log.flush(); return row
    if a.stage == 'A':
        for spec in a.specs.split(','):
            faces = build(spec); ev = evaluate(faces, a.cap_states, deadline); row = record(spec, faces, ev); print(json.dumps({k: row[k] for k in row if k != 'rho'}), flush=True)
            if ev is None: break
    else:
        rng = random.Random(a.seed); cur = build(a.start); ev = evaluate(cur, a.cap_states, deadline)
        row = record(a.start, cur, ev)
        if ev is None or 'inconclusive' in ev: sys.exit('start graph not evaluated')
        key = lambda e: (e['F'], e['mean_DL_frac'])
        for step in range(a.steps):
            moved = False
            for nf in neighbours_flip(cur, rng):
                e2 = evaluate(nf, a.cap_states, deadline)
                record('flip-step%d' % step, nf, e2)
                if e2 is None: sys.exit(0)
                if 'inconclusive' in e2: continue
                if key(e2) > key(ev): cur, ev, moved = nf, e2, True; print('step', step, 'F', ev['F'], 'DL', ev['mean_DL_frac'], flush=True); break
                if time.process_time() > deadline: sys.exit(0)
            if not moved: print('local optimum at step', step, flush=True); break
