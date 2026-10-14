// cfast.cpp -- Studio Job 15 (14 Oct 2026, exploratory): C-reducibility search on top of the dfast closure.
//
// D-closure: exactly dfast.cpp / DCheck.run (ring colourings up to renaming, level-synchronous Kempe closure over
// non-crossing matchings).  bad = ring colouring classes NOT reached.
// C-reducibility with a contraction X (RSST): every ring colouring that extends to the configuration with the edges of X
// contracted must be reached (good).  Contracting an edge turns its constraint "different colours" into "same colour";
// a ring-interior edge forces the interior vertex to the ring vertex's colour; two ring vertices joined through
// contracted edges must have equal colours.  So: X works iff no bad class extends under the contracted constraints.
// Admissibility checked here (local only):
//   |X| <= KMAX (default 4); every edge of X has an interior end; no loop: no edge of the configuration (ring edges
//   included, edges in X excluded) joins two vertices that X identifies.
// Also Gonthier's valid_contract conditions (fourcolor theories/proof/coloring.v): sparse (no triangle with two
// contracted edges), size 1..4, and for size 4 a triad (an interior vertex adjacent to >= 3 endpoints of X, not to all).
// NOT checked here: the global minimal-counterexample conditions on the contracted map (no new separating triangle /
// short cycle in G'); RSST verify those separately.  A hit is a candidate, not a certified C-reduction.
// Input: WheelMain lines `name r m ringAdj intAdj` (stdin or file).  Modes:
//   cfast FILE --search [--kmax 4] [--limit N]   enumerate admissible X, report every working X (up to N) and the best leftover
//   cfast FILE --fixed "R0-I8,R2-I8"            test one X (R<i> ring position, I<j> interior index)
// Build: c++ -O2 -std=c++17 -o cfast cfast.cpp
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <unordered_map>
#include <sstream>
#include <algorithm>
#include <functional>
#include <chrono>
#include <random>
#include <set>
#include <array>
typedef uint64_t u64;
static int R, Mi;
static std::vector<std::vector<int>> ringAdj, intAdj;
static inline int col(u64 k, int i) { return (int)((k >> (2 * i)) & 3); }
static u64 canonc(u64 k) { int mp[4] = {-1, -1, -1, -1}, nx = 0; u64 out = 0; for (int i = 0; i < R; i++) { int c = col(k, i); if (mp[c] < 0) mp[c] = nx++; out |= (u64)mp[c] << (2 * i); } return out; }
static std::vector<u64> ringColourings(int r) {
    std::vector<std::pair<u64, int>> cur = {{0, 1}};
    for (int i = 1; i < r; i++) { std::vector<std::pair<u64, int>> nx;
        for (auto [k, used] : cur) for (int c = 0; c < std::min(4, used + 1); c++) if (c != col(k, i - 1) && (i + 1 != r || c != col(k, 0))) nx.push_back({k | ((u64)c << (2 * i)), c == used ? used + 1 : used});
        cur.swap(nx); }
    std::vector<u64> out; for (auto &p : cur) out.push_back(p.first); return out;
}
// ---------- extension with constraints: vertices 0..R-1 ring, R..R+Mi-1 interior; eq edges (contracted) and ne edges
struct Cons { std::vector<std::vector<std::pair<int, bool>>> back; };   // for interior a: (earlier vertex, mustEqual)
static bool extC(u64 k, const std::vector<std::vector<std::pair<int, bool>>> &cons, const std::vector<std::pair<int, int>> &ringEq, std::vector<int> &cols) {
    for (auto &e : ringEq) if (col(k, e.first) != col(k, e.second)) return false;
    std::function<bool(int)> rec = [&](int a) -> bool {
        if (a == Mi) return true;
        for (int x = 0; x < 4; x++) {
            bool ok = true;
            for (auto [v, eq] : cons[a]) { int cv = v < R ? col(k, v) : cols[v - R]; if (eq ? cv != x : cv == x) { ok = false; break; } }
            if (!ok) continue;
            cols[a] = x; if (rec(a + 1)) return true;
        }
        return false;
    };
    return rec(0);
}
// ---------- the D closure (as dfast.cpp)
static std::vector<std::vector<std::vector<int>>> matchTable;
static void ncm(std::vector<int> pts, std::vector<std::pair<int, int>> &cur, std::vector<std::vector<std::pair<int, int>>> &out) {
    if (pts.empty()) { out.push_back(cur); return; }
    int a = pts[0];
    for (size_t j = 1; j < pts.size(); j += 2) {
        std::vector<int> L(pts.begin() + 1, pts.begin() + j), Rr(pts.begin() + j + 1, pts.end());
        cur.push_back({a, pts[j]});
        std::vector<std::vector<std::pair<int, int>>> o1, o2; std::vector<std::pair<int, int>> c1, c2; ncm(L, c1, o1); ncm(Rr, c2, o2);
        for (auto &m1 : o1) for (auto &m2 : o2) { auto m = cur; m.insert(m.end(), m1.begin(), m1.end()); m.insert(m.end(), m2.begin(), m2.end()); out.push_back(m); }
        cur.pop_back();
    }
}
static std::vector<int> arcRegions(int n, const std::vector<std::pair<int, int>> &Mt) {
    std::vector<int> lab(n); for (int i = 0; i < n; i++) lab[i] = i;
    for (auto [s, t] : Mt) { int i = std::min(s, t), j = std::max(s, t); int pr[2][2] = {{(i + n - 1) % n, j}, {i, (j + n - 1) % n}};
        for (auto &xy : pr) { int lx = lab[xy[0]], ly = lab[xy[1]]; for (int &l : lab) if (l == ly) l = lx; } }
    std::vector<int> mp(n, -1), out; int nx = 0; for (int j = 0; j < n; j++) { int l = lab[j]; if (mp[l] < 0) mp[l] = nx++; out.push_back(mp[l]); }
    return out;
}
int main(int argc, char **argv) {
    matchTable.resize(10);
    for (int p = 0; p <= 9; p++) { std::vector<int> pts(2 * p); for (int i = 0; i < 2 * p; i++) pts[i] = i;
        std::vector<std::vector<std::pair<int, int>>> ms; std::vector<std::pair<int, int>> cur; ncm(pts, cur, ms); for (auto &m : ms) matchTable[p].push_back(arcRegions(2 * p, m)); }
    std::string fixed; bool search = false, gonthier = true; int KMAX = 4; long LIMIT = 50;
    for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "--search")) search = true; else if (!strcmp(argv[i], "--fixed")) fixed = argv[++i];
        else if (!strcmp(argv[i], "--kmax")) KMAX = atoi(argv[++i]); else if (!strcmp(argv[i], "--nogonthier")) gonthier = false; else if (!strcmp(argv[i], "--limit")) LIMIT = atol(argv[++i]); }
    FILE *in = fopen(argv[1], "r"); char buf[1 << 16];
    while (fgets(buf, sizeof buf, in)) {
        std::istringstream ss(buf); std::string name, ra, ia; int r, m; if (!(ss >> name >> r >> m >> ra >> ia)) continue;
        auto parse = [](const std::string &s) { std::vector<std::vector<int>> out; std::stringstream q(s); std::string t;
            while (std::getline(q, t, ';')) { std::vector<int> v; if (t != "-") { std::stringstream q2(t); std::string a; while (std::getline(q2, a, ',')) v.push_back(atoi(a.c_str())); } out.push_back(v); } return out; };
        R = r; Mi = m; ringAdj = parse(ra); intAdj = parse(ia);
        auto t0 = std::chrono::steady_clock::now();
        // ---- D closure (dfast)
        std::vector<u64> ks = ringColourings(r); size_t N = ks.size();
        std::unordered_map<u64, int> index; index.reserve(N * 2); for (size_t i = 0; i < N; i++) index[ks[i]] = i;
        // plain extension constraints (no contraction)
        std::vector<std::vector<std::pair<int, bool>>> cons0(m);
        for (int a = 0; a < m; a++) { for (int t : ringAdj[a]) cons0[a].push_back({t, false}); for (int b : intAdj[a]) if (b < a) cons0[a].push_back({R + b, false}); }
        std::vector<char> good(N); std::vector<int> cols(m); size_t ext = 0;
        for (size_t i = 0; i < N; i++) { good[i] = extC(ks[i], cons0, {}, cols); ext += good[i]; }
        size_t reached = ext; int depth = 0; const int DEAD = 1 << 30;
        std::vector<int> prog(3 * N, 0); std::vector<std::vector<int>> cache(3 * N); std::vector<char> cached(3 * N, 0);
        for (size_t level = 0; level <= N; level++) {
            std::vector<int> nw;
            for (size_t i = 0; i < N; i++) {
                if (good[i]) continue; u64 k = ks[i]; bool done = false;
                for (int th = 1; th <= 3 && !done; th++) {
                    int slot = 3 * i + th - 1; int pi = prog[slot]; if (pi == DEAD) continue;
                    int T[32], n = 0; for (int v = 0; v < r; v++) { int x = col(k, v) ^ col(k, (v + 1) % r); if (x != 0 && x != th) T[n++] = v; }
                    if (n == 0) { prog[slot] = DEAD; continue; }
                    std::vector<int> arcOf(r); for (int v = 0; v < r; v++) { int c = 0; for (int q = 0; q < n; q++) if (T[q] < v) c++; arcOf[v] = (c + n - 1) % n; }
                    auto &mats = matchTable[n / 2]; int ptr = pi; bool stuck = false;
                    while (ptr < (int)mats.size() && !stuck) {
                        bool sat = false;
                        if (cached[slot]) { for (int j : cache[slot]) if (good[j]) { sat = true; break; } }
                        else { auto &lab = mats[ptr]; int P = n / 2; u64 rm[16] = {0};
                            for (int v = 0; v < r; v++) { int g = lab[arcOf[v]]; rm[g] |= (u64)th << (2 * v); }
                            std::vector<int> reach;
                            for (int s = 1; s < (1 << P); s++) { u64 k2 = k; for (int b = 0; b < P; b++) if (s >> b & 1) k2 ^= rm[b + 1];
                                auto it = index.find(canonc(k2)); if (it != index.end()) { if (good[it->second]) { sat = true; break; } reach.push_back(it->second); } }
                            if (!sat) { std::sort(reach.begin(), reach.end()); reach.erase(std::unique(reach.begin(), reach.end()), reach.end()); cache[slot] = reach; cached[slot] = 1; } }
                        if (sat) { ptr++; cached[slot] = 0; cache[slot].clear(); cache[slot].shrink_to_fit(); } else stuck = true;
                    }
                    prog[slot] = ptr; if (ptr == (int)mats.size()) done = true;
                }
                if (done) nw.push_back(i);
            }
            if (nw.empty()) break; for (int i : nw) good[i] = 1; reached += nw.size(); depth++;
        }
        std::vector<u64> bad; for (size_t i = 0; i < N; i++) if (!good[i]) bad.push_back(ks[i]);
        { std::mt19937 g(7); std::shuffle(bad.begin(), bad.end(), g); }
        double sD = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
        printf("%s r=%d m=%d classes=%zu ext=%zu reached=%zu bad=%zu D=%s depth=%d (%.1fs)\n", name.c_str(), r, m, N, ext, reached, bad.size(), bad.empty() ? "true" : "false", depth, sD);
        if (bad.empty()) { fflush(stdout); continue; }
        // ---- configuration edges: vertices 0..R-1 ring, R+a interior a
        std::vector<std::pair<int, int>> E, ringE;
        for (int a = 0; a < m; a++) { for (int t : ringAdj[a]) E.push_back({t, R + a}); for (int b : intAdj[a]) if (b > a) E.push_back({R + a, R + b}); }
        for (int t = 0; t < R; t++) ringE.push_back({t, (t + 1) % R});
        // adjacency (configuration + ring edges), edge ids, triangles (3-cycles = faces in a configuration with no separating triangle)
        std::vector<std::set<int>> nbr(R + m);
        for (auto &e : E) { nbr[e.first].insert(e.second); nbr[e.second].insert(e.first); }
        for (auto &e : ringE) { nbr[e.first].insert(e.second); nbr[e.second].insert(e.first); }
        std::unordered_map<int, int> eid; for (size_t e = 0; e < E.size(); e++) eid[std::min(E[e].first, E[e].second) * 1000 + std::max(E[e].first, E[e].second)] = e;
        std::vector<std::array<int, 3>> tris;
        for (int u = 0; u < R + m; u++) for (int v : nbr[u]) if (v > u) for (int w : nbr[v]) if (w > v && nbr[u].count(w)) tris.push_back({u, v, w});
        auto edgeName = [&](std::pair<int, int> e) { auto nm = [&](int v) { return v < R ? "R" + std::to_string(v) : "I" + std::to_string(v - R); }; return nm(e.first) + "-" + nm(e.second); };
        // test one X: returns number of bad classes that extend (leftover), or -1 if inadmissible; stops after `stopAt` hits
        int lastTriad = -1;                                          // triad vertex of the last admissible |X| = 4 test
        auto testX = [&](const std::vector<int> &X, long stopAt) -> long {
            lastTriad = -1;
            int V = R + m; std::vector<int> par(V); for (int i = 0; i < V; i++) par[i] = i;
            std::function<int(int)> f = [&](int x) { return par[x] == x ? x : par[x] = f(par[x]); };
            std::vector<char> inX(E.size(), 0); for (int e : X) { inX[e] = 1; par[f(E[e].first)] = f(E[e].second); }
            for (size_t e = 0; e < E.size(); e++) if (!inX[e] && f(E[e].first) == f(E[e].second)) return -1;     // loop
            for (auto &e : ringE) if (f(e.first) == f(e.second)) return -1;                                    // loop on the ring
            // Gonthier valid_contract (fourcolor coloring.v), in triangulation terms:
            //  sparse: no triangle of the configuration contains two contracted edges
            if (gonthier) for (auto &T : tris) { int c = 0; for (int q = 0; q < 3; q++) { int u = T[q], v = T[(q + 1) % 3]; auto it = eid.find(std::min(u, v) * 1000 + std::max(u, v)); if (it != eid.end() && inX[it->second]) c++; } if (c >= 2) return -1; }
            //  triad (|X| = 4): an interior vertex x adjacent to >= 3 endpoints of X, and not every endpoint of X adjacent to x
            if (gonthier && X.size() == 4) {
                std::vector<char> endp(V, 0); for (int e : X) { endp[E[e].first] = 1; endp[E[e].second] = 1; }
                bool triad = false;
                for (int a = 0; a < m && !triad; a++) {
                    int x = R + a, cnt = 0; bool all = true;
                    for (int w = 0; w < V; w++) { if (!endp[w]) continue; bool adj = nbr[x].count(w) > 0; if (adj) cnt++; else all = false; }
                    if (cnt > 2 && !all) { triad = true; lastTriad = a; }
                }
                if (!triad) return -1;
            }
            // constraints
            std::vector<std::vector<std::pair<int, bool>>> cons(m);
            for (size_t e = 0; e < E.size(); e++) {
                int u = E[e].first, v = E[e].second, a = v - R;              // v is interior; u ring or interior with u < v
                if (u >= R) { int b = u - R; int hi = std::max(a, b), lo = std::min(a, b); cons[hi].push_back({R + lo, (bool)inX[e]}); }
                else cons[a].push_back({u, (bool)inX[e]});
            }
            std::vector<std::pair<int, int>> ringEq;                         // ring vertices identified through X
            for (int s = 0; s < R; s++) for (int t = s + 1; t < R; t++) if (f(s) == f(t)) ringEq.push_back({s, t});
            long hits = 0; std::vector<int> cc(m);
            for (u64 k : bad) if (extC(k, cons, ringEq, cc)) { if (++hits >= stopAt) return hits; }
            return hits;
        };
        if (!fixed.empty()) {
            std::vector<int> X; std::stringstream q(fixed); std::string t;
            while (std::getline(q, t, ',')) { for (size_t e = 0; e < E.size(); e++) if (edgeName(E[e]) == t) X.push_back(e); }
            long h = testX(X, 1L << 60);
            printf("  fixed X={%s} (%zu edges): %s, leftover bad classes extending after contraction = %ld\n", fixed.c_str(), X.size(), h < 0 ? "INADMISSIBLE" : h == 0 ? "C-REDUCIBLE" : "fails", h);
        }
        if (search) {
            long tested = 0, inadm = 0, works = 0; long best = 1L << 60; std::vector<int> bestX; std::vector<int> X;
            std::function<void(size_t)> rec = [&](size_t start) {
                if (!X.empty()) {
                    long h = testX(X, best == (1L << 60) ? (1L << 60) : best + 1);
                    if (h < 0) inadm++;                // a superset can be admissible again (contracting the loop edge too)
                    else {
                    tested++;
                    if (h < best) { best = h; bestX = X; }
                    if (h == 0) { works++; if (works <= LIMIT) { std::string s; int ringTouch = 0; for (int e : X) { s += (s.empty() ? "" : ",") + edgeName(E[e]); ringTouch += E[e].first < R; }
                        printf("  C-REDUCIBLE with X={%s} size=%zu ringEdges=%d triad=%s\n", s.c_str(), X.size(), ringTouch, lastTriad >= 0 ? ("I" + std::to_string(lastTriad)).c_str() : "-"); fflush(stdout); } }
                    }
                }
                if ((int)X.size() == KMAX) return;
                for (size_t e = start; e < E.size(); e++) { X.push_back(e); rec(e + 1); X.pop_back(); }
            };
            rec(0);
            std::string s; for (int e : bestX) s += (s.empty() ? "" : ",") + edgeName(E[e]);
            double sec = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
            printf("  search |X|<=%d: admissible tested %ld, inadmissible %ld, working X %ld, best X={%s} leftover %ld (%.1fs)\n", KMAX, tested, inadm, works, s.c_str(), best, sec);
        }
        fflush(stdout);
    }
}
