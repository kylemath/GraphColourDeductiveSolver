# K-5 bind75 pack: ring 15-16 windows of the ST-75 upper binder receivers (lead, 9 Nov 2026)

Rows: the 98 top-load receivers of sol_k86MS5_in03_tight on K3l5j + 240 keys (ST-75, tneg_receiver_violators.txt a8d39a37):
75 d8 rows at 2.018674921 (19 links) and 23 d7 rows at 1.018674921 / 1.018674906. List: rows.txt.
Ring <= 14 of all 98 rows was already screened in the container (6,385 windows, all N). This pack is ring 15 (2329 windows)
and ring 16 (2804), 5,133 windows in 8 batches (windows from earlier Mac packs removed): ring 15 first, windows covering
more rows first, then smallest m. Column 5 lists the rows each window occurs on.
Note (ST-75): 189 sender rows bind too, so kills here help but will not move this point much on their own.

Windows from gen3.windows on each row's realised 2-ball picture (rotation-correct by construction; 9+ never inside).
Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind75
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb75.sh 8

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". Stop rule is PER ROW (as ST-67): once a hit passes
K3CHK its rows are dead; windows whose rows are all dead can be skipped. Report each passing hit with its rows.
