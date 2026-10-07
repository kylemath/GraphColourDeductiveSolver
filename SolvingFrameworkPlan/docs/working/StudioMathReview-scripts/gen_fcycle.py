"""Lean module for an F-cycle replay (from fcycle_check.py output).
Usage: python3 -I gen_fcycle.py <replay.json> <Namespace> <label>"""
import json, sys
from collections import deque
D = json.load(open(sys.argv[1])); NS = sys.argv[2]; label = sys.argv[3]
n, hole, adj = D['n'], D['hole'], D['adj']
fix = lambda c: [0 if x < 0 else x for x in c]
vec = lambda xs: '![' + ', '.join(map(str, xs)) + ']'
out = []; w = out.append
def step(name, src, dst, st, c):
    a, b, s0, S = st['a'], st['b'], st['s'], st['S']
    par = list(range(n)); rk = [0]*n; seen = {s0}; q = deque([s0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v != hole and v not in seen and c[v] in (a, b): seen.add(v); par[v] = u; rk[v] = rk[u]+1; q.append(v)
    assert sorted(seen) == S
    Sl = '{' + ', '.join(map(str, S)) + '}'
    w(f'theorem {name} : KempeStep G {hole} {src} {dst} :=')
    w(f'  ⟨{a}, {b}, ↑({Sl} : Finset (Fin {n})), by decide,')
    w(f'    whole_of_cert {s0} _ (by decide) (by decide) (by decide) {vec(par)} {vec(rk)} (by decide),')
    w(f'    swap_eq _ _ _ _ _ (by decide)⟩\n')
def fill(prefix, c0, steps, final):
    """Defines prefix_0 .. prefix_k and proves PureFill G hole prefix_0 k."""
    cols = [fix(s['c']) for s in steps] + [fix(final)]
    for i, c in enumerate(cols): w(f'def {prefix}_{i} : Fin {n} → Fin 4 := {vec(c)}')
    for i, s in enumerate(steps): step(f'{prefix}_step{i+1}', f'{prefix}_{i}', f'{prefix}_{i+1}', s, cols[i])
    k = len(steps); last = cols[-1]
    miss = [x for x in range(4) if all(last[v] != x for v in adj[hole])][0]
    p = f'(.nil {prefix}_{k})'
    for i in range(k, 0, -1): p = f'(.cons {prefix}_step{i} {p})'
    w(f'theorem {prefix}_fill : PureFill G {hole} {prefix}_0 {k} :=')
    w(f'  ⟨{k}, le_rfl, {prefix}_{k}, {p},')
    w(f'    ⟨{miss}, fun v hv => (by decide : ∀ v : Fin {n}, G.Adj {hole} v → {prefix}_{k} v ≠ {miss}) v hv⟩⟩\n')
w(f'namespace {NS}\n')
w(f'/-- {label}: neighbour lists of the {n}-vertex triangulation. -/')
w(f'def nbrs : Fin {n} → List (Fin {n}) := ' + '![' + ', '.join('[' + ', '.join(map(str, a)) + ']' for a in adj) + ']\n')
w(f'def G : SimpleGraph (Fin {n}) where')
w('  Adj u v := v ∈ nbrs u')
w(f'  symm := by refine ⟨?_⟩; intro u v h; exact (by decide : ∀ u v : Fin {n}, v ∈ nbrs u → u ∈ nbrs v) u v h')
w(f'  loopless := by refine ⟨?_⟩; intro v h; exact (by decide : ∀ v : Fin {n}, v ∉ nbrs v) v h\n')
w('instance : DecidableRel G.Adj := fun u v => inferInstanceAs (Decidable (v ∈ nbrs u))\n')
for i, st in enumerate(D['states']):
    r = st['radius']; P = f's{i}'
    w(f'/-! ### State {i} (radius {r}) -/\n')
    assert st['path'][0]['c'] == st['c'] and len(st['path']) == r
    fill(P, st['c'], st['path'], st['final'])
    w(f'theorem {P}_proper : ProperOff G {hole} {P}_0 := fun u v e hu hv =>')
    w(f'  (by decide : ∀ u v : Fin {n}, G.Adj u v → u ≠ {hole} → v ≠ {hole} → {P}_0 u ≠ {P}_0 v) u v e hu hv\n')
    w(f'theorem {P}_unfilled : ¬ Target G {hole} {P}_0 := by')
    w('  rintro ⟨x, hx⟩')
    w(f'  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj {hole} v ∧ {P}_0 v = x) x')
    w('  exact hx hv e\n')
    for j, (m, sp) in enumerate(zip(st['silent'], st['silent_paths'])):
        Q = f'{P}_m{j}'
        assert len(sp['path']) == r - 1
        if sp['path']:
            fill(Q, m['next'], sp['path'], sp['final'])
        else:
            fill(Q, m['next'], [], m['next'])
        step(f'{Q}_move', f'{P}_0', f'{Q}_0', {'a': m['pair'][0], 'b': m['pair'][1], 's': m['s'], 'S': m['S']}, fix(st['c']))
        w(f'/-- Silent move {j} of state {i}: pair {tuple(m["pair"])}, component of size {m["size"]}, no link vertex. -/')
        w(f'theorem {Q}_silent : KempeStep G {hole} {P}_0 {Q}_0 ∧ (∀ v, G.Adj {hole} v → {Q}_0 v = {P}_0 v) ∧')
        w(f'    PureFill G {hole} {Q}_0 {r - 1} :=')
        w(f'  ⟨{Q}_move, fun v hv => (by decide : ∀ v : Fin {n}, G.Adj {hole} v → {Q}_0 v = {P}_0 v) v hv, {Q}_fill⟩\n')
w(f'end {NS}')
print('\n'.join(out))
