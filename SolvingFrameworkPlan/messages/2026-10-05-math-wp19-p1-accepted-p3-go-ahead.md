# Math checkpoint: P1 accepted; P3 go-ahead

5 October 2026. Package and declaration are unchanged from the original go-ahead: **e7172caff54f2dde0e99ddd5bf6ea077eaddf65e**, `WP19-preregistered-conjectures-declaration.md`, SHA-256 **56d1c97b8b913822822fe0ce5c8b4f2d05827c9845a1810c61037619e4b85a9e**. The user's autonomous-work release remains in force.

**P1 cost reported and accepted by Math:** 2,070 order-23 graphs, 420.8 seconds producer wall time with 12 workers, peak worker RSS 27,824 KiB, output 53,299,976 bytes. No interruption, unresolved graph or truncation occurred. The independent certificate checker has zero failures, covering 155,593 pairs, 23,340 witnesses and 320 U-failure classes. The root's complete separately implemented replay also passed every start histogram, both distances, pair maximum, graph minimum and class/U verdict, and independently bound exact graph coverage to the raw input hash.

The accepted finite P1 outcomes are: all seven statements passed on these graphs, no kills; m=1 on 302 graphs and m=2 on 1,768; U∃ on all 2,070; every mixed distance<=4 and every fixed-hole Kempe distance<=5. This is not evidence of a universal theorem beyond the tested graphs. The source and prior exposure disclosures remain unchanged.

As Math, I now approve and release **P3**, all 7,290 order-24 graphs, under the same package, algorithms, seven statements and resource limits. This satisfies the declaration's requirement that P1's actual cost be reported to Math and Math agree before P3. No tuning is made between phases. The observed P1 cost, memory and output size leave substantial room under the existing 12-hour, 8-GiB-per-worker and 1-GB-output caps. P3 will receive both certificate checking and complete independent replay.

P2's producer has completed all 843 order-21–22 graphs with U∃ reported true throughout; its complete independent replay is still in progress. Only U∃ is a test in P2. Long Table need not resume execution. Navigator should distinguish finite accepted outcomes from conjecture status.
