// f66.cpp -- Track F [exploratory]: DL runs, all-DL pi-cycles and lock-pocket geometry at degree-5 holes.
// Independent re-implementation (does not share code with picyc.cpp / radius.py); same definitions as NightG66 §1.1:
//   state at hole h = proper 4-colouring of T - h up to renaming. Unfilled states are normalised by FIXING the link:
//   repeat index j, colours x_j..x_{j+4} = (alpha, mu, alpha, A, B) = (0, 1, 0, 2, 3). Each unfilled class mod S4 has exactly
//   one such representative, so the key is the colouring vector itself.
//   Lock1: x_{j+3} in the {mu,A}-component K1 of m = x_{j+1};  Lock2: x_{j+4} in the {mu,B}-component K2 of m;  DL = both.
//   pi on a DL state (R+3): swap the {alpha,A}-component K of x_{j+2}; image is unfilled at j+3 with link (alpha,B,alpha,mu,A),
//   renamed (0,3,1,2) -> (0,1,2,3) i.e. old 0->0, 3->1, 1->2, 2->3.
//   pocket2 = component of x_{j+2} in T - h - K2 (the Tait pocket of the Lock2 inner path s_{j+1}..s_{j+3});
//   pocket1 = component of x_{j+2} in T - h - K1 (the Tait pocket of the Lock1 inner path s_{j+1}..s_{j+2}).
//   curv(X) = sum_{v in X} (6 - deg v);  E(X,K) = number of T-edges between X and K.
// Modes:  exh (default): enumerate all DL states at each hole;  --sample S: S random fixed-link colourings per hole,
//   each DL hit is extended to its full maximal DL run (pi forward, pi^{-1} backward) -- for graphs too large to enumerate.
// Input: "name n r0;r1;...;r_{n-1}" (0-based rotation lists), one graph per line.  n <= 64*W.
// Output: one JSON line per hole.  --dump L: also dump every maximal run of length >= L (pocket pentagon sets per state).
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
#include <set>
#include <random>
#include <chrono>
#ifndef W
#define W 4
#endif
typedef uint64_t u64;
struct BS { u64 w[W]; };
static inline void bclr(BS &a) { for (int i = 0; i < W; i++) a.w[i] = 0; }
static inline void bset(BS &a, int v) { a.w[v >> 6] |= 1ULL << (v & 63); }
static inline bool bget(const BS &a, int v) { return a.w[v >> 6] >> (v & 63) & 1; }
static inline bool bany(const BS &a) { for (int i = 0; i < W; i++) if (a.w[i]) return true; return false; }
static inline int bcount(const BS &a) { int c = 0; for (int i = 0; i < W; i++) c += __builtin_popcountll(a.w[i]); return c; }
struct Key { u64 k[(2 * 64 * W) / 64]; bool operator<(const Key &o) const { for (int i = 0; i < 2 * W; i++) if (k[i] != o.k[i]) return k[i] < o.k[i]; return false; }
                                          bool operator==(const Key &o) const { for (int i = 0; i < 2 * W; i++) if (k[i] != o.k[i]) return false; return true; } };
static int N, H; static std::vector<std::vector<int>> rot; static std::vector<int> deg; static BS adj[64 * W];
static int X[5];                     // link of H in rotation order
static std::vector<int> order;       // colouring order of T - H (link first, then BFS)
static std::vector<std::vector<int>> prevn;  // earlier neighbours in order
static std::vector<Key> DL;          // sorted DL keys
static long long nUnf = 0, capN = 400000000LL; static bool capHit = false;
static int col[64 * W];

static inline Key keyof(const int *c) { Key K; memset(&K, 0, sizeof K); for (int v = 0; v < N; v++) if (v != H) K.k[v >> 5] |= (u64)c[v] << (2 * (v & 31)); return K; }
static inline void unkey(const Key &K, int *c) { for (int v = 0; v < N; v++) c[v] = v == H ? -1 : (int)(K.k[v >> 5] >> (2 * (v & 31)) & 3); }
static inline BS flood(int s, const BS &M) { BS comp, front; bclr(comp); bset(comp, s); front = comp;
    while (bany(front)) { BS nb; bclr(nb);
        for (int i = 0; i < W; i++) for (u64 f = front.w[i]; f; f &= f - 1) { int u = i * 64 + __builtin_ctzll(f); for (int q = 0; q < W; q++) nb.w[q] |= adj[u].w[q]; }
        for (int q = 0; q < W; q++) { nb.w[q] &= M.w[q] & ~comp.w[q]; comp.w[q] |= nb.w[q]; } front = nb; }
    return comp; }
