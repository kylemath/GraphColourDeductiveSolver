#!/usr/bin/env python3
"""path3-local/kc_search_local.py -- [exploratory] Local intel (MacBook), 6 Oct 2026. Path 3 v3 search, extended.
Same objective and tabu walk as ../path3/kc_search3.py (v3): score = (2 if some class of T - v has no filled state, else 1 if a class of
size >= LMIN exists, -lowest filled fraction among classes of size >= LMIN over all degree-5 holes, far of that class, max kappa).
Core class kept on every move: min degree >= 5, max degree <= MAXDEG, no separating triangle (= 4-connected), sphere triangulation.
Additions:
  * TARGETED FLIPS (Math 16:45 note, item 3): engine v4 reports, for the target class R (lowest filled fraction at the target hole)
    and every flip ab -> cd avoiding the hole, how many filled / unfilled states of R have col(c) = col(d) (the flip removes those).
    Each step evaluates the KT best-ranked legal targeted flips (rank: filled fraction of R's survivors, survivors >= LMIN), then fills
    up to K candidates with random legal flips. Every candidate is re-evaluated in full (flips also add states and merge components).
  * INTERN C SIGNATURE: every evaluated hole reports, for each class with exactly one filled state f, the number of bichromatic
    components of f missing the link (must be 0). Totals are logged; any violation is saved to sigviol/.
  * STUCK CLASS: if any class has no filled state, the engine dumps all its states; the certificate (faces, hole, order, all states)
    is written to cert/ at once, replayed with Math's independent checker (path3_kclasses.analyse_hole), and the run STOPS (exit 42).
Usage: kc_search_local.py SEED_GRAPH SEED K KT WALL_SECONDS OUTDIR MAXDEG TAG"""
import sys, os, json, random, time, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib  # noqa
from lib import graphs, load_faces, ghash, core_ok, checker_json, MATH
lib.BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kempe_classes4')
LMIN = 40; CAP = 30000000


def evaluate(F, tmpdir):
    dg = graphs.degrees(F); per = {}; dumps = {}
    for h in sorted(v for v in dg if dg[v] == 5):
        dp = os.path.join(tmpdir, 'dump_h%d.txt' % h)
        if os.path.exists(dp): os.unlink(dp)
        r = _kc(F, h, dp)
        if 'classes' not in r: return None
        per[h] = r
        if r['classes_without_filled_state'] > 0: dumps[h] = dp
    large = sorted((c[1] / c[0], c[0], c[1], c[2], h) for h, r in per.items() for c in r['classes'] if c[0] >= LMIN)
    kmax = max(r['n_classes'] for r in per.values())
    sig = {'onefill': sum(r['sig']['onefill_classes'] for r in per.values()), 'viol': sum(r['sig']['violations'] for r in per.values())}
    if large:
        hmin = large[0][4]; score = (1, -large[0][0], per[hmin]['min_class']['far'], kmax)
    else:
        hmin = min(per, key=lambda h: per[h]['min_class']['filled']); score = (0, 0.0, 0, kmax)
    if dumps: score = (2, 0.0, 0, kmax)
    return {'score': score, 'hole': hmin, 'per': per, 'large10': [list(x) for x in large[:10]], 'sig': sig, 'dumps': dumps,
            'target': {k: per[hmin]['min_class'][k] for k in ('size', 'filled', 'DL', 'far')}}


def _kc(F, h, dump):
    import subprocess, tempfile
    labels = sorted({x for f in F for x in f}); m = {u: i for i, u in enumerate(labels)}
    assert labels == list(range(len(labels)))
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
        fh.write('%d %d\n' % (len(labels), len(F)))
        for f in F: fh.write('%d %d %d\n' % f)
    out = subprocess.run([lib.BIN, fh.name, str(h), str(CAP), str(LMIN), dump], capture_output=True, text=True).stdout
    os.unlink(fh.name)
    return json.loads(out)


def legal(F, maxdeg):
    dg = graphs.degrees(F)
    return min(dg.values()) >= 5 and max(dg.values()) <= maxdeg and graphs.n_separating_triangles(F) == 0


def write_cert(F, ev, out, tag):
    p3k_spec = importlib.util.spec_from_file_location('p3k', os.path.join(MATH, 'path3_kclasses.py'))
    p3k = importlib.util.module_from_spec(p3k_spec); p3k_spec.loader.exec_module(p3k)
    sha = ghash(F)[:16]
    for h, dp in ev['dumps'].items():
        lines = open(dp).read().strip().split('\n')
        order = [int(x) for x in lines[0].split(':')[1].split()]
        states = {}
        for L in lines[2:]:
            t = list(map(int, L.split())); states.setdefault(t[0], []).append({'kind': t[1], 'colours': t[2:]})
        cert = {'WARNING': '[exploratory] candidate stuck class (counterexample to R* at hole); NOT verified until replayed independently',
                'tag': tag, 'graph_sha256': ghash(F), 'faces': [list(f) for f in F], 'hole': h, 'order_T_minus_v': order,
                'engine': {k: ev['per'][h][k] for k in ('n_states', 'n_classes', 'classes', 'classes_without_filled_state')},
                'stuck_classes': list(states.values())}
        cp = os.path.join(out, 'cert', '%s.hole%d.json' % (sha, h))
        json.dump(cert, open(cp, 'w'))
        print('STUCK CLASS written', cp, flush=True)
        try:   # independent replay (Math's pure-Python checker, imports nothing from the engine)
            rep = p3k.analyse_hole(checker_json(F, sha), h, 5000000)
        except OverflowError:
            rep = {'inconclusive': 'checker state cap'}
        json.dump(rep, open(cp.replace('.json', '.checker.json'), 'w'))
        print('CHECKER new_classes', rep.get('new_classes'), 'kH', rep.get('kH'), flush=True)


