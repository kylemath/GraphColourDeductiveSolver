# Unequal poles: the doubled-other-pole opening

Independent audit, 4 October 2026. Local lemma for Long Table's review; not a termination proof.

Use the belt edges `a-u_i`, `b-v_i`, `u_i-u_(i+1)`, `v_i-v_(i+1)`, `u_i-v_i`, `u_i-v_(i-1)`, with indices modulo n and n >= 5. Fix a=0, b=1 and {rho,tau}={2,3}. Suppose the hole is u_i and its link in the order (a,u_(i+1),v_i,v_(i-1),u_(i-1)) is

    (0,1,rho,tau,1).

This covers both doubled-1 local words by exchanging rho and tau.

Slide u_i -> v_i, which is legal because rho occurs once in the old link. It writes rho at u_i. The new link at v_i, in the order (b,v_(i-1),u_i,u_(i+1),v_(i+1)), is

    (1,tau,rho,1,x).

Originally v_(i+1) is adjacent to b=1, v_i=rho, and u_(i+1)=1, so x is either 0 or tau.

* If x=tau, this link uses only {1,rho,tau}. Fill v_i with 0: one slide suffices.
* If x=0, slide v_i -> v_(i+1), which is legal because 0 occurs once in the current link. This writes 0 at v_i. Put p=c(u_(i+2)). The original neighbours a=0, u_(i+1)=1, and v_(i+1)=0 force p in {rho,tau}. Put q equal to the other colour in {rho,tau}. The original neighbours b=1, v_(i+1)=0, and u_(i+2)=p force c(v_(i+2))=q. The original neighbours a=0, u_(i+2)=p, and v_(i+2)=q force c(u_(i+3))=1. Thus the current link at v_(i+1), ordered (b,v_i,u_(i+1),u_(i+2),v_(i+2)), is (1,0,1,p,q). Slide v_(i+1) -> u_(i+2), legal because p occurs once. The link at the new hole u_(i+2) is (0,1,q,p,1).

Therefore this opening either fills after one slide or returns to the same opening class two indices forward after three slides. Both poles stay fixed. All three slides are legal by the displayed singleton colours. The local argument holds for n=5 as well: all displayed vertices on each ring that need distinctness are distinct.

Repeated application on a cycle is not a decreasing measure. This lemma supplies the missing doubled-1 transition, but a cap, a Kempe escape, or an independently proved termination argument is still needed. The eight doubled-0 words remain separate opening cases. A global belt theorem does not follow from this page.
