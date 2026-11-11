import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDRS403V00
import HDRS403V01
import HDRS403V02
import HDRS403V03
import HDRS403V04
import HDRS403V05
import HDRS403V06
import HDRS403V07
import HDRS403V08
import HDRS403V09
import HDRS403V10
import HDRS403V11
import HDRS403V12
import HDRS403V13
import HDRS403V14
import HDRS403V15
import HDRS403V16
import HDRS403V17
import HDRS403V18
import HDRS403V19
import HDRS403V20
import HDRS403V21
import HDRS403V22
import HDRS403V23
import HDRS403V24
import HDRS403V25
import HDRS403V26
import HDRS403V27
import HDRS403V28
import HDRS403V29
import HDRS403V30
import HDRS403V31
import HDRS403V32
import HDRS403V33
import HDRS403V34
import HDRS403V35
import HDRS403V36
import HDRS403V37
import HDRS403V38
import HDRS403V39
import HDRS403V40
import HDRS403V41
import HDRS403V42
import HDRS403V43
import HDRS403V44
import HDRS403V45
import HDRS403V46
import HDRS403V47
import HDRS403V48
import HDRS403V49
import HDRS403V50
import HDRS403V51
import HDRS403V52
import HDRS403V53
import HDRS403V54
import HDRS403V55
import HDRS403V56
import HDRS403V57
import HDRS403V58
import HDRS403V59
import HDRS403V60
import HDRS403V61
import HDRS403V62
import HDRS403V63
import HDRS403V64
import HDRS403V65
import HDRS403V66
import HDRS403V67
import HDRS403V68
import HDRS403V69
import HDRS403V70
import HDRS403V71
import HDRS403V72
import HDRS403V73
import HDRS403V74
import HDRS403V75
import HDRS403V76
import HDRS403V77
import HDRS403V78
import HDRS403V79
import HDRS403V80
import HDRS403V81
import HDRS403V82
import HDRS403V83
import HDRS403V84
import HDRS403V85
import HDRS403V86
import HDRS403V87
import HDRS403V88
import HDRS403V89
import HDRS403V90
import HDRS403V91
import HDRS403V92
import HDRS403V93
import HDRS403V94
import HDRS403V95
import HDRS403V96
import HDRS403V97
import HDRS403V98
import HDRS403V99
import HDRS403V100
import HDRS403V101
import HDRS403V102
import HDRS403V103
import HDRS403V104
import HDRS403V105
import HDRS403V106
import HDRS403V107
import HDRS403V108
import HDRS403V109
import HDRS403V110
import HDRS403V111
import HDRS403V112
import HDRS403V113
import HDRS403V114
import HDRS403V115
import HDRS403V116
import HDRS403V117
import HDRS403V118
import HDRS403V119
import HDRS403V120
import HDRS403V121
import HDRS403V122
import HDRS403V123
import HDRS403V124
import HDRS403V125
import HDRS403V126
import HDRS403V127
import HDRS403V128
import HDRS403V129
import HDRS403V130
import HDRS403V131
import HDRS403V132
import HDRS403V133
import HDRS403V134
import HDRS403V135
import HDRS403V136
import HDRS403V137
import HDRS403V138
import HDRS403V139
import HDRS403V140
import HDRS403V141
import HDRS403V142
import HDRS403V143
import HDRS403V144
import HDRS403V145
import HDRS403V146
import HDRS403V147
import HDRS403V148
import HDRS403V149
import HDRS403V150
import HDRS403V151
import HDRS403V152
import HDRS403V153
import HDRS403V154
import HDRS403V155
import HDRS403V156
import HDRS403V157
import HDRS403V158
import HDRS403V159
import HDRS403V160
import HDRS403V161
import HDRS403V162
import HDRS403V163
import HDRS403V164
import HDRS403V165
import HDRS403V166
import HDRS403V167
import HDRS403V168
import HDRS403V169
import HDRS403V170
import HDRS403V171
import HDRS403V172
import HDRS403V173
import HDRS403V174
import HDRS403V175
import HDRS403V176
import HDRS403V177
import HDRS403V178
import HDRS403V179
import HDRS403V180
import HDRS403V181
import HDRS403V182
import HDRS403V183
import HDRS403V184
import HDRS403V185
import HDRS403V186
import HDRS403V187
import HDRS403V188
import HDRS403V189
import HDRS403V190
import HDRS403V191
import HDRS403V192
import HDRS403V193
import HDRS403V194
import HDRS403V195
import HDRS403V196
import HDRS403V197
open HDRS403 DCheck18
namespace HDRS403V
theorem hD_all (k : Fin 198) : DCheck18.dReducible (hdrs403Confs.get (k.cast hdrs403Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
  · exact hD_1
  · exact hD_2
  · exact hD_3
  · exact hD_4
  · exact hD_5
  · exact hD_6
  · exact hD_7
  · exact hD_8
  · exact hD_9
  · exact hD_10
  · exact hD_11
  · exact hD_12
  · exact hD_13
  · exact hD_14
  · exact hD_15
  · exact hD_16
  · exact hD_17
  · exact hD_18
  · exact hD_19
  · exact hD_20
  · exact hD_21
  · exact hD_22
  · exact hD_23
  · exact hD_24
  · exact hD_25
  · exact hD_26
  · exact hD_27
  · exact hD_28
  · exact hD_29
  · exact hD_30
  · exact hD_31
  · exact hD_32
  · exact hD_33
  · exact hD_34
  · exact hD_35
  · exact hD_36
  · exact hD_37
  · exact hD_38
  · exact hD_39
  · exact hD_40
  · exact hD_41
  · exact hD_42
  · exact hD_43
  · exact hD_44
  · exact hD_45
  · exact hD_46
  · exact hD_47
  · exact hD_48
  · exact hD_49
  · exact hD_50
  · exact hD_51
  · exact hD_52
  · exact hD_53
  · exact hD_54
  · exact hD_55
  · exact hD_56
  · exact hD_57
  · exact hD_58
  · exact hD_59
  · exact hD_60
  · exact hD_61
  · exact hD_62
  · exact hD_63
  · exact hD_64
  · exact hD_65
  · exact hD_66
  · exact hD_67
  · exact hD_68
  · exact hD_69
  · exact hD_70
  · exact hD_71
  · exact hD_72
  · exact hD_73
  · exact hD_74
  · exact hD_75
  · exact hD_76
  · exact hD_77
  · exact hD_78
  · exact hD_79
  · exact hD_80
  · exact hD_81
  · exact hD_82
  · exact hD_83
  · exact hD_84
  · exact hD_85
  · exact hD_86
  · exact hD_87
  · exact hD_88
  · exact hD_89
  · exact hD_90
  · exact hD_91
  · exact hD_92
  · exact hD_93
  · exact hD_94
  · exact hD_95
  · exact hD_96
  · exact hD_97
  · exact hD_98
  · exact hD_99
  · exact hD_100
  · exact hD_101
  · exact hD_102
  · exact hD_103
  · exact hD_104
  · exact hD_105
  · exact hD_106
  · exact hD_107
  · exact hD_108
  · exact hD_109
  · exact hD_110
  · exact hD_111
  · exact hD_112
  · exact hD_113
  · exact hD_114
  · exact hD_115
  · exact hD_116
  · exact hD_117
  · exact hD_118
  · exact hD_119
  · exact hD_120
  · exact hD_121
  · exact hD_122
  · exact hD_123
  · exact hD_124
  · exact hD_125
  · exact hD_126
  · exact hD_127
  · exact hD_128
  · exact hD_129
  · exact hD_130
  · exact hD_131
  · exact hD_132
  · exact hD_133
  · exact hD_134
  · exact hD_135
  · exact hD_136
  · exact hD_137
  · exact hD_138
  · exact hD_139
  · exact hD_140
  · exact hD_141
  · exact hD_142
  · exact hD_143
  · exact hD_144
  · exact hD_145
  · exact hD_146
  · exact hD_147
  · exact hD_148
  · exact hD_149
  · exact hD_150
  · exact hD_151
  · exact hD_152
  · exact hD_153
  · exact hD_154
  · exact hD_155
  · exact hD_156
  · exact hD_157
  · exact hD_158
  · exact hD_159
  · exact hD_160
  · exact hD_161
  · exact hD_162
  · exact hD_163
  · exact hD_164
  · exact hD_165
  · exact hD_166
  · exact hD_167
  · exact hD_168
  · exact hD_169
  · exact hD_170
  · exact hD_171
  · exact hD_172
  · exact hD_173
  · exact hD_174
  · exact hD_175
  · exact hD_176
  · exact hD_177
  · exact hD_178
  · exact hD_179
  · exact hD_180
  · exact hD_181
  · exact hD_182
  · exact hD_183
  · exact hD_184
  · exact hD_185
  · exact hD_186
  · exact hD_187
  · exact hD_188
  · exact hD_189
  · exact hD_190
  · exact hD_191
  · exact hD_192
  · exact hD_193
  · exact hD_194
  · exact hD_195
  · exact hD_196
  · exact hD_197
end HDRS403V
#print axioms HDRS403V.hD_all
