"""Admission check on main (explore): git-archive main's out/job30, out/job31 and loop into a scratch copy, regress
main's twoeng (k3x byte-identical), add the named kill files from SHA (byte-identical, same paths), rerun twoeng, and
check that the new k3x adds exactly the files' f-names, loses nothing, and keeps every old line.
usage: python3 adm.py MAINREF SHA OUTDIR RELPATH...   (RELPATH under wheeldis/loop, e.g. k47/r54j_kills.txt)"""
import sys, os, re, subprocess, shutil, hashlib
REPO = '/home/claude/GraphColourDeductiveSolver'; W = 'backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
MAIN, SHA, OUT, rels = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
T = OUT + '/tree'; shutil.rmtree(T, ignore_errors=True); os.makedirs(T)
ar = subprocess.run(['git', '-C', REPO, 'archive', MAIN, W + '/out/job30', W + '/out/job31', W + '/loop'], capture_output=True, check=True).stdout
subprocess.run(['tar', '-x', '-C', T], input=ar, check=True)
J = os.path.join(T, W, 'out', 'job30'); md5 = lambda f: hashlib.md5(open(f, 'rb').read()).hexdigest()
def twoeng():
    r = subprocess.run(['python3', '-I', os.path.join(J, 'twoeng.py')], capture_output=True, text=True, cwd=os.path.join(T, W))
    return [l for l in r.stdout.splitlines() if l.startswith(('files', 'ring-merge', 'letter-9', 'sender'))] + r.stderr.splitlines()[-3:]
m0 = (md5(J + '/k3x_D.out'), md5(J + '/k3x_C.cfast')); oD = open(J + '/k3x_D.out').read().splitlines(); oC = open(J + '/k3x_C.cfast').read().splitlines()
print('main', MAIN, subprocess.run(['git', '-C', REPO, 'rev-parse', '--short', MAIN], capture_output=True, text=True).stdout.strip(), 'k3x md5', m0)
print('regress:', *twoeng(), sep='\n  ')
print('regress byte-identical:', (md5(J + '/k3x_D.out'), md5(J + '/k3x_C.cfast')) == m0)
names = set()
for r in rels:
    b = subprocess.run(['git', '-C', REPO, 'show', '%s:%s/loop/%s' % (SHA, W, r)], capture_output=True, check=True).stdout
    dst = os.path.join(T, W, 'loop', r); os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'wb').write(b)
    if r.endswith('_kills.txt'): names |= {l.split()[0] for l in b.decode().splitlines() if l.strip()}
print('with', len(rels), 'files from', SHA, ':', *twoeng(), sep='\n  ')
nm = lambda L: {l.split()[0] for l in L if re.match(r'^[A-Za-z]\w*_\S+ r=', l)}
nD = open(J + '/k3x_D.out').read().splitlines(); nC = open(J + '/k3x_C.cfast').read().splitlines()
add = (nm(nD) - nm(oD)) | (nm(nC) - nm(oC))
print('D %d -> %d (+%d), C %d -> %d (+%d); lost %d; old lines verbatim %s' % (len(nm(oD)), len(nm(nD)), len(nm(nD) - nm(oD)), len(nm(oC)), len(nm(nC)),
      len(nm(nC) - nm(oC)), len((nm(oD) - nm(nD)) | (nm(oC) - nm(nC))), set(oD) <= set(nD) and set(oC) <= set(nC)))
print('kill-file names %d; already in main %d; added %d; added == new names: %s' % (len(names), len(names & (nm(oD) | nm(oC))), len(add), add == names - (nm(oD) | nm(oC))))
for f in ('k3x_D.out', 'k3x_C.cfast'): shutil.copy(os.path.join(J, f), os.path.join(OUT, f)); print(f, md5(os.path.join(OUT, f)))
