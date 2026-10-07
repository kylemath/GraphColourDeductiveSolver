#!/usr/bin/env python3
"""path3-local/kc_dd_search.py -- [exploratory] Local intel, 6 Oct 2026. Math's C6 adversary objective (MathQuarterFloorBijections.md).
Engine: kempe_dd (every class at every degree-5 hole: Gamma paths/cycles of R+3, DD_j, room_j, excess_j = |DD_j| - room_j, identity
checks). Graph score (lexicographic, larger is better), over all holes and classes:
  MODE exc:   (#classes with 3F < U,  max excess_j,  max DL chain length,  -min filled fraction among classes with chain >= 2)
  MODE chain: (#classes with 3F < U,  max DL chain length,  max excess_j,  -min filled fraction among classes with chain >= 2)
DL chain length = max over the class of d(P) (DL states inside a Gamma path) and of cycle lengths (all-DL Gamma cycles).
Moves: random legal edge flips (core class kept: min degree >= 5, max degree <= MAXDEG, no separating triangle); tabu walk as v3.
Any class with 3F < U (filled fraction < 1/4) or F = 0: all its states are written to cert/ at once, replayed with Math's independent
checker (path3_kclasses.analyse_hole), and the run STOPS (exit 42). Identity / dichotomy check failures are logged (checks_bad).
Usage: kc_dd_search.py SEED_GRAPH SEED K WALL_SECONDS OUTDIR MAXDEG MODE TAG"""
import sys, os, json, random, time, subprocess, tempfile, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib  # noqa
from lib import graphs, load_faces, ghash, core_ok, checker_json, MATH
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kempe_dd'); CAP = 30000000


def run_hole(F, h, dump):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
        fh.write('%d %d\n' % (1 + max(x for f in F for x in f), len(F)))
        for f in F: fh.write('%d %d %d\n' % tuple(f))
    out = subprocess.run([BIN, fh.name, str(h), str(CAP), dump], capture_output=True, text=True).stdout
    os.unlink(fh.name)
    return json.loads(out)


def evaluate(F, tmp, mode):
    dg = graphs.degrees(F); per = {}; dumps = {}
    for h in sorted(v for v in dg if dg[v] == 5):
        dp = os.path.join(tmp, 'dump_h%d.txt' % h)
        if os.path.exists(dp): os.unlink(dp)
        r = run_hole(F, h, dp)
        if 'summary' not in r: return None
        per[h] = r
        if r['summary']['below_quarter'] > 0: dumps[h] = dp
    S = [r['summary'] for r in per.values()]
    below = sum(s['below_quarter'] for s in S); exc = max(s['max_excess'] for s in S); chain = max(s['max_chain'] for s in S)
    mf = [s['min_frac_chain2'] for s in S if s['min_frac_chain2'] >= 0]; mfl = min(mf) if mf else 1.0
    score = (below, exc, chain, -mfl) if mode == 'exc' else (below, chain, exc, -mfl)
    bad = sum(v for r in per.values() for v in r['checks'].values())
    hx = max(per, key=lambda h: (per[h]['summary']['max_excess'], per[h]['summary']['max_chain']))
    return {'score': score, 'per': per, 'dumps': dumps, 'checks_bad': bad,
            'stats': {'max_excess': exc, 'max_chain': chain, 'max_DDsum': max(s['max_DDsum'] for s in S), 'max_DD': max(s['max_DD'] for s in S),
                      'min_frac': min(s['min_frac'] for s in S), 'min_frac_chain2': mfl, 'below': below,
                      'excess_hole': hx, 'excess_class': per[hx]['summary']['excess_class']}}


