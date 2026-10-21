// EXPLORE round 33 (H-KC): an independent Kempe D-closure engine.
// C++ port of loop/kempe_w7_5666567.py (textbook Birkhoff/Heesch D-reducibility); no dfast/cfast/Lean source read.
//
// Input lines (stdin or file): name r m ringadj intadj   (the configuration format used across wheeldis)
//   ringadj: m ';'-separated lists of ring vertices adjacent to interior vertex j ('-' = none)
//   intadj:  m ';'-separated lists of interior neighbours of interior vertex j
// Output, one line per key:
//   name r=.. m=.. classes=.. ext=.. reached=.. D=true|false depth=.. passes=.. mode=gs|jacobi ..ms
//
// Definitions.  Ring colourings are proper 4-colourings of the ring cycle, up to the 24 colour permutations
// (canonical form: colours numbered by first appearance).  A class is good at the start if it extends to the
// interior.  For a pairing x in {1,2,3} ({0,x} | the other two), the ring splits into 2t maximal runs of one pair
// type ("ab" = colours {0,x}); every Kempe chain meets the ring in a union of runs, and the chains form a
// non-crossing partition of the runs whose blocks are type-monochromatic.  Finer partitions offer more swaps, so it
// is enough to test the coarsest ones: a non-crossing partition pi of the t ab-runs with the coarsest non-crossing
// partition of the cd-runs compatible with it (Kreweras complement, t + 1 blocks in all).  Swapping a set of chains
// is XOR by x on their ring vertices; a set and its complement give the same class, so the swaps are the nonempty
// unions of blocks that avoid the block of run 0.  A bad class becomes good if for some x, every coarsest partition
// has a swap landing on a good class.  D-reducible: the closure is every class.
//
// Options:  -j  Jacobi passes (new goods used from the next pass; depth comparable with dfast's)
//           -c FILE  checkpoint file (Gauss-Seidel only; resumes if present)   -t SEC  stop and checkpoint after SEC
//           -s SEC  checkpoint interval (default 600)   -v  per-pass log to stderr
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
typedef unsigned int u32;

static int n, m;
static u32 FULL;
static vector<u32> ringMask;          // interior j -> ring neighbours (bitmask)
static vector<vector<int>> intN;      // interior j -> interior neighbours

// ---------------- ranking of canonical ring colourings ----------------
static u64 CNT[34][5][2];             // completions from position i, used colours u, last colour == 0 ?
static u64 RA[34][5][4][4];           // rank offset at position i for choosing colour c (used u, last l)
static void build_rank() {
    for (int u = 0; u <= 4; u++) for (int z = 0; z < 2; z++) CNT[n][u][z] = z ? 0 : 1;   // ring closes: last != 0
    for (int i = n - 1; i >= 1; i--)
        for (int u = 1; u <= 4; u++)
            for (int z = 0; z < 2; z++) {
                u64 s = 0;
                if (!z) s += CNT[i + 1][u][1];                         // colour 0
                s += (u64)((u - 1) - (z ? 0 : 1)) * CNT[i + 1][u][0];  // a used nonzero colour other than the last
                if (u < 4) s += CNT[i + 1][u + 1][0];                  // a new colour
                CNT[i][u][z] = s;
            }
    for (int i = 1; i < n; i++)
        for (int u = 1; u <= 4; u++)
            for (int l = 0; l < 4; l++)
                for (int c = 0; c < 4; c++) {
                    u64 s = 0;
                    for (int cc = 0; cc < c; cc++) {
                        if (cc == l || cc > u || cc > 3) continue;
                        s += CNT[i + 1][max(u, cc + 1)][cc == 0 ? 1 : 0];
                    }
                    RA[i][u][l][c] = s;
                }
}
static inline u64 canon_rank(u32 q0, u32 q1) {
    u32 mk[4] = {~q0 & ~q1 & FULL, q0 & ~q1 & FULL, ~q0 & q1 & FULL, q0 & q1 & FULL};
    int f[4];
    for (int v = 0; v < 4; v++) f[v] = mk[v] ? __builtin_ctz(mk[v]) : 64;
    int lab[4];
    for (int v = 0; v < 4; v++) { lab[v] = 0; for (int w = 0; w < 4; w++) if (f[w] < f[v]) lab[v]++; }
    u64 r = 0; int used = 1, last = 0;
    for (int i = 1; i < n; i++) {
        int col = ((q0 >> i) & 1) | (((q1 >> i) & 1) << 1);
        int c = lab[col];
        r += RA[i][used][last][c];
        if (c == used) used++;
        last = c;
    }
    return r;
}

// chunked ranking: 4 positions per table lookup (state = (used - 1) * 4 + last)
struct RT { u32 d; uint8_t ns; };
static RT RTAB[9][16][256]; static int NCH;
static void build_rank_chunks() {
    NCH = (n - 1 + 3) / 4;
    for (int ch = 0; ch < NCH; ch++) {
        int lo = 1 + 4 * ch, len = min(4, n - lo);
        for (int st = 0; st < 16; st++)
            for (int code = 0; code < 256; code++) {
                int used = st / 4 + 1, last = st % 4; u64 r = 0; bool okk = true;
                for (int k = 0; k < len; k++) {
                    int c = ((code >> k) & 1) | (((code >> (4 + k)) & 1) << 1);
                    if (c == last || c > used || c > 3) { okk = false; break; }
                    r += RA[lo + k][used][last][c];
                    if (c == used) used++;
                    last = c;
                }
                RTAB[ch][st][code].d = okk ? (u32)r : 0;
                RTAB[ch][st][code].ns = okk ? (uint8_t)((used - 1) * 4 + last) : 0;
            }
    }
}
static inline u64 canon_rank2(u32 q0, u32 q1) {
    u32 mk[4] = {~q0 & ~q1 & FULL, q0 & ~q1 & FULL, ~q0 & q1 & FULL, q0 & q1 & FULL};
    int f[4];
    for (int v = 0; v < 4; v++) f[v] = mk[v] ? __builtin_ctz(mk[v]) : 64;
    u32 c0 = 0, c1 = 0;
    for (int v = 0; v < 4; v++) {
        int L = (f[0] < f[v]) + (f[1] < f[v]) + (f[2] < f[v]) + (f[3] < f[v]);
        if (L & 1) c0 |= mk[v];
        if (L & 2) c1 |= mk[v];
    }
    u64 r = 0; int st = 0;   // position 0 has colour 0: used 1, last 0
    for (int ch = 0; ch < NCH; ch++) {
        int lo = 1 + 4 * ch;
        int code = ((c0 >> lo) & 15) | (((c1 >> lo) & 15) << 4);
        const RT &e = RTAB[ch][st][code];
        r += e.d; st = e.ns;
    }
    return r;
}

