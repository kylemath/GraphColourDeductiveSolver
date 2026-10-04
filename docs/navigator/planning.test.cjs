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
assert.deepEqual(clone(Tree.getStats(statsFixture)), {leaves:2, proved:0, killed:0, inProgress:1, exploring:1, total:3});
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
  assert.equal(root.title, 'Structural constructive Four Colour');
  assert.equal(root.active, true);
  assert.equal(Tree.findNode(root, 'structural-four-colour').active, true);
  assert.equal(Tree.findNode(root, 'structural-gate-a').status, 'proved');
  assert.equal(Tree.findNode(root, 'structural-gate-b').status, 'proved');
  assert.equal(Tree.findNode(root, 'structural-gate-d').status, 'exploring');
  assert.equal(Tree.findNode(root, 'structural-gate-e').status, 'unstarted');
  assert.equal(Tree.findNode(root, 'historical-research').active, false);
  assert.equal(Tree.findParent(root, 'f2').id, 'structural-gate-f');
  const result = JSON.stringify(root);
  assert.equal(State.applyPlanningBoard(integration), false);
  assert.equal(JSON.stringify(State.getTree()), result);
  console.log(label + ' integration passed; active statistics:', clone(Tree.getStats(root)));
 }
 verifyIntegration(original, 'Fresh default');
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
 assert.equal(Tree.findParent(State.getTree(), 'track1').id, 'historical-research');
}
console.log('Navigator regression checks passed: real data migration, title/active updates, ordering, history/ID preservation, revision idempotence, cycle guards, inactive statistics, persistence.');
