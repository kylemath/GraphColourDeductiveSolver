# Independent audit of Math's L4 and Theorem P Lean modules (audit team; imports no Math script).
# usage: python3 audit_l4p.py OUTDIR OVERLAYROOT   (run under `lake env` in the live checkout)
# Module set = the 105 listed in audit-101/manifest.json (list only) + new modules + the custom-import
# closure of the new modules, recomputed here from sources. Every olean whose source is in
# the custom set (changed vs upstream Mathlib commit 300d0e5, or untracked) is hidden from the overlay,
# so all custom code is rebuilt from source; only upstream Mathlib/packages oleans are reused.
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
repo = Path('/Users/fulkanjou/mathlib4-planemap')
out, root = Path(sys.argv[1]), Path(sys.argv[2])
(out/'logs').mkdir(parents=True, exist_ok=True)
base = json.load(open('/Users/fulkanjou/GraphColour/backgroundMaterial/planemap-structural/audit-101/manifest.json'))['modules']
new = ['Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyLemmaL4'] + [
    'Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPole' + s for s in
    ['Basic', 'Moves', 'Rules', 'Cut', 'Degen', 'Chain', 'Flip', 'NoSingleton']] + [
    'MathlibTest.PlaneMapVacancyLemmaL4', 'MathlibTest.PlaneMapTheoremPPole']
src = lambda m: repo/(m.replace('.', '/') + '.lean')
imp = lambda m: set(re.findall(r'^\s*(?:public\s+)?import\s+(\S+)', src(m).read_text(), re.M))
UPSTREAM = '300d0e5'
git = lambda *a: subprocess.run(['git', *a], cwd=repo, capture_output=True, text=True, check=True).stdout.split('\n')
cfiles = {f for f in git('diff', '--name-only', UPSTREAM) if f.endswith('.lean')}
cfiles |= {l[3:] for l in git('status', '--porcelain', '-uall') if l.endswith('.lean')}
customset = {f[:-5].replace('/', '.') for f in cfiles}
custom = lambda m: m in customset and src(m).exists()
mods, todo = set(base) | set(new), list(new)
while todo:
    m = todo.pop()
    for d in imp(m):
        if custom(d) and d not in mods:
            mods.add(d); todo.append(d)
closure_extra = sorted(mods - set(base) - set(new))
# Detect custom deps of any module that are NOT being rebuilt (would be silently taken from cache).
missing = sorted({d for m in mods for d in imp(m) if custom(d) and d not in mods})
hashes = lambda: {m: hashlib.sha256(src(m).read_bytes()).hexdigest() for m in sorted(mods)}
before = hashes()
overlay = root/'lib'; overlay.mkdir(parents=True)
old = repo/'.lake/build/lib/lean'; linked = hidden = 0
hidestems = {m.replace('.', '/') for m in customset}
for d, _, files in os.walk(old):
    rel = Path(d).relative_to(old); (overlay/rel).mkdir(parents=True, exist_ok=True)
    for n in files:
        r = str(rel/n)
        if r.split('.')[0] in hidestems: hidden += 1; continue
        (overlay/rel/n).symlink_to(Path(d)/n); linked += 1
paths = os.environ['LEAN_PATH'].split(':'); assert str(old) in paths
os.environ['LEAN_PATH'] = ':'.join(str(overlay) if p == str(old) else p for p in paths)
deps = {m: imp(m) & mods for m in mods}; order = []
while deps:
    ready = sorted(m for m, d in deps.items() if not d & deps.keys())
    assert ready, 'cycle'
    for m in ready: order.append(m); del deps[m]
meta = dict(custom_files=len(customset), module_count=len(order), new=new, closure_extra=closure_extra, missing_custom_deps=missing,
            hidden_cached_files=hidden, linked=linked, order=order, status='running')
print(len(order), 'modules; extra closure', closure_extra, 'missing', missing, 'hidden', hidden, flush=True)
fails = []
for i, m in enumerate(order, 1):
    o = overlay/src(m).relative_to(repo).with_suffix('.olean'); o.parent.mkdir(parents=True, exist_ok=True)
    t = time.time()
    with (out/'logs'/(m + '.log')).open('w') as log:
        r = subprocess.run(['lean', '-o', str(o), str(src(m))], cwd=repo, stdout=log, stderr=subprocess.STDOUT)
    print(f'{i}/{len(order)} {m}: exit {r.returncode} ({time.time()-t:.1f}s)', flush=True)
    if r.returncode: fails.append(m); break
# Axiom sweep over every non-internal constant declared in the new source modules.
ax = out/'AxiomSweep.lean'
srcnew = [m for m in new if not m.startswith('MathlibTest')]
ax.write_text('import ' + '\nimport '.join(srcnew) + '\nopen Lean Elab Command in\n#eval show CommandElabM Unit from do\n'
  '  let env ← getEnv\n  let mods : List Name := [' + ', '.join('`' + m for m in srcnew) + ']\n'
  '  let idxs := mods.filterMap env.getModuleIdx?\n  let mut n := 0\n  let mut bad := #[]\n'
  '  for (c, _) in env.constants.toList do\n'
  '    match env.getModuleIdxFor? c with\n    | some i => if idxs.contains i && !c.isInternal then\n'
  '        n := n + 1\n        let axs ← liftCoreM (collectAxioms c)\n'
  '        for a in axs do\n          if a != ``propext && a != ``Classical.choice && a != ``Quot.sound then bad := bad.push (c, a)\n'
  '      else pure ()\n    | none => pure ()\n'
  '  logInfo m!"constants checked: {n}; nonstandard: {bad.size}; {bad.toList.take 20}"\n')
if not fails:
    r = subprocess.run(['lean', str(ax)], cwd=repo, capture_output=True, text=True)
    (out/'axiom-sweep-output.txt').write_text(r.stdout + r.stderr); meta['axiom_sweep_exit'] = r.returncode
after = hashes()
meta['sources_changed_during_run'] = [m for m in before if before[m] != after[m]]
(out/'SHA256SUMS-sources').write_text(''.join(f'{h}  {src(m).relative_to(repo)}\n' for m, h in after.items()))
meta['status'] = 'failed' if fails else 'passed'; meta['failed'] = fails
(out/'manifest.json').write_text(json.dumps(meta, indent=2) + '\n'); print(meta['status'])
