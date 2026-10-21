# LP export for the interpretable-route thread (Opus, 21 Oct 2026)

- `lp_weights.csv`: solve, path, t, family, key, weight. One row per nonzero column, from all 152 `sol_*.json` under P_own_lp. List-valued keys are joined digit by digit; the letter 0 means "small/other" where the spec says so.
- `binders_all.csv`: the receiver rows that bind each round's dual certificate (dual weight, receiver degree d, link word, second-ring word, canonical key).
- The newest and best solve is `s53/run_A97/sol_q53A97.json`, t = 0.098789 (upper FEASIBLE on A97).

Keys (full detail in `RELAY_SPEC.md` §2 and §12.2):
- **y `D|abcd`:** a 5 sends this to a big neighbour of degree D (7, 8, or 9 meaning >= 9). abcd is the 5's link word read from that big, with reflections identified.
- **g `w1 H F H w2` (5 digits):** 5 -> 6. These are the six's letters around the five; 0/1 are hat/apex classes.
- **h (8 digits):** 6 -> big. The first digit is the big's degree, then the six's link word with apexes.
- **x `tau`:** big -> big. tau = (((fl-2)*3 + (tl-2))*125 + min(s1,s2))*125 + max(s1,s2), where fl, tl are the indices of {7, 8, >=9} and s1, s2 are the side triples (c, a, b) in base 5 over letters 5..9. Capped at 3.
- **r:** relay columns.
- **lq / lQ:** l3q (RSST rule 9) payee masks.
- **yT, tau, xo:** older or parked families.

Charge model: initial charge is 6 - deg. A solution is valid if every 5 ends <= t and every big ends <= 0 in every admissible neighbourhood. t <= 0 would prove the four colour theorem, given reducibility.
