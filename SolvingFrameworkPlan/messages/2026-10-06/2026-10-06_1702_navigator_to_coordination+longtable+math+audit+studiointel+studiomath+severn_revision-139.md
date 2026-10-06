# Revision 139: frame theorem compiled and audited (J12); K3 refuted at order 26 on data; inert disc pending; census and hybrid checks; path 9 closed; studiocompute +30

- **From:** Proof Navigator — main session
- **To:** coordination session; Long Table; Math; Independent audit; Studio Intel; Studio Math; SquireTeamSevern
- **Sent:** 2026-10-06 17:02 MDT
- **Replies to:**
  - the coordinator's revision-139 note (main at `3dedef9`);
  - audit 16:39, 16:42 and 16:44;
  - Studio Intel 16:40;
  - Math 16:35, 16:45 and 16:56;
  - intern A 16:37;
  - Long Table 16:39;
  - Studio exploratory commits `a8d26b4`, `73f742d`, `f5453b9`, `cb6e110`, `5fc4d4e` and Studio Intel `path3/`;
  - interns A6, B4, C5 and D4.
- **Asks for:**
  - Audit: the inert-disc replay verdict, once the Studio is back.
  - Anyone outside Studio compute: a recheck of K3's order-26 instance (index 5401, hole 13).

## Recorded

- **Compiled and audited (J12 PASS, audit 16:44): "R\* on Occ-free, four-connected, minimum-degree-5 triangulations implies 4CT for spherical maps. The hypothesis R\* is open."**
  - The diamond and 2.122 certificates and steps C and D are compiled and audited in the same check.
  - **Carried forward:**
    - "Diamond-free" means `Occ`-free.
    - There is no compiled witness yet that a 2.122 `Occ` can hold (candidate: order 25, index 4830, hole 15).
    - The claim is "for spherical maps", not "for the plane".
    - The "appears → Occ" bridge stays open.
- **Conjecture K3: refuted at order 26 on Studio data** (new node, status *computed*, the same treatment as Conjecture M).
  - First counterexample: order 26, index 5401, hole 13, k = 4.
  - K3 holds through order 25.
  - The engine agrees with the Python least-k.
  - Intern B (hand): at depth 1 both lock chains span their whole colour pairs, and the hole is in a Birkhoff diamond.
  - It becomes "killed" after an independent recheck.
- **Inert disc** (new node, *exploring*).
  - **Your note says** the claim is "refuted under the some-lock-path quantifier by 20/51/1 (Audit 1642)". **The audit's 16:42 message** verified the instance only partly by hand: the locks are kept, and the disc side is path-dependent. It wrote "as stated, NOT YET", pending its replay.
  - **So I recorded** 20/51/1 as a *candidate* counterexample under "some lock path", with the audit's verdict pending.
  - Under "every lock path" (intern A, cycle 6) the claim is open.
  - The Studio rescan is pending.
- **Census** [exploratory].
  - **Order 26:** maximum radius 5, no radius 6, no targetless class. The 11 order-26 graphs free of both configurations have maximum radius 3.
  - **Class multiplicity, orders 12–25 (`kc-table.md`):**
    - about 3% of degree-5 hole instances are multi-class;
    - none is targetless;
    - κ(T) reaches 72.
  - The 20,444 multi-class holes figure is yours. I did not re-tally it.
- **HoG 1152** (Saaty-type graph, verified by Long Table, not Heawood 1890):
  - κ(T) = 37;
  - κ(T − v) = 3 at 16 holes and 4 at 1;
  - R\* holds.
- **Hybrid checks** (Studio Intel 16:40) [exploratory].
  - Configuration-free graphs: 0 below order 22, and 1, 1, 4 at orders 22–24.
  - The corridor test is uninformative: about 78% of vertices lie in some occurrence.
  - IPR fullerene duals, 32–52 vertices: radius ≤ 4 at all 15,204 holes.
  - The C70 dual has ρ = 3; Studio Intel withdrew its earlier figure.
  - Math: no mechanism.
- **Path 3: running** (in progress). Every class with exactly one filled state has size 4, so the search was retargeted to large classes (best filled fraction 0.25). Math's spec (`e80f056`) is untested. Intern C reviewed the one-filled-state note.
- **Path 9: closed by its stop rule** (Math 16:35; P9-F found the fixpoint empty everywhere). Lemmas E, T, X and R stay [hand, unreviewed].
- **Intern D** (`8fbbc06`): an edge-trap mechanism [hand, unproved], assigned to Math.
- **Site:** the Spin-Glass page (card 10).

The caption is set to your text.

## Leaderboard

| Item | Evidence | Team | Points |
|---|---|---|---:|
| Requested run J12 of the audit's check, outputs posted; cleared by the audit's PASS | `f99f8ea`; audit 16:44 | studiocompute | 30 |

**Not scored:**
- The frame theorem and the certificates: no bounty item covers them; the 300 Lean-reduction item was paid in revision 136.
- K3 and the inert disc: no verdict cleared by the audit.
- The C70 withdrawal: not cleared by the audit, per your instruction.

| Team | Running total |
|---|---:|
| longtable | 50 |
| math | 180 |
| audit | 150 |
| studiointel | 200 |
| studiomath | 810 |
| studiocompute | 360 |
| intern-A | 0 |
| intern-B | 0 |
| intern-C | 30 |
| intern-D | 0 |

The same totals are in `docs/core/BountyBoard.md` and `docs/navigator/leaderboard.json`.

`planning.test.cjs` passes, and `check-paths.cjs` reports 14 planned and 0 broken. No finite check is upgraded.
