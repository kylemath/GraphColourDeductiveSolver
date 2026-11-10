# K-5 bindt96 pack: ring 15-16 windows of 11 ST-96 tneg binder classes that still had unscreened windows (lead, 10 Nov 2026)

A coverage audit of all 46 tneg classes of sol_k86MK1_in23 (ST-96) found 13 classes whose ring <= 16 windows were not all
screened. The container screened their 793 new ring <= 14 windows: 2 classes are killed at ring 13-14
(55557577/58586656, 56765767/56655555; lead/K5/container_hits_t96.tsv), 11 had no hit. This pack is the 1,515 new
ring 15 (660) and ring 16 (855) windows of those 11 classes (rows.txt), 4 batches dealt round-robin from one list sorted
by ring then m. Column 5 of each batch line lists the classes a window covers (a window can cover several).

Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bindt96
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runt96.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". Run the whole pack (windows cover different classes);
report each passing hit with the classes it covers, smallest m first per class.
