import Lake
open Lake DSL

package dcheck

@[default_target]
lean_lib DCheck where
  precompileModules := true

lean_lib DCheckData where
  precompileModules := true

lean_exe dcheck where
  root := `Main

lean_lib DCheckThms

lean_lib DCheckThms11

lean_lib DCheckSound
