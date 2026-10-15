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

## Result (15 Oct 2026): H23 survives with one refinement. The ring 16–19 checkers are now under the proved chain.

`./build_r2.sh` does a clean build of everything in about 5 min at nice 10 (`check9` takes about 2.5 min of that).

| file | content |
|---|---|
| `DCheckT` | `matchTableN N`, `runT mt`, `dReducibleT mt`; `dReducible_eq_T : dReducible cf = dReducibleT (matchTableN 8) cf` (`rfl`) |
| `DCheckTEq` | `Conf.of16/of18`; `dReducible16_eq_T`, `dReducible18_eq_T` (N = 9, 10) |
| `DCheckSoundT` | `GoodT`, `KempeMatchingT`, `good_soundT` (S2); `good_eq_T`, `kempeMatching_eq_T` |
| `DCheckRefT`, `DCheckS1T` | (S1) for any table: `run_soundT`, `dReducible_soundT` (mechanical copy of S1; no proof idea changed) |
| `DCheckR1T` | `check9 : checkP 18 = true` (native_decide), `matchTableN_complete` for N ≤ 10, p < N |
| `DCheckR2C/D` | `abstract_matching` and `kempeMatching` for `matchTableN N`, r < 2N; `colorable_of_dReducibleT`; corollaries `colorable_of_dReducible` (r ≤ 15), **`colorable_of_dReducible16` (r ≤ 17)**, **`colorable_of_dReducible18` (r ≤ 19)** |

- **Refinement of H23.** The copies are *not* all `rfl`-equal: `DCheck16/18.ncm` and `.extAux` each compile their own structural recursion. Each takes a short induction (`ncm16_eq'`, `extAux16_eq`, and the same for 18). Everything else is `rfl`.
- **Axioms of `colorable_of_dReducible18`:** propext, Classical.choice, Quot.sound, `DCheck.R1.check4..9` (native_decide).
- **Meaning for studio14c/14d.** Those runs evaluate `DCheck18.run` as a compiled executable (`wheelcheck18`). A `D=true` output is therefore `DCheck18.dReducible cf = true` at native-evaluation trust, the same trust as `native_decide`, and `colorable_of_dReducible18` turns it into reducibility in the project's terms. Two conditions per key: a `ConfigOcc` for the key's 2-ball, and the decidable side conditions (`hsym`, `hloop`).
- Diamond end-to-end check (`DCheckR2Diamond`) rebuilt against the generalised glue: OK.