def write_cert(F, ev, out, tag):
    spec = importlib.util.spec_from_file_location('p3k', os.path.join(MATH, 'path3_kclasses.py'))
    p3k = importlib.util.module_from_spec(spec); spec.loader.exec_module(p3k)
    sha = ghash(F)[:16]
    for h, dp in ev['dumps'].items():
        lines = open(dp).read().strip().split('\n'); order = [int(x) for x in lines[0].split(':')[1].split()]
        states = {}
        for L in lines[2:]:
            t = list(map(int, L.split())); states.setdefault(t[0], []).append({'filled': t[1], 'colours': t[2:]})
        bad = [c for c in ev['per'][h]['classes'] if 3 * c['F'] < c['U'] or c['F'] == 0]
        cert = {'WARNING': '[exploratory] candidate class with filled fraction < 1/4 at a degree-5 hole; NOT verified until replayed',
                'tag': tag, 'graph_sha256': ghash(F), 'faces': [list(f) for f in F], 'hole': h, 'order_T_minus_v': order,
                'engine_classes': bad, 'classes_states': list(states.values())}
        cp = os.path.join(out, 'cert', '%s.hole%d.json' % (sha, h)); json.dump(cert, open(cp, 'w'))
        print('BELOW-QUARTER CLASS written', cp, flush=True)
        try:
            rep = p3k.analyse_hole(checker_json(F, sha), h, 5000000)
            rep['replay_match'] = [any(c['size'] == b['size'] and c['filled_states'] == b['F'] for c in rep['classes']) for b in bad]
        except OverflowError:
            rep = {'inconclusive': 'checker state cap'}
        json.dump(rep, open(cp.replace('.json', '.checker.json'), 'w'))
        print('CHECKER', rep.get('replay_match'), flush=True)


if __name__ == '__main__':
    start, seed, K, wall, out, maxdeg, mode, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5], int(sys.argv[6]), sys.argv[7], sys.argv[8]
    for d in ('cert', 'tmp-%s' % tag): os.makedirs(os.path.join(out, d), exist_ok=True)
    tmp = os.path.join(out, 'tmp-%s' % tag); log = open(os.path.join(out, 'log-%s.jsonl' % tag), 'a'); rng = random.Random(seed); t_end = time.time() + wall
    cur = load_faces(start) if not start.startswith('A_') else [tuple(f) for f in graphs.A_r(int(start[2:]))]
    ok, why = core_ok(cur, maxdeg)
    if not ok: print('seed not core:', why); sys.exit(2)
    tot = {'evals': 0, 'checks_bad': 0}

    def rec(F, e, step):
        tot['evals'] += 1
        row = {'tag': tag, 'step': step, 'sha': ghash(F)[:16], 'n': len(graphs.degrees(F))}
        if e:
            row.update({'score': e['score'], 'stats': e['stats'], 'checks_bad': e['checks_bad']}); tot['checks_bad'] += e['checks_bad']
            if e['checks_bad']: print('CHECK FAILURE', row['sha'], flush=True); json.dump({'faces': [list(f) for f in F], 'per': e['per']}, open(os.path.join(out, 'checkfail-%s.json' % row['sha']), 'w'))
        log.write(json.dumps(row) + '\n'); log.flush()
        if e and e['score'][0] > 0:
            write_cert(F, e, out, tag); log.write(json.dumps({'STOP': 'below quarter', 'sha': row['sha']}) + '\n'); log.close(); sys.exit(42)

    ev = evaluate(cur, tmp, mode); visited = {ghash(cur)}; rec(cur, ev, -1); best = (ev['score'], cur, ev); step = 0
    json.dump({'faces': [list(f) for f in cur], 'score': list(ev['score']), 'stats': ev['stats']}, open(os.path.join(out, 'best-%s.json' % tag), 'w'))
    while time.time() < t_end:
        es = sorted({(min(f[i], f[(i + 1) % 3]), max(f[i], f[(i + 1) % 3])) for f in cur for i in range(3)}); rng.shuffle(es); cands = []
        for a, b in es:
            if len(cands) >= K or time.time() > t_end: break
            nf = graphs.flip(cur, a, b)
            if nf is None or not core_ok(nf, maxdeg)[0]: continue
            h = ghash(nf)
            if h in visited: continue
            visited.add(h); e = evaluate(nf, tmp, mode); rec(nf, e, step)
            if e: cands.append((e['score'], nf, e))
        if not cands:
            if ghash(cur) != ghash(best[1]): cur = best[1]; continue
            break
        s, nf, e = max(cands, key=lambda c: c[0]); cur = nf
        if s > best[0]:
            best = (s, nf, e); json.dump({'faces': [list(f) for f in nf], 'score': list(s), 'stats': e['stats']}, open(os.path.join(out, 'best-%s.json' % tag), 'w'))
        print('step', step, 'score', s, 'best', best[0], flush=True); step += 1
    log.write(json.dumps({'END': True, 'best_score': best[0], 'best_stats': best[2]['stats'], 'totals': tot}) + '\n'); log.close()
    for f in os.listdir(tmp): os.unlink(os.path.join(tmp, f))
    os.rmdir(tmp); print('END', best[0], best[2]['stats'], tot, flush=True)
