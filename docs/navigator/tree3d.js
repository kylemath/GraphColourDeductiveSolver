import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const COLORS = {
  proved: '#3fb950',
  compiled: '#3fb950',
  computed: '#39d2c0',
  inProgress: '#58a6ff',
  exploring: '#bc8cff',
  blocked: '#d29922',
  unstarted: '#7d8590',
  killed: '#f85149'
};
const ORDER = ['proved', 'compiled', 'computed', 'inProgress', 'exploring', 'blocked', 'unstarted', 'killed'];
const REACH = {
  proved: 2.6,
  compiled: 2.6,
  computed: 1.7,
  inProgress: 1.2,
  exploring: 0.82,
  blocked: 0.28,
  unstarted: 0.34,
  killed: 0.1
};

function reachOf(node) {
  const mix = leafMix(node);
  const score = mix.reduce((sum, part) => sum + part.share * (REACH[part.key] ?? 0.4), 0);
  return Math.max(REACH.killed, score);
}

function statusKey(status) {
  return status === 'in-progress' ? 'inProgress' : status;
}

function leafMix(node) {
  if (!window.Tree || node.active === false) return [{ key: statusKey(node.status || 'unstarted'), share: 1 }];
  const active = (node.children || []).filter(child => child.active !== false);
  if (!active.length) return [{ key: statusKey(node.status || 'unstarted'), share: 1 }];
  const stats = Tree.getStats(node);
  if (!stats.leaves) return [{ key: statusKey(node.status || 'unstarted'), share: 1 }];
  return ORDER.filter(key => stats[key]).map(key => ({ key, share: stats[key] / stats.leaves }));
}

function activeChildren(node) {
  return (node.children || []).filter(child => child.active !== false);
}

function opensForward(node) {
  return activeChildren(node).some(child => child.status !== 'killed' && child.status !== 'proved' && child.status !== 'compiled' && child.status !== 'computed');
}

const CLOSED_END = 0.55;

function closedEnd(node) {
  return window.Tree && Tree.isClosedEnd(node);
}

function linkLength(node) {
  const children = activeChildren(node);
  if (closedEnd(node)) return CLOSED_END;
  if (!children.length) return reachOf(node);
  const key = statusKey(node.status);
  if ((key === 'proved' || key === 'compiled' || key === 'computed') && opensForward(node)) return REACH[key];
  return 1;
}

function norm(v) {
  const len = Math.hypot(v.x, v.y, v.z) || 1;
  return { x: v.x / len, y: v.y / len, z: v.z / len };
}

function layout(node, x, y, z, out, spin) {
  const children = activeChildren(node);
  const here = {
    id: node.id,
    title: node.title,
    x,
    y,
    z,
    reach: linkLength(node),
    node
  };
  out.push(here);
  if (!children.length) return here;
  const n = children.length;
  const splay = Math.min(1.15, 0.38 + n * 0.06);
  children.forEach((child, i) => {
    const len = linkLength(child);
    const angle = spin + (n === 1 ? 0.7 : (i / n) * Math.PI * 2);
    const horiz = len * Math.sin(splay);
    const vert = len * Math.cos(splay);
    const childDir = norm({ x: Math.cos(angle) * horiz, y: vert, z: Math.sin(angle) * horiz });
    const placed = layout(
      child,
      x + childDir.x * len,
      y + childDir.y * len,
      z + childDir.z * len,
      out,
      angle + Math.PI / Math.max(n, 2)
    );
    placed.parent = here;
  });
  return here;
}

