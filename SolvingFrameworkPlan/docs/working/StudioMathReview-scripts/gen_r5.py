"""Generate a Lean check that a radius-5 certificate state fills within five pure Kempe swaps.
Usage: python3 -I gen_r5.py <bfs-output.json> <Namespace> <certificate id>   (prints a Lean section)"""
import json, sys
from collections import deque
D = json.load(open(sys.argv[1])); NS = sys.argv[2]; gid = sys.argv[3]
n, hole, adj = D['n'], D['hole'], D['adj']
fix = lambda c: [0 if x < 0 else x for x in c]
cols = [fix(s['c']) for s in D['steps']] + [fix(D['final'])]
def vec(xs): return '![' + ', '.join(str(x) for x in xs) + ']'
out = []
w = out.append
w(f'namespace {NS}\n')
w(f'/-- Certificate `{gid}`: neighbour lists of the {n}-vertex triangulation. -/')
w(f'def nbrs : Fin {n} → List (Fin {n}) := ' + '![' + ', '.join('[' + ', '.join(map(str, a)) + ']' for a in adj) + ']\n')
w(f'def G : SimpleGraph (Fin {n}) where')
w('  Adj u v := v ∈ nbrs u')
w(f'  symm := by refine ⟨?_⟩; intro u v h; exact (by decide : ∀ u v : Fin {n}, v ∈ nbrs u → u ∈ nbrs v) u v h')
w(f'  loopless := by refine ⟨?_⟩; intro v h; exact (by decide : ∀ v : Fin {n}, v ∉ nbrs v) v h\n')
w('instance : DecidableRel G.Adj := fun u v => inferInstanceAs (Decidable (v ∈ nbrs u))\n')
for i, c in enumerate(cols):
    w(f'def c{i} : Fin {n} → Fin 4 := {vec(c)}')
w('')
for i, s in enumerate(D['steps']):
    a, b, s0, S = s['a'], s['b'], s['s'], s['S']; c = cols[i]
    par = list(range(n)); rk = [0]*n; seen = {s0}; q = deque([s0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v != hole and v not in seen and c[v] in (a, b): seen.add(v); par[v] = u; rk[v] = rk[u]+1; q.append(v)
    assert sorted(seen) == S
    Sl = '{' + ', '.join(map(str, S)) + '}'
    w(f'theorem step{i+1} : KempeStep G {hole} c{i} c{i+1} :=')
    w(f'  ⟨{a}, {b}, ↑({Sl} : Finset (Fin {n})), by decide,')
    w(f'    whole_of_cert {s0} _ (by decide) (by decide) (by decide) {vec(par)} {vec(rk)} (by decide),')
    w(f'    swap_eq _ _ _ _ _ (by decide)⟩\n')
k = len(D['steps']); last = cols[-1]
miss = [x for x in range(4) if all(last[v] != x for v in adj[hole])][0]
w(f'theorem proper : ProperOff G {hole} c0 := fun u v e hu hv =>')
w(f'  (by decide : ∀ u v : Fin {n}, G.Adj u v → u ≠ {hole} → v ≠ {hole} → c0 u ≠ c0 v) u v e hu hv\n')
w(f'theorem unfilled : ¬ Target G {hole} c0 := by')
w('  rintro ⟨x, hx⟩')
w(f'  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj {hole} v ∧ c0 v = x) x')
w('  exact hx hv e\n')
w(f'/-- **The certificate state fills within {k} pure Kempe swaps** (the formal `PureFill`). -/')
w(f'theorem pureFill : PureFill G {hole} c0 {k} :=')
path = '(.nil c%d)' % k
for i in range(k, 0, -1): path = f'(.cons step{i} {path})'
w(f'  ⟨{k}, le_rfl, c{k}, {path},')
w(f'    ⟨{miss}, fun v hv => (by decide : ∀ v : Fin {n}, G.Adj {hole} v → c{k} v ≠ {miss}) v hv⟩⟩\n')
w(f'end {NS}\n')
print('\n'.join(out))
