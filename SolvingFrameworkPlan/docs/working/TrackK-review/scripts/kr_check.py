"""TrackK review: data check of every step of the hand proof of Conjecture F (TrackK/FProof.md).
Independent code (kr_core.py only).  Usage:
  nice -n 10 python3 -I kr_check.py FAMILY SEED NGRAPHS STEPS
FAMILY in: min3, min5, census, torus, bipyr
"""
import os, sys, random, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from kr_core import *  # noqa

CENSUS = os.path.join(HERE, '..', '..', 'Census29', 'out')

fails = Counter(); counts = Counter(); dist = Counter(); examples = {}


def ok(key, cond, info=None):
    counts[key] += 1
    if not cond:
        fails[key] += 1
        if key not in examples:
            examples[key] = info


def nohole_states(t, genus, rng, steps, fam):
    M = map_of_tri(t); M.validate(2 - 2 * genus)
    vs = set(t.adj)
    col = random_colouring(t.adj, rng)
    if col is None:
        return
    if fam == 'bipyr':   # deliberately start from a 3-colouring
        m = len(t.adj) - 2
        if m % 2 == 0:
            col = {i: i % 2 for i in range(m)}; col[m] = 2; col[m + 1] = 2
    for s in range(steps):
        if s % 3 == 0:
            r = analyse(M, col, genus, want_sep=(genus == 1))
            n = r['n']; N = r['N']; d = r['ds'][0]
            L0 = lemma0_checks(r)
            for kk, vv in L0.items():
                if kk == 'cw_formula':
                    ok('noh:' + kk, r['cw'] == r['F'] // 2 + 2 * d)
                else:
                    ok('noh:' + kk, vv)
            ncol = len(set(col.values()))
            counts['noh:states_%dcol' % ncol] += 1
            for i, pt in enumerate(r['parts']):
                ok('noh:two_reg', pt['two_reg']); ok('noh:sides_ok', pt['sides_ok'])
                ok('noh:gen_ok', pt['gen_ok']); ok('noh:a_mod2', pt['a_mod2']); ok('noh:a_gen', pt['a_gen'])
                ok('noh:b_gen', pt['b_gen']); ok('noh:sumXYb', pt['sumXYb'])
                if genus == 0:
                    ok('noh:G_i=0', pt['G'] == 0); ok('noh:a_exact', pt['a_exact'] is True); ok('noh:b', pt['b'])
                else:
                    ok('noh:torus_G_i_in_01', pt['G'] in (0, 1))
                    ok('noh:torus_G_i=1_iff_all_curves_separating', (pt['G'] == 1) == pt['allsep'])
            res = (2 * N - r['cw'] - n) % 4
            if genus == 0:
                ok('noh:F0 2N=cw+n mod4', res == 0, (n, N, r['cw']))
                ok('noh:N=n+1+d mod2', (N - n - 1 - d) % 2 == 0)
            else:
                ok('noh:torus residue=2G', res == (2 * r['G']) % 4)
                dist['noh:torus G=%d' % r['G']] += 1
                dist['noh:torus residue=%d' % res] += 1
        v = rng.choice(list(vs)); o = rng.choice([c for c in range(4) if c != col[v]])
        kempe_swap(t.adj, col, v, o, vs)


def chains_TminusH(t, h, col):
    vs = [v for v in t.adj if v != h]
    N = 0
    for (X, Y) in PAIRS:
        nodes = [v for v in vs if col[v] in (X, Y)]
        f = uf_count(nodes, [(u, v) for u in nodes for v in t.adj[u] if v != h and col[v] in (X, Y)])
        N += len({f(v) for v in nodes})
    return N


def frame(L, col):
    lc = [col[v] for v in L]
    if len(set(lc)) < 4:
        return None
    js = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]]
    assert len(js) == 1
    j = js[0]
    return [L[(j + s) % 5] for s in range(5)]


def hole_states(t, genus, rng, steps, fam):
    hs = [v for v in t.adj if len(t.adj[v]) == 5]
    rng.shuffle(hs)
    for h in hs[:3]:
        L = oriented_link(t, h)
        vs = set(t.adj) - {h}
        col = random_colouring(t.adj, rng, verts=vs)
        if col is None:
            counts['hole:uncolourable_skip'] += 1
            continue
        n = len(t.adj)
        for s in range(steps):
            x = frame(L, col)
            if x is not None:
                one_state(t, genus, h, L, x, col, n, fam)
            v = rng.choice(list(vs)); o = rng.choice([c for c in range(4) if c != col[v]])
            kempe_swap(t.adj, col, v, o, vs)


