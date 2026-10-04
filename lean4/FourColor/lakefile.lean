import Lake
open Lake DSL

package FourColor where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.15.0"

-- Sources live at `lean4/FourColor/Foundation/*.lean` (the paths linked from the
-- navigator), so the library collects the `Foundation.*` modules from the package root.
@[default_target]
lean_lib FourColor where
  srcDir := "."
  globs := #[.submodules `Foundation]
