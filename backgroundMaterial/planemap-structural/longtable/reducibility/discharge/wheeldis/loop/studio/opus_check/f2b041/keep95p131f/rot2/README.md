# rot2: l3q / §14' kill / kill6 tables, flag off (byte-identity) vs ROT on (L3Q_ROT=1 / ST16_ROT=1)
current keep95p131f: l3q +1/-1 f4b86569c6c5485103679c4dd96732a6/f4b86569c6c5485103679c4dd96732a6; V8 2e8e8f5ee1e88efae667e49bb3ee4047/2e8e8f5ee1e88efae667e49bb3ee4047; kill6 U7/U8/U9 c0527d29aea611d4c8b888b6abeb67c1/618eb3001e0119b3e116af850f95ab99/618eb3001e0119b3e116af850f95ab99; KILL7 kill6_U7 b493a0ce45d676350f34737ac1fa0945
off/tab: studio_l3q_reqs.json=77a2beb9 studio_l3qtab_+1.json=f4b86569 studio_l3qtab_-1.json=f4b86569
off/V8: studio_l3qV8_reqs.json=2d884e45 studio_l3qtabV8_+1.json=2e8e8f5e studio_l3qtabV8_-1.json=2e8e8f5e
off/kill: check4_full.json=ff07b294 kill6_U7.npy=c0527d29 kill6_U8.npy=618eb300 kill6_U9.npy=618eb300 kill_U7.npy=f2d89893 kill_U8.npy=c9e2d251 kill_U9.npy=c9e2d251
off/kill7: check4_full.json=8a2a721a kill6_U7.npy=b493a0ce kill6_U8.npy=618eb300 kill6_U9.npy=618eb300 kill_U7.npy=4758f0a9 kill_U8.npy=c9e2d251 kill_U9.npy=c9e2d251
off2/tab: studio_l3q_reqs.json=01dca3e6 studio_l3qtab_+1.json=f4b86569 studio_l3qtab_-1.json=f4b86569
on/tab: studio_l3q_reqs.json=249a7edd studio_l3qtab_+1.json=f4b86569 studio_l3qtab_-1.json=f4b86569
on/V8: studio_l3qV8_reqs.json=880e874c studio_l3qtabV8_+1.json=2e8e8f5e studio_l3qtabV8_-1.json=2e8e8f5e
on/kill: check4_full.json=4a5fdf2b kill6_U7.npy=c0527d29 kill6_U8.npy=618eb300 kill6_U9.npy=618eb300 kill_U7.npy=f2d89893 kill_U8.npy=c9e2d251 kill_U9.npy=c9e2d251
on/kill7: check4_full.json=8a2a721a kill6_U7.npy=b493a0ce kill6_U8.npy=618eb300 kill6_U9.npy=618eb300 kill_U7.npy=4758f0a9 kill_U8.npy=c9e2d251 kill_U9.npy=c9e2d251
RESULT: every flag-off table is byte-identical to the current one, and every ROT-on table is byte-identical to its flag-off table. ROT drops 0 entries and 0 bits in l3q (sigma +-1, V7 and V8; letter-5 kills: 200 / 50 per side kept) and in the kill tables U7/U8/U9 and KILL7 kill6 (b493a0ce).
on/tab_bug_sigma-1, on/V8_bug_sigma-1: the first ROT-on l3q run, with a bug in my hook (it set only w_1..w_4 to the requirement letters, so sigma = -1 images had the wrong degree), superseded by on/tab and on/V8.

Note: studio_l3q*_reqs.json and check4_full.json differ only in ordering. The requirement-set dumps differ even between two flag-off runs (off vs off2, set iteration order), and the check4_full kill contents (slot -> letter -> configurations) are identical off vs on.
