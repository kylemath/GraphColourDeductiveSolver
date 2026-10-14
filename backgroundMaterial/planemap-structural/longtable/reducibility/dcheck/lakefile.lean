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

lean_exe wheelcheck where
  root := `WheelMain

lean_lib TB_dred_00

lean_lib TB_dred_01

lean_lib TB_dred_02

lean_lib TB_dred_03

lean_lib TB_dred_04

lean_lib TB_dred_05

lean_lib TB_dred_06

lean_lib TB_dred_07

lean_lib TB_dred_08

lean_lib TB_dred_09

lean_lib TB_dred_10

lean_lib TB_dred_11

lean_lib TB_dred_12

lean_lib TB_dred_13

lean_lib TB_t14_5656567658

lean_lib TB_t14_5567566667

lean_lib TB_t14_5665666676

lean_lib TB_t14_5575567658

lean_lib TB_t14_5565685577

lean_lib TB_t14_5575685576

lean_lib TB_t14_5556577667

lean_lib TB_t14_5575675658

lean_lib TB_t14_5656656767

lean_lib TB_t14_5567575568

lean_lib TB_t14_5577576566

lean_lib TB_t14_5566676567

lean_lib TB_t14_5666665667

lean_lib TB_t14_5556566867

lean_lib TB_t14_5565685766

lean_lib TB_t14_5576675666

lean_lib TB_t14_5575666568

lean_lib TB_t14_5565766658

lean_lib TB_t14_5568665576

lean_lib TB_t14_5566657577

lean_lib TB_t15_5557586667

lean_lib TB_t15_5657665677

lean_lib TB_t15_5566766667

lean_lib TB_t15_5557686558

lean_lib TB_t15_5656575858

lean_lib TB_t15_5675667567

lean_lib TB_t15_5568676656

lean_lib TB_t15_5675657568

lean_lib TB_t15_5576565858

lean_lib TB_t15_5558566758

lean_lib TB_t15_5556677667

lean_lib TB_t15_5557656867

lean_lib TB_t15_5666765676

lean_lib TB_t15_5656566777

lean_lib TB_t15_5567567757

lean_lib TB_t15_5558656668

lean_lib TB_t15_5576585667

lean_lib TB_t15_5576667576

lean_lib TB_t15_5565685857

lean_lib TB_t15_5666757666

lean_lib TB_nd10

lean_lib TB_nd11

lean_lib TB_nd12

lean_lib TB_nd13

lean_lib TB_nd14_0

lean_lib TB_nd14_1

lean_lib TB_nd14_2

lean_lib TB_nd14_3

lean_lib TB_nd14_4

lean_lib TB_nd14_5

lean_lib TB_nd14_6

lean_lib TB_nd14_7

lean_lib TB_nd14_8

lean_lib TB_nd14_9

lean_lib TB_nd15_0

lean_lib TB_nd15_1

lean_lib TB_nd15_2

lean_lib TB_nd15_3

lean_lib TB_nd15_4

lean_lib TB_nd15_5

lean_lib TB_nd15_6

lean_lib TB_nd15_7

lean_lib TB_nd15_8

lean_lib TB_nd15_9

lean_lib DCheck16 where
  precompileModules := true

lean_exe wheelcheck16 where
  root := `WheelMain16