const TreeView = {
  renderer: null,
  scene: null,
  camera: null,
  controls: null,
  host: null,
  pick: [],
  hoverId: null,
  frame: 0,

  rod(start, end, up, material, radius, id) {
    const dir = end.clone().sub(start);
    const length = Math.max(dir.length(), 0.001);
    const mesh = new THREE.Mesh(
      new THREE.CylinderGeometry(radius * 0.85, radius, length, 7),
      material
    );
    mesh.position.copy(start).add(end).multiplyScalar(0.5);
    mesh.quaternion.setFromUnitVectors(up, dir.normalize());
      mesh.userData.id = id;
      mesh.userData.kind = 'rod';
      return mesh;
  },

  mount() {
    this.host = document.getElementById('tree3d-host');
    if (!this.host || this.renderer) return;
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    this.renderer.setClearColor(0x0d1117, 1);
    this.host.appendChild(this.renderer.domElement);
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(40, 1, 0.1, 200);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.target.set(0, 2, 0);
    this.scene.add(new THREE.AmbientLight(0xffffff, 0.65));
    const sun = new THREE.DirectionalLight(0xffffff, 1.1);
    sun.position.set(4, 8, 6);
    this.scene.add(sun);
    const resize = new ResizeObserver(() => this.resize());
    resize.observe(this.host);
    this.renderer.domElement.addEventListener('pointerdown', (event) => this.onPick(event));
    this.renderer.domElement.addEventListener('pointermove', (event) => this.onHover(event));
    this.renderer.domElement.addEventListener('pointerleave', () => this.highlight(null));
    this.resize();
    const loop = () => {
      this.frame = requestAnimationFrame(loop);
      if (this.host.offsetParent !== null) {
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
      }
    };
    loop();
  },

  resize() {
    if (!this.renderer || !this.host) return;
    const w = this.host.clientWidth || 320;
    const h = this.host.clientHeight || 360;
    this.renderer.setSize(w, h, false);
    this.camera.aspect = w / Math.max(h, 1);
    this.camera.updateProjectionMatrix();
  },

  refresh() {
    if (!window.State || !window.Tree) return;
    this.mount();
    const root = State.getTree();
    if (!root || !this.scene) return;
    const placed = [];
    layout(root, 0, 0, 0, placed, 0);
    const old = this.scene.getObjectByName('proof-tree');
    if (old) this.scene.remove(old);
    const group = new THREE.Group();
    group.name = 'proof-tree';
    this.pick = [];
    const up = new THREE.Vector3(0, 1, 0);
    for (const item of placed) {
      const working = window.Tree && Tree.isWorking(item.id);
      const ended = closedEnd(item.node);
      const reach = item.reach || REACH.unstarted;
      const stub = reach <= REACH.killed + 0.02;
      const sphere = new THREE.Mesh(
        ended
          ? new THREE.OctahedronGeometry(0.11, 0)
          : new THREE.SphereGeometry(working ? 0.16 : stub ? 0.045 : 0.07, 16, 12),
        new THREE.MeshStandardMaterial({
          color: ended ? '#7ee787' : (COLORS[statusKey(item.node.status)] || COLORS.unstarted),
          emissive: working ? 0xbc8cff : 0x000000,
          emissiveIntensity: working ? 0.55 : 0,
          roughness: 0.45
        })
      );
      sphere.position.set(item.x, item.y, item.z);
      sphere.userData.id = item.id;
      sphere.userData.kind = 'node';
      sphere.userData.working = working;
      sphere.userData.closedEnd = ended;
      group.add(sphere);
      this.pick.push(sphere);
      if (!item.parent) continue;
      const girth = stub ? 0.02 : 0.024 + reach * 0.018;
      const coat = new THREE.MeshStandardMaterial({
        color: COLORS[statusKey(item.node.status)] || COLORS.unstarted,
        roughness: 0.5,
        metalness: 0.04,
        emissive: working ? 0x3a2458 : 0x000000,
        emissiveIntensity: working ? 0.35 : 0
      });
      const rod = this.rod(
        new THREE.Vector3(item.parent.x, item.parent.y, item.parent.z),
        new THREE.Vector3(item.x, item.y, item.z),
        up,
        coat,
        girth,
        item.id
      );
      rod.userData.working = working;
      rod.userData.parentId = item.parent.id;
      group.add(rod);
      this.pick.push(rod);
    }
    this.scene.add(group);
    const box = new THREE.Box3().setFromObject(group);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    this.controls.target.copy(center);
    const distance = Math.max(size.x, size.y, size.z, 4) * 1.35;
    this.camera.position.set(center.x + size.x * 0.08, center.y - size.y * 0.05, distance);
    this.controls.update();
    this.resize();
    this.hoverId = null;
  },

  paint(mesh, on) {
    const mat = mesh.material;
    if (!mat || !mat.emissive) return;
    if (on) {
      mat.emissive.setHex(0x58a6ff);
      mat.emissiveIntensity = mesh.userData.kind === 'rod' ? 0.45 : 0.9;
      return;
    }
    if (mesh.userData.working) {
      mat.emissive.setHex(mesh.userData.kind === 'rod' ? 0x3a2458 : 0xbc8cff);
      mat.emissiveIntensity = mesh.userData.kind === 'rod' ? 0.35 : 0.55;
      return;
    }
    mat.emissive.setHex(0x000000);
    mat.emissiveIntensity = 0;
  },

  highlight(id, mirror) {
    const next = id || null;
    if (this.hoverId === next) return;
    this.hoverId = next;
    for (const mesh of this.pick) this.paint(mesh, mesh.userData.id === next);
    if (mirror === false || !window.Tree) return;
    if (next) Tree.reveal(next);
    else Tree.setHovered(null);
  },

  onHover(event) {
    if (!this.camera || event.buttons) return;
    const hit = this.cast(event);
    this.highlight(hit && hit.object.userData.id);
  },

  cast(event) {
    const rect = this.renderer.domElement.getBoundingClientRect();
    const mouse = new THREE.Vector2(
      ((event.clientX - rect.left) / rect.width) * 2 - 1,
      -((event.clientY - rect.top) / rect.height) * 2 + 1
    );
    const ray = new THREE.Raycaster();
    ray.setFromCamera(mouse, this.camera);
    return ray.intersectObjects(this.pick, false)[0] || null;
  },

  onPick(event) {
    if (!this.camera || !window.NavigatorDetail || !window.Tree || !window.State) return;
    const hit = this.cast(event);
    if (!hit) return;
    const node = Tree.findNode(State.getTree(), hit.object.userData.id);
    if (node) NavigatorDetail.show(node);
  }
};

window.TreeView = TreeView;
document.addEventListener('DOMContentLoaded', () => TreeView.refresh());
