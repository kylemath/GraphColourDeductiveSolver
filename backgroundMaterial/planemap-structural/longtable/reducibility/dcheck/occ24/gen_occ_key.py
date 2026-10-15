#!/usr/bin/env python3
"""Job 24 (Studio, exploratory): per-key occurrence module for a 2-ball key (a DCheck18 `Conf` line).
The `Occ`/`configOcc` emitter is `StudioMathReview-scripts/gen_occ.py`'s `gen` (orientation -1), with
the Kempe-certificate generation removed; the rotation comes from the link cycles of the 2-ball.
Usage: gen_occ_key.py KEYFILE LINENO NS OUTDIR"""
import sys

def parse(line):
    f = line.split()
    name, r, m = f[0], int(f[1]), int(f[2])
    ra = [[int(x) for x in s.split(',')] if s != '-' else [] for s in f[3].split(';')]
    ia = [[int(x) for x in s.split(',')] if s != '-' else [] for s in f[4].split(';')]
    return name, r, m, ra, ia

def rotation(r, m, ra, ia):
    """Free-completion rotation (RSST labels: ring t -> t+1, interior a -> r+1+a), consistently oriented."""
    L = lambda a: r + 1 + a
    nb = {}
    for a in range(m):
        nb[L(a)] = set(L(b) for b in ia[a]) | set(t + 1 for t in ra[a])
    for t in range(r):
        nb.setdefault(t + 1, set())
    for a in range(m):
        for t in ra[a]: nb[t + 1].add(L(a))
    for t in range(r):
        nb[t + 1].add((t + 1) % r + 1); nb[(t + 1) % r + 1].add(t + 1)
    rot = {}
    for a in range(m):
        v = L(a); N = nb[v]
        for u in N:
            if len(nb[u] & N) != 2: raise ValueError('link of %d not a cycle at %d' % (v, u))
        start = min(N); cyc = [start]; prev = None; cur = start
        while True:
            nxt = [w for w in nb[cur] & N if w != prev and w not in cyc[1:] ]
            nxt = [w for w in nxt if w != cur]
            if len(cyc) == len(N):
                break
            w = [x for x in nb[cur] & N if x not in cyc][0]
            cyc.append(w); prev, cur = cur, w
        rot[v] = cyc
    # orient by BFS from the hole
    done = {L(0)}; queue = [L(0)]
    while queue:
        v = queue.pop()
        c = rot[v]
        for i, b in enumerate(c):
            if b not in rot or b in done: continue
            a = c[i - 1]
            cb = rot[b]; j = cb.index(v)
            if cb[(j + 1) % len(cb)] != a:
                rot[b] = cb[::-1]
            done.add(b); queue.append(b)
    # check consistency
    for v, c in rot.items():
        for i, b in enumerate(c):
            if b in rot:
                a = c[i - 1]; cb = rot[b]; j = cb.index(v)
                assert cb[(j + 1) % len(cb)] == a, ('inconsistent', v, b)
    return rot

def V(u, r, idx):
    return "(ring %d)" % (u - 1) if u <= r else "(int %d)" % idx[u]


