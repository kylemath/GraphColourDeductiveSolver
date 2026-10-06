#!/usr/bin/env python3
"""Generate `Conf2122Witness.lean`: a concrete spherical triangulation, entered by its oriented
face list, with explicit `C2122M.Occ` and `C2122P.Occ` labellings (F3 of the 16:18 audit message).

The spherical map is built exactly as the library icosahedron (`PlaneMap/Icosahedron.lean`):
finite tables (edges, rotation, face labels) checked by the kernel, and a linear filling
certificate (face potentials along a dual spanning tree plus vertex-incidence combinations).

Usage: python3 -I gen_witness2122.py <faces.json> <graph-id> > Conf2122Witness.lean
The occurrence search is the one of `ico_occ.py`, read from the generated `…Occ.lean` files.
"""
import json, re, sys
from collections import deque

OCCDIR = sys.argv[3] if len(sys.argv) > 3 else \
    'SolvingFrameworkPlan/docs/working/StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/'

faces = json.load(open(sys.argv[1]))['faces']
gid = sys.argv[2]
n = 1 + max(max(f) for f in faces)
F = len(faces)

# rotation: faceNext (u,v) = (v, next v u); oriented face [a,b,c] gives next[b][a] = c etc.
nxt = {}
for a, b, c in faces:
    for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
        assert (y, x) not in nxt
        nxt[(y, x)] = z
prv = {(u, w): v for (u, v), w in nxt.items()}
adj = set(nxt)
assert all((v, u) in adj for (u, v) in adj)
nbr = {u: sorted(v for (x, v) in adj if x == u) for u in range(n)}
deg = {u: len(nbr[u]) for u in range(n)}
D = max(deg.values())
for u in range(n):  # one rotation cycle per vertex
    v0 = nbr[u][0]; seen = [v0]; v = nxt[(u, v0)]
    while v != v0: seen.append(v); v = nxt[(u, v)]
    assert sorted(seen) == nbr[u]
edges = sorted((u, v) for (u, v) in adj if u < v)
E = len(edges)
assert n - E + F == 2
eidx = {}
for i, (u, v) in enumerate(edges): eidx[(u, v)] = eidx[(v, u)] = i
label = {}
reps = []
for f, (a, b, c) in enumerate(faces):
    label[(a, b)] = label[(b, c)] = label[(c, a)] = f
    reps.append((a, b))

# dual spanning tree (BFS from face 0) and face potentials
pot = [None] * F
pot[0] = [0] * E
fadj = {}
for (u, v) in adj:
    fadj.setdefault(label[(u, v)], []).append((label[(v, u)], eidx[(u, v)]))
q = deque([0])
while q:
    f = q.popleft()
    for g, e in sorted(fadj[f]):
        if pot[g] is None:
            pot[g] = pot[f][:]; pot[g][e] ^= 1; q.append(g)
assert all(p is not None for p in pot)

# incidence combination per edge: S with delta(S) = ind(e) + pot(f1) + pot(f2)
star = [[1 if u in edges[e] else 0 for e in range(E)] for u in range(n)]


def solve(target):
    # Gaussian elimination over GF(2): find s in GF(2)^n with sum s_u star_u = target
    rows = [(star[u][:], 1 << u) for u in range(n)]
    piv = []
    for col in range(E):
        r = next((i for i, (vec, _) in enumerate(rows) if vec[col] and i not in [p for p, _ in piv]), None)
        if r is None: continue
        piv.append((r, col))
        for i in range(len(rows)):
            if i != r and rows[i][0][col]:
                rows[i] = ([x ^ y for x, y in zip(rows[i][0], rows[r][0])], rows[i][1] ^ rows[r][1])
    t = target[:]; comb = 0
    for r, col in piv:
        if t[col]:
            t = [x ^ y for x, y in zip(t, rows[r][0])]; comb ^= rows[r][1]
    assert not any(t), 'not a cut'
    return [(comb >> u) & 1 for u in range(n)]


