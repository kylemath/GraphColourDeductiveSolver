"""Track I review driver: Theorem 6 (primal only) + step checks (Tait) on fresh surfaces.

usage: python3 ri_run.py SOURCE SEED COUNT OUT.json [--tait]
SOURCE in sphere5 | sphere3 | census | rp2 | torus
"""
import sys, json, random, time
from collections import Counter
import ri_core as rc
from ri_tait import check_state

CENSUS = '/Users/kylemathewson/GraphColourDeductiveSolver/SolvingFrameworkPlan/docs/working/Census29/out/frame-%d.txt'


def states_for(nbr, rng, n, full_limit=150000, sample=2500):
    if n <= 27:
        cols = rc.enumerate_colourings(nbr, limit=full_limit)
        if len(cols) < full_limit:
            return cols, 'full'
    # Kempe-walk sample with restarts
    seen = set(); out = []
    restarts = 0
    while len(out) < sample and restarts < 8:
        restarts += 1
        c = rc.random_colouring(nbr, rng)
        if c is None:
            continue
        for _ in range(sample * 4):
            v = rng.randrange(len(nbr)); o = rng.randrange(4)
            if o == c[v]:
                continue
            c = rc.kempe_swap(nbr, c, v, o)
            k = rc.normalise(c)
            if k not in seen:
                seen.add(k); out.append(k)
                if len(out) >= sample:
                    break
    return out, 'sample'


def run_surface(s, tag, stats, rng, tait, tait_cap=400, holes_cap=None):
    holes = [h for h in s.V if len(s.adj[h]) == 5]
    if holes_cap:
        rng.shuffle(holes); holes = holes[:holes_cap]
    for h in holes:
        L0 = s.link(h)
        V, ix, nbr = rc.graph_minus(s, h)
        L = [ix[x] for x in L0]
        cols, mode = states_for(nbr, rng, len(s.V))
        stats['holes'] += 1; stats['mode_' + mode] += 1
        low = any(len(s.adj[x]) <= 4 for x in L0)
        if low:
            stats['holes_lowdeg_link'] += 1
        ntait = 0
        for col in cols:
            st = rc.hole_state(nbr, col, L)
            stats['states'] += 1
            if st is None:
                continue
            stats['unfilled'] += 1
            if not st['DL']:
                continue
            stats['DL'] += 1
            colp, K = rc.pi_move(nbr, col, st)
            if colp is None:
                stats['DL_pi_undefined'] += 1
                continue
            stp = rc.hole_state(nbr, colp, L)
            assert stp is not None and stp['j'] == (st['j'] + 3) % 5
            assert (stp['al'], stp['mu'], stp['A'], stp['B']) == (st['al'], st['B'], st['mu'], st['A'])
            stp['col'] = colp
            Nc = rc.N_total(nbr, col); Np = rc.N_total(nbr, colp)
            ok6 = ((Np - Nc) % 2) == int(stp['DL'])
            stats['thm6_tested'] += 1
            if low:
                stats['thm6_tested_lowdeg_link'] += 1
                stats['thm6_lowdeg_FAIL'] += (((Np - Nc) % 2) != int(stp['DL']))
            if not ok6:
                stats['thm6_FAIL'] += 1
            key = 'DL->DL' if stp['DL'] else 'DL->nonDL'
            stats[key] += 1
            stats[key + '_dN_odd'] += (Np - Nc) % 2
            rig = rc.counts6(nbr, col, st) == rc.RIGID
            if rig:
                stats['rigid'] += 1
                if Nc != 8:
                    stats['rigid_N_not8'] += 1
                if stp['DL'] and rc.counts6(nbr, colp, stp) == rc.RIGID:
                    stats['RI_FAIL'] += 1
            elif Nc == 8:
                stats['N8_not_rigid'] += 1
            if Nc < 8:
                stats['N_lt8'] += 1
            if tait and ntait < tait_cap:
                ntait += 1
                try:
                    r = check_state(s, h, ix, nbr, col, st, stp, K, Np, Nc)
                except AssertionError as ex:
                    stats['tait_assert'] += 1
                    continue
                stats['tait_states'] += 1
                if r.get('holed'):
                    stats['tait_holed'] += 1
                    stats['thm6_holed_tested'] += 1
                    stats['thm6_holed_FAIL'] += (not ok6)
                piiok = r.get('Pii_noncross') and r.get('Pii_samecircle')
                if not piiok:
                    stats['joint_Pii_bad'] += 1
                    stats['joint_Pii_bad_LemmaR_fail'] += (r['LemmaR_concl'] is False)
                else:
                    stats['joint_Pii_ok_LemmaR_fail'] += (r['LemmaR_concl'] is False)
                    stats['joint_Pii_ok_Lemma5_fail'] += (r['Lemma5'] is False)
                for k2, v2 in r.items():
                    if k2 == 'holed':
                        continue
                    if v2 is False:
                        stats['FAIL_' + k2] += 1
                    elif v2 is True:
                        stats['ok_' + k2] += 1


def make_surfaces(source, seed, count):
    rng = random.Random(seed)
    if source == 'census':
        lines = []
        for n in range(22, 33):
            with open(CENSUS % n) as f:
                L = f.read().splitlines()
            lines += L
        rng.shuffle(lines)
        for line in lines[:count]:
            name, s = rc.parse_census_line(line)
            assert s.check() and s.euler() == 2
            yield name, s
        return
    for i in range(count):
        if source == 'sphere5':
            n = rng.randint(14, 40)
            s = rc.random_surface(rc.tetra(), n, rng, 200 * n, target_min5=True)
            if rc.min_degree(s) < 5:
                continue
            assert s.euler() == 2
        elif source == 'sphere3':
            n = rng.randint(8, 30)
            s = rc.random_surface(rc.tetra(), n, rng, 10 * n, mindeg=3)
            assert s.euler() == 2
        elif source == 'rp2':
            n = rng.randint(12, 26)
            s = rc.random_surface(rc.rp2_6(), n, rng, 30 * n, target_min5=(i % 2 == 0))
            assert s.euler() == 1
        elif source == 'torus':
            n = rng.randint(12, 26)
            s = rc.random_surface(rc.torus_grid(3, 4), n, rng, 30 * n, target_min5=(i % 2 == 0))
            assert s.euler() == 0
        assert s.check()
        yield '%s_%d_%d' % (source, seed, i), s


if __name__ == '__main__':
    source, seed, count, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    tait = '--tait' in sys.argv
    holes_cap = None
    for a in sys.argv:
        if a.startswith('--holes='):
            holes_cap = int(a.split('=')[1])
    stats = Counter(); rng = random.Random(seed + 1)
    t0 = time.time(); ng = 0
    mind = Counter()
    for name, s in make_surfaces(source, seed, count):
        ng += 1
        mind[rc.min_degree(s)] += 1
        run_surface(s, source, stats, rng, tait, holes_cap=holes_cap)
        if ng % 5 == 0:
            print(source, ng, dict(thm6=stats['thm6_tested'], fail=stats['thm6_FAIL'], t=round(time.time() - t0)), flush=True)
        json.dump(dict(source=source, seed=seed, graphs=ng, mindeg=dict(mind), stats=dict(stats),
                       secs=round(time.time() - t0)), open(out, 'w'), indent=1, sort_keys=True)
    print('done', source, ng, dict(stats))
