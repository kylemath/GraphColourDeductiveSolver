# Team A: both missing belt tasks

Independent competing proof team, 5 October 2026. Candidate proof for review. Only singleton slides are used, and both pole colours remain fixed. This completes the unequal-pole belt-vertex case for every ring length n >= 5; it does not by itself prove the equal-pole case or the pole-deletion theorem.

Use a-u_i, b-v_i, both ring cycles, and u_i-v_i,u_i-v_(i-1), indices modulo n. The poles have colours a=0,b=1; write {rho,tau}={2,3}. A hole is fillable when its neighbours use at most three colours.

## Symmetries and complete opening list

A belt hole can be named u_0: rotations suffice for upper-ring holes; the symmetry a'<-b,b'<-a,u'_j<-v_(-j),v'_j<-u_(-j) exchanges rings. Rename colour 0 and 1 when exchanging the poles. The reflection u'_j=u_(-j),v'_j=v_(-j-1), with poles fixed, reverses the u_0 link.

The link order is (a,u_1,v_0,v_(-1),u_(-1)). Any nonfillable link uses all four colours, so exactly one colour is doubled. The permitted upper/lower colour sets, link edges u_1-v_0,v_0-v_(-1),v_(-1)-u_(-1), and the pole edges give exactly:

* eight doubled-0 words; up to reflection and exchange rho/tau they are A=(0,1,0,rho,tau) and B=(0,1,rho,0,tau);
* two doubled-1 words (0,1,rho,tau,1);
* four doubled-rho/tau words; up to reflection and exchange they are (0,1,rho,tau,rho).

These cases are exhaustive: a four-colour five-position link has multiplicities 2,1,1,1, and the proper local choices just stated enumerate every location of the double.

## Doubled-1: the original cap forces termination

Start with (0,1,rho,tau,1). In particular the untouched original cap is u_(n-1)=1,v_(n-1)=tau. The established local return at u_i is: slide u_i->v_i; either fill immediately, or slide v_i->v_(i+1)->u_(i+2), returning to a doubled-1 word. A nonfilling return forces the ORIGINAL colours v_(i+1)=0, u_(i+2) in {rho,tau}, v_(i+2) the opposite tight colour, and u_(i+3)=1, provided those forward vertices are untouched.

Lift indices to 0,1,...,n-1. Successive return positions are 0,2,4,...; a return consumes two new indices, and neither cap vertex changes. If n is even, a prospective nonfill at i=n-2 would require v_(n-1)=0, contradicting its cap colour. If n is odd, at i=n-3 it would require u_(n-1) in {rho,tau}, contradicting the cap colour 1. In fact a contradiction can occur one return earlier because the forced u_(n-2)=1 would be adjacent to u_(n-1)=1, but that sharper bound is unnecessary. Thus the process fills strictly before any forward slide could revisit u_0 or enter the cap. Every use of the local lemma has distinct untouched forward vertices. The decreasing measure is the number of unprocessed indices before the cap, not a cyclic distance.

## All eight doubled-0 words

### A=(0,1,0,rho,tau)

The colour rho at v_(-1) is unique. Slide u_0->v_(-1), writing rho on u_0. Originally v_(-2) is adjacent to b=1,v_(-1)=rho,u_(-1)=tau, so v_(-2)=0. The new v_(-1) link is (1,0,tau,rho,0).

Exchange rings using u'_j=v_(-j),v'_j=u_(-j), exchange the names of pole colours 0 and 1, and rotate the new upper hole to index zero. The word becomes (0,1,tau,rho,1), a doubled-1 word. The previous paragraph proves finite filling. This symmetry is only a change of notation; the actual poles retain their original colours.

### B=(0,1,rho,0,tau)

Slide u_0->u_(-1), writing tau on u_0. Originally v_(-2)=rho: it meets b=1,v_(-1)=0,u_(-1)=tau. Originally u_(-2)=1: it meets a=0,u_(-1)=tau,v_(-2)=rho. The u_(-1) link is therefore (0,tau,0,rho,1), so rho is unique. Slide u_(-1)->v_(-2), writing rho on u_(-1).

The v_(-2) link is (1,w,1,rho,0), where w is the original v_(-3). Properness of the original edge v_(-3)v_(-2) excludes w=rho, and the pole excludes w=1, so w is 0 or tau. If w=0, fill immediately. If w=tau, the original v_(-4)=0 (a run of three tight lower colours would force adjacent upper colours 1), and u_(-3)=rho (it meets a=0,v_(-3)=tau,u_(-2)=1). Two A_tau slides v_(-2)->v_(-3)->v_(-4) produce a prepared zero, with trailing u_(-3)=rho and v_(-3)=0.