// ---------------- coarsest admissible partitions per t ----------------
struct PSet { int t; vector<u32> blk; };   // per partition: t run-masks (blocks other than run 0's)
static PSet MAXP[11];
static void set_partitions(int t, vector<vector<vector<int>>> &out) {
    vector<vector<int>> cur;
    function<void(int)> rec = [&](int e) {
        if (e == t) { out.push_back(cur); return; }
        for (size_t b = 0; b < cur.size(); b++) { cur[b].push_back(e); rec(e + 1); cur[b].pop_back(); }
        cur.push_back({e}); rec(e + 1); cur.pop_back();
    };
    rec(0);
}
static bool crossing(const vector<vector<int>> &P) {
    for (size_t i = 0; i < P.size(); i++)
        for (size_t j = i + 1; j < P.size(); j++)
            for (int a1 : P[i]) for (int a2 : P[i]) if (a1 < a2)
                for (int b1 : P[j]) for (int b2 : P[j]) if (b1 < b2)
                    if ((a1 < b1 && b1 < a2 && a2 < b2) || (b1 < a1 && a1 < b2 && b2 < a2)) return true;
    return false;
}
static void build_maxp(int tmax) {
    for (int t = 1; t <= tmax; t++) {
        vector<vector<vector<int>>> parts; set_partitions(t, parts);
        PSet &ps = MAXP[t]; ps.t = t;
        for (auto &pi : parts) {
            if (crossing(pi)) continue;
            vector<vector<int>> ab;
            for (auto &B : pi) { vector<int> b; for (int i : B) b.push_back(2 * i); ab.push_back(b); }
            vector<int> par(2 * t);
            iota(par.begin(), par.end(), 0);
            function<int(int)> fnd = [&](int c) { while (par[c] != c) c = par[c]; return c; };
            auto sep = [&](int x, int y) {
                for (auto &B : ab) {
                    bool ins = false, outs = false;
                    for (int b : B) { if (x < b && b < y) ins = true; if (b < x || b > y) outs = true; }
                    if (ins && outs) return true;
                }
                return false;
            };
            for (int i = 0; i < t; i++)
                for (int j = i + 1; j < t; j++) {
                    int x = 2 * i + 1, y = 2 * j + 1;
                    if (!sep(x, y)) par[fnd(x)] = fnd(y);
                }
            map<int, vector<int>> cdb;
            for (int i = 0; i < t; i++) cdb[fnd(2 * i + 1)].push_back(2 * i + 1);
            vector<vector<int>> blocks = ab;
            for (auto &kv : cdb) blocks.push_back(kv.second);
            if ((int)blocks.size() != t + 1 || crossing(blocks)) { fprintf(stderr, "Kreweras check failed t=%d\n", t); exit(2); }
            int z = -1;
            for (size_t b = 0; b < blocks.size(); b++) for (int x : blocks[b]) if (x == 0) z = (int)b;
            for (size_t b = 0; b < blocks.size(); b++) if ((int)b != z) {
                u32 mm = 0; for (int x : blocks[b]) mm |= 1u << x; ps.blk.push_back(mm);
            }
        }
    }
}

// ---------------- configuration ----------------
static vector<int> order_;                       // interior colouring order
static vector<vector<int>> earlier;              // interior neighbours placed before j (by order position)
static bool parse(const string &line, string &name) {
    istringstream ss(line);
    string rs, ms, rp, ip;
    if (!(ss >> name >> rs >> ms >> rp >> ip)) return false;
    n = stoi(rs); m = stoi(ms);
    auto split = [](const string &s, char d) { vector<string> v; string x; for (char c : s) { if (c == d) { v.push_back(x); x.clear(); } else x += c; } v.push_back(x); return v; };
    auto R = split(rp, ';'), I = split(ip, ';');
    if ((int)R.size() != m || (int)I.size() != m) { fprintf(stderr, "%s: bad field counts\n", name.c_str()); return false; }
    ringMask.assign(m, 0); intN.assign(m, {});
    for (int j = 0; j < m; j++) {
        if (R[j] != "-" && !R[j].empty()) for (auto &x : split(R[j], ',')) ringMask[j] |= 1u << stoi(x);
        if (I[j] != "-" && !I[j].empty()) for (auto &x : split(I[j], ',')) intN[j].push_back(stoi(x));
    }
    for (int j = 0; j < m; j++) for (int i : intN[j])
        if (find(intN[i].begin(), intN[i].end(), j) == intN[i].end()) { fprintf(stderr, "%s: asymmetric %d-%d\n", name.c_str(), j, i); return false; }
    FULL = (n == 32) ? 0xffffffffu : ((1u << n) - 1);
    // order: most already-placed neighbours first (ring vertices count as placed)
    vector<int> placed(m, 0), pos(m, -1); order_.clear();
    for (int s = 0; s < m; s++) {
        int best = -1, bs = -1;
        for (int j = 0; j < m; j++) if (pos[j] < 0) {
            int sc = __builtin_popcount(ringMask[j]) * 1 + placed[j] * 1;
            if (sc > bs) { bs = sc; best = j; }
        }
        pos[best] = s; order_.push_back(best);
        for (int i : intN[best]) placed[i]++;
    }
    earlier.assign(m, {});
    for (int j = 0; j < m; j++) for (int i : intN[j]) if (pos[i] < pos[j]) earlier[j].push_back(i);
    return true;
}
static bool extends(u32 q0, u32 q1) {
    u32 mk[4] = {~q0 & ~q1 & FULL, q0 & ~q1 & FULL, ~q0 & q1 & FULL, q0 & q1 & FULL};
    static int col[64], forb[64], cand[64];
    for (int j = 0; j < m; j++) {
        int f = 0;
        for (int v = 0; v < 4; v++) if (ringMask[j] & mk[v]) f |= 1 << v;
        forb[j] = f;
    }
    int s = 0;
    // cand[s] = remaining colour candidates at depth s
    {
        int j = order_[0]; cand[0] = 15 & ~forb[j];
    }
    while (s >= 0) {
        if (!cand[s]) { s--; continue; }
        int j = order_[s];
        int c = __builtin_ctz(cand[s]); cand[s] &= cand[s] - 1; col[j] = c;
        if (s == m - 1) return true;
        s++;
        int jj = order_[s], a = 15 & ~forb[jj];
        for (int i : earlier[jj]) a &= ~(1 << col[i]);
        cand[s] = a;
    }
    return false;
}

