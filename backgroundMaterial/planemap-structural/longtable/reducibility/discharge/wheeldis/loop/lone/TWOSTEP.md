# Two-step rule class 5 -> 6 -> big: what Job 28 / gen28 need (16 Oct 2026, round 9) [exploratory spec, not built]

A two-step rule moves charge z from a five f through a 6-neighbour x to a big vertex q that is adjacent to x but not
to f. Its purpose is the lone five (u its only big neighbour), whose whole charge otherwise has to go to u.

## Why the current LP cannot see it

- wlp3's variables are y[rooted word] = (U; w_i+1, s_i, s_i-1, w_i-1). A lone five's rooted word does not say whether
  a big q exists at distance 2.
- So a sender row with a route and a sender row without one have the same y. If any pattern-free completion of a lone
  five has no route, its row is y + t >= 1, exactly as now, and the rule gains nothing.
- The rule can only lower t* if y depends on the route letters AND the completions without a route are forbidden
  (reducible). Round 8 (`hl3.py`) is the first test of the second half: in A1 the completions with p = 5 and p = 6 die.

## Geometry (checked with gen.py's builder)

Around a receiver u of degree d, link w_0..w_d-1, s_i the common neighbour of w_i and w_i+1:
- a link 6 w_j has one extra second-ring neighbour p_j, between s_j-1 and s_j (gen name ('p', j, 1));
- a link 5 w_j has s_j-1 adjacent to s_j;
- for a lone five w_i, the routes inside the 2-ball of u are: via w_i+1 = 6 to p_i+1, s_i+1 or w_i+2; via
  w_i-1 = 6 likewise; via s_i = 6 to p_i+1 (if w_i+1 = 6) or s_i+1 (if w_i+1 = 5); via s_i-1 likewise.
- Everything else is in the third ring.

## What to add

1. **Letters.** In sep3's arrangement DP, a p_j letter (5..9) whenever w_j = 6. The DP choice at a 6 becomes
   (s_c, w_next, p_c) instead of (s_c, w_next). gen28's `build(d, link, r2)` already takes r2[('p', j, 1)] (used by
   `hl3.py`), so configurations need no new builder.
2. **Extended rooted words for lone fives.** y[(U; a, b, c, e; R)], where R is the set of the five's in-ball route
   targets that are big, with their degree classes (7, 8, >= 9). Words with R empty are today's words.
3. **Two-step variables.** z[(R-entry, target class)] >= 0. Coarsest version: one z per target class 7, 8, >= 9.
4. **Sender rows.** For each extended lone word: y + sum over R of z + t >= 1. Only in-ball routes count. A route that
   only reaches the third ring counts as no route (conservative).
5. **Receiver rows at u**, both terms:
   - one-step: sum of y over the fives on the link, read with their extended words (needs the p letters);
   - two-step inflow: for each link 6 w_j, every five among s_j-1, s_j, p_j sends z[class of u] through w_j. Without
     third-ring letters the DP cannot tell whether that five is lone, so it must assume it is (charge the full z).
   Then sum - t <= d - 6.
6. **Patterns.** Pattern slots for p letters, so a B-fixed configuration plus an exact p (`hl3.txt`) becomes a pattern.
   Today `hl3.out` cannot be used as a wlp3 pattern, because wlp3 has no p letter.
7. **gen28.** For a certificate arrangement whose binders are lone fives with an open p slot, add the configurations
   u + S + N(S) + p at exact p in {5, 6} (the completions that would leave a lone five without a route). That is
   `hl3.py`, generalised to any arrangement.

## Cost side (what can go wrong)

- A big q of degree 7 has charge -1 and a link of 7. Each link 6 of q can pass z from up to three second-ring fives,
  so a 7 next to several 6s can be overloaded. The receiver rows in (5) carry that cost. The oracle in round 9 ignores
  it.
- H-R1's kill (pre-registered in EXPLORE-LOG): the oracle cannot move t below the one-step baseline, or the new bound
  is set by an arrangement with a lone five that has no in-ball route.
