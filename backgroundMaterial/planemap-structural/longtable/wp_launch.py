#!/usr/bin/env python3
"""Detached launch helper (macOS has no setsid(1); Python's start_new_session=True calls setsid(2)).

  wp_launch.py start NAME [--dir DIR] [--no-caffeinate] -- COMMAND ...
  wp_launch.py status NAME [--dir DIR]
  wp_launch.py stop   NAME [--dir DIR] [--wait SECONDS]

Starts COMMAND in a NEW SESSION and process group (so closing the terminal or the parent shell does
not kill it), wrapped in `caffeinate -ims` (no idle/disk/system sleep while it runs; skipped with a
notice if caffeinate is absent).  Writes DIR/NAME.pid (JSON: pid = process-group leader, command,
start time) and DIR/NAME.log (stdout+stderr, appended).  `stop` sends SIGTERM to the whole process
group (a wp_shard_runner scheduler handles it: terminates its workers, flushes its ledger, exits),
then SIGKILL after --wait seconds (default 20) if anything is left.
A reboot or power loss still kills everything: that is what the shard ledger is for.
"""
import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time


def paths(a):
    d = os.path.abspath(a.dir)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, a.name + ".pid"), os.path.join(d, a.name + ".log")


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def group_alive(pgid):
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def cmd_start(a):
    pidf, logf = paths(a)
    if os.path.exists(pidf):
        old = json.load(open(pidf))
        if group_alive(old["pid"]):
            sys.exit("already running: pid %d" % old["pid"])
    cmd = list(a.command)
    if not cmd:
        sys.exit("no command")
    if not a.no_caffeinate:
        if shutil.which("caffeinate"):
            cmd = ["caffeinate", "-ims"] + cmd
        else:
            print("caffeinate not found; starting without it")
    log = open(logf, "ab")
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                         start_new_session=True, cwd=os.getcwd())
    tmp = pidf + ".tmp"
    with open(tmp, "w") as f:
        json.dump({"pid": p.pid, "command": cmd, "started": time.time(), "cwd": os.getcwd()}, f)
    os.rename(tmp, pidf)
    print("started pid %d (own session); log %s; pid file %s" % (p.pid, logf, pidf))


def cmd_status(a):
    pidf, logf = paths(a)
    if not os.path.exists(pidf):
        print("no pid file")
        sys.exit(1)
    info = json.load(open(pidf))
    up = group_alive(info["pid"])
    print("pid %d %s; log %s" % (info["pid"], "RUNNING" if up else "not running", logf))
    sys.exit(0 if up else 1)


def cmd_stop(a):
    pidf, _ = paths(a)
    if not os.path.exists(pidf):
        sys.exit("no pid file")
    pid = json.load(open(pidf))["pid"]
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        print("not running")
        os.remove(pidf)
        return
    t0 = time.time()
    while group_alive(pid) and time.time() - t0 < a.wait:
        time.sleep(0.2)
    if group_alive(pid):
        os.killpg(pid, signal.SIGKILL)
        print("SIGKILL after %ss" % a.wait)
    else:
        print("stopped (SIGTERM)")
    os.remove(pidf)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("start")
    p.add_argument("name")
    p.add_argument("--dir", default=".")
    p.add_argument("--no-caffeinate", action="store_true")
    p.set_defaults(f=cmd_start)
    p = sp.add_parser("status")
    p.add_argument("name")
    p.add_argument("--dir", default=".")
    p.set_defaults(f=cmd_status)
    p = sp.add_parser("stop")
    p.add_argument("name")
    p.add_argument("--dir", default=".")
    p.add_argument("--wait", type=float, default=20)
    p.set_defaults(f=cmd_stop)
    argv = sys.argv[1:]
    rest = []
    if "--" in argv:
        k = argv.index("--")
        argv, rest = argv[:k], argv[k + 1:]
    a = ap.parse_args(argv)
    a.command = rest
    a.f(a)


if __name__ == "__main__":
    main()