// ---------------- closure ----------------
static vector<u64> reps;            // packed colouring: plane0 | plane1 << 32
static vector<u64> good, nxt;       // bitsets
static vector<uint16_t> wit;        // witness partition per (class, pairing)
static vector<u32> stamp; static vector<uint8_t> memo; static u32 cur = 0;
static inline bool isgood(u64 i) { return (good[i >> 6] >> (i & 63)) & 1; }
static inline void setb(vector<u64> &b, u64 i) { b[i >> 6] |= 1ULL << (i & 63); }

static bool try_pairing(u64 idx, u32 p0, u32 p1, int x) {
    u32 mk[4] = {~p0 & ~p1 & FULL, p0 & ~p1 & FULL, ~p0 & p1 & FULL, p0 & p1 & FULL};
    u32 ab = mk[0] | mk[x];
    u32 prev = ((ab << 1) | (ab >> (n - 1))) & FULL;   // bit i: type of i - 1
    u32 D = (ab ^ prev) & FULL;
    if (!D) return false;                               // one run: only the global swap
    int st[40], k2 = 0;
    for (u32 d = D; d; d &= d - 1) st[k2++] = __builtin_ctz(d);
    int t = k2 / 2, s0 = 0;
    while (!((ab >> st[s0]) & 1)) s0++;                 // run 0 is an ab run
    u32 runV[40];
    for (int q = 0; q < k2; q++) {
        int a = st[(s0 + q) % k2], b = st[(s0 + q + 1) % k2];
        u32 v = (b > a) ? (((b >= 32) ? 0xffffffffu : ((1u << b) - 1)) & ~((1u << a) - 1))
                        : ((FULL & ~((1u << a) - 1)) | ((1u << b) - 1));
        runV[q] = v;
    }
    if (++cur == 0) { fill(stamp.begin(), stamp.end(), 0); cur = 1; }
    const PSet &ps = MAXP[t];
    int np = (int)ps.blk.size() / t;
    uint16_t &w = wit[idx * 3 + (x - 1)];
    int w0 = (w < np) ? w : 0;
    u32 xa = (x & 1) ? 0xffffffffu : 0, xb = (x & 2) ? 0xffffffffu : 0;
    for (int pp = 0; pp < np; pp++) {
        int p = (w0 + pp) % np;
        const u32 *bl = &ps.blk[(size_t)p * t];
        u32 bV[12];
        for (int j = 0; j < t; j++) { u32 v = 0; for (u32 r = bl[j]; r; r &= r - 1) v |= runV[__builtin_ctz(r)]; bV[j] = v; }
        bool found = false; u32 R = 0, V = 0;
        for (u32 g = 1; g < (1u << t); g++) {
            int j = __builtin_ctz(g);
            R ^= bl[j]; V ^= bV[j];
            u32 key = R >> 1;
            bool val;
            if (stamp[key] == cur) val = memo[key];
            else { val = isgood(canon_rank2(p0 ^ (V & xa), p1 ^ (V & xb))); stamp[key] = cur; memo[key] = val; }
            if (val) { found = true; break; }
        }
        if (!found) { w = (uint16_t)p; return false; }
    }
    return true;
}

