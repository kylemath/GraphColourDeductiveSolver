import RS403V00
import RS403V01
import RS403V02
import RS403V03
import RS403V04
import RS403V05
import RS403V06
import RS403V07
import RS403V08
import RS403V09
import RS403V10
import RS403V11
import RS403V12
import RS403V13
import RS403V14
import RS403V15
import RS403V16
import RS403V17
import RS403V18
import RS403V19
import RS403V20
import RS403V21
import RS403V22
import RS403V23
import RS403V24
import RS403V25
import RS403V26
import RS403V27
import RS403V28
import RS403V29
import RS403V30
import RS403V31
import RS403V32
import RS403V33
import RS403V34
import RS403V35
import RS403V36
import RS403V37
import RS403V38
import RS403V39
import RS403V40
import RS403V41
import RS403V42
import RS403V43
import RS403V44
import RS403V45
import RS403V46
import RS403V47
import RS403V48
import RS403V49
import RS403V50
import RS403V51
import RS403V52
import RS403V53
import RS403V54
import RS403V55
import RS403V56
import RS403V57
import RS403V58
import RS403V59
import RS403V60
import RS403V61
import RS403V62
import RS403V63
import RS403V64
import RS403V65
import RS403V66
import RS403V67
import RS403V68
import RS403V69
import RS403V70
import RS403V71
import RS403V72
import RS403V73
import RS403V74
import RS403V75
import RS403V76
import RS403V77
import RS403V78
import RS403V79
import RS403V80
import RS403V81
import RS403V82
import RS403V83
import RS403V84
import RS403V85
import RS403V86
import RS403V87
import RS403V88
import RS403V89
import RS403V90
import RS403V91
import RS403V92
import RS403V93
import RS403V94
import RS403V95
import RS403V96
import RS403V97
import RS403V98
import RS403V99
import RS403V100
import RS403V101
import RS403V102
import RS403V103
import RS403V104
import RS403V105
import RS403V106
import RS403V107
import RS403V108
import RS403V109
import RS403V110
import RS403V111
import RS403V112
import RS403V113
import RS403V114
import RS403V115
import RS403V116
import RS403V117
import RS403V118
import RS403V119
import RS403V120
import RS403V121
import RS403V122
import RS403V123
import RS403V124
import RS403V125
import RS403V126
import RS403V127
import RS403V128
import RS403V129
import RS403V130
import RS403V131
import RS403V132
import RS403V133
import RS403V134
import RS403V135
import RS403V136
import RS403V137
import RS403V138
import RS403V139
import RS403V140
import RS403V141
import RS403V142
import RS403V143
import RS403V144
import RS403V145
import RS403V146
import RS403V147
import RS403V148
import RS403V149
import RS403V150
import RS403V151
import RS403V152
import RS403V153
import RS403V154
import RS403V155
import RS403V156
import RS403V157
import RS403V158
import RS403V159
import RS403V160
import RS403V161
import RS403V162
import RS403V163
import RS403V164
import RS403V165
import RS403V166
import RS403V167
import RS403V168
import RS403V169
import RS403V170
import RS403V171
import RS403V172
import RS403V173
import RS403V174
import RS403V175
import RS403V176
import RS403V177
import RS403V178
import RS403V179
import RS403V180
import RS403V181
import RS403V182
import RS403V183
import RS403V184
import RS403V185
import RS403V186
import RS403V187
import RS403V188
import RS403V189
import RS403V190
import RS403V191
import RS403V192
import RS403V193
import RS403V194
import RS403V195
import RS403V196
import RS403V197
import RS403V198
import RS403V199
import RS403V200
import RS403V201
import RS403V202
import RS403V203
import RS403V204
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace RS403V
theorem hC_all (k : Fin 205) : cReducible18 (rs403Entries.get (k.cast rs403Entries_length.symm)).cf
    (rs403Entries.get (k.cast rs403Entries_length.symm)).eqR (rs403Entries.get (k.cast rs403Entries_length.symm)).eqI = true := by
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
  · exact hC_96
  · exact hC_97
  · exact hC_98
  · exact hC_99
  · exact hC_100
  · exact hC_101
  · exact hC_102
  · exact hC_103
  · exact hC_104
  · exact hC_105
  · exact hC_106
  · exact hC_107
  · exact hC_108
  · exact hC_109
  · exact hC_110
  · exact hC_111
  · exact hC_112
  · exact hC_113
  · exact hC_114
  · exact hC_115
  · exact hC_116
  · exact hC_117
  · exact hC_118
  · exact hC_119
  · exact hC_120
  · exact hC_121
  · exact hC_122
  · exact hC_123
  · exact hC_124
  · exact hC_125
  · exact hC_126
  · exact hC_127
  · exact hC_128
  · exact hC_129
  · exact hC_130
  · exact hC_131
  · exact hC_132
  · exact hC_133
  · exact hC_134
  · exact hC_135
  · exact hC_136
  · exact hC_137
  · exact hC_138
  · exact hC_139
  · exact hC_140
  · exact hC_141
  · exact hC_142
  · exact hC_143
  · exact hC_144
  · exact hC_145
  · exact hC_146
  · exact hC_147
  · exact hC_148
  · exact hC_149
  · exact hC_150
  · exact hC_151
  · exact hC_152
  · exact hC_153
  · exact hC_154
  · exact hC_155
  · exact hC_156
  · exact hC_157
  · exact hC_158
  · exact hC_159
  · exact hC_160
  · exact hC_161
  · exact hC_162
  · exact hC_163
  · exact hC_164
  · exact hC_165
  · exact hC_166
  · exact hC_167
  · exact hC_168
  · exact hC_169
  · exact hC_170
  · exact hC_171
  · exact hC_172
  · exact hC_173
  · exact hC_174
  · exact hC_175
  · exact hC_176
  · exact hC_177
  · exact hC_178
  · exact hC_179
  · exact hC_180
  · exact hC_181
  · exact hC_182
  · exact hC_183
  · exact hC_184
  · exact hC_185
  · exact hC_186
  · exact hC_187
  · exact hC_188
  · exact hC_189
  · exact hC_190
  · exact hC_191
  · exact hC_192
  · exact hC_193
  · exact hC_194
  · exact hC_195
  · exact hC_196
  · exact hC_197
  · exact hC_198
  · exact hC_199
  · exact hC_200
  · exact hC_201
  · exact hC_202
  · exact hC_203
  · exact hC_204
end RS403V
#print axioms RS403V.hC_all
