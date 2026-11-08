# K-5 bind64 pack: ring 15-16 windows of the ST-64a binding upper class (lead, 8 Nov 2026)

Rows (one d9 class, 6 labels, all t-neg binders of sol_repS2MW_06_tight on K3l5g+240, ST-64a):
555557558/758587857, 555558557/585775878, 555575585/585878577, 555585575/857758785, 555755855/858785775, 555855755/577587858.
Ring <= 14 is being screened in the container in parallel (lead will say stop if it finds a kill). This pack is ring 15 (556 windows) and ring 16 (591), 1,147 windows in
4 batches, ring 15 first, smallest m first. Every window occurs on all 6 labels (column 5).

Windows from gen3.windows on each row's realised 2-ball picture (rotation-correct by construction; 9+ never inside).
Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind64
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb64.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". One passing hit kills the whole class: stop the pack
after the first hit that passes K3CHK and report it.