// ---------------- C-reducibility (round 35, H-KCC) ----------------
// Own derivation of the contract argument (no cfast/dfast/Lean source read).  X: 1..4 free-completion edges, each
// with an interior end.  Admissible (conservative): every component of (V, X) holds at most one ring vertex, and no
// free-completion edge outside X (ring edges included) joins two vertices of one component.  Then G/X is loopless
// and smaller, its 4-colouring restricts to a proper ring colouring that extends to K/X (each component one colour,
// every other edge proper), so K is C-reducible with X if no unreached class extends to K/X.
// Vertex ids: interior 0..m-1, ring k = m + k.
struct CEdge { int a, b; };
static vector<CEdge> cedges, alledges;          // X candidates; candidates + ring edges (loop check)
static void build_edges() {
    cedges.clear();
    for (int j = 0; j < m; j++) for (int i : intN[j]) if (j < i) cedges.push_back({j, i});
    for (int j = 0; j < m; j++) for (u32 r = ringMask[j]; r; r &= r - 1) cedges.push_back({m + __builtin_ctz(r), j});
    alledges = cedges;
    for (int k = 0; k < n; k++) alledges.push_back({m + k, m + (k + 1) % n});
}
static string xname(const vector<int> &X) {
    string s = "{";
    for (size_t q = 0; q < X.size(); q++) {
        const CEdge &e = cedges[X[q]]; char b[32];
        if (e.a >= m) snprintf(b, 32, "R%d-I%d", e.a - m, e.b); else snprintf(b, 32, "I%d-I%d", e.a, e.b);
        s += (q ? "," : ""); s += b;
    }
    return s + "}";
}
struct KX { int M; vector<int> pin; vector<u32> req; vector<u32> rforb; vector<int> order; vector<vector<int>> earlier; };
static int ufp[80];
// -C2 (broad): a component may hold several ring vertices.  Then r, r' are identified, which is safe unless an edge
// of G outside K joins them (a chord).  With the X-path P from r to r' (length l <= 4), a chord closes a cycle of
// length l + 1 that separates the two ring arcs between r and r'.  A minimal counterexample has no separating 3- or
// 4-cycle, and a separating 5-cycle has a single vertex on one side.  So l <= 3 is safe; l = 4 is safe unless r, r'
// are two apart on the ring and the ring vertex between them is adjacent to all three inner vertices of P (then that
// vertex alone could fill one side).  Any other shape (a ring vertex inside P) is refused.  A ring colouring is in
// C'(X) only if it gives the ring vertices of each component one colour.
static bool BROAD = false; static int LMAX = 4;   // -L k: refuse ring pairs at X-distance > k (experiments)
static int uff(int x) { while (ufp[x] != x) x = ufp[x] = ufp[ufp[x]]; return x; }
// builds K/X; returns false if X is not admissible
static bool build_kx(const vector<int> &X, KX &K) {
    int V = m + n;
    for (int v = 0; v < V; v++) ufp[v] = v;
    vector<char> inX(alledges.size(), 0);
    for (int e : X) { inX[e] = 1; ufp[uff(cedges[e].a)] = uff(cedges[e].b); }
    vector<int> rc(V, 0), rpin(V, -1); vector<u32> rreq(V, 0);
    for (int k = 0; k < n; k++) {
        int r = uff(m + k);
        if (rc[r]++ && !BROAD) return false;
        if (rpin[r] < 0) rpin[r] = k; else rreq[r] |= 1u << k;
    }
    for (size_t e = 0; e < alledges.size(); e++) if (!inX[e] && uff(alledges[e].a) == uff(alledges[e].b)) return false;
    if (BROAD) for (int k = 0; k < n; k++) {
        int r = uff(m + k); if (rc[r] < 2) continue;
        // BFS over X from ring vertex k
        vector<int> dist(V, -1), par(V, -1); deque<int> dq; dist[m + k] = 0; dq.push_back(m + k);
        while (!dq.empty()) {
            int v = dq.front(); dq.pop_front();
            for (int e : X) {
                int a = cedges[e].a, b = cedges[e].b, w = (a == v) ? b : (b == v) ? a : -1;
                if (w >= 0 && dist[w] < 0) { dist[w] = dist[v] + 1; par[w] = v; dq.push_back(w); }
            }
        }
        for (int k2 = k + 1; k2 < n; k2++) {
            if (uff(m + k2) != r) continue;
            int l = dist[m + k2];
            if (l > LMAX) return false;
            if (l <= 3) continue;
            vector<int> inner; for (int v = par[m + k2]; v != m + k; v = par[v]) inner.push_back(v);
            for (int v : inner) if (v >= m) return false;
            int gap = (k2 - k + n) % n;
            int mid = (gap == 2) ? (k + 1) % n : (gap == n - 2) ? (k2 + 1) % n : -1;
            if (mid >= 0) { bool all = true; for (int v : inner) if (!((ringMask[v] >> mid) & 1)) all = false; if (all) return false; }
        }
    }
    vector<int> sid(V, -1); K.M = 0; K.pin.clear(); K.rforb.clear(); K.req.clear();
    for (int j = 0; j < m; j++) { int r = uff(j); if (sid[r] < 0) { sid[r] = K.M++; K.pin.push_back(rpin[r]); K.req.push_back(rreq[r]); K.rforb.push_back(0); } }
    vector<set<int>> nb(K.M);
    for (size_t e = 0; e < cedges.size(); e++) {
        if (inX[e]) continue;
        int a = cedges[e].a, b = cedges[e].b, sb = sid[uff(b)];
        if (a >= m) K.rforb[sb] |= 1u << (a - m);
        else { int sa = sid[uff(a)]; nb[sa].insert(sb); nb[sb].insert(sa); }
    }
    // order: pinned first, then most placed neighbours / ring constraints
    vector<int> pos(K.M, -1), placed(K.M, 0); K.order.clear();
    for (int s = 0; s < K.M; s++) {
        int best = -1, bs = -1;
        for (int j = 0; j < K.M; j++) if (pos[j] < 0) {
            int sc = (K.pin[j] >= 0 ? 1000 : 0) + __builtin_popcount(K.rforb[j]) + placed[j];
            if (sc > bs) { bs = sc; best = j; }
        }
        pos[best] = s; K.order.push_back(best);
        for (int i : nb[best]) placed[i]++;
    }
    K.earlier.assign(K.M, {});
    for (int j = 0; j < K.M; j++) for (int i : nb[j]) if (pos[i] < pos[j]) K.earlier[j].push_back(i);
    return true;
}
static bool extends_kx(const KX &K, u32 q0, u32 q1) {
    u32 mk[4] = {~q0 & ~q1 & FULL, q0 & ~q1 & FULL, ~q0 & q1 & FULL, q0 & q1 & FULL};
    int col[64], dom[64], cand[64];
    for (int j = 0; j < K.M; j++) {
        int f = 0;
        for (int v = 0; v < 4; v++) if (K.rforb[j] & mk[v]) f |= 1 << v;
        int d = 15;
        if (K.pin[j] >= 0) {
            int k = K.pin[j], c = ((q0 >> k) & 1) | (((q1 >> k) & 1) << 1); d = 1 << c;
            if (K.req[j] && (K.req[j] & ~mk[c])) return false;     // identified ring vertices must share a colour
        }
        dom[j] = d & ~f;
    }
    int s = 0; cand[0] = dom[K.order[0]];
    while (s >= 0) {
        if (!cand[s]) { s--; continue; }
        int j = K.order[s];
        int c = __builtin_ctz(cand[s]); cand[s] &= cand[s] - 1; col[j] = c;
        if (s == K.M - 1) return true;
        s++;
        int jj = K.order[s], a = dom[jj];
        for (int i : K.earlier[jj]) a &= ~(1 << col[i]);
        cand[s] = a;
    }
    return false;
}
static bool parse_x(const string &xs, vector<int> &X) {   // "{R0-I0,I2-I3}" -> cedges indices
    X.clear(); string t;
    for (char c : xs) if (c != '{' && c != '}') t += c;
    stringstream ss(t); string tok;
    while (getline(ss, tok, ',')) {
        size_t d = tok.find('-'); if (d == string::npos) return false;
        auto vid = [&](const string &s) { int k = stoi(s.substr(1)); return s[0] == 'R' ? m + k : k; };
        int a = vid(tok.substr(0, d)), b = vid(tok.substr(d + 1)); bool f = false;
        for (size_t e = 0; e < cedges.size(); e++)
            if ((cedges[e].a == a && cedges[e].b == b) || (cedges[e].a == b && cedges[e].b == a)) { X.push_back((int)e); f = true; break; }
        if (!f) return false;
    }
    return true;
}

