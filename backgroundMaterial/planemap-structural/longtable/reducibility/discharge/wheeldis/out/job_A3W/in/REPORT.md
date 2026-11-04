# A3: is the 7-5-5-5 diamond motif reducible? (3 Nov 2026)

Arrangements: 14 dual rows in the four classes (a3_rows.json): 7:5566766 x6, 7:5566676 x5, 7:5566776 x2, 8:55556776 x1.
Method: all connected sub-windows (win45 construction, exact degrees, no letter 9) at ring <= 16 per arrangement (9,608 unique windows).
Reused 3,945 prior verdicts from windows_judged.tsv (all "neither"); ran kc -C on the rest (dfast on any D, cfast on any C: never triggered).
Engines built from repo source in /tmp/swarm-A3/bin. Logs r13.kc, r14.kc, r15.kc here. Ring <= 14 complete, ring 15 partial (157 windows, most fives first), ring 16 not run.

## Result [M, kc only for new windows]
- 0 of 14 arrangements have a D- or C-reducible window at ring <= 14 (kc C limited to |X| <= 4). Zero kc D / C among ~5,800 judged-or-run windows.
- Per class: 7:5566766 0/6, 7:5566676 0/5, 7:5566776 0/2, 8:55556776 0/1; all 14 "neither" at ring <= 14.
- Prior: row 7665566/6765766 was 100% judged neither (windows_judged). binder-probe: whole 2-ball ring 19 not D; only p6=5 is D (RSST 052).
- Smallest neither: every window, ring 6 up. Best C leftover 2 (a8_-....555._.....5.., ring 7): no near miss.

## Verdict
Kill criterion met at ring <= 14: motif is an obstruction for 2-ball methods [M, one engine].
Not checked: ring 15 (mostly) and 16, |X| > 4, second engine on non-D, rows outside the restricted dual.