The untouched cap has u_0=tau,u_1=1,u_(-1)=rho,v_0=rho,v_(-1)=0. This is precisely the cap in the next argument. All indices used are distinct for n>=5. For n=5 the returned zero v_(-4)=v_1 forces the short-cap alternative; for n=6 a long cap would put the new prepared upper colour rho next to cap u_2=rho; for n=7 the two original zeros v_(-4)=v_3 and cap v_2 would be adjacent. Thus no small-length overlap escapes the following cap argument.

## Prepared-zero: finite traversal and the terminal cap

This covers both the tight doubled-rho opening and the B opening above. The tight opening uses u_0->v_(-1)->v_(-2). It sets u_0=tau,v_(-1)=0 and leaves u_(-1)=rho,u_1=1,v_0=rho. Its first prepared zero is v_(n-2). The B opening either fills or reaches v_(n-4), with the same fixed cap.

Use decreasing unwrapped indices. A prepared zero v_i has trailing u_(i+1)=rho,v_(i+1)=0. The vertices ahead of the hole retain their original colours. The original lower-ring colour-0 vertices, in increasing order, form a finite list. Consecutive zeros are separated by an A gap (one tight vertex) or a B gap (two tight vertices), because three consecutive tight vertices force adjacent upper colours 1, away from the initial hole edge. The next zero ahead is therefore i-2 or i-3.

The verified tile lemmas exhaust the next tile:

* A_rho, outer upper colour 1: fill at the present zero.
* A_rho, outer upper colour tau: two slides fill if the next outer upper colour is rho; otherwise two further slides return at i-2.
* A_tau: outer rho is improper against trailing rho; outer 1 returns at i-2 after two slides.
* B_rho is improper against trailing rho; B_tau returns at i-3 after four slides.

A return changes only the consumed tile and the old hole; the forward zero and its yet unprocessed side remain the original colouring. Thus each return removes exactly one gap from a finite ordered list without changing the cap. This gives a single measure for all A/B returns: the number of original gaps still between the present zero and the cap. It is never interpreted modulo n.

The cap has two possible extensions. Since v_0=rho,u_1=1, v_1 is 0 or tau. If v_1=tau, then v_2=0 and u_2=rho (three tight vertices would force adjacent upper 1s, and u_2 meets v_1=tau and u_1=1).

Short cap v_1=0: every ordinary return ends at a zero of index at least 1. At index 1 the prepared link is (1,rho,1,rho,0), so it fills. No cap vertex has been rewritten.

Long cap v_1=tau,v_2=0,u_2=rho: a prepared zero cannot be at index 2, because trailing u_3=rho would be adjacent to cap u_2=rho. Consider the final ordinary gap ending at original zero v_2. A B gap has either its low upper vertex u_3=rho, improper next to u_2, or its high upper vertex rho, improper next to the prepared trailing rho. An A_tau gap also has u_3=rho, improper next to u_2. The only remaining gap is A_rho at indices 2,3,4. Outer u_4=1 makes the current link at v_4 three-coloured. Outer u_4=tau gives two legal slides v_4->u_4->u_3 and the link (0,1,rho,0,rho), which fills. Thus the terminal gap ends the process before it could touch the cap zero.

For n=5 the tight opening's long cap would give adjacent original zeros v_2 and v_3, so it cannot occur. All other small overlaps are covered either by the original-zero nonadjacency constraint or by the displayed cap-edge contradiction. Reflection gives the opposite direction.

## Conclusion and verification status

Every proper four-colouring with unequal pole colours and a belt-vertex hole on this graph has a finite singleton-slide path to a fillable link, for every n>=5. Both repeating mechanisms use the same measure: the number of original untouched belt columns on the oriented arc from the macro-state hole to its fixed cap. In the doubled-1 coordinates this is n-1-i; in decreasing prepared-zero coordinates it is i-ell, where ell=1 for the short cap and ell=2 for the long cap. A return decreases this number by 2 or 3. The opening transitions form a finite prefix before this measure is needed; a branch that changes representation does so only once. This ranks the selected strategy, not every possible legal slide. No step changes either pole and no Kempe swap is needed.

The local slide assertions have existing separately checked notes. Team A deterministic replay (`team-a-belt-check.py`, standard library plus the audit chat's independent deletion-start enumerator) checked this exact combined strategy on the already named n=5,8,11 graphs: all 19, 121 and 807 unequal-pole starts filled. It records and independently replays 947 explicit original-labelled paths, validates singleton legality/properness after every slide, and checks both poles remain fixed. The strategy maxima are 4,10,14 slides; these are lengths of this selected strategy, not shortest distances. Branch counts include 148 doubled-1 returns and 154 prepared-zero returns. This is a regression check of the proof, not a new census and not the source of the infinite claim. External acceptance is still required.
