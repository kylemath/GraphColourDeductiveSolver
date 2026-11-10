# K-5 bind96 pack: ring 15-16 windows of the new ST-96 d8 binder class (lead, 10 Nov 2026)

Rows: the top tneg binder of sol_k86MK1_in23 (t = 0.014164305, K3l5j + 260 keys, ST-96): one d8 class at 2.014164299,
6 labels (55556859/58576556, 55559586/58565567, 55568595/85765565, 55595865/85655675, 55685955/57655658, 55958655/56556758), in rows.txt.
All 1,120 ring <= 16 windows of the class cover all 6 labels. 916 were already screened (container screens and earlier Mac packs, all N);
ring <= 14 (95 new windows) runs in the container. This pack is the 109 new ring 15 (55) and ring 16 (54) windows,
4 batches dealt round-robin from one list sorted by ring then m.

Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind96
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb96.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". Every window covers all 6 labels, so stop at the first
passing hit and report it.
