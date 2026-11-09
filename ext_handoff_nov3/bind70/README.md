# K-5 bind70 pack: ring 15-16 windows of the ST-70 upper binder class (lead, 9 Nov 2026)

Rows (one d7 class, 4 labels, the binders of sol_repS4MW_01__K3l5i at 1.020077 on K3l5i + 240 keys, ST-70):
5757578/5577555, 5757587/7755555, 5757857/7755555, 5758757/5555577 (rows.txt).
Ring <= 14 (356 windows not screened before) runs in the container in parallel; the lead will say stop if it finds a kill.
This pack is ring 15 (310 windows) and ring 16 (267), windows already screened in earlier Mac packs removed, 4 batches,
ring 15 first, smallest m first. Every window occurs on all 4 labels (column 5).

Windows from gen3.windows on each row's realised 2-ball picture (rotation-correct by construction; 9+ never inside).
Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind70
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb70.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". One passing hit kills the whole class: stop the pack
after the first hit that passes K3CHK and report it.
