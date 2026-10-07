// picyc.cpp -- [exploratory] Mac Studio run 27: pi-cycles, windings, positive cycles versus configurations, and transport
// (lock-breaking exits) at every degree-5 hole. C++ port of the MacBook's Python (local-runs/22 escape.py, 23 scan.py,
// 26 lib26.py), same definitions:
//  state   = proper 4-colouring of T-v up to renaming; canonical by first occurrence along the BFS order of T-v from link[0]
//            (neighbours by ascending label), vertex 0 of that order gets colour 0;
//  link    = rotation order at the hole as listed in the input (planar-code orientation); x_t = link[t];
//  filled  = link uses 3 colours; unfilled: 4 colours, the repeat is c(x_j) = c(x_{j+2}), alpha = c(x_j), mu = c(x_{j+1}),
//            A = c(x_{j+3}), B = c(x_{j+4}), m = x_{j+1}, a = x_{j+3}, b = x_{j+4};
//  lock 1  = a in the {mu,A}-component of m; lock 2 = b in the {mu,B}-component of m; DL = both;
//  pi      = (unfilled) lock 2 ? R+3: swap the {alpha,A}-component of x_{j+2}, lambda +1
//                                   : phiB^-1: swap the {mu,B}-component of x_{j+4}, lambda -1
//            (filled, W unique at x_i, X = c(x_{i+1}), Y = c(x_{i+2}), Z the fourth colour)
//            x_{i+4} not in K = {Y,Z}-component of x_{i+2} ? phiA: swap K, lambda -1 : tau: swap the {W,X}-component of x_{i+3}, lambda -3;
//  winding of a pi-cycle = (sum of lambda)/5; Theorem W: 3F - U = -5 * sum of windings over a Kempe class (checked in --full mode);
//  move    = whole-component Kempe swap; link-free = the component misses all 5 link vertices; lock-breaking (at a DL state) =
//            the component meets K1 | K2 (the two lock chains); other-pair = colour pair is not {alpha,A} or {alpha,B};
//  transport variants from positive cycle Z to negative cycles: (a) DL states, any pair; (b) DL, other pair; (c) any state;
//            (d) DL, lock-breaking; (e) DL, other pair and lock-breaking. ok = max-flow routes the whole supply; Hall ratio =
//            min over subsets S of positive cycles (same bipartite component, <= 18) of cap(N(S)) / supply(S).
//  configurations: Birkhoff diamond (RSST 0.7322) = edge ab with face-neighbours c, d, all four of degree 5, c and d not adjacent;
//            RSST 2.122 = same with {deg a, deg b} = {5,6}, deg c = deg d = 5, c and d not adjacent. Counted once per edge ab.
// Input: text, one graph per line: "name n r0;r1;...;r_{n-1}", r_v = comma-separated 0-based neighbours in rotation order.
// --full also: per class clsig [size, F, sum w, DD, N0, E2, tau] (DD = DL with DL pi-image; N0 = unfilled with neither lock;
//   E2 = unfilled runs of length exactly 2 between filled states on a pi-cycle; tau = filled with lambda -3) and f5_bad = classes where
//   sum lambda != DD - 2 N0 - E2 - 3 tau (Theorem F5 identity, NightF5Review.md).
// --jobe: only (5,5,5,5,6)/(5,5,5,6,6) holes; per hole sigC (pi-cycles joined by sigma = {alpha,mu}-swap at m from every DD-step endpoint;
//   fail = a joined group with sum w > 0) and per all-DL pi-cycle (Gamma): R-types (w0 = A: R1; w0 = B, w3 = alpha: R2; w0 = B, w3 = mu: R3; else other),
//   [type, kmask (bit i = x_{j+i} has degree >= 6), count], R3 states whose sigma image is lockless (C1-Gamma), first R3 failure.
// --jobn rows: [pos in cycle, k, lockless, y~z in {c(y),c(z)}, pm bridge of G[{v}+c(p),c(m)], p, m, y, z (original labels), #m candidates, |K_{c(p),c(m)}(p)|, |K(y)|, |K(z)|, sigma fixed point]
// --jobo rows per state x of a Gamma-cycle (pi order): [pos, type, kmask, pairmask, compmask, |swapped comp|, y~z before, y~z after the step, |K(y)|, |K(z)| after]
//   (pairmask / compmask bits: p, m, y, z have a colour in the swapped pair / lie in the swapped component; the step x -> pi x is R+3: the {alpha,A}-swap at x_{j+2})
// --jobp rows: K = [|K|, dist(K, v), y~z before, |K & K_yz|, K cuts y from z in {c(y),c(z)}, #K vertices on a BFS shortest y-z path (-1 if not joined), K separates y,z in T - K];
//   edges = {"a-b": bridge?} over role vertices 0..4 = x_{j+i}, 5..9 = w_{j+i}, 10 = m (R3 states only; bridge of G[{v} + c(a) + c(b)])
// --jobq rows: [pos, type, kmask, sigma fixed point, sigma lockless, |K step|, |K & K_sigma(x)|, |K & K_sigma(pi x)|, |K_sigma(x)|, |other {alpha,mu} vertices|, K meets them]
// --jobs: pos = positive cycles {id, Lambda, gamma, L, CrN, CrP, def, nbrN = nonpositive sigma-neighbour ids}; targets = [id, Lambda, L, hit, #exits, #distinct excursions, rem]
// --jobab fails rows: [cycle, w, u, f, mass, credit (all lockless exits from the excursion DD states), credit (exits to other cycles)]
// Usage: picyc FILE [--full] [--mirror] [--cap M] [--holes h,h,...] [--cfree] [--adj5] [--graphonly]   (default --pi: no class union-find)
// Per hole also: linkdeg (degrees of x_0..x_4 in link order), vrole (bits: 1 diamond centre, 2 diamond tip, 4 2.122 deg-5 centre, 16 2.122 tip),
// dist_config (graph distance from v to the nearest vertex of any diamond or 2.122, -1 if none). Per graph: adj55 = edges between degree-5 vertices.
// Output: JSON lines: {"kind":"graph",...} once per graph, {"kind":"hole",...} per degree-5 hole. Requires n-1 <= 64.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <string>
#include <algorithm>
#include <functional>
#include <array>
#include <array>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator<(const Key&o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
                         bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
static int N; static u64 adjm[64]; static int link_[5]; static u64 linkmask, ring2mask;
static std::vector<Key> ALL; static int col[64]; static long long capStates = 80000000LL; static bool capHit = false;
static bool FULL = false, MIRROR = false, CFREE = false, ADJ5 = false, GRAPHONLY = false, JOBE = false, SIGC = false, JOBG = false, JOBH = false, JOBI = false, JOBK = false, JOBM = false, JOBN = false, JOBO = false, JOBP = false, JOBQ = false, JOBS = false, JOBX = false, ALLTYPES = false, JOBAB = false, JOBAK = false, JOBBB = false, JOBBC = false, JOBBGH = false, JOBBJ = false, JOBBK = false, JOBBL = false, JOBBO = false, JOBBP = false, JOBBQ = false, NOCLS = false, JOBBT = false;
static std::vector<int> VROLE; static int ADJ55;
static int dist_config(int n, const std::vector<std::vector<int>> &rot, int v);

