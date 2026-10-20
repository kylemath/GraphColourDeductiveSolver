# Literature on the degree-7 case, mapped onto the last binder (Long Table, 20 Oct 2026)

This note is an idea source, not a claim. Nothing in it counts until it is re-expressed as our own column or lemma and
checked by our engines (two engines or Lean). Binder: d7 face row **8666655/5677657** (u = 7; link w0..w6 = 8,6,6,6,6,5,5;
apexes s0..s6 = 5,6,7,7,6,5,7, with s_i the apex across w_i w_{i+1}). Survivors after the census (4770a564):
(a) p41 >= 6, apex 6-9, every free slot >= 7; (b) p41 = 5 and every outer contact of s3 >= 9.

**Sources read (20 Oct, via web fetch; arxiv.org and the GitHub repos could not be cloned from this container).**
- [N26] "The Four Color Theorem with Linearly Many Reducible Configurations and Near-Linear Time Coloring",
  arXiv:2603.24880; code at github.com/near-linear-4ct (discharging-rules, reducible-configurations, computer-checks, MIT).
  Section 8 ("Reducible configurations around low-degree vertices"). The extracted text has no page numbers, so citations
  are by section and lemma only.
- [S10] R. Steinberger, "An unavoidable set of D-reducible configurations", arXiv:0905.0043 (Trans. AMS 2010), Section 4.
  The rule drawings (Fig. 8) and the degree-7 case table (Fig. 15) are images and were not readable. So the individual
  7-to-7 rule shapes are **not** stated below; only what the prose says.

## 1. [N26] Lemmas 8.4-8.7: what they say and how they are proved

**First, a correction to the owner's point 5.** In [N26], plain unavoidability (Theorem 4.5: a vertex with positive final
charge has a D_0 configuration in its cartwheel) is Steinberger's result with the same rules, and **it does not use
Section 8**. Lemmas 8.x serve the *linear-count* strengthening (Theorem 6.5 (ii)-(iii), feeding Theorem 3.3). They concern
"flat" vertices, final charge 0 and all degrees <= 7 or <= 8 in a large ball, and they find a reducible configuration
there anyway. Configuration X is not a leftover of the 4CT discharging. It is an exception inside Lemma 8.3(iii), about
whether a flat region contains a reducible configuration. The *pattern* still transfers: one non-reducible exception, killed
by showing it forces a nearby vertex that completes a reducible configuration.

