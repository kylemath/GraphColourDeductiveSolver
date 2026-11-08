# HCK3k (Studio, 8 Nov): Lean hC for the K3k C kill (1 entry, exactly like HCK3j)
- Kill: f8_...56556_.....66. r=12 m=8 X={I0-I3} (pat_K3g2_C.cfast 6f6dce95, window b8_u...56556_.....66.). It is in our K3CHK7 set:
  per_config.tsv row "b8_u...56556_.....66. C I0-I3 12 8 ... CK3C7 ok/admissibleX/foldSafeX, rim-pinned no, PASS" (engines reused from K3CHK5: kc -x + cfast --fixed).
- CK3K.lean: CK3J.lean with the entry replaced by CK3C7's literal for b8_u...56556_.....66. verbatim (same cf, eqR [], eqI [(3,0)], lbl, X I0-I3);
  XRData.ok, admissibleX, foldSafeX by native_decide. Not rim-pinned (X = I0-I3 interior).
- K3KV00 (hC_0 : cReducible18 …), K3KVAll (hC_all, Fin 1). extraC.tsv = our K3CHK7 kc line. Build root out_hck3k.