inc = []
for e, (u, v) in enumerate(edges):
    tgt = [pot[label[(u, v)]][k] ^ pot[label[(v, u)]][k] ^ (1 if k == e else 0) for k in range(E)]
    inc.append(solve(tgt))
# check the certificate identity in Python before emitting
for (u, v) in adj:
    e0 = eidx[(u, v)]
    for e in range(E):
        lhs = (1 if e == e0 else 0) ^ (sum(inc[e0][x] * star[x][e] for x in range(n)) % 2)
        assert lhs == pot[label[(u, v)]][e] ^ pot[label[(v, u)]][e]

# connectivity: BFS parent tree from 0
par = [0] * n; rk = [0] * n; seen = {0}; q = deque([0])
while q:
    u = q.popleft()
    for v in nbr[u]:
        if v not in seen: seen.add(v); par[v] = u; rk[v] = rk[u] + 1; q.append(v)
assert len(seen) == n

# occurrences (the search of ico_occ.py)


def parse(t):
    m = re.match(r'(ring|int) (\d+)', t.strip('() ')); return (m.group(1), int(m.group(2)))


def spec(ns):
    occ = open(OCCDIR + ns + 'Occ.lean').read().split('structure Occ')[1].split('theorem')[0]
    facts = [tuple(parse(x) for x in re.findall(r'\((?:ring|int) \d+\)', l))
             for l in occ.splitlines() if ': Nx T' in l]
    fields = re.findall(r'^\s+(r\d+_\d+) : Nx T', occ, re.M)
    degs = [int(x) for x in re.search(r'deg : .*?!\[([\d, ]+)\]', occ).group(1).split(',')]
    R = 1 + max(i for f in facts for k, i in f if k == 'ring')
    return facts, fields, degs, R


def search(ns):
    facts, fields, degs, R = spec(ns); I = len(degs); out = []
    for (i0, i1) in sorted(adj):
        asg = {('int', 0): i0, ('int', 1): i1}; ch = True
        while ch:
            ch = False
            for (x, y, z) in facts:
                if x in asg and y in asg and z not in asg and (asg[x], asg[y]) in adj:
                    asg[z] = nxt[(asg[x], asg[y])]; ch = True
                if x in asg and z in asg and y not in asg and (asg[x], asg[z]) in adj:
                    asg[y] = prv[(asg[x], asg[z])]; ch = True
        if len(asg) < R + I: continue
        ok = all((asg[x], asg[y]) in adj and nxt[(asg[x], asg[y])] == asg[z] for x, y, z in facts)
        vals = list(asg.values())
        if ok and len(set(vals)) == len(vals) and all(deg[asg[('int', a)]] == degs[a] for a in range(I)):
            out.append(([asg[('ring', t)] for t in range(R)], [asg[('int', a)] for a in range(I)]))
    return out, fields


def vec(xs): return '![' + ', '.join(map(str, xs)) + ']'


def mat(rows): return '![' + ', '.join(vec(r) for r in rows) + ']'


def tbl(fn): return mat([[fn(u, v) for v in range(n)] for u in range(n)])


found = {ns: search(ns) for ns in ['C2122M', 'C2122P', 'DiamondM', 'DiamondP']}
for ns in found: sys.stderr.write('%s: %d labelled occurrences\n' % (ns, len(found[ns][0])))
assert found['C2122M'][0] and found['C2122P'][0]

