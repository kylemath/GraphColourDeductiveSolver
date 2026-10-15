# Job 23 (Studio): one parametrised checker for rings up to 19 [exploratory]

Pre-registration, written 2026-10-15 00:48 MDT before the work.

**Observation.** `DCheck16.lean` and `DCheck18.lean` are copies of `DCheck.lean` (separate namespaces, own `Conf`)
whose only difference is the size of `matchTable`: `Array.range 8 / 9 / 10`, i.e. p ≤ 7 / 8 / 9.

**Plan.**
1. `DCheckT`: `matchTableN N`, `runT mt cf`, `dReducibleT mt cf` (the body of `run` with the table as a parameter).
   Then `DCheck.dReducible = dReducibleT (matchTableN 8)`, and `DCheck16/18.dReducible cf = dReducibleT (matchTableN 9/10) (toConf cf)`.
2. `DCheckRefT`, `DCheckSoundT`, `DCheckS1T`: (S1) and (S2) for an arbitrary table: `run_soundT`, `good_soundT`, `dReducible_soundT`.
3. R1: `check9 : checkP 18 = true` (native_decide), and `matchTableN_complete` for N ≤ 10, p < N.
4. R2: `abstract_matching`, `kempeMatching` and `colorable_of_dReducible` for `matchTableN N` with r ≤ 2N − 1,
   with corollaries for DCheck16 (r ≤ 17) and DCheck18 (r ≤ 19).

**H23.** Steps 1–4 go through with definitional equalities (`rfl`) for the three existing checkers and a mechanical
generalisation of S1, with no change to any proof idea.
**Kill.** `rfl` fails for `DCheck16/18.dReducible` (the copies are not definitionally the parametrised checker),
`checkP 18` is false, or an S1 lemma uses the specific table contents. Report which one.
