# K-5 bind86r17 pack: ring 17 windows of the 7 open ST-86 binder rows (lead, 9 Nov 2026)

Rows R1-R7 (3 d7, 4 d8; 36 labels in rows.txt, grouped in rows_grouped.txt) are the ST-86 binder rows that stayed open through
ring 16 (container ring <= 14: 82 windows N; ST-87 ring 15-16: 1,984 windows N). The same d7/d8 rows bind ST-89.
This pack is ring 17 only: 1,112 windows (766 from the d8 rows, 346 from the d7 rows), none screened before, 4 batches dealt
round-robin from one list sorted by m (smallest first).

Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind86r17
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb86r17.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". Stop PER ROW as in bind86; stop the pack when all 7 rows
are dead. Report each passing hit with its labels. Low priority: Lean and upper checks first.
