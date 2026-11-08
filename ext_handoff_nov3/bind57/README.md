# K-5 bind57 pack: ring 15-16 windows of the ST-57 binding upper class (lead, 8 Nov 2026)

Rows (one d9 class, 6 labels, all t-neg binders of sol_k86MS1_in12 on K3l and K3l5+240, ST-57):
555557557/578587767, 555557557/587576778, 555575575/785877675, 555575575/875767785, 555755755/757677858, 555755755/858776757.
Ring <= 14 was screened in the container (no kill). This pack is ring 15 (533 windows) and ring 16 (751), 1,284 windows in
4 batches, ring 15 first, smallest m first. Every window occurs on all 6 labels (column 5).

Windows from gen3.windows on each row's realised 2-ball picture (rotation-correct by construction; 9+ never inside).
Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind57
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb57.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". One passing hit kills the whole class: stop the pack
after the first hit that passes K3CHK and report it.
