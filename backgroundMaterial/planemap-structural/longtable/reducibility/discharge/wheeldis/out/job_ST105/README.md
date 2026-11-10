# K-5 bindt102 pack: ring 15-16 windows of 10 ST-102 tneg binder classes (lead, 10 Nov 2026)

Coverage audit of the ST-102 tneg list (sol_repK2MW_04__K3l5n_k268, 4a181f67): 14 classes had unscreened ring <= 14
windows. The container screened their 1,090 new ring <= 14 windows (0 errors): the d8 55557858/585655xx family (3 classes)
and 55658577/58559557 are killed at ring 14 (lead/K5/container_hits_t102.tsv). This pack is the new ring 15-16 windows of
the other 10 classes (rows.txt), including the new top binder d8 55556959/58585666. 4 batches dealt round-robin from one
list sorted by ring then m. Column 5 lists the classes a window covers.

Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bindt102
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runt102.sh 4

Run the whole pack, skip-listing a class once killed; report each passing hit with its classes, smallest m first.