def one_state(t, genus, h, L, x, col, n, fam):
    al, mu, A, B = col[x[0]], col[x[1]], col[x[3]], col[x[4]]
    assert col[x[2]] == al and len({al, mu, A, B}) == 4
    vs = set(t.adj) - {h}
    L1 = int(x[3] in kempe_component(t.adj, col, x[1], A, vs))
    L2 = int(x[4] in kempe_component(t.adj, col, x[1], B, vs))
    N = chains_TminusH(t, h, col)
    cw = 0; nf = 0
    for f in t.faces():
        if h in f:
            continue
        nf += 1
        cw += tait_cw(col[f[0]], col[f[1]], col[f[2]])
    hand = int((al ^ mu, al ^ A, al ^ B) in CYC)
    resF = (2 * N - cw - (n - 1) + hand - 2 * (L1 + L2)) % 4
    if os.environ.get('KR_SABOTAGE') == '1':   # sabotage: drop the lock term
        resF = (2 * N - cw - (n - 1) + hand) % 4
    par13 = x[3] in t.adj[x[1]]; par14 = x[4] in t.adj[x[1]]
    counts['hole:states'] += 1
    if par13 or par14:
        counts['hole:parallel_diagonal_states'] += 1
    if par13 and par14:
        counts['hole:both_diagonals_parallel'] += 1
    if par13:
        ok('hole:existing x1x3 => L1', L1 == 1)
    if par14:
        ok('hole:existing x1x4 => L2', L2 == 1)
    # global orientation reversal (reverse every face and the link): F must be invariant
    Lr = L[::-1]; xr = frame(Lr, col)
    alr, mur, Ar, Br = col[xr[0]], col[xr[1]], col[xr[3]], col[xr[4]]
    handr = int((alr ^ mur, alr ^ Ar, alr ^ Br) in CYC)
    L1r = int(xr[3] in kempe_component(t.adj, col, xr[1], Ar, vs))
    L2r = int(xr[4] in kempe_component(t.adj, col, xr[1], Br, vs))
    resFr = (2 * N - (nf - cw) - (n - 1) + handr - 2 * (L1r + L2r)) % 4
    ok('hole:F residue orientation-invariant', resFr == resF)
    # wrong convention (link reversed but faces not): must be odd
    hand_bad = handr
    ok('hole:mismatched convention gives odd residue',
       (2 * N - cw - (n - 1) + hand_bad - 2 * (L1r + L2r)) % 2 == 1)
    # the filled map
    M = filled_map(t, h, x)
    M.validate(2 - 2 * genus)
    r = analyse(M, col, genus, want_sep=(genus == 1))
    ok('S1 N(T-h)=N(T°)+2-L1-L2', N == r['N'] + 2 - L1 - L2, (N, r['N'], L1, L2))
    ok('S2 cw(T°)=cw+3hand', r['cw'] == cw + 3 * hand, (r['cw'], cw, hand))
    # T2 on the actual new faces
    for f in M.faces[-3:]:
        ok('S2b each new face cw==hand', int(tait_cw(col[f[0]], col[f[1]], col[f[2]])) == hand)
    L0 = lemma0_checks(r); d = r['ds'][0]
    for kk, vv in L0.items():
        ok('L0:' + kk, vv)
    for pt in r['parts']:
        ok('P1:two_reg', pt['two_reg']); ok('P1:sides_ok', pt['sides_ok']); ok('P1:gen_ok', pt['gen_ok'])
        ok('P1:a_mod2', pt['a_mod2']); ok('P1:a_gen', pt['a_gen']); ok('P1:b_gen', pt['b_gen'])
        ok('P1:sumXYb', pt['sumXYb'])
        if genus == 0:
            ok('P1:G_i=0 (every region planar, chi=2-b)', pt['G'] == 0)
            ok('P1:(a) exact', pt['a_exact'] is True); ok('P1:(b)', pt['b'])
        else:
            ok('torus:G_i in {0,1}', pt['G'] in (0, 1))
            ok('torus:G_i=1 iff all curves separating', (pt['G'] == 1) == pt['allsep'])
    res0 = (2 * r['N'] - r['cw'] - r['n']) % 4
    if genus == 0:
        ok('S6 F0 on T°', res0 == 0)
        ok('F0 N(T°)=n(T°)+1+d mod2', (r['N'] - r['n'] - 1 - d) % 2 == 0)
        ok('remark N+L1+L2=n+d mod2', (N + L1 + L2 - n - d) % 2 == 0)
        ok('S7 F', resF == 0, (fam, n, N, cw, hand, L1, L2))
    else:
        ok('S8 torus: F residue = 2G (G in T°)', resF == (2 * r['G']) % 4)
        ok('torus: F0 residue on T° = 2G', res0 == (2 * r['G']) % 4)
        dist['torus G=%d' % r['G']] += 1
        dist['torus F residue=%d' % resF] += 1


def graphs(fam, rng, ng):
    if fam == 'min3':
        for _ in range(ng):
            yield random_tri(tetra(), rng.randint(8, 40), rng, 300), 0
    elif fam == 'min5':
        for _ in range(ng):
            n = rng.choice([12] + list(range(14, 41)))
            t = random_min5(n, rng, 300)
            if t is not None:
                yield t, 0
    elif fam == 'census':
        files = sorted(f for f in os.listdir(CENSUS) if f.startswith('frame-') and f.endswith('.txt'))
        per = max(1, ng // len(files))
        for fn in files:
            lines = [l for l in open(os.path.join(CENSUS, fn)).read().split('\n') if l.strip()]
            for l in rng.sample(lines, min(per, len(lines))):
                yield from_census(l), 0
    elif fam == 'torus':
        for _ in range(ng):
            base = torus_grid(rng.choice([3, 4]), rng.choice([3, 4]))
            yield random_tri(base, rng.randint(20, 40), rng, 600), 1
    elif fam == 'bipyr':
        for _ in range(ng):
            yield bipyramid(rng.randint(3, 20)), 0


def main():
    fam, seed, ng, steps = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed); t0 = time.time(); ngr = 0
    for t, genus in graphs(fam, rng, ng):
        ngr += 1
        assert t.euler() == 2 - 2 * genus
        nohole_states(t, genus, rng, max(6, steps // 10), fam)
        if fam != 'bipyr':
            hole_states(t, genus, rng, steps, fam)
    print('family=%s seed=%d graphs=%d steps=%d time=%.0fs' % (fam, seed, ngr, steps, time.time() - t0))
    for k in sorted(counts):
        print('  %-55s checks=%-9d fails=%d' % (k, counts[k], fails[k]))
    for k in sorted(dist):
        print('  dist %-50s %d' % (k, dist[k]))
    for k, v in examples.items():
        print('  FIRST FAILURE', k, v)
    print('TOTAL FAILURES', sum(fails.values()), flush=True)


if __name__ == '__main__':
    main()
