import W3V00
import W3V01
import W3V02
import W3V03
import W3V04
import W3V05
import W3V06
import W3V07
import W3V08
import W3V09
import W3V10
import W3V11
import W3V12
import W3V13
import W3V14
import W3V15
import W3V16
import W3V17
import W3V18
import W3V19
import W3V20
import W3V21
import W3V22
import W3V23
import W3V24
import W3V25
import W3V26
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace W3V
theorem hC_all (k : Fin 27) : cReducible18 (w3Entries.get (k.cast w3Entries_length.symm)).cf
    (w3Entries.get (k.cast w3Entries_length.symm)).eqR (w3Entries.get (k.cast w3Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
  · exact hC_1
  · exact hC_2
  · exact hC_3
  · exact hC_4
  · exact hC_5
  · exact hC_6
  · exact hC_7
  · exact hC_8
  · exact hC_9
  · exact hC_10
  · exact hC_11
  · exact hC_12
  · exact hC_13
  · exact hC_14
  · exact hC_15
  · exact hC_16
  · exact hC_17
  · exact hC_18
  · exact hC_19
  · exact hC_20
  · exact hC_21
  · exact hC_22
  · exact hC_23
  · exact hC_24
  · exact hC_25
  · exact hC_26
end W3V
#print axioms W3V.hC_all
