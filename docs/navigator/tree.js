/* tree.js — Proof tree rendering, expand/collapse, selection, status propagation */

const Tree = (() => {
  let selectedId = null;
  let onSelectCallback = null;
  let onChangeCallback = null;

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

  function renderNode(parent, node, depth) {
    const div = document.createElement('div');
    div.className = 'tree-node';
    div.dataset.id = node.id;

    const hasChildren = node.children && node.children.length > 0;
    const isExpanded = node.expanded !== false;

    // Node row
    const row = document.createElement('div');
    row.className = 'node-row' + (node.id === selectedId ? ' selected' : '');

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
    if (node.status === 'proved') title.classList.add('proved-text');
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
    const result = { leaves: 0, proved: 0, killed: 0, inProgress: 0, exploring: 0, total: 0 };
    function visit(current) {
      if (current.active === false) return;
      result.total++;
      const children = (current.children || []).filter(child => child.active !== false);
      if (!children.length) {
        result.leaves++;
        const key = current.status === 'in-progress' ? 'inProgress' : current.status;
        if (['proved', 'killed', 'inProgress', 'exploring'].includes(key)) result[key]++;
      } else {
        children.forEach(visit);
      }
    }
    visit(node);
    return result;
  }

  function getSelectedId() { return selectedId; }
  function setSelectedId(id) { selectedId = id; }

  return {
    render, refreshTree, refreshSelection,
    setCallbacks, findNode, findParent, deleteNode, addChild,
    expandAll, collapseAll, getStats,
    getSelectedId, setSelectedId, countByStatus, countLeaves
  };
})();