static inline void cmask(const int *c, BS *cm) { for (int a = 0; a < 4; a++) bclr(cm[a]); for (int v = 0; v < N; v++) if (v != H) bset(cm[c[v]], v); }
static inline BS bor(const BS &a, const BS &b) { BS r; for (int i = 0; i < W; i++) r.w[i] = a.w[i] | b.w[i]; return r; }
static int repeat_index(const int *c) { int lc[5]; int seen = 0; for (int t = 0; t < 5; t++) { lc[t] = c[X[t]]; seen |= 1 << lc[t]; }
    if (__builtin_popcount(seen) < 4) return -1; for (int j = 0; j < 5; j++) if (lc[j] == lc[(j + 2) % 5]) return j; return -2; }
// normalise an unfilled colouring to fixed-link form; returns j
static int normalise(int *c) { int j = repeat_index(c); if (j < 0) return j; int mp[4]; mp[c[X[j]]] = 0; mp[c[X[(j + 1) % 5]]] = 1; mp[c[X[(j + 3) % 5]]] = 2; mp[c[X[(j + 4) % 5]]] = 3;
    for (int v = 0; v < N; v++) if (v != H) c[v] = mp[c[v]]; return j; }
struct Info { int j, l1, l2; BS K1, K2; };
static Info info(const int *c, const BS *cm) { Info r; r.j = repeat_index(c); r.l1 = r.l2 = 0; if (r.j < 0) return r; int j = r.j;
    int m = X[(j + 1) % 5], a = X[(j + 3) % 5], b = X[(j + 4) % 5]; int mu = c[m], A = c[a], B = c[b];
    r.K1 = flood(m, bor(cm[mu], cm[A])); r.K2 = flood(m, bor(cm[mu], cm[B])); r.l1 = bget(r.K1, a); r.l2 = bget(r.K2, b); return r; }
// pi of a DL state in normal form (colours 0,1,0,2,3 at j..): returns new normalised colouring in nc, new j
static int pi_dl(const int *c, int j, int *nc) { BS cm[4]; cmask(c, cm); BS K = flood(X[(j + 2) % 5], bor(cm[0], cm[2]));
    for (int v = 0; v < N; v++) { if (v == H) { nc[v] = -1; continue; } int x = c[v]; if (bget(K, v)) x = x == 0 ? 2 : (x == 2 ? 0 : x); nc[v] = x; }
    return normalise(nc); }
// candidate pi^{-1}: swap the {alpha,B} = {0,3}-component of x_{j+4}
static int piinv_cand(const int *c, int j, int *nc) { BS cm[4]; cmask(c, cm); BS K = flood(X[(j + 4) % 5], bor(cm[0], cm[3]));
    for (int v = 0; v < N; v++) { if (v == H) { nc[v] = -1; continue; } int x = c[v]; if (bget(K, v)) x = x == 0 ? 3 : (x == 3 ? 0 : x); nc[v] = x; }
    return normalise(nc); }
static bool isDL(const int *c) { BS cm[4]; cmask(c, cm); Info I = info(c, cm); return I.j >= 0 && I.l1 && I.l2; }
// Lock parity lemma (Track F): Lock2 <=> K_{alpha,A}(x_{j+2}) has odd curvature; Lock1 <=> K_{alpha,B}(x_{j+2}) odd;
// K_{alpha,mu}(x_{j+2}) always odd.  curvature parity = number of odd-degree vertices (mod 2).
static BS oddv; static long long lpBad[3] = {0, 0, 0}, lpCnt = 0;
static inline int bpar(const BS &a, const BS &b) { int c = 0; for (int i = 0; i < W; i++) c += __builtin_popcountll(a.w[i] & b.w[i]); return c & 1; }
static void lockparity(const int *c) { BS cm[4]; cmask(c, cm); Info I = info(c, cm); if (I.j < 0) return; int x2 = X[(I.j + 2) % 5];
    BS KA = flood(x2, bor(cm[0], cm[2])), KB = flood(x2, bor(cm[0], cm[3])), KM = flood(x2, bor(cm[0], cm[1])); lpCnt++;
    if (bpar(KA, oddv) != I.l2) lpBad[0]++; if (bpar(KB, oddv) != I.l1) lpBad[1]++; if (!bpar(KM, oddv)) lpBad[2]++; }