def gen_occ(name, r, rot, ns):
    eps = -1
    labels = sorted(rot)
    idx = {v: i for i, v in enumerate(labels)}
    pos_of = lambda u: u - 1
    lab_of = lambda t: t % r + 1
    posexpr = "t %% %d" % r
    m = len(labels)
    # occurrence facts: (a, k) -> (u, y) with Nx T (int a) u y
    facts = {}
    for a in labels:
        L = rot[a]
        d = len(L)
        for k in range(d):
            if eps == 1:
                facts[(a, k)] = (L[k], L[(k + 1) % d])
            else:
                facts[(a, k)] = (L[(k + 1) % d], L[k])
    # derived ring steps: at vertex R: next(R -> p) = (R -> q), proof term
    steps = {}
    for (a, k), (u, y) in facts.items():
        f = "h.r%d_%d" % (idx[a], k)
        steps.setdefault(y, {})[a] = (u, "(nx_tri htri %s).1" % f)   # Nx y a u
        steps.setdefault(u, {})[y] = (a, "(nx_tri htri %s).2" % f)   # Nx u y a
    lines = []
    A = lines.append
    A("""module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.{ns}Cert
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.OccToRing
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.MinimalFrame

/-!
# Occurrence of {name} (orientation {eps:+d}) gives a ring reduction (generated)

`Occ T ring int` is the audit's rotation-based occurrence: injective ring (`ring k` is RSST ring
vertex `k+1`), injective interior, disjoint, every interior vertex has the free-completion degree,
and the rotation of `T` at every interior vertex is the free-completion rotation, read
{dirword}. Ring chords are allowed.

`configOcc`: on a triangulation, deleting the interior gives a `ConfigOcc` and a strictly smaller
support. `colorable_of_occ`: a triangulation with an occurrence is four-colourable when every
spherical map of smaller support is.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap.{ns}
open VacancySlide VacancyShortFill VacancyIcosahedral VacancyCliqueLift SimpleGraph.SphericalMap

variable {{n : ℕ}}

/-- Ring position `t` to ring vertex. -/
def ρOf (ring : Fin {r} → Fin n) : ℕ → Fin n := fun t => ring ⟨{pe}, by omega⟩
""".format(ns=ns, name=name, eps=eps, dirword="forwards" if eps == 1 else "backwards", r=r, pe=posexpr))
    # Occ structure
    degs = ", ".join(str(len(rot[a])) for a in labels)
    A("/-- The configuration occurs in `T` with ring `ring` and interior `int`. -/")
    A("structure Occ (T : SphericalMap n) (ring : Fin %d → Fin n) (int : Fin %d → Fin n) : Prop where" % (r, m))
    A("  ring_inj : Function.Injective ring")
    A("  int_inj : Function.Injective int")
    A("  disj : ∀ t a, ring t ≠ int a")
    A("  deg : ∀ a, T.graph.degree (int a) = (![%s] : Fin %d → ℕ) a" % (degs, m))
    for a in labels:
        for k in range(len(rot[a])):
            u, y = facts[(a, k)]
            A("  r%d_%d : Nx T (int %d) %s %s" % (idx[a], k, idx[a], V(u, r, idx), V(y, r, idx)))
    A("")
    # theorem configOcc
    A("theorem configOcc {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin %d → Fin n}" % r)
    A("    {int : Fin %d → Fin n} (h : Occ T ring int) :" % m)
    A("    ∃ G : SphericalMap n, ConfigOcc T G %d %d (ρOf ring) int intAdj ringAdj ∧" % (r, m))
    A("      supportSize G < supportSize T := by")
    A("  classical")
    A("  obtain ⟨G, hN, hle, spec⟩ := subgraph_tracked T (sideGraph T.graph {x | ∀ a, x ≠ int a})")
    A("    (fun _ _ e => e.1)")
    A("  have hGadj : ∀ x y, G.Adj x y ↔ T.Adj x y ∧ (∀ a, x ≠ int a) ∧ (∀ a, y ≠ int a) := by")
    A("    intro x y; change G.graph.Adj x y ↔ _; rw [hN]; rfl")
    # fans: for each ring position t, fan at rho(t+1) from rho(t) to rho(t+2)
    fan_blocks = []
    for t in range(r):
        R = lab_of(t + 1)
        start = lab_of(t)
        end = lab_of(t + 2)
        chain = [start]
        terms = []
        cur = start
        while True:
            q, term = steps[R][cur]
            terms.append(term)
            chain.append(q)
            cur = q
            if cur == end:
                break
            assert cur > r, (name, eps, t, chain)
        fan_blocks.append((t, R, chain, terms))
    # step proof
    A("  have hstep : ∀ t, t < %d → ∀ h1 h2, G.rotation.faceNext ⟨(ρOf ring t, ρOf ring (t + 1)), h1⟩ =" % r)
    A("      ⟨(ρOf ring (t + 1), ρOf ring (t + 2)), h2⟩ := by")
    A("    intro t ht h1 h2")
    A("    rw [RotationSystem.face_next_apply]")
    A("    interval_cases t")
    for (t, R, chain, terms) in fan_blocks:
        K = len(chain) - 1
        xs = ", ".join(V(u, r, idx) for u in chain)
        A("    · -- ring position %d: fan at RSST %d: %s" % (t, R, chain))
        A("      let X : ℕ → Fin n := fun j => ([%s] : List (Fin n)).getD j (ring 0)" % xs)
        A("      have hc : ∀ j, j < %d → Nx T %s (X j) (X (j + 1)) := by" % (K, V(R, r, idx)))
        A("        intro j hj; interval_cases j")
        A("        exacts [%s]" % ", ".join(terms))
        A("      have h0 : T.Adj %s (X 0) := nx_adj_left (hc 0 (by norm_num))" % V(R, r, idx))
        A("      have ch := iterate_chain h0 hc")
        A("      have r0 := spec (Dart.symm ⟨(ρOf ring %d, ρOf ring %d), h1⟩)" % (t, t + 1))
        A("      obtain ⟨hK, eK⟩ := ch %d le_rfl" % K)
        A("      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := %d) (by norm_num)" % K)
        A("        (fun j hj1 hj2 => by")
        A("          obtain ⟨_, ej⟩ := ch j (by omega)")
        A("          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj")
        A("            ((⇑T.rotation.next)^[j] ⟨(%s, X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨(%s, X 0), h0⟩).snd" % (V(R, r, idx), V(R, r, idx)))
        A("          rw [ej]")
        A("          interval_cases j")
        for j in range(1, K):
            a = chain[j]
            A("          · exact fun hh => hh.2.2 %d rfl" % idx[a])
        A("        )")
        A("        (by")
        A("          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj")
        A("            ((⇑T.rotation.next)^[%d] ⟨(%s, X 0), h0⟩).fst ((⇑T.rotation.next)^[%d] ⟨(%s, X 0), h0⟩).snd" % (K, V(R, r, idx), K, V(R, r, idx)))
        A("          rw [eK]")
        A("          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)")
        A("      apply liftDart_injective hle")
        A("      rw [e]")
        A("      change (⇑T.rotation.next)^[%d] ⟨(%s, X 0), h0⟩ = _" % (K, V(R, r, idx)))
        A("      rw [eK]; rfl")
    # adjacency
    A("  have hadj : ∀ t, t < %d → G.Adj (ρOf ring t) (ρOf ring (t + 1)) := by" % r)
    A("    intro t ht")
    A("    interval_cases t")
    for (t, R, chain, terms) in fan_blocks:
        A("    · exact (hGadj _ _).2 ⟨(nx_adj_left %s).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩" % terms[0])
    A("  have hinj : ∀ s t, s < %d → t < %d → ρOf ring s = ρOf ring t → s = t := by" % (r, r))
    A("    intro s t hs ht e")
    A("    have := h.ring_inj e")
    A("    simp only [Fin.mk.injEq] at this")
    A("    omega")
    A("  have hper : ∀ t, ρOf ring (t + %d) = ρOf ring t := by" % r)
    A("    intro t; unfold ρOf; congr 2; simp [Nat.add_mod_right]")
    A("  have hring : RingFace G %d (ρOf ring) := RingFace.mk_lt (by norm_num) hper hadj hstep hinj" % r)
    # nbr
    A("  have hnbr : ∀ a w, T.Adj (int a) w →")
    A("      (∃ b, w = int b ∧ intAdj a b = true) ∨ (∃ t, t < %d ∧ w = ρOf ring t ∧ ringAdj a t = true) := by" % r)
    A("    intro a w hw")
    A("    fin_cases a")
    for a in labels:
        L = rot[a]
        d = len(L)
        if eps == 1:
            order = [L[j] for j in range(d)]
            fk = lambda j: (a, j)
        else:
            order = [L[(-j) % d] for j in range(d)]
            fk = lambda j: (a, (-j - 1) % d)
        xs = ", ".join(V(u, r, idx) for u in order)
        A("    · let X : ℕ → Fin n := fun j => ([%s] : List (Fin n)).getD j (ring 0)" % xs)
        A("      have hc : ∀ j, j + 1 < %d → Nx T (int %d) (X j) (X (j + 1)) := by" % (d, idx[a]))
        A("        intro j hj; have hj' : j < %d := by omega" % (d - 1))
        A("        interval_cases j")
        A("        exacts [%s]" % ", ".join("h.r%d_%d" % (idx[a], fk(j)[1]) for j in range(d - 1)))
        A("      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := %d) (by simpa using h.deg %d) (nx_adj_left (hc 0 (by norm_num))) hc w hw" % (d, idx[a]))
        A("      interval_cases j")
        for j, u in enumerate(order):
            if u <= r:
                A("      · exact Or.inr ⟨%d, by norm_num, rfl, by decide⟩" % pos_of(u))
            else:
                A("      · exact Or.inl ⟨%d, rfl, by decide⟩" % idx[u])
    # support
    A("  have hsupp : supportSize G < supportSize T := by")
    A("    apply Finset.card_lt_card")
    A("    refine ⟨fun w hw => ?_, fun hsub => ?_⟩")
    A("    · simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hw ⊢")
    A("      exact lt_of_lt_of_le hw (SimpleGraph.degree_le_of_le hle)")
    A("    · have hmem : int 0 ∈ Finset.univ.filter (fun x => 0 < T.graph.degree x) := by")
    A("        simp only [Finset.mem_filter, Finset.mem_univ, true_and]")
    A("        have := h.deg 0; simp at this; omega")
    A("      have := hsub hmem")
    A("      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at this")
    A("      obtain ⟨u, hu⟩ := G.graph.degree_pos_iff_exists_adj _ |>.mp this")
    A("      exact ((hGadj _ _).1 hu).2.1 0 rfl")
    A("  exact ⟨G, ⟨hring, h.int_inj, fun t a => h.disj _ a, hGadj, hnbr, by norm_num⟩, hsupp⟩")
    A("")
    A("""/-- **Reduction.** A triangulation in which the configuration occurs is four-colourable when every
spherical map of smaller support is. -/
theorem colorable_of_occ {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin %d → Fin n}
    {int : Fin %d → Fin n} (h : Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 := by
  obtain ⟨G, O, hlt⟩ := configOcc htri h
  obtain ⟨cG⟩ := IH n G (by rw [natCard_support_eq, natCard_support_eq]; exact hlt)
  exact colorable O cG (fun x y e _ _ => cG.valid e)

end SimpleGraph.SphericalMap.%s
""" % (r, m, ns))
    return "\n".join(lines)



