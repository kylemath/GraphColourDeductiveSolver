'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const base = __dirname + path.sep;
const storage = new Map();
const context = vm.createContext({ console, localStorage: {
  getItem: key => storage.get(key) ?? null,
  setItem: (key, value) => storage.set(key, value)
}});
vm.runInContext(fs.readFileSync(base + 'data.js', 'utf8'), context);
vm.runInContext(fs.readFileSync(base + 'tree.js', 'utf8') + '\nglobalThis.TestTree = Tree;', context);
const prefix = fs.readFileSync(base + 'app.js', 'utf8').split('/* ===== DETAIL PANEL ===== */')[0];
assert(prefix.includes('function applyPlanningBoard'));
vm.runInContext(prefix + '\nglobalThis.TestState = State;', context);
const State = context.TestState, Tree = context.TestTree;
const clone = x => JSON.parse(JSON.stringify(x));
const flatten = t => [t, ...(t.children || []).flatMap(flatten)];
State.init();
const original = clone(State.getTree());
const f = Tree.findNode(State.getTree(), 'foundation');
assert(f);
const moving = f.children[0];
assert(moving, 'real default foundation has a migratable child');
const id = moving.id, originalStatus = moving.status, originalNotes = clone(moving.notes || []);
const originalIds = flatten(State.getTree()).map(n => n.id).sort();
const rev = (State.getTree().planningRevision || 0) + 1;
const board = { revision: rev, patches: [
  { op: 'insert', parentId: '4ct', index: 1, node: { id: 'audit-route-test', title: 'Route', status: 'exploring', notes: [], children: [] } },
  { op: 'move', id, parentId: 'audit-route-test', index: 0 },
  { id, title: 'Migrated and retitled', active: true },
  { id: 'foundation', active: false, title: 'Archived foundation' }
], journal: [{time: '2026-10-04T00:00:00Z', action: 'test migration', node: id}] };
assert.equal(State.applyPlanningBoard(board), true);
assert.equal(Tree.findParent(State.getTree(), id).id, 'audit-route-test');
assert.equal(Tree.findNode(State.getTree(), id), moving, 'preserve object and descendant history');
assert.equal(moving.title, 'Migrated and retitled');
assert.equal(moving.active, true);
assert.equal(moving.status, originalStatus);
assert.deepEqual(clone(moving.notes || []), originalNotes);
assert.deepEqual(flatten(State.getTree()).map(n => n.id).filter(i => i !== 'audit-route-test').sort(), originalIds);
assert.equal(State.getTree().children[1].id, 'audit-route-test', 'insert honors index');
const snapshot = JSON.stringify(State.getTree());
assert.equal(State.applyPlanningBoard(board), false);
assert.equal(JSON.stringify(State.getTree()), snapshot);
assert.equal(State.getJournal().filter(e => e.action === 'test migration').length, 1);
assert.equal(State.applyPlanningBoard({ revision: rev - 1, patches: [{id, title: 'wrong'}] }), false);
assert.equal(moving.title, 'Migrated and retitled');
// A same-parent move uses its index after removal.
assert.equal(State.applyPlanningBoard({revision: rev + 1, patches: [{op: 'move', id: 'audit-route-test', parentId: '4ct', index: 0}]}), true);
assert.equal(State.getTree().children[0].id, 'audit-route-test');
// An ancestor cannot move under itself or any descendant; the root cannot move.
assert.equal(State.applyPlanningBoard({revision: rev + 2, patches: [
  {op: 'move', id: 'audit-route-test', parentId: id},
  {op: 'move', id, parentId: id},
  {op: 'move', id: '4ct', parentId: id}
]}), true);
assert.equal(Tree.findParent(State.getTree(), 'audit-route-test').id, '4ct');
assert.equal(Tree.findParent(State.getTree(), id).id, 'audit-route-test');
assert.equal(State.getTree().id, '4ct');
assert.equal(new Set(flatten(State.getTree()).map(n => n.id)).size, flatten(State.getTree()).length);
// A descendant remains excluded when its ancestor is inactive even if marked active.
const statsFixture = {id: 's', status: 'exploring', children: [
 {id: 'archive', active: false, status: 'proved', children: [{id: 'hidden', active: true, status: 'proved'}]},
 {id: 'visible', status: 'in-progress'},
 {id: 'branch', status: 'exploring', children: [{id: 'off', active: false, status: 'killed'}]}
]};
assert.deepEqual(clone(Tree.getStats(statsFixture)), {leaves:2, proved:0, compiled:0, killed:0, inProgress:1, exploring:1, computed:0, blocked:0, unstarted:0, total:3});
assert.equal(Tree.getStats({id: 'off-root', active: false, children: statsFixture.children}).total, 0);
State.setTree(original);
State.save();
State.init();
assert.deepEqual(clone(State.getTree()), original, 'persistence roundtrip preserves default data');
// Already-applied patch revisions must not overwrite local state on a new board.
const revisionFixture = {id:'rev-root', planningRevision:5, title:'local', children:[]};
State.setTree(revisionFixture);
assert.equal(State.applyPlanningBoard({revision:6, patches:[
 {revision:5, id:'rev-root', title:'historical'},
 {revision:6, id:'rev-root', active:true}
]}), true);
assert.equal(State.getTree().title, 'local');
assert.equal(State.getTree().active, true);
State.setTree(original);
// Validate final effective fields: the board intentionally retains historical overrides.
const integrationPath = process.argv[2] || base + 'planning.json';
if (integrationPath) {
 const integration = JSON.parse(fs.readFileSync(integrationPath, 'utf8'));
 function verifyIntegration(before, label) {
  State.setTree(clone(before));
  const payloadSnapshot = JSON.stringify(integration);
  assert.equal(State.applyPlanningBoard(integration), true);
  assert.equal(JSON.stringify(integration), payloadSnapshot, 'board payload remains immutable');
  const integrated = flatten(State.getTree());
  assert.equal(new Set(integrated.map(n => n.id)).size, integrated.length, 'no duplicate IDs: ' + label);
  for (const old of flatten(before)) {
   const n = Tree.findNode(State.getTree(), old.id);
   assert(n, 'preserve old ID: ' + old.id);
   if(old.status === 'proved') assert.equal(n.status, 'proved', 'preserve checked green: '+old.id);
   for (const note of old.notes || []) assert((n.notes || []).some(x => x.time === note.time && x.text === note.text), 'preserve history: ' + old.id);
  }
  const expected = new Map();
  const parents = new Map();
  for (const patch of integration.patches || []) {
   if (patch.revision != null && patch.revision <= (before.planningRevision || 0)) continue;
   if (patch.op === 'insert') continue;
   if (patch.op === 'move') { parents.set(patch.id, patch.parentId); continue; }
   const fields = expected.get(patch.id) || {};
   for (const key of ['title', 'active', 'status', 'expanded']) if (patch[key] != null) fields[key] = patch[key];
   expected.set(patch.id, fields);
  }
  for (const [id, fields] of expected) {
   const n = Tree.findNode(State.getTree(), id);
   if (!n) continue; // Historical patches can refer to nodes not inserted in that revision.
   for (const [key, value] of Object.entries(fields)) assert.equal(n[key], value, label + ': ' + id + '.' + key);
  }
  for (const [id, parentId] of parents) if (Tree.findNode(State.getTree(), id)) assert.equal(Tree.findParent(State.getTree(), id)?.id, parentId);
  const root = State.getTree();
  assert.equal(root.id, '4ct');
  assert.equal(root.title, 'Four Colour Theorem');
  assert.equal(root.active, true);
  assert.equal(Tree.findNode(root, 'structural-four-colour').active, true);
  assert.equal(Tree.findNode(root, 'structural-gate-a').status, 'proved');
  assert.equal(Tree.findNode(root, 'structural-gate-b').status, 'proved');
  assert.equal(Tree.findNode(root, 'structural-gate-d').status, 'exploring');
  assert.equal(Tree.findNode(root, 'structural-gate-e').status, 'unstarted');
  assert.equal(Tree.findNode(root, 'historical-research').active, false);
  assert.equal(Tree.findNode(root, 'historical-research').title, 'Route integration log');
  for(let i=1;i<=8;i++) {
   assert.equal(Tree.findParent(root, 'track'+i).id, '4ct');
   assert.equal(Tree.findNode(root, 'track'+i).active, true);
  }
  assert.equal(Tree.findNode(root, 'foundation').status, 'proved');
  assert.equal(Tree.findNode(root, 'f5-lean').status, 'proved');
  assert.equal(Tree.findParent(root, 'f2').id, 'structural-gate-f');
  assert.equal(Tree.findParent(root, 'structural-a-extension').id, 'structural-a-rotation');
  assert.equal(Tree.findNode(root, 'structural-a-extension').status, 'proved');
  assert.equal(Tree.findNode(root, 'structural-b-eleven').status, 'proved');
  assert.equal(Tree.findNode(root, 'structural-b-certificate').status, 'proved');
  assert.equal(Tree.findNode(root, 'structural-b-icosahedron').status, 'proved');
  assert.equal(Tree.findNode(root, 'structural-c-kittell').status, 'computed');
  assert.equal(Tree.findNode(root, 'structural-c-sigma').status, 'killed');
  assert.equal(Tree.findParent(root, 'structural-c-semantics').id, 'structural-gate-c');
  assert.equal(Tree.findNode(root, 'structural-c-semantics').status, 'unstarted');
  assert.equal(Tree.findNode(root, 'structural-d-root').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-d-recursive').id, 'structural-gate-d');
  assert.equal(Tree.findNode(root, 'structural-d-recursive').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-mass-descent').id, 'structural-contact');
  assert.equal(Tree.findNode(root, 'structural-mass-descent').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-component-mass-rank').id, 'structural-mass-descent');
  assert.equal(Tree.findNode(root, 'structural-component-mass-rank').status, 'killed');
  assert.equal(Tree.findParent(root, 'structural-component-mass-two-swap').id, 'structural-mass-descent');
  assert.equal(Tree.findNode(root, 'structural-component-mass-two-swap').status, 'computed');
  assert.equal(Tree.findNode(root, 'structural-mass-select').status, 'unstarted');
  assert.equal(Tree.findNode(root, 'structural-mass-corpus').status, 'computed');
  assert.equal(Tree.findParent(root, 'structural-mass-corpus').id, 'structural-mass-descent');
  assert.equal(Tree.findNode(root, 'structural-candidate-set').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-s0').id, 'structural-candidate-set');
  assert.equal(Tree.findNode(root, 'structural-s0').status, 'killed');
  assert.equal(Tree.findNode(root, 'structural-s1').status, 'killed');
  assert.equal(Tree.findNode(root, 'structural-s2').status, 'unstarted');
  assert.equal(Tree.findParent(root, 'structural-mass-invariance').id, 'structural-mass-descent');
  assert.equal(Tree.findNode(root, 'structural-mass-invariance').status, 'exploring');
  assert.equal(Tree.findNode(root, 'structural-rule-adversary').status, 'computed');
  assert.equal(Tree.findParent(root, 'structural-breadcrumb-descent').id, 'structural-contact');
  assert.equal(Tree.findParent(root, 'f-deg4-step').id, 'f-chain-eq');
  assert.equal(Tree.findParent(root, 'f-jordan-even').id, 'f-planemap-core');
  assert.equal(Tree.findParent(root, 'f-heawood-bridge').id, 'f-jordan-even');
  assert.equal(Tree.findParent(root, 'f5').id, 'f-heawood-bridge');
  assert.equal(Tree.findParent(root, 'f4').id, 'f1');
  assert.equal(Tree.findParent(root, 'structural-gate-b').id, 'structural-gate-a');
  assert.equal(Tree.findParent(root, 'structural-b-twelve').id, 'structural-b-rank');
  assert.equal(Tree.findParent(root, 'structural-b-eleven').id, 'structural-b-twelve');
  assert.equal(Tree.findParent(root, 'structural-gate-e').id, 'structural-gate-d');
  assert.equal(Tree.findParent(root, 'structural-rank-validation').id, 'structural-rank-discovery');
  assert.equal(Tree.findParent(root, 'structural-long-fill').id, 'structural-m3');
  assert.equal(Tree.findParent(root, 'structural-six-choice').id, 'structural-six-outside');
  assert.equal(Tree.findNode(root, 'structural-breadcrumb-descent').status, 'exploring');
  const gateD = Tree.findNode(root, 'structural-gate-d');
  const gateIds = gateD.children.map(child => child.id);
  assert.equal(gateIds[0], 'structural-contact');
  assert.equal(gateIds[1], 'structural-triangulation-completion');
  assert.equal(gateIds[2], 'structural-mass-select');
  assert.equal(gateIds.includes('structural-mass-descent'), false);
  assert.equal(gateIds.includes('structural-gate-e'), true);
  assert.equal(Tree.findParent(root, 'structural-breadcrumb-corpus').id, 'structural-breadcrumb-descent');
  assert.equal(Tree.findNode(root, 'structural-breadcrumb-corpus').status, 'computed');
  assert.equal(Tree.findNode(root, 'structural-breadcrumb-warnings').status, 'exploring');
  assert.equal(Tree.findNode(root, 'structural-breadcrumb-invariance').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-recursion-trace').id, 'structural-d-recursive');
  assert.equal(Tree.findNode(root, 'structural-recursion-trace').status, 'unstarted');
  assert.equal(Tree.findParent(root, 'structural-chord-availability').id, 'structural-edge-insertion');
  assert.equal(Tree.findNode(root, 'structural-chord-availability').status, 'proved');
  assert.equal(Tree.findNode(root, 'structural-edge-insertion').status, 'proved');
  assert.equal(Tree.findNode(root, 'structural-triangulation-completion').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-completion-exists').id, 'structural-triangulation-completion');
  assert.equal(Tree.findNode(root, 'structural-completion-exists').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-wp7').id, 'structural-mass-descent');
  assert.equal(Tree.findNode(root, 'structural-wp7').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-wp7-dominance').id, 'structural-wp7');
  assert.equal(Tree.findNode(root, 'structural-wp7-dominance').status, 'killed');
  assert.equal(Tree.findParent(root, 'structural-wp7-lean').id, 'structural-wp7');
  assert.equal(Tree.findNode(root, 'structural-wp7-lean').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-wp7d-c7d').id, 'structural-wp7d');
  assert.equal(Tree.findNode(root, 'structural-wp7d-c7d').status, 'computed');
  assert.equal(Tree.findParent(root, 'structural-wp7d-hub').id, 'structural-wp7d');
  assert.equal(Tree.findNode(root, 'structural-wp7d-hub').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-search-programmes').id, 'structural-contact');
  assert.equal(Tree.findNode(root, 'structural-search-programmes').status, 'exploring');
  assert.equal(Tree.findNode(root, 'structural-rank-synthesis').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-rank-discovery').id, 'structural-rank-synthesis');
  assert.equal(Tree.findNode(root, 'structural-rank-discovery').status, 'computed');
  assert.equal(Tree.findParent(root, 'structural-rank-replay').id, 'structural-rank-synthesis');
  assert.equal(Tree.findNode(root, 'structural-rank-replay').status, 'computed');
  assert.equal(Tree.findParent(root, 'structural-rank-validation').id, 'structural-rank-discovery');
  assert.equal(Tree.findNode(root, 'structural-rank-validation').status, 'computed');
  assert.equal(Tree.findParent(root, 'structural-ranked-contact').id, 'structural-contact');
  assert.equal(Tree.findNode(root, 'structural-ranked-contact').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-singleton-exterior').id, 'structural-wp7-lean');
  assert.equal(Tree.findNode(root, 'structural-singleton-exterior').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-curvature-charge').id, 'structural-mass-descent');
  assert.equal(Tree.findNode(root, 'structural-curvature-charge').status, 'killed');
  assert.equal(Tree.findParent(root, 'structural-receiver').id, 'structural-mass-descent');
  assert.equal(Tree.findNode(root, 'structural-receiver').status, 'unstarted');
  assert.equal(Tree.findParent(root, 'structural-vacancy').id, 'structural-mass-descent');
  assert.equal(Tree.findNode(root, 'structural-vacancy').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-equal-pole').id, 'structural-vacancy');
  assert.equal(Tree.findNode(root, 'structural-equal-pole').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-unequal-poles').id, 'structural-vacancy');
  assert.equal(Tree.findNode(root, 'structural-unequal-poles').status, 'compiled');
  assert.equal(Tree.findParent(root, 'structural-wp18').id, 'structural-vacancy');
  assert.equal(Tree.findNode(root, 'structural-wp18').status, 'computed');
  assert.equal(Tree.findParent(root, 'structural-wp19').id, 'structural-vacancy');
  assert.equal(Tree.findNode(root, 'structural-wp19').status, 'computed');
  assert.equal(Tree.findParent(root, 'structural-wp19-c1').id, 'structural-wp19');
  assert.equal(Tree.findNode(root, 'structural-wp19-c1').status, 'killed');
  assert.equal(Tree.findNode(root, 'structural-wp19-c3').status, 'killed');
  assert.equal(Tree.findNode(root, 'structural-wp19-m2').status, 'killed');
  assert.equal(Tree.findParent(root, 'structural-m3').id, 'structural-swap-budget');
  assert.equal(Tree.findNode(root, 'structural-m3').status, 'compiled');
  assert.equal(Tree.findParent(root, 'structural-m3-family').id, 'structural-wp18-bound-two');
  assert.equal(Tree.findParent(root, 'structural-l3').id, 'structural-long-fill');
  assert.equal(Tree.findNode(root, 'structural-l3').status, 'compiled');
  assert.equal(Tree.findParent(root, 'structural-axis-symmetry').id, 'structural-m3-family');
  assert.equal(Tree.findNode(root, 'structural-axis-symmetry').status, 'killed');
  assert.equal(Tree.findParent(root, 'structural-vhe-obstruction').id, 'structural-vacancy');
  assert.equal(Tree.findNode(root, 'structural-vhe-obstruction').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-vhe-potential').id, 'structural-vacancy');
  assert.equal(Tree.findNode(root, 'structural-vhe-potential').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-fixed-hole-triangle').id, 'structural-vhe-obstruction');
  assert.equal(Tree.findNode(root, 'structural-fixed-hole-triangle').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-face-reduction').id, 'structural-vhe-obstruction');
  assert.equal(Tree.findNode(root, 'structural-face-reduction').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-clique-lift').id, 'structural-vhe-obstruction');
  assert.equal(Tree.findNode(root, 'structural-clique-lift').status, 'compiled');
  assert.equal(Tree.findParent(root, 'structural-deg5-mobility').id, 'structural-vhe-obstruction');
  assert.equal(Tree.findNode(root, 'structural-deg5-mobility').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-free-quad-game').id, 'structural-vhe-obstruction');
  assert.equal(Tree.findNode(root, 'structural-free-quad-game').status, 'killed');
  assert.equal(Tree.findNode(root, 'structural-m3-family').status, 'proved');
  for (const [id, parent, status] of [
    ['structural-trace-lift','structural-vhe-obstruction','proved'],
    ['structural-trace-five-cycle','structural-trace-lift','proved'],
    ['structural-math-horizon','structural-vacancy','in-progress'],
    ['structural-mobility-general-lean','structural-math-horizon','compiled'],
    ['structural-math-t2-attack','structural-math-t2','exploring'],
    ['structural-math-t3-attack','structural-math-t3','exploring'],
    ['structural-wp21','structural-sep-d1','unstarted'],
    ['structural-mobility-triangulated-lean','structural-math-horizon','compiled'],
    ['structural-n-disc-search','structural-math-t3-attack','exploring'],
    ['structural-n-pinch-t3','structural-math-t3-attack','exploring'],
    ['structural-trace-exploratory','structural-trace-lift','exploring'],
    ['structural-deg6-split','structural-vhe-obstruction','proved'],
    ['structural-tilley','structural-vacancy','exploring'],
    ['structural-tilley-bridge','structural-tilley','proved'],
    ['structural-lemma-f','structural-tilley','proved'],
    ['structural-sep-d1','structural-tilley','exploring'],
    ['structural-d1-rigid','structural-sep-d1','proved'],
    ['structural-wp20','structural-sep-d1','in-progress']]) {
    assert.equal(Tree.findParent(root, id).id, parent, id);
    assert.equal(Tree.findNode(root, id).status, status, id);
  }
  assert.equal(
    Tree.findNode(root, 'structural-wp21').title,
    'WP21: D1 and P on a fresh order, sample and adversarial search (announced; version 2 package planned, not started)'
  );
  assert.equal(Tree.isWorking('structural-wp20'), true);
  assert.equal(Tree.isWorking('structural-math-horizon'), true);
  assert.equal(Tree.isWorking('structural-vhe-potential'), false);
  assert.equal(Tree.isClosedEnd(Tree.findNode(root, 'f5-lean')), true);
  assert.equal(Tree.isOpenPath(Tree.findNode(root, 'f5-lean')), false);
  assert.equal(Tree.isClosedEnd(Tree.findNode(root, 'structural-contact')), false);
  assert(flatten(root).some(node => Tree.isOpenPath(node)), 'a proved or compiled node still opens');
  assert.equal(Tree.findParent(root, 'structural-wp18-bound-two').id, 'structural-wp18');
  assert.equal(Tree.findNode(root, 'structural-wp18-bound-two').status, 'killed');
  assert.equal(Tree.findNode(root, 'structural-swap-budget').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-frozen-branches').id, 'structural-swap-budget');
  assert.equal(Tree.findNode(root, 'structural-frozen-branches').status, 'computed');
  assert.equal(Tree.findNode(root, 'structural-slide-ranks').status, 'killed');
  assert.equal(Tree.findNode(root, 'structural-long-arc').status, 'exploring');
  assert.equal(Tree.findNode(root, 'structural-ion-path').status, 'computed');
  assert.equal(Tree.findNode(root, 'structural-route-b').status, 'unstarted');
  assert.equal(Tree.findNode(root, 'structural-beyond-20').status, 'unstarted');
  assert.equal(Tree.findParent(root, 'structural-wp12').id, 'structural-beyond-20');
  assert.equal(Tree.findNode(root, 'structural-wp12').status, 'unstarted');
  assert.equal(Tree.findParent(root, 'structural-wp7f-ht').id, 'structural-breadcrumb-warnings');
  assert.equal(Tree.findNode(root, 'structural-wp7f-ht').status, 'computed');
  assert.equal(Tree.findParent(root, 'structural-wp7g-lemma-w').id, 'structural-breadcrumb-warnings');
  assert.equal(Tree.findNode(root, 'structural-wp7g-lemma-w').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-wp7-charging').id, 'structural-wp7');
  assert.equal(Tree.findNode(root, 'structural-wp7-charging').status, 'killed');
  assert.equal(Tree.findNode(root, 'structural-wp7-ha').status, 'killed');
  assert.equal(Tree.findNode(root, 'structural-wp7-hb').status, 'killed');
  assert.equal(Tree.findNode(root, 'structural-wp7-hc').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-wp7d').id, 'structural-wp7');
  assert.equal(Tree.findNode(root, 'structural-wp7d').status, 'exploring');
  assert.equal(Tree.findParent(root, 'structural-wp7-singleton-target').id, 'structural-wp7-lean');
  assert.equal(Tree.findNode(root, 'structural-wp7-singleton-target').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-edge-insertion').id, 'structural-triangulation-completion');
  assert.equal(Tree.findNode(root, 'structural-support-relabel').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-contact').id, 'structural-gate-d');
  assert.equal(Tree.findNode(root, 'structural-contact').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-stitch').id, 'structural-triangulation-completion');
  assert.equal(Tree.findNode(root, 'structural-stitch').status, 'proved');
  assert.equal(Tree.findParent(root, 'structural-local-determinacy').id, 'structural-mass-descent');
  assert.equal(Tree.findNode(root, 'structural-local-determinacy').status, 'killed');
  assert.equal(Tree.findParent(root, 'structural-wp7g-colouring').id, 'structural-wp7g-lemma-w');
  assert.equal(Tree.findNode(root, 'structural-wp7g-colouring').status, 'unstarted');
  assert.equal(Tree.findParent(root, 'structural-distant-hub').id, 'structural-wp7d');
  assert.equal(Tree.findNode(root, 'structural-distant-hub').status, 'unstarted');
  assert.equal(Tree.findNode(root, 'structural-graph36-sigma-beta').status, 'computed');
  assert.equal(Tree.findNode(root, 'structural-d2'), null);
  assert.equal(root.planningRevision, integration.revision);
  const result = JSON.stringify(root);
  assert.equal(State.applyPlanningBoard(integration), false);
  assert.equal(JSON.stringify(State.getTree()), result);
  console.log(label + ' integration passed; active statistics:', clone(Tree.getStats(root)));
 }
 verifyIntegration(original, 'Fresh default');
 const board35={revision:35,patches:integration.patches.filter(p=>(p.revision||33)<=35),journal:[]};
 State.setTree(clone(original));State.applyPlanningBoard(board35);
 const cache35=clone(State.getTree());
 Tree.findNode(cache35,'track2').notes.push({time:'2026-10-04T12:00:00Z',text:'Preserve revision35 user note'});
 verifyIntegration(cache35,'Revision-35 cached');
 assert.equal(Tree.findParent(State.getTree(),'track2').id,'4ct');
 // Reconstruct the actual revision-33 cached tree by applying its actual board.
 // Add a representative user note/status to test preservation across migration.
 const existing = { revision:33, patches:integration.patches.filter(p => p.revision != null && p.revision <= 33), journal:[] };
 assert(existing.patches.length > 0, 'board carries original revision-33 migration patches');
 assert.equal(existing.revision, 33);
 State.setTree(clone(original));
 assert.equal(State.applyPlanningBoard(existing), true);
 const cached = clone(State.getTree());
 const tracked = Tree.findNode(cached, 'track1');
 assert(tracked);
 tracked.notes = tracked.notes || [];
 tracked.notes.push({time:'2026-10-04T12:34:56Z', text:'User-local migration sentinel'});
 tracked.status = 'in-progress';
 // Also preserve a user status on an untouched leaf.
 const patchedIds = new Set(integration.patches.filter(p => p.status != null).map(p => p.id));
 const untouched = flatten(cached).find(n => !(n.children || []).length && !patchedIds.has(n.id));
 assert(untouched);
 untouched.status = 'in-progress';
 tracked.localStatusHistory = [{status:'exploring', time:'2026-10-03T00:00:00Z'}];
 verifyIntegration(cached, 'Revision-33 cached');
 assert.equal(Tree.findNode(State.getTree(), 'track1').status, 'in-progress');
 assert.equal(Tree.findNode(State.getTree(), untouched.id).status, 'in-progress');
 assert.deepEqual(clone(Tree.findNode(State.getTree(), 'track1').localStatusHistory), tracked.localStatusHistory);
 assert.equal(Tree.findParent(State.getTree(), 'track1').id, '4ct');
}
console.log('Navigator regression checks passed: real data migration, title/active updates, ordering, history/ID preservation, revision idempotence, cycle guards, inactive statistics, persistence.');
