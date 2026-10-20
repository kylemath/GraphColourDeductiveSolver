"""Check the g7 twoeng-ready files against main's twoeng in a scratch copy: k3x must stay byte-identical, every g7 name
must be logged as held with its two-engine verdict.  usage: python3 -I chkg7.py MAINREF OUTDIR SRCDIR"""
import sys, os, subprocess, shutil, hashlib, glob
REPO = '/home/claude/GraphColourDeductiveSolver'; W = 'backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
MAIN, OUT, SRC = sys.argv[1:4]; T = OUT + '/tree'; shutil.rmtree(T, ignore_errors=True); os.makedirs(T)
ar = subprocess.run(['git', '-C', REPO, 'archive', MAIN, W + '/out/job30', W + '/out/job31', W + '/loop'], capture_output=True, check=True).stdout
subprocess.run(['tar', '-x', '-C', T], input=ar, check=True)
J = os.path.join(T, W, 'out', 'job30'); md5 = lambda f: hashlib.md5(open(f, 'rb').read()).hexdigest(); HL = os.path.join(J, 'sender_names_held.log')
def twoeng():
    r = subprocess.run(['python3', '-I', os.path.join(J, 'twoeng.py')], capture_output=True, text=True, cwd=os.path.join(T, W))
    return [l for l in r.stdout.splitlines() if l.startswith(('files', 'ring-merge', 'letter-9', 'sender'))] + r.stderr.splitlines()[-3:]
m0 = (md5(J + '/k3x_D.out'), md5(J + '/k3x_C.cfast')); print('main k3x', m0)
print('regress:', *twoeng(), sep='\n  '); print('regress byte-identical:', (md5(J + '/k3x_D.out'), md5(J + '/k3x_C.cfast')) == m0)
h0 = open(HL).read() if os.path.exists(HL) else ''
dst = os.path.join(T, W, 'loop', 'k53'); os.makedirs(dst, exist_ok=True)
for f in glob.glob(os.path.join(SRC, 'g7_53_kills*')): shutil.copy(f, dst)
print('with g7 files:', *twoeng(), sep='\n  '); print('k3x byte-identical:', (md5(J + '/k3x_D.out'), md5(J + '/k3x_C.cfast')) == m0)
names = [l.split()[0] for l in open(os.path.join(SRC, 'g7_53_kills.txt'))]
new = open(HL).read()[len(h0):].splitlines()
for n in names:
    hit = [l for l in new if l.split()[0] == n]; print(' ', n, '|', hit[-1].split(' ', 1)[1] if hit else 'NOT LOGGED')