if __name__ == '__main__':
    start, seed, K, KT, wall, out, maxdeg, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), sys.argv[6], int(sys.argv[7]), sys.argv[8]
    for d in ('cert', 'sigviol', 'tmp-%s' % tag): os.makedirs(os.path.join(out, d), exist_ok=True)
    tmp = os.path.join(out, 'tmp-%s' % tag)
    log = open(os.path.join(out, 'log-%s.jsonl' % tag), 'a'); rng = random.Random(seed); t_end = time.time() + wall
    cur = load_faces(start); ok, why = core_ok(cur, maxdeg)
    if not ok: print('seed not core:', why); sys.exit(2)
    stats = {'evals': 0, 'onefill': 0, 'sigviol': 0, 'acc_targeted': 0, 'acc_random': 0, 'imp_targeted': 0, 'imp_random': 0}

    def rec(kind, F, e, step):
        stats['evals'] += 1
        row = {'tag': tag, 'step': step, 'move': kind, 'sha': ghash(F)[:16], 'n': len(graphs.degrees(F))}
        if e:
            row.update({'score': e['score'], 'hole': e['hole'], 'target': e['target'], 'large10': e['large10'], 'sig': e['sig'],
                        'kappa': {h: p['n_classes'] for h, p in e['per'].items()}})
            stats['onefill'] += e['sig']['onefill']; stats['sigviol'] += e['sig']['viol']
            if e['sig']['viol']:
                json.dump({'faces': [list(f) for f in F], 'per_sig': {h: p['sig'] for h, p in e['per'].items()}},
                          open(os.path.join(out, 'sigviol', row['sha'] + '.json'), 'w'))
                print('INTERN C SIGNATURE VIOLATION', row['sha'], flush=True)
        log.write(json.dumps(row) + '\n'); log.flush()
        if e and e['score'][0] == 2:
            write_cert(F, e, out, tag); log.write(json.dumps({'STOP': 'stuck class', 'sha': row['sha'], 'stats': stats}) + '\n'); log.close()
            sys.exit(42)

    ev = evaluate(cur, tmp); visited = {ghash(cur)}; rec('seed', cur, ev, -1); best = (ev['score'], cur, ev); curev = ev; step = 0
    while time.time() < t_end:
        cands = []
        # targeted flips from the current target class
        tf = []
        S, Fl = curev['target']['size'], curev['target']['filled']
        for a, b, c, d, fs, us in curev['per'][curev['hole']]['flips']:
            surv = S - fs - us
            if fs == 0 or surv < LMIN: continue
            tf.append(((Fl - fs) / surv, -surv, a, b))
        tf.sort()
        for _, _, a, b in tf:
            if len([c for c in cands if c[3] == 'targeted']) >= KT: break
            nf = graphs.flip(cur, a, b)
            if nf is None or not legal(nf, maxdeg): continue
            h = ghash(nf)
            if h in visited: continue
            visited.add(h); e = evaluate(nf, tmp); rec('targeted', nf, e, step)
            if e: cands.append((e['score'], nf, e, 'targeted'))
        # random flips (v3 move)
        es = sorted({(min(f[i], f[(i + 1) % 3]), max(f[i], f[(i + 1) % 3])) for f in cur for i in range(3)}); rng.shuffle(es)
        for a, b in es:
            if len(cands) >= K or time.time() > t_end: break
            nf = graphs.flip(cur, a, b)
            if nf is None or not legal(nf, maxdeg): continue
            h = ghash(nf)
            if h in visited: continue
            visited.add(h); e = evaluate(nf, tmp); rec('random', nf, e, step)
            if e: cands.append((e['score'], nf, e, 'random'))
        if not cands:
            if ghash(cur) != ghash(best[1]): cur, curev = best[1], best[2]; continue
            break
        s, nf, e, kind = max(cands, key=lambda c: c[0]); cur, curev = nf, e; stats['acc_' + kind] += 1
        if s > best[0]:
            stats['imp_' + kind] += 1; best = (s, nf, e)
            json.dump({'faces': [list(f) for f in nf], 'score': list(s), 'hole': e['hole'], 'target': e['target'], 'large10': e['large10']},
                      open(os.path.join(out, 'best-%s.json' % tag), 'w'))
        print('step', step, kind, 'score', s, 'best', best[0], flush=True); step += 1
    log.write(json.dumps({'END': True, 'best_score': best[0], 'stats': stats}) + '\n'); log.close()
    for f in os.listdir(tmp): os.unlink(os.path.join(tmp, f))
    os.rmdir(tmp)
    print('END', best[0], stats, flush=True)