L = []
A = L.append
A('''module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RStarSanity

/-!
# Sanity check: RSST 2.122 occurs (non-vacuity of `Conf2122Free`)

A concrete spherical triangulation with {n} vertices, {E} edges and {F} faces: `{gid}`, the
order-22 F-cycle graph of Studio intel (faces copied from
`backgroundMaterial/planemap-structural/studiointel/fcycle/fcycle_order22.json`). It is built as the
library icosahedron is: finite tables checked by the kernel and a linear filling certificate (face
potentials along a dual spanning tree, and a vertex-incidence combination per edge).

* `mem_class`: the map lies in the class of `RStarNoSepTri` (connected, triangulated, minimum
  degree five, no separating triangle).
* `occ_C2122M`, `occ_C2122P`: RSST configuration 2.122 occurs in both orientations, for explicit
  labellings. So the occurrence predicates of 2.122 are not vacuous, and `Conf2122Free` excludes a
  map of the class (`not_conf2122Free`).

The tables and labellings are produced by `gen_witness2122.py` (Studio Math scripts); they need not
be trusted, since wrong tables fail one of the finite checks.
-/

@[expose] public section
namespace SimpleGraph.Witness2122
open scoped BigOperators
open SphericalMap
set_option maxRecDepth 8192
'''.format(n=n, E=E, F=F, gid=gid))
A('/-- The %d undirected edges, listed with increasing endpoints. -/' % E)
A('def endpoints : Fin %d → Fin %d × Fin %d := ![%s]' % (E, n, n, ', '.join('(%d, %d)' % e for e in edges)))
A('/-- Adjacency table. -/')
A('def adjT : Fin %d → Fin %d → Bool := %s' % (n, n, tbl(lambda u, v: 'true' if (u, v) in adj else 'false')))
A('''def graph : SimpleGraph (Fin {n}) where
  Adj u v := adjT u v = true
  symm := by
    refine ⟨?_⟩; intro u v h
    exact (by decide +kernel : ∀ u v : Fin {n}, adjT u v = true → adjT v u = true) u v h
  loopless := by
    refine ⟨?_⟩; intro v h
    exact Bool.false_ne_true (((by decide +kernel : ∀ v : Fin {n}, adjT v v = false) v).symm.trans h)

instance : DecidableRel graph.Adj := fun u v => inferInstanceAs (Decidable (adjT u v = true))
'''.format(n=n))
A('/-- Successor and predecessor tables of the rotation. -/')
A('def nextTable : Fin %d → Fin %d → Fin %d := %s' % (n, n, n, tbl(lambda u, v: nxt.get((u, v), 0))))
A('def prevTable : Fin %d → Fin %d → Fin %d := %s' % (n, n, n, tbl(lambda u, v: prv.get((u, v), 0))))
A('/-- Label of the oriented triangular face containing an adjacent pair. -/')
A('def labelTable : Fin %d → Fin %d → Fin %d := %s' % (n, n, F, tbl(lambda u, v: label.get((u, v), 0))))
A('def edgeTable : Fin %d → Fin %d → Fin %d := %s' % (n, n, E, tbl(lambda u, v: eidx.get((u, v), 0))))
A('''theorem next_adj : ∀ u v, graph.Adj u v → graph.Adj u (nextTable u v) := by decide +kernel
theorem prev_adj : ∀ u v, graph.Adj u v → graph.Adj u (prevTable u v) := by decide +kernel
def nextDart (d : graph.Dart) : graph.Dart := ⟨(d.fst, nextTable d.fst d.snd), next_adj _ _ d.adj⟩
def prevDart (d : graph.Dart) : graph.Dart := ⟨(d.fst, prevTable d.fst d.snd), prev_adj _ _ d.adj⟩
def rotation : RotationSystem graph where
  next := {{
    toFun := nextDart
    invFun := prevDart
    left_inv := by
      have h : ∀ u v, graph.Adj u v → prevTable u (nextTable u v) = v := by decide +kernel
      intro d; apply Dart.ext; exact Prod.ext rfl (h _ _ d.adj)
    right_inv := by
      have h : ∀ u v, graph.Adj u v → nextTable u (prevTable u v) = v := by decide +kernel
      intro d; apply Dart.ext; exact Prod.ext rfl (h _ _ d.adj) }}
  next_fst := fun _ => rfl
  cyclic := by
    have h : ∀ u v w, graph.Adj u v → graph.Adj u w →
      ∃ k : Fin {D}, (nextTable u)^[k.val] v = w := by decide +kernel
    intro d e he
    obtain ⟨k,hk⟩ := h d.fst d.snd e.snd d.adj (by simp [he])
    refine ⟨k.val, ?_⟩
    apply Dart.ext
    have hi : ∀ k : ℕ, ((nextDart : graph.Dart → graph.Dart)^[k] d).toProd =
      (d.fst, (nextTable d.fst)^[k] d.snd) := by
      intro k; induction k with
      | zero => rfl
      | succ k ih =>
        rw [Function.iterate_succ_apply']; change (_, nextTable _ _) = _
        rw [ih]; simp only [Function.iterate_succ_apply']
    change ((nextDart : graph.Dart → graph.Dart)^[k.val] d).toProd = e.toProd
    rw [hi]; exact Prod.ext he hk
'''.format(D=D))
A('def repTable : Fin %d → Fin %d × Fin %d := ![%s]' % (F, n, n, ', '.join('(%d, %d)' % r for r in reps)))
A('''def representatives : Fin {F} → graph.Dart := fun f => ⟨repTable f,
  (by decide +kernel : ∀ f : Fin {F}, graph.Adj (repTable f).1 (repTable f).2) f⟩'''.format(F=F))
