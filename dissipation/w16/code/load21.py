# W16: load the Studio-side checker st21_w10.py (W10 copy, md5 fa40e97f) as a library.
# Runs its LOWER_ONLY path on a given certificate (validation), catches the sys.exit, returns the namespace.
import os, sys, time
R='/home/user/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
S=R+'/out/job31/f2bA'; K=R+'/loop/studio/opus_check/f2b041/keep95p131/tab'; T='/mnt/project-files/swarm/round6/W1-minimal-set/k95f'
BASEENV=dict(F2B=T+'/tab/rules_studio_keep95p131f.json', L3Q='1', L3TAB=S+'/studio_l3qtab_+1.json,'+S+'/studio_l3qtab_-1.json',
  L3Q8='1', L3TAB8=S+'/V8/studio_l3qtabV8_+1.json,'+S+'/V8/studio_l3qtabV8_-1.json', KILLDIR=K+'/kill', RPATN='out/job31/s39o_rpatN3_studio.txt',
  HAT5='1', V6='0', FB='0', XO='0', LOWER_ONLY='1', EXPECT_PAT='18159,627,158', WLP3X_DEF='1', WLP_SEPF='1', DMAXP='17')
FAMENV=dict(HATRR='1', ZH='1', ZR='1', ZCAP='3', Q7='1', Q7M='1', Q7CAP='3')
def load(cert, expect_t='0', fam=True, sol=None, args='/tmp/swarm-W10/args_k95f.txt', extra=None):
    env=dict(BASEENV); env['EXPECT_T']=expect_t
    if fam: env.update(FAMENV)
    else: env.update(dict(HATRR='0', ZH='0', ZR='0', Q7='0', Q7M='0'))
    if extra: env.update(extra)
    os.environ.update(env)
    sol = sol or ('/tmp/swarm-W10/sol/sol_zero.json' if fam else T+'/sol_c_repaired_opusfmt.json')
    P='/tmp/swarm-W16/code/st21_w10.py'
    sys.path.insert(0, '/tmp/swarm-W16/code'); cwd=os.getcwd(); os.chdir('/tmp/swarm-W10/wd')
    sys.argv=[P, sol, cert, args]; ns={'__file__':P, '__name__':'st21lib'}; t0=time.time()
    try: exec(compile(open(P).read(), P, 'exec'), ns)
    except SystemExit: pass
    os.chdir(cwd); print('[load21] loaded in %.0f s, FAIL=%s' % (time.time()-t0, ns.get('FAIL')), flush=True)
    return ns
if __name__ == '__main__':
    ns = load(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '0', fam=(os.environ.get('W16FAM','1')=='1'))
