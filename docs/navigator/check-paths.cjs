// Path check for the navigator tree: every node file path must exist in the repository,
// except paths the node lists in plannedFiles ("planned, not yet written").
// Exits 1 on any real broken path. Usage: node check-paths.cjs
const fs = require('node:fs'), vm = require('node:vm'), path = require('node:path');
const base = __dirname + path.sep, repo = path.resolve(__dirname, '..', '..') + path.sep;

function checkTree(root, exists) {
  const broken = [], planned = [], plannedNowExist = [];
  (function walk(n) {
    const pf = new Set(n.plannedFiles || []);
    for (const f of n.files || []) {
      if (pf.has(f)) { planned.push([n.id, f]); if (exists(f)) plannedNowExist.push([n.id, f]); }
      else if (!exists(f)) broken.push([n.id, f]);
    }
    (n.children || []).forEach(walk);
  })(root);
  return { broken, planned, plannedNowExist };
}

function loadTree() {
  const storage = new Map();
  const ctx = vm.createContext({ console, localStorage: { getItem: k => storage.get(k) ?? null, setItem: (k, v) => storage.set(k, v) } });
  vm.runInContext(fs.readFileSync(base + 'data.js', 'utf8'), ctx);
  vm.runInContext(fs.readFileSync(base + 'tree.js', 'utf8') + '\nglobalThis.TestTree = Tree;', ctx);
  const prefix = fs.readFileSync(base + 'app.js', 'utf8').split('/* ===== DETAIL PANEL ===== */')[0];
  vm.runInContext(prefix + '\nglobalThis.TestState = State;', ctx);
  ctx.TestState.init();
  ctx.TestState.applyPlanningBoard(JSON.parse(fs.readFileSync(base + 'planning.json', 'utf8')));
  return ctx.TestState.getTree();
}

module.exports = { checkTree };
if (require.main === module) {
  const r = checkTree(loadTree(), f => fs.existsSync(repo + f));
  console.log(`planned, not yet written: ${r.planned.length}`);
  r.plannedNowExist.forEach(([id, f]) => console.log(`NOTE planned file now exists, remove the flag: ${id} ${f}`));
  r.broken.forEach(([id, f]) => console.log(`BROKEN ${id}: ${f}`));
  console.log(`broken: ${r.broken.length}`);
  process.exit(r.broken.length ? 1 : 0);
}
