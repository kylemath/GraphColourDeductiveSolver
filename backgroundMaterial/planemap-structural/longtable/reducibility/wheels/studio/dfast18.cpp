// dfast.cpp -- Studio Job 9 (14 Oct 2026, exploratory): a C++ port of the Lean DCheck closure (dcheck/DCheck.lean,
// `run`), for screening many configurations.  Same model and the same level-synchronous closure, so classes, ext,
// reached and depth must agree with the Lean executable (checked on every Job 8 wheel).  Speed-up: for a stuck
// (class, theta) the set of classes reachable through its current matching is computed once and cached; at later
// levels only `good` is re-tested (the good set only grows, so a cached failure can only turn into a success).
// Input/Output: the WheelMain format.  Rings up to 18 (matchings of up to 18 transitions; dfast18 variant, Job 13).
// Build: c++ -O2 -std=c++17 -o dfast dfast.cpp
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <unordered_map>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <functional>
#include <chrono>
typedef uint64_t u64;

static int R, Mi;
static std::vector<std::vector<int>> ringAdj, intAdj;
static inline int col(u64 k, int i) { return (int)((k >> (2 * i)) & 3); }

static u64 canonc(u64 k) {
    int mp[4] = {-1, -1, -1, -1}, nx = 0; u64 out = 0;
    for (int i = 0; i < R; i++) { int c = col(k, i); if (mp[c] < 0) mp[c] = nx++; out |= (u64)mp[c] << (2 * i); }
    return out;
}

static std::vector<u64> ringColourings(int r) {
    std::vector<std::pair<u64, int>> cur = {{0, 1}};
    for (int i = 1; i < r; i++) {
        std::vector<std::pair<u64, int>> nx;
        for (auto [k, used] : cur)
            for (int c = 0; c < std::min(4, used + 1); c++)
                if (c != col(k, i - 1) && (i + 1 != r || c != col(k, 0)))
                    nx.push_back({k | ((u64)c << (2 * i)), c == used ? used + 1 : used});
        cur.swap(nx);
    }
    std::vector<u64> out; for (auto &p : cur) out.push_back(p.first);
    return out;
}

static bool extAux(u64 k, std::vector<int> &cols) {
    int a = cols.size(); if (a == Mi) return true;
    for (int x = 0; x < 4; x++) {
        bool ok = true;
        for (int t : ringAdj[a]) if (col(k, t) == x) { ok = false; break; }
        if (!ok) continue;
        for (int b : intAdj[a]) if (b < a && cols[b] == x) { ok = false; break; }
        if (!ok) continue;
        cols.push_back(x); if (extAux(k, cols)) { cols.pop_back(); return true; } cols.pop_back();
    }
    return false;
}

// non-crossing perfect matchings of 0..n-1 as arc-region labellings (same as DCheck.arcRegions)
static std::vector<std::vector<std::vector<int>>> matchTable;
static void ncm(std::vector<int> pts, std::vector<std::pair<int, int>> &cur, std::vector<std::vector<std::pair<int, int>>> &out) {
    if (pts.empty()) { out.push_back(cur); return; }
    int a = pts[0];
    for (size_t j = 1; j < pts.size(); j += 2) {
        std::vector<int> L(pts.begin() + 1, pts.begin() + j), Rr(pts.begin() + j + 1, pts.end());
        cur.push_back({a, pts[j]});
        std::vector<std::vector<std::pair<int, int>>> o1; std::vector<std::pair<int, int>> c1; ncm(L, c1, o1);
        std::vector<std::vector<std::pair<int, int>>> o2; std::vector<std::pair<int, int>> c2; ncm(Rr, c2, o2);
        for (auto &m1 : o1) for (auto &m2 : o2) { auto m = cur; m.insert(m.end(), m1.begin(), m1.end()); m.insert(m.end(), m2.begin(), m2.end()); out.push_back(m); }
        cur.pop_back();
    }
}
// DCheck.ncm order: for a :: rest, j over rest indices (even j), m1 from rest.take j, m2 from rest.drop (j+1):
// (a, rest[j]) :: m1 ++ m2.  The matching ORDER matters only for the progress pointer, not for the result
// (reached/depth): a class is good at level i+1 iff every matching is satisfied by the level-i good set.
static std::vector<int> arcRegions(int n, const std::vector<std::pair<int, int>> &Mt) {
    std::vector<int> lab(n); for (int i = 0; i < n; i++) lab[i] = i;
    for (auto [s, t] : Mt) {
        int i = std::min(s, t), j = std::max(s, t);
        int pr[2][2] = {{(i + n - 1) % n, j}, {i, (j + n - 1) % n}};
        for (auto &xy : pr) { int lx = lab[xy[0]], ly = lab[xy[1]]; for (int &l : lab) if (l == ly) l = lx; }
    }
    std::vector<int> mp(n, -1), out; int nx = 0;
    for (int j = 0; j < n; j++) { int l = lab[j]; if (mp[l] < 0) mp[l] = nx++; out.push_back(mp[l]); }
    return out;
}

