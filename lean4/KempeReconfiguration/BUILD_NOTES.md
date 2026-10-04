# Build notes

Toolchain: `leanprover/lean4:v4.15.0`, installed with `elan toolchain install leanprover/lean4:v4.15.0`.
`lake update` in this directory checks out Mathlib at the revision in `lake-manifest.json`.

On macOS 26 the Mathlib `cache` executable linked by Lean 4.15's `ld64.lld` is killed at startup (`__DATA_CONST segment missing SG_READ_ONLY flag`, signal 134). The working binary was relinked with the system linker:

```
/usr/bin/clang -o .lake/packages/mathlib/.lake/build/bin/cache \
  .lake/packages/mathlib/.lake/build/ir/Cache/*.c.o.export \
  -fuse-ld=/usr/bin/ld -Wl,-segprot,__DATA_CONST,r,rw \
  -L "$HOME/.elan/toolchains/leanprover--lean4---v4.15.0/lib" \
  -L "$HOME/.elan/toolchains/leanprover--lean4---v4.15.0/lib/libc" \
  -L "$HOME/.elan/toolchains/leanprover--lean4---v4.15.0/lib/lean" \
  -lleancpp -lInit -lStd -lLean -lleanrt -lc++ -lLake -lgmp -luv -lSystem
```

Then `.lake/packages/mathlib/.lake/build/bin/cache get` from this directory. Do not rebuild that executable with `lake build mathlib/cache`; Lake will replace it with the binary macOS refuses to run.
