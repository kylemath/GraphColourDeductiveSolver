# K-5 Mac screen pack: ring 15-16 windows of the GL5 lower-bound binding rows (lead, 8 Nov 2026)

Rows: ranks 3-20 of from_opus/s86_k86GL5/BINDING_k86GL5_p1_00.txt (largest row of each class), i.e. the
receivers that carry the GL5 floor after row A (7/7665566/6765776, no kill to ring 16) and row B
(7/7666666/6567656, killed by C f7_.666666_.5...5., [E2] + Lean HCK3l).
The container screens ring <= 14 of the same rows (../wl_GL5top20_r14_container.tsv); this pack is ring 15 and 16 only (9,764 windows).

Windows come from each row's realised 2-ball picture (gen3.windows), so they are rotation-correct by construction.
Batches are in value order: windows covering more dual weight first (batch 01 most valuable).

Engines and run: identical to ../../mac/README.md (K-3 pack): kc -C, then dfast18 (+dfast) for D, cfast --fixed X for C.

    cd round6/W13-open-row-kills/round6/K3/lead/K5/mac
    shasum -a 256 -c SHA256SUMS
    KC=/path/kc DF18=/path/dfast18 CF=/path/cfast bash runk5.sh 8

Results: results/res_K5_<tag>.tsv. A hit = column 5 D with "dfast18:D" in column 11, or C with "cfast:C-REDUCIBLE".
Please report hits as they appear (any hit kills a binding row), then run the K3CHK second check on each.