A('/-- Linear face-potential reconstruction, rooted at face zero. -/')
A('def potentialCoeffs : Fin %d → Fin %d → ZMod 2 := %s' % (F, E, mat(pot)))
A('/-- Incidence combinations certifying each edge reconstruction identity. -/')
A('def incidenceCoeffs : Fin %d → Fin %d → ZMod 2 := %s' % (E, n, mat(inc)))
A('''
theorem label_next (d : graph.Dart) :
    labelTable (rotation.faceNext d).fst (rotation.faceNext d).snd =
      labelTable d.fst d.snd := by
  have h : ∀ u v, graph.Adj u v → labelTable v (nextTable v u) = labelTable u v := by
    decide +kernel
  exact h _ _ d.adj

def faceIndex : rotation.Face → Fin {F}
  | .inl q => Quotient.lift (fun d : graph.Dart => labelTable d.fst d.snd) (by
      intro d e h
      induction h with
      | refl d => rfl
      | step d => exact (label_next d).symm
      | symm h ih => exact ih.symm
      | trans h₁ h₂ ih₁ ih₂ => exact ih₁.trans ih₂) q
  | .inr h => False.elim (@IsEmpty.false graph.Dart h.property (representatives 0))

@[simp] theorem faceIndex_faceOf (d : graph.Dart) :
    faceIndex (rotation.faceOf d) = labelTable d.fst d.snd := rfl

def indexedEdge (e : Fin {E}) : graph.edgeSet :=
  ⟨s((endpoints e).1, (endpoints e).2), by
    rw [mem_edgeSet]
    exact (by decide +kernel : ∀ e : Fin {E}, graph.Adj (endpoints e).1 (endpoints e).2) e⟩

theorem indexedEdge_dart (d : graph.Dart) :
    indexedEdge (edgeTable d.fst d.snd) = RotationSystem.edgeOfDart d := by
  have h : ∀ u v, graph.Adj u v →
      s((endpoints (edgeTable u v)).1, (endpoints (edgeTable u v)).2) = s(u,v) := by
    decide +kernel
  apply Subtype.ext
  exact h _ _ d.adj

theorem indexedEdge_injective : Function.Injective indexedEdge := by
  have h : ∀ i j : Fin {E},
    s((endpoints i).1, (endpoints i).2) = s((endpoints j).1, (endpoints j).2) → i = j := by
    decide +kernel
  intro i j hij
  exact h i j (congrArg Subtype.val hij)

theorem indexedEdge_surjective : Function.Surjective indexedEdge := by
  intro e
  obtain ⟨d, hd⟩ := RotationSystem.edge_of_dart_surjective e
  exact ⟨edgeTable d.fst d.snd, (indexedEdge_dart d).trans hd⟩

noncomputable def edgeEquiv : Fin {E} ≃ graph.edgeSet :=
  Equiv.ofBijective indexedEdge ⟨indexedEdge_injective, indexedEdge_surjective⟩

def faceRepresentative (f : Fin {F}) : rotation.Face := rotation.faceOf (representatives f)

@[simp] theorem faceIndex_representative (f : Fin {F}) :
    faceIndex (faceRepresentative f) = f := by
  have h : ∀ f : Fin {F}, labelTable (representatives f).fst (representatives f).snd = f := by
    decide +kernel
  exact h f

theorem representative_faceOf (d : graph.Dart) :
    faceRepresentative (labelTable d.fst d.snd) = rotation.faceOf d := by
  have h : ∀ u v, graph.Adj u v →
    ∃ k : Fin 3, ((fun p : Fin {n} × Fin {n} => (p.2, nextTable p.2 p.1))^[k.val])
      (representatives (labelTable u v)).toProd = (u,v) := by decide +kernel
  obtain ⟨k,hk⟩ := h d.fst d.snd d.adj
  have hi : ∀ j : ℕ, (rotation.faceNext^[j] (representatives (labelTable d.fst d.snd))).toProd =
    ((fun p : Fin {n} × Fin {n} => (p.2, nextTable p.2 p.1))^[j])
      (representatives (labelTable d.fst d.snd)).toProd := by
    intro j
    induction j with
    | zero => rfl
    | succ j ih =>
      simp only [Function.iterate_succ_apply']
      change (_, nextTable _ _) = _
      change (((rotation.faceNext^[j] (representatives (labelTable d.fst d.snd))).toProd).2,
        nextTable (((rotation.faceNext^[j] (representatives (labelTable d.fst d.snd))).toProd).2)
          (((rotation.faceNext^[j] (representatives (labelTable d.fst d.snd))).toProd).1)) = _
      rw [ih]
  have he : rotation.faceNext^[k.val] (representatives (labelTable d.fst d.snd)) = d := by
    apply Dart.ext
    rw [hi, hk]
  apply congrArg Sum.inl
  apply Quotient.sound
  change rotation.FaceRelation (representatives (labelTable d.fst d.snd)) d
  have hr : ∀ j : ℕ, rotation.FaceRelation (representatives (labelTable d.fst d.snd))
      (rotation.faceNext^[j] (representatives (labelTable d.fst d.snd))) := by
      intro j
      induction j with
      | zero => exact .refl _
      | succ j ih => rw [Function.iterate_succ_apply']; exact ih.trans (.step _)
  simpa [he] using hr k.val

noncomputable def faceEquiv : rotation.Face ≃ Fin {F} where
  toFun := faceIndex
  invFun := faceRepresentative
  left_inv := by
    intro f
    cases f with
    | inl q =>
      induction q using Quotient.inductionOn with
      | h d => exact representative_faceOf d
    | inr h => exact False.elim (@IsEmpty.false graph.Dart h.property (representatives 0))
  right_inv := faceIndex_representative

def incidenceEntry (e : Fin {E}) (v : Fin {n}) : ZMod 2 :=
  if v ∈ (indexedEdge e).val then 1 else 0

theorem incidence_coordinates (φ : graph.edgeSet → ZMod 2) (v : Fin {n}) :
    edgeIncidence graph φ v = ∑ e : Fin {E}, incidenceEntry e v * φ (indexedEdge e) := by
  classical
  let : DecidableRel graph.Adj := Classical.decRel _
  unfold edgeIncidence
  calc
    (∑ e : graph.edgeSet, if v ∈ e.val then φ e else 0) =
        ∑ e : Fin {E}, if v ∈ (edgeEquiv e).val then φ (edgeEquiv e) else 0 :=
      (edgeEquiv.sum_comp (fun e : graph.edgeSet => if v ∈ e.val then φ e else 0)).symm
    _ = _ := by
      congr 1
      funext e
      change (if v ∈ (indexedEdge e).val then φ (indexedEdge e) else 0) = _
      simp only [incidenceEntry, ite_mul, one_mul, zero_mul]

def potential (φ : graph.edgeSet → ZMod 2) (f : Fin {F}) : ZMod 2 :=
  ∑ e : Fin {E}, potentialCoeffs f e * φ (indexedEdge e)

/-- The incidence entries as a table (checked against `incidenceEntry`). -/
def incT : Fin {E} → Fin {n} → ZMod 2 := {incT}

theorem incidenceEntry_eq : ∀ e v, incidenceEntry e v = incT e v := by
  have h : ∀ e : Fin {E}, ∀ v : Fin {n},
      (if v ∈ s((endpoints e).1, (endpoints e).2) then (1 : ZMod 2) else 0) = incT e v := by
    decide +kernel
  intro e v; exact h e v

/-- A finite coefficient identity certifies filling. The incidence combination cancels for every
even edge combination, leaving a face potential. -/
theorem coefficient_certificate : ∀ u v, graph.Adj u v → ∀ e : Fin {E},
    (if edgeTable u v = e then (1 : ZMod 2) else 0) +
      ∑ x : Fin {n}, incidenceCoeffs (edgeTable u v) x * incidenceEntry e x =
      potentialCoeffs (labelTable u v) e + potentialCoeffs (labelTable v u) e := by
  simp only [incidenceEntry_eq]
  decide +kernel

theorem fills : rotation.Fills := by
  intro φ hφ
  refine ⟨fun f => potential φ (faceIndex f), ?_⟩
  intro d
  have hc := coefficient_certificate d.fst d.snd d.adj
  have hs := congrArg (fun c : Fin {E} → ZMod 2 => ∑ e : Fin {E}, c e * φ (indexedEdge e))
    (funext hc)
  simp only [add_mul, Finset.sum_add_distrib,
    Finset.sum_mul] at hs
  have hzero : (∑ e : Fin {E}, ∑ x : Fin {n},
      (incidenceCoeffs (edgeTable d.fst d.snd) x * incidenceEntry e x) *
        φ (indexedEdge e)) = 0 := by
    rw [Finset.sum_comm]
    simp_rw [mul_assoc, ← Finset.mul_sum, ← incidence_coordinates]
    simp [hφ]
  rw [hzero, add_zero] at hs
  simpa [potential, ite_mul, indexedEdge_dart, Dart.symm] using hs

theorem face_length_three (f : rotation.Face) : rotation.faceLength f = 3 := by
  have hp : ∀ u v, graph.Adj u v →
      (fun p : Fin {n} × Fin {n} => (p.2, nextTable p.2 p.1))^[3] (u,v) = (u,v) := by
    decide +kernel
  have hperiod (d : graph.Dart) : rotation.faceNext^[3] d = d := by
    apply Dart.ext
    exact hp _ _ d.adj
  have hfix (d : graph.Dart) : rotation.faceNext d ≠ d := by
    intro he
    exact d.adj.ne (congrArg (fun a : graph.Dart => a.fst) he).symm
  rw [← faceEquiv.left_inv f]
  change rotation.faceLength (rotation.faceOf (representatives (faceIndex f))) = 3
  rw [rotation.face_length_eq_period]
  exact Function.minimalPeriod_eq_prime (hperiod _) (hfix _)

/-- The spherical triangulation `{gid}`. -/
def sphericalMap : SphericalMap {n} where
  graph := graph
  rotation := rotation
  fills := fills

/-- Vertex degrees. -/
def degT : Fin {n} → ℕ := {degT}

theorem degree_eq (v : Fin {n}) : graph.degree v = degT v := by
  have h : ∀ v : Fin {n}, graph.degree v = degT v := by decide +kernel
  exact h v

theorem sphericalMap_degree (v : Fin {n}) : sphericalMap.graph.degree v = degT v := by
  have h := degree_eq v
  rw [← card_neighborSet_eq_degree, ← Nat.card_eq_fintype_card] at h ⊢
  exact h

theorem sphericalMap_triangulated : sphericalMap.Triangulated := by
  intro d
  classical
  have h := face_length_three (sphericalMap.faceOf d)
  unfold RotationSystem.faceLength at h ⊢
  rw [← Nat.card_eq_fintype_card] at h ⊢
  exact h

theorem nx {{u v w : Fin {n}}} (h : graph.Adj u v) (e : nextTable u v = w) :
    sphericalMap.Nx u v w := ⟨h, e⟩

theorem connected : sphericalMap.graph.Connected := by
  have r : ∀ v, True → graph.Reachable 0 v :=
    reachable_of_parent (G := graph) 0 {par} {rk} (fun _ => True)
      (fun v _ hv => ⟨trivial, (by decide +kernel : ∀ v : Fin {n}, v ≠ 0 →
        ({rk} : Fin {n} → ℕ) (({par} : Fin {n} → Fin {n}) v) < ({rk} : Fin {n} → ℕ) v ∧
        graph.Adj (({par} : Fin {n} → Fin {n}) v) v) v hv⟩)
  exact Connected.mk (fun u v => (r u trivial).symm.trans (r v trivial))

theorem noSep : NoSep sphericalMap := by
  have h : ∀ x y : Fin {n}, graph.Adj x y → ∀ z, graph.Adj y z → graph.Adj z x →
      nextTable y x = z ∨ nextTable x y = z := by decide +kernel
  intro x y z hxy hyz hzx
  rcases h x y hxy z hyz hzx with e | e
  · exact Or.inl (nx hxy.symm e)
  · exact Or.inr (nx hxy e)

/-- **The map lies in the class of `RStarNoSepTri`**: connected, triangulated, minimum degree
five, no separating triangle. -/
theorem mem_class : 0 < {n} ∧ sphericalMap.graph.Connected ∧ sphericalMap.Triangulated ∧
    (∀ x, 5 ≤ sphericalMap.graph.degree x) ∧ NoSep sphericalMap :=
  ⟨by norm_num, connected, sphericalMap_triangulated,
    fun x => by rw [sphericalMap_degree]; revert x; decide, noSep⟩
'''.format(n=n, E=E, F=F, gid=gid,
           incT=mat([[1 if u in edges[e] else 0 for u in range(n)] for e in range(E)]),
           degT=vec([deg[u] for u in range(n)]), par=vec(par), rk=vec(rk)))

for ns in ['C2122M', 'C2122P']:
    (ring, it), fields = found[ns][0][0], found[ns][1]
    A('/-- RSST 2.122 occurs in this map (`%s`). -/' % ns)
    A('theorem occ_%s : %s.Occ sphericalMap %s %s where' % (ns, ns, vec(ring), vec(it)))
    A('  ring_inj := by decide')
    A('  int_inj := by decide')
    A('  disj := by decide')
    A('  deg := fun a => by rw [sphericalMap_degree]; revert a; decide')
    for f in fields: A('  %s := nx (by decide) rfl' % f)
    A('')
A('''/-- **`Conf2122Free` excludes this map**, a member of the class of `RStarNoSepTri`. So the
2.122 exclusion in `RStarFrame` is not vacuous. -/
theorem not_conf2122Free : ¬ Conf2122Free sphericalMap := fun h => h.1 ⟨_, _, occ_C2122M⟩

end SimpleGraph.Witness2122''')
print('\n'.join(L))
