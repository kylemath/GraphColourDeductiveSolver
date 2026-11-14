import sys, json, random, math, collections as C, statistics as st
sys.path.insert(0, 'code')
from parts import parse
from mir import mirror
sc, P = parse('data/synth_rules_588.txt')
T = 2
GEN = (5, 9, 5, 9, ())
def canon(p, slots=None):
    s = slots if slots is not None else p['slots']
    q = dict(p, slots=s)
    return min(s, mirror(q, T, 1, 'with_spoke'))
def classes(parts):
    seen = {}
    for p in parts:
        k = (p['pre'], p['hub'], p['w'], canon(p))
        seen.setdefault(k, []).append(p)
    return seen
class UF:
    def __init__(s, n): s.p = list(range(n))
    def f(s, x):
        while s.p[x] != x: s.p[x] = s.p[s.p[x]]; x = s.p[x]
        return x
    def u(s, a, b): s.p[s.f(a)] = s.f(b)
def analyse(parts, label):
    cl = classes(parts); keys = list(cl); n = len(keys)
    uf = UF(n); e = C.Counter()
    # one-slot edits within (template, hub, weight), compared mod mirror
    by = C.defaultdict(list)
    for i, k in enumerate(keys): by[(k[0], k[1], k[2])].append(i)
    variants = {}
    for i, k in enumerate(keys):
        s = k[3]; q = dict(hub=k[1], slots=s)
        variants[i] = [s, mirror(q, T, 1, 'with_spoke')]
    for g, idx in by.items():
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                i, j = idx[a], idx[b]
                sj = keys[j][3]
                dmin = min(sum(1 for x, y in zip(si, sj) if x != y) for si in variants[i])
                if dmin == 1: e['slot1'] += 1; uf.u(i, j)
    # weight edit: same template + slots, other weight
    byS = C.defaultdict(list)
    for i, k in enumerate(keys): byS[(k[0], k[1], k[3])].append(i)
    for g, idx in byS.items():
        for a in idx[1:]: e['weight'] += 1; uf.u(idx[0], a)
    # hub lift: drop one generic non-target slot -> class of hub-1 (same template, weight)
    look = {(k[0], k[1], k[2], k[3]): i for i, k in enumerate(keys)}
    for i, k in enumerate(keys):
        for s in variants[i]:
            for r in range(len(s)):
                if r == T or s[r] != GEN: continue
                s2 = s[:r] + s[r + 1:]
                q = dict(hub=k[1] - 1, slots=s2)
                c2 = min(s2, mirror(q, T if r > T else T - 1, 1, 'with_spoke')) if True else s2
                for cand in (s2, c2):
                    j = look.get((k[0], k[1] - 1, k[2], cand))
                    if j is not None: e['lift'] += 1; uf.u(i, j); break
    # retarget: same hub, slots equal up to rotation (and mirror): one local picture, two targets
    rot = C.defaultdict(list)
    for i, k in enumerate(keys):
        cands = []
        for s in variants[i]:
            cands += [s[r:] + s[:r] for r in range(len(s))]
        rot[(k[1], min(cands))].append(i)
    for g, idx in rot.items():
        for a in idx[1:]:
            e['retarget'] += 1; uf.u(idx[0], a)
            if keys[a][2] == -keys[idx[0]][2]: e['retarget_opposite_weight'] += 1
    comp = C.Counter(uf.f(i) for i in range(n))
    sizes = sorted(comp.values(), reverse=True)
    vocab = C.Counter(s for k in keys for s in k[3])
    return dict(label=label, parts=len(parts), mirror_classes=n,
                selfsym=sum(1 for p in parts if mirror(p, T, 1, 'with_spoke') == p['slots']),
                coarse_templates=len({(k[0], k[1], k[2]) for k in keys}),
                edges=dict(e), schemas=len(sizes), singletons=sum(1 for x in sizes if x == 1),
                largest=sizes[:8], slot_vocab=len(vocab))
out = {'real': {}, 'null': {}}
groups = {'all604': P, 'rsst71': [p for p in P if p['pre'] == 'drule'],
          'SP493': [p for p in P if p['pre'] == 'SP_'], 'ST40': [p for p in P if p['pre'] in ('STm_', 'STp_')]}
for g, ps in groups.items(): out['real'][g] = analyse(ps, g)
# null: keep template, hub, weight and target slot; redraw every other slot from
# the empirical slot distribution at that position for that (template, hub); then mirror-close
rng = random.Random(3)
for g, ps in groups.items():
    if g == 'ST40': pass
    reps = []
    base = [p for p in ps if p['tag'] <= p['tag']]
    pos = C.defaultdict(list)
    for p in ps:
        for r, s in enumerate(p['slots']): pos[(p['pre'], p['hub'], r)].append(s)
    for rep in range(20):
        Q = []
        seenc = set()
        for p in ps:
            k = (p['pre'], p['hub'], p['w'], canon(p))
            if k in seenc: continue   # one per mirror class
            seenc.add(k)
            s = tuple(p['slots'][r] if r == T else rng.choice(pos[(p['pre'], p['hub'], r)]) for r in range(p['hub']))
            q = dict(p, slots=s); Q.append(q)
            Q.append(dict(p, slots=mirror(q, T, 1, 'with_spoke')))
        reps.append(analyse(Q, g))
    out['null'][g] = dict(mirror_classes=st.mean(r['mirror_classes'] for r in reps),
                          schemas_mean=st.mean(r['schemas'] for r in reps), schemas_sd=round(st.pstdev(r['schemas'] for r in reps), 1),
                          singletons_mean=st.mean(r['singletons'] for r in reps),
                          slot1_mean=st.mean(r['edges'].get('slot1', 0) for r in reps),
                          lift_mean=st.mean(r['edges'].get('lift', 0) for r in reps),
                          largest_mean=st.mean(r['largest'][0] for r in reps))
json.dump(out, open('res4.json', 'w'), indent=1)
for g in groups: print(g, out['real'][g]); print('   null', out['null'][g])
