import subprocess, shutil, os, sys
root='/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver/78bd1589-fda1-4d14-8502-268e6b6d2668/scratchpad'
B=os.path.expanduser('~/mathlib4-planemap-build'); W=root+'/tcF'
TC=os.path.expanduser('~/.elan/toolchains/leanprover--lean4---v4.35.0-rc3')
import glob
LP=W+':'+':'.join(glob.glob(B+'/.lake/packages/*/.lake/build/lib/lean'))
P='Mathlib/Combinatorics/SimpleGraph/PlaneMap'
CF="""  intro c j hc hr
  set φ := M.rotation.faceNext with hφdef"""
target_head = ": ChainFormulaF M P := by\n"
def stmt(nterm):
    return (": ∀ (c : Fin n → Fin 4) (j : Fin 5), ProperOff M.graph h c → RepeatAt P c j →\n"
      "      2 * (nChains M.graph h c : ZMod 4) = (cwCount M.rotation.faceNext h c : ZMod 4) + "+nterm+" -\n"
      "        (if handS M P c j then 1 else 0) +\n"
      "        2 * ((if Lock1 P c j then 1 else 0) + (if Lock2 P c j then 1 else 0)) := by\n")
tests=[
 ('control: explicit F statement (should compile)','ChainF',target_head,stmt("((n : ZMod 4) - 1)")),
 ('F with n instead of n-1','ChainF',target_head,stmt("(n : ZMod 4)")),
 ('F with hand sign flipped','ChainF',target_head,stmt("((n : ZMod 4) - 1)").replace(" -\n        (if handS"," +\n        (if handS")),
 ('omT_link with 3 for 5','ChainF',"      5 - 2 * ind8 (if s = 1","      3 - 2 * ind8 (if s = 1"),
 ('tutte_sides with 2*gamma','TutteSides',"Module.finrank (ZMod 2) (chainSpace M.graph τ) + gammaM M =","Module.finrank (ZMod 2) (chainSpace M.graph τ) + 2 * gammaM M ="),
 ('euler_tri with 5*gamma','TutteSides',"Fintype.card M.graph.edgeSet + 6 * gammaM M = 3 * n","Fintype.card M.graph.edgeSet + 5 * gammaM M = 3 * n"),
 ('merge lemma with else 2','TutteSides',"(if (sideGraph G τ).Reachable a b then 0 else 1) =\n      Module.finrank","(if (sideGraph G τ).Reachable a b then 0 else 2) =\n      Module.finrank"),
]
for name,f,old,new in tests:
    src=root+'/sab/src'; shutil.rmtree(src,ignore_errors=True); shutil.copytree(root+'/srcF',src)
    fp=f'{src}/{P}/{f}.lean'; s=open(fp).read(); assert s.count(old)==1,(name,s.count(old)); open(fp,'w').write(s.replace(old,new))
    r=subprocess.run(['nice','-n','10',TC+'/bin/lean','-R',src,'-o',root+'/sab/x.olean','-i',root+'/sab/x.ilean',f'{P}/{f}.lean'],cwd=src,env=dict(os.environ,LEAN_PATH=LP),capture_output=True,text=True)
    errs=[l for l in r.stdout.splitlines() if 'error' in l]
    print(f'{name}: exit {r.returncode}; first error: {errs[0][:160] if errs else "-"}')
