# Job 28: design for p letters + the two-step rule 5 → 6 → big (DESIGN ONLY, not run) [exploratory]

Written 16 Oct 2026 on Long Table's instruction. It is gated on the explore thread's H-R1 probe. If H-R1 dies, shelve it.

## The obstruction it targets

The d = 10 receiver u has link 5656556565 and every s = 6, giving six lone fives (round 8 certificate, t* = 2/7).
- Every configuration that kills it fixes p, the second-ring private vertex of a 6-neighbour w_j. Here w_j has degree
  6, so it has exactly one neighbour outside {u, w_{j±1}, s_{j-1}, s_j}.
- The arrangement survives only when all four such p are ≥ 7.
- Under 5 → big rules, the six lone fives with the 6s between them form a closed positive cluster, so the bound 2/7
  cannot move. Long Table's reading is the same.
- Something must send charge out of the cluster: lone five → 6 → big p.

## 1. Rule class (new variables)

- **Direct, unchanged:** y[r] for r = the five's link word rooted at its big neighbour (wlp.py `roots`).
- **Two-step, new:** z[q], the charge a five v sends through a 6-neighbour x to a big neighbour p of x.
  - Minimal index: q = (r_v, σ, P), where r_v is v's link word rooted at x (x has letter 6), σ ∈ {left, right} says which
    of x's two neighbours in v's link is the other common neighbour, and P ∈ {7, 8, 9} is p's letter.
  - Here p is the vertex of x's link opposite to v, across x. For x of degree 6 its link is (v, a, b, p, b', a'), so p
    is the far vertex.
  - With p fixed as "the far vertex of x's link", σ is not needed. Index q = (r_v at x, x's link word rooted at v,
    letter 6 only). That is about 5^5 × 5^5 before canonical folding; restrict to x's link words with p ≥ 7. In
    practice, only the ones that occur in the separated arrangements become columns (column generation, as the
    rows already are).
- **Variant used by H-R1** (to be matched to whatever the explore thread tested): z indexed by v's root at u, plus
  the side, plus p's letter. That is smaller, but it sees less.

## 2. Sender rows

Σ_{big nbrs} y[root] + Σ_{6-nbrs x, far vertex p of x big} z[q] ≥ 1 − t, for every non-R five link word extended by
its 6-neighbours' links. Sender rows therefore become radius-2 objects: the five's 2-ball, restricted to the 6s.
- Enumerate them as now: senders × (for each letter-6 position of the five's link, the 6's link word with the
  shared letters consistent). Each 6 contributes 5^3 free letters; prune by R5/R6 wheels and the fan/diamond lists.

## 3. Receiver rows (the expensive part)

A big receiver u of degree d gets direct charge from its 5-neighbours, and two-step charge from every five v at
distance 2 that reaches u through a 6-neighbour w_j of u. From u's side, v is a 5 among {w_{j±1}, s_{j-1}, s_j, p_j}
and u is the far vertex of w_j's link from v.
- So u's arrangement needs, at each link position j with w_j = 6, the private letter **p_j** (one letter, since
  deg w_j = 6). The two-step senders through w_j are then the fives in w_j's link opposite to u.
  - For w_j = 6 that link is (u, w_{j+1}, s_j, p_j, s_{j-1}, w_{j-1}). The vertex opposite u is p_j, so the
    only two-step sender through w_j toward u is **p_j itself, when p_j = 5**. (The fives w_{j±1}, s_{j-1}, s_j are
    not opposite u.)
- **sep3 state change.** At each link position with w_j = 6, add one letter p_j ∈ {5..9}.
  - Sender roots at w_j = 5 positions are unchanged.
  - New z columns contribute when w_j = 6 and p_j = 5. Their index needs p_j's link rooted at w_j:
    (w_j = 6, s_{j-1}, ?, ?, s_j), two letters beyond the receiver's 2-ball. Option A: add them to the state as well
    (2 more letters per 6-position). Option B: aggregate them as a max over the unknown letters. That is sound for
    an upper bound on the receiver load: take the max of z over those letters, which is what the separation DP
    does if those letters are free.
- **State size.** Now 125 states × 25 choices. With p_j: the state gains p_{j} for the current w_j only when
  w_j = 6. That is a factor ≤ 5 on states, and ≤ 5 more with Option A. The bounds matrix grows 25–125×. That is
  feasible for d ≤ 10; d ≥ 11 stays on the plain DP + Karp bound, unchanged.
- **Patterns.** The p_j letter makes the hl3 verdicts matchable: the pattern carries p_j at the positions their
  name fixes. Extend sep3's mask to the new slot, and give wlp3 a name format carrying p letters, e.g.
  `f<d>_<link>_<s>_<p>` with '.' where unspecified.

## 4. Where p letters are needed (Long Table: "only next to lone fives, d = 7..10")

- The z columns only matter at 6-positions adjacent to a lone five, and p letters only at those positions.
- In sep3 a five's loneness is known once its two links are chosen. So add p_j to the state only when
  w_{j-1} or w_{j+1} is a lone 5. That is at most a factor 5 at those positions, and none elsewhere.

## 5. Soundness checklist (before any run)

1. Every sender row lists all its outflows, direct and two-step, so that Σ out ≥ 1 − t is a valid constraint on
   the rule.
2. Every receiver row counts every two-step inflow possible in its arrangement. That needs p_j at every w_j = 6
   adjacent to a 5, or else an explicit max over the missing letters (Option B). It must not count only the ones
   next to lone fives unless z is restricted to lone senders, which is itself a rule restriction and is fine.
3. Charge passing through a 6 leaves the 6's net charge 0, because it forwards everything it receives.
4. The d ≥ 11 tail: two-step inflow is bounded by (number of 6-neighbours) × max z, so add it to the Karp bound.
5. Validation, as for wlp3:
   - With all z forced to 0, the new code must reproduce wlp3's t* (2/7 on the round-8 pattern set).
   - With the hl3 patterns only, t* must not rise.

## 6. Estimate

- sep3 changes, ~150 lines: state extension, z contributions, mask slot.
- wlp3, ~100 lines: z columns, radius-2 sender rows, new name format.
- Validation runs: about 1 day of work, plus CPU. Nothing has been run.
