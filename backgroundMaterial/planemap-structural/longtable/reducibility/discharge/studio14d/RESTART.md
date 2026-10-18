# studio14d k19 restart (17 Oct 2026, 20:46 MDT)

The Mac Studio rebooted at 18:58 MDT on 17 Oct (power outage). wheelcheck18 cannot checkpoint, so k19 restarted from scratch.
- Same command and priority as the original: `nice -n 10 /usr/bin/time -l .../wheelcheck18 k19`, which runs at
  effective nice 15.
- New PID 7776. The governor was re-armed on it.
- Lost: about 63–64 CPU-hours (56.4 CPU-h at 11:13 MDT plus about 7.5 h until the reboot).
- Expected time: dfast18 takes 19,736 s on this key. The Lean/dfast18 ratio was about 30x at ring 18 (k02: 116,913 s
  vs 3,600–4,200 s) and 18–27x at ring 17. At 30x that is about 165 CPU-h.
