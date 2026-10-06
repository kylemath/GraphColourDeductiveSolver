# Intern A: link class (5,5,5,6,6), two ADJACENT degree-6 link vertices

No code run. All by hand, from HP's proof as summarised in MathReviewTheoremHP.md and StudioMathReviewHPandH.md (I did not re-read MathConjectureR.md).

## 1. Claim
**[open]** with a **[hand] partial** structure result: HP's proof does not extend verbatim to (5,5,5,6,6); no finite bound is proved. I locate exactly which HP steps fail, for each of the three position-pairs of the two free vertices, and one pair ({3,4}) where the failure is confined to two new patterns plus the AB kill.

Setup: frame link (a,b,a,g,d), colours as in HP. Free vertices are x_k, x_{k+1} (deg 6), the other three have degree 5. A deg-6 x_t has neighbours v, x_{t-1}, x_{t+1}, w_{t-1}, m_t, w_t, so ring edge w_{t-1}w_t is NOT forced (path w_{t-1} m_t w_t instead), and any lock-end condition read at x_t is lost. Pairs up to the mirror k -> 2-k: {0,1}~{1,2}; {2,3}~{4,0}; {3,4} self-mirror.

## 2. Step table
| HP step | needs deg 5 at | survives for (5,5,5,6,6)? |
|---|---|---|
| Setup, no link chords, w's may coincide | none | survives |
| Jordan facts (x_0 not in K_F, x_2 not in K_B) | none | survives |
| F-/B-starvation as a *mechanism* (d-nbr of x_2 unchanged by F; g-nbr of x_0 unchanged by B) | none | survives |
| Starvation as a *kill* | F: x_2; B: x_0 | F-kill fails if 2 in {k,k+1} (pairs {1,2},{2,3}); B-kill fails if 0 in {k,k+1} (pairs {4,0},{0,1}); both survive for {3,4} |
| Lemma 1 (pattern list) | ring edges at t not free; lock ends at x_1,x_3,x_4 | list **enlarges**. For {3,4} I derived it: x_0,x_1,x_2 deg 5 give ring edges w4w0, w0w1, w1w2 and {w0,w1}={g,d}; lost: b in {w2,w3}, b in {w3,w4}. Result: gdbab, gdbbb, dg{b,d}{a,b}{b,g} (10 patterns) = the 7-pattern union of the k=3 and k=4 lists plus three new: **gdbbb, dgbbb, dgdag** |
| Lemma 2 easy kills | as kills above | For {3,4}: dgbbb dies by B-kill; the 7 old patterns keep their HP kills (those only read x_0/x_2 colours) except R3; **gdbbb (w0=g, w1=d) and dgdag (w2=d, w4=g) escape both starvation kills** and are new non-easy states |
| AB kill for R3 at k=3,4 | x_3 or x_4 deg 5 for the last colour check | **fails**: after the swap the deg-6 x_3/x_4 has an extra neighbour m of unconstrained colour, so lock 1'/2' is not forced to fail (the component {x_0,x_1,x_2} itself is still exact, those are deg 5) |
| Lemma 3 transitions F/B on R1,R3 | colours of named ring vertices only | colour reading survives (Jordan fact is degree-free), but the position shifts by -3 (F) / +3 (B), so pair {3,4} goes to {0,1} (F) or {1,2} (B): exactly the pairs where a starvation kill is lost. Image is no longer forced into HP's list |
| Termination table (D values, radius <= 6) | all above | **fails**: chains no longer end in easy states |

## 3. Precise gap
(i) R3 at pair {3,4} has no terminal kill (AB needs the colour of m_3/m_4). (ii) The new patterns gdbbb, dgdag at {3,4} have no kill. For gdbbb, F leaves the ring colours unchanged (no a/g ring vertex next to K_F) and gives ring (g',g',d',b',g') in the new frame with free pair {0,1}, where Lemma 1 has lost the {w'0,w'1}={g',d'} condition, so I cannot continue. (iii) For pairs {0,1},{1,2},{2,3},{4,0} one starvation kill is lost for every pattern needing it, and the pattern lists grow by an amount I did not derive.
**Extra hypotheses that would repair the AB step** for R3@{3,4}: the colour of m_4 (resp. m_3) after the swap is not d (resp. not the colour lock 1' needs); equivalently m_3, m_4 coloured so that the deg-6 vertex is "starved" like a deg-5 one. A separate Kempe step recolouring m outside the {a,b} component is plausible but unproved. Any bound is >= 4 (T4), and I expect HP's 6 to grow, not to survive.

## 4. Self-check, two weakest points
1. The 10-pattern list for {3,4} is derived once by hand; a slip in an allowed-colour set would change which patterns are "new". I did not derive lists for the other four pairs.
2. "AB kill fails" is a statement that HP's argument fails, not that the state cannot be killed another way (e.g. another swap or the colours of m); I did not search for a different kill, and I did not check the F-image of gdbbb for an actual DL pattern.
