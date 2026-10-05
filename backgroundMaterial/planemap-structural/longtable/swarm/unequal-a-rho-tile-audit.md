# The remaining A_rho tile: local audit

4 October 2026. Hand argument with an independent symbolic-neighbourhood replay. This is a local slide lemma, not a compiled theorem or a completed proof for every belt hole.

Use the belt conventions of `unequal-tile.md` and `unequal-b-tile.md`. Let n >= 5, c(a)=0, c(b)=1, and {rho,tau}={2,3}. Indices are modulo n. The hole is v_i. The prepared shape is

    link(v_i) = (b,v_{i-1},u_i,u_{i+1},v_{i+1})
    colours   = (1,rho,tau,rho,0).

The A_rho tile has c(v_{i-2})=0, c(v_{i-1})=rho, c(u_{i-1})=1 and c(u_i)=tau. These are the previously unnamed slides for the orientation whose outer u-vertex has colour tau.

## First two slides

At v_i, tau is unique at u_i. Slide v_i -> u_i, writing tau on v_i. The new link is

    link(u_i) = (a,u_{i+1},v_i,v_{i-1},u_{i-1})
    colours   = (0,rho,tau,rho,1).

Colour 1 is unique at u_{i-1}. Slide u_i -> u_{i-1}, writing 1 on u_i. The new link is

    link(u_{i-1}) = (a,u_i,v_{i-1},v_{i-2},u_{i-2})
    colours       = (0,1,rho,0,x),

where x is the unchanged original colour of u_{i-2}. Originally u_{i-2} was adjacent to a=0 and u_{i-1}=1, so x belongs to {rho,tau}.

If x=rho, this link uses only {0,1,rho}. Fill u_{i-1} with tau. This branch ends after two slides.

## Return when x=tau

The link is now (0,1,rho,0,tau). Colour rho is unique at v_{i-1}. Slide u_{i-1} -> v_{i-1}, writing rho on u_{i-1}. The new link is

    link(v_{i-1}) = (b,v_{i-2},u_{i-1},u_i,v_i)
    colours       = (1,0,rho,1,tau).

Colour 0 is unique at v_{i-2}. Slide v_{i-1} -> v_{i-2}, writing 0 on v_{i-1}. The new link is

    link(v_{i-2}) = (b,v_{i-3},u_{i-2},u_{i-1},v_{i-1})
    colours       = (1,d,tau,rho,0).

This is the prepared-zero shape one A tile further along, with the same trailing colour rho. The poles have not moved or changed colour. In fact d=rho: before the slides, v_{i-3} was adjacent to b=1, v_{i-2}=0 and u_{i-2}=tau. The return therefore has exactly (1,rho,tau,rho,0).

The complete return path is

    v_i -> u_i -> u_{i-1} -> v_{i-1} -> v_{i-2}.

Each recolouring preserves properness because the colour transferred onto the old hole was unique on its full neighbour link. For n >= 5 the named same-ring vertices needed in these neighbourhoods are distinct. Extra wrap edges at n=5 do not change the neighbour lists or the singleton checks.

## Verification and remaining scope

The independent checker at `/Users/fulkanjou/Documents/ChatGPT/planemap/audits/gremlin-2026-10-04/check.py` checks both choices of rho/tau and all possible x,d consistent with the stated local edges. It imports none of the team's move implementations. Every singleton check passes, the x=rho branch reaches three colours, and the x=tau branch returns the prepared shape.

No n=14 enumeration was run. To obtain the general unequal-pole theorem, the opening cases, these tile transitions, cap cases, small-ring overlaps and termination of the joined walk still need to be assembled and reviewed. This page closes the local missing transition only.
