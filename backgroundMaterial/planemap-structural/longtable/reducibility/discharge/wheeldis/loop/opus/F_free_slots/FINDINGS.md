# F_free_slots: do the 16 free fillings (s1,s4 >= 6) of the 7/27 binder contain a D-reducible configuration?
Q: For each (s1,s4) in {6,7,8,9+}^2 with all fixed slots at their letters, is there an RSST config or a D-reducible u-centred window (ring <= 19) inside the fixed patch?
Guess (before computing): mostly no; windows that only add s at 6..9 to the 7-centred fan rarely D-reduce at ring <= 17, maybe some 6,6 filling dies at ring 18-19.
Would change the plan: if all 16 die, the row is forbidden under a receiver-2-ball rule class (c), which the rooted-word LP cannot express; if some survive, the binder is a genuine obstruction for any rule reading u's 2-ball.

## Answer (09:25Z): no filling dies. All 16 fillings (s1, s4 >= 6) are RSST-free on the fixed patch. With one more ring (w's private neighbours), every filling still has RSST-free completions: 4,332 to 10,000 of 15,625 [E].

Scope: the lead dropped part (i), the u-centred windows; the explore thread's loop/k34 part C covers them over all 25 fillings. Before the scope change, kc ran on 6 windows at rings 13-14 (win.txt, win_kc.out), all with s1 and s4 absent. All 6 are not D [E]. That part stopped there. freewin.py and drive.py are left in this folder.

### (ii-a) RSST's 633 in the filled patch: u, link, all s, with s1 and s4 at the filling (`rsst16.py`, `rsst16.txt`) [E]
- I used B's rsst_rows.py in relaxed mode: every exact slot may host an interior vertex.
- A 9 is run as exact 9. That allows more than 9+ does, so "free at 9" implies "free at 9+".
- Result: all 16 fillings are RSST-free. This reproduces B's table.

### (ii-b) Patch + one ring: the 6 private neighbours of the non-5 link vertices (`rsst_ext.py`, `rsst_ext.txt`, `rsst_ext_free.py`, `rsst_ext_free.txt`)
- The privates are p1 (w1=6), p2a and p2b (w2=7), p4a and p4b (w4=7), p5 (w5=6). Each sits on the 13-cycle ring 2 (s's plus privates).
- Their letters are free over 5..8 and 9+. Ring-3 vertices are ring vertices of K only.
- I assume generic adjacency: no chords or identifications on rings 1-2 beyond B's 6-connectivity facts [I].

| (s1,s4) | RSST hits (some private letters) | RSST-free private completions / 15625 |
|---|---|---|
| 6,6 | 12 (2.126 r8 C, 122.126 r9 C, 122.368 r10 C, 2.3701166 r12 D, ... ) | 4332 |
| 6,7 / 6,8 / 6,9+ | 13 / 12 / 12 | 5700 each |
| 7,6 / 8,6 / 9+,6 | 9 / 8 / 8 | 7600 each |
| 7,7 7,8 7,9+ 8,7 8,8 8,9+ 9+,7 9+,8 9+,9+ | 2-3 (2.126, 122.126, 2.504980 r13 C) | 10000 each |

- Every hit needs at least one private at letter 5 or 6:
  - 2.126 (the 5566 diamond w0, w1, s0, p1) needs p1 = 5;
  - 122.126 needs p5 = 5;
  - the larger ones need 5s and 6s on p2 and p4.
- Every filling has completions that avoid every hit. Example: all six privates at 7 is RSST-free for all 16 fillings [E, direct check]. Not every mix is free: p1 = p5 = 6 with the other privates at 7 still has a hit in 4 fillings.
- No filling is killed. **So the row is not forbidden even by a receiver-2-ball rule class (c) that reads s1, s4 and the privates, as far as RSST containment goes.**
- Any such class would need class (c), and the current rooted-word LP cannot use it.

### Inference [I]
RSST alone does not remove the binder's free fillings, even after adding a ring. The kills in the extension are 5s and 6s at the privates: diamonds and fans next to the w0/w6 fives. Those privates are again unread by any 5-sender's word. Killing the row would take D/C windows beyond RSST (the explore thread's k34 part C) or a different rule class.
