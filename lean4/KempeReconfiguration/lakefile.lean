import Lake
open Lake DSL

package KempeReconfiguration where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

@[default_target]
lean_lib KempeReconfiguration where
  -- Sources use the module prefix `KempeReconfiguration.*`, so the package
  -- root is the source directory. The default srcDir name made Lake look for
  -- KempeReconfiguration/KempeReconfiguration.lean.
  srcDir := "."
  globs := #[.one `KempeReconfiguration, .submodules `KempeReconfiguration]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.15.0"
