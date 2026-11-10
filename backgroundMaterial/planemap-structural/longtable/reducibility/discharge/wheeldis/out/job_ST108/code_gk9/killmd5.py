# W15: verify a kill-table directory before an upper check.  usage: python3 -I killmd5.py KILLDIR
# Checks kill6_U{7,8,9}.npy (or kill_U{7,8,9}.npy): (1) against KILLDIR/MD5 (or MD5SUMS) when present: any mismatch -> exit 2;
# (2) against EXPECT_KILL="u7,u8,u9" md5 prefixes when set: mismatch -> exit 3; (3) names the stack when it is a known one.
import sys, os, hashlib, re
D = sys.argv[1]; KNOWN = {('b493a0ce', '618eb300', '618eb300'): 'patched298 (keep95p131f U7 + 298 B1 bits; Opus s77_k6patch, md5 b493a0ce)',
                          ('c0527d29', '618eb300', '618eb300'): 'stock keep95p131 / keep95p131f (unpatched)'}
got = {}
for U in (7, 8, 9):
    for nm in ('kill6_U%d.npy' % U, 'kill_U%d.npy' % U):
        f = os.path.join(D, nm)
        if os.path.exists(f): got[U] = (nm, hashlib.md5(open(f, 'rb').read()).hexdigest()); break
    else: print('KILLDIR %s: no kill6_U%d.npy / kill_U%d.npy' % (D, U, U)); sys.exit(2)
for U in (7, 8, 9): print('kill U%d: %s md5 %s' % (U, got[U][0], got[U][1]))
bad = 0
for mf in ('MD5', 'MD5SUMS', 'md5.txt'):
    f = os.path.join(D, mf)
    if not os.path.exists(f): continue
    ref = {}
    for l in open(f):
        m = re.match(r'^([0-9a-f]{32})\s+\*?(\S+)', l.strip())
        if m: ref[os.path.basename(m.group(2))] = m.group(1)
    for U in (7, 8, 9):
        nm, h = got[U]
        if nm in ref:
            ok = ref[nm] == h; bad += not ok; print('  %s vs %s: %s' % (nm, mf, 'OK' if ok else 'MISMATCH (file %s, %s says %s)' % (h, mf, ref[nm])))
        else: print('  %s not listed in %s' % (nm, mf))
if bad: print('KILL MD5 CHECK FAILED'); sys.exit(2)
key = tuple(got[U][1][:8] for U in (7, 8, 9))
if os.environ.get('EXPECT_KILL'):
    exp = tuple(os.environ['EXPECT_KILL'].split(','))
    if len(exp) != 3 or not all(g.startswith(e) for g, e in zip((got[U][1] for U in (7, 8, 9)), exp)): print('KILL MD5 CHECK FAILED: expected %s, got %s' % (exp, key)); sys.exit(3)
print('kill stack: %s' % KNOWN.get(key, 'UNKNOWN (md5 %s/%s/%s; not one of the known stacks)' % key))
print('KILL MD5 CHECK OK')
