# The letter 9 in an f-name (Studio rule; Long Table ruling 19 Oct 09:00Z)

**Rule. A '9' in the link or s word of an e/f-name means an interior vertex of degree exactly 9.** It does not mean
>= 9. No letter above 9 can occur: names carry one digit per slot, and explore's rows only use 5..9.

## Why this reading, not >= 9 (it is forced by the engines)
- Explore's window cutter (loop/k47/win45.py, same as earlier rounds) cuts a window as a connected set X of the
  receiver's fixed vertices (u, w_i, s_i).
  - Each vertex of X is an interior vertex at its *exact* letter: `build` gives a lettered vertex exactly that many
    neighbours, and `extract` asserts `len(adj[x]) == deg[x]`.
  - A row letter 9 is therefore built as a vertex of degree exactly 9.
- The window is written as a kc line (interior adjacency + ring adjacency). Every vertex's degree is its adjacency
  count. kc, dfast and cfast all read that same line, so each D or C verdict is about the configuration with that
  vertex at degree exactly 9. None of them has a ">= 9" notion. (kc's source was not read, per standing rule; the
  statement is about its input format, which all three engines share.)
- A kill proved at degree 9 says nothing about degree 10, 11, .... So reading 9 as >= 9 would be unsound.

## What it means for the LP registry
- The LP alphabet's letter 9 means degree >= 9. A pattern with an exact-9 slot at a link or s position matches no LP
  letter, so it can never forbid an LP arrangement. It is sound but unmatchable.
- Such names are excluded from the k3x registry at admission, with a log line. They are recorded, not dropped
  silently.
- To be useful to the LP, the window must be re-cut with that vertex on the ring rather than in the interior. A ring
  vertex's degree is free, so the configuration is valid for every degree >= 9.
- Exception, already sound: a 9 only at the centre u of a d = 9 window (an f9_ name) is exact. f9_ patterns apply to
  receivers of exact degree 9, since d = 7..15 are exact in the LP. Studio's LP parser reads these as before.
- Relation to the section 14' kill tables: there a fixed letter-9 vertex never matches a configuration vertex (9 =
  >= 9, never exact). That is the same convention seen from the other side: an exact-degree configuration vertex may
  not land on an LP letter 9.

## Implementation (frozen tools untouched)
- out/job31/letter9.py: `parse9` (the name's frame, with 9 = exactly 9) and `lp_reading` ('lp' / 'unmatchable').
- wlp3.py's parse / fullparse are frozen for Job 31 and unchanged. On a link/s 9 they raise (AssertionError / KeyError)
  rather than misread. Admission calls lp_reading first, so a name with a link/s 9 never reaches them.

## Test (out/job31/letter9_test.py -> letter9_test.out, md5 fd1175241aa2e7780bf4ba9be8d8e9a3)
- 7 rows: explore's next row d=9 655665556/666559575, the r9f binder 765556565/566956665, and 5 synthetic rows with 9s
  in the link and in the s word.
- 823 windows (ring <= 12, interior <= 7) whose interior holds a 9-lettered vertex, cut with win45's own build /
  extract.
- Name frame (parse9) vs the kc line's frame (degrees as grow.kcline reads the line the engines take): **823 / 823
  equal**, with every 9 at kc degree exactly 9.
- LP side: 642 windows have their only 9 at u (d = 9): the LP parser reads them and lp_reading says 'lp'. 181 windows
  have a link/s 9: the LP parser refuses them and lp_reading says 'unmatchable'. 0 disagreements.
