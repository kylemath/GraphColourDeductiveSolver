// node a6_paths.js MAPS.json KEYS(comma) : print every hard-star walk (start key, solved, steps, why, path) of the rule, for cross-checks
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const SQ = path.join(process.env.HOME, '4square'), AR = path.join(process.env.HOME, 'GraphColourRLArena');
const ctx = { window: {}, console, Math, Date }; ctx.window.window = ctx.window; vm.createContext(ctx);
for (const f of ['rim.js', 'degree.js', 'lab/star-rules.js']) vm.runInContext(fs.readFileSync(path.join(SQ, f), 'utf8'), ctx, { filename: f });
const S = ctx.window.FTH_STAR, RIM = ctx.window.FTH_RIM, RULE = S.BUILTIN.find(r => r.id === 'few-locks-new');
global.window = global; require(path.join(AR, 'docs/levels.js')); const A = require(path.join(AR, 'docs/arena/engine.js'));
const want = new Set(process.argv[3].split(','));
for (const m of JSON.parse(fs.readFileSync(process.argv[2], 'utf8'))) {
  if (!want.has(m.key)) continue;
  const Gr = { n: m.n, hole: m.hole, link: m.link, edges: m.edges, rot: m.rot, ncol: 4, goal: 3 }, SS = A.stateSpace(A.makeGraph(m), 2e6), done = new Set();
  for (let i = 0; i < SS.N; i++) {
    const col = Array.from(SS.cols[i]); col[m.hole] = -1; const k0 = RIM.canon(S.prep(Gr), col); if (done.has(k0)) continue;
    const LG = S.graph({ graphs: { g: Gr } }, { g: 'g', start: col, id: m.key, num: '0' }, null); LG.S.forEach(s => done.add(s.key));
    LG.S.forEach((s, k) => { if (s.dF >= 2) { const w = S.run(RULE, LG, k); console.log(JSON.stringify({ map: m.key, start: s.key, solved: w.solved, steps: w.steps, why: w.why, path: w.path.map(p => LG.S[p].key) })); } });
  }
}