static bool LP = false;
static void rec(int i) {
    if (capHit) return;
    if (i == (int)order.size()) { nUnf++; if (nUnf > capN) { capHit = true; return; } if (LP) lockparity(col); if (isDL(col)) DL.push_back(keyof(col)); return; }
    int v = order[i]; int forb = 0; for (int u : prevn[i]) forb |= 1 << col[u];
    for (int a = 0; a < 4; a++) if (!(forb >> a & 1)) { col[v] = a; rec(i + 1); } col[v] = -1;
}
static std::mt19937_64 RNG(12345); static long long nodeBudget;
static bool recr(int i) {
    if (--nodeBudget < 0) return false;
    if (i == (int)order.size()) return true;
    int v = order[i]; int forb = 0; for (int u : prevn[i]) forb |= 1 << col[u];
    int perm[4] = {0, 1, 2, 3}; std::shuffle(perm, perm + 4, RNG);
    for (int t = 0; t < 4; t++) { int a = perm[t]; if (!(forb >> a & 1)) { col[v] = a; if (recr(i + 1)) return true; } } col[v] = -1; return false;
}
static void setup_order(int j) { // link fixed first, then BFS
    order.clear(); std::vector<int> seen(N, 0); seen[H] = 1; for (int t = 0; t < 5; t++) { order.push_back(X[(j + t) % 5]); seen[X[(j + t) % 5]] = 1; }
    for (size_t q = 0; q < order.size(); q++) { int u = order[q]; for (int w : rot[u]) if (!seen[w]) { seen[w] = 1; order.push_back(w); } }
    std::vector<int> pos(N, -1); for (size_t q = 0; q < order.size(); q++) pos[order[q]] = q;
    prevn.assign(order.size(), {}); for (size_t q = 5; q < order.size(); q++) for (int w : rot[order[q]]) if (w != H && pos[w] < (int)q) prevn[q].push_back(w);
}
static void fixlink(int j) { for (int v = 0; v < N; v++) col[v] = -1; int L5[5] = {0, 1, 0, 2, 3}; for (int t = 0; t < 5; t++) col[X[(j + t) % 5]] = L5[t]; }
// geometry of a DL state
struct Geo { int curv1, curv2, E1, E2, np1, np2, sz1, sz2, szK1, szK2, rK; bool ok; std::vector<int> P1, P2; };
static std::vector<int> distH;
static Geo geo(const int *c, int j) { BS cm[4]; cmask(c, cm); Info I = info(c, cm); Geo g; g.ok = true;
    BS all; bclr(all); for (int v = 0; v < N; v++) if (v != H) bset(all, v);
    auto pocket = [&](const BS &K, int &curv, int &E, int &np, int &sz, std::vector<int> &P) { BS M; for (int q = 0; q < W; q++) M.w[q] = all.w[q] & ~K.w[q];
        BS Pk = flood(X[(j + 2) % 5], M); curv = 0; E = 0; np = 0; sz = bcount(Pk); P.clear();
        for (int v = 0; v < N; v++) if (bget(Pk, v)) { curv += 6 - deg[v]; if (deg[v] != 6) { np++; P.push_back(v); } for (int w : rot[v]) if (w != H && bget(K, w)) E++; }
        return Pk; };
    BS P1 = pocket(I.K1, g.curv1, g.E1, g.np1, g.sz1, g.P1); BS P2 = pocket(I.K2, g.curv2, g.E2, g.np2, g.sz2, g.P2);
    // Jordan sanity: x_j not in either pocket; x_{j+3} in pocket2
    if (bget(P2, X[j]) || bget(P1, X[j]) || !bget(P2, X[(j + 3) % 5]) || bget(P1, X[(j + 4) % 5])) g.ok = false;
    g.szK1 = bcount(I.K1); g.szK2 = bcount(I.K2); g.rK = 0; BS u = bor(I.K1, I.K2); for (int v = 0; v < N; v++) if (bget(u, v)) g.rK = std::max(g.rK, distH[v]);
    return g; }
