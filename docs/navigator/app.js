/* app.js — State persistence, event wiring, detail panel, journal */

/* ===== STATE MANAGEMENT ===== */
const State = (() => {
  const STORAGE_KEY = 'proofNavigator_tree';
  const JOURNAL_KEY = 'proofNavigator_journal';
  const memory = new Map();
  let tree = null;
  let journal = [];
  let persistent = true;

  function storageGet(key) {
    if (!persistent) return memory.has(key) ? memory.get(key) : null;
    try {
      return localStorage.getItem(key);
    } catch (e) {
      persistent = false;
      return memory.has(key) ? memory.get(key) : null;
    }
  }

  function storageSet(key, value) {
    memory.set(key, value);
    if (!persistent) return;
    try {
      localStorage.setItem(key, value);
    } catch (e) {
      persistent = false;
    }
  }

  function init() {
    const saved = storageGet(STORAGE_KEY);
    if (saved) {
      try { tree = JSON.parse(saved); } catch (e) { tree = JSON.parse(JSON.stringify(DEFAULT_TREE)); }
    } else {
      tree = JSON.parse(JSON.stringify(DEFAULT_TREE));
    }
    const savedJournal = storageGet(JOURNAL_KEY);
    if (savedJournal) {
      try { journal = JSON.parse(savedJournal); } catch (e) { journal = []; }
    }
  }

  function save() {
    storageSet(STORAGE_KEY, JSON.stringify(tree));
    storageSet(JOURNAL_KEY, JSON.stringify(journal));
  }

  function reset() {
    tree = JSON.parse(JSON.stringify(DEFAULT_TREE));
    journal = [];
    save();
  }

  function getTree() { return tree; }
  function setTree(t) { tree = t; save(); }
  function getJournal() { return journal; }

  function addJournalEntry(action, nodeName) {
    const entry = {
      time: new Date().toISOString(),
      action: action,
      node: nodeName || ''
    };
    journal.unshift(entry);
    if (journal.length > 500) journal.length = 500;
    save();
  }

  function exportJSON() {
    const data = { tree, journal, exportedAt: new Date().toISOString() };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'proof-navigator-' + new Date().toISOString().slice(0, 10) + '.json';
    a.click();
    URL.revokeObjectURL(url);
  }

  function importJSON(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        if (data.tree) { tree = data.tree; }
        if (data.journal) { journal = data.journal; }
        save();
        location.reload();
      } catch (err) {
        alert('Invalid JSON file.');
      }
    };
    reader.readAsText(file);
  }

  function canPersist() { return persistent; }

  function applyPlanningBoard(board) {
    const rev = board.revision || 0;
    if (rev <= (tree.planningRevision || 0)) return false;
    const previousRevision = tree.planningRevision || 0;
    for (const patch of board.patches || []) {
      if (patch.revision != null && patch.revision <= previousRevision) continue;
      if (patch.op === 'insert') {
        if (!patch.node || Tree.findNode(tree, patch.node.id)) continue;
        const parent = Tree.findNode(tree, patch.parentId);
        if (!parent) continue;
        parent.children = parent.children || [];
        const index = Number.isInteger(patch.index)
          ? Math.max(0, Math.min(patch.index, parent.children.length))
          : parent.children.length;
        parent.children.splice(index, 0, JSON.parse(JSON.stringify(patch.node)));
        parent.expanded = true;
        continue;
      }
      const node = Tree.findNode(tree, patch.id);
      if (!node) continue;
      if (patch.op === 'move') {
        const parent = Tree.findNode(tree, patch.parentId);
        const previous = Tree.findParent(tree, patch.id);
        // Preserve the node and its history; reject root moves and cycles.
        if (!parent || !previous || Tree.findNode(node, parent.id)) continue;
        previous.children = previous.children.filter(child => child.id !== node.id);
        parent.children = parent.children || [];
        const index = Number.isInteger(patch.index)
          ? Math.max(0, Math.min(patch.index, parent.children.length))
          : parent.children.length;
        parent.children.splice(index, 0, node);
        continue;
      }
      if (patch.title != null) node.title = patch.title;
      if (patch.expanded != null) node.expanded = patch.expanded;
      if (patch.active != null) node.active = patch.active;
      if (patch.status) node.status = patch.status;
      if (patch.evidence != null) node.evidence = patch.evidence;
      if (patch.approach) node.approach = patch.approach;
      if (patch.killCriteria != null) node.killCriteria = patch.killCriteria;
      if (patch.statement) node.statement = patch.statement;
      if (patch.files) {
        node.files = node.files || [];
        for (const f of patch.files) {
          if (!node.files.includes(f)) node.files.push(f);
        }
      }
      if (patch.notes) {
        node.notes = node.notes || [];
        for (const n of patch.notes) {
          if (!node.notes.some(x => x.time === n.time && x.text === n.text)) node.notes.push(n);
        }
      }
    }
    for (const entry of board.journal || []) {
      if (!journal.some(x => x.time === entry.time && x.action === entry.action)) {
        journal.unshift(entry);
      }
    }
    if (journal.length > 500) journal.length = 500;
    tree.planningRevision = rev;
    save();
    return true;
  }

  return { init, save, reset, getTree, setTree, getJournal, addJournalEntry, exportJSON, importJSON, canPersist, applyPlanningBoard };
})();


