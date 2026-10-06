/* tree.js — Proof tree rendering, expand/collapse, selection, status propagation */

const Tree = (() => {
  let selectedId = null;
  let hoveredId = null;
  let onSelectCallback = null;
  let onChangeCallback = null;
  const WORKING = new Set([
    'structural-vacancy',
    'structural-vhe-obstruction',
    'structural-vhe-potential'
  ]);

  function setCallbacks(onSelect, onChange) {
    onSelectCallback = onSelect;
    onChangeCallback = onChange;
  }

  /* ---- Render the full tree into a container ---- */
  function render(container, node, depth) {
    if (depth === undefined) depth = 0;
    container.innerHTML = '';
    renderNode(container, node, depth);
  }

  const COAT = [
    ['proved', 'var(--green)'],
    ['compiled', 'var(--green)'],
    ['computed', 'var(--cyan)'],
    ['inProgress', 'var(--accent)'],
    ['exploring', 'var(--purple)'],
    ['blocked', 'var(--orange)'],
    ['unstarted', 'var(--text-2)'],
    ['killed', 'var(--red)']
  ];

  function statusColor(status) {
    if (status === 'in-progress') return 'var(--accent)';
    const row = COAT.find(([key]) => key === status);
    return row ? row[1] : 'var(--text-2)';
  }

  function coatOf(node, direction) {
    if (node.active === false) return 'var(--text-2)';
    const activeChildren = (node.children || []).filter(child => child.active !== false);
    if (!activeChildren.length) return statusColor(node.status);
    const stats = getStats(node);
    if (!stats.leaves) return statusColor(node.status);
    let covered = 0;
    const stops = [];
    for (const [key, color] of COAT) {
      const count = stats[key] || 0;
      if (!count) continue;
      const start = covered / stats.leaves * 100;
      covered += count;
      const end = covered / stats.leaves * 100;
      stops.push(color + ' ' + start + '% ' + end + '%');
    }
    return 'linear-gradient(to ' + direction + ', ' + stops.join(', ') + ')';
  }

  function renderNode(parent, node, depth) {
    const div = document.createElement('div');
    div.className = 'tree-node' + (depth === 0 ? ' is-root' : '') + (node.active === false ? ' inactive' : '');
    div.dataset.id = node.id;
    div.style.setProperty('--arm', coatOf(node, 'right'));
    div.style.setProperty('--coat', coatOf(node, 'bottom'));

    const hasChildren = node.children && node.children.length > 0;
    const isExpanded = node.expanded !== false;

    // Node row
    const row = document.createElement('div');
    row.className = 'node-row'
      + (node.id === selectedId ? ' selected' : '')
      + (node.id === hoveredId ? ' hovered' : '')
      + (WORKING.has(node.id) ? ' working' : '');

    // Toggle arrow
    const toggle = document.createElement('span');
    toggle.className = 'node-toggle' + (isExpanded ? ' expanded' : '') + (!hasChildren ? ' leaf' : '');
    toggle.textContent = '\u25B6';
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      node.expanded = !node.expanded;
      if (onChangeCallback) onChangeCallback();
      refreshTree();
    });

    // Status dot
    const status = document.createElement('span');
    status.className = 'node-status ' + node.status;

    // Title
    const title = document.createElement('span');
    title.className = 'node-title';
    if (node.status === 'killed') title.classList.add('killed-text');
    if (node.status === 'proved' || node.status === 'compiled') title.classList.add('proved-text');
    title.textContent = node.title;

    // Child count badge
    if (hasChildren) {
      const stats = node.active === false ? null : getStats(node);
      const proved = stats ? stats.proved : countByStatus(node, 'proved');
      const total = stats ? stats.leaves : countLeaves(node);
      const badge = document.createElement('span');
      badge.className = 'node-count';
      badge.textContent = proved + '/' + total;
      row.appendChild(toggle);
      row.appendChild(status);
      row.appendChild(title);
      row.appendChild(badge);
    } else {
      row.appendChild(toggle);
      row.appendChild(status);
      row.appendChild(title);
    }

    // Click to select
    row.addEventListener('click', () => {
      selectedId = node.id;
      if (onSelectCallback) onSelectCallback(node);
      refreshSelection();
    });
    row.addEventListener('mouseenter', () => {
      setHovered(node.id);
      if (window.TreeView) window.TreeView.highlight(node.id, false);
    });
    row.addEventListener('mouseleave', () => {
      if (hoveredId !== node.id) return;
      setHovered(null);
      if (window.TreeView) window.TreeView.highlight(null, false);
    });

    div.appendChild(row);

    // Children container
    if (hasChildren) {
      const childContainer = document.createElement('div');
      childContainer.className = 'node-children' + (isExpanded ? '' : ' collapsed');
      for (const child of node.children) {
        renderNode(childContainer, child, depth + 1);
      }
      div.appendChild(childContainer);
    }

    parent.appendChild(div);
  }

  /* ---- Refresh just the selection highlights ---- */
  function refreshSelection() {
    document.querySelectorAll('.node-row.selected').forEach(el => el.classList.remove('selected'));
    if (selectedId) {
      const target = document.querySelector(`.tree-node[data-id="${selectedId}"] > .node-row`);
      if (target) target.classList.add('selected');
    }
  }

  /* ---- Re-render the entire tree (preserves scroll) ---- */
  function refreshTree() {
    const container = document.getElementById('tree-container');
    const scrollTop = container.scrollTop;
    const root = State.getTree();
    render(container, root, 0);
    container.scrollTop = scrollTop;
  }

  /* ---- Count helpers ---- */
  function countByStatus(node, status) {
    let c = 0;
    if (!node.children || node.children.length === 0) {
      return node.status === status ? 1 : 0;
    }
    for (const child of node.children) {
      c += countByStatus(child, status);
    }
    return c;
  }

  function countLeaves(node) {
    if (!node.children || node.children.length === 0) return 1;
    let c = 0;
    for (const child of node.children) {
      c += countLeaves(child);
    }
    return c;
  }

  function countAll(node) {
    let c = 1;
    if (node.children) {
      for (const child of node.children) {
        c += countAll(child);
      }
    }
    return c;
  }

  /* ---- Tree manipulation ---- */
  function findNode(node, id) {
    if (node.id === id) return node;
    if (node.children) {
      for (const child of node.children) {
        const found = findNode(child, id);
        if (found) return found;
      }
    }
    return null;
  }

  function findParent(node, id) {
    if (node.children) {
      for (const child of node.children) {
        if (child.id === id) return node;
        const found = findParent(child, id);
        if (found) return found;
      }
    }
    return null;
  }

  function deleteNode(tree, id) {
    if (tree.id === id) return false;
    const parent = findParent(tree, id);
    if (parent) {
      parent.children = parent.children.filter(c => c.id !== id);
      return true;
    }
    return false;
  }

  function addChild(parentId, childData) {
    const tree = State.getTree();
    const parent = findNode(tree, parentId);
    if (!parent) return false;
    if (!parent.children) parent.children = [];
    parent.children.push(childData);
    parent.expanded = true;
    return true;
  }

  function expandAll(node) {
    node.expanded = true;
    if (node.children) node.children.forEach(c => expandAll(c));
  }

  function collapseAll(node) {
    node.expanded = false;
    if (node.children) node.children.forEach(c => collapseAll(c));
  }

  /* ---- Global stats ---- */
  function getStats(node) {
    const result = { leaves: 0, proved: 0, compiled: 0, killed: 0, inProgress: 0, exploring: 0, computed: 0, blocked: 0, unstarted: 0, total: 0 };
    function visit(current) {
      if (current.active === false) return;
      result.total++;
      const children = (current.children || []).filter(child => child.active !== false);
      if (!children.length) {
        result.leaves++;
        const key = current.status === 'in-progress' ? 'inProgress' : current.status;
        if (Object.prototype.hasOwnProperty.call(result, key)) result[key]++;
      } else {
        children.forEach(visit);
      }
    }
    visit(node);
    return result;
  }

  function getSelectedId() { return selectedId; }
  function setSelectedId(id) { selectedId = id; }
  function isWorking(id) { return WORKING.has(id); }

  function setHovered(id) {
    hoveredId = id || null;
    document.querySelectorAll('.node-row.hovered').forEach(el => el.classList.remove('hovered'));
    if (!hoveredId) return null;
    const row = document.querySelector('.tree-node[data-id="' + hoveredId + '"] > .node-row');
    if (row) row.classList.add('hovered');
    return row;
  }

  function reveal(id) {
    const root = State.getTree();
    if (!root || !findNode(root, id)) return;
    let parent = findParent(root, id);
    let opened = false;
    while (parent) {
      if (parent.expanded === false) {
        parent.expanded = true;
        opened = true;
      }
      parent = findParent(root, parent.id);
    }
    if (opened) refreshTree();
    const row = setHovered(id);
    if (row) row.scrollIntoView({ block: 'nearest' });
  }

  return {
    render, refreshTree, refreshSelection,
    setCallbacks, findNode, findParent, deleteNode, addChild,
    expandAll, collapseAll, getStats,
    getSelectedId, setSelectedId, countByStatus, countLeaves,
    isWorking, setHovered, reveal
  };
})();
