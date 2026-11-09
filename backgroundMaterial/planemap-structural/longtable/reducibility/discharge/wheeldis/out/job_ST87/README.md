# K-5 bind86 pack: ring 15-16 windows of the new ST-86 upper binders (lead, 9 Nov 2026)

Rows: binders of sol_repK1MW_04 (t = 0.015991263, K3l5j + 260 keys, ST-86 tneg list) that no earlier pack or container screen covered:
7 distinct rows (3 d7, 4 d8), 36 labels; rows.txt lists the labels, rows_grouped.txt groups them into rows R1-R7.
(The ST-86 d9 class is the K5m M1 class, dead on family m; the other 20 binder rows were already screened in bind75/bind83.)
Ring <= 14 (82 windows) runs in the container. This pack is ring 15 (870 windows) and ring 16 (1,114), windows from earlier packs and
container screens removed, 8 batches dealt round-robin from one list sorted by ring then m, so every batch does ring 15 first.

Windows from gen3.windows on each row's realised 2-ball picture (rotation-correct by construction; 9+ never inside).
Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind86
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb86.sh 8

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". Stop PER ROW: a passing hit kills the labels it lists in column 5;
once every label of a row R1-R7 is dead, later windows that only list that row's labels can be skipped. Stop the pack when all 7 rows
are dead, and report each passing hit with its labels.
