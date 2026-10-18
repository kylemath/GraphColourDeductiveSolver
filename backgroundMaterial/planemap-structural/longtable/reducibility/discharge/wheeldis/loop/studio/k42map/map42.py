"""Studio, 18 Oct (Long Table order after explore round 42): map the round-42 kills of R*'s privates into receiver
windows of the d = 7 big link vertices w2 and w4, whose (link, s) frames contain the privates.
- Verdicts: a k42 tag qualifies if C on both engines with one conservative X (k42/cut_kcc.out kc -C, and
  k42/cut_fixedkc.cfast cfast --fixed with kc's X, leftover 0), or D on both (cut_dfast.out D=true and kc D).
- For each qualifying (config, embedding image) of grow.py, and each frame F in {w2, w4}: if the image lies in
  F + F's link + F's s-ring, write the window f7_<link>_<s> in F's rotation order (frames: w2, w4, and the 7s s2, s3, s5 when the built patch contains
  their whole frame): image slots carry the
  configuration vertex's exact degree, the rest '.'.
- Soundness check (independent of grow.py): the configuration's interior must embed (exact degrees, induced,
  triangles onto triangles) into the receiver-arrangement model of the window. The model is u = F, w_i, s_i; edges
  u-w_i, w_i-w_{i+1}, s_i-w_i, s_i-w_{i+1}, and s_{i-1}-s_i iff w_i = 5. Hosts are only the window's exact slots.
  If two s images flank an unspecified w_i, the induced condition depends on w_i, so the frame is skipped.
Writes k42map.out (pat file with D=true lines and a cpat block file) and map42.txt (per hit: pass/fail and why)."""
import os, sys, re, itertools, collections
import networkx as nx
from networkx.algorithms import isomorphism as iso
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.normpath(os.path.join(H, '..', '..', 'k42'))
G = {'__file__': os.path.join(K, 'grow.py'), '__name__': 'grow'}; exec(open(G['__file__']).read(), G)
P, pa, pf = G['structure'](); fd = G['fixed_deg'](); VAR = G['VAR']
C = G['rsst']() + G['explore_kills']()
def nx_(x): return frozenset(e.strip() for e in x.strip('{}').split(','))
# --- verdicts ---
kcC, kcD, cfC, dfD = {}, set(), {}, set()
cur = None
for l in open(os.path.join(K, 'cut_kcc.out')):
    m = re.match(r'^(k42_\S+) r=', l)
    if m: cur = m.group(1); kcD.update([cur] if 'D=true' in l else []); continue
    m = re.search(r'C-REDUCIBLE X=(\{[^}]*\})', l)
    if m and cur: kcC[cur] = nx_(m.group(1))
for l in open(os.path.join(K, 'cut_fixedkc.cfast')):
    m = re.match(r'^(k42_\S+) r=', l)
    if m: cur = m.group(1); continue
    m = re.search(r'fixed X=(\{[^}]*\}) .*C-REDUCIBLE, leftover bad classes extending after contraction = 0$', l)
    if m and cur: cfC[cur] = nx_(m.group(1))
for l in open(os.path.join(K, 'cut_dfast.out')):
    if 'D=true' in l: dfD.add(l.split()[0])
okC = {t for t in kcC if cfC.get(t) == kcC[t]}; okD = dfD & kcD
# broad (Long Table 11:43Z): C only with a broad X; enters only if cfast's search X is accepted by kc -C2 -x with
# leftover 0 (loop/k3studio/k42broad_C2.kc; kc -C2 validated against cfast on this X shape in explore round 40, ad376d04)
cfS = {}
for l in open(os.path.join(K, 'cut.cfast')):
    m = re.match(r'^(k42_\S+) r=', l)
    if m: cur = m.group(1); continue
    m = re.search(r'C-REDUCIBLE with X=(\{[^}]*\})', l)
    if m and cur: cfS[cur] = nx_(m.group(1))
c2 = {}
for l in open(os.path.join(H, '..', '..', 'k3studio', 'k42broad_C2.kc')):
    m = re.match(r'^(k42_\S+) r=', l)
    if m: cur = m.group(1); continue
    m = re.match(r'^\s+X=(\{[^}]*\}) adm=yes leftover 0', l)
    if m and cur: c2[cur] = nx_(m.group(1))
okB = {t for t in c2 if cfS.get(t) == c2[t]} - okC
kcC.update({t: c2[t] for t in okB})
# --- frames of w2, w4 in the reference geometry ---
adj, name, faces = G['build2'](G['letters'](7, 7, (7,) * 6)); inv = {v: x for x, v in name.items()}
def frame(F):
    f = inv[F]; nb = adj[f]; tri = [t - {f} for t in faces if f in t]
    nxt = collections.defaultdict(set)
    for t in tri:
        a, b = sorted(t); nxt[a].add(b); nxt[b].add(a)
    start = min(nb); cyc = [start]; prev = None
    while True:
        c = sorted(nxt[cyc[-1]] - {prev} - set(cyc[1:]))[0] if len(cyc) > 1 else sorted(nxt[cyc[-1]])[0]
        if c == cyc[0]: break
        prev = cyc[-1]; cyc.append(c)
        if len(cyc) > len(nb): break
    assert len(cyc) == len(nb) == 7, (F, len(cyc), len(nb))
    sl = []
    for i in range(7):
        a, b = cyc[i], cyc[(i + 1) % 7]
        cm = (adj[a] & adj[b]) - {f}; assert len(cm) == 1; sl.append(cm.pop())
    return [name.get(x) for x in cyc], [name.get(x) for x in sl]
