// node a6_run.js MAPS.json OUT.jsonl [--shard i/k] [--sample 200] [--cap 1500000]
//   Studio Job 11 (14 Oct 2026, exploratory): does the game team's rule "Fewest locks, new stars"
//   (4square lab/star-rules.js, built-in 'few-locks-new': cards fill; fewlocks; new) always reach a fill?
//   For every map (sphere triangulation + degree-5 hole, arena spec format) every colouring of T - hole is enumerated
//   (arena engine stateSpace), the colourings are split into Kempe classes with FTH_STAR.graph (the rule's own state
//   tree), and the rule is run from every hard star (dF >= 2, the double locks) of every class, or from a fixed sample of
//   SAMPLE of them (deterministic, by star key hash) when a class has more.  star-rules.js, rim.js and degree.js are
//   loaded unchanged from ~/4square.  Output per hole: counts, failures (with start key, why, path keys), and per walk
//   the per-step features (lock, dF, Fisk degree, spot t, N, nm, visits) for the decreasing-measure search.
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const SQ = path.join(process.env.HOME, '4square'), AR = path.join(process.env.HOME, 'GraphColourRLArena');
const argv = process.argv.slice(2), flag = (k, d) => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : d; };
const [inF, outF] = argv; const [si, sk] = flag('shard', '0/1').split('/').map(Number);
const SAMPLE = +flag('sample', 200), CAP = +flag('cap', 1500000);
const ctx = { window: {}, console, Math, Date }; ctx.window.window = ctx.window; vm.createContext(ctx);
for (const f of ['rim.js', 'degree.js', 'lab/star-rules.js']) vm.runInContext(fs.readFileSync(path.join(SQ, f), 'utf8'), ctx, { filename: f });
const S = ctx.window.FTH_STAR, RIM = ctx.window.FTH_RIM;
global.window = global; require(path.join(AR, 'docs/levels.js')); const A = require(path.join(AR, 'docs/arena/engine.js'));
const RULE = S.BUILTIN.find(r => r.id === 'few-locks-new');
const hash = s => { let h = 2166136261 >>> 0; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h; };
const maps = JSON.parse(fs.readFileSync(inF, 'utf8'));
const out = fs.openSync(outF, 'w');
maps.forEach((m, mi) => {
  if (mi % sk !== si) return;
  const t0 = Date.now();
  const Gr = { name: m.key, n: m.n, hole: m.hole, link: m.link, edges: m.edges, rot: m.rot, ncol: 4, goal: 3 };
  const AG = A.makeGraph(m), SS = A.stateSpace(AG, CAP);
  const rec = { key: m.key, family: m.family || '', n: m.n, hole: m.hole, classes: 0, states: 0, hard: 0, walks: 0, solved: 0, extra: 0, revisits: 0, maxSteps: 0, fails: [], why: {}, feats: [] };
  if (!SS) { rec.skip = 'state space > ' + CAP; fs.writeSync(out, JSON.stringify(rec) + '\n'); return; }
  const GAME = { graphs: { g: Gr } }, done = new Set(), cache = new Map();
  for (let i = 0; i < SS.N; i++) {
    const col = Array.from(SS.cols[i]); col[m.hole] = -1;
    const G = S.prep(Gr), key = RIM.canon(G, col);
    if (done.has(key)) continue;
    const LG = S.graph(GAME, { g: 'g', start: col, id: m.key, num: String(rec.classes) }, null);
    LG.S.forEach(s => done.add(s.key));
    rec.classes++; rec.states += LG.S.length;
    let hard = LG.S.map((s, k) => k).filter(k => LG.S[k].dF >= 2 || (LG.S[k].dF < 0 && !LG.S[k].f.filled));
    rec.hard += hard.length;
    if (hard.length > SAMPLE) hard = hard.sort((a, b) => hash(LG.S[a].key) - hash(LG.S[b].key)).slice(0, SAMPLE);
    for (const k of hard) {
      const w = S.run(RULE, LG, k);
      rec.walks++;
      if (w.solved) { rec.solved++; rec.extra += w.steps - w.dF; rec.maxSteps = Math.max(rec.maxSteps, w.steps); }
      else { rec.why[w.why] = (rec.why[w.why] || 0) + 1; rec.fails.push({ start: LG.S[k].key, dF: LG.S[k].dF, why: w.why, steps: w.steps, path: w.path.map(p => LG.S[p].key) }); }
      if (w.revisit) rec.revisits++;
      if (rec.feats.length < 400 || w.revisit || !w.solved)
        rec.feats.push(w.path.map(p => { const f = LG.S[p].f; return [f.filled ? -1 : f.lock, LG.S[p].dF, f.deg, f.t, f.N, f.nm]; }));
    }
  }
  rec.N = SS.N; rec.coverOK = rec.states === SS.N;
  rec.sec = (Date.now() - t0) / 1000;
  fs.writeSync(out, JSON.stringify(rec) + '\n');
  console.log(mi, m.key, 'classes', rec.classes, 'hard', rec.hard, 'walks', rec.walks, 'solved', rec.solved, 'fails', rec.fails.length, rec.sec.toFixed(1) + 's');
});
fs.closeSync(out);
