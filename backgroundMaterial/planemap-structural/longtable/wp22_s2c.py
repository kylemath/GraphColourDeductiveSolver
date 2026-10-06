#!/usr/bin/env python3
"""wp22_s2c.py -- S2c (descriptive, post hoc, not a kill criterion): the Kempe radius of every state in Math's chain
certificates, with the same radius code as S2a/S2b (wp22_radius).

A certificate (Math's format, SolvingFrameworkPlan/docs/working/MathChainSearch/{certs_len_ge6,lt_certs}) is
{"n","v","link","rot","colour","claimed_length"}.  The states of a certificate are s_0 = its colouring, s_{i+1} = F(s_i)
(F with the certificate's own `link` order, as in Math's checker.py) while s_i is doubly locked, plus the first state
that is not doubly locked (flagged); an orbit is cut when a canonical state repeats (A3.json has an infinite orbit of
period 20 up to renaming).  At most 40 doubly locked states per certificate.
Files accepted: a JSON object with "rot" (a certificate), or with a non-null "certificate" member (Math's search
run records, e.g. runs_md5/band_*/seed_*.json), so the second search can be added by naming its directory.

  wp22_s2c.py list DIR [DIR ...]                    certificate files found (sorted), one per line
  wp22_s2c.py one FILE                              records of one certificate (JSON lines) and a summary
"""
import hashlib
import json
import os
import sys
import time

import wp22_radius as R

CHAIN_CAP = 40


def load_cert(path):
    with open(path) as f:
        d = json.load(f)
    if "rot" in d:
        return d
    if isinstance(d.get("certificate"), dict) and "rot" in d["certificate"]:
        return d["certificate"]
    return None


def list_certs(dirs):
    out = []
    for d in dirs:
        for root, _dn, fn in os.walk(d):
            for name in fn:
                if name.endswith(".json"):
                    p = os.path.join(root, name)
                    try:
                        if load_cert(p) is not None:
                            out.append(p)
                    except (ValueError, OSError):
                        pass
    return sorted(out)


def faces_of_rot(rot):
    fs = {}
    for u, ns in rot.items():
        for i in range(len(ns)):
            f = (u, ns[i], ns[(i + 1) % len(ns)])
            fs[R.norm_face(f)] = f
    return list(fs.values())


def hole_of_cert(cert):
    rot = {int(u): list(ns) for u, ns in cert["rot"].items()}
    H = R.Hole(faces_of_rot(rot), cert["v"])
    # the certificate's link order (possibly the reverse of the rotation order) is the one F is defined with
    H.link_labels = list(cert["link"])
    H.link = [H.idx[x] for x in cert["link"]]
    return H


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def cert_records(path, cap=R.ENUM_CAP, deadline=None, name=None):
    """records (one per state of the certificate) and a summary."""
    cert = load_cert(path)
    H = hole_of_cert(cert)
    msg = H.check()
    if msg:
        raise ValueError("%s: %s" % (path, msg))
    if len(H.link) != 5:
        raise ValueError("hole is not of degree 5")
    col = [cert["colour"][u] for u in H.labels]
    if not H.proper(col):
        raise ValueError("colouring not proper")
    name = name or os.path.basename(path)
    recs = []
    seen = set()
    cur = col
    step = 0
    n_dl = 0
    while True:
        st = R.canon(cur)
        if st in seen:
            recs.append({"cert": name, "step": step, "note": "orbit closed (a canonical state repeats)"})
            break
        seen.add(st)
        dl = H.is_dl(cur)
        rr, info = R.radius(H, st, cap=cap, deadline=deadline)
        rad = None if rr is None else ("inf" if rr == float("inf") else rr)
        recs.append({"cert": name, "step": step, "doubly_locked": dl, "filled": H.filled(st), "radius": rad,
                     "status": info["status"], "state": list(st)})
        if not dl:
            break
        n_dl += 1
        if n_dl >= CHAIN_CAP:
            recs.append({"cert": name, "step": step + 1, "note": "cap of %d doubly locked states" % CHAIN_CAP})
            break
        cur = H.F(cur)
        step += 1
    dl_rad = [r["radius"] for r in recs if r.get("doubly_locked")]
    hist = {}
    for x in dl_rad:
        hist[str(x)] = hist.get(str(x), 0) + 1
    summary = {"cert": name, "sha256": sha256_file(path), "order": H.n, "claimed_length": cert.get("claimed_length"),
               "states": sum(1 for r in recs if "state" in r), "doubly_locked_states": n_dl,
               "radius_hist_dl": dict(sorted(hist.items())),
               "max_radius_dl": max((x for x in dl_rad if isinstance(x, int)), default=None),
               "capped": sum(1 for r in recs if r.get("status") in ("capped", "depth")),
               "kill2_candidates": [r["step"] for r in recs if r.get("radius") == "inf"]}
    return recs, summary


def dumps_records(recs):
    return "".join(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n" for r in recs)


if __name__ == "__main__":
    if sys.argv[1] == "list":
        for p in list_certs(sys.argv[2:]):
            print(p)
    else:
        t = time.process_time()
        recs, s = cert_records(sys.argv[2])
        sys.stdout.write(dumps_records(recs))
        print(json.dumps(s), file=sys.stderr)
        print("cpu %.1f" % (time.process_time() - t), file=sys.stderr)
