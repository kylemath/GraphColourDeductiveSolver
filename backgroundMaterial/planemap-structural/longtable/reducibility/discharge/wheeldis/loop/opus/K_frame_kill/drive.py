"""K_frame_kill driver: kc -C (conservative) on windows from a list; claims each window with an O_EXCL marker in
claim/ so two workers never repeat one.  D hit -> dfast (ring<=16) / dfast18; C hit -> cfast --search with the X
re-checked by kc -C -x.  Logs to run_<tag>.log, hits to hits.txt.  usage: python3 drive.py TAG LIST TLIMIT"""
import sys, os, subprocess, time
H = os.path.dirname(os.path.abspath(__file__)); TAG, LIST, TL = sys.argv[1], sys.argv[2], float(sys.argv[3])
KCC = os.path.join(H, 'kcc'); DF = os.path.join(H, '..', 'A_rsst_defects', 'bin', 'dfast'); DF18 = os.path.join(H, 'dfast18')
CF = os.path.join(H, '..', 'A_rsst_defects', 'bin', 'cfast')
os.makedirs(os.path.join(H, 'claim'), exist_ok=True)
LOG = open(os.path.join(H, 'run_%s.log' % TAG), 'a')
def log(s): LOG.write(s + '\n'); LOG.flush()
def run(cmd, inp, t=None):
    try: return subprocess.run(cmd, input=inp, capture_output=True, text=True, timeout=t).stdout
    except subprocess.TimeoutExpired: return 'TIMEOUT'
for line in open(LIST):
    line = line.strip()
    if not line: continue
    nm = line.split()[0]; r = int(line.split()[1])
    try: os.close(os.open(os.path.join(H, 'claim', nm), os.O_CREAT | os.O_EXCL))
    except FileExistsError: continue
    t0 = time.time(); o = run([KCC, '-C', '-t', str(TL)], line + '\n', TL + 120)
    log('%s\n%s(%.0fs)' % (line, o, time.time() - t0))
    hd = o.split('\n')[0]
    if 'D=true' in hd:
        o2 = run([DF if r <= 16 else DF18, '/dev/stdin'], line + '\n')
        log('  2nd dfast: ' + o2.strip()); open(os.path.join(H, 'hits.txt'), 'a').write('D %s\n%s  dfast: %s\n' % (line, o, o2.strip()))
    elif 'C-REDUCIBLE' in o:
        X = o.split('C-REDUCIBLE X=')[1].split()[0]
        xf = os.path.join(H, 'claim', nm + '.x'); open(xf, 'w').write('%s %s\n' % (nm, X))
        o2 = run([CF, '/dev/stdin', '--search', '--limit', '1'], line + '\n')
        log('  2nd cfast: ' + o2.strip().replace('\n', '\n  2nd cfast: '))
        open(os.path.join(H, 'hits.txt'), 'a').write('C %s\n%s  cfast: %s\n' % (line, o, o2.strip().replace('\n', '\n  cfast: ')))
