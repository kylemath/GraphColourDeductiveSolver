# K-5 bindt98 pack: ring 15-16 windows of 6 ST-98 tneg binder classes that still had unscreened windows (lead, 10 Nov 2026)

Coverage audit of the ST-98 tneg list (sol_repK1MW_22, K3l5n + 260 keys): 7 classes had unscreened ring <= 14 windows.
The container screened their 731 new ring <= 14 windows (0 errors): the d9 class 555557577/578587566 is killed at ring 14
(lead/K5/container_hits_t98.tsv); the other 6 (rows.txt) had no hit. This pack is their new ring 15 and 16 windows,
4 batches dealt round-robin from one list sorted by ring then m. Column 5 lists the classes a window covers.

Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bindt98
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runt98.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". Run the whole pack, skip-listing a class once killed;
report each passing hit with its classes, smallest m first per class.