static std::string vlist(const std::vector<int> &P) { std::string s = "["; for (size_t i = 0; i < P.size(); i++) { s += (i ? "," : "") + std::to_string(P[i]); } return s + "]"; }

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: f66 FILE [--holes 5|all|h,h] [--sample S] [--seed s] [--dump L] [--cap M] [--budget B] [--only66666]\n"); return 1; }
    long long sample = 0; int dumpL = 1 << 30; long long budget = 2000000; bool only66 = false; std::string holesel = "5"; FILE *DF = nullptr;
    for (int i = 2; i < argc; i++) { std::string a = argv[i];
        if (a == "--sample") sample = atoll(argv[++i]); else if (a == "--seed") RNG.seed(atoll(argv[++i])); else if (a == "--dump") dumpL = atoi(argv[++i]);
        else if (a == "--cap") capN = atoll(argv[++i]); else if (a == "--budget") budget = atoll(argv[++i]); else if (a == "--only66666") only66 = true;
        else if (a == "--holes") holesel = argv[++i]; else if (a == "--lockparity") LP = true; else if (a == "--dumpfile") DF = fopen(argv[++i], "w"); }
    if (!DF) DF = stdout;
    FILE *in = fopen(argv[1], "r"); if (!in) { perror("open"); return 1; }
    static char line[1 << 20];
    while (fgets(line, sizeof line, in)) {
        char name[256]; int n, off; if (sscanf(line, "%255s %d %n", name, &n, &off) < 2) continue; if (n > 64 * W) { fprintf(stderr, "skip %s n=%d\n", name, n); continue; }
        N = n; rot.assign(N, {}); char *p = line + off; for (int v = 0; v < N; v++) { while (*p && *p != ';' && *p != '\n' && *p != ' ' && *p != '\r') { int x = strtol(p, &p, 10); rot[v].push_back(x); if (*p == ',') p++; } if (*p == ';') p++; }
        deg.assign(N, 0); bclr(oddv); for (int v = 0; v < N; v++) { deg[v] = rot[v].size(); bclr(adj[v]); for (int w : rot[v]) bset(adj[v], w); if (deg[v] & 1) bset(oddv, v); }
        std::vector<int> holes; if (holesel == "5") { for (int v = 0; v < N; v++) if (deg[v] == 5) holes.push_back(v); }
        else if (holesel == "all") { for (int v = 0; v < N; v++) holes.push_back(v); } else { char *q = (char *)holesel.c_str(); while (*q) { holes.push_back(strtol(q, &q, 10)); if (*q == ',') q++; } }
        for (int h : holes) {
            if (deg[h] != 5) continue; H = h; for (int t = 0; t < 5; t++) X[t] = rot[h][t];
            std::string pat; for (int t = 0; t < 5; t++) pat += std::to_string(std::min(deg[X[t]], 8));
            bool is66 = true; for (int t = 0; t < 5; t++) if (deg[X[t]] != 6) is66 = false; if (only66 && !is66) continue;
            // distances from h
            distH.assign(N, -1); { std::vector<int> q{h}; distH[h] = 0; for (size_t a = 0; a < q.size(); a++) for (int w : rot[q[a]]) if (distH[w] < 0) { distH[w] = distH[q[a]] + 1; q.push_back(w); } }
            int dpent = 99; for (int v = 0; v < N; v++) if (v != h && deg[v] != 6 && distH[v] < dpent) dpent = distH[v];
            auto t0 = std::chrono::steady_clock::now();
            // ---- collect DL states (exhaustive) or runs (sample)
            std::map<int, long long> RL; long long nall = 0; std::vector<int> allL; long long maxrun = 0; long long parfail1 = 0, parfail2 = 0, jordanfail = 0;
            std::map<std::string, long long> mod4; std::map<int, long long> np2h, np1h; std::map<int, std::pair<long long, long long>> runByNp2; // np2 -> (count, sum of run length containing)
            long long nDLtot = 0, runsSeen = 0, samplesDone = 0; long long piFail = 0; int maxrK = 0;
            std::vector<std::vector<int>> runsStates; // not stored; dumping inline
            int c[64 * W], nc[64 * W];
            auto process_run = [&](std::vector<Key> &run, bool cyc) {
                long long L = run.size(); if (cyc) { nall++; allL.push_back(L); } else { RL[L]++; maxrun = std::max(maxrun, L); }
                bool dump = L >= dumpL || cyc;
                std::string ds;
                for (long long i = 0; i < L; i++) { unkey(run[i], c); int j = repeat_index(c); Geo g = geo(c, j);
                    if (!g.ok) jordanfail++; if ((g.curv2 & 1) == 0) parfail2++; if ((g.curv1 & 1) == 0) parfail1++;
                    mod4["p2 curv+E mod4=" + std::to_string(((g.curv2 + g.E2) % 4 + 4) % 4)]++; mod4["p1 curv+E mod4=" + std::to_string(((g.curv1 + g.E1) % 4 + 4) % 4)]++;
                    np2h[g.np2]++; np1h[g.np1]++; auto &e = runByNp2[g.np2]; e.first++; e.second += L; maxrK = std::max(maxrK, g.rK);
                    if (dump) { char b[256]; snprintf(b, sizeof b, "%s{\"j\":%d,\"P1\":%s,\"P2\":%s,\"c1\":%d,\"c2\":%d,\"E1\":%d,\"E2\":%d,\"sz1\":%d,\"sz2\":%d,\"K1\":%d,\"K2\":%d,\"rK\":%d}", i ? "," : "", j, vlist(g.P1).c_str(), vlist(g.P2).c_str(), g.curv1, g.curv2, g.E1, g.E2, g.sz1, g.sz2, g.szK1, g.szK2, g.rK); ds += b; } }
                if (dump) { // end info: which lock dies at the image of the last state
                    std::string endk = "cycle"; if (!cyc) { unkey(run[L - 1], c); int j = repeat_index(c); int j2 = pi_dl(c, j, nc); BS cm[4]; cmask(nc, cm); Info I = info(nc, cm);
                        endk = j2 < 0 ? "filled" : (I.l1 && !I.l2 ? "Lock1only" : (!I.l1 && I.l2 ? "Lock2only" : (!I.l1 && !I.l2 ? "lockless" : "DL?"))); }
                    std::string pents = "["; bool f = true; for (int v = 0; v < N; v++) if (v != H && deg[v] != 6) { pents += (f ? "" : ",") + std::string("[") + std::to_string(v) + "," + std::to_string(distH[v]) + "]"; f = false; } pents += "]";
                    fprintf(DF, "{\"kind\":\"run\",\"graph\":\"%s\",\"hole\":%d,\"pattern\":\"%s\",\"L\":%lld,\"cycle\":%d,\"end\":\"%s\",\"pents\":%s,\"states\":[%s]}\n", name, h, pat.c_str(), L, cyc ? 1 : 0, endk.c_str(), pents.c_str(), ds.c_str()); fflush(DF); }
            };
            if (!sample) {
                lpBad[0] = lpBad[1] = lpBad[2] = lpCnt = 0; DL.clear(); nUnf = 0; capHit = false;
                for (int j = 0; j < 5; j++) { setup_order(j); fixlink(j); rec(5); }
                std::sort(DL.begin(), DL.end()); long long S = DL.size(); nDLtot = S;
                std::vector<long long> nxt(S, -1), prv(S, -1);
                for (long long i = 0; i < S; i++) { unkey(DL[i], c); int j = repeat_index(c); int j2 = pi_dl(c, j, nc); if (j2 != (j + 3) % 5) { piFail++; continue; }
                    Key k = keyof(nc); auto it = std::lower_bound(DL.begin(), DL.end(), k); if (it != DL.end() && *it == k) { long long t = it - DL.begin(); nxt[i] = t; if (prv[t] >= 0) piFail++; prv[t] = i; } }
                std::vector<char> vis(S, 0);
                for (long long i = 0; i < S; i++) if (prv[i] < 0 && !vis[i]) { std::vector<Key> run; long long t = i; while (t >= 0 && !vis[t]) { vis[t] = 1; run.push_back(DL[t]); t = nxt[t]; } process_run(run, false); runsSeen++; }
                for (long long i = 0; i < S; i++) if (!vis[i]) { std::vector<Key> run; long long t = i; while (t >= 0 && !vis[t]) { vis[t] = 1; run.push_back(DL[t]); t = nxt[t]; } if (t < 0) { piFail++; process_run(run, false); } else process_run(run, true); runsSeen++; }
            } else {
                std::set<Key> seenRun;  // keys of run starts already processed
                for (long long s = 0; s < sample; s++) {
                    int j = RNG() % 5; setup_order(j); fixlink(j); nodeBudget = budget; if (!recr(5)) continue; samplesDone++;
                    for (int v = 0; v < N; v++) c[v] = col[v]; c[H] = -1; if (!isDL(c)) continue; nDLtot++;
                    // walk backward to run start (or detect cycle)
                    Key k0 = keyof(c); std::vector<Key> back; bool cyc = false; int cur[64 * W]; memcpy(cur, c, sizeof(int) * N);
                    for (long long step = 0; step < 100000; step++) { int jj = repeat_index(cur); int j2 = piinv_cand(cur, jj, nc); if (j2 != (jj + 2) % 5 || !isDL(nc)) break;
                        int chk[64 * W]; pi_dl(nc, j2, chk); if (!(keyof(chk) == keyof(cur))) { piFail++; break; } Key kk = keyof(nc); if (kk == k0) { cyc = true; break; } back.push_back(kk); memcpy(cur, nc, sizeof(int) * N); }
                    Key start = back.empty() ? k0 : back.back(); if (seenRun.count(start)) continue; seenRun.insert(start);
                    std::vector<Key> run(back.rbegin(), back.rend()); run.push_back(k0);
                    if (!cyc) { memcpy(cur, c, sizeof(int) * N); for (long long step = 0; step < 100000; step++) { int jj = repeat_index(cur); pi_dl(cur, jj, nc); if (!isDL(nc)) break; Key kk = keyof(nc); if (kk == start) { cyc = true; break; } run.push_back(kk); memcpy(cur, nc, sizeof(int) * N); } }
                    else { run.clear(); run.push_back(k0); memcpy(cur, c, sizeof(int) * N); while (true) { int jj = repeat_index(cur); pi_dl(cur, jj, nc); Key kk = keyof(nc); if (kk == k0) break; run.push_back(kk); memcpy(cur, nc, sizeof(int) * N); } }
                    process_run(run, cyc); runsSeen++;
                }
            }
            double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
            std::string rl = "{"; bool f = true; for (auto &kv : RL) { rl += (f ? "" : ",") + std::string("\"") + std::to_string(kv.first) + "\":" + std::to_string(kv.second); f = false; } rl += "}";
            std::string m4 = "{"; f = true; for (auto &kv : mod4) { m4 += (f ? "" : ",") + std::string("\"") + kv.first + "\":" + std::to_string(kv.second); f = false; } m4 += "}";
            std::string h2 = "{"; f = true; for (auto &kv : runByNp2) { char b[96]; snprintf(b, sizeof b, "%s\"%d\":[%lld,%.3f]", f ? "" : ",", kv.first, kv.second.first, (double)kv.second.second / kv.second.first); h2 += b; f = false; } h2 += "}";
            std::string h1 = "{"; f = true; for (auto &kv : np1h) { h1 += (f ? "" : ",") + std::string("\"") + std::to_string(kv.first) + "\":" + std::to_string(kv.second); f = false; } h1 += "}";
            std::string al = "["; for (size_t i = 0; i < allL.size(); i++) al += (i ? "," : "") + std::to_string(allL[i]); al += "]";
            printf("{\"kind\":\"hole\",\"graph\":\"%s\",\"n\":%d,\"hole\":%d,\"pattern\":\"%s\",\"dpent\":%d,\"mode\":\"%s\",\"samples\":%lld,\"nUnf\":%lld,\"nDL\":%lld,\"cap\":%d,\"runs\":%lld,\"maxrun\":%lld,\"allDL\":%lld,\"allDL_L\":%s,\"piFail\":%lld,\"parfail1\":%lld,\"parfail2\":%lld,\"jordanfail\":%lld,\"maxrK\":%d,\"mod4\":%s,\"np2\":%s,\"np1\":%s,\"runlen\":%s,\"lp\":[%lld,%lld,%lld,%lld],\"secs\":%.2f}\n",
                   name, N, h, pat.c_str(), dpent, sample ? "sample" : "exh", samplesDone, nUnf, nDLtot, capHit ? 1 : 0, runsSeen, maxrun, nall, al.c_str(), piFail, parfail1, parfail2, jordanfail, maxrK, m4.c_str(), h2.c_str(), h1.c_str(), rl.c_str(), lpCnt, lpBad[0], lpBad[1], lpBad[2], secs);
            fflush(stdout);
        }
    }
    return 0;
}
