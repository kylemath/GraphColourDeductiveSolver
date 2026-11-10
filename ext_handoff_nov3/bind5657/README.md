# K-5 bind5657 pack: ring 15-16 windows of the d8 binder class 56576578/55665555 (lead, 10 Nov 2026)

Row: a binding tneg class of sol_k86MK1_in23 (t = 0.014164305, ST-96) that W6r's split-on-tight pilot found binding at
realisation level (3,000 of 120,000 fillings bind; W6r-replay/split_tight/). Unlike the other d8 binders, it was never
kill-screened: 451 of its 2,356 ring <= 16 windows were in earlier packs (all N). Ring <= 14 (865 new windows) runs in the
container. This pack is the 1,040 new ring 15 (525) and ring 16 (515) windows, 4 batches dealt round-robin from one list
sorted by ring then m.

Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind5657
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb5657.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". Every window covers the whole class, so stop at the
first passing hit and report it.
