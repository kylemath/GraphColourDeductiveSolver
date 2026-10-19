# Held sender-pattern set (NOT in any LP set; waits for RELAY_SPEC section 17)

Source: explore's loop/k51/sender_kills51.txt at 04a8b71c (claude/project-thread-nh6pv2), copied by explicit path
(md5 4cddaf67af95bfc2cbfab3504007614c). There are 14 s5_ windows: 5-centred sender contexts (spec in the file header).
Status: **held**. None of them is in k3x or any LP registry, and twoeng.py holds any name with a centre degree < 7 out
of k3x (out/job30/sender_names_held.log). They will be used only once section 17 defines sender 2-ball containment.

Studio verification (19 Oct ~12:05Z):
- Both engines re-run on the 14 kc lines (sender51_kc.in): kc -j, 14 / 14 D=true (sender51_kc.out); dfast (studio15
  cfast D-closure), 14 / 14 D=true (sender51_dfast.out).
- Frames (check_frames.py, from the file's spec header only; check_frames.out): **14 / 14 consistent, 0 inconsistent.**
  Checked per window:
  - every interior vertex's kc degree equals the digit at its frame slot;
  - the kc interior adjacency equals the spec adjacency between the framed slots (v-w_k, w_k-w_{k+1}, s_k-w_k and
    w_{k+1}, s_{k-1}-s_k iff w_k = 5, f_k-w_k / s_{k-1} / s_k, no others);
  - the frame's slots are exactly the name's lettered slots;
  - the F/N/x markers match the spec.
- No 9 occurs, so the letter-9 rule needs no exclusion.