def gen_key(line, ns):
    name, r, m, ra, ia = parse(line)
    rot = rotation(r, m, ra, ia)
    try:
        occ = gen_occ(name, r, rot, ns)
    except (KeyError, AssertionError):
        rot = {v: c[::-1] for v, c in rot.items()}
        occ = gen_occ(name, r, rot, ns)
    # plain (non-module) Lean file
    occ = occ.replace('module\n\n', '', 1)
    occ = occ.replace('public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.%sCert\n' % ns, '')
    occ = occ.replace('public import', 'import')
    occ = occ.replace('import Mathlib.Combinatorics.SimpleGraph.PlaneMap.MinimalFrame',
        'import Mathlib.Combinatorics.SimpleGraph.PlaneMap.MinimalFrame\nimport DCheckR2D\nimport DCheckTEq')
    occ = occ.replace('@[expose] public section\n', '')
    labels = sorted(rot)
    idx = {v: i for i, v in enumerate(labels)}
    rl = ', '.join('[%s]' % ', '.join(str(t) for t in ra[a]) for a in range(m))
    il = ', '.join('[%s]' % ', '.join(str(b) for b in ia[a]) for a in range(m))
    defs = """
/-- Ring neighbours (ring positions) and interior neighbours of each interior vertex. -/
def ringList : Fin %d → List ℕ := ![%s]
def intList : Fin %d → List (Fin %d) := ![%s]
def ringAdj : Fin %d → ℕ → Bool := fun a t => decide (t ∈ ringList a)
def intAdj : Fin %d → Fin %d → Bool := fun a b => decide (b ∈ intList a)
""" % (m, rl, m, m, il, m, m, m)
    occ = occ.replace('/-- Ring position `t` to ring vertex. -/', defs + '\n/-- Ring position `t` to ring vertex. -/', 1)
    ras = ', '.join('#[%s]' % ', '.join(str(t) for t in ra[a]) for a in range(m))
    ias = ', '.join('#[%s]' % ', '.join(str(b) for b in ia[a]) for a in range(m))
    link = """
/-- The key as a `DCheck18` configuration (the dfast/wheelcheck18 input line). -/
def cf : DCheck18.Conf where
  name := "%s"
  r := %d
  m := %d
  ringAdj := #[%s]
  intAdj := #[%s]

theorem intAdjOf_eq : intAdjOf (DCheck.Conf.of18 cf) = intAdj := by
  funext a b
  change Fin %d at a b
  fin_cases a <;> fin_cases b <;> simp [intAdjOf, DCheck.Conf.of18, cf, intAdj, intList]

theorem ringAdjOf_eq : ringAdjOf (DCheck.Conf.of18 cf) = ringAdj := by
  funext a t
  change Fin %d at a
  fin_cases a <;> simp [ringAdjOf, DCheck.Conf.of18, cf, ringAdj, ringList]

theorem cf_sym : ∀ a b, intAdjOf (DCheck.Conf.of18 cf) a b = true →
    intAdjOf (DCheck.Conf.of18 cf) b a = true := by
  rw [intAdjOf_eq]; unfold intAdj intList; decide

theorem cf_loop : ∀ a, intAdjOf (DCheck.Conf.of18 cf) a a = false := by
  rw [intAdjOf_eq]; unfold intAdj intList; decide

/-- **Per-key reduction**, given the checker's verdict `hD` (studio14c/14d, `wheelcheck18`). -/
theorem colorable_of_occ_dred (hD : DCheck18.dReducible cf = true) {T : SphericalMap n}
    (htri : T.Triangulated) {ring : Fin %d → Fin n} {int : Fin %d → Fin n} (h : Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 := by
  obtain ⟨G, O, hlt⟩ := configOcc htri h
  obtain ⟨cG⟩ := IH n G (by rw [natCard_support_eq, natCard_support_eq]; exact hlt)
  rw [← intAdjOf_eq, ← ringAdjOf_eq] at O
  exact ConfigOcc.colorable_of_dReducible18 (T := T) (G := G) cf hD (by decide) (by decide)
    cf_sym cf_loop O (c := cG) (fun x y e _ _ => cG.valid e)
""" % (name, r, m, ras, ias, m, m, r, m)
    # drop the generated colorable_of_occ (it needs the certificate) and append the DCheck link
    i = occ.index('/-- **Reduction.**')
    occ = occ[:i] + link + '\nend SimpleGraph.SphericalMap.%s\n\n#print axioms SimpleGraph.SphericalMap.%s.colorable_of_occ_dred\n' % (ns, ns)
    return occ

if __name__ == "__main__":
    keyfile, lineno, ns, outdir = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    line = [l for l in open(keyfile) if l.strip()][lineno]
    open('%s/%s.lean' % (outdir, ns), 'w').write(gen_key(line, ns))
