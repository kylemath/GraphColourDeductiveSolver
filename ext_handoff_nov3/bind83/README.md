# K-5 bind83 pack: ring 15-16 windows of the ST-83 upper binder class (lead, 9 Nov 2026)

Rows (one d7 class, 8 labels, top-load binders of sol_repS6MW_04 at 1.016520033 on K3l5j + 240 keys, ST-83): rows.txt.
Ring <= 14 is exhausted in the container (447 windows, all N). This pack is ring 15 (165 windows) and ring 16 (186),
windows from earlier Mac packs removed, 4 batches, ring 15 first, smallest m first. Column 5 lists the labels: 36 windows cover all 8, the rest cover one of two mirror halves of 4.

Windows from gen3.windows on each row's realised 2-ball picture (rotation-correct by construction; 9+ never inside).
Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind83
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb83.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". Stop PER ROW (as ST-67): a passing hit kills the labels it lists; stop the pack once all 8 are dead,
and report each passing hit with its labels.
