# K-5 bind2140 pack: ring 15-16 windows of the 17 GL5 rank 21-40 rows still open after ring 14 (lead, 8 Nov 2026, floor side)

Rows: ranks 21-40 of from_opus/s86_k86GL5/BINDING_k86GL5_p1_00.txt (largest row of each class), minus the 3 killed by
K5b (L1 C b7_u86..665_5...555, L2 C b7_u5656777_5...5.5, L3 D b8_u755..556_66...5..). List: rows_open.txt (17 rows).
Ring <= 14 of all 17 rows is already screened in the container (no kill). This pack is ring 15 (4,836 windows) and
ring 16 (6,117), 10,953 windows in 8 batches: ring 15 first, then windows covering more rows first, then smallest m.
Column 5 lists the rows each window occurs on.

Windows from gen3.windows on each row's realised 2-ball picture (rotation-correct by construction; 9+ never inside).
Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind2140
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb2140.sh 8

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". Stop rule is PER ROW (as in ST-42): once a hit
passes K3CHK, its rows are killed; windows whose rows are all killed can be skipped (SKIP file of codes, restart the
batch to pick it up). Report each passing hit with its rows.