static inline u64 flood(u64 start, u64 M) {
    u64 comp = start, front = start;
    while (front) { u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~comp; comp |= nb; front = nb; }
    return comp;
}
static inline Key keyof(const int *c) { Key k{0, 0}; for (int i = 0; i < N; i++) { if (i < 32) k.hi |= (u64)c[i] << (62 - 2 * i); else k.lo |= (u64)c[i] << (62 - 2 * (i - 32)); } return k; }
static inline void unkey(const Key &k, int *c) { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
static inline void masks(const int *c, u64 *cm) { cm[0] = cm[1] = cm[2] = cm[3] = 0; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i; }
static void rec(int i, int used) {
    if (capHit) return;
    if (i == N) { ALL.push_back(keyof(col)); if ((long long)ALL.size() > capStates) capHit = true; return; }
    u64 forb = 0; for (u64 f = adjm[i] & ((1ULL << i) - 1); f; f &= f - 1) forb |= 1ULL << col[__builtin_ctzll(f)];
    int top = used + 1 < 4 ? used + 1 : 4;
    for (int c = 0; c < top; c++) if (!(forb >> c & 1)) { col[i] = c; rec(i + 1, c + 1 > used ? c + 1 : used); }
}
// swap component K of pair (p,q) in colouring c, canonicalise into nc, return state index
static inline long long swap_index(const int *c, u64 K, int p, int q, int *nc) {
    int mp[4] = {-1, -1, -1, -1}, nx = 0;
    for (int i = 0; i < N; i++) { int x = c[i]; if (K >> i & 1) x = (x == p) ? q : p; if (mp[x] < 0) mp[x] = nx++; nc[i] = mp[x]; }
    Key nk = keyof(nc); auto it = std::lower_bound(ALL.begin(), ALL.end(), nk);
    if (it == ALL.end() || !(*it == nk)) { fprintf(stderr, "state not found\n"); exit(3); }
    return it - ALL.begin();
}
struct StateInfo { int kind; int al, A, B; u64 lock; int l1, l2; };   // kind 0 filled, 1 unfilled non-DL, 2 DL
static inline StateInfo info_of(const int *c, const u64 *cm) {
    StateInfo r{0, -1, -1, -1, 0, 0, 0}; int lc[5]; int seen = 0; for (int t = 0; t < 5; t++) { lc[t] = c[link_[t]]; seen |= 1 << lc[t]; }
    if (__builtin_popcount(seen) <= 3) return r;
    int j = 0; for (; j < 5; j++) if (lc[j] == lc[(j + 2) % 5]) break;
    int m = link_[(j + 1) % 5], a = link_[(j + 3) % 5], b = link_[(j + 4) % 5];
    int mu = lc[(j + 1) % 5]; r.al = lc[j]; r.A = lc[(j + 3) % 5]; r.B = lc[(j + 4) % 5];
    u64 K1 = flood(1ULL << m, cm[mu] | cm[r.A]); u64 K2 = flood(1ULL << m, cm[mu] | cm[r.B]);
    r.l1 = (K1 >> a & 1) ? 1 : 0; r.l2 = (K2 >> b & 1) ? 1 : 0; r.kind = (r.l1 && r.l2) ? 2 : 1; r.lock = K1 | K2; return r;
}
// pi and lambda
static inline long long pi_of(const int *c, const u64 *cm, int *nc, int &lam) {
    int lc[5]; int seen = 0; for (int t = 0; t < 5; t++) { lc[t] = c[link_[t]]; seen |= 1 << lc[t]; }
    if (__builtin_popcount(seen) == 4) {
        int j = 0; for (; j < 5; j++) if (lc[j] == lc[(j + 2) % 5]) break;
        int al = lc[j], mu = lc[(j + 1) % 5], A = lc[(j + 3) % 5], B = lc[(j + 4) % 5];
        int m = link_[(j + 1) % 5], b = link_[(j + 4) % 5];
        u64 K2 = flood(1ULL << m, cm[mu] | cm[B]);
        if (K2 >> b & 1) { lam = 1; u64 K = flood(1ULL << link_[(j + 2) % 5], cm[al] | cm[A]); return swap_index(c, K, al, A, nc); }
        lam = -1; u64 K = flood(1ULL << b, cm[mu] | cm[B]); return swap_index(c, K, mu, B, nc);
    }
    int cnt[4] = {0, 0, 0, 0}; for (int t = 0; t < 5; t++) cnt[lc[t]]++;
    int i = 0; for (; i < 5; i++) if (cnt[lc[i]] == 1) break;
    int W = lc[i], X = lc[(i + 1) % 5], Y = lc[(i + 2) % 5]; int Z = 0; for (int z = 0; z < 4; z++) if (z != W && z != X && z != Y) Z = z;
    int x2 = link_[(i + 2) % 5], x4 = link_[(i + 4) % 5];
    u64 K = flood(1ULL << x2, cm[Y] | cm[Z]);
    if (!(K >> x4 & 1)) { lam = -1; return swap_index(c, K, Y, Z, nc); }
    lam = -3; u64 K2 = flood(1ULL << link_[(i + 3) % 5], cm[W] | cm[X]); return swap_index(c, K2, W, X, nc);
}
// ---------- max flow / Hall on small bipartite graphs
struct Flow { bool ok; long long flow, supply, capreach; int nneg; double hall; std::vector<int> hallW; long long hallcap, hallsup; bool hallnone; };
static Flow flow_report(const std::vector<int> &pos, const std::map<int, long long> &W, const std::map<int, std::set<int>> &edges) {
    std::vector<int> sinks; { std::set<int> s; for (int z : pos) { auto it = edges.find(z); if (it != edges.end()) for (int n : it->second) s.insert(n); } sinks.assign(s.begin(), s.end()); }
    int P = pos.size(), Q = sinks.size(); std::map<int, int> sid; for (int i = 0; i < Q; i++) sid[sinks[i]] = i;
    // nodes: 0 = S, 1..P positives, P+1..P+Q sinks, P+Q+1 = T
    int V = P + Q + 2, T = V - 1; std::vector<std::vector<long long>> cap(V, std::vector<long long>(V, 0));
    long long supply = 0, capreach = 0;
    for (int i = 0; i < P; i++) { cap[0][1 + i] = W.at(pos[i]); supply += W.at(pos[i]); auto it = edges.find(pos[i]); if (it != edges.end()) for (int n : it->second) cap[1 + i][P + 1 + sid[n]] = 1000000000LL; }
    for (int j = 0; j < Q; j++) { cap[P + 1 + j][T] = -W.at(sinks[j]); capreach += -W.at(sinks[j]); }
    long long flow = 0;
    while (true) {
        std::vector<int> par(V, -1); par[0] = 0; std::vector<int> q{0};
        for (size_t h = 0; h < q.size() && par[T] < 0; h++) { int u = q[h]; for (int v = 0; v < V; v++) if (par[v] < 0 && cap[u][v] > 0) { par[v] = u; q.push_back(v); } }
        if (par[T] < 0) break;
        long long b = 1000000000LL; for (int v = T; v != 0; v = par[v]) b = std::min(b, cap[par[v]][v]);
        for (int v = T; v != 0; v = par[v]) { cap[par[v]][v] -= b; cap[v][par[v]] += b; }
        flow += b;
    }
    Flow r; r.ok = (flow == supply); r.flow = flow; r.supply = supply; r.capreach = capreach; r.nneg = Q; r.hall = 1e18; r.hallnone = true; r.hallcap = r.hallsup = 0;
    if (P <= 18) {
        r.hallnone = false;
        for (unsigned S = 1; S < (1u << P); S++) {
            std::set<int> Nn; long long s = 0; for (int i = 0; i < P; i++) if (S >> i & 1) { s += W.at(pos[i]); auto it = edges.find(pos[i]); if (it != edges.end()) Nn.insert(it->second.begin(), it->second.end()); }
            long long c = 0; for (int n : Nn) c += -W.at(n);
            double ratio = (double)c / (double)s;
            if (ratio < r.hall) { r.hall = ratio; r.hallW.clear(); for (int i = 0; i < P; i++) if (S >> i & 1) r.hallW.push_back(W.at(pos[i])); std::sort(r.hallW.begin(), r.hallW.end()); r.hallcap = c; r.hallsup = s; }
        }
    }
    return r;
}
static std::string flow_json(const Flow &f) {
    char buf[512]; std::string s = "{\"ok\": "; s += f.ok ? "true" : "false";
    snprintf(buf, sizeof buf, ", \"flow\": %lld, \"supply\": %lld, \"capreach\": %lld, \"nneg_reach\": %d", f.flow, f.supply, f.capreach, f.nneg); s += buf;
    if (f.hallnone) s += ", \"hall_ratio\": null, \"hall_set\": null";
    else { snprintf(buf, sizeof buf, ", \"hall_ratio\": %.4f, \"hall_set\": {\"W\": [", f.hall); s += buf; for (size_t i = 0; i < f.hallW.size(); i++) { snprintf(buf, sizeof buf, "%s%d", i ? ", " : "", f.hallW[i]); s += buf; }
           snprintf(buf, sizeof buf, "], \"cap\": %lld, \"supply\": %lld}", f.hallcap, f.hallsup); s += buf; }
    return s + "}";
}
// ---------- one hole
struct Exit { long long any = 0, dl = 0, alphaAB = 0, other = 0, lb = 0, nonlb = 0, other_lb = 0; };
static void analyse_hole(const std::string &name, int n, const std::vector<std::vector<int>> &rot, int hole) {
    std::vector<std::set<int>> adj(n); for (int v = 0; v < n; v++) for (int w : rot[v]) if (v != hole && w != hole) adj[v].insert(w);
    const std::vector<int> &L = rot[hole];
    std::string jpat;
    if (JOBE || SIGC || JOBG || JOBH) {   // JOBE: only (5,5,5,5,6) and (5,5,5,6,6) holes; SIGC: every hole (cyclic, up to reflection, degrees capped at 8)
        int d[5]; for (int t = 0; t < 5; t++) d[t] = std::min((int)rot[L[t]].size(), 8);
        std::vector<int> best; for (int rf = 0; rf < 2; rf++) for (int r = 0; r < 5; r++) { std::vector<int> v(5); for (int t = 0; t < 5; t++) v[t] = rf ? d[(r - t + 10) % 5] : d[(r + t) % 5]; if (best.empty() || v < best) best = v; }
        if (JOBI && !(best == std::vector<int>{5, 5, 5, 5, 6} || best == std::vector<int>{5, 5, 5, 6, 6})) return;
        if (SIGC || JOBG || JOBH) { for (int t = 0; t < 5; t++) { if (t) jpat += ","; jpat += best[t] >= 8 ? std::string("8+") : std::to_string(best[t]); } }
        else if (best == std::vector<int>{5, 5, 5, 5, 6}) jpat = "5,5,5,5,6"; else if (best == std::vector<int>{5, 5, 5, 6, 6}) jpat = "5,5,5,6,6"; else return;
    }
    std::vector<int> order{L[0]}, idx(n, -1); idx[L[0]] = 0;
    for (size_t h = 0; h < order.size(); h++) for (int w : adj[order[h]]) if (idx[w] < 0) { idx[w] = order.size(); order.push_back(w); }
    N = order.size(); if (N > 64 || N != n - 1) { printf("{\"kind\": \"hole\", \"name\": \"%s\", \"hole\": %d, \"error\": \"N=%d unsupported\"}\n", name.c_str(), hole, N); return; }
    for (int i = 0; i < N; i++) { adjm[i] = 0; for (int w : adj[order[i]]) adjm[i] |= 1ULL << idx[w]; }
    linkmask = 0; for (int t = 0; t < 5; t++) { link_[t] = idx[L[t]]; linkmask |= 1ULL << link_[t]; }
    ring2mask = 0; for (int t = 0; t < 5; t++) ring2mask |= adjm[link_[t]]; ring2mask &= ~linkmask;
    ALL.clear(); ALL.shrink_to_fit(); capHit = false; col[0] = 0; rec(1, 1);
    if (capHit) { printf("{\"kind\": \"hole\", \"name\": \"%s\", \"hole\": %d, \"inconclusive\": \"more than %lld states\"}\n", name.c_str(), hole, capStates); fflush(stdout); return; }
    for (size_t i = 1; i < ALL.size(); i++) if (!(ALL[i - 1] < ALL[i])) { fprintf(stderr, "not sorted\n"); exit(3); }
    long long S = ALL.size();
    std::vector<int32_t> pi(S); std::vector<int8_t> lam(S), kind(S), nolock(S, 0); std::vector<int32_t> cyc(S, -1);
    long long F = 0, nDL = 0;
    { int c[64], nc[64]; u64 cm[4];
      for (long long k = 0; k < S; k++) { unkey(ALL[k], c); masks(c, cm); int l; pi[k] = (int32_t)pi_of(c, cm, nc, l); lam[k] = (int8_t)l;
          StateInfo si = info_of(c, cm); kind[k] = (int8_t)si.kind; nolock[k] = (si.kind == 1 && !si.l1 && !si.l2); if (si.kind == 0) F++; if (si.kind == 2) nDL++; } }
    // permutation check and cycles
    { std::vector<char> hit(S, 0); for (long long k = 0; k < S; k++) { if (hit[pi[k]]) { fprintf(stderr, "pi not injective\n"); exit(3); } hit[pi[k]] = 1; } }
    std::vector<std::vector<int32_t>> cycles; std::vector<long long> wind;
    for (long long k = 0; k < S; k++) { if (cyc[k] >= 0) continue; std::vector<int32_t> z; long long x = k, sl = 0; int id = cycles.size();
        while (cyc[x] < 0) { cyc[x] = id; z.push_back((int32_t)x); sl += lam[x]; x = pi[x]; }
        if (x != k) { fprintf(stderr, "pi cycle closure failed\n"); exit(3); }
        if (sl % 5 != 0) { fprintf(stderr, "sum lambda not divisible by 5\n"); exit(3); }
        cycles.push_back(z); wind.push_back(sl / 5); }
    std::map<std::pair<long long, long long>, long long> hist; for (size_t i = 0; i < cycles.size(); i++) hist[{wind[i], (long long)cycles[i].size()}]++;
    std::vector<int> pos; for (size_t i = 0; i < cycles.size(); i++) if (wind[i] > 0) pos.push_back(i);
    // classes (full mode)
    std::vector<int32_t> par; long long nclasses = 0; std::map<int, int> cls_of_cycle;
    std::function<int(int)> find = [&](int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; };
    if (FULL) {
        par.resize(S); for (long long i = 0; i < S; i++) par[i] = i;
        int c[64], nc[64]; u64 cm[4];
        for (long long i = 0; i < S; i++) { unkey(ALL[i], c); masks(c, cm);
            for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; long long j = swap_index(c, K, p, q, nc); int a = find(i), b = find(j); if (a != b) par[a] = b; } } }
        std::set<int> roots; for (long long i = 0; i < S; i++) roots.insert(find(i)); nclasses = roots.size();
    }
    std::string clsig; long long cls_bad = 0, cyc_split = 0, f5_bad = 0;
    if (FULL) {   // per-class check: every pi-cycle inside one class; 3F - U = -5 * (sum of windings of the class's cycles)
        std::vector<int32_t> pinv(S); for (long long k = 0; k < S; k++) pinv[pi[k]] = (int32_t)k;
        std::map<int, std::array<long long, 3>> cs;   // root -> size, F, sum lambda
        std::map<int, std::array<long long, 4>> f5;   // root -> DD, N0, E2, tau   (Theorem F5 identity: sum lambda = DD - 2 N0 - E2 - 3 tau)
        for (long long k = 0; k < S; k++) { int r = find(k); auto &e = cs[r]; e[0]++; if (kind[k] == 0) e[1]++; e[2] += lam[k];
            auto &g = f5[r];
            if (kind[k] == 2 && kind[pi[k]] == 2) g[0]++;
            if (nolock[k]) g[1]++;
            if (kind[k] != 0 && kind[pinv[k]] == 0 && kind[pi[k]] != 0 && kind[pi[pi[k]]] == 0) g[2]++;
            if (kind[k] == 0 && lam[k] == -3) g[3]++; }
        for (auto &kv : f5) { auto &g = kv.second; if (cs[kv.first][2] != g[0] - 2 * g[1] - g[2] - 3 * g[3]) f5_bad++; }
        for (auto &z : cycles) { int r = find(z[0]); for (int32_t x : z) if (find(x) != r) { cyc_split++; break; } }
        std::vector<std::array<long long, 7>> sig;
        for (auto &kv : cs) { long long sz = kv.second[0], f = kv.second[1], sl = kv.second[2]; if (sl % 5 != 0 || 3 * f - (sz - f) != -sl) cls_bad++;
            auto &g = f5[kv.first]; sig.push_back({sz, f, sl / 5, g[0], g[1], g[2], g[3]}); }
        std::sort(sig.begin(), sig.end()); char b3[160];
        for (auto &t : sig) { snprintf(b3, sizeof b3, "%s[%lld, %lld, %lld, %lld, %lld, %lld, %lld]", clsig.empty() ? "" : ", ", t[0], t[1], t[2], t[3], t[4], t[5], t[6]); clsig += b3; }
    }
    // exits from positive cycles
    std::map<int, std::map<int, Exit>> exits;   // pos cycle -> target cycle -> counters
    struct LB { long long exits_DL = 0, exits_lb = 0, to_neg = 0, to_neg_lb = 0, nDL = 0, exits_any = 0, to_neg_any = 0; }; std::map<int, LB> lbs;
    { int c[64], nc[64]; u64 cm[4];
      for (int ci : pos) { LB &lb = lbs[ci];
        for (int32_t x : cycles[ci]) { unkey(ALL[x], c); masks(c, cm); StateInfo si = info_of(c, cm); bool dl = si.kind == 2; if (dl) lb.nDL++;
            for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; if (K & linkmask) continue;
                    long long t = swap_index(c, K, p, q, nc); if (t == x) continue; int cj = cyc[t]; if (cj == ci) continue;
                    Exit &e = exits[ci][cj]; e.any++; lb.exits_any++; if (wind[cj] < 0) lb.to_neg_any++;
                    if (dl) { e.dl++; lb.exits_DL++; bool ab = (p == si.al && (q == si.A || q == si.B)) || (q == si.al && (p == si.A || p == si.B));
                        if (ab) e.alphaAB++; else e.other++; bool isl = (K & si.lock) != 0; if (isl) { e.lb++; lb.exits_lb++; } else e.nonlb++;
                        if (!ab && isl) e.other_lb++; if (wind[cj] < 0) { lb.to_neg++; if (isl) lb.to_neg_lb++; } } } } } } }
    // transport per bipartite component of positive cycles (sinks = negative cycles)
    std::map<int, long long> Wm; for (size_t i = 0; i < cycles.size(); i++) Wm[i] = wind[i];
    auto edge_set = [&](int flag) { std::map<int, std::set<int>> E; for (int z : pos) { std::set<int> s; for (auto &kv : exits[z]) { const Exit &e = kv.second; if (wind[kv.first] >= 0) continue;
        long long v = flag == 0 ? e.dl : flag == 1 ? e.other : flag == 2 ? e.any : flag == 3 ? e.lb : e.other_lb; if (v) s.insert(kv.first); } E[z] = s; } return E; };
    std::map<int, std::set<int>> Eall = edge_set(2);
    // components of positive cycles via shared sinks (any-state edges give the coarsest grouping)
    std::map<int, int> comp; { std::map<int, std::vector<int>> by_sink; for (int z : pos) for (int s : Eall[z]) by_sink[s].push_back(z);
        std::map<int, int> up; for (int z : pos) up[z] = z; std::function<int(int)> f2 = [&](int x) { while (up[x] != x) { up[x] = up[up[x]]; x = up[x]; } return x; };
        for (auto &kv : by_sink) for (size_t i = 1; i < kv.second.size(); i++) { int a = f2(kv.second[0]), b = f2(kv.second[i]); if (a != b) up[a] = b; }
        for (int z : pos) comp[z] = f2(z); }
    std::string jobe;
    if (JOBE || SIGC || JOBG || JOBH) {
        int widx[5]; for (int t = 0; t < 5; t++) { int a = L[t], b = L[(t + 1) % 5]; const std::vector<int> &ra = rot[a]; int da = ra.size(), p = std::find(ra.begin(), ra.end(), b) - ra.begin();
            int c1 = ra[(p + 1) % da], c2 = ra[(p + da - 1) % da]; widx[t] = idx[c1 == hole ? c2 : c1]; }
        int hi[5]; for (int t = 0; t < 5; t++) hi[t] = rot[L[t]].size() >= 6;
        std::vector<int32_t> pinv(S); for (long long k = 0; k < S; k++) pinv[pi[k]] = (int32_t)k;
        int c[64], nc[64]; u64 cm[4];
        auto frame = [&](long long k, int &j, int &type, int &kmask, long long &sig, int &sig_l1, int &sig_l2, int &sig_kind) {
            unkey(ALL[k], c); masks(c, cm); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = c[link_[t]];
            for (j = 0; j < 5; j++) if (lc[j] == lc[(j + 2) % 5]) break;
            int al = lc[j], mu = lc[(j + 1) % 5], A = lc[(j + 3) % 5], B = lc[(j + 4) % 5];
            int w0 = c[widx[j]], w3 = c[widx[(j + 3) % 5]];
            type = (w0 == A) ? 1 : (w0 == B && w3 == al) ? 2 : (w0 == B && w3 == mu) ? 3 : 0;
            kmask = 0; for (int i = 0; i < 5; i++) if (hi[(j + i) % 5]) kmask |= 1 << i;
            u64 K = flood(1ULL << link_[(j + 1) % 5], cm[al] | cm[mu]); sig = swap_index(c, K, al, mu, nc);
            u64 cm2[4]; masks(nc, cm2); StateInfo si = info_of(nc, cm2); sig_l1 = si.l1; sig_l2 = si.l2; sig_kind = si.kind; };
        // sigma-joined groups over DD-step endpoints
        std::vector<int> up(cycles.size()); for (size_t i = 0; i < up.size(); i++) up[i] = i;
        std::function<int(int)> fu = [&](int x) { while (up[x] != x) { up[x] = up[up[x]]; x = up[x]; } return x; };
        long long nedges = 0, nendpoints = 0;
        for (long long k = 0; k < S; k++) { if (kind[k] != 2) continue; bool ep = kind[pi[k]] == 2 || kind[pinv[k]] == 2; if (!ep) continue;
            int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd); nendpoints++; int a = fu(cyc[k]), b = fu(cyc[sg]); if (cyc[k] != cyc[sg]) nedges++; if (a != b) up[a] = b; }
        std::map<int, std::pair<long long, int>> comp_sum; for (size_t i = 0; i < cycles.size(); i++) { auto &e = comp_sum[fu(i)]; e.first += wind[i]; e.second++; }
        long long nfail = 0, maxsum = -1000000000LL; int maxsize = 0; std::string firstfail;
        for (auto &kv : comp_sum) { maxsize = std::max(maxsize, kv.second.second); maxsum = std::max(maxsum, kv.second.first);
            if (kv.second.first > 0) { nfail++; if (firstfail.empty()) { char b4[128]; snprintf(b4, sizeof b4, "{\"sumw\": %lld, \"ncycles\": %d}", kv.second.first, kv.second.second); firstfail = b4; } } }
        char b5[512]; snprintf(b5, sizeof b5, ", \"pattern\": \"%s\", \"sigC\": {\"ncomp\": %zu, \"cross_edges\": %lld, \"endpoints\": %lld, \"max_ncycles\": %d, \"max_sumw\": %lld, \"fail\": %lld, \"first_fail\": %s}", jpat.c_str(), comp_sum.size(), nedges, nendpoints, maxsize, maxsum, nfail, firstfail.empty() ? "null" : firstfail.c_str());
        jobe += b5;
        if (JOBH) {   // Job H: sigma' = all link-free lock-breaking swaps (result not DL) from DD-step endpoints; H2 adds sigma at R3 endpoints
            std::vector<int> u1(cycles.size()), u2(cycles.size()); for (size_t i = 0; i < u1.size(); i++) u1[i] = u2[i] = i;
            auto fx = [](std::vector<int> &up, int x) { while (up[x] != x) { up[x] = up[up[x]]; x = up[x]; } return x; };
            long long nend = 0, nend_cross = 0;
            for (long long k = 0; k < S; k++) { if (kind[k] != 2) continue; if (!(kind[pi[k]] == 2 || kind[pinv[k]] == 2)) continue; nend++;
                unkey(ALL[k], c); masks(c, cm); bool cross = false;
                for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                    while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; if (K & linkmask) continue; long long t = swap_index(c, K, p, q, nc);
                        if (t == k || kind[t] == 2) continue; if (cyc[t] != cyc[k]) cross = true;
                        int a = fx(u1, cyc[k]), b = fx(u1, cyc[t]); if (a != b) u1[a] = b; a = fx(u2, cyc[k]); b = fx(u2, cyc[t]); if (a != b) u2[a] = b; } }
                if (cross) nend_cross++;
                int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd);
                if (ty == 3) { int a = fx(u2, cyc[k]), b = fx(u2, cyc[sg]); if (a != b) u2[a] = b; } }
            for (int v = 0; v < 2; v++) { std::vector<int> &up = v ? u2 : u1; std::map<int, std::pair<long long, int>> cs2;
                for (size_t i = 0; i < cycles.size(); i++) { auto &e = cs2[fx(up, i)]; e.first += wind[i]; e.second++; }
                long long nf = 0, mx = -1000000000LL; int ms = 0; std::string ff;
                for (auto &kv : cs2) { ms = std::max(ms, kv.second.second); mx = std::max(mx, kv.second.first); if (kv.second.first > 0) { nf++; if (ff.empty()) { char b4[96]; snprintf(b4, sizeof b4, "{\"sumw\": %lld, \"ncycles\": %d}", kv.second.first, kv.second.second); ff = b4; } } }
                char b5[400]; snprintf(b5, sizeof b5, ", \"%s\": {\"ncomp\": %zu, \"endpoints\": %lld, \"endpoints_with_cross_sigmap\": %lld, \"max_ncycles\": %d, \"max_sumw\": %lld, \"fail\": %lld, \"first_fail\": %s}",
                    v ? "H2_sigmap_plus_sigmaR3" : "H1_sigmap", cs2.size(), nend, nend_cross, ms, mx, nf, ff.empty() ? "null" : ff.c_str()); jobe += b5; } }







        if (JOBBT) {   // Job BT (NightImagesBoundary 4): per Gamma-cycle Z, per cycle T of Z's class: images by kind; per-cycle tallies and exact checks
            std::vector<int> gam; for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (all) gam.push_back(ci); }
            if (!gam.empty()) {
                std::vector<int32_t> cp(S); for (long long i = 0; i < S; i++) cp[i] = i;
                std::function<int(int)> cf = [&](int x) { while (cp[x] != x) { cp[x] = cp[cp[x]]; x = cp[x]; } return x; };
                { int cc[64], ncc[64]; u64 cmm[4];
                  for (long long i = 0; i < S; i++) { unkey(ALL[i], cc); masks(cc, cmm);
                    for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cmm[p] | cmm[q];
                        while (M) { u64 K = flood(M & -M, cmm[p] | cmm[q]); M &= ~K; long long j = swap_index(cc, K, p, q, ncc); int a = cf(i), b = cf(j); if (a != b) cp[a] = b; } } } }
                std::vector<int> ccl(cycles.size()); for (size_t i = 0; i < cycles.size(); i++) ccl[i] = cf(cycles[i][0]);
                std::set<int> gcl; for (int zi : gam) gcl.insert(ccl[zi]);
                size_t NCY = cycles.size(); std::vector<std::array<long long, 13>> st(NCY);   // e, b, F, N0, L1, L2, DL, E2, tau, DD, fmax, dlpartner, unused
                std::vector<int8_t> lk(S, -1);   // for unfilled non-DL: 0 lockless, 1 Lock1-only, 2 Lock2-only
                auto isb = [&](long long k) { return kind[k] != 0 && (kind[pinv[k]] == 0 || kind[pi[k]] == 0); };
                auto lockof = [&](long long k) { if (lk[k] < 0) { int cc[64]; u64 c4[4]; unkey(ALL[k], cc); masks(cc, c4); StateInfo si = info_of(cc, c4); lk[k] = (!si.l1 && !si.l2) ? 0 : (si.l1 ? 1 : 2); } return (int)lk[k]; };
                for (size_t i = 0; i < NCY; i++) { if (!gcl.count(ccl[i])) continue; auto &a = st[i]; long long run = 0;
                    for (int32_t x : cycles[i]) {
                        if (kind[x] == 0) { a[2]++; if (kind[pi[x]] == 0) a[8]++; }
                        else { if (kind[pinv[x]] == 0) a[0]++; if (isb(x)) a[1]++; if (kind[x] == 2) { a[6]++; if (kind[pi[x]] == 2) a[9]++; } else { int t = lockof(x); a[3 + t]++; }
                               if (kind[pinv[x]] == 0 && kind[pi[x]] != 0 && kind[pi[pi[x]]] == 0) a[7]++;
                               int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); if (sg != x && kd == 2) a[11]++; } }
                    // longest filled run
                    size_t Lc = cycles[i].size(); long long best = 0, cur = 0; for (size_t t = 0; t < 2 * Lc; t++) { if (kind[cycles[i][t % Lc]] == 0) { cur++; best = std::max(best, cur); } else cur = 0; } a[10] = std::min<long long>(best, Lc); }
                std::string o = ", \"jobbt\": ["; bool f1 = true;
                for (int zi : gam) { std::map<int, std::array<long long, 6>> nt; long long nonbR3 = 0, dlR3 = 0, dlR1 = 0;
                    for (int32_t x : cycles[zi]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); auto &e = nt[cyc[sg]];
                        if (sg == x) { e[5]++; continue; } e[0]++;
                        if (kind[sg] == 2) { e[4]++; if (ty == 3) dlR3++; else dlR1++; } else { int t = lockof(sg); e[1 + t]++; }
                        if (ty == 3 && (kind[sg] == 2 || !isb(sg))) nonbR3++; }
                    char b[160]; snprintf(b, sizeof b, "%s{\"w\": %lld, \"L\": %zu, \"nonboundary_R3_images\": %lld, \"DL_images_R3\": %lld, \"DL_images_R1\": %lld, \"T\": [", f1 ? "" : ", ", wind[zi], cycles[zi].size(), nonbR3, dlR3, dlR1); o += b; f1 = false; bool f2 = true;
                    for (size_t t = 0; t < NCY; t++) { if (ccl[t] != ccl[zi]) continue; std::array<long long, 6> e{}; if (nt.count(t)) e = nt[t]; auto &a = st[t];
                        char b2[400]; snprintf(b2, sizeof b2, "%s[%zu, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %zu, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %lld, %d]", f2 ? "" : ", ",
                            t, e[0], e[1], e[2], e[3], e[4], e[5], a[0], a[1], a[2], wind[t], cycles[t].size(), a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], (int)(t == (size_t)zi));
                        o += b2; f2 = false; }
                    o += "]}"; }
                o += "]"; jobe += o; } }
        if (JOBBQ) {   // Job BQ (NightBudget 1): B' slack on every sigma u sigma' group: slack = 2 N0 + E2 + 3 tau - 2 |R_rho|; exact identity 5 sum w = |DD| - 2 N0 - E2 - 3 tau
            std::vector<int> uu(cycles.size()); for (size_t i = 0; i < uu.size(); i++) uu[i] = i;
            auto fx = [](std::vector<int> &up, int x) { while (up[x] != x) { up[x] = up[up[x]]; x = up[x]; } return x; };
            std::vector<int> ty3(S, -1); auto isR3 = [&](long long k) { if (ty3[k] < 0) { int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd); ty3[k] = (ty == 3); } return ty3[k] == 1; };
            for (long long k = 0; k < S; k++) { if (kind[k] != 2) continue; if (!(kind[pi[k]] == 2 || kind[pinv[k]] == 2)) continue;
                int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd); { int a = fx(uu, cyc[k]), b = fx(uu, cyc[sg]); if (a != b) uu[a] = b; }
                unkey(ALL[k], c); masks(c, cm);
                for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                    while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; if (K & linkmask) continue; long long t = swap_index(c, K, p, q, nc);
                        if (t == k || kind[t] == 2) continue; int a = fx(uu, cyc[k]), b = fx(uu, cyc[t]); if (a != b) uu[a] = b; } } }
            struct GS { long long N0 = 0, E2 = 0, tau = 0, DD = 0, R = 0, sl = 0, pos = 0; };
            std::map<int, GS> G; std::set<long long> Rset;
            for (long long k = 0; k < S; k++) { auto &g = G[fx(uu, cyc[k])]; g.sl += lam[k];
                if (kind[k] != 0 && kind[pi[k]] == 0 && kind[pinv[k]] == 0) g.N0++;
                if (kind[k] != 0 && kind[pinv[k]] == 0 && kind[pi[k]] != 0 && kind[pi[pi[k]]] == 0) g.E2++;
                if (kind[k] == 0 && kind[pi[k]] == 0) g.tau++;
                if (kind[k] == 2 && kind[pi[k]] == 2) { g.DD++; long long r = isR3(k) ? k : (isR3(pi[k]) ? pi[k] : k); Rset.insert(r); } }
            for (long long r : Rset) G[fx(uu, cyc[r])].R++;
            for (size_t i = 0; i < cycles.size(); i++) if (wind[i] > 0) G[fx(uu, i)].pos = 1;
            long long mn = 1LL << 40, mnpos = 1LL << 40, nneg = 0, idfail = 0; std::map<long long, long long> hist;
            for (auto &kv : G) { auto &g = kv.second; long long slack = 2 * g.N0 + g.E2 + 3 * g.tau - 2 * g.R; mn = std::min(mn, slack); if (g.pos) mnpos = std::min(mnpos, slack); if (slack < 0) nneg++;
                if (g.sl != g.DD - 2 * g.N0 - g.E2 - 3 * g.tau) idfail++; hist[slack < 0 ? -1 : (slack < 10 ? slack : (slack < 100 ? 10 : 100))]++; }
            std::string o = ", \"jobbq\": {\"groups\": " + std::to_string(G.size()) + ", \"min_slack\": " + std::to_string(mn) + ", \"min_slack_posgroups\": " + std::to_string(mnpos) +
                ", \"neg\": " + std::to_string(nneg) + ", \"identity_fail\": " + std::to_string(idfail) + ", \"hist\": {"; bool f = true;
            for (auto &kv : hist) { o += f ? "" : ", "; o += "\"" + std::to_string(kv.first) + "\": " + std::to_string(kv.second); f = false; } o += "}}"; jobe += o; }
        if (JOBBP && (jpat == "6,6,6,6,6" || jpat == "5,5,6,6,6" || jpat == "5,5,7,5,7")) {   // Job BP: all single Kempe swaps at ring roles from every DL state
            auto dword = [&](int j) { std::string w; for (int i = 0; i < 5; i++) w += (char)('0' + std::min<int>(8, rot[L[(j + i) % 5]].size())); return w; };
            int mi[5]; for (int t = 0; t < 5; t++) { mi[t] = -1; if (rot[L[t]].size() != 6) continue; int pv = L[t];
                for (int w : rot[pv]) { if (w == hole) continue; int wi = idx[w]; if (wi == link_[(t + 1) % 5] || wi == link_[(t + 4) % 5] || wi == widx[(t + 4) % 5] || wi == widx[t]) continue; mi[t] = wi; } }
            std::map<std::string, std::array<long long, 6>> T; std::map<std::string, long long> MS; long long nDL = 0, nnone = 0; std::string noneex;
            static const char *RN = "amAB";   // role letters: alpha mu A B
            for (long long k = 0; k < S; k++) { if (kind[k] != 2) continue; nDL++; int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd);
                int cc[64], ncc[64]; u64 c4[4]; unkey(ALL[k], cc); masks(cc, c4); int lc[5]; for (int u = 0; u < 5; u++) lc[u] = cc[link_[u]];
                int role[4]; role[lc[j]] = 0; role[lc[(j + 1) % 5]] = 1; role[lc[(j + 3) % 5]] = 2; role[lc[(j + 4) % 5]] = 3;
                std::string base = jpat + " R" + std::to_string(ty) + " " + dword(j); u64 succ = 0; int bit = 0;
                for (int rr = 0; rr < 15; rr++) { int v; std::string rn;
                    if (rr < 5) { v = link_[(j + rr) % 5]; rn = "x" + std::to_string(rr); } else if (rr < 10) { v = widx[(j + rr - 5) % 5]; rn = "w" + std::to_string(rr - 5); } else { v = mi[(j + rr - 10) % 5]; rn = "m" + std::to_string(rr - 10); }
                    for (int d = 0, q = 0; d < 4; d++) { int cv = v >= 0 ? cc[v] : 0; if (d == cv) continue; int b = rr * 4 + role[d]; (void)bit; q++; if (v < 0) continue;
                        u64 K = flood(1ULL << v, c4[cv] | c4[d]); std::string pr; { char a1 = RN[role[cv]], a2 = RN[role[d]]; pr = std::string(1, a1) + a2; }
                        int out; if (K == (c4[cv] | c4[d])) out = 0; else { long long t2 = swap_index(cc, K, cv, d, ncc); u64 c5[4]; masks(ncc, c5); StateInfo si = info_of(ncc, c5);
                            out = si.kind == 0 ? 1 : (si.kind == 2 ? 4 : (!si.l1 && !si.l2 ? 2 : 3)); (void)t2; }
                        auto &e = T[base + " " + rn + " " + pr]; e[out]++; e[5]++; if (out != 0 && out != 4) succ |= 1ULL << b; } }
                MS[base + " " + std::to_string(succ)]++; if (!succ) { nnone++; if (noneex.size() < 300) noneex += (noneex.empty() ? "" : ", ") + std::to_string(k); } }
            std::string o = ", \"jobbp\": {\"nDL\": " + std::to_string(nDL) + ", \"no_escape\": " + std::to_string(nnone) + ", \"tab\": {"; bool f = true;
            for (auto &kv : T) { o += f ? "" : ", "; char b[128]; snprintf(b, sizeof b, "[%lld, %lld, %lld, %lld, %lld, %lld]", kv.second[0], kv.second[1], kv.second[2], kv.second[3], kv.second[4], kv.second[5]); o += "\"" + kv.first + "\": " + b; f = false; }
            o += "}, \"masks\": {"; f = true; for (auto &kv : MS) { o += f ? "" : ", "; o += "\"" + kv.first + "\": " + std::to_string(kv.second); f = false; } o += "}}"; jobe += o; }
        if (JOBBO && (jpat == "6,6,6,6,6" || jpat == "5,5,6,6,6" || jpat == "5,5,7,5,7")) {   // Job BO (+ NightG66 T2/T3 and PureClean): DL runs, run ends, cut radius, classes without filled states
            auto dword = [&](int j) { std::string w; for (int i = 0; i < 5; i++) w += (char)('0' + std::min<int>(8, rot[L[(j + i) % 5]].size())); return w; };
            int mi[5]; for (int t = 0; t < 5; t++) { mi[t] = -1; if (rot[L[t]].size() != 6) continue; int pv = L[t];
                for (int w : rot[pv]) { if (w == hole) continue; int wi = idx[w]; if (wi == link_[(t + 1) % 5] || wi == link_[(t + 4) % 5] || wi == widx[(t + 4) % 5] || wi == widx[t]) continue; mi[t] = wi; } }
            std::vector<int> dist(N, -1); std::vector<int> qq; for (int t = 0; t < 5; t++) { dist[link_[t]] = 1; qq.push_back(link_[t]); }
            for (size_t h2 = 0; h2 < qq.size(); h2++) { int u = qq[h2]; for (u64 f = adjm[u]; f; f &= f - 1) { int v = __builtin_ctzll(f); if (dist[v] < 0) { dist[v] = dist[u] + 1; qq.push_back(v); } } }
            int maxd = 0; for (int v = 0; v < N; v++) maxd = std::max(maxd, dist[v]); std::vector<u64> ball(maxd + 1, 0); for (int r = 1; r <= maxd; r++) for (int v = 0; v < N; v++) if (dist[v] <= r) ball[r] |= 1ULL << v;
            u64 allv = (N == 64) ? ~0ULL : ((1ULL << N) - 1);
            std::map<long long, long long> RL; std::map<std::string, long long> EH, CR; long long nall = 0, maxrun = 0; std::string allc; bool fa = true;
            for (size_t ci = 0; ci < cycles.size(); ci++) { const auto &z = cycles[ci]; size_t Lz = z.size(); bool all = true; for (int32_t x : z) if (kind[x] != 2) { all = false; break; }
                if (all) { nall++; long long nd = 0; for (int32_t x : z) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); if (sg != x && kd != 2) nd++; }
                    char b[96]; snprintf(b, sizeof b, "%s[%lld, %zu, %lld]", fa ? "" : ", ", wind[ci], Lz, nd); allc += b; fa = false; continue; }
                for (size_t i = 0; i < Lz; i++) { if (kind[z[i]] != 2 || kind[z[(i + Lz - 1) % Lz]] == 2) continue; size_t t = i; long long len = 0; while (kind[z[t % Lz]] == 2) { len++; t++; }
                    RL[len]++; maxrun = std::max(maxrun, len);
                    int32_t x = z[(t - 1) % Lz], yv = z[t % Lz]; int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd);
                    unkey(ALL[x], c); masks(c, cm); int lc[5]; for (int u = 0; u < 5; u++) lc[u] = c[link_[u]]; int al = lc[j], A = lc[(j + 3) % 5];
                    int role[4]; role[lc[j]] = 0; role[lc[(j + 1) % 5]] = 1; role[lc[(j + 3) % 5]] = 2; role[lc[(j + 4) % 5]] = 3; const char *RN = "amAB";
                    std::string ww; for (int u = 0; u < 5; u++) ww += RN[role[c[widx[(j + u) % 5]]]];
                    std::string mm; for (int u : {1, 4}) { int v = mi[(j + u) % 5]; mm += v < 0 ? '-' : RN[role[c[v]]]; }
                    u64 K = flood(1ULL << link_[(j + 2) % 5], cm[al] | cm[A]);
                    std::string lb, wb; for (int u = 0; u < 5; u++) { lb += (K >> link_[(j + u) % 5] & 1) ? '1' : '0'; wb += (K >> widx[(j + u) % 5] & 1) ? '1' : '0'; }
                    std::string leave; int rcut = -1;
                    if (kind[yv] == 0) leave = "filled";
                    else { int cc[64]; unkey(ALL[yv], cc); u64 c4[4]; masks(cc, c4); StateInfo si = info_of(cc, c4);
                        leave = si.l1 && !si.l2 ? "Lock1-only" : (!si.l1 && si.l2 ? "Lock2-only" : (!si.l1 && !si.l2 ? "lockless" : "DL?"));
                        int j2 = 0; int l5[5]; for (int u = 0; u < 5; u++) l5[u] = cc[link_[u]]; for (; j2 < 5; j2++) if (l5[j2] == l5[(j2 + 2) % 5]) break;
                        int mu2 = l5[(j2 + 1) % 5], A2 = l5[(j2 + 3) % 5], B2 = l5[(j2 + 4) % 5]; int mv = link_[(j2 + 1) % 5];
                        int other = !si.l2 ? B2 : A2; int endv = !si.l2 ? link_[(j2 + 4) % 5] : link_[(j2 + 3) % 5];   // the dead lock: Lock2 if dead, else Lock1
                        u64 pairm = c4[mu2] | c4[other];
                        for (int r = 1; r <= maxd; r++) { u64 blockers = ball[r] & ~pairm; u64 Kr = flood(1ULL << mv, allv & ~blockers); if (!(Kr >> endv & 1)) { rcut = r; break; } } }
                    int j2 = -1, ty2 = -1; if (kind[yv] != 0) { int km2, a1, a2, a3; long long sg2; frame(yv, j2, ty2, km2, sg2, a1, a2, a3); }
                    std::string key = "last R" + std::to_string(ty) + " " + dword(j) + " -> " + leave + (ty2 >= 0 ? " R" + std::to_string(ty2) + " " + dword(j2) : std::string("")) + " | K∩x(j..j+4) " + lb + " K∩w(j..j+4) " + wb + " | len " + (len >= 10 ? std::string("10+") : std::to_string(len));
                    EH[key]++; CR["wword " + ww + " m(j+1,j+4) " + mm + " -> " + leave + " rcut " + std::to_string(rcut)]++; } }
            // PureClean: Kempe classes of T - h without a filled state
            long long ncls = 0, nofill = 0; double minfn = 2.0; std::string clist;
            if (!NOCLS) { std::vector<int32_t> cp(S); for (long long i = 0; i < S; i++) cp[i] = i;
              std::function<int(int)> cf = [&](int x) { while (cp[x] != x) { cp[x] = cp[cp[x]]; x = cp[x]; } return x; };
              int cc[64], ncc[64]; u64 cmm[4];
              for (long long i = 0; i < S; i++) { unkey(ALL[i], cc); masks(cc, cmm);
                for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cmm[p] | cmm[q];
                    while (M) { u64 Kk = flood(M & -M, cmm[p] | cmm[q]); M &= ~Kk; long long jx = swap_index(cc, Kk, p, q, ncc); int a = cf(i), b = cf(jx); if (a != b) cp[a] = b; } } }
              std::map<int, long long> fil, csz; for (long long i = 0; i < S; i++) { auto &e = fil[cf(i)]; csz[cf(i)]++; if (kind[i] == 0) e++; } ncls = fil.size(); for (auto &kv : fil) { if (!kv.second) nofill++; double fr = (double)kv.second / csz[kv.first]; if (fr < minfn) minfn = fr; if (clist.size() < 4000) clist += (clist.empty() ? "" : ", ") + std::string("[") + std::to_string(csz[kv.first]) + ", " + std::to_string(kv.second) + "]"; } }
            std::string o = ", \"jobbo\": {\"all_DL_cycles\": [" + allc + "], \"maxrun\": " + std::to_string(maxrun) + ", \"maxdist\": " + std::to_string(maxd) + ", \"classes\": " + std::to_string(ncls) + ", \"classes_without_filled\": " + std::to_string(nofill) + ", \"min_F_over_N\": " + std::to_string(minfn) + ", \"class_sizes_F\": [" + clist + "], \"runlen\": {"; bool f = true;
            for (auto &kv : RL) { o += f ? "" : ", "; o += "\"" + std::to_string(kv.first) + "\": " + std::to_string(kv.second); f = false; }
            o += "}, \"ends\": {"; f = true; for (auto &kv : EH) { o += f ? "" : ", "; o += "\"" + kv.first + "\": " + std::to_string(kv.second); f = false; }
            o += "}, \"cut\": {"; f = true; for (auto &kv : CR) { o += f ? "" : ", "; o += "\"" + kv.first + "\": " + std::to_string(kv.second); f = false; } o += "}}"; jobe += o; }
        if (JOBBL) {   // Job BL: every DL state: key = type R<ty> + link degrees from x_j (x_j .. x_{j+4}, capped 8) + sigma-image outcome (fixed / DL / notDL);
                       // every all-DL pi-orbit: #non-fixed non-DL sigma-images, and the set of (type, degree-word) positions it visits.
            std::map<std::string, long long> H; std::string g; bool f1 = true;
            auto dword = [&](int j) { std::string w; for (int i = 0; i < 5; i++) w += (char)('0' + std::min<int>(8, rot[L[(j + i) % 5]].size())); return w; };
            for (long long k = 0; k < S; k++) { if (kind[k] != 2) continue; int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd);
                H["R" + std::to_string(ty) + " " + dword(j) + " " + (sg == k ? "fixed" : (kd == 2 ? "DL" : "notDL"))]++; }
            for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
                long long nd = 0; std::set<std::string> vis;
                for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); if (sg != x && kd != 2) nd++; vis.insert("R" + std::to_string(ty) + dword(j)); }
                std::string vs; for (auto &v : vis) { vs += vs.empty() ? "" : " "; vs += v; }
                char b[96]; snprintf(b, sizeof b, "%s[%lld, %zu, %lld, \"", f1 ? "" : ", ", wind[ci], cycles[ci].size(), nd); g += b; g += vs + "\"]"; f1 = false; }
            std::string o = ", \"jobbl\": {\"states\": {"; bool f2 = true; for (auto &kv : H) { o += f2 ? "" : ", "; o += "\"" + kv.first + "\": " + std::to_string(kv.second); f2 = false; }
            o += "}, \"gamma\": [" + g + "]}"; jobe += o; }
        if (JOBBK && !pos.empty()) {   // Job BK: statement (c) on every positive cycle, giant-cycle statistics per Kempe class, Hall check on the giant
            std::vector<int32_t> cp(S); for (long long i = 0; i < S; i++) cp[i] = i;
            std::function<int(int)> cf = [&](int x) { while (cp[x] != x) { cp[x] = cp[cp[x]]; x = cp[x]; } return x; };
            { int cc[64], ncc[64]; u64 cmm[4];
              for (long long i = 0; i < S; i++) { unkey(ALL[i], cc); masks(cc, cmm);
                for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cmm[p] | cmm[q];
                    while (M) { u64 K = flood(M & -M, cmm[p] | cmm[q]); M &= ~K; long long j = swap_index(cc, K, p, q, ncc); int a = cf(i), b = cf(j); if (a != b) cp[a] = b; } } } }
            std::map<int, int> clsid; std::vector<int> ccl(cycles.size());
            for (size_t i = 0; i < cycles.size(); i++) { int r = cf(cycles[i][0]); if (!clsid.count(r)) { int k = clsid.size(); clsid[r] = k; } ccl[i] = clsid[r]; }
            int NC = clsid.size(); std::vector<long long> csz(NC, 0), cF(NC, 0), cnc(NC, 0); std::vector<int> giant(NC, -1);
            for (long long k = 0; k < S; k++) { int c2 = clsid[cf(k)]; csz[c2]++; if (kind[k] == 0) cF[c2]++; }
            for (size_t i = 0; i < cycles.size(); i++) { int c2 = ccl[i]; cnc[c2]++; if (giant[c2] < 0 || wind[i] < wind[giant[c2]]) giant[c2] = i; }
            std::vector<long long> gF(NC, 0); for (int c2 = 0; c2 < NC; c2++) for (int32_t x : cycles[giant[c2]]) if (kind[x] == 0) gF[c2]++;
            // lockless credits from DD endpoints of positive cycles (Job AQ / S convention) onto nonpositive cycles
            std::map<int, long long> credit_on;
            for (long long k = 0; k < S; k++) { if (kind[k] != 2 || wind[cyc[k]] <= 0) continue; if (!(kind[pi[k]] == 2 || kind[pinv[k]] == 2)) continue;
                int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd); if (!(kd == 1 && !l1 && !l2) || cyc[sg] == cyc[k] || wind[cyc[sg]] > 0) continue;
                long long y = pi[sg], f = 0; while (kind[y] == 0) { f++; y = pi[y]; } credit_on[cyc[sg]] += 3 * f - 1; }
            std::vector<long long> need(NC, 0); std::string o = ", \"jobbk\": {\"pos\": ["; bool f1 = true;
            for (int zi : pos) { const auto &z = cycles[zi]; bool okA = false, okD = false; std::set<int> hit; long long bestneg = -(1LL << 40);
                for (int32_t x : z) { if (kind[x] == 0) continue; int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); if (sg == x) continue;
                    int T = cyc[sg]; if (T == zi) continue; hit.insert(T); bestneg = std::max(bestneg, -wind[T]); bool ok = wind[T] <= -wind[zi]; if (ok) okA = true;
                    if (ok && kind[x] == 2 && (kind[pi[x]] == 2 || kind[pinv[x]] == 2)) okD = true; }
                int c2 = ccl[zi]; bool hg = hit.count(giant[c2]) > 0; if (hg) need[c2] += 5 * wind[zi];
                bool gam = true; for (int32_t x : z) if (kind[x] != 2) { gam = false; break; }
                char b[220]; snprintf(b, sizeof b, "%s[%lld, %zu, %d, %d, %d, %zu, %d, %d, %lld]", f1 ? "" : ", ", wind[zi], z.size(), (int)gam, (int)okA, (int)okD, hit.size(), (int)hg, c2, bestneg); o += b; f1 = false; }
            o += "], \"classes\": ["; f1 = true; std::set<int> pc; for (int zi : pos) pc.insert(ccl[zi]);
            for (int c2 : pc) { int g = giant[c2]; long long remg = 5 * wind[g] + (credit_on.count(g) ? credit_on[g] : 0);
                char b[240]; snprintf(b, sizeof b, "%s[%d, %lld, %lld, %lld, %lld, %zu, %lld, %lld, %lld]", f1 ? "" : ", ", c2, cnc[c2], csz[c2], cF[c2], wind[g], cycles[g].size(), gF[c2], need[c2], remg); o += b; f1 = false; }
            o += "]}"; jobe += o; }
        if (JOBBJ) {   // Job BJ: U = sigma (all DD endpoints) u sigma' (link-free swaps from DD endpoints, result not DL) groups: max group sum w, #groups with sum w > 0;
                       // Gamma-cycles: per cycle #states whose sigma-image is not DL (a fixed point counts as DL); min over Gamma; floor: min over Kempe classes of F/N (needs --full).
            std::vector<int> uu(cycles.size()); for (size_t i = 0; i < uu.size(); i++) uu[i] = i;
            auto fx = [](std::vector<int> &up, int x) { while (up[x] != x) { up[x] = up[up[x]]; x = up[x]; } return x; };
            for (long long k = 0; k < S; k++) { if (kind[k] != 2) continue; if (!(kind[pi[k]] == 2 || kind[pinv[k]] == 2)) continue;
                int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd); { int a = fx(uu, cyc[k]), b = fx(uu, cyc[sg]); if (a != b) uu[a] = b; }
                unkey(ALL[k], c); masks(c, cm);
                for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                    while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; if (K & linkmask) continue; long long t = swap_index(c, K, p, q, nc);
                        if (t == k || kind[t] == 2) continue; int a = fx(uu, cyc[k]), b = fx(uu, cyc[t]); if (a != b) uu[a] = b; } } }
            std::map<int, std::pair<long long, int>> gs; for (size_t i = 0; i < cycles.size(); i++) { auto &e = gs[fx(uu, i)]; e.first += wind[i]; e.second++; }
            long long mx = -(1LL << 40), nf = 0; for (auto &kv : gs) { mx = std::max(mx, kv.second.first); if (kv.second.first > 0) nf++; }
            long long mx_pos = -(1LL << 40); { std::set<int> pg; for (size_t i = 0; i < cycles.size(); i++) if (wind[i] > 0) pg.insert(fx(uu, i)); for (int g : pg) mx_pos = std::max(mx_pos, gs[g].first); }
            long long minND = -1, nG = 0;
            for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue; nG++;
                long long nd = 0; for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); if (sg != x && kind[sg] != 2) nd++; }
                if (minND < 0 || nd < minND) minND = nd; }
            double minFN = 2.0; long long ncl = 0;
            if (FULL) { std::map<int, std::pair<long long, long long>> cf; for (long long k = 0; k < S; k++) { auto &e = cf[find(k)]; e.first++; if (kind[k] == 0) e.second++; }
                for (auto &kv : cf) { ncl++; minFN = std::min(minFN, (double)kv.second.second / kv.second.first); } }
            char b[400]; snprintf(b, sizeof b, ", \"jobbj\": {\"U_groups\": %zu, \"U_max_sumw\": %lld, \"U_max_sumw_posgroups\": %lld, \"U_fail\": %lld, \"gamma\": %lld, \"gamma_min_nonDL_sigma\": %lld, \"classes\": %lld, \"min_F_over_N\": %.6f}",
                gs.size(), mx, mx_pos, nf, nG, minND, ncl, minFN); jobe += b; }
        if (JOBAK && jpat == "5,5,5,5,6") {   // Job AK (1): W2* on maximal DL runs: at R3k2 (kmask 4) whose next four pi-steps stay DL: R3k2 fixed => R3k0 (4 steps later) not fixed
            long long ntest = 0, nfix2 = 0, nfail = 0, nbadshape = 0, nfail2pp = 0; std::string ce, ce2; std::map<std::string, long long> whereG; std::map<std::string, long long> cnt[2]; std::map<std::string, std::map<long long, long long>> alDist; std::map<std::string, std::map<std::string, long long>> alLeave; long long minTC[2] = {1LL << 40, 1LL << 40}; std::string ceL; std::map<long long, long long> backDist;
            for (size_t ci = 0; ci < cycles.size(); ci++) { const auto &z = cycles[ci]; size_t Lz = z.size(); bool gam = true; for (int32_t x : z) if (kind[x] != 2) { gam = false; break; }
                for (size_t i = 0; i < Lz; i++) { if (kind[z[i]] != 2) continue; bool ok = true; for (int t = 1; t <= 4; t++) if (kind[z[(i + t) % Lz]] != 2) { ok = false; break; } if (!ok) continue;
                    if (!gam && Lz < 5) continue;
                    int j, ty, km, l1, l2, kd; long long sg; frame(z[i], j, ty, km, sg, l1, l2, kd); if (!(ty == 3 && km == 4)) continue;
                    int j2, ty2, km2, a1, a2, a3; long long sg2; frame(z[(i + 4) % Lz], j2, ty2, km2, sg2, a1, a2, a3); if (!(ty2 == 3 && km2 == 1)) { nbadshape++; continue; }
                    ntest++; bool f2 = (sg == z[i]), f0 = (sg2 == z[(i + 4) % Lz]); if (f2) nfix2++;
                    // W2'': at R3k2 or R3k0 some {A,B}-cycle passes through y or z  <=> (fan lemma) y or z has an {alpha,mu}-neighbour outside K_sigma
                    int t6 = -1; for (int t = 0; t < 5; t++) if (rot[L[t]].size() >= 6) t6 = t;
                    int yv = widx[(t6 + 4) % 5], zv = widx[t6];
                    auto w2pp = [&](long long st, std::string &where) { int cc[64]; unkey(ALL[st], cc); u64 c4[4]; masks(cc, c4); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = cc[link_[t]];
                        int jj = 0; for (; jj < 5; jj++) if (lc[jj] == lc[(jj + 2) % 5]) break; int al = lc[jj], mu = lc[(jj + 1) % 5];
                        u64 Ks = flood(1ULL << link_[(jj + 1) % 5], c4[al] | c4[mu]); bool any = false;
                        for (int v : {yv, zv}) { u64 nb = adjm[v] & (c4[al] | c4[mu]) & ~Ks; if (nb) { any = true; int w = __builtin_ctzll(nb); std::string lab = "out";
                                for (int t = 0; t < 5; t++) { if (w == link_[t]) lab = "x" + std::to_string((t - t6 + 5) % 5); if (w == widx[t]) lab = "w" + std::to_string((t - t6 + 5) % 5); }
                                where += (v == yv ? "y:" : "z:") + lab + " "; } }
                        return any; };
                    std::string wa, wb; bool g2 = w2pp(z[i], wa), g0 = w2pp(z[(i + 4) % Lz], wb);
                    { // second addendum (NightW2 10.4): R = w3 not in K_sigma(R3k2) or w0 not in K_sigma(R3k0); outside-2-ball escape; R1k4: p ~ x4 in {c(p), c(z)}
                      auto ksig = [&](long long st) { int cc[64]; unkey(ALL[st], cc); u64 c4[4]; masks(cc, c4); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = cc[link_[t]];
                          int jj = 0; for (; jj < 5; jj++) if (lc[jj] == lc[(jj + 2) % 5]) break; return flood(1ULL << link_[(jj + 1) % 5], c4[lc[jj]] | c4[lc[(jj + 1) % 5]]); };
                      bool in1 = ksig(z[i]) >> widx[(t6 + 1) % 5] & 1, in2 = ksig(z[(i + 4) % Lz]) >> widx[(t6 + 3) % 5] & 1; bool R = !in1 || !in2;
                      bool outesc = wa.find("out") != std::string::npos || wb.find("out") != std::string::npos;
                      int cc[64]; unkey(ALL[z[(i + 1) % Lz]], cc); u64 c4[4]; masks(cc, c4); int pv = link_[t6], x4 = link_[(t6 + 2) % 5];
                      bool px4 = flood(1ULL << pv, c4[cc[pv]] | c4[cc[zv]]) >> x4 & 1;
                      int G = gam ? 1 : 0; cnt[G]["windows"]++; if (f2 && f0) cnt[G]["W2star_fail"]++; if (!g2 && !g0) cnt[G]["W2pp_fail"]++;
                      if (!R) { cnt[G]["R_fail"]++; if (g2 || g0) cnt[G]["R_fail_W2pp_holds"]++; if (outesc) cnt[G]["R_fail_outside_escape"]++; }
                      {   // NightW2 section 11: six-pair ranks / components at positions 3..9; identity total rank = total components - 8; lemma L-death; backward lock-death distance
                          auto sixpair = [&](long long st, long long &trank, long long &tcomp) { int cc[64]; unkey(ALL[st], cc); u64 c4[4]; masks(cc, c4); trank = 0; tcomp = 0;
                              for (int a = 0; a < 4; a++) for (int b2 = a + 1; b2 < 4; b2++) { u64 M = c4[a] | c4[b2]; long long V = __builtin_popcountll(M), E = 0, C = 0;
                                  for (u64 t = M; t; t &= t - 1) { int u = __builtin_ctzll(t); E += __builtin_popcountll(adjm[u] & M); } E /= 2;
                                  for (u64 t = M; t; ) { u64 K = flood(t & -t, M); t &= ~K; C++; } trank += E - V + C; tcomp += C; } };
                          for (int q = -1; q <= 5; q++) { long long st = z[(i + q + Lz) % Lz]; long long tr, tc; sixpair(st, tr, tc);
                              cnt[G][(tr == tc - 8) ? "identity_ok" : "identity_FAIL"]++; if (kind[st] == 2) { minTC[G] = std::min(minTC[G], tc); cnt[G]["DL_states_checked"]++; } }
                          int jq, tq, kq, q1, q2, q3; long long sq; frame(z[(i + 2) % Lz], jq, tq, kq, sq, q1, q2, q3); bool f1b = (tq == 3 && sq == z[(i + 2) % Lz]);
                          if (f2 && f1b && f0) {   // L-death: preceding R1k0 (position 3) lacks Lock1, or following R1k2 (position 9) lacks Lock2
                              auto locks = [&](long long st, int &a1, int &a2) { if (kind[st] == 0) { a1 = a2 = 0; return; } int cc[64]; unkey(ALL[st], cc); u64 c4[4]; masks(cc, c4); StateInfo si = info_of(cc, c4); a1 = si.l1; a2 = si.l2; };
                              int p1, p2, n1, n2; locks(z[(i + Lz - 1) % Lz], p1, p2); locks(z[(i + 5) % Lz], n1, n2);
                              bool ok = (!p1) || (!n2); cnt[G][ok ? "Ldeath_ok" : "Ldeath_FAIL"]++;
                              if (!ok && ceL.empty()) { char b[128]; snprintf(b, sizeof b, "{\"cycle\": %zu, \"pos\": %zu, \"gamma\": %s}", ci, i, gam ? "true" : "false"); ceL = b; }
                              if (!gam) { long long d = 0; size_t e = i; while (kind[z[(e + Lz - 1) % Lz]] == 2 && d < (long long)Lz) { e = (e + Lz - 1) % Lz; d++; } backDist[d + 1]++; } } }
                      if (!gam) {   // Job AL: distance from R3k0 to the run end, and the leaving step, per failure category
                          bool f1 = false; { int jq, tq, kq, q1, q2, q3; long long sq; frame(z[(i + 2) % Lz], jq, tq, kq, sq, q1, q2, q3); f1 = (tq == 3 && sq == z[(i + 2) % Lz]); }
                          std::vector<std::string> cats; if (f2 && f0) cats.push_back("W2star_fail"); if (f2 && f1 && f0) cats.push_back("all3_fixed"); if (!g2 && !g0) cats.push_back("W2pp_fail");
                          if (!R && (g2 || g0)) cats.push_back("R_fail_W2pp_holds"); cats.push_back("all_windows");
                          size_t e = (i + 4) % Lz; long long d = 0; while (kind[z[(e + 1) % Lz]] == 2 && d < (long long)Lz) { e = (e + 1) % Lz; d++; } d++;   // steps from R3k0 to the first non-DL state
                          int je, te, ke, l1e, l2e, kde; long long sge; frame(z[e], je, te, ke, sge, l1e, l2e, kde);
                          long long nx = pi[z[e]]; int nk = kind[nx]; int n1 = 0, n2 = 0; if (nk == 1) { int c5[64]; unkey(ALL[nx], c5); u64 m5[4]; masks(c5, m5); StateInfo si = info_of(c5, m5); n1 = si.l1; n2 = si.l2; }
                          int ce6[64]; unkey(ALL[z[e]], ce6); u64 cm6[4]; masks(ce6, cm6); int lc6[5]; for (int t = 0; t < 5; t++) lc6[t] = ce6[link_[t]];
                          int al6 = lc6[je], A6 = lc6[(je + 3) % 5]; u64 K6 = flood(1ULL << link_[(je + 2) % 5], cm6[al6] | cm6[A6]);
                          int pv6 = link_[t6], mv6 = -1; for (int w : rot[L[t6]]) { if (w == hole) continue; int wi = idx[w]; if (wi == link_[(t6 + 1) % 5] || wi == link_[(t6 + 4) % 5] || wi == yv || wi == zv) continue; mv6 = wi; }
                          std::string pr, cp; int V4[4] = {pv6, mv6, yv, zv}; const char *nmv = "pmyz";
                          for (int q = 0; q < 4; q++) { if (ce6[V4[q]] == al6 || ce6[V4[q]] == A6) pr += nmv[q]; if (K6 >> V4[q] & 1) cp += nmv[q]; }
                          char key[200]; snprintf(key, sizeof key, "last R%d k%d -> %s (L1 %d L2 %d) step pair %s comp %s", te, ke == 1 ? 0 : ke == 2 ? 1 : ke == 4 ? 2 : ke == 8 ? 3 : ke == 16 ? 4 : -1,
                              nk == 0 ? "filled" : nk == 2 ? "DL" : "unfilled", n1, n2, pr.c_str(), cp.empty() ? "-" : cp.c_str());
                          for (auto &cname : cats) { alDist[cname][d]++; if (cname != "all_windows") alLeave[cname][key]++; } }
                      cnt[G][px4 ? "R1k4_p~x4" : "R1k4_p!~x4"]++; cnt[G][std::string("w3inKs_") + (in1 ? "1" : "0") + "_w0inKs_" + (in2 ? "1" : "0")]++; }
                    if (!g2 && !g0) { nfail2pp++; if (ce2.empty()) { char b[96]; snprintf(b, sizeof b, "{\"cycle\": %zu, \"pos\": %zu, \"gamma\": %s}", ci, i, gam ? "true" : "false"); ce2 = b; } }
                    if (gam) { if (g2) whereG["k2 " + wa]++; if (g0) whereG["k0 " + wb]++; }

                    if (f2 && f0) { nfail++; if (ce.empty()) { char b[160]; snprintf(b, sizeof b, "{\"cycle\": %zu, \"pos\": %zu, \"gamma\": %s, \"states\": [%d, %d, %d, %d, %d]}", ci, i, gam ? "true" : "false", z[i], z[(i + 1) % Lz], z[(i + 2) % Lz], z[(i + 3) % Lz], z[(i + 4) % Lz]); ce = b; } } } }
            std::string wg; for (auto &kv : whereG) { char b[96]; snprintf(b, sizeof b, "%s\"%s\": %lld", wg.empty() ? "" : ", ", kv.first.c_str(), kv.second); wg += b; }
            char b2[400]; snprintf(b2, sizeof b2, ", \"jobak\": {\"tests\": %lld, \"k2_fixed\": %lld, \"fail\": %lld, \"badshape\": %lld, \"fail_w2pp\": %lld, \"first\": %s, \"first_w2pp\": %s, \"where_gamma\": {", ntest, nfix2, nfail, nbadshape, nfail2pp, ce.empty() ? "null" : ce.c_str(), ce2.empty() ? "null" : ce2.c_str()); jobe += b2; jobe += wg; jobe += "}";
            for (int G = 0; G < 2; G++) { jobe += G ? ", \"gamma_counts\": {" : ", \"run_counts\": {"; bool f = true; for (auto &kv : cnt[G]) { char b[96]; snprintf(b, sizeof b, "%s\"%s\": %lld", f ? "" : ", ", kv.first.c_str(), kv.second); jobe += b; f = false; } jobe += "}"; }
            jobe += ", \"al_dist\": {"; { bool f = true; for (auto &kv : alDist) { jobe += std::string(f ? "" : ", ") + "\"" + kv.first + "\": {"; bool g = true; for (auto &kv2 : kv.second) { char b[48]; snprintf(b, sizeof b, "%s\"%lld\": %lld", g ? "" : ", ", kv2.first, kv2.second); jobe += b; g = false; } jobe += "}"; f = false; } }
            jobe += "}, \"al_leave\": {"; { bool f = true; for (auto &kv : alLeave) { jobe += std::string(f ? "" : ", ") + "\"" + kv.first + "\": {"; bool g = true; for (auto &kv2 : kv.second) { jobe += std::string(g ? "" : ", ") + "\"" + kv2.first + "\": " + std::to_string(kv2.second); g = false; } jobe += "}"; f = false; } }
            { char b[200]; snprintf(b, sizeof b, "}, \"minTC_run\": %lld, \"minTC_gamma\": %lld, \"first_Ldeath_fail\": %s, \"back_dist\": {", minTC[0], minTC[1], ceL.empty() ? "null" : ceL.c_str()); jobe += b;
              bool f = true; for (auto &kv : backDist) { char b3[48]; snprintf(b3, sizeof b3, "%s\"%lld\": %lld", f ? "" : ", ", kv.first, kv.second); jobe += b3; f = false; } }
            jobe += "}}"; }
        if (JOBAB && jpat == "5,5,5,5,6") {   // Job AB: excursion-level Lemma S. Excursion = maximal unfilled run (u) + following filled run (f) on a cycle with filled states.
            long long nexc = 0, npos = 0, fail_all = 0, fail_cross = 0, minslack_all = (1LL << 60), minslack_cross = (1LL << 60); std::map<long long, long long> massh; std::string fx;
            for (size_t ci = 0; ci < cycles.size(); ci++) { const auto &z = cycles[ci]; size_t Lz = z.size(); size_t s0 = Lz;
                for (size_t i = 0; i < Lz; i++) if (kind[z[i]] != 0 && kind[z[(i + Lz - 1) % Lz]] == 0) { s0 = i; break; }
                if (s0 == Lz) continue;   // Gamma-cycle or all-filled cycle: no excursion
                size_t i = 0;
                while (i < Lz) { std::vector<int32_t> ex; long long u = 0, f = 0;
                    while (i < Lz && kind[z[(s0 + i) % Lz]] != 0) { ex.push_back(z[(s0 + i) % Lz]); u++; i++; }
                    while (i < Lz && kind[z[(s0 + i) % Lz]] == 0) { ex.push_back(z[(s0 + i) % Lz]); f++; i++; }
                    nexc++; long long mass = 0; for (int32_t x : ex) mass += lam[x];
                    if (mass <= 0) continue; npos++; massh[mass]++;
                    long long cra = 0, crc = 0;
                    for (int32_t x : ex) { if (!(kind[x] == 2 && (kind[pi[x]] == 2 || kind[pinv[x]] == 2))) continue;
                        int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); if (!(kd == 1 && !l1 && !l2)) continue;
                        long long y = pi[sg], ff = 0; while (kind[y] == 0) { ff++; y = pi[y]; } cra += 3 * ff - 1; if (cyc[sg] != (int)ci) crc += 3 * ff - 1; }
                    minslack_all = std::min(minslack_all, cra - mass); minslack_cross = std::min(minslack_cross, crc - mass);
                    if (cra < mass) fail_all++; if (crc < mass) fail_cross++;
                    if ((cra < mass || crc < mass) && fx.size() < 3000) { char b[200]; snprintf(b, sizeof b, "%s[%zu, %lld, %lld, %lld, %lld, %lld, %lld]", fx.empty() ? "" : ", ", ci, wind[ci], u, f, mass, cra, crc); fx += b; } } }
            std::string mh; for (auto &kv : massh) { char b[40]; snprintf(b, sizeof b, "%s[%lld, %lld]", mh.empty() ? "" : ", ", kv.first, kv.second); mh += b; }
            char b2[300]; snprintf(b2, sizeof b2, ", \"jobab\": {\"excursions\": %lld, \"positive\": %lld, \"fail_all\": %lld, \"fail_cross\": %lld, \"minslack_all\": %lld, \"minslack_cross\": %lld, \"mass_hist\": [",
                nexc, npos, fail_all, fail_cross, npos ? minslack_all : 0, npos ? minslack_cross : 0);
            jobe += b2; jobe += mh; jobe += "], \"fails\": ["; jobe += fx; jobe += "]}"; }
        if (JOBX) {   // Job X: maximal DL runs along pi at (5,5,5,5,6) holes; pairs of R3@k4 visits 10 steps apart with both sigma-exits not lockless
            int nhi = 0; for (int t = 0; t < 5; t++) if (rot[L[t]].size() >= 6) nhi++;
            if (nhi == 1 && jpat == "5,5,5,5,6") {
                long long nruns = 0, npairs = 0, ngamma = 0, nwbad = 0; long long nwin[2] = {0, 0}, wfail[2][4] = {{0,0,0,0},{0,0,0,0}}; std::string ev, wex; bool fe = true;
                for (size_t ci = 0; ci < cycles.size(); ci++) { const auto &z = cycles[ci]; size_t Lz = z.size(); bool all = true; for (int32_t x : z) if (kind[x] != 2) { all = false; break; }
                    std::vector<std::vector<int32_t>> runs;
                    if (all) { runs.push_back(z); ngamma++; }
                    else { for (size_t i = 0; i < Lz; i++) { if (kind[z[i]] != 2 || kind[z[(i + Lz - 1) % Lz]] == 2) continue; std::vector<int32_t> rr; size_t t = i; while (kind[z[t % Lz]] == 2) { rr.push_back(z[t % Lz]); t++; } runs.push_back(rr); } }
                    for (auto &rr : runs) { nruns++; size_t R = rr.size(); std::vector<int> fail(R, -1);
                        for (size_t i = 0; i < R; i++) { int j, ty, km, l1, l2, kd; long long sg; frame(rr[i], j, ty, km, sg, l1, l2, kd); if (ty == 3 && km == 16) fail[i] = (kd == 1 && !l1 && !l2) ? 0 : 1; }
                        { std::vector<int> kk(R, -1), ok(R, 0); std::vector<long long> fv(R, -1);
                          for (size_t i = 0; i < R; i++) { int j, ty, km, l1, l2, kd; long long sg; frame(rr[i], j, ty, km, sg, l1, l2, kd); if (ty != 3) continue;
                              kk[i] = km == 1 ? 0 : km == 2 ? 1 : km == 4 ? 2 : km == 8 ? 3 : km == 16 ? 4 : -1; if (kd == 1 && !l1 && !l2) { ok[i] = 1; long long y = pi[sg], f = 0; while (kind[y] == 0) { f++; y = pi[y]; } fv[i] = f; } }
                          for (size_t i = 0; i < R; i++) { if (kk[i] != 3) continue; if (!all && i + 8 >= R) continue; size_t q[5]; for (int t = 0; t < 5; t++) q[t] = (i + 2 * t) % R;
                              if (kk[q[1]] != 2 || kk[q[2]] != 1 || kk[q[3]] != 0 || kk[q[4]] != 4) { nwbad++; continue; }
                              long long cr = 0; for (int t = 0; t < 5; t++) if (ok[q[t]]) cr += 3 * fv[q[t]] - 1;
                              bool W1 = ok[q[0]] || ok[q[4]], W2 = ok[q[1]] || ok[q[2]] || ok[q[3]], W4 = ok[q[4]] || (ok[q[0]] && fv[q[0]] == 3);
                              nwin[all ? 1 : 0]++; if (cr < 10) wfail[all ? 1 : 0][0]++; if (!W1) wfail[all ? 1 : 0][1]++; if (!W2) wfail[all ? 1 : 0][2]++; if (!W4) wfail[all ? 1 : 0][3]++;
                              if ((cr < 10 || !W1 || !W2 || !W4) && wex.size() < 2000) { char b[200]; snprintf(b, sizeof b, "%s{\"gamma\": %s, \"cycle\": %zu, \"pos\": %zu, \"credit\": %lld, \"W1\": %d, \"W2\": %d, \"W4\": %d, \"dist_to_run_end\": %lld}",
                                  wex.empty() ? "" : ", ", all ? "true" : "false", ci, i, cr, (int)W1, (int)W2, (int)W4, all ? -1LL : (long long)(R - (i + 8))); wex += b; } } }
                        for (size_t i = 0; i < R; i++) { size_t i2 = i + 10; if (all) i2 %= R; else if (i2 >= R) continue; if (fail[i] < 0 || fail[i2] < 0) continue; npairs++;
                            if (fail[i] == 1 && fail[i2] == 1) { char b[256];
                                if (all) snprintf(b, sizeof b, "%s{\"gamma\": true, \"cycle\": %zu, \"L\": %zu, \"dist\": -1}", fe ? "" : ", ", ci, R);
                                else { int j, ty, km, l1, l2, kd; long long sg; frame(rr[R - 1], j, ty, km, sg, l1, l2, kd); long long nx = pi[rr[R - 1]];
                                    int nk = kind[nx]; int a1 = 0, a2 = 0; if (nk == 1) { int cc[64]; unkey(ALL[nx], cc); u64 c4[4]; masks(cc, c4); StateInfo si = info_of(cc, c4); a1 = si.l1; a2 = si.l2; }
                                    snprintf(b, sizeof b, "%s{\"gamma\": false, \"cycle\": %zu, \"run_len\": %zu, \"first_fail_pos\": %zu, \"dist\": %zu, \"last_DL_type\": %d, \"last_DL_kmask\": %d, \"next_kind\": %d, \"next_lock1\": %d, \"next_lock2\": %d}",
                                        fe ? "" : ", ", ci, R, i, R - i2, ty, km, nk, a1, a2); }
                                ev += b; fe = false; } } } }
                char b2[400]; snprintf(b2, sizeof b2, ", \"jobx\": {\"runs\": %lld, \"gamma\": %lld, \"k4_pairs\": %lld, \"windows\": [%lld, %lld], \"windows_malformed\": %lld, \"wfail_run\": [%lld, %lld, %lld, %lld], \"wfail_gamma\": [%lld, %lld, %lld, %lld], \"events\": [", nruns, ngamma, npairs, nwin[0], nwin[1], nwbad, wfail[0][0], wfail[0][1], wfail[0][2], wfail[0][3], wfail[1][0], wfail[1][1], wfail[1][2], wfail[1][3]); jobe += b2; jobe += ev; jobe += "], \"wfail_examples\": ["; jobe += wex; jobe += "]}"; } }



        if (JOBBGH) {  // Job BH: windows with positions 4..8 DL (R3k2 R1k4 R3k1 R1k3 R3k0), Gamma and open runs, link pattern 5,5,5,5,{6,7}. Position-4 frame names (alpha = 1).
                       // Record F4 F5 F7 F8 (sigma fixed), W = w3's G_12-component at position 6 (G_12 = {alpha, B} at position 6), K6 = step-6 component ({alpha, A} of x_{j+2}), W meets K6?
                       // Job BG (degree 6): windows u0..u20 all DL from R3k4 (positions 0..9, 0..9, 0): T3 / T13 = step-3 / step-13 component contains a far neighbour of m;
                       // B0 = J false at u9, B1 = J false at u19.
            int nhi = 0, t6 = -1, dg = 0; for (int t = 0; t < 5; t++) if (rot[L[t]].size() >= 6) { nhi++; t6 = t; dg = rot[L[t]].size(); }
            if (nhi == 1 && (dg == 6 || dg == 7)) {
                int p = link_[t6], y = widx[(t6 + 4) % 5], z = widx[t6], w3 = widx[(t6 + 3) % 5]; std::map<std::string, long long> H;
                u64 named = linkmask; for (int t = 0; t < 5; t++) named |= 1ULL << widx[t]; u64 farm = 0; int m = -1;
                if (dg == 6) { int pv = order[p], mv = -1; for (int w : rot[pv]) { if (w == hole) continue; int wi = idx[w]; if (wi == link_[(t6 + 1) % 5] || wi == link_[(t6 + 4) % 5] || wi == y || wi == z) continue; mv = w; }
                    m = idx[mv]; named |= 1ULL << m; farm = adjm[m] & ~named; }
                static const int PT[10] = {3, 1, 3, 1, 3, 1, 3, 1, 3, 1}, PK[10] = {4, 1, 3, 0, 2, 4, 1, 3, 0, 2};
                for (size_t ci = 0; ci < cycles.size(); ci++) { const auto &zc = cycles[ci]; size_t Lz = zc.size(); bool all = true; for (int32_t x : zc) if (kind[x] != 2) { all = false; break; }
                    std::vector<std::vector<int32_t>> runs;
                    if (all) runs.push_back(zc);
                    else for (size_t i = 0; i < Lz; i++) { if (kind[zc[i]] != 2 || kind[zc[(i + Lz - 1) % Lz]] == 2) continue; std::vector<int32_t> rr; size_t t = i; while (kind[zc[t % Lz]] == 2) { rr.push_back(zc[t % Lz]); t++; } runs.push_back(rr); }
                    std::string G = all ? "G" : "O";
                    for (auto &rr : runs) { size_t R = rr.size(); std::vector<int> ty(R), kk(R), jj(R), fx(R);
                        for (size_t i = 0; i < R; i++) { int j, t2, km, l1, l2, kd; long long sg; frame(rr[i], j, t2, km, sg, l1, l2, kd); ty[i] = t2; kk[i] = km ? __builtin_ctz(km) : -1; jj[i] = j; fx[i] = (sg == rr[i]); }
                        auto at = [&](size_t i, int pos) { return ty[i % R] == PT[pos] && kk[i % R] == PK[pos]; };
                        auto stepK = [&](size_t i) { unkey(ALL[rr[i % R]], c); masks(c, cm); int j = jj[i % R]; int al = c[link_[j]], A = c[link_[(j + 3) % 5]]; return flood(1ULL << link_[(j + 2) % 5], cm[al] | cm[A]); };
                        for (size_t i = 0; i < R; i++) {
                            // BH window: i = position 4
                            if ((all || i + 4 < R) && at(i, 4) && at(i + 1, 5) && at(i + 2, 6) && at(i + 3, 7) && at(i + 4, 8)) {
                                size_t i6 = (i + 2) % R; unkey(ALL[rr[i6]], c); masks(c, cm); int j = jj[i6]; int al = c[link_[j]], B = c[link_[(j + 4) % 5]];
                                u64 W = flood(1ULL << w3, cm[al] | cm[B]); u64 K6 = stepK(i + 2);
                                std::string key = "BH " + G + std::to_string(dg) + " F4" + (fx[i % R] ? "1" : "0") + " F5" + (fx[(i + 1) % R] ? "1" : "0") + " F7" + (fx[(i + 3) % R] ? "1" : "0") + " F8" + (fx[(i + 4) % R] ? "1" : "0")
                                    + " w3inG12=" + ((cm[al] | cm[B]) >> w3 & 1 ? "y" : "n") + " meetsK6=" + ((W & K6) ? "y" : "n") + " |W|=" + std::to_string(__builtin_popcountll(W)); H[key]++; }
                            // BG window: i = position 0, 21 states
                            if (dg == 6 && (all || i + 20 < R) && at(i, 0) && at(i + 10, 0) && at(i + 20, 0)) {
                                bool ok = true; for (int t = 0; t <= 20 && ok; t++) if (!at(i + t, t % 10)) ok = false; if (!ok) continue;
                                int T3 = (stepK(i + 3) & farm) ? 1 : 0, T13 = (stepK(i + 13) & farm) ? 1 : 0;
                                unkey(ALL[rr[(i + 9) % R]], c); masks(c, cm); int B0 = !((flood(1ULL << y, cm[c[y]] | cm[c[z]]) >> z) & 1);
                                unkey(ALL[rr[(i + 19) % R]], c); masks(c, cm); int B1 = !((flood(1ULL << y, cm[c[y]] | cm[c[z]]) >> z) & 1);
                                std::string key = "BG " + G + (all ? " L=" + std::to_string(R) : "") + " B0=" + std::to_string(B0) + " B1=" + std::to_string(B1) + " T3=" + std::to_string(T3) + " T13=" + std::to_string(T13); H[key]++; } } } }
                std::string o = ", \"jobbgh\": {"; bool f = true;
                for (auto &kv : H) { o += f ? "" : ", "; o += "\"" + kv.first + "\": " + std::to_string(kv.second); f = false; } o += "}"; jobe += o; } }
        if (JOBBC) {   // Job BC (NightW2Euler 2-3): windows = 7 consecutive DL states at positions 3..9 (R1k0 R3k2 R1k4 R3k1 R1k3 R3k0 R1k2) on Gamma-cycles and maximal DL runs,
                       // at holes with one link vertex of degree 6 or 7 (5,5,5,5,6 / 5,5,5,5,7). Colours named at the window's R3k2 state: 1 = c(p), 3 = c(y), 4 = c(z), 2 = the fourth.
                       // C(1c) = #components of G_{1c} in T - h. Events: s3 C12 >=2 -> 1, s4 C12 1 -> >=2, s5 C13 >=2 -> 1, s6 C13 1 -> >=2, s7 C14 >=2 -> 1, s8 C14 1 -> >=2.
                       // Dualities checked at every window state: r(AB) = C(al mu) - 1, r(mu A) = C(al B) - 1 - Lock1, r(mu B) = C(al A) - 1 - Lock2.
            int nhi = 0, t6 = -1, dg = 0; for (int t = 0; t < 5; t++) if (rot[L[t]].size() >= 6) { nhi++; t6 = t; dg = rot[L[t]].size(); }
            if (nhi == 1 && (dg == 6 || dg == 7)) {
                int p = link_[t6], y = widx[(t6 + 4) % 5], z = widx[t6]; std::map<std::string, long long> H; long long dfail = 0, dchk = 0, namefail = 0;
                auto ncomp = [&](u64 M) { int k = 0; while (M) { u64 K = flood(M & -M, M); M &= ~K; k++; } return k; };
                auto rk = [&](u64 M) { long long e = 0; for (u64 f = M; f; f &= f - 1) e += __builtin_popcountll(adjm[__builtin_ctzll(f)] & M); return e / 2 - __builtin_popcountll(M) + ncomp(M); };
                static const int WT[7] = {1, 3, 1, 3, 1, 3, 1}, WK[7] = {0, 2, 4, 1, 3, 0, 2};
                for (size_t ci = 0; ci < cycles.size(); ci++) { const auto &zc = cycles[ci]; size_t Lz = zc.size(); bool all = true; for (int32_t x : zc) if (kind[x] != 2) { all = false; break; }
                    std::vector<std::vector<int32_t>> runs;
                    if (all) runs.push_back(zc);
                    else for (size_t i = 0; i < Lz; i++) { if (kind[zc[i]] != 2 || kind[zc[(i + Lz - 1) % Lz]] == 2) continue; std::vector<int32_t> rr; size_t t = i; while (kind[zc[t % Lz]] == 2) { rr.push_back(zc[t % Lz]); t++; } runs.push_back(rr); }
                    for (auto &rr : runs) { size_t R = rr.size(); std::vector<int> ty(R), kk(R), jj(R);
                        for (size_t i = 0; i < R; i++) { int j, t2, km, l1, l2, kd; long long sg; frame(rr[i], j, t2, km, sg, l1, l2, kd); ty[i] = t2; kk[i] = km ? __builtin_ctz(km) : -1; jj[i] = j; }
                        for (size_t i = 0; i < R; i++) { if (!all && i + 6 >= R) continue; bool ok = true; for (int t = 0; t < 7; t++) { size_t q = (i + t) % R; if (ty[q] != WT[t] || kk[q] != WK[t]) { ok = false; break; } } if (!ok) continue;
                            static const int RM[7] = {3, 2, 4, 3, 2, 4, 3}, RA[7] = {4, 3, 2, 4, 3, 2, 4}, RB[7] = {2, 4, 3, 2, 4, 3, 2};
                            int C[7][5]; bool fx[7];
                            for (int t = 0; t < 7; t++) { size_t q = (i + t) % R; unkey(ALL[rr[q]], c); masks(c, cm);
                                int lc[5]; for (int u = 0; u < 5; u++) lc[u] = c[link_[u]]; int j = jj[q]; int al = lc[j], mu = lc[(j + 1) % 5], A = lc[(j + 3) % 5], B = lc[(j + 4) % 5];
                                int byname[5]; byname[1] = al; byname[RM[t]] = mu; byname[RA[t]] = A; byname[RB[t]] = B; for (int a = 2; a <= 4; a++) C[t][a] = ncomp(cm[al] | cm[byname[a]]);
                                if (t == 1 && !(c[p] == al && c[y] == A && c[z] == B)) namefail++;
                                u64 Km = flood(1ULL << link_[(j + 1) % 5], cm[al] | cm[mu]); fx[t] = Km == (cm[al] | cm[mu]);
                                int L1 = (int)(flood(1ULL << link_[(j + 1) % 5], cm[mu] | cm[A]) >> link_[(j + 3) % 5] & 1), L2 = (int)(flood(1ULL << link_[(j + 1) % 5], cm[mu] | cm[B]) >> link_[(j + 4) % 5] & 1);
                                dchk++; if (rk(cm[A] | cm[B]) != ncomp(cm[al] | cm[mu]) - 1 || rk(cm[mu] | cm[A]) != ncomp(cm[al] | cm[B]) - 1 - L1 || rk(cm[mu] | cm[B]) != ncomp(cm[al] | cm[A]) - 1 - L2) dfail++; }
                            int ev[6] = { C[0][2] >= 2 && C[1][2] == 1, C[1][2] == 1 && C[2][2] >= 2, C[2][3] >= 2 && C[3][3] == 1, C[3][3] == 1 && C[4][3] >= 2, C[4][4] >= 2 && C[5][4] == 1, C[5][4] == 1 && C[6][4] >= 2 };
                            std::string key = std::string(all ? "G" : "O") + std::to_string(dg) + " ev"; for (int t = 0; t < 6; t++) key += ev[t] ? '1' : '0';
                            key += " F468 "; key += fx[1] ? 'F' : '-'; key += fx[3] ? 'F' : '-'; key += fx[5] ? 'F' : '-';
                            key += " C"; for (int t = 0; t < 7; t++) { key += ' '; for (int a = 2; a <= 4; a++) key += (char)('0' + std::min(C[t][a], 9)); }
                            H[key]++; } } }
                std::string o = ", \"jobbc\": {\"dual_checked\": " + std::to_string(dchk) + ", \"dual_fail\": " + std::to_string(dfail) + ", \"name_fail\": " + std::to_string(namefail) + ", \"hist\": {"; bool f = true;
                for (auto &kv : H) { o += f ? "" : ", "; o += "\"" + kv.first + "\": " + std::to_string(kv.second); f = false; } o += "}}"; jobe += o; } }
        if (JOBBB) {   // Job BB (NightA34Two 9.2): one-period Phi test on all maximal DL runs and Gamma-cycles at (5,5,5,5,6). Pair = R3k4 u0 with u0..u10 DL and u10 R3k4.
                       // B = k4 failure at u10 (sigma-exit not lockless). Candidates: 0 |K_{c(p),c(m)}(p)| at R3k4; 1 Lock2 witness |K_{mu,B}(x_{j+1})| at R3k4; 2+i |K_i| = step-i component
                       // ({alpha,A}-component of x_{j+2} at u_i vs u_{10+i}; needs u_{10+i} DL).
            int nhi = 0, t6 = -1; for (int t = 0; t < 5; t++) if (rot[L[t]].size() >= 6) { nhi++; t6 = t; }
            if (nhi == 1 && jpat == "5,5,5,5,6") {
                const int NC = 12; long long npair[2] = {0, 0}, nB[2] = {0, 0}, jmis[2] = {0, 0}, av[2][2][NC], vs[2][2][NC], vl[2][2][NC];
                for (int a = 0; a < 2; a++) for (int b = 0; b < 2; b++) for (int k = 0; k < NC; k++) av[a][b][k] = vs[a][b][k] = vl[a][b][k] = 0;
                int p = link_[t6], y = widx[(t6 + 4) % 5], z = widx[t6]; int pv = order[p], mv = -1;
                for (int w : rot[pv]) { if (w == hole) continue; int wi = idx[w]; if (wi == link_[(t6 + 1) % 5] || wi == link_[(t6 + 4) % 5] || wi == y || wi == z) continue; mv = w; }
                int m = idx[mv]; std::string ex; int nex = 0;
                auto feat = [&](int32_t x, long long *v, int &isr3k4, int &okk) {   // v[0], v[1] at R3k4; v[2] = step component size
                    int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); okk = (kd == 1 && !l1 && !l2); isr3k4 = (ty == 3 && km == 16);
                    unkey(ALL[x], c); masks(c, cm); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = c[link_[t]];
                    int al = lc[j], mu = lc[(j + 1) % 5], A = lc[(j + 3) % 5], B = lc[(j + 4) % 5];
                    v[0] = __builtin_popcountll(flood(1ULL << p, cm[c[p]] | cm[c[m]])); v[1] = __builtin_popcountll(flood(1ULL << link_[(j + 1) % 5], cm[mu] | cm[B]));
                    v[2] = __builtin_popcountll(flood(1ULL << link_[(j + 2) % 5], cm[al] | cm[A])); };
                for (size_t ci = 0; ci < cycles.size(); ci++) { const auto &zc = cycles[ci]; size_t Lz = zc.size(); bool all = true; for (int32_t x : zc) if (kind[x] != 2) { all = false; break; }
                    std::vector<std::vector<int32_t>> runs;
                    if (all) runs.push_back(zc);
                    else for (size_t i = 0; i < Lz; i++) { if (kind[zc[i]] != 2 || kind[zc[(i + Lz - 1) % Lz]] == 2) continue; std::vector<int32_t> rr; size_t t = i; while (kind[zc[t % Lz]] == 2) { rr.push_back(zc[t % Lz]); t++; } runs.push_back(rr); }
                    int g = all ? 1 : 0;
                    for (auto &rr : runs) { size_t R = rr.size(); std::vector<std::array<long long, 3>> F(R); std::vector<int> r34(R), okv(R), J(R);
                        for (size_t i = 0; i < R; i++) { long long v[3]; int a, o; feat(rr[i], v, a, o); F[i] = {v[0], v[1], v[2]}; r34[i] = a; okv[i] = o;
                            unkey(ALL[rr[i]], c); masks(c, cm); J[i] = (int)(flood(1ULL << y, cm[c[y]] | cm[c[z]]) >> z & 1); }
                        for (size_t i = 0; i < R; i++) { if (!r34[i]) continue; size_t i10 = i + 10; if (!all && i10 >= R) continue; i10 %= R; if (!r34[i10]) continue;
                            npair[g]++; int Bk = !okv[i10]; nB[g] += Bk; if (Bk != !J[(i + 9) % R]) jmis[g]++;
                            for (int k = 0; k < NC; k++) { long long a, b;
                                if (k < 2) { a = F[i][k]; b = F[i10][k]; }
                                else { size_t ii = i + (k - 2), jj = i + 10 + (k - 2); if (!all && jj >= R) continue; a = F[ii % R][2]; b = F[jj % R][2]; }
                                av[g][Bk][k]++; if (a >= b) vs[g][Bk][k]++; if (a > b) vl[g][Bk][k]++; }
                            if (Bk && F[i][0] >= F[i10][0] && nex < 6) { char e[160]; snprintf(e, sizeof e, "%s[%d, %zu, %zu, %lld, %lld, %lld]", nex ? ", " : "", g, ci, i, F[i][0], F[i10][0], all ? -1LL : (long long)R); ex += e; nex++; } } } }
                std::string o = ", \"jobbb\": {\"pairs\": [" + std::to_string(npair[0]) + ", " + std::to_string(npair[1]) + "], \"breaks\": [" + std::to_string(nB[0]) + ", " + std::to_string(nB[1]) + "], \"J_mismatch\": [" + std::to_string(jmis[0]) + ", " + std::to_string(jmis[1]) + "], \"cand\": [";
                for (int k = 0; k < NC; k++) { o += k ? ", [" : "["; for (int gg = 0; gg < 2; gg++) for (int b = 0; b < 2; b++) { o += (gg || b) ? ", " : ""; o += std::to_string(av[gg][b][k]) + ", " + std::to_string(vs[gg][b][k]) + ", " + std::to_string(vl[gg][b][k]); } o += "]"; }
                o += "], \"kpm_viol_examples\": [" + ex + "]}"; jobe += o; } }
        if (JOBS) {   // Job S (NightF6Flow 1.1): exits = R3 DD-endpoint states of a positive cycle Z with lockless sigma-image on a cycle T != Z
            auto isDDend = [&](long long k) { return kind[k] == 2 && (kind[pi[k]] == 2 || kind[pinv[k]] == 2); };
            std::map<int, long long> hitsum, nhits; std::map<int, std::set<long long>> hitstates; std::string exl; std::string ss = ", \"jobs\": {\"pos\": ["; bool f1 = true; std::set<int> needT;
            for (size_t ci = 0; ci < cycles.size(); ci++) { if (wind[ci] <= 0) continue; bool gam = true; long long crN = 0, crP = 0, crN_other = 0; std::set<int> nb;
                for (int32_t x : cycles[ci]) { if (kind[x] != 2) gam = false; if (!isDDend(x)) continue; int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd);
                    if (cyc[sg] != (int)ci && wind[cyc[sg]] <= 0) nb.insert(cyc[sg]);
                    if ((!ALLTYPES && ty != 3) || !(kd == 1 && !l1 && !l2) || cyc[sg] == (int)ci) continue;
                    long long y = pi[sg], f = 0; while (kind[y] == 0) { f++; y = pi[y]; } int T = cyc[sg];
                    if (wind[T] <= 0 && ty != 3) crN_other += 3 * f - 1;
                    { char e[96]; snprintf(e, sizeof e, "%s[%zu, %d, %lld, %d]", exl.empty() ? "" : ", ", ci, T, 3 * f - 1, ty); exl += e; }
                    if (wind[T] <= 0) { crN += 3 * f - 1; hitsum[T] += 1 - 3 * f; nhits[T]++; hitstates[T].insert(sg); } else crP += 3 * f - 1; }
                long long Lam = 5 * wind[ci], def = Lam - crN;
                char b[200]; snprintf(b, sizeof b, "%s{\"id\": %zu, \"Lambda\": %lld, \"gamma\": %s, \"L\": %zu, \"CrN\": %lld, \"CrN_nonR3\": %lld, \"CrP\": %lld, \"def\": %lld, \"nbrN\": [", f1 ? "" : ", ", ci, Lam, gam ? "true" : "false", cycles[ci].size(), crN, crN_other, crP, def);
                ss += b; f1 = false; bool f2 = true; for (int t : nb) { char e[16]; snprintf(e, sizeof e, "%s%d", f2 ? "" : ", ", t); ss += e; f2 = false; needT.insert(t); } ss += "]}"; }
            ss += "], \"targets\": ["; bool f3 = true; for (auto &kv : hitsum) needT.insert(kv.first);
            for (int t : needT) { long long hs = hitsum.count(t) ? hitsum[t] : 0, nh = nhits.count(t) ? nhits[t] : 0, nd = hitstates.count(t) ? hitstates[t].size() : 0;
                char b[160]; snprintf(b, sizeof b, "%s[%d, %lld, %zu, %lld, %lld, %lld, %lld]", f3 ? "" : ", ", t, 5 * wind[t], cycles[t].size(), hs, nh, nd, 5 * wind[t] - hs); ss += b; f3 = false; }
            ss += "], \"exits\": ["; ss += exl; ss += "]}"; jobe += ss; }
        if (JOBQ) {   // Job Q: per state of each Gamma-cycle: sigma fixed point? (the {alpha,mu}-component of m is all of those colours), sigma(x) lockless?, and the step's component vs K_sigma
            std::string qq = ", \"jobq\": ["; bool f1 = true;
            for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
                qq += f1 ? "[" : ", ["; f1 = false; bool f2 = true; int pos = 0;
                for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd);
                    unkey(ALL[x], c); masks(c, cm); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = c[link_[t]]; int al = lc[j], mu = lc[(j + 1) % 5], A = lc[(j + 3) % 5];
                    u64 Ks = flood(1ULL << link_[(j + 1) % 5], cm[al] | cm[mu]); bool fixedp = Ks == (cm[al] | cm[mu]); bool lockless = (kd == 1 && !l1 && !l2);
                    u64 K = flood(1ULL << link_[(j + 2) % 5], cm[al] | cm[A]);
                    int cc[64]; unkey(ALL[pi[x]], cc); u64 cm2[4]; masks(cc, cm2); int lc2[5]; for (int t = 0; t < 5; t++) lc2[t] = cc[link_[t]];
                    int j2 = 0; for (; j2 < 5; j2++) if (lc2[j2] == lc2[(j2 + 2) % 5]) break; u64 Ks2 = flood(1ULL << link_[(j2 + 1) % 5], cm2[lc2[j2]] | cm2[lc2[(j2 + 1) % 5]]);
                    u64 rest = (cm[al] | cm[mu]) & ~Ks;
                    char b[200]; snprintf(b, sizeof b, "%s[%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d]", f2 ? "" : ", ", pos, ty, km, fixedp ? 1 : 0, lockless ? 1 : 0,
                        __builtin_popcountll(K), __builtin_popcountll(K & Ks), __builtin_popcountll(K & Ks2), __builtin_popcountll(Ks), __builtin_popcountll(rest), (int)((K & rest) != 0));
                    qq += b; f2 = false; pos++; }
                qq += "]"; }
            qq += "]"; jobe += qq; }
        if (JOBP) {   // Job P: P1 = role-edge bridge vectors at every R3 state of Gamma-cycles at (5,5,5,5,6); P2 = geometry of every step's swapped component
            int t6 = -1, nhi = 0; for (int t = 0; t < 5; t++) if (rot[L[t]].size() >= 6) { t6 = t; nhi++; }
            if (nhi == 1) {
                int p = link_[t6], y = widx[(t6 + 4) % 5], z = widx[t6]; int mv = -1; for (int w : rot[L[t6]]) { if (w == hole) continue; int wi = idx[w]; if (wi == link_[(t6 + 1) % 5] || wi == link_[(t6 + 4) % 5] || wi == y || wi == z) continue; mv = w; }
                int m = idx[mv];
                std::vector<int> dv(N, -1); { std::vector<int> q; for (int t = 0; t < 5; t++) { dv[link_[t]] = 1; q.push_back(link_[t]); } for (size_t h = 0; h < q.size(); h++) { u64 nb = adjm[q[h]]; while (nb) { int w = __builtin_ctzll(nb); nb &= nb - 1; if (dv[w] < 0) { dv[w] = dv[q[h]] + 1; q.push_back(w); } } } }
                auto bridge = [&](const int *cc, const u64 *cmm, int a, int b) {   // is edge ab a bridge of G[{v} + vertices coloured c(a) or c(b)]?
                    u64 M = cmm[cc[a]] | cmm[cc[b]]; u64 seen = 1ULL << a; bool vseen = false; std::vector<int> st{a};
                    while (!st.empty()) { int u = st.back(); st.pop_back(); u64 nb = adjm[u] & M & ~seen; if (u == a) nb &= ~(1ULL << b);
                        if ((linkmask >> u & 1) && !vseen) { vseen = true; for (int t = 0; t < 5; t++) { int lv = link_[t]; if ((M >> lv & 1) && !(seen >> lv & 1) && !(u == a && lv == b)) { if (lv == b) return false; seen |= 1ULL << lv; st.push_back(lv); } } }
                        while (nb) { int w = __builtin_ctzll(nb); nb &= nb - 1; if (w == b) return false; seen |= 1ULL << w; st.push_back(w); } }
                    return true; };
                std::string pp = ", \"jobp\": {\"cycles\": ["; bool f1 = true;
                for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
                    pp += f1 ? "[" : ", ["; f1 = false; bool f2 = true; int pos = 0;
                    for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd);
                        unkey(ALL[x], c); masks(c, cm); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = c[link_[t]]; int al = lc[j], A = lc[(j + 3) % 5];
                        // P2: the step's swapped component K
                        u64 K = flood(1ULL << link_[(j + 2) % 5], cm[al] | cm[A]); int dK = 99; for (int i = 0; i < N; i++) if (K >> i & 1) dK = std::min(dK, dv[i]);
                        u64 Myz = cm[c[y]] | cm[c[z]]; u64 Kyz = flood(1ULL << y, Myz); bool yz = Kyz >> z & 1; int inter = __builtin_popcountll(K & Kyz);
                        bool cut = yz && !(flood(1ULL << y, Myz & ~K) >> z & 1);   // K meets every y-z {c(y),c(z)}-path
                        int onpath = -1; if (yz) { std::vector<int> par(N, -2); std::vector<int> q{y}; par[y] = -1; for (size_t h = 0; h < q.size(); h++) { u64 nb = adjm[q[h]] & Myz; while (nb) { int w = __builtin_ctzll(nb); nb &= nb - 1; if (par[w] == -2) { par[w] = q[h]; q.push_back(w); } } }
                            onpath = 0; for (int u = z; u != -1; u = par[u]) if (K >> u & 1) onpath++; }
                        u64 all_but = ((N == 64) ? ~0ULL : ((1ULL << N) - 1)) & ~K; bool sepT = !(flood(1ULL << y, all_but) >> z & 1);
                        // P1: role vertices x0..x4, w0..w4, m (relative to j); edges among them; bridge bits
                        int R[11]; for (int i = 0; i < 5; i++) { R[i] = link_[(j + i) % 5]; R[5 + i] = widx[(j + i) % 5]; } R[10] = m;
                        std::string eb; if (ty == 3) { for (int a = 0; a < 11; a++) for (int b = a + 1; b < 11; b++) { if (R[a] == R[b] || !(adjm[R[a]] >> R[b] & 1) || c[R[a]] == c[R[b]]) continue; char e[24]; snprintf(e, sizeof e, "%s\"%d-%d\": %d", eb.empty() ? "" : ", ", a, b, bridge(c, cm, R[a], R[b]) ? 1 : 0); eb += e; } }
                        bool lockless = (kd == 1 && !l1 && !l2); long long f = -1; if (ty == 3 && lockless) { long long yy = pi[sg]; f = 0; while (kind[yy] == 0) { f++; yy = pi[yy]; } }
                        char b[300]; snprintf(b, sizeof b, "%s{\"pos\": %d, \"type\": %d, \"kmask\": %d, \"exit\": \"%c\", \"f\": %lld, \"K\": [%d, %d, %d, %d, %d, %d, %d], \"edges\": {",
                            f2 ? "" : ", ", pos, ty, km, ty != 3 ? '-' : lockless ? 'L' : (kd == 1 ? (l1 ? '1' : '2') : (kd == 2 ? (sg == x ? 'X' : 'D') : 'F')), f,
                            __builtin_popcountll(K), dK, yz ? 1 : 0, inter, cut ? 1 : 0, onpath, sepT ? 1 : 0); pp += b; pp += eb; pp += "}}"; f2 = false; pos++; }
                    pp += "]"; }
                pp += "]}"; jobe += pp; } }
        if (JOBO) {   // Job O: per pi-step of Gamma-cycles at (5,5,5,5,6): p = degree-6 link vertex, y = w_{t-1}, z = w_t, m = p's third outer neighbour
            int t6 = -1, nhi = 0; for (int t = 0; t < 5; t++) if (rot[L[t]].size() >= 6) { t6 = t; nhi++; }
            if (nhi == 1) {
                int p = link_[t6], y = widx[(t6 + 4) % 5], z = widx[t6]; int mv = -1; for (int w : rot[L[t6]]) { if (w == hole) continue; int wi = idx[w]; if (wi == link_[(t6 + 1) % 5] || wi == link_[(t6 + 4) % 5] || wi == y || wi == z) continue; mv = w; }
                int m = idx[mv]; int V4[4] = {p, m, y, z};
                std::string oo = ", \"jobo\": {\"pmyz\": ["; char b0[64]; snprintf(b0, sizeof b0, "%d, %d, %d, %d], \"cycles\": [", order[p], mv, order[y], order[z]); oo += b0; bool f1 = true;
                for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
                    oo += f1 ? "[" : ", ["; f1 = false; bool f2 = true; int pos = 0;
                    for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd);
                        unkey(ALL[x], c); masks(c, cm); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = c[link_[t]]; int al = lc[j], A = lc[(j + 3) % 5];
                        u64 K = flood(1ULL << link_[(j + 2) % 5], cm[al] | cm[A]); int pairmask = 0, compmask = 0;
                        for (int i = 0; i < 4; i++) { if (c[V4[i]] == al || c[V4[i]] == A) pairmask |= 1 << i; if (K >> V4[i] & 1) compmask |= 1 << i; }
                        int csz = __builtin_popcountll(K);
                        int cc[64]; unkey(ALL[pi[x]], cc); u64 cm2[4]; masks(cc, cm2); u64 Ky = flood(1ULL << y, cm2[cc[y]] | cm2[cc[z]]); bool yz = Ky >> z & 1;
                        int sy = __builtin_popcountll(Ky), sz = __builtin_popcountll(flood(1ULL << z, cm2[cc[y]] | cm2[cc[z]]));
                        u64 K0 = flood(1ULL << y, cm[c[y]] | cm[c[z]]); bool yz0 = K0 >> z & 1;
                        char b[160]; snprintf(b, sizeof b, "%s[%d, %d, %d, %d, %d, %d, %d, %d, %d, %d]", f2 ? "" : ", ", pos, ty, km, pairmask, compmask, csz, yz0 ? 1 : 0, yz ? 1 : 0, sy, sz); oo += b; f2 = false; pos++; }
                    oo += "]"; }
                oo += "]}"; jobe += oo; } }
        if (JOBN) {   // Job N (NightF6Flow 2.1): at R3@k in {3,4} on Gamma-cycles: p = x_{j+k}, y = w_{j+k-1}, z = w_{j+k}, m = p's third outer neighbour
            std::string nn = ", \"jobn\": ["; bool f1 = true;
            for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
                nn += f1 ? "[" : ", ["; f1 = false; bool f2 = true; int pos = 0;
                for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); pos++;
                    if (ty != 3 || !(km == 8 || km == 16)) continue; int k = km == 8 ? 3 : 4;
                    int p = link_[(j + k) % 5], y = widx[(j + k + 4) % 5], z = widx[(j + k) % 5];
                    int pv = order[p]; int mv = -1, cntm = 0;
                    for (int w : rot[pv]) { if (w == hole) continue; int wi = idx[w]; if (wi == link_[(j + k + 1) % 5] || wi == link_[(j + k + 4) % 5] || wi == y || wi == z) continue; mv = w; cntm++; }
                    int m = idx[mv];
                    unkey(ALL[x], c); masks(c, cm);
                    bool lockless = (kd == 1 && !l1 && !l2);
                    u64 Kyz = flood(1ULL << y, cm[c[y]] | cm[c[z]]); bool yz = Kyz >> z & 1;
                    // bridge test of edge pm in G[H], H = {v} + vertices coloured c(p) or c(m)
                    u64 M = cm[c[p]] | cm[c[m]]; u64 seen = 1ULL << p; bool vseen = false; std::vector<int> st{p}; bool reached = false;
                    while (!st.empty() && !reached) { int u = st.back(); st.pop_back(); u64 nb = adjm[u] & M & ~seen; if (u == p) nb &= ~(1ULL << m);
                        if ((linkmask >> u & 1) && !vseen) { vseen = true; for (int t = 0; t < 5; t++) { int lv = link_[t]; if ((M >> lv & 1) && !(seen >> lv & 1) && !(u == p && lv == m)) { seen |= 1ULL << lv; st.push_back(lv); if (lv == m) reached = true; } } }
                        while (nb) { int w = __builtin_ctzll(nb); nb &= nb - 1; seen |= 1ULL << w; st.push_back(w); if (w == m) reached = true; } }
                    bool bridge = !reached;
                    int cp = __builtin_popcountll(flood(1ULL << p, M)), cy = __builtin_popcountll(Kyz), cz = __builtin_popcountll(flood(1ULL << z, cm[c[y]] | cm[c[z]]));
                    char b[256]; snprintf(b, sizeof b, "%s[%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d]", f2 ? "" : ", ", pos - 1, k, lockless ? 1 : 0, yz ? 1 : 0, bridge ? 1 : 0, pv, mv, order[y], order[z], cntm, cp, cy, cz, (int)(sg == x));
                    nn += b; f2 = false; }
                nn += "]"; }
            nn += "]"; jobe += nn; }
        if (JOBM) {   // Job M: Gamma-cycles as ordered state sequences [type, kmask, exit, f]; exit L lockless, 1 Lock1-only, 2 Lock2-only, X fixed point, D other DL, F filled
            std::string mm = ", \"jobm\": ["; bool f1 = true;
            for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
                mm += f1 ? "[" : ", ["; f1 = false; bool f2 = true;
                for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); char ex = '-'; long long f = -1;
                    if (ty == 3) { if (kd == 1 && !l1 && !l2) { ex = 'L'; long long y = pi[sg]; f = 0; while (kind[y] == 0) { f++; y = pi[y]; } }
                        else if (kd == 1) ex = l1 ? '1' : '2'; else if (kd == 2) ex = (sg == x) ? 'X' : 'D'; else ex = 'F'; }
                    char b[48]; snprintf(b, sizeof b, "%s[%d, %d, \"%c\", %lld]", f2 ? "" : ", ", ty, km, ex, f); mm += b; f2 = false; }
                mm += "]"; }
            mm += "]"; jobe += mm; }
        if (JOBK) {   // Job K: Lemma R per target cycle; sigma-chain from positive cycles without lockless exits
            std::map<int, std::pair<long long, long long>> hit;   // target cycle -> (#hits, sum of excursion contributions 1 - 3f)
            std::vector<std::set<int>> sadj(cycles.size());
            for (long long k = 0; k < S; k++) { if (kind[k] != 2) continue; if (!(kind[pi[k]] == 2 || kind[pinv[k]] == 2)) continue;
                int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd); if (cyc[sg] != cyc[k]) { sadj[cyc[k]].insert(cyc[sg]); sadj[cyc[sg]].insert(cyc[k]); } }
            std::string kk = ", \"jobk_pos\": ["; bool fk2 = true;
            for (size_t ci = 0; ci < cycles.size(); ci++) { if (wind[ci] <= 0) continue; long long a = 0; bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) all = false;
                for (int32_t x : cycles[ci]) { if (kind[x] != 2) continue; int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); if (ty != 3) continue;
                    if (kd == 1 && !l1 && !l2) { a++; long long y = pi[sg], f = 0; while (kind[y] == 0) { f++; y = pi[y]; } auto &h = hit[cyc[sg]]; h.first++; h.second += 1 - 3 * f; } }
                // BFS over sigma-adjacency to the nearest cycle with w < 0
                std::map<int, int> dist; std::vector<int> q{(int)ci}; dist[ci] = 0; int found = -1, fw = 0; long long gsum = 0;
                for (size_t h = 0; h < q.size(); h++) { int z = q[h]; gsum += wind[z]; if (found < 0 && wind[z] < 0) { found = dist[z]; fw = wind[z]; } for (int y : sadj[z]) if (!dist.count(y)) { dist[y] = dist[z] + 1; q.push_back(y); } }
                char b6[300]; snprintf(b6, sizeof b6, "%s{\"gamma\": %s, \"L\": %zu, \"w\": %lld, \"a\": %lld, \"sigma_chain_to_negative\": %d, \"first_negative_w\": %d, \"group_ncycles\": %zu, \"group_sumw\": %lld}",
                    fk2 ? "" : ", ", all ? "true" : "false", cycles[ci].size(), wind[ci], a, found, fw, q.size(), gsum); kk += b6; fk2 = false; }
            kk += "], \"lemmaR\": ["; bool f3 = true; long long rbad = 0;
            for (auto &kv : hit) { long long rem = 5 * wind[kv.first] - kv.second.second; if (rem > 0) rbad++;
                char b7[200]; snprintf(b7, sizeof b7, "%s[%lld, %zu, %lld, %lld, %lld]", f3 ? "" : ", ", wind[kv.first], cycles[kv.first].size(), kv.second.first, kv.second.second, rem); kk += b7; f3 = false; }
            char b8[64]; snprintf(b8, sizeof b8, "], \"lemmaR_bad\": %lld", rbad); kk += b8; jobe += kk; }
        if (JOBG) {   // Job G (NightC1Gamma section 5): per Gamma-cycle exits of R3 states
            auto excursion = [&](long long x, long long &u, long long &f) {   // x unfilled: its unfilled run length u and the following filled run length f
                long long st = x, guard = 0; while (kind[pinv[st]] != 0 && guard < S) { st = pinv[st]; guard++; } if (guard >= S) { u = cycles[cyc[x]].size(); f = 0; return; }
                u = 0; long long y = st; while (kind[y] != 0) { u++; y = pi[y]; } f = 0; while (kind[y] == 0) { f++; y = pi[y]; } };
            std::string g = ", \"jobg\": ["; bool fg = true; std::map<int, int> target_owner; long long shared_targets = 0;
            for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all && !(JOBI && wind[ci] > 0)) continue;
                long long a = 0, b = 0, d = 0, credit = 0, s1bad = 0, s1n = 0; std::map<std::string, long long> h; std::set<int> tg;
                for (int32_t x : cycles[ci]) { if (kind[x] != 2) continue; int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); if (ty != 3) continue;
                    unkey(ALL[x], c); masks(c, cm); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = c[link_[t]];
                    int al = lc[j], mu = lc[(j + 1) % 5], A = lc[(j + 3) % 5], B = lc[(j + 4) % 5]; int m = link_[(j + 1) % 5];
                    bool crit3 = flood(1ULL << m, cm[mu] | cm[B]) >> widx[(j + 2) % 5] & 1, crit4 = flood(1ULL << m, cm[mu] | cm[A]) >> widx[(j + 4) % 5] & 1;
                    bool lockless = (kd == 1 && !l1 && !l2); char key[160];
                    if (km == 8 || km == 16) { s1n++; bool crit = km == 8 ? crit3 : crit4; bool other_ok = km == 8 ? (l1 && !l2) : (!l1 && l2); if (crit != lockless || (!lockless && !(kd == 1 && other_ok))) s1bad++; }
                    if (lockless) { a++; long long u, f; excursion(sg, u, f); credit += 3 * f - 1; tg.insert(cyc[sg]); snprintf(key, sizeof key, "lockless_k%d_u%lld_f%lld_wT%lld", km, u, f, wind[cyc[sg]]); h[key]++; }
                    else if (kd == 2) { d++; snprintf(key, sizeof key, "DL_k%d_fixed%d_same%d_type%d", km, sg == x ? 1 : 0, cyc[sg] == (int)ci ? 1 : 0, [&]{ int j2, t2, k2, a1, a2, a3; long long s2; frame(sg, j2, t2, k2, s2, a1, a2, a3); return t2; }()); h[key]++; }
                    else if (kd == 1) { b++; long long u, f; excursion(sg, u, f); tg.insert(cyc[sg]); snprintf(key, sizeof key, "onelock_k%d_L%d%d_u%lld_f%lld_wT%lld", km, l1, l2, u, f, wind[cyc[sg]]); h[key]++; }
                    else { snprintf(key, sizeof key, "filled_k%d", km); h[key]++; } }
                for (int t : tg) { auto it = target_owner.find(t); if (it != target_owner.end() && it->second != (int)ci) shared_targets++; else target_owner[t] = ci; }
                char b1[300]; snprintf(b1, sizeof b1, "%s{\"gamma\": %s, \"L\": %zu, \"w\": %lld, \"a\": %lld, \"b\": %lld, \"d\": %lld, \"G_credit\": %lld, \"G_ok\": %s, \"s1_checked\": %lld, \"s1_bad\": %lld, \"exits\": {",
                    fg ? "" : ", ", all ? "true" : "false", cycles[ci].size(), wind[ci], a, b, d, credit, credit >= (long long)cycles[ci].size() ? "true" : "false", s1n, s1bad); g += b1; fg = false;
                bool f2 = true; for (auto &kv : h) { char b2[200]; snprintf(b2, sizeof b2, "%s\"%s\": %lld", f2 ? "" : ", ", kv.first.c_str(), kv.second); g += b2; f2 = false; }
                g += "}}"; }
            char b3[64]; snprintf(b3, sizeof b3, "], \"jobg_shared_targets\": %lld", shared_targets); g += b3;
            if (!fg) jobe += g; }
        if (JOBE) {
        // Gamma-cycles
        jobe += ", \"gamma\": [";
        bool fg = true;
        for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
            long long ty_n[4] = {0, 0, 0, 0}; std::map<std::pair<int, int>, long long> tk; std::map<std::string, long long> fk; long long r3 = 0, r3ok = 0, r3same = 0; std::string ff;
            for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); ty_n[ty]++; tk[{ty, km}]++;
                if (ty == 3) { r3++; bool ok = (kd == 1 && !l1 && !l2); if (ok) r3ok++; if (cyc[sg] == (int)ci) r3same++;
                    if (!ok) { char kk[64]; snprintf(kk, sizeof kk, "k%d_kind%d_l1%d_l2%d_same%d_wsig%lld", km, kd, l1, l2, cyc[sg] == (int)ci ? 1 : 0, wind[cyc[sg]]); fk[kk]++; }
                    if (!ok && ff.empty()) { char b6[256]; snprintf(b6, sizeof b6, "{\"state_index\": %d, \"kmask\": %d, \"sigma_kind\": %d, \"sigma_lock1\": %d, \"sigma_lock2\": %d, \"sigma_same_cycle\": %s, \"sigma_cycle_w\": %lld}", x, km, kd, l1, l2, cyc[sg] == (int)ci ? "true" : "false", wind[cyc[sg]]); ff = b6; } } }
            char b7[512]; snprintf(b7, sizeof b7, "%s{\"L\": %zu, \"w\": %lld, \"R1\": %lld, \"R2\": %lld, \"R3\": %lld, \"other\": %lld, \"r3_sigma_lockless\": %lld, \"r3_sigma_same_cycle\": %lld, \"first_r3_fail\": %s, \"type_kmask\": [",
                fg ? "" : ", ", cycles[ci].size(), wind[ci], ty_n[1], ty_n[2], ty_n[3], ty_n[0], r3ok, r3same, ff.empty() ? "null" : ff.c_str()); jobe += b7; fg = false;
            bool f8 = true; for (auto &kv : tk) { char b8[64]; snprintf(b8, sizeof b8, "%s[%d, %d, %lld]", f8 ? "" : ", ", kv.first.first, kv.first.second, kv.second); jobe += b8; f8 = false; }
            jobe += "], \"r3_fail_kinds\": {"; bool f9 = true; for (auto &kv : fk) { char b9[128]; snprintf(b9, sizeof b9, "%s\"%s\": %lld", f9 ? "" : ", ", kv.first.c_str(), kv.second); jobe += b9; f9 = false; }
            jobe += "}}"; }
        jobe += "]";
        }
    }
    // ---- output
    std::string out = "{\"kind\": \"hole\", \"name\": \"" + name + "\""; char buf[1024];
    snprintf(buf, sizeof buf, ", \"n\": %d, \"hole\": %d, \"linkdeg\": [%zu, %zu, %zu, %zu, %zu], \"vrole\": %d, \"dist_config\": %d, \"states\": %lld, \"F\": %lld, \"U\": %lld, \"nDL\": %lld, \"ncyc\": %zu, \"npos\": %zu, \"sumw\": %lld, \"minw\": %lld, \"maxw\": %lld",
             n, hole, rot[L[0]].size(), rot[L[1]].size(), rot[L[2]].size(), rot[L[3]].size(), rot[L[4]].size(), VROLE[hole], dist_config(n, rot, hole), S, F, S - F, nDL, cycles.size(), pos.size(), [&]{ long long t = 0; for (long long w : wind) t += w; return t; }(), *std::min_element(wind.begin(), wind.end()), *std::max_element(wind.begin(), wind.end()));
    out += buf;
    if (FULL) { snprintf(buf, sizeof buf, ", \"nclasses\": %lld, \"cls_bad\": %lld, \"cyc_split\": %lld, \"f5_bad\": %lld, \"clsig\": [", nclasses, cls_bad, cyc_split, f5_bad); out += buf; out += clsig + "]"; }
    out += ", \"hist\": ["; bool first = true; for (auto &kv : hist) { snprintf(buf, sizeof buf, "%s[%lld, %lld, %lld]", first ? "" : ", ", kv.first.first, kv.first.second, kv.second); out += buf; first = false; } out += "]";
    if (!pos.empty()) {
        out += ", \"pos\": [";
        for (size_t i = 0; i < pos.size(); i++) { int z = pos[i]; LB &lb = lbs[z];
            std::map<long long, int> nbw; long long minnb = 0; for (auto &kv : exits[z]) { nbw[wind[kv.first]]++; minnb = std::min(minnb, wind[kv.first]); }
            snprintf(buf, sizeof buf, "%s{\"w\": %lld, \"L\": %zu, \"nDL\": %lld, \"exits_any\": %lld, \"exits_to_neg_any\": %lld, \"exits_DL\": %lld, \"exits_lockbreaking\": %lld, \"exits_to_neg\": %lld, \"exits_to_neg_lockbreaking\": %lld, \"exits_to_neg_nonlb\": %lld, \"minnb\": %lld, \"comp\": %d, \"nbw\": [",
                     i ? ", " : "", wind[z], cycles[z].size(), lb.nDL, lb.exits_any, lb.to_neg_any, lb.exits_DL, lb.exits_lb, lb.to_neg, lb.to_neg_lb, lb.to_neg - lb.to_neg_lb, minnb, comp[z]); out += buf;
            bool f1 = true; for (auto &kv : nbw) { snprintf(buf, sizeof buf, "%s[%lld, %d]", f1 ? "" : ", ", kv.first, kv.second); out += buf; f1 = false; }
            out += "]";
            if (FULL) { int r = find(cycles[z][0]); long long cs = 0, cf = 0, cu = 0; long long sw = 0; std::set<int> cc; // class stats (computed per positive cycle; cheap at these sizes)
                for (long long k = 0; k < S; k++) if (find(k) == r) { cs++; if (kind[k] == 0) cf++; else cu++; cc.insert(cyc[k]); }
                for (int ci : cc) sw += wind[ci];
                bool thmW = (3 * cf - cu == -5 * sw);
                if (!thmW) fprintf(stderr, "THEOREM W FAILS %s hole %d\n", name.c_str(), hole);
                snprintf(buf, sizeof buf, ", \"class\": {\"root\": %d, \"states\": %lld, \"F\": %lld, \"U\": %lld, \"ncyc\": %zu, \"sumw\": %lld, \"thmW\": %s}", r, cs, cf, cu, cc.size(), sw, thmW ? "true" : "false"); out += buf; }
            out += "}"; }
        out += "], \"transport\": [";
        std::set<int> comps; for (int z : pos) comps.insert(comp[z]); bool fc = true;
        const char *vn[5] = {"a_DL_allpairs", "b_DL_otherpair", "c_anystate", "d_DL_lockbreaking", "e_DL_otherpair_lockbreaking"};
        for (int cid : comps) { std::vector<int> P; for (int z : pos) if (comp[z] == cid) P.push_back(z);
            out += fc ? "{" : ", {"; fc = false; out += "\"posW\": ["; for (size_t i = 0; i < P.size(); i++) { snprintf(buf, sizeof buf, "%s%lld", i ? ", " : "", wind[P[i]]); out += buf; } out += "]";
            for (int v = 0; v < 5; v++) { std::map<int, std::set<int>> E = edge_set(v); Flow f = flow_report(P, Wm, E); out += std::string(", \"") + vn[v] + "\": " + flow_json(f); }
            out += "}"; }
        out += "]";
    }
    out += jobe;
    out += "}\n"; fputs(out.c_str(), stdout); fflush(stdout);
}
// per-vertex role bits: 1 diamond centre, 2 diamond tip, 4 2.122 degree-5 centre, 8 2.122 degree-6 centre, 16 2.122 tip
static void config_flags(int n, const std::vector<std::vector<int>> &rot, int &diamonds, int &c2122) {
    diamonds = c2122 = 0; ADJ55 = 0; VROLE.assign(n, 0); std::vector<std::set<int>> adj(n); for (int v = 0; v < n; v++) for (int w : rot[v]) adj[v].insert(w);
    for (int a = 0; a < n; a++) { int da = rot[a].size(); for (size_t p = 0; p < rot[a].size(); p++) { int b = rot[a][p]; if (b < a) continue; int db = rot[b].size();
        if (da == 5 && db == 5) ADJ55++;
        int c = rot[a][(p + 1) % da], d = rot[a][(p + da - 1) % da]; if (adj[c].count(d)) continue; if ((int)rot[c].size() != 5 || (int)rot[d].size() != 5) continue;
        if (da == 5 && db == 5) { diamonds++; VROLE[a] |= 1; VROLE[b] |= 1; VROLE[c] |= 2; VROLE[d] |= 2; }
        else if ((da == 5 && db == 6) || (da == 6 && db == 5)) { c2122++; VROLE[da == 5 ? a : b] |= 4; VROLE[da == 6 ? a : b] |= 8; VROLE[c] |= 16; VROLE[d] |= 16; } } }
}
static int dist_config(int n, const std::vector<std::vector<int>> &rot, int v) {
    std::vector<int> d(n, -1); d[v] = 0; std::vector<int> q{v};
    for (size_t h = 0; h < q.size(); h++) { int x = q[h]; if (VROLE[x]) return d[x]; for (int w : rot[x]) if (d[w] < 0) { d[w] = d[x] + 1; q.push_back(w); } }
    return -1;
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: picyc FILE [--full] [--mirror] [--cap M] [--holes h,h]\n"); return 2; }
    std::set<int> holesel; for (int i = 2; i < argc; i++) { std::string a = argv[i]; if (a == "--full") FULL = true; else if (a == "--mirror") MIRROR = true; else if (a == "--cfree") CFREE = true; else if (a == "--adj5") ADJ5 = true; else if (a == "--graphonly") GRAPHONLY = true; else if (a == "--jobe") JOBE = true; else if (a == "--sigc") SIGC = true; else if (a == "--jobg") JOBG = true; else if (a == "--jobh") JOBH = true; else if (a == "--jobi") { JOBI = true; JOBG = true; } else if (a == "--jobak") { JOBAK = true; JOBI = true; JOBG = true; } else if (a == "--jobab") { JOBAB = true; JOBI = true; JOBG = true; } else if (a == "--jobz") { JOBS = true; JOBG = true; ALLTYPES = true; } else if (a == "--jobbt") { JOBBT = true; JOBG = true; } else if (a == "--nocls") NOCLS = true; else if (a == "--jobbq") { JOBBQ = true; JOBG = true; } else if (a == "--jobbp") { JOBBP = true; JOBG = true; } else if (a == "--jobbo") { JOBBO = true; JOBG = true; } else if (a == "--jobbl") { JOBBL = true; JOBG = true; } else if (a == "--jobbk") { JOBBK = true; JOBG = true; } else if (a == "--jobbj") { JOBBJ = true; JOBG = true; } else if (a == "--jobbgh") { JOBBGH = true; JOBG = true; } else if (a == "--jobbc") { JOBBC = true; JOBG = true; } else if (a == "--jobbb") { JOBBB = true; JOBI = true; JOBG = true; } else if (a == "--jobx") { JOBX = true; JOBI = true; JOBG = true; } else if (a == "--jobs") { JOBS = true; JOBI = true; JOBG = true; } else if (a == "--jobq") { JOBQ = true; JOBI = true; JOBG = true; } else if (a == "--jobp") { JOBP = true; JOBI = true; JOBG = true; } else if (a == "--jobo") { JOBO = true; JOBI = true; JOBG = true; } else if (a == "--jobn") { JOBN = true; JOBI = true; JOBG = true; } else if (a == "--jobm") { JOBM = true; JOBI = true; JOBG = true; } else if (a == "--jobk") { JOBK = true; JOBI = true; JOBG = true; } else if (a == "--cap") capStates = atoll(argv[++i]);
        else if (a == "--holes") { std::string s = argv[++i]; size_t p = 0; while (p < s.size()) { size_t q = s.find(',', p); if (q == std::string::npos) q = s.size(); holesel.insert(atoi(s.substr(p, q - p).c_str())); p = q + 1; } } }
    FILE *fp = fopen(argv[1], "r"); if (!fp) { fprintf(stderr, "cannot open\n"); return 2; }
    char *line = nullptr; size_t cap = 0; ssize_t len;
    while ((len = getline(&line, &cap, fp)) > 0) {
        std::string s(line); while (!s.empty() && (s.back() == '\n' || s.back() == '\r')) s.pop_back(); if (s.empty()) continue;
        size_t p1 = s.find(' '), p2 = s.find(' ', p1 + 1); std::string name = s.substr(0, p1); int n = atoi(s.substr(p1 + 1, p2 - p1 - 1).c_str());
        std::vector<std::vector<int>> rot; { std::string r = s.substr(p2 + 1); size_t p = 0; while (p <= r.size()) { size_t q = r.find(';', p); if (q == std::string::npos) q = r.size(); std::string seg = r.substr(p, q - p); std::vector<int> v; size_t a = 0;
            while (a < seg.size()) { size_t b = seg.find(',', a); if (b == std::string::npos) b = seg.size(); v.push_back(atoi(seg.substr(a, b - a).c_str())); a = b + 1; } rot.push_back(v); p = q + 1; } }
        if ((int)rot.size() != n) { fprintf(stderr, "bad line %s\n", name.c_str()); return 2; }
        if (MIRROR) for (auto &v : rot) std::reverse(v.begin(), v.end());
        int dia, c2; config_flags(n, rot, dia, c2); int d5 = 0; for (int v = 0; v < n; v++) if (rot[v].size() == 5) d5++;
        bool cf = (dia == 0 && c2 == 0); if (CFREE && !cf) continue; if (ADJ5 && ADJ55 == 0) continue;
        std::string ld; for (int v = 0; v < n; v++) if (rot[v].size() == 5) { char b2[64]; snprintf(b2, sizeof b2, "%s[%zu,%zu,%zu,%zu,%zu]", ld.empty() ? "" : ",", rot[rot[v][0]].size(), rot[rot[v][1]].size(), rot[rot[v][2]].size(), rot[rot[v][3]].size(), rot[rot[v][4]].size()); ld += b2; }
        printf("{\"kind\": \"graph\", \"name\": \"%s\", \"n\": %d, \"deg5\": %d, \"adj55\": %d, \"diamonds\": %d, \"c2122\": %d, \"cfree\": %s, \"linkdegs\": [%s]}\n", name.c_str(), n, d5, ADJ55, dia, c2, cf ? "true" : "false", ld.c_str()); fflush(stdout);
        if (GRAPHONLY) continue;
        for (int v = 0; v < n; v++) if (rot[v].size() == 5 && (holesel.empty() || holesel.count(v))) analyse_hole(name, n, rot, v);
    }
    return 0;
}
