# studio14c pre-registration (written 2026-10-14 23:34 MDT, before the run)

Lean checker (`dcheck/.lake/build/bin/wheelcheck18`, DCheck18) on the 43 of the 47 deferred K=1 keys that have no
Lean check yet: 36 ring-17 + 7 ring-18 (`r17.txt`, `r18.txt`, one key per file in `in/`). The 3 ring-17 keys of
studio14b/v_a? are done; the ring-19 key (`6:6:6|6:6:6|6:6:6|6:6:6|8:666:6`) is not run (cost, see below).

- **H14c:** every one of the 43 keys is D=true under wheelcheck18, with classes/ext/reached equal to dfast18's
  (studio14b/part*.out).
- **Kill:** any D=false, or any count that differs from dfast18 (an engine disagreement; report the key).
- **Cost estimate:** Lean/dfast18 time ratio on v_a? is 28-34x. Ring 17: 36 x ~5.5 h = ~200 CPU-h.
  Ring 18: 7 x (3,967 s x ~30) = ~33 h each, ~230 CPU-h. Ring 19 (not run): 19,736 s x ~30 = ~165 h on one core.
- **Run:** 12 workers, nice 10, ring-18 first; /usr/bin/time -l per key for RSS.
