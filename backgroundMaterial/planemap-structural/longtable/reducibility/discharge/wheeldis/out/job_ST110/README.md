# K-5 bindt107 pack: ring 15-16 windows of 9 ST-107 tneg binder classes (lead, 10 Nov 2026)

Coverage audit of the ST-107 tneg list (sol_k86MK2_in08_tight__K3l5q_k260, 337e1c81), deduped against every earlier
container screen and every Mac pack (lead done list snapshot tools/done_codes_1145Z.txt). The container screened the 340
new ring <= 14 windows of 7 classes: P18 (5757758/5775555) and P19 (5569577/5667957) found, [E2] ST-109. The top d9
binder 555557557/588586778 is open to ring 16 (container, all 12 ring-16 windows N). Classes already killed in family t
(P15, P16, P17, P18, P19) are left out. This pack is the 1,046 unscreened ring 15-16 windows (379 ring 15, 667 ring 16)
of the other 9 classes (rows.txt): 6666767/5675575, the d8 55556858/5857585x and 55556857/585857xx families,
5566776/5675667, 5557557/5788877, 55557557/58598689. 4 batches dealt round-robin from one list sorted by ring then m.
Column 5 lists the classes a window covers.

Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bindt107
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runt107.sh 4

Run the whole pack, skip-listing a class once killed; report each passing hit with its classes, smallest m first.
