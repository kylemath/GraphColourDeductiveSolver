#!/usr/bin/env python3
"""Generate, for a configuration and an orientation, the certificate module and the module
deriving `ConfigOcc` from a rotation-based occurrence `Occ` (the audit's `Occurs`)."""
import sys
sys.path.insert(0, '.')
from gen_cert import Config, generate

CONFS = {
    "Diamond": (6, {7: [2, 8, 9, 10, 1], 8: [2, 3, 4, 9, 7], 9: [8, 4, 5, 10, 7], 10: [9, 5, 6, 1, 7]}),
    "Conf2122": (7, {8: [2, 3, 9, 10, 11, 1], 9: [3, 4, 5, 10, 8], 10: [9, 5, 6, 11, 8], 11: [10, 6, 7, 1, 8]}),
}


def setup(name, eps):
    r, rot = CONFS[name]
    labels = sorted(rot)
    idx = {v: i for i, v in enumerate(labels)}
    # ring order: eps = +1 decreasing RSST order, eps = -1 increasing
    if eps == 1:
        pos_of = lambda u: (r - (u - 1)) % r          # RSST label -> ring position
        lab_of = lambda t: (r - t % r) % r + 1        # ring position -> RSST label
        posexpr = "(%d - t %% %d) %% %d" % (r, r, r)
    else:
        pos_of = lambda u: u - 1
        lab_of = lambda t: t % r + 1
        posexpr = "t %% %d" % r
    return r, rot, labels, idx, pos_of, lab_of, posexpr


def V(u, r, idx):
    return "(ring %d)" % (u - 1) if u <= r else "(int %d)" % idx[u]


def gen(name, eps, ns):
    r, rot, labels, idx, pos_of, lab_of, posexpr = setup(name, eps)
    m = len(labels)
    cfg = Config(name, r, rot, pos_of)
    cert = generate(cfg, None, ns)
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
    return cert, "\n".join(lines)


if __name__ == "__main__":
    name, eps, ns, outdir = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    cert, occ = gen(name, eps, ns)
    open("%s/%sCert.lean" % (outdir, ns), "w").write(cert)
    open("%s/%sOcc.lean" % (outdir, ns), "w").write(occ)