int main(int argc, char **argv) {
    matchTable.resize(10);
    for (int p = 0; p <= 9; p++) {
        std::vector<int> pts(2 * p); for (int i = 0; i < 2 * p; i++) pts[i] = i;
        std::vector<std::vector<std::pair<int, int>>> ms; std::vector<std::pair<int, int>> cur; ncm(pts, cur, ms);
        for (auto &m : ms) matchTable[p].push_back(arcRegions(2 * p, m));
    }
    std::string line;
    FILE *in = argc > 1 ? fopen(argv[1], "r") : stdin;
    char buf[1 << 16];
    while (fgets(buf, sizeof buf, in)) {
        std::istringstream ss(buf); std::string name, ra, ia; int r, m;
        if (!(ss >> name >> r >> m >> ra >> ia)) continue;
        if (r > 18) { printf("%s r=%d m=%d SKIP ring>18\n", name.c_str(), r, m); fflush(stdout); continue; }
        auto parse = [](const std::string &s) { std::vector<std::vector<int>> out; std::stringstream q(s); std::string t;
            while (std::getline(q, t, ';')) { std::vector<int> v; if (t != "-") { std::stringstream q2(t); std::string a; while (std::getline(q2, a, ',')) v.push_back(atoi(a.c_str())); } out.push_back(v); }
            return out; };
        R = r; Mi = m; ringAdj = parse(ra); intAdj = parse(ia);
        auto t0 = std::chrono::steady_clock::now();
        std::vector<u64> ks = ringColourings(r); size_t N = ks.size();
        std::unordered_map<u64, int> index; index.reserve(N * 2);
        for (size_t i = 0; i < N; i++) index[ks[i]] = i;
        std::vector<char> good(N);
        size_t ext = 0;
        for (size_t i = 0; i < N; i++) { std::vector<int> cols; good[i] = extAux(ks[i], cols); ext += good[i]; }
        size_t reached = ext; int depth = 0;
        const int DEAD = 1 << 30;
        std::vector<int> prog(3 * N, 0);
        std::vector<std::vector<int>> cache(3 * N);     // reachable classes of the current (stuck) matching
        std::vector<char> cached(3 * N, 0);
        for (size_t level = 0; level <= N; level++) {
            std::vector<int> nw;
            for (size_t i = 0; i < N; i++) {
                if (good[i]) continue;
                u64 k = ks[i]; bool done = false;
                for (int th = 1; th <= 3 && !done; th++) {
                    int slot = 3 * i + th - 1; int pi = prog[slot];
                    if (pi == DEAD) continue;
                    int T[32], n = 0;
                    for (int v = 0; v < r; v++) { int x = col(k, v) ^ col(k, (v + 1) % r); if (x != 0 && x != th) T[n++] = v; }
                    if (n == 0) { prog[slot] = DEAD; continue; }
                    std::vector<int> arcOf(r);
                    for (int v = 0; v < r; v++) { int c = 0; for (int q = 0; q < n; q++) if (T[q] < v) c++; arcOf[v] = (c + n - 1) % n; }
                    auto &mats = matchTable[n / 2];
                    int ptr = pi; bool stuck = false;
                    while (ptr < (int)mats.size() && !stuck) {
                        bool sat = false;
                        if (cached[slot]) {
                            for (int j : cache[slot]) if (good[j]) { sat = true; break; }
                        } else {
                            auto &lab = mats[ptr]; int P = n / 2;
                            u64 rm[16] = {0};
                            for (int v = 0; v < r; v++) { int g = lab[arcOf[v]]; rm[g] |= (u64)th << (2 * v); }
                            std::vector<int> reach;
                            for (int s = 1; s < (1 << P); s++) {
                                u64 k2 = k; for (int b = 0; b < P; b++) if (s >> b & 1) k2 ^= rm[b + 1];
                                auto it = index.find(canonc(k2));
                                if (it != index.end()) { if (good[it->second]) { sat = true; break; } reach.push_back(it->second); }
                            }
                            if (!sat) { std::sort(reach.begin(), reach.end()); reach.erase(std::unique(reach.begin(), reach.end()), reach.end()); cache[slot] = reach; cached[slot] = 1; }
                        }
                        if (sat) { ptr++; cached[slot] = 0; cache[slot].clear(); cache[slot].shrink_to_fit(); }
                        else stuck = true;
                    }
                    prog[slot] = ptr;
                    if (ptr == (int)mats.size()) done = true;
                }
                if (done) nw.push_back(i);
            }
            if (nw.empty()) break;
            for (int i : nw) good[i] = 1;
            reached += nw.size(); depth++;
        }
        double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
        printf("%s r=%d m=%d classes=%zu ext=%zu reached=%zu D=%s depth=%d %.0fms\n", name.c_str(), r, m, N, ext, reached, reached == N ? "true" : "false", depth, ms);
        fflush(stdout);
    }
}