FR = {}
for F in (('w', 2), ('w', 4), ('s', 2), ('s', 3), ('s', 5)):   # every exact degree-7 vertex of R*'s 2-ball but u
    try: FR[F] = frame(F)
    except (AssertionError, IndexError, ValueError) as ex: print('frame %s not inside the built patch: %r' % (F, ex))
def model_ok(c, img_map, F, W, S):
    """the configuration (interior graph, exact degrees, triangles) embeds into the window's arrangement model."""
    nm, tag, U, g, E, tri = c
    Hh = nx.Graph(); deg = {}
    deg['u'] = 7
    for i in range(7):
        if W[i] != '.': deg[('w', i)] = int(W[i])
        if S[i] != '.': deg[('s', i)] = int(S[i])
    for v in deg: Hh.add_node(v, deg=deg[v])
    def e(a, b):
        if a in deg and b in deg: Hh.add_edge(a, b)
    for i in range(7):
        j = (i + 1) % 7
        e('u', ('w', i)); e(('w', i), ('w', j)); e(('s', i), ('w', i)); e(('s', i), ('w', j))
        if W[i] == '5': e(('s', (i - 1) % 7), ('s', i))
    Kg = nx.Graph(); Kg.add_nodes_from(U)
    for x in U:
        for y in E[x]: Kg.add_edge(x, y)
    nx.set_node_attributes(Kg, g, 'deg')
    GM = iso.GraphMatcher(Hh, Kg, node_match=lambda a, b: a['deg'] == b['deg'])
    for m in GM.subgraph_isomorphisms_iter():   # induced; check triangles map to triangles of the model
        inv_m = {b: a for a, b in m.items()}
        if all(all(Hh.has_edge(inv_m[x], inv_m[y]) for x, y in itertools.combinations(t, 2)) for t in tri): return True
    return False
out_D, out_C, out_B, rep = [], [], [], []; seen = set()
for c in C:
    for emb in G['embeddings'](c, P, pa, pf, fd):
        req = dict((v, c[3][u]) for u, v in emb if v not in fd)
        key = tuple(req.get(x, 0) for x in VAR)
        if key[0] == 5 or key[1] == 5: continue
        tag = 'k42_%s_%s' % (c[0].replace('.', 'o'), ''.join(str(k) if k else 'x' for k in key))
        kind = 'C' if tag in okC else 'D' if tag in okD else 'Cbroad' if tag in okB else None
        if kind is None: continue
        im = {v: c[3][u] for u, v in emb}
        for F, (lk, sv) in FR.items():
            slots = set(lk) | set(sv) | {F}
            if not set(im) <= slots: rep.append('%s %s frame %s: image leaves the frame (%s)' % (tag, c[1], F, ' '.join(str(x) for x in sorted(set(im) - slots, key=str)))); continue
            if F in im and im[F] != 7: rep.append('%s frame %s: centre degree %d' % (tag, F, im[F])); continue
            W = ''.join(str(im[x]) if x in im else '.' for x in lk); S = ''.join(str(im[x]) if x in im else '.' for x in sv)
            flank = [i for i in range(7) if S[(i - 1) % 7] != '.' and S[i] != '.' and W[i] == '.']
            if flank: rep.append('%s frame %s: s images flank an unspecified link slot %s, skipped' % (tag, F, flank)); continue
            if not model_ok(c, im, F, W, S): rep.append('%s frame %s window f7_%s_%s: MODEL CHECK FAILED' % (tag, F, W, S)); continue
            wn = 'f7_%s_%s' % (W, S)
            if wn in seen: rep.append('%s frame %s: window %s (duplicate)' % (tag, F, wn)); continue
            seen.add(wn); rep.append('%s %s frame %s: PASS window %s (%s)' % (tag, c[1], F, wn, kind))
            if kind == 'D': out_D.append('%s r=0 m=0 classes=0 ext=0 reached=0 D=true (derived from %s, %s; dfast + kc)' % (wn, tag, c[1]))
            elif kind == 'Cbroad': out_B.append('%s r=0 m=0 (derived from %s, %s) [broad]\n  C-REDUCIBLE (cfast search X accepted by kc -C2 -x, X = %s)' % (wn, tag, c[1], ','.join(sorted(kcC[tag]))))
            else: out_C.append('%s r=0 m=0 (derived from %s, %s)\n  C-REDUCIBLE (cfast --fixed and kc -C, X = %s)' % (wn, tag, c[1], ','.join(sorted(kcC[tag]))))
open(os.path.join(H, 'k42map_D.out'), 'w').write(''.join(l + '\n' for l in out_D))
open(os.path.join(H, 'k42map_C.cfast'), 'w').write(''.join(l + '\n' for l in out_C))
open(os.path.join(H, 'k42map_C_broad.cfast'), 'w').write(''.join(l + '\n' for l in out_B))
open(os.path.join(H, 'map42.txt'), 'w').write('# qualifying tags: C %d (%s), D %d (%s), broad C %d (%s)\n' % (len(okC), ' '.join(sorted(okC)), len(okD), ' '.join(sorted(okD)), len(okB), ' '.join(sorted(okB))) + '\n'.join(rep) + '\n')
print('qualifying: C %d, D %d, broad %d; windows: D %d, C %d, broad %d' % (len(okC), len(okD), len(okB), len(out_D), len(out_C), len(out_B)))
print('\n'.join(r for r in rep if 'PASS' in r or 'FAILED' in r))
