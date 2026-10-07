# [exploratory] Charge map for the "Wrapping the sphere" page.
# Reads docs/wrap/data.json (made by build_data.py), adds a "charge" block, writes it back and rebuilds index.html
# from template.html (the only substitution is __DATA__ -> the JSON text).
# Run from the repo root:  nice -n 10 python3 docs/wrap/build_charge.py [--stats]
# Heawood charge q(v) = sum of signs of the faces at v; face sign = +1 if the triangle (C[col a], C[col b], C[col c])
# is outward on the tetrahedron. Colours are NOT renamed here: an odd renaming flips every sign, so the labelled
# colouring is carried along each shortest Kempe fill (BFS over canonical states, labelled colouring tracked beside).
import json, sys, math, itertools, collections
sys.path.insert(0, 'backgroundMaterial/planemap-structural/longtable/local-runs/common')
from kempe_py import Space
SRC = 'backgroundMaterial/planemap-structural/studiointel/fcycle/fcycle_order22.json'
D = json.load(open('docs/wrap/data.json')); J = json.load(open(SRC))
n, F, HOLE, LINK = D['n'], [tuple(f) for f in D['faces']], D['hole'], D['link']
adj = {v: set() for v in range(n)}
for a, b, c in F:
    for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
# graph distance from the hole (hole = 0, link = 1, ring 2 = 2, ...)
dist = {HOLE: 0}; q = collections.deque([HOLE])
while q:
    u = q.popleft()
    for w in adj[u]:
        if w not in dist: dist[w] = dist[u] + 1; q.append(w)
DIST = [dist[v] for v in range(n)]
s3 = 1 / math.sqrt(3)
CORN = [(s3, s3, s3), (s3, -s3, -s3), (-s3, s3, -s3), (-s3, -s3, s3)]
def tsign(a, b, c):
    A, B, C = CORN[a], CORN[b], CORN[c]
    u = [B[k] - A[k] for k in range(3)]; w = [C[k] - A[k] for k in range(3)]
    nr = [u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0]]
    return 1 if sum(nr[k] * (A[k] + B[k] + C[k]) for k in range(3)) > 0 else -1
TS = {t: tsign(*t) for t in itertools.permutations(range(4), 3)}
FACES_AT = [[f for f in F if v in f] for v in range(n)]
def charges(col):
    """col: list, -1 = absent. Faces with an absent or repeated colour are skipped (cannot happen for proper colourings)."""
    q = [0] * n
    for f in F:
        t = tuple(col[v] for v in f)
        if -1 in t: continue
        s = TS[t]
        for v in f: q[v] += s
    return q
def degree(col, m=0):
    return sum(TS[tuple(col[v] for v in f)] for f in F if m not in [col[v] for v in f] and -1 not in [col[v] for v in f])

S = Space(adj, hole=HOLE, link=LINK)
order = S.order; N = S.N
G_moves = None
def build():
    global G_moves
    S.build_graph(); S.dist_to_filled()
build()
dist_f = S.dist
print('states', N and len(S.states), 'filled', sum(1 for k in range(len(S.states)) if S.filled(k)), file=sys.stderr)

def lab_of(canon_state, lab):
    """permutation canonical colour -> labelled colour"""
    pi = {}
    for c, l in zip(canon_state, lab): pi[c] = l
    return pi
def fill_path(lab):
    """lab: list over S.order of labelled colours. Returns list of steps; each: dict(pair, K, lab_after)."""
    s = S.canon(lab); k = S.index[s]; steps = []
    while dist_f[k] > 0:
        pi = lab_of(S.states[k], lab); best = None
        for t, p, q_, K in S.moves(k):
            if t != k and dist_f[t] == dist_f[k] - 1:
                best = (t, p, q_, K); break
        t, p, q_, K = best
        lp, lq = pi[p], pi[q_]
        new = list(lab)
        for i in range(N):
            if K >> i & 1: new[i] = lq if lab[i] == lp else lp
        steps.append({'pair': sorted((lp, lq)), 'K': S.mask_vertices(K), 'lab': new})
        lab = new; k = t
        assert S.canon(lab) == S.states[k]
    return steps, lab
def to_full(lab, hole_col=-1):
    c = [-1] * n
    for u, x in zip(order, lab): c[u] = x
    c[HOLE] = hole_col
    return c

