# R3-A1: ring 15/16 windows of the 7-5-5-5 diamond motif (3 Nov 2026)
Method: A3's queue (3,403 unreduced-unjudged windows at ring 15-16 over the 14 rows), prioritised by row mass, ring 15 first, most fives first; kc -C (|X|<=4), 300 s cap per window, nice 10. D would go to dfast, C to cfast (never triggered). res.jsonl = every verdict.
Coverage (new, on top of A3's 157 ring-15 windows): row0 (7665566/6765776) ring15 19, ring16 32; row2 ring15 234; total 285 windows. Container shared (load ~6), 20-60 s/window, so the job was stopped. Ring 16: 32 of 2,103 done. Ring 15 about 30% done.
Result [M, one engine]: 0 D, 0 C, 0 timeouts among 285 (+157 A3). Smallest C leftover among new windows: 298, no near miss.
|X|<=6: kc6.cpp (kc with -S flag) on the 20 smallest-leftover windows overall (x6.json): 0 C, leftovers identical to |X|<=4 (2,4,4,...,10).
Kill criterion NOT decided: top three rows not covered through ring 16. Not checked: ~3,100 windows; second engine on non-D.
Next: run rest of queue.json on the Mac fast engines (python3 run.py LO HI BUDGET TIMEOUT resumes from res.jsonl).
