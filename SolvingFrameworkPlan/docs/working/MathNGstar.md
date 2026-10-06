# Math attack on (N), part 4: is (G*) provable? No: (G*) is false at N = 24

Math-team research worker, 6 October 2026. Continuation of `MathNCaseI.md`. Exploratory, undeclared; no declared experiment, nothing of others' edited, nothing staged or committed. Labels: [hand], [computed] (exploratory, post hoc), [open]. Status words stay with the Navigator. Scripts used are scratch scripts (session scratchpad: g3.py = Case I/II and (G*) test for c' and mirror c'' on every locked disc line of `res_23.txt` and `res2_24_p*.txt`; g5.py = BFS in the D'-free class with swap descriptions; g6.py/g7.py = branch B test; g8.py = link colours); they import `MathNCaseI-scripts/tn_lib.py`.

## 0. Result

| Question | Outcome |
|---|---|
| Is (G*) true? | **No. [computed] (G*) fails at N = 24.** Data: the 26 locked discs of `res2_24_p0..p3.txt` (new since `MathNCaseI.md`, all 26 satisfy (N) with *both* neighbours separable). 52 neighbours, 22 in Case I; 18 of those satisfy (G*), **4 do not**: the same three swaps Q4, E34, R reach c3 in the locked branch (u1 not~ u3, u4 in [alpha,gamma]_3, chain {D,beta} intact at c3). Lines: `res2_24_p0.txt` line 9 (mirror neighbour c''), `res2_24_p1.txt` line 3 (c''), `res2_24_p3.txt` lines 4 and 5 (c'). `recheck.py` (independent code) on all four: certifies the structure, `N HOLDS`, both neighbours separable (class sizes 31/24, 24/24, 19/36, 12/45). So these are genuine states; (G*) is not a theorem and cannot be proved. |
| Does this contradict (N) or T3? | No. In the four bad neighbours the unlock exists at D'-free distance exactly 3, by a different branch (below). |
| What replaces (G*)? | A branch-free statement: **(B3)** every neighbour is separable after at most three D'-free swaps, with a forced two-swap prefix (branch B, §2). [computed] 80 of 80 neighbours (N = 23: 28, N = 24: 52), Case I and II alike. Not proved. |
| Proof of (B3) or of (G*)-like fact? | Not found. The token automaton of `MathNPinchT3.md` §5.4 has closed orbits on every branch; I found no geometric input that kills the locked branch (§3). |

## 1. The numbers [computed]

N = 23 plus N = 24 (40 discs, 80 neighbours; none first-order unlocked): Case II 50, Case I 30. Of the 30 Case I neighbours: (G*) holds in 26 (and in each of them "chain {D,beta} broken at c3" coincides with (G*)), fails in 4 (chain intact too). So 'Case I always breaks at c3' (`MathNCaseI.md` §2, 8 of 8) was an N = 23 artefact, just as 'exactly one Case II' was an n = 17 artefact. Case I x Case I occurs also at N = 24 (res2_24_p0 lines 2, 4; p2 lines 1, 3).

Apex degree: in 28 of the 30 Case I neighbours deg(u0) = 5 (resp. deg(u2) = 5 for c''), in 2 it is 6.

## 2. What distinguishes the 4 failures, and branch B [computed]

Local picture (deg u0 = 5, link of u0 in T-x = u1, p, q, u4, in c colours alpha, gamma, beta, gamma with p the gamma-vertex, q the beta-vertex, both adjacent to u0): in the 22+ cases where (G*) holds with deg 5 the vertex q lies in E34, so after the swaps the link reads alpha gamma alpha gamma and u0 has **no beta neighbour in c3**: the chain {D,beta} is broken trivially, and the [alpha,gamma]_3 path of (G*) is just the link u1 - p - q - u4 (+ the arc to u3). In the 4 failures q is **not** in E34 (the E34 component stops before reaching q), q stays beta, and the chain {D,beta} survives. [hand] So for deg(u0) = 5 (G*) is equivalent to "q in E34"; this is a statement about whether an [alpha,beta]_1 component that contains u3, u4 reaches the neighbour q of u0, and nothing in the local data forces it.

Branch B. In c' (ring D alpha gamma beta gamma) the [alpha,gamma']-component of u4 is separated from the one of u1,u2 (H1); branch A (the note) swaps the u4-component first. Branch B swaps the other one:
 B1: swap the [alpha,gamma']-component of u1 (it contains u2) -> ring D gamma alpha beta gamma;
 B2: swap the [beta,gamma]-component of u1 -> ring D beta alpha beta gamma;
 B3: one further swap (various types) gives a chain-broken state.
[computed] Exhaustive check (g6/g7): after B1, B2 no neighbour is broken (no B2 case), and in all 80 neighbours some single further swap breaks a chain. The third swap is not uniform: the [alpha,gamma]-component through u2 (and/or u4) works in 59 cases (mirror: [alpha,beta]-comp through u0, u3 etc.), an [alpha,beta]-component through u1,u2,u3 in 9, a ring-free component in all of them (that last item is probably an artefact of such components being present; I did not analyse). For the 4 bad neighbours the BFS minimal unlocks are B-type: e.g. `res2_24_p0` line 9 (c''): swaps [alpha,beta] comp of (u0,u1) size 6, [beta,gamma] comp of u1 size 3, [alpha,gamma] comp of (u0,u1,u4) size 7, ending ring gamma alpha D beta alpha; the D'-free class has 14 or 18 members, distance 3 as before.

## 3. Attempts at a proof, and where they stop [hand]

1. Counting. Pair data (comps/cyc/m) along c', c1, c2, c3 (branch A) on the data: c' has [D,alpha] cyc 1; c2 has cyc 1 in [D,alpha], [D,beta], [alpha,gamma]; c3 keeps [D,alpha] 1, [D,beta] 1. In the locked branch Lemma DI/M fix the m-values and leave a consistent integer solution; since comps - cyc = V_pair - E_pair is just an edge count, any contradiction would need to constrain edge counts of colour classes under a Kempe swap, and these depend on R, E34, Q4 individually. No contradiction obtained. (Consistent with the closed orbit of `MathNPinchT3.md` §5.4.)
2. Planarity/winding: unchanged from `MathNCaseI.md` §4; the failure of (G*) at N = 24 shows no argument that works uniformly on branch A can exist (it would prove a false statement). In particular any proof must use something that is not true of the 4 failures: they have (O), tau = -1, one-rhombus pinch like the others [not recomputed for N = 24, so this last remark is [open]].
3. Link argument (deg u0 = 5): reduces (G*) to "q in E34" (§2); false in the failures.

So the obstruction is exact: **(G*) holds iff the swap component E34 meets the beta-neighbour of u0 (deg 5 case), and E34 is a component of [alpha,beta]_1 that depends on the whole disc.** There is a Case I configuration, consistent with all local data I know and realised by an actual triangulation of order 24, in which branch A gets to c3 locked.

## 4. Recommended reformulation [open]

Replace (G*) by (B3), or by the branch-free unlock statement 'the D'-free Kempe class of c' contains a chain-broken or 3-coloured-ring member within 3 swaps' (28 of 28 at N = 23, 52 of 52 at N = 24 [computed: B3 80/80 and first-order lower bound by `MathNPinchT3.md` §5.2]). Also still to do: (a) rerun `geo23.py` pinch data ((O), tau, Lambda) on the N = 24 discs; (b) analyse the third swap of branch B (is there a canonical choice, e.g. depending on a single token as in Case I/II?). N = 24 data came from `disc_gen2` (post hoc; the exhaustiveness of the N = 24 run is untested against an independent census).
