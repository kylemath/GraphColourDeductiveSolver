import json, re, sys
from collections import deque
J = json.load(open(sys.argv[1])); faces = J['faces']; P = sys.argv[2]
N = 1 + max(max(f) for f in faces)
adj = [set() for _ in range(N)]
for f in faces:
    for i in range(3): a, b = f[i], f[(i+1) % 3]; adj[a].add(b); adj[b].add(a)
par = list(range(N)); rk = [0]*N; seen = {0}; q = deque([0])
while q:
    u = q.popleft()
    for v in sorted(adj[u]):
        if v not in seen: seen.add(v); par[v] = u; rk[v] = rk[u] + 1; q.append(v)
vec = lambda xs: '![' + ', '.join(map(str, xs)) + ']'
occs = {'C2122M': ([2, 10, 13, 21, 14, 5, 1], [3, 12, 4, 0]), 'C2122P': ([13, 10, 2, 1, 5, 14, 21], [3, 0, 4, 12]),
        'DiamondM': ([2, 1, 8, 17, 20, 10], [6, 7, 19, 11])}
o = []; w = o.append
w('''module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Tri22Map
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FCycle22
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameAppears

/-!
# Sanity: concrete 2.122 and diamond occurrences in the order-22 F-cycle map

`Tri22.sphericalMap` is the F-cycle triangulation (tri22.txt index 417) as a genuine
`SphericalMap`, with `Fills` proved by its linear certificate.
* It lies in the frame class apart from the exclusions: it is connected and triangulated, has
  minimum degree five, and has no separating triangle.
* RSST 2.122 occurs in it, in both orientations (`occ_C2122M`, `occ_C2122P`). So the 2.122
  exclusion in `RStarFrame` is not vacuous. The diamond occurs too.
* `G_eq`: the F-cycle graph `FCycle22.G` is this map's graph. So the F-cycle facts in `FCycle22`
  (radii, silent moves) hold on the spherical map.
-/

@[expose] public section
namespace SimpleGraph.Tri22
open SphericalMap VacancyIcosahedral

theorem nx_t {u v w : Fin 22} (h : graph.Adj u v) (e : nextTable u v = w) :
    sphericalMap.Nx u v w := ⟨h, e⟩

theorem G_eq : FCycle22.G = sphericalMap.graph := by
  ext u v
  exact (by decide : ∀ u v : Fin 22, FCycle22.G.Adj u v ↔ graph.Adj u v) u v

theorem connected : sphericalMap.graph.Connected := by
  have r : ∀ v, True → graph.Reachable 0 v :=
    reachable_of_parent (G := graph) 0 PAR RK (fun _ => True)
      (fun v _ hv => ⟨trivial, (by decide : ∀ v : Fin 22, v ≠ 0 →
        RK (PAR v) < RK v ∧ graph.Adj (PAR v) v) v hv⟩)
  exact Connected.mk (fun u v => (r u trivial).symm.trans (r v trivial))

theorem noSep : NoSep sphericalMap := by
  have h : ∀ x y : Fin 22, graph.Adj x y → ∀ z, graph.Adj y z → graph.Adj z x →
      nextTable y x = z ∨ nextTable x y = z := by decide
  intro x y z hxy hyz hzx
  rcases h x y hxy z hyz hzx with e | e
  · exact Or.inl (nx_t hxy.symm e)
  · exact Or.inr (nx_t hxy e)

theorem min_degree (x : Fin 22) : 5 ≤ sphericalMap.graph.degree x := by
  rw [sphericalMap_degree]; revert x; decide
'''.replace('PAR', vec(par)).replace('RK', vec(rk)))
for ns, (ring, it) in occs.items():
    occ = open(P + ns + 'Occ.lean').read().split('structure Occ')[1].split('\ntheorem')[0]
    fields = re.findall(r'^\s+(r\d+_\d+) : Nx T', occ, re.M)
    w(f'theorem occ_{ns} : {ns}.Occ sphericalMap {vec(ring)} {vec(it)} where')
    w('  ring_inj := by decide')
    w('  int_inj := by decide')
    w('  disj := by decide')
    w('  deg := fun a => by rw [sphericalMap_degree]; revert a; decide')
    for f in fields: w(f'  {f} := nx_t (by decide) rfl')
    w('')
w('''/-- **The 2.122 exclusion is not vacuous**: `Tri22` is not `Occ`-free for 2.122. -/
theorem not_conf2122Free : ¬ Conf2122Free sphericalMap := fun h => h.1 ⟨_, _, occ_C2122M⟩

theorem not_diamondFree : ¬ DiamondFree sphericalMap := fun h => h.1 ⟨_, _, occ_DiamondM⟩

end SimpleGraph.Tri22''')
print('\n'.join(o))