// ---------------- fillings (chord-split thread) ----------------
// A filling replaces the interior by: groups of interior vertices merged into one node (optionally pinned to a ring
// vertex, i.e. contracted into it), deleted interior vertices, and chords (ring pairs forced to differ).
struct Fill { int M; vector<int> pin; vector<u32> rforb; vector<vector<int>> earlier; vector<int> order; vector<pair<int,int>> ch; };
static void make_fill(const vector<int> &grp, const vector<int> &gpin, int G, const vector<pair<int,int>> &ch, Fill &F) {
    // grp[j] = node of interior j, or -1 (deleted); gpin[node] = ring vertex or -1
    F.M = G; F.pin = gpin; F.rforb.assign(G, 0); F.ch = ch;
    vector<set<int>> nb(G);
    for (int j = 0; j < m; j++) { int a = grp[j]; if (a < 0) continue;
        F.rforb[a] |= ringMask[j];
        for (int i : intN[j]) { int b = grp[i]; if (b < 0 || b == a) continue; nb[a].insert(b); } }
    for (int a = 0; a < G; a++) if (gpin[a] >= 0) F.rforb[a] &= ~(1u << gpin[a]);
    vector<int> pos(G, -1), placed(G, 0); F.order.clear();
    for (int s = 0; s < G; s++) { int best = -1, bs = -1;
        for (int j = 0; j < G; j++) if (pos[j] < 0) { int sc = (gpin[j] >= 0 ? 1000 : 0) + __builtin_popcount(F.rforb[j]) + placed[j]; if (sc > bs) { bs = sc; best = j; } }
        pos[best] = s; F.order.push_back(best); for (int i : nb[best]) placed[i]++; }
    F.earlier.assign(G, {});
    for (int j = 0; j < G; j++) for (int i : nb[j]) if (pos[i] < pos[j]) F.earlier[j].push_back(i);
}
static bool extends_fill(const Fill &K, u32 q0, u32 q1) {
    for (auto &c : K.ch) { int a = ((q0 >> c.first) & 1) | (((q1 >> c.first) & 1) << 1), b = ((q0 >> c.second) & 1) | (((q1 >> c.second) & 1) << 1); if (a == b) return false; }
    if (K.M == 0) return true;
    u32 mk[4] = {~q0 & ~q1 & FULL, q0 & ~q1 & FULL, ~q0 & q1 & FULL, q0 & q1 & FULL};
    int col[64], dom[64], cand[64];
    for (int j = 0; j < K.M; j++) {
        int f = 0; for (int v = 0; v < 4; v++) if (K.rforb[j] & mk[v]) f |= 1 << v;
        int d = 15; if (K.pin[j] >= 0) { int k = K.pin[j]; d = 1 << (((q0 >> k) & 1) | (((q1 >> k) & 1) << 1)); }
        dom[j] = d & ~f; if (!dom[j]) return false;
    }
    int s = 0; cand[0] = dom[K.order[0]];
    while (s >= 0) {
        if (!cand[s]) { s--; continue; }
        int j = K.order[s]; int c = __builtin_ctz(cand[s]); cand[s] &= cand[s] - 1; col[j] = c;
        if (s == K.M - 1) return true;
        s++; int jj = K.order[s], a = dom[jj];
        for (int i : K.earlier[jj]) a &= ~(1 << col[i]);
        cand[s] = a;
    }
    return false;
}
// counts bad classes that extend (early exit at stop)
static u64 leftover(const Fill &K, const vector<u64> &bad, u64 stop = ~0ull) {
    u64 L = 0; for (u64 i : bad) if (extends_fill(K, (u32)reps[i], (u32)(reps[i] >> 32))) { if (++L >= stop) break; } return L;
}
static bool connected_set(u32 S) {
    if (!S) return false; u32 seen = S & -S, fr = seen;
    while (fr) { int j = __builtin_ctz(fr); fr &= fr - 1; for (int i : intN[j]) if (((S >> i) & 1) && !((seen >> i) & 1)) { seen |= 1u << i; fr |= 1u << i; } }
    return seen == S;
}
static bool induced_tree(u32 S, int u) {   // S + ring u: edges = |S| exactly
    int e = 0; for (int j = 0; j < m; j++) if ((S >> j) & 1) { if ((ringMask[j] >> u) & 1) e++; for (int i : intN[j]) if (i > j && ((S >> i) & 1)) e++; }
    return e == __builtin_popcount(S);
}
static int RESTARTS = 40, STEPS = 400;
static void run_fillings(const vector<u64> &bad, u64 N, int TMAX) {
    u64 B = bad.size();
    printf("  FILL bad=%llu of %llu\n", (unsigned long long)B, (unsigned long long)N);
    if (getenv("DUMPBAD")) { FILE *f = fopen(getenv("DUMPBAD"), "w"); for (u64 i : bad) { for (int k = 0; k < n; k++) fputc('0' + (int)(((reps[i] >> k) & 1) | (((reps[i] >> (32 + k)) & 1) << 1)), f); fputc('\n', f); } fclose(f); }
    // A: chord only (everything inside deleted, one chord)
    { u64 best = ~0ull; int bu = -1, bv = -1; vector<int> grp(m, -1);
      for (int u = 0; u < n; u++) for (int v = u + 2; v < n; v++) { if (u == 0 && v == n - 1) continue;
          Fill F; make_fill(grp, {}, 0, {{u, v}}, F); u64 L = leftover(F, bad); if (L < best) { best = L; bu = u; bv = v; } }
      printf("  A chord-only: best pair R%d-R%d leftover %llu (%.1f%% of bad)\n", bu, bv, (unsigned long long)best, 100.0 * best / B); }
    // B: delete a separator S (|S|<=3), keep both halves, add the chord u-v.  Compared with contracting S into u.
    { u64 best = ~0ull, bestC = ~0ull; string bs, bsC; u64 nsep = 0, dominated = 0;
      for (u32 S = 1; S < (1u << m); S++) { int sz = __builtin_popcount(S); if (sz > 3) continue;
        // components of K-S and their ring contacts
        vector<int> comp(m, -1); int nc = 0; vector<u32> cr;
        for (int j = 0; j < m; j++) if (!((S >> j) & 1) && comp[j] < 0) { cr.push_back(0); deque<int> q{j}; comp[j] = nc;
            while (!q.empty()) { int a = q.front(); q.pop_front(); cr[nc] |= ringMask[a]; for (int i : intN[a]) if (!((S >> i) & 1) && comp[i] < 0) { comp[i] = nc; q.push_back(i); } } nc++; }
        for (int u = 0; u < n; u++) for (int v = u + 2; v < n; v++) { if (u == 0 && v == n - 1) continue;
          u32 arc1 = 0, arc2 = 0; for (int k = u + 1; k < v; k++) arc1 |= 1u << k; arc2 = FULL & ~arc1 & ~(1u << u) & ~(1u << v);
          bool ok = true, s1 = false, s2 = false; for (int c = 0; c < nc; c++) { bool a = cr[c] & arc1, b = cr[c] & arc2; if (a && b) ok = false; s1 |= a; s2 |= b; }
          if (!ok || !s1 || !s2) continue;   // a real split: both holes get something
          nsep++;
          vector<int> grp(m, -1); for (int j = 0; j < m; j++) if (comp[j] >= 0 && !((S >> j) & 1)) grp[j] = j;
          // renumber
          vector<int> id(m, -1); int G = 0; for (int j = 0; j < m; j++) if (grp[j] >= 0) { id[j] = G++; } for (int j = 0; j < m; j++) if (grp[j] >= 0) grp[j] = id[j];
          Fill F; make_fill(grp, vector<int>(G, -1), G, {{u, v}}, F); u64 L = leftover(F, bad);
          char b[96]; snprintf(b, 96, "S=%x u=R%d v=R%d", S, u, v);
          if (L < best) { best = L; bs = b; }
          // contraction of S into u (if S+u connected) or into v
          for (int w : {u, v}) { bool adj = false; for (int j = 0; j < m; j++) if (((S >> j) & 1) && ((ringMask[j] >> w) & 1)) adj = true;
            if (!adj || !connected_set(S)) continue;
            vector<int> g2(m); int G2 = 0; vector<int> pin;
            pin.push_back(w); G2 = 1; for (int j = 0; j < m; j++) g2[j] = ((S >> j) & 1) ? 0 : G2++;
            pin.resize(G2, -1); Fill F2; make_fill(g2, pin, G2, {}, F2); u64 L2 = leftover(F2, bad);
            if (L2 <= L) dominated++; else printf("  !! contraction worse than split S=%x w=R%d\n", S, w);
            if (L2 < bestC) { bestC = L2; snprintf(b, 96, "S=%x into R%d", S, w); bsC = b; } }
        } }
      printf("  B separator+chord: %llu splits, best %s leftover %llu; contracting S into u or v instead: best %s leftover %llu; contraction <= split in %llu cases\n",
             (unsigned long long)nsep, bs.c_str(), (unsigned long long)best, bsC.c_str(), (unsigned long long)bestC, (unsigned long long)dominated); }
    // C: contract a connected interior set T into one ring vertex u (any size up to TMAX)
    for (int variant = 0; variant < 2; variant++) {
      u64 best = ~0ull; string bs; u64 tested = 0; u64 bysz[40]; for (auto &x : bysz) x = ~0ull;
      vector<u64> killers;
      for (u32 T = 1; T < (1u << m); T++) { int sz = __builtin_popcount(T); if (sz > TMAX || sz == m) continue; if (!connected_set(T)) continue;
        u32 rr = 0; for (int j = 0; j < m; j++) if ((T >> j) & 1) rr |= ringMask[j];
        for (u32 q = rr; q; q &= q - 1) { int u = __builtin_ctz(q);
          if (variant == 0 && !induced_tree(T, u)) continue;
          tested++;
          vector<int> g(m); int G = 1; for (int j = 0; j < m; j++) g[j] = ((T >> j) & 1) ? 0 : G++;
          vector<int> pin(G, -1); pin[0] = u; Fill F; make_fill(g, pin, G, {}, F);
          u64 L = leftover(F, bad, bysz[sz]);
          if (L < bysz[sz]) bysz[sz] = L;
          if (L < best) { best = L; char b[64]; snprintf(b, 64, "T=%x into R%d (|T|=%d)", T, u, sz); bs = b; } } }
      printf("  C%d contract T into one ring vertex (%s), |T|<=%d: tested %llu, best %s leftover %llu; best by size:", variant, variant ? "any connected T" : "T+u induces a tree",
             TMAX, (unsigned long long)tested, bs.c_str(), (unsigned long long)best);
      for (int s = 1; s <= TMAX && s < m; s++) if (bysz[s] < ~0ull) printf(" %d:%llu", s, (unsigned long long)bysz[s]);
      printf("\n"); }
    // D: general contraction, no size cap: interior vertices merged into connected groups, each group contracted
    //    into at most one ring vertex it touches (so no two ring vertices are ever identified).  Local search.
    { mt19937_64 R(777); u64 best = ~0ull; string bs;
      auto score = [&](const vector<int> &g, const vector<int> &pin, u64 stop) {
          // groups contracted into the same ring vertex are one vertex of G/X
          vector<int> lab(m); for (int j = 0; j < m; j++) lab[j] = pin[g[j]] >= 0 ? m + pin[g[j]] : g[j];
          int G = 0; vector<int> id(m + n, -1), gg(m); for (int j = 0; j < m; j++) { if (id[lab[j]] < 0) id[lab[j]] = G++; gg[j] = id[lab[j]]; }
          vector<int> pp(G, -1); for (int j = 0; j < m; j++) pp[gg[j]] = pin[g[j]];
          if (G == m) { bool any = false; for (int x : pp) if (x >= 0) any = true; if (!any) return ~0ull; }
          Fill F; make_fill(gg, pp, G, {}, F); return leftover(F, bad, stop); };
      auto gconn = [&](const vector<int> &g, int grp) { u32 S = 0; for (int j = 0; j < m; j++) if (g[j] == grp) S |= 1u << j; return !S || connected_set(S); };
      for (int rs = 0; rs < RESTARTS; rs++) {
        vector<int> g(m), pin(m, -1); iota(g.begin(), g.end(), 0);
        // random seed: one random ring contraction
        { int j = R() % m; u32 r = ringMask[j]; if (r) { int c = __builtin_popcount(r), k = R() % c; while (k--) r &= r - 1; pin[j] = __builtin_ctz(r); } }
        u64 cur = score(g, pin, ~0ull);
        for (int it = 0; it < STEPS; it++) {
          vector<int> g2 = g, p2 = pin; int j = R() % m, typ = R() % 3;
          if (typ == 0) { if (intN[j].empty()) continue; int i = intN[j][R() % intN[j].size()]; int a = g2[j], b = g2[i]; if (a == b) continue;
              if (p2[a] >= 0 && p2[b] >= 0 && p2[a] != p2[b]) continue;
              // move j alone into b's group
              g2[j] = b; if (p2[b] < 0) { /* keep */ } if (!gconn(g2, a)) continue; if (p2[a] >= 0) { bool still = false; for (int q = 0; q < m; q++) if (g2[q] == a && ((ringMask[q] >> p2[a]) & 1)) still = true; if (!still) p2[a] = -1; } }
          else if (typ == 1) { int a = g2[j]; u32 r = 0; for (int q = 0; q < m; q++) if (g2[q] == a) r |= ringMask[q]; if (!r) continue;
              int c = __builtin_popcount(r), k = R() % (c + 1); if (k == c) p2[a] = -1; else { while (k--) r &= r - 1; p2[a] = __builtin_ctz(r); } }
          else { int a = g2[j]; int nf = -1; for (int q = 0; q < m; q++) { bool used = false; for (int z = 0; z < m; z++) if (g2[z] == q) used = true; if (!used) { nf = q; break; } }
              if (nf < 0) continue; g2[j] = nf; p2[nf] = -1; if (!gconn(g2, a)) continue;
              if (p2[a] >= 0) { bool still = false; for (int q = 0; q < m; q++) if (g2[q] == a && ((ringMask[q] >> p2[a]) & 1)) still = true; if (!still) p2[a] = -1; } }
          u64 s = score(g2, p2, cur + 1);
          if (s < cur || (s == cur && R() % 2)) { g = g2; pin = p2; cur = s; }
          if (cur == 0) break;
        }
        if (cur < best) { best = cur; string d; for (int j = 0; j < m; j++) { d += to_string(g[j]); if (pin[g[j]] >= 0) d += "R" + to_string(pin[g[j]]); d += j + 1 < m ? "," : ""; } bs = d; }
        if (best == 0) break;
      }
      printf("  D general contraction (one ring vertex per group, no cap), %d restarts: best leftover %llu  groups[%s]\n", RESTARTS, (unsigned long long)best, bs.c_str()); }
    fflush(stdout);
}

