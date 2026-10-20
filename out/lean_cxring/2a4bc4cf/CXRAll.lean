import CXR00
import CXR01
import CXR02
import CXR03
import CXR04
import CXR05
import CXR06
import CXR07
import CXR08
import CXR09
import CXR10
import CXR11
import CXR12
import CXR13
import CXR14
import CXR15
import CXR16
import CXR17
import CXR18
import CXR19
import CXR20
import CXR21
import CXR22
import CXR23
import CXR24
import CXR25
import CXR26
import CXR27
import CXR28
import CXR29
import CXR30
import CXR31
import CXR32
import CXR33
import CXR34
import CXR35
import CXR36
import CXR37
import CXR38
import CXR39
import CXR40
import CXR41
import CXR42
import CXR43
import CXR44
import CXR45
import CXR46
import CXR47
import CXR48
import CXR49
import CXR50
import CXR51
import CXR52
import CXR53
import CXR54
import CXR55
import CXR56
import CXR57
import CXR58
import CXR59
import CXR60
import CXR61
import CXR62
import CXR63
import CXR64
import CXR65
import CXR66
import CXR67
import CXR68
import CXR69
import CXR70
import CXR71
import CXR72
import CXR73
import CXR74
import CXR75
import CXR76
import CXR77
import CXR78
import CXR79
import CXR80
import CXR81
import CXR82
import CXR83
import CXR84
import CXR85
import CXR86
import CXR87
import CXR88
import CXR89
import CXR90
import CXR91
import CXR92
import CXR93
import CXR94
import CXR95
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace CXR
theorem hC_all (k : Fin 96) : cReducible18 (xrEntries.get (k.cast xrEntries_length.symm)).cf
    (xrEntries.get (k.cast xrEntries_length.symm)).eqR (xrEntries.get (k.cast xrEntries_length.symm)).eqI = true := by
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
  · exact hC_27
  · exact hC_28
  · exact hC_29
  · exact hC_30
  · exact hC_31
  · exact hC_32
  · exact hC_33
  · exact hC_34
  · exact hC_35
  · exact hC_36
  · exact hC_37
  · exact hC_38
  · exact hC_39
  · exact hC_40
  · exact hC_41
  · exact hC_42
  · exact hC_43
  · exact hC_44
  · exact hC_45
  · exact hC_46
  · exact hC_47
  · exact hC_48
  · exact hC_49
  · exact hC_50
  · exact hC_51
  · exact hC_52
  · exact hC_53
  · exact hC_54
  · exact hC_55
  · exact hC_56
  · exact hC_57
  · exact hC_58
  · exact hC_59
  · exact hC_60
  · exact hC_61
  · exact hC_62
  · exact hC_63
  · exact hC_64
  · exact hC_65
  · exact hC_66
  · exact hC_67
  · exact hC_68
  · exact hC_69
  · exact hC_70
  · exact hC_71
  · exact hC_72
  · exact hC_73
  · exact hC_74
  · exact hC_75
  · exact hC_76
  · exact hC_77
  · exact hC_78
  · exact hC_79
  · exact hC_80
  · exact hC_81
  · exact hC_82
  · exact hC_83
  · exact hC_84
  · exact hC_85
  · exact hC_86
  · exact hC_87
  · exact hC_88
  · exact hC_89
  · exact hC_90
  · exact hC_91
  · exact hC_92
  · exact hC_93
  · exact hC_94
  · exact hC_95
/-- every ring-X entry as a fold-safe CEntryF -/
def cxF (k : Fin 96) : CEntryF :=
  (xrEntries.get (k.cast xrEntries_length.symm)).toCEntryF
    (List.all_eq_true.1 xrEntries_ok _ (List.get_mem _ _)) (hC_all k)
end CXR
#print axioms CXR.hC_all
#print axioms CXR.cxF
