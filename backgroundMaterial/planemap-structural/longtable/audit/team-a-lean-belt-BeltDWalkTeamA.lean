module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.BeltCapsMath

@[expose] public section
namespace SimpleGraph.BeltDWalkTeamA
open VacancySlide BeltVacancyTeamA BeltVacancyTeamA.Vertex BeltCapsMath

/-- The complete D-family walk, with actual cap preservation and decreasing
unwrapped index budget. This is not yet the all-opening belt theorem. -/
theorem doubled_one_walk {n : Nat} (hn : 5 ≤ n) (i : Nat) (hi : i ≤ n-2)
    (c : Vertex n → Colour) (rho tau : Colour)
    (hc : ProperOff (graph n) (u (i : ZMod n)) c)
    (ca : c a=0) (cb : c b=1)
    (cup : c (u ((i : ZMod n)+1))=1) (cum : c (u ((i : ZMod n)-1))=1)
    (cvi : c (v (i : ZMod n))=rho) (cvm : c (v ((i : ZMod n)-1))=tau)
    (hr0 : rho ≠ 0) (hr1 : rho ≠ 1) (ht0 : tau ≠ 0)
    (ht1 : tau ≠ 1) (hrt : rho ≠ tau)
    (capu : c (u ((n-1 : Nat) : ZMod n))=1)
    (capv : c (v ((n-1 : Nat) : ZMod n)) ≠ 0) :
    ∃ k t, SlidePath k (u (i : ZMod n),c) t ∧ Target t.1 t.2 ∧ k ≤ 2*(n-i) := by
  generalize hm : n-i=m
  induction m using Nat.strong_induction_on generalizing i c rho tau with
  | h m ih =>
    obtain ⟨first,done|zero⟩ := doubled_one_first hn (i : ZMod n) c rho tau
      hc ca cb cup cum cvi cvm hr0 hr1 ht0 ht1 hrt
    · exact ⟨1,_,first,done,by omega⟩
    have hnlast : i ≠ n-2 := by
      intro he; subst i
      have e : (((n-2 : Nat) : ZMod n)+1) = ((n-1 : Nat) : ZMod n) := by
        have e : n-2+1=n-1 := by omega
        simpa using congrArg (fun j : Nat => (j : ZMod n)) e
      rw [e] at zero
      exact capv zero
    have hnpre : i ≠ n-3 := by
      intro he; subst i
      have e : (((n-3 : Nat) : ZMod n)+1) = ((n-2 : Nat) : ZMod n) := by
        have e : n-3+1=n-2 := by omega
        simpa using congrArg (fun j : Nat => (j : ZMod n)) e
      rw [e] at cup
      exact d_prelast_impossible hn c hc cup capu
    have hirange : i ≤ n-4 := by omega
    obtain ⟨d,p,q,path,da,db,du3,du1,dv2,dv1,hp0,hp1,hq0,hq1,hpq,deq⟩ :=
      doubled_one_return hn (i : ZMod n) c rho tau hc ca cb cup cum cvi cvm
        hr0 hr1 ht0 ht1 hrt zero
    have cap := d_return_preserves_last hn hirange c
    change _ ∧ _ at cap
    rw [←deq] at cap
    have hdcapu : d (u ((n-1 : Nat) : ZMod n))=1 := cap.1.trans capu
    have hdcapv : d (v ((n-1 : Nat) : ZMod n)) ≠ 0 := by rw [cap.2]; exact capv
    have hi' : i+2 ≤ n-2 := by omega
    have hproper : ProperOff (graph n) (u ((i+2 : Nat) : ZMod n)) d := by
      simpa using path.proper hc
    have idx3 : (((i+2 : Nat) : ZMod n)+1)=(i : ZMod n)+3 := by push_cast; ring
    have idx1 : (((i+2 : Nat) : ZMod n)-1)=(i : ZMod n)+1 := by push_cast; ring
    have hcup : d (u (((i+2 : Nat) : ZMod n)+1))=1 := by rw [idx3]; exact du3
    have hcum : d (u (((i+2 : Nat) : ZMod n)-1))=1 := by rw [idx1]; exact du1
    have hcvi : d (v ((i+2 : Nat) : ZMod n))=q := by simpa using dv2
    have hcvm : d (v (((i+2 : Nat) : ZMod n)-1))=p := by rw [idx1]; exact dv1
    obtain ⟨k,t,tail,target,bound⟩ := ih (n-(i+2)) (by omega) (i+2) hi'
      d q p hproper da db hcup hcum hcvi hcvm hq0 hq1 hp0 hp1 hpq.symm hdcapu hdcapv rfl
    have tail' : SlidePath k (u ((i : ZMod n)+2),d) t := by simpa using tail
    exact ⟨3+k,t,path.append tail',target,by omega⟩

/-- A normalized doubled-1 opening fills within the claimed 2n slide budget. -/
theorem doubled_one_opening_fills {n : Nat} (hn : 5 ≤ n)
    (c : Vertex n → Colour) (rho tau : Colour)
    (hc : ProperOff (graph n) (u 0) c)
    (ca : c a=0) (cb : c b=1) (cup : c (u 1)=1) (cum : c (u (-1))=1)
    (cvi : c (v 0)=rho) (cvm : c (v (-1))=tau)
    (hr0 : rho ≠ 0) (hr1 : rho ≠ 1) (ht0 : tau ≠ 0)
    (ht1 : tau ≠ 1) (hrt : rho ≠ tau) :
    ∃ k t, SlidePath k (u 0,c) t ∧ Target t.1 t.2 ∧ k ≤ 2*n := by
  have elast : ((n-1 : Nat) : ZMod n) = -1 := by
    rw [Nat.cast_sub (by omega : 1 ≤ n),ZMod.natCast_self,Nat.cast_one,zero_sub]
  have capu : c (u ((n-1 : Nat) : ZMod n))=1 := by rw [elast]; exact cum
  have capv : c (v ((n-1 : Nat) : ZMod n)) ≠ 0 := by rw [elast,cvm]; exact ht0
  simpa using doubled_one_walk hn 0 (by omega) c rho tau (by simpa using hc) ca cb
    (by simpa using cup) (by simpa using cum) (by simpa using cvi) (by simpa using cvm)
    hr0 hr1 ht0 ht1 hrt capu capv

end SimpleGraph.BeltDWalkTeamA