/* ===== DETAIL PANEL ===== */
const Detail = (() => {
  let currentNode = null;
  let autoSaveTimer = null;

  function show(node) {
    currentNode = node;
    const empty = document.getElementById('detail-empty');
    const content = document.getElementById('detail-content');
    empty.hidden = true;
    content.hidden = false;

    document.getElementById('detail-title').textContent = node.title;
    document.getElementById('detail-id').textContent = 'id: ' + node.id;
    document.getElementById('detail-status').value = node.status;
    document.getElementById('detail-statement').value = node.statement || '';
    document.getElementById('detail-approach').value = node.approach || '';
    document.getElementById('detail-kill').value = node.killCriteria || '';
    document.getElementById('detail-evidence').value = node.evidence || '';

    renderFiles(node);
    renderNotes(node);
    renderProgress(node);
  }

  function hide() {
    currentNode = null;
    document.getElementById('detail-empty').hidden = false;
    document.getElementById('detail-content').hidden = true;
    if (window.TreeView) window.TreeView.resize();
  }

  function getCurrent() { return currentNode; }

  function renderFiles(node) {
    const container = document.getElementById('detail-files');
    container.innerHTML = '';
    (node.files || []).forEach((f, i) => {
      const div = document.createElement('div');
      div.className = 'file-item';
      div.innerHTML = '<span>' + escapeHtml(f) + '</span><button class="remove-btn" data-idx="' + i + '">&times;</button>';
      div.querySelector('.remove-btn').addEventListener('click', () => {
        node.files.splice(i, 1);
        scheduleAutoSave();
        renderFiles(node);
      });
      container.appendChild(div);
    });
  }

  function renderNotes(node) {
    const container = document.getElementById('detail-notes');
    container.innerHTML = '';
    (node.notes || []).forEach((n) => {
      const div = document.createElement('div');
      div.className = 'note-item';
      const timeStr = new Date(n.time).toLocaleString();
      div.innerHTML = '<div class="note-time">' + timeStr + '</div><div class="note-text">' + escapeHtml(n.text) + '</div>';
      container.appendChild(div);
    });
  }

  function renderProgress(node) {
    const stats = node.active === false ? null : Tree.getStats(node);
    const leaves = stats ? stats.leaves : Tree.countLeaves(node);
    const proved = stats ? stats.proved : Tree.countByStatus(node, 'proved');
    const pct = leaves > 0 ? Math.round((proved / leaves) * 100) : 0;
    document.getElementById('detail-progress-fill').style.width = pct + '%';
    document.getElementById('detail-progress-text').textContent = proved + ' / ' + leaves + ' proved';
  }

  function scheduleAutoSave() {
    if (autoSaveTimer) clearTimeout(autoSaveTimer);
    autoSaveTimer = setTimeout(() => {
      State.save();
      Tree.refreshTree();
      updateGlobalProgress();
    }, 400);
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  return { show, hide, getCurrent, renderFiles, renderNotes, renderProgress, scheduleAutoSave, escapeHtml };
})();
window.NavigatorDetail = Detail;


/* ===== JOURNAL ===== */
function renderJournal() {
  const container = document.getElementById('journal-entries');
  container.innerHTML = '';
  const entries = State.getJournal();
  entries.slice(0, 100).forEach(e => {
    const div = document.createElement('div');
    div.className = 'journal-entry';
    const timeStr = new Date(e.time).toLocaleString();
    div.innerHTML = '<span class="je-time">' + timeStr + '</span> '
      + '<span class="je-action">' + Detail.escapeHtml(e.action) + '</span>'
      + (e.node ? ' <span class="je-node">' + Detail.escapeHtml(e.node) + '</span>' : '');
    container.appendChild(div);
  });
}


/* ===== GLOBAL PROGRESS ===== */
function updateGlobalProgress() {
  const stats = Tree.getStats(State.getTree());
  const bar = document.getElementById('global-progress-bar');
  const segments = [
    ['proved', 'Proved', 'var(--green)'],
    ['computed', 'Computed', 'var(--cyan)'],
    ['inProgress', 'In progress', 'var(--accent)'],
    ['exploring', 'Exploring', 'var(--purple)'],
    ['blocked', 'Blocked', 'var(--orange)'],
    ['unstarted', 'Unstarted', 'var(--text-2)'],
    ['killed', 'Killed', 'var(--red)']
  ];
  const leaves = stats.leaves;
  bar.replaceChildren();
  const labels = [];
  for (const [key, label, color] of segments) {
    const count = stats[key] || 0;
    if (!count || !leaves) continue;
    const seg = document.createElement('div');
    seg.className = 'progress-seg';
    seg.style.width = (count / leaves * 100) + '%';
    seg.style.background = color;
    seg.title = label + ': ' + count;
    bar.appendChild(seg);
    labels.push(count + ' ' + label.toLowerCase());
  }
  bar.title = labels.join(' · ');
  document.getElementById('global-progress-text').textContent = leaves + ' end branches';
}


/* ===== MODAL ===== */
function showModal(title, onConfirm) {
  document.getElementById('modal-overlay').hidden = false;
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-node-title').value = '';
  document.getElementById('modal-node-statement').value = '';
  document.getElementById('modal-node-approach').value = '';
  document.getElementById('modal-node-title').focus();

  const confirmBtn = document.getElementById('modal-confirm');
  const newConfirm = confirmBtn.cloneNode(true);
  confirmBtn.parentNode.replaceChild(newConfirm, confirmBtn);
  newConfirm.addEventListener('click', () => {
    const t = document.getElementById('modal-node-title').value.trim();
    if (!t) return;
    try {
      onConfirm({
        title: t,
        statement: document.getElementById('modal-node-statement').value.trim(),
        approach: document.getElementById('modal-node-approach').value.trim()
      });
    } finally {
      hideModal();
    }
  });
}

function hideModal() {
  document.getElementById('modal-overlay').hidden = true;
}

function generateId() {
  return 'n-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 6);
}


/* ===== INITIALIZATION ===== */
document.addEventListener('DOMContentLoaded', () => {
  window.State = State;
  window.Tree = Tree;
  State.init();

  Tree.setCallbacks(
    (node) => { Detail.show(node); },
    () => { State.save(); updateGlobalProgress(); }
  );

  function renderAll() {
    const tree = State.getTree();
    Tree.render(document.getElementById('tree-container'), tree, 0);
    updateGlobalProgress();
    renderJournal();
    if (window.TreeView) window.TreeView.refresh();
  }

  renderAll();
  if (!State.canPersist()) {
    const label = document.getElementById('project-name');
    if (label) label.textContent = 'Changes last until reload — export JSON to keep them';
  }

  // planning.json is the agent-editable board. A higher revision overlays
  // status, evidence, notes, and new nodes onto localStorage.
  fetch('planning.json', { cache: 'no-store' })
    .then(res => res.ok ? res.json() : null)
    .then(board => {
      if (board && State.applyPlanningBoard(board)) renderAll();
    })
    .catch(() => {});

  /* ---- Detail panel: auto-save on changes ---- */
  const fieldMap = [
    { el: 'detail-statement', key: 'statement' },
    { el: 'detail-approach', key: 'approach' },
    { el: 'detail-kill', key: 'killCriteria' },
    { el: 'detail-evidence', key: 'evidence' }
  ];

  fieldMap.forEach(({ el, key }) => {
    document.getElementById(el).addEventListener('input', () => {
      const node = Detail.getCurrent();
      if (!node) return;
      node[key] = document.getElementById(el).value;
      Detail.scheduleAutoSave();
    });
  });

  // Title edit
  document.getElementById('detail-title').addEventListener('blur', () => {
    const node = Detail.getCurrent();
    if (!node) return;
    const newTitle = document.getElementById('detail-title').textContent.trim();
    if (newTitle && newTitle !== node.title) {
      State.addJournalEntry('Renamed to "' + newTitle + '"', node.title);
      node.title = newTitle;
      Detail.scheduleAutoSave();
    }
  });

  // Status change
  document.getElementById('detail-status').addEventListener('change', (e) => {
    const node = Detail.getCurrent();
    if (!node) return;
    const oldStatus = node.status;
    node.status = e.target.value;
    State.addJournalEntry('Status: ' + oldStatus + ' \u2192 ' + node.status, node.title);
    State.save();
    Tree.refreshTree();
    updateGlobalProgress();
    renderJournal();
    Detail.renderProgress(node);
  });

  // Add file
  document.getElementById('btn-add-file').addEventListener('click', () => {
    const node = Detail.getCurrent();
    if (!node) return;
    const input = document.getElementById('new-file-input');
    const path = input.value.trim();
    if (!path) return;
    if (!node.files) node.files = [];
    node.files.push(path);
    input.value = '';
    State.save();
    Detail.renderFiles(node);
  });

  // Add note
  const addNote = () => {
    const node = Detail.getCurrent();
    if (!node) return;
    const input = document.getElementById('new-note-input');
    const text = input.value.trim();
    if (!text) return;
    if (!node.notes) node.notes = [];
    node.notes.unshift({ time: new Date().toISOString(), text });
    input.value = '';
    State.addJournalEntry('Note: ' + text.slice(0, 60), node.title);
    State.save();
    Detail.renderNotes(node);
    renderJournal();
  };

  document.getElementById('btn-add-note').addEventListener('click', addNote);
  document.getElementById('new-note-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addNote();
  });

  // Add child
  document.getElementById('btn-add-child').addEventListener('click', () => {
    const node = Detail.getCurrent();
    if (!node) return;
    showModal('Add Sub-goal to "' + node.title + '"', (data) => {
      const child = {
        id: generateId(),
        title: data.title,
        statement: data.statement,
        status: 'unstarted',
        approach: data.approach,
        killCriteria: '',
        files: [],
        notes: [],
        evidence: '',
        expanded: false,
        children: []
      };
      Tree.addChild(node.id, child);
      State.addJournalEntry('Created sub-goal "' + data.title + '"', node.title);
      State.save();
      Tree.refreshTree();
      updateGlobalProgress();
      renderJournal();
      Detail.show(node);
    });
  });

  // Add root-level node
  document.getElementById('btn-add-root').addEventListener('click', () => {
    const tree = State.getTree();
    showModal('Add Node to Root', (data) => {
      const child = {
        id: generateId(),
        title: data.title,
        statement: data.statement,
        status: 'unstarted',
        approach: data.approach,
        killCriteria: '',
        files: [],
        notes: [],
        evidence: '',
        expanded: false,
        children: []
      };
      Tree.addChild(tree.id, child);
      State.addJournalEntry('Created "' + data.title + '"', tree.title);
      State.save();
      Tree.refreshTree();
      updateGlobalProgress();
      renderJournal();
    });
  });

  // Delete node
  document.getElementById('btn-delete-node').addEventListener('click', () => {
    const node = Detail.getCurrent();
    if (!node) return;
    const tree = State.getTree();
    if (node.id === tree.id) { alert('Cannot delete root node.'); return; }
    if (!confirm('Delete "' + node.title + '" and all its children?')) return;
    State.addJournalEntry('Deleted "' + node.title + '"', '');
    Tree.deleteNode(tree, node.id);
    Detail.hide();
    State.save();
    Tree.refreshTree();
    updateGlobalProgress();
    renderJournal();
  });

  // Collapsible sections
  document.querySelectorAll('.collapse-toggle').forEach(toggle => {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('open');
      const body = toggle.nextElementSibling;
      if (body) body.classList.toggle('open');
    });
  });

  // Journal toggle
  document.getElementById('journal-toggle').addEventListener('click', () => {
    document.getElementById('journal-body').classList.toggle('open');
    document.getElementById('journal-caret').classList.toggle('open');
  });

  // Modal cancel
  document.getElementById('modal-cancel').addEventListener('click', hideModal);
  document.getElementById('modal-overlay').addEventListener('click', (e) => {
    if (e.target === document.getElementById('modal-overlay')) hideModal();
  });

  // Header buttons
  document.getElementById('btn-show-tree').addEventListener('click', () => Detail.hide());

  document.getElementById('btn-expand-all').addEventListener('click', () => {
    Tree.expandAll(State.getTree());
    State.save();
    Tree.refreshTree();
  });

  document.getElementById('btn-collapse-all').addEventListener('click', () => {
    const tree = State.getTree();
    tree.expanded = true;
    if (tree.children) tree.children.forEach(c => Tree.collapseAll(c));
    State.save();
    Tree.refreshTree();
  });

  document.getElementById('btn-export').addEventListener('click', () => {
    State.exportJSON();
    State.addJournalEntry('Exported project to JSON', '');
    renderJournal();
  });

  document.getElementById('btn-import').addEventListener('click', () => {
    document.getElementById('import-file').click();
  });

  document.getElementById('import-file').addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      State.importJSON(e.target.files[0]);
    }
  });

  document.getElementById('btn-reset').addEventListener('click', () => {
    if (!confirm('Reset to default? All changes will be lost.')) return;
    State.reset();
    location.reload();
  });

  // Keyboard: Enter on new-file-input
  document.getElementById('new-file-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') document.getElementById('btn-add-file').click();
  });
});