Setup: T_0(v) = 10(6 - d(v)), 84 rules (R1-R43 plus mirrors; Steinberger's set with his rules 12 and 13 split).
Configurations in D have at most 19 vertices and ring size <= 18.

| Lemma | Statement (quoted fragments) | Proof |
|---|---|---|
| 8.3 (context) | V_0 is (i) two adjacent 8s, (ii) an 8 next to a 7 with all other neighbours <= 6, or (iii) "a path of length exactly two with vertex degrees 7, 8, 7". Conclusion holds "except for a single special case within (iii)", where v is the centre of X (Fig. 13: "not reducible, but it is so special that it will help us in other ways") | computer: cartwheel enumeration (Section 11), unions of cartwheels (Section 9), D-check (Alg. A.1.1) |
| 8.4 | "Let v be a degree-8 vertex in G. If every vertex in B_3(v) has final charge 0" and "all vertices in B_5(v) have degree at most 8, then B_5(v) contains a separating 3- or 4-cycle or a reducible configuration in D" | by hand from 8.3. If B_2(v) has no X, apply 8.3 at v. Otherwise apply 8.3 at the degree-8 vertex v' of X at distance 2. X must be centred at v' too, so v' has two 5-neighbours between its 7-neighbours. This forces a degree-5 w beside X, and X + w is D-reducible (Fig. 14) |
| 8.5 | "Suppose G has a T_{7^3} with vertices v1v2v3, all of which have final charge 0. If all vertices in B have degree at most 7, then B has a separating 3- or 4-cycle or a reducible configuration in D", with B = union of B_2(v_i) and T_{7^3} a facial triangle of three 7s | computer: enumerate flat degree-7 cartwheels, glue the three over B, test against D; one case needs the radius-3 configuration of Fig. 5. "Sketch of computer-assisted proof", no case count given |
| 8.6 | "Let v be a degree-7 vertex and suppose that all vertices in B_3(v) have degree at most 7. Then B = union over u in V_0 of B_2(u) contains a separating 3- or 4-cycle or a reducible configuration from D or a T_{7^3}" | computer, "similar to Lemma 8.3" (same enumerate, glue, check) |
| 8.7 | "Let v be a degree-7 vertex in G. If every vertex in B_3(v) has final charge 0 and all vertices in B_5(v) have degrees of at most 7, then B_5(v) contains a separating 3- or 4-cycle or a reducible configuration in D" | by hand: no T_{7^3} in B_3(v) gives 8.6; otherwise 8.5 |

All of [N26]'s checks run "within a couple of hours" on 256 cores. Degree caps: 8.5-8.7 need **every** degree <= 7 in the
ball, and 8.4 needs <= 8. Our binder has an 8 (w0), and survivor (b) has 9+ vertices. **None of 8.4-8.7 applies to our
binder as stated.** What carries over is the method: glue cartwheels of neighbouring flat 7s and test the union.

## 2. [S10] Second-stage rules and the 1/2 bound

- Charge 6 - d(v) (sum 12; our §1 scale is the same: a five carries 1, 1 RSST unit = 0.1). Amounts are 1/10 or 1/5.
  "the discharging procedure is two-staged: in the first stage charge is removed from minor vertices". Stage 1 is Mayer's
  first seven rules (5s and 6s pay majors). Then "the overcharged vertices are those of degree 7 and 8", and stage 2 moves
  charge among majors.
- A rule is a tuple (q, G(L), s, t, gamma-, gamma+). Source s and sink t are adjacent, and every vertex of G(L) is "at
  distance at most two" from both s and t. Non-internal vertices carry degree ranges. Rules may have "both a source and a
  sink of degree 7", which lets "a few simple rules ... combine among themselves to achieve an overall complex effect".
  Rules 39-42 have a degree-8 source and an unbounded sink. Exact 7->7 and 8->7 shapes are in Fig. 8 (not read).
- **Lemma 4.4:** "Let u, v be adjacent vertices of an internally 6-connected triangulation T, where v has degree at least
  8. Then r(u, v) <= 1/2 if no members of U_2822 appear in T." Use: a vertex of degree >= 12 cannot be overcharged, since
  6 - d + d/2 <= 0 for d >= 12. Proof by hand. The degree-7 case is "the lengthiest case, as there are the most rules
  with source of degree 7": Fig. 15 lists which rules can co-occur, crosses out pairs that complete a Fig. 14
  configuration (all in U_2822), and concludes "at most 5 rules can appear simultaneously", so 5 x 1/10 = 1/2.
  Degree 8: only rules 39-42, "only 5 rules can appear".
- The cartwheel proof for hubs 5-11 runs on RSST's program with machine-readable presentations, and the verbose output
  exceeds 13,000,000 lines.

## 3. Mapping onto survivors (a) and (b), with proposals in our family

Charge picture (our convention: bigs absorb inflow up to d - 6 + t). u takes the fives w5 and w6 directly and 6-relayed
charge from w1-w4. Its only big link neighbour is w0 = 8, and `l3q` (7 -> big link neighbour) already pays u -> w0. u has
**no 7-neighbour**: its 7s s2, s3 and s6 are at distance 2. So a Steinberger 7->7 rule cannot start at u. The 7->7 / 8->7
direction helps only as a **second hop** out of w0, or as a choice made by the 6s and fives about which 7 they feed.

### (a) all free slots >= 7: open l3q's U = 8, V = 7 subfamily (8 -> 7, Steinberger stage 2)

In (a), w0's link is (u 7, w1 6, s0 5, p0a, p0b, p0c, s6 7, w6 5) with p0* >= 7, and s6 (7) touches only w6, s5 (fives),
w0 and four privates >= 7. So s6 has outlets and little inflow. The first l3q family fixed U = 7 and c, a in {5,6}. That
excludes w0 -> s6, and every key with a big letter.
- **Column (own family, l3q full keys, BORROWED-CHANNEL-7FACE §q):** payer w0 (U = 8), payee s6 (V = 7), sent per side.
  The w6 side has key (8,7,5,7,6), meaning c = w6, a = u, a2 = w1. The far side has (8,7,c,a,a2) with c, a, a2 in {7,8,9}.
  The payer reads its own link exactly. Payee s6 reads (U,V,c,a) exactly and gets a2 through the §14′ private mask.
  About 2 x 3^3 + 1 new keys for this row. Open the whole U = 8, V = 7, letters 5..9 block for pricing.
- **Guard from [S10] Lemma 4.4:** for every v with deg >= 8, the sum of q over one edge (u, v) is at most 1/2. Add this as an
  LP row family. It cannot raise the bound by more than the dual on it, and it makes d >= 12 receivers safe by counting.
  That cross-checks the receiver DP (d = 18..30) independently.
- **Hypothesis H-L8:** on the current stacked cert, at least one q(8,7,·) column prices negative, and it sits on the
  w0 row of 8666655/5677657. **Kill line:** every q(8,7,·) has rc >= 0; or the solve gains < 0.002; or the binder moves to
  s6's row (s6 becomes tight) with gain < 0.002. **Controls:** mask off gives 0, side swap, U = 7 subfamily unchanged.
  Engines: Opus prices, and Studio rebuilds the U = 8 mask table spec-only.

### (b) p41 = 5, s3's outer contacts all >= 9: a sink-aware 6 -> 7 choice (owner's point 3), else a targeted lemma

In (b), w4 (6) has link (u 7, w3 6, s3 7, p41 5, s4 6, w5 5). It touches two fives and two 7s, u and s3. Whatever w4
relays, it can send to u or to s3. s3's onward outlet already exists: s3 -> 9 has l3q key (7,9,5,6,6) (c = p41, a = w4,
a2 = w3), inside the first family. The missing piece is **visibility**. Our 6-relays key on the payer's link and apex
classes, so w4 cannot see that s3's outer contacts are >= 9. In [S10] and RSST every rule vertex lies within distance 2 of
both s and t, and s3's outer contacts are at distance <= 2 from w4. So this is a template limit, not a floor.
- **Column (own family):** a 6 -> 7 relay keyed on (payer's exact link, payee's outer-contact class vector, capped at
  9). It pays only when the payee 7 has all outer contacts >= 9, written `r67o[L, s, h]` with h in {<=8, all>=9}.
  Payee credit is exact, because the payee reads its own link. The payer row splits cons2 6-types by h, two classes per
  big link neighbour. The extra 6-types are the whole cost. Check the s25c "t >= 7 -> s3" column first: if that column
  already prices this route, the new one is redundant.
