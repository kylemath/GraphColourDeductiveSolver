# maclane macshim v2: a timeout stand-in that cannot hit a stray PID or leave orphans

**Studio question (9 Nov 11:40Z).** ST-69 Lean wrappers (`time` around `lean`) got SIGTERM twice at 4-5 min, exit 143, with `lean` left
orphaned. Could the lane, v2d, or macshim/timeout kill a stale PID?

**The lane never calls `timeout`.** Nothing in the pack, the add-ons, v2d / v2d1 or the engines calls `timeout` (the scripts were
searched for the command and python for a `'timeout'` argv). The lane kills by PID only in three places:
- stop_fam.sh / launch_upper_fam.sh, by tag pattern;
- the smoke scripts, on their own child that they have not yet reaped (so its PID cannot have been reused);
- python's subprocess timeouts, also on their own child.

v2d added no kill.

**macshim/timeout v1 has two real faults, both shown in a container test:**
1. On timeout it signals only its direct child. `timeout D time lean ...` therefore kills `time` and leaves `lean` running as an
   orphan. A race between `wait` and the marker file also makes it exit 143 instead of 124. That is exactly the ST-69 symptom.
   GNU timeout signals the whole process group, so `lean` would die too.
2. If the timeout process itself is killed before its command ends, its watcher subshell lives on. After the full duration it runs
   `kill -0 $P && kill -TERM $P` on the old PID, which may by then belong to another process.

So if ST-69's runner calls `timeout` and `type -a timeout` in its environment resolves to /tmp/maclane-k86/macshim/timeout (for
example a shell with the lane's PATH), the 4-5 min kills are its own time limit firing (fault 1), or a stale watcher (fault 2).

**v2** (`timeout`, bash 3.2 safe; GNU options -s, -k, --foreground, --preserve-status):
- The watcher polls once a second. It exits as soon as the timeout process or the command is gone.
- Before signalling, it checks that the command's PID still has the command's start time (`ps -o lstart`), so a reused PID is never
  signalled.
- On timeout it signals the command and all its descendants, children first, then exits 124 (137 when -k had to send KILL).
- TERM / INT / HUP sent to timeout are passed on to the command's tree.
- Duration 0 means no limit (as GNU); under 1 s counts as 1 s.

**Container tests:**
- the command's exit code is passed through;
- a timeout with a grandchild gives 124 and no orphans (v1: 143, both sleeps orphaned);
- -s KILL gives 124; -k on a TERM-ignoring command gives 137 with no orphans;
- a TERMed wrapper gives 143, with the command tree and watcher gone;
- a SIGKILLed wrapper leaves its watcher exiting within 1 s (v1: the watcher's sleep stays alive and fires later);
- 0, 0.3, 1s and 1m durations behave as described.

**Install:** `DRY=1 bash install_macshim2.sh; bash install_macshim2.sh`. It replaces /tmp/maclane-k86/macshim/timeout (v1 1cefd903),
keeps v1 as timeout.v1, and runs a self-test (exit 3 passes through, 1 s on `sleep 5` gives 124). Lane scripts pick it up on their
next call; nothing needs restarting. If ST-69's runner uses it, also check the runner's time limit: with v2 a module that hits it dies
cleanly with its `lean`, exit 124.
