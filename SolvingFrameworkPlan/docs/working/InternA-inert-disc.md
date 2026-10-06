# Inert-disc lemma: what survives, what does not

Intern A, 6 Oct 2026. Hand only. Labels: [hand] proved, [conditional] proved under a stated hypothesis, [refuted] with mechanism.

Notation: x0..x4 = link (a,b,a,g,d); sage's v1..v5 = x0..x4, so v2 = x1, v3 = x2, v4 = x3, v5 = x4. L1 = a {b,g}-chain x1~x3, L2 = a {b,d}-chain x1~x4, J1 = v+L1, J2 = v+L2. The rotation at v is x0,x1,x2,x3,x4, so J1 puts **x2 alone** on one side (call it D1) and x4,x0 on the other. J2 puts **x0 alone** on one side (D2) and x2,x3 on the other. (Agrees with the sage: only x2 is inside D1.)

## Planarity facts [hand]
- J1 carries only colours b,g (plus v). Every {a,d}-component is vertex-disjoint from J1, hence lies wholly on one side. Same for {a,g}-components versus J2 (J2 is b,d). Other pairs ({a,b},{a,g},{b,d},{g,d}) may touch J1 at its b or g vertices and then pass from one side to the other.
- Nesting: x2 in D1 not D2, x0 in D2 not D1, so neither disc contains the other. If L1 and L2 share only x1, then J2 lies in the closure of the far side of J1, and D1 and D2 are disjoint. If they share another b vertex, L2 can make an excursion into D1 and the discs can overlap; I found no obstruction to this.

## (i) [conditional, not true as stated]
Let K be a component strictly inside D1 (K disjoint from J1) containing no link vertex. Then the link, the frame and L1 are unchanged, so **lock 1 survives**. **Lock 2 survives iff a lock-2 path avoids K**: this is automatic if K is a {b,d}-component (it differs from K2, which contains x1), or if L2 never enters D1 (e.g. L1 and L2 meet only in x1). If L2 has an excursion into D1 and K is, for example, an {a,d}-component containing a d vertex of the excursion, K's swap recolours that vertex to a and may cut lock 2. So (i) needs "K does not meet L2".
If K contains x2: the only candidate is K_D2 (the {a,d}-component of x2; it is disjoint from J1 by colours). That swap is the catalogue move D2: it changes the link and the frame (new middle x3), keeps lock 1 as the old lock, and needs a new lock. It is strictly inside D1 but not lock-preserving; it can kill (D2-starvation).

## (ii) [refuted as stated]
A swap strictly inside D1 can start a shortest filling sequence. Mechanism: suppose x2 has degree 5, w1 is not d, and w2 = d, and the {b,d}-component Y of w2 is disjoint from J1 (so Y is strictly inside D1; Y is not K2 since K2 contains x1). The swap of Y keeps both locks (lock 1: L1 untouched; lock 2: K2 is a different {b,d}-component). It turns w2 to b, so x2 loses its only d-neighbour; then F fails lock 2' (F-starvation), so the sequence Y, F, fill has length 3. This is the dual of Math's silent swap SS3. Whenever the pattern has radius at least 4 and these hypotheses hold, the shortest sequence starts inside D1. I did not exhibit a concrete graph satisfying all hypotheses, so what is refuted is the implication "(i) hence (ii)", not that some instance exists.
What is true: a swap inside D1 with colour pair {a,d} that is not adjacent to x2 and not meeting L2 cannot affect any {a,d}-structure outside D1, so by itself it does not unlock a kill outside; I did not prove it cannot via other pairs (next point).

## (iii) What an inside-D1 swap can and cannot change [hand]
Cannot: any colour on or outside J1 (so x0,x1,x3,x4 and L1 intact, lock 1 kept); the {a,d}-connectivity outside D1 (Jordan); for a {b,d}- or {a,d}-swap the b-g structure of L1.
Can: colours of the interior vertices, hence (1) the neighbour colours at x2 (and at x3 along its inner arc between v and the L1 entry), changing the starvation tests (F-, D2-starvation, E1 at x2) on this side; (2) membership in K_F, K_AB, K_D2 and the {a,b}/{a,g} chains that cross J1 through its b/g vertices, so predicates such as AB★ can flip; (3) for L2 excursions, lock 2 itself. Anything outside D1 reads inside D1 only through x2's neighbours and through chains crossing J1.

## Self-check (two weakest points)
1. The side of J1 containing x2 is derived from the rotation at v and the rotations at x1 and x3 (x1: v,x0,w0,w1,x2; x3: v,x2,w2,m3,w3,x4); I did not draw a figure.
2. In (ii) I did not check whether the hypotheses (x2 degree 5, w2 = d, Y missing J1) are realised together with radius at least 4; Studio data should test exactly that.