def run_state(col_dict_or_list):
    c0 = col_dict_or_list
    lab = [c0[u] for u in order]
    steps, lab_end = fill_path(lab)
    cols = [to_full(lab)] + [to_full(s['lab']) for s in steps]
    Q = [charges(c) for c in cols]
    end = cols[-1][:]
    lc = {end[w] for w in LINK}; assert len(lc) <= 3
    miss = [k for k in range(4) if k not in lc][0]
    capped = end[:]; capped[HOLE] = miss
    Qc = charges(capped)
    assert Qc[HOLE] in (3, -3), Qc[HOLE]
    out = {'k': len(steps), 'col': cols, 'q': Q, 'pairs': [s['pair'] for s in steps], 'chain': [s['K'] for s in steps],
           'changed': [[v for v in range(n) if Q[i][v] != Q[i+1][v]] for i in range(len(steps))],
           'cap': {'colour': miss, 'col': capped, 'q': Qc, 'deg': degree(capped)}}
    assert sum(Qc) == 12 * out['cap']['deg'], (sum(Qc), out['cap']['deg'])
    out['changedDist'] = [[DIST[v] for v in ch] for ch in out['changed']]
    return out

# ---------------- the blocked state and the 20 cycle states
cyc = []
for cs in J['cycle_canonical_states']:
    c0 = {int(k): v for k, v in cs['state'].items()}
    cyc.append(run_state(c0))
def pack(r):
    return {'k': r['k'], 'col': r['col'], 'q': r['q'], 'pairs': r['pairs'], 'chain': r['chain'], 'changed': r['changed'],
            'capCol': r['cap']['col'], 'capQ': r['cap']['q'], 'capDeg': r['cap']['deg'], 'capColour': r['cap']['colour']}

# ---------------- statistics
def hist(vals): return dict(sorted(collections.Counter(vals).items()))
def stats(rs, label):
    per_step = collections.defaultdict(list); last = []; allmax = []
    for r in rs:
        for i, dd in enumerate(r['changedDist']):
            per_step[i].append(dd)
    allhist = hist([d for r in rs for dd in r['changedDist'] for d in dd])
    maxd = hist([max(dd) if dd else -1 for r in rs for dd in r['changedDist']])
    lasthist = hist([d for r in rs for d in r['changedDist'][-1]]) if rs else {}
    lastmax = hist([max(r['changedDist'][-1]) if r['changedDist'][-1] else -1 for r in rs])
    far_last = sum(1 for r in rs if r['changedDist'][-1] and max(r['changedDist'][-1]) >= 3)
    nchg = hist([len(ch) for r in rs for ch in r['changed']])
    ring = hist(DIST[1:] if False else [DIST[v] for v in range(n) if v != HOLE])
    steps_tot = sum(r['k'] for r in rs); last_tot = len(rs)
    frac_all = {d: round(c / (ring[d] * steps_tot), 3) for d, c in allhist.items()}
    frac_last = {d: round(c / (ring[d] * last_tot), 3) for d, c in lasthist.items()}
    first_hist = hist([d for r in rs for d in r['changedDist'][0]])
    absdq = collections.defaultdict(int)
    dsum = []
    for r in rs:
        for i in range(r['k']):
            for v in range(n):
                dq = r['q'][i + 1][v] - r['q'][i][v]
                if dq: absdq[DIST[v]] += abs(dq)
            dsum.append(sum(r['q'][i + 1]) - sum(r['q'][i]))
    mean_abs = {d: round(absdq[d] / (ring[d] * steps_tot), 3) for d in sorted(absdq)}
    return {'label': label, 'n': len(rs), 'steps': hist([r['k'] for r in rs]), 'dist_hist_all_changes': allhist, 'maxdist_per_step': maxd,
            'last_step_dist_hist': lasthist, 'last_step_maxdist': lastmax, 'last_step_with_far_change(>=3)': far_last,
            'n_changed_per_step': nchg, 'vertices_at_distance': ring, 'frac_of_ring_changed_per_step': frac_all,
            'frac_of_ring_changed_last_step': frac_last, 'first_step_dist_hist': first_hist, 'mean_abs_dq_per_vertex_per_step_by_dist': mean_abs,
            'delta_total_charge_per_step': hist(dsum)}
cycle_stats = stats(cyc, '20 cycle states')
if '--stats' in sys.argv: print(json.dumps(cycle_stats, indent=1))
# link-end signature for the cycle states (before the fill) and net charge on link + ring 2
def sig(col, q):
    lc = [col[x] for x in LINK]
    for j in range(5):
        if lc[j] == lc[(j + 2) % 5]: break
    m, a, b = (LINK[(j + 1) % 5], LINK[(j + 3) % 5], LINK[(j + 4) % 5])
    eps = TS[(col[m], col[a], col[b])]   # oriented link triangle (global sign of the labelling)
    near = [v for v in range(n) if 1 <= DIST[v] <= 2]
    return {'eps': eps, 'qa': q[a] * eps, 'qb': q[b] * eps, 'qm': q[m] * eps, 'net12': sum(q[v] for v in near) * eps,
            'netlink': sum(q[v] for v in LINK) * eps, 'qx': (q[LINK[j]] + q[LINK[(j + 2) % 5]]) * eps}
