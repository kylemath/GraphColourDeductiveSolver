# K-5 bind61 pack: ring 15-16 windows of the ST-61 binding upper class (lead, 8 Nov 2026)

Rows (one d9 class, 6 labels, all t-neg binders of sol_k86MS2_in04 on K3l5e+240, ST-61):
555556667/578587656, 555557666/587565678, 555566675/785876565, 555576665/875656785, 555666755/858765657, 555766655/756567858.
Ring <= 14 is being screened in the container in parallel (lead will say stop if it finds a kill). This pack is ring 15 (846 windows) and ring 16 (841), 1,687 windows in
4 batches, ring 15 first, smallest m first. Every window occurs on all 6 labels (column 5).

Windows from gen3.windows on each row's realised 2-ball picture (rotation-correct by construction; 9+ never inside).
Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind61
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb61.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". One passing hit kills the whole class: stop the pack
after the first hit that passes K3CHK and report it.
