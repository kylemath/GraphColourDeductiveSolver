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
//           -v  per-pass log to stderr
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
            else { val = isgood(canon_rank(p0 ^ (V & xa), p1 ^ (V & xb))); stamp[key] = cur; memo[key] = val; }
            if (val) { found = true; break; }
        }
        if (!found) { w = (uint16_t)p; return false; }
    }
    return true;
}

int main(int argc, char **argv) {
    bool jacobi = false, verbose = false; string ckpt; double tbudget = 1e18; string inpath;
    for (int a = 1; a < argc; a++) {
        string s = argv[a];
        if (s == "-j") jacobi = true; else if (s == "-v") verbose = true;
        else if (s == "-c") ckpt = argv[++a]; else if (s == "-t") tbudget = atof(argv[++a]);
        else inpath = s;
    }
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
        auto T0 = chrono::steady_clock::now();
        auto el = [&]() { return chrono::duration<double>(chrono::steady_clock::now() - T0).count(); };
        build_rank();
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
                if (canon_rank((u32)reps[i], (u32)(reps[i] >> 32)) != i) { fprintf(stderr, "%s: rank mismatch at %llu\n", name.c_str(), (unsigned long long)i); return 2; }
        }
        size_t W = (N + 63) / 64;
        good.assign(W, 0); wit.assign(N * 3, 0);
        u64 ext = 0; int pass = 0, depth = 0; u64 startpos = 0; bool changed = false; bool resumed = false;
        if (!ckpt.empty() && !jacobi) {
            FILE *f = fopen(ckpt.c_str(), "rb");
            if (f) {
                u64 hdr[7];
                if (fread(hdr, 8, 7, f) == 7 && hdr[0] == 0x4b43434b && hdr[1] == (u64)n && hdr[2] == N &&
                    fread(good.data(), 8, W, f) == W) {
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
            fwrite(hdr, 8, 7, f); fwrite(good.data(), 8, W, f); fclose(f);
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
                if (!jacobi && (i & 0xfffff) == 0 && el() - lastsave > 600) {
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
    }
    return 0;
}