if '--stats' in sys.argv:
    csig = [sig(r['col'][0], r['q'][0]) for r in cyc]
    cycle_sig = {'qa_qb': hist([str((x['qa'], x['qb'])) for x in csig]), 'has_minus2_at_a_lock_end': sum(1 for x in csig if -2 in (x['qa'], x['qb'])),
                 'same_sign_both_ends': sum(1 for x in csig if x['qa'] * x['qb'] > 0), 'net12': hist([x['net12'] for x in csig])}
    print('cycle signature', cycle_sig)
    # all states of the hole: DL / unfilled non-DL / filled
    def comp(col, start, p, q_):
        seen = {start}; st = [start]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w != HOLE and w not in seen and col[w] in (p, q_): seen.add(w); st.append(w)
        return seen
    def classify(col):
        lc = [col[x] for x in LINK]
        if len(set(lc)) <= 3: return 'filled'
        for j in range(5):
            if lc[j] == lc[(j + 2) % 5]: break
        m, a, b = LINK[(j + 1) % 5], LINK[(j + 3) % 5], LINK[(j + 4) % 5]
        if a not in comp(col, m, col[m], col[a]): return 'nonDL'
        if b not in comp(col, m, col[m], col[b]): return 'nonDL'
        return 'DL'
    cls = collections.Counter(); sigs = collections.defaultdict(list); dl_runs = []
    for k, s in enumerate(S.states):
        col = to_full(s); c = classify(col); cls[c] += 1
        if c == 'filled': continue
        sigs[c].append(sig(col, charges(col)))
        if c == 'DL': dl_runs.append(run_state(dict(zip(order, s))))
    print('classes', dict(cls))
    dl_stats = stats(dl_runs, 'all DL states')
    print(json.dumps(dl_stats, indent=1))
    sg = {}
    for c, L in sigs.items():
        sg[c] = {'n': len(L), 'net12': hist([x['net12'] for x in L]), 'qa_qb_sign': hist([(x['qa'] > 0) - (x['qa'] < 0), (x['qb'] > 0) - (x['qb'] < 0)].__repr__() for x in L)}
        sg[c]['qa_qb_sign'] = hist([str(((x['qa'] > 0) - (x['qa'] < 0), (x['qb'] > 0) - (x['qb'] < 0))) for x in L])
        sg[c]['qa'] = hist([x['qa'] for x in L]); sg[c]['qb'] = hist([x['qb'] for x in L]); sg[c]['qm'] = hist([x['qm'] for x in L])
        sg[c]['netlink'] = hist([x['netlink'] for x in L])
        sg[c]['qx'] = hist([x['qx'] for x in L])
        sg[c]['qa+qb'] = hist([x['qa'] + x['qb'] for x in L])
        sg[c]['has_minus2_at_a_lock_end'] = sum(1 for x in L if -2 in (x['qa'], x['qb']))
        sg[c]['same_sign_both_ends'] = sum(1 for x in L if x['qa'] * x['qb'] > 0)
        sg[c]['mean_net12'] = round(sum(x['net12'] for x in L) / len(L), 3)
        sg[c]['mean_netlink'] = round(sum(x['netlink'] for x in L) / len(L), 3)
    print(json.dumps(sg, indent=1))
    json.dump({'cycle': cycle_stats, 'cycle_signature': cycle_sig, 'dl': dl_stats, 'signature': sg, 'class_counts': dict(cls)}, open('docs/wrap/charge_stats.json', 'w'), indent=1)
    sys.exit()

cs0 = cyc[0]
assert D['blocked'] == cs0['col'][0]
D['charge'] = {'dist': DIST, 'states': [pack(r) for r in cyc], 'hole_cap_q': [r['cap']['q'][HOLE] for r in cyc]}
try: D['charge']['stats'] = json.load(open('docs/wrap/charge_stats.json'))
except FileNotFoundError: pass
json.dump(D, open('docs/wrap/data.json', 'w'))
t = open('docs/wrap/template.html').read()
open('docs/wrap/index.html', 'w').write(t.replace('__DATA__', open('docs/wrap/data.json').read()))
print('wrote data.json + index.html;', 'steps per cycle state', [r['k'] for r in cyc], 'cap charge at hole', [r['cap']['q'][HOLE] for r in cyc])