int main(int argc, char **argv) {
    bool fmode = false; int TMAXF = 6; bool jacobi = false, verbose = false, cmode = false, countonly = false; string ckpt, xfile; double tbudget = 1e18, saveint = 600; string inpath;
    for (int a = 1; a < argc; a++) {
        string s = argv[a];
        if (s == "-j") jacobi = true; else if (s == "-v") verbose = true; else if (s == "-C") cmode = true; else if (s == "-C2") { cmode = true; BROAD = true; }
        else if (s == "-L") LMAX = atoi(argv[++a]); else if (s == "-A") countonly = true; else if (s == "-F") { fmode = true; TMAXF = atoi(argv[++a]); }
        else if (s == "-x") xfile = argv[++a];
        else if (s == "-c") ckpt = argv[++a]; else if (s == "-t") tbudget = atof(argv[++a]); else if (s == "-s") saveint = atof(argv[++a]);
        else inpath = s;
    }
    multimap<string, string> xq;                     // -x FILE: lines "name X", X evaluated exactly
    if (!xfile.empty()) { ifstream xf(xfile); string nm, xs; while (xf >> nm >> xs) xq.insert({nm, xs}); }
    build_maxp(10);
    stamp.assign(1u << 19, 0); memo.assign(1u << 19, 0);
    ifstream fin; istream *in = &cin;
    if (!inpath.empty()) { fin.open(inpath); in = &fin; }
    string line;
    while (getline(*in, line)) {
        if (line.empty() || line[0] == '#') continue;
        string name;
        if (!parse(line, name)) continue;
        if (n > 20) { printf("%s r=%d SKIP (ring > 20)\n", name.c_str(), n); fflush(stdout); continue; }
        if (countonly) {                             // -A: admissible X counts by size, no closure
            build_edges(); int E = (int)cedges.size(); u64 tot = 0, adm = 0;
            for (int sz = 1; sz <= 4; sz++) {
                vector<int> c(sz); iota(c.begin(), c.end(), 0);
                while (true) {
                    tot++; KX K; if (build_kx(c, K)) adm++;
                    int q = sz - 1; while (q >= 0 && c[q] == E - sz + q) q--;
                    if (q < 0) break;
                    c[q]++; for (int r = q + 1; r < sz; r++) c[r] = c[r - 1] + 1;
                }
            }
            printf("%s r=%d m=%d edges=%d subsets=%llu admissible=%llu\n", name.c_str(), n, m, E, (unsigned long long)tot, (unsigned long long)adm);
            fflush(stdout); continue;
        }
        auto T0 = chrono::steady_clock::now();
        auto el = [&]() { return chrono::duration<double>(chrono::steady_clock::now() - T0).count(); };
        build_rank(); build_rank_chunks();
        u64 N = CNT[1][1][1];
        // enumerate canonical colourings in rank order
        reps.assign(N, 0);
        {
            u64 k = 0; int c[34]; c[0] = 0;
            function<void(int, int)> rec = [&](int i, int used) {
                if (i == n) {
                    if (c[n - 1] == 0) return;
                    u32 q0 = 0, q1 = 0;
                    for (int j = 0; j < n; j++) { q0 |= (u32)(c[j] & 1) << j; q1 |= (u32)(c[j] >> 1) << j; }
                    reps[k++] = (u64)q0 | ((u64)q1 << 32);
                    return;
                }
                for (int cc = 0; cc <= min(used, 3); cc++) {
                    if (cc == c[i - 1]) continue;
                    c[i] = cc; rec(i + 1, max(used, cc + 1));
                }
            };
            rec(1, 1);
            if (k != N) { fprintf(stderr, "%s: enumeration %llu != %llu\n", name.c_str(), (unsigned long long)k, (unsigned long long)N); return 2; }
            // spot-check the ranking
            for (u64 i = 0; i < N; i += max<u64>(1, N / 100000))
                if (canon_rank((u32)reps[i], (u32)(reps[i] >> 32)) != i || canon_rank2((u32)reps[i], (u32)(reps[i] >> 32)) != i) { fprintf(stderr, "%s: rank mismatch at %llu\n", name.c_str(), (unsigned long long)i); return 2; }
            // and on permuted colourings (the hot path ranks non-canonical colourings)
            {
                const int P4[6][4] = {{1,0,2,3},{2,3,0,1},{3,2,1,0},{1,2,3,0},{0,3,2,1},{2,0,1,3}};
                for (u64 i = 0; i < N; i += max<u64>(1, N / 20000))
                    for (auto &pm : P4) {
                        u32 a0 = (u32)reps[i], a1 = (u32)(reps[i] >> 32), b0 = 0, b1 = 0;
                        for (int j = 0; j < n; j++) { int c = pm[((a0 >> j) & 1) | (((a1 >> j) & 1) << 1)]; b0 |= (u32)(c & 1) << j; b1 |= (u32)(c >> 1) << j; }
                        if (canon_rank2(b0, b1) != i || canon_rank(b0, b1) != i) { fprintf(stderr, "%s: permuted rank mismatch at %llu\n", name.c_str(), (unsigned long long)i); return 2; }
                    }
            }
        }
        size_t W = (N + 63) / 64;
        good.assign(W, 0); wit.assign(N * 3, 0);
        u64 ext = 0; int pass = 0, depth = 0; u64 startpos = 0; bool changed = false; bool resumed = false;
        if (!ckpt.empty() && !jacobi) {
            FILE *f = fopen(ckpt.c_str(), "rb");
            if (f) {
                u64 hdr[7];
                if (fread(hdr, 8, 7, f) == 7 && hdr[0] == 0x4b43434b && hdr[1] == (u64)n && hdr[2] == N &&
                    fread(good.data(), 8, W, f) == W && fread(wit.data(), 2, N * 3, f) == N * 3) {
                    ext = hdr[3]; pass = (int)hdr[4]; startpos = hdr[5]; changed = hdr[6]; resumed = true;
                    fprintf(stderr, "%s: resumed at pass %d pos %llu\n", name.c_str(), pass, (unsigned long long)startpos);
                }
                fclose(f);
            }
        }
        auto save = [&](u64 pos) {
            if (ckpt.empty() || jacobi) return;
            string tmp = ckpt + ".tmp";
            FILE *f = fopen(tmp.c_str(), "wb");
            u64 hdr[7] = {0x4b43434b, (u64)n, N, ext, (u64)pass, pos, (u64)changed};
            fwrite(hdr, 8, 7, f); fwrite(good.data(), 8, W, f); fwrite(wit.data(), 2, N * 3, f); fclose(f);
            rename(tmp.c_str(), ckpt.c_str());
        };
        if (!resumed) {
            for (u64 i = 0; i < N; i++) if (extends((u32)reps[i], (u32)(reps[i] >> 32))) { setb(good, i); ext++; }
            if (verbose) fprintf(stderr, "%s: classes %llu ext %llu (%.1fs)\n", name.c_str(), (unsigned long long)N, (unsigned long long)ext, el());
            save(0);
        }
        double lastsave = el(); bool stopped = false;
        while (true) {
            u64 nw = 0;
            if (jacobi) nxt.assign(W, 0);
            for (u64 i = startpos; i < N; i++) {
                if (isgood(i)) continue;
                u32 p0 = (u32)reps[i], p1 = (u32)(reps[i] >> 32);
                bool ok = false;
                for (int x = 1; x <= 3 && !ok; x++) ok = try_pairing(i, p0, p1, x);
                if (ok) { nw++; if (jacobi) setb(nxt, i); else setb(good, i); }
                if (!jacobi && (i & 0xffff) == 0 && el() - lastsave > saveint) {
                    if (nw) changed = true;
                    save(i); lastsave = el();
                    if (el() > tbudget) { stopped = true; break; }
                }
            }
            if (stopped) break;
            if (jacobi) for (size_t q = 0; q < W; q++) good[q] |= nxt[q];
            if (nw) changed = true;
            pass++;
            if (nw) depth++;
            u64 g = 0; for (size_t q = 0; q < W; q++) g += __builtin_popcountll(good[q]);
            if (verbose) fprintf(stderr, "%s: pass %d new %llu good %llu (%.1fs)\n", name.c_str(), pass, (unsigned long long)nw, (unsigned long long)g, el());
            startpos = 0;
            bool done = (g == N) || (!changed && !jacobi) || (jacobi && !nw);
            if (!jacobi) { bool c0 = changed; changed = false; save(0); if (!c0) done = true; }
            if (done) break;
            if (el() > tbudget) { stopped = true; break; }
        }
        u64 g = 0; for (size_t q = 0; q < W; q++) g += __builtin_popcountll(good[q]);
        if (stopped) { printf("%s r=%d m=%d classes=%llu ext=%llu reached=%llu INCOMPLETE pass=%d %.0fms\n", name.c_str(), n, m,
                              (unsigned long long)N, (unsigned long long)ext, (unsigned long long)g, pass, el() * 1000); fflush(stdout); return 3; }
        printf("%s r=%d m=%d classes=%llu ext=%llu reached=%llu D=%s depth=%d passes=%d mode=%s %.0fms\n", name.c_str(), n, m,
               (unsigned long long)N, (unsigned long long)ext, (unsigned long long)g, g == N ? "true" : "false", depth, pass,
               jacobi ? "jacobi" : "gs", el() * 1000);
        fflush(stdout);
        if (fmode && g < N) { vector<u64> bad; for (u64 i = 0; i < N; i++) if (!isgood(i)) bad.push_back(i); run_fillings(bad, N, TMAXF); }
        if (g == N || (!cmode && xq.find(name) == xq.end())) continue;
        // ---- C stage ----
        build_edges();
        vector<u64> bad;
        for (u64 i = 0; i < N; i++) if (!isgood(i)) bad.push_back(i);
        auto exact = [&](const KX &K) { u64 L = 0; for (u64 i : bad) if (extends_kx(K, (u32)reps[i], (u32)(reps[i] >> 32))) L++; return L; };
        auto rg = xq.equal_range(name);
        for (auto it = rg.first; it != rg.second; ++it) {
            vector<int> X; KX K;
            if (!parse_x(it->second, X)) { printf("  X=%s parse=fail\n", it->second.c_str()); continue; }
            bool adm = build_kx(X, K);
            if (!adm) printf("  X=%s adm=no\n", xname(X).c_str());
            else printf("  X=%s adm=yes leftover %llu\n", xname(X).c_str(), (unsigned long long)exact(K));
            fflush(stdout);
        }
        if (!cmode) continue;
        mt19937_64 rng(12345); shuffle(bad.begin(), bad.end(), rng);
        vector<u64> killers;                         // classes that refuted recent X, tried first
        u64 nadm = 0, ntot = 0, bestscan = 0; vector<int> bestX, X, work;
        bool found = false;
        int E = (int)cedges.size();
        for (int sz = 1; sz <= 4 && !found; sz++) {
            vector<int> c(sz); iota(c.begin(), c.end(), 0);
            while (!found) {
                ntot++; KX K;
                if (build_kx(c, K)) {
                    nadm++; bool ref = false;
                    for (size_t q = 0; q < killers.size(); q++) {
                        u64 i = killers[q];
                        if (extends_kx(K, (u32)reps[i], (u32)(reps[i] >> 32))) { ref = true; rotate(killers.begin(), killers.begin() + q, killers.begin() + q + 1); break; }
                    }
                    if (!ref) {
                        u64 p = 0;
                        for (; p < bad.size(); p++) {
                            u64 i = bad[p];
                            if (extends_kx(K, (u32)reps[i], (u32)(reps[i] >> 32))) {
                                ref = true; killers.insert(killers.begin(), i); if (killers.size() > 48) killers.pop_back(); break;
                            }
                        }
                        if (p >= bestscan) { bestscan = p; bestX = c; }
                        if (!ref) { found = true; work = c; }
                    }
                }
                int q = sz - 1;                       // next combination
                while (q >= 0 && c[q] == E - sz + q) q--;
                if (q < 0) break;
                c[q]++; for (int r = q + 1; r < sz; r++) c[r] = c[r - 1] + 1;
            }
        }
        if (found) printf("  C-REDUCIBLE X=%s size=%d (kc-C: tested %llu, admissible %llu, edges %d, %.0fms)\n", xname(work).c_str(),
                          (int)work.size(), (unsigned long long)ntot, (unsigned long long)nadm, E, el() * 1000);
        else {
            u64 L = 0; if (!bestX.empty()) { KX K; build_kx(bestX, K); L = exact(K); }
            printf("  C=false |X|<=4 (kc-C: tested %llu, admissible %llu, edges %d) best X=%s leftover %llu (%.0fms)\n",
                   (unsigned long long)ntot, (unsigned long long)nadm, E, bestX.empty() ? "-" : xname(bestX).c_str(), (unsigned long long)L, el() * 1000);
        }
        fflush(stdout);
    }
    return 0;
}
