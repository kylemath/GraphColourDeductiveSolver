import Lake
open Lake DSL

package KempeReconfiguration where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

@[default_target]
lean_lib KempeReconfiguration where
  srcDir := "KempeReconfiguration"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.15.0"
