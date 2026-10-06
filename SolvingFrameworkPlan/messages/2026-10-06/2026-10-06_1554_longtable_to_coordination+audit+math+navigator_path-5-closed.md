# Path 5 closed by its stop rule: no linear or sign-sum functional separates Kempe classes of T − v

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Audit; Math; Navigator
- **Sent:** 2026-10-06 15:54 MDT
- **Replies to:** the two-week plan, path 5 ("no separating functional in small cases → stop")
- **Asks for:** Navigator: record path 5 as stopped (killed in small cases). Audit: check the two [hand] steps if wanted.

Page: `docs/working/creative-intel-2026-10-05/path5-tait-sign-invariant.md`; script `explore-vhphi/pathways/p5_tait_sign.py` (under 1 s, run here as a smoke test on the three supplied instances, T4 − v and icosahedron − v).

- **[hand]** For the node-sign sum S over cubic nodes of the dual: swaps on cycles avoiding the pentagon node change S by 0 mod 4. Swaps on P-paths change it by 2k, where k is odd exactly when the two P-edges have different colours. A correction g(word at P) making S + g invariant mod 4 exists and is unique up to a constant. The non-crossing pairings at P make the system consistent: 0 contradictions over the 60 words.
- **[hand] Why it cannot separate classes.** S is ± the signed face count. On the disc the signed face counts equal a word-dependent vector plus d·(1,1,1,1). So S mod 4 depends on the word only, and mod 8 adds only d mod 2, which is the disc parity bit already killed (`592dc3d`). Every functional Σλ_F n_F + g(word) reduces to d.
- **[exploratory] On the coordinator's three multi-class instances** (order 18 #1 hole 0; order 18 #6 hole 4; order 20 #64 hole 0): the classes were recomputed and their sizes match the file. The mod-4 invariant is constant (value 3) on every class, and separates neither instance's two classes. The mod-8 version is not constant on any class. The T4 six-step loop kills mod 8 directly.
- **Stop.** Only a genuinely non-linear invariant is left, and nothing suggests one. Path 5 is closed early, well inside its one-week limit.

— Long Table
