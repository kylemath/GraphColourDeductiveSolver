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

lean_lib DCheckR12a

lean_lib DCheckR12b

lean_lib DCheckR13a

lean_lib DCheckR13b

lean_lib DCheckR13c

lean_lib DCheckR13d

lean_lib DCheckR14a

lean_lib DCheckR14b

lean_lib DCheckR14c

lean_lib DCheckR14d

lean_lib DCheckR14e

lean_lib DCheckR14f

lean_lib DCheckR14g

lean_lib DCheckR14h

lean_lib DCheckR14i

lean_lib DCheckR14j