- **Hypothesis H-R67:** the r67o composite (w4 -> s3 at h = all>=9, then s3 -> 9 via l3q) has rc < 0 on the stacked cert.
  **Kill line:** rc >= 0; or the gain is < 0.002; or the type split raises cons2 rows by more than 2x without a gain.
- **Fallback, an [N26]-8.4-shaped targeted lemma (only if H-R67 dies):** "If 8666655/5677657 occurs with p41 = 5 and every
  outer contact of s3 >= 9, then B_3(u) contains a configuration of our registry, or one of s3's 9+ contacts has slack
  >= sigma under the current rules." Engines would need (i) the ring <= 16 windows that join s3's 9+ contacts with
  p41's other neighbours, as D/C on dfast + cfast with second-engine agreement, then Lean; and (ii) for the slack branch, a
  receiverR2 evaluation of a 9 whose link contains s3 = 7, w4 = 6, p41 = 5, run exhaustively over the 9's other letters.
  Kill line: some filling has neither a kill nor slack >= sigma at the sigma that the cert needs.

### What is not supported

- Taking [N26]'s 8,202 configurations as ready-made kills for this row. They are a search map at most (point 1 is the
  coordinator's call). None of 8.4-8.7 is a kill for our row, because of the degree caps.
- Expecting ring 17-18 to close (a) on its own. Our all->= 7 fillings had no window to ring 16, and the drawing thread saw
  survivors to ring 17. [N26] closes 7s by gluing cartwheels of flat neighbours, not by bigger rings around one hub.

**Order:** H-L8 pricing (minutes), then H-R67 pricing, then the 1/2 guard as a cross-check row, then the lemma fallback.
