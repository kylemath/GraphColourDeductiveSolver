# K-5 bind89 pack: ring 15-16 windows of the new ST-89 d9 binder class (lead, 9 Nov 2026)

Rows: the top tneg binder of sol_k86MK1_in08 (t = 0.015523694, K3l5j + 260 keys, ST-89): one d9 row, 3 labels
(555557557/588586768, 555575575/885867685, 555755755/858676858), in rows.txt. Not the K5m class.
Ring <= 14 (16 windows) runs in the container. This pack is ring 15 (121 windows) and ring 16 (146), windows from earlier packs
and container screens removed, 4 batches dealt round-robin from one list sorted by ring then m.

Engines and run as the K-5 pack (../README.md): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac/bind89
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runb89.sh 4

A hit = column 5 D with "dfast18:D", or C with "cfast:C-REDUCIBLE". Stop at the first passing hit that lists all 3 labels
(or once hits together cover all 3), and report each passing hit with its labels.
