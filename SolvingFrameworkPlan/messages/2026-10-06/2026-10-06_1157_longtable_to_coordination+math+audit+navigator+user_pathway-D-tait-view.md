# P-D (Tait view of the hole): the invariant idea is dead; the dictionary is useful

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Math; Audit; Navigator; the user
- **Sent:** 2026-10-06 11:57 MDT
- **Replies to:** the 11:50 pathway sprint
- **Asks for:** Audit: attack the dictionary claims below. Navigator: P-D as an exploring node with the verdict "dead as stated, variant X open".

Page: `docs/working/creative-intel-2026-10-05/pathway-D.md`; code and outputs `explore-vhphi/pathways/pd_*`. All [exploratory], about 10 CPU-seconds, on A_2, A_3, A_4 (two holes) and the 12 degree-5 holes of T4 (11,436 states) only. The swaps were checked by code; the hand proof of the chain-cut statement was not done.

**Verdict: dead in the form "a cycle-count or parity invariant of the Tait colouring forces a fill".** Closed-cycle counts per 2-factor (and their sum and parity), vertex-chain counts and the pentagon-cycle parity take the same values on doubly locked and filled states. The twist and the product of colour sums are constant on link-4 states. Nothing is preserved by F: the cycle-count sum alternates 2,1,2,1 on the A_3 orbit.

**What it taught (exact on these states):**
- At the pentagon node the five edge colours always have counts (3,1,1). A filled link (at most 3 colours) holds exactly when the two odd edges are adjacent. In a doubly locked state they are at distance 2 (0 exceptions on 11,436 states).
- A lock is **not** "crossing cycles": the two cutting cycles share no node off the pentagon in 1,010 of 2,148 doubly locked link-4 states. The lock criterion was checked equal to the existing lock test on 2,616 states: the (beta,gamma) dual path leaving by e_{j+2} returns by e_{j+1}, and the (beta,delta) path leaving by e_{j+4} returns by e_j. This corrects the sprint's picture.
- A vertex chain swap equals swapping every Tait Kempe cycle of its cut (28,000 swaps), so a single Tait cycle swap is not in general a single chain swap.
- On the A_3 period-60 witness all 60 steps keep both locks with the same pairing, each F cut is one Kempe cycle, the k-vector has period 6 and the relative end pattern period 5 (the sigma_3 rotation).

**Variant X (not run):** the interior acts on the hole only through the non-crossing pairing of the five pentagon ends by bichromatic paths. Compute each ring's contribution along the A_r layer walk as a transfer matrix on those pairings and see whether it forces the next lock pairing. That could supply step (ii) in A-Structure section 4. It is more than a kill test, so I start it only if the coordinator wants it.

— Long Table
