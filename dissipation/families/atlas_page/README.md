# Discharging Rule Atlas

Published page: https://claude.ai/artifact/CZnurqSukekcNnbzCaqtyn (private to the owner until shared).
A self-contained copy of the published page is `rule-atlas.html` in this folder: open it in a browser.

## What it shows

One toggle at the top switches the whole page between four proofs, all drawn in the same format:
RSST 1996 / Gonthier's Coq 2005 (the same rules and configurations), Inoue et al. 2026, the outside team's 588
proof, and the outside team's 854 proof.

| Tab | Content |
| --- | --- |
| Rules | Every rule as the picture it reads, with its compact form, plain-English reading, nearest shapes and a "Families" grouping of rules that differ by 1 to 4 node changes |
| Family tree | Nearest-relative tree of all rules with the swap on each branch, and nested clusters at swap sizes 6, 4, 3, 2, 1 |
| Template | Each rule as a hierarchy (payer on top, ring 1, hats, fans), the same rule on the shared 41-position template, and how often each template position carries a condition across the whole proof |
| Who pays whom | Rule-by-rule bipartite graph of sender degree to receiver degree, and the world-average charge moved per adjacent pair |
| Configurations | The reducible configurations of the selected proof, drawn with their rings, contraction sets and coverage by rules |

## Rebuilding it

1. `python3 ../code/build_atlas.py` builds `db/atlas4.json` from the rule files and registries (needs the outside
   team's rule file and the project data; see `../../README.md`).
2. `python3 assemble.py` joins `css.txt`, `body3.html` and `atlas4.json` into `rule-atlas.html`.

Limits: the 2026 proof has no whole-world flow numbers; the 854 proof's flow leaves out its 8 N2 parts; coverage is
shown only for RSST and the 588 proof; the Template grid applies to the three proofs written in the hub language,
not to the free-form 2026 pattern graphs.
