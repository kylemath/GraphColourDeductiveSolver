// Fast exact C++ separator sep3r_l3q (100% drop-in compatible with WDIR/sep3r_l3q.cpp).
// Implements:
//  1. Tight XREL[st][c], EX6REL[ui][st][c], L3REL_TIGHT[st][c], L8REL7_TIGHT[st][c], L8REL8_TIGHT[st][c] in W[st][c].
//  2. Incremental resolution of X, EX6, FB6, RTAB, L3Q, L3Q8 at the exact DFS step where their window slots are fixed.
//  3. Incremental pruning of FULL / SEP_FULLX (rpatN3) patterns using 1-hot 64-bit bitmasks for d <= 12.
//  4. Lossless cyclic rotation symmetry breaking ((wl[i], sl[i]) >= (wl[0], sl[0])) + min_ws-aware DP bounding.
//  5. Multi-threaded work-stealing across (ws_iter, a0) start states using std::thread.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <set>
#include <map>
#include <string>
#include <algorithm>
#include <unordered_set>
#include <cmath>
#include <thread>
#include <mutex>
#include <atomic>
using namespace std;

static int NV;
static int AL[3][125][25], VA[3][125][25], CO[3][125][25];
static set<string> RBIG;
struct Img { vector<pair<int,int>> rest; };
static map<int, vector<vector<Img>>> PIDX;
static const vector<vector<Img>> *CUR_PIDX = nullptr;

static uint32_t CODE_1HOT[625];
static void initCode1Hot() {
    for (int c = 0; c < 625; c++) {
        int d0 = (c / 125) % 5, d1 = (c / 25) % 5, d2 = (c / 5) % 5, d3 = c % 5;
        CODE_1HOT[c] = (1u << d0) | (1u << (5 + d1)) | (1u << (10 + d2)) | (1u << (15 + d3));
    }
}
static int revmask(int m) {
    int r = 0; for (int t = 0; t < 4; t++) r |= ((m >> (5 * t)) & 31) << (5 * (3 - t)); return r;
}
static inline bool matches(int m, int c) {
    uint32_t h = CODE_1HOT[c];
    return (h & (uint32_t)m) == h;
}
static void addPattern(int d, vector<pair<int,int>> P) {
    auto &V = PIDX[d]; if (V.empty()) V.resize(d * 625);
    set<vector<pair<int,int>>> seen;
    for (int refl = 0; refl < 2; refl++) for (int r = 0; r < d; r++) {
        vector<pair<int,int>> Q;
        for (auto [p, m] : P) {
            int q = refl ? ((d - p) % d) : p; int mm = refl ? revmask(m) : m;
            Q.push_back({(q + r) % d, mm});
        }
        sort(Q.begin(), Q.end());
        if (!seen.insert(Q).second) continue;
        auto last = Q.back(); Img im; im.rest.assign(Q.begin(), Q.end() - 1);
        for (int c = 0; c < 625; c++) if (matches(last.second, c)) V[last.first * 625 + c].push_back(im);
    }
}

static double W[125][25];
static double XREL[125][25];
static double EX6REL[3][125][25];
static double L3REL_TIGHT[125][25];
static double L8REL7_TIGHT[125][25];
static double L8REL8_TIGHT[125][25];

static int d, ui; static double thr; static int maxout;
static int NOSYM = 0;
static int NTHREADS = 0;

static vector<double> XV(140625, 0.0); static bool HASX = false;
static int RV[3][125][25][5]; static bool RMODE = false; static vector<double> RY; static int RA[125][25]; static double RMAXV = 0;

static vector<int> RES_X[33];
static vector<int> RES_EX6[33];
static vector<int> RES_RTAB[33];
static vector<int> RES_L3Q[33];

static inline int sidecode(int c, int a, int b) { return c * 25 + a * 5 + b; }
static inline int taucode(int f, int t, int s1, int s2) {
    int lo = min(s1, s2), hi = max(s1, s2);
    return ((f * 3 + t) * 125 + lo) * 125 + hi;
}

static inline int ws_step(int k) {
    k = ((k % d) + d) % d;
    return (k == 0 || k == d - 1) ? 0 : k - 1;
}
static inline int ss_step(int k) {
    k = ((k % d) + d) % d;
    return (k == d - 1) ? 0 : k;
}

struct MaskPat {
    uint64_t bw, bs;
};
static vector<MaskPat> MPATS_FULL[33];
static vector<vector<pair<int,int>>> FPATS_STEP[33];

static map<int, vector<vector<pair<int,int>>>> FULL;
static void addFull(int dd, vector<pair<int,int>> P) {
    auto &V = FULL[dd]; set<vector<pair<int,int>>> seen;
    for (int refl = 0; refl < 2; refl++) for (int r = 0; r < dd; r++) {
        vector<pair<int,int>> Q;
        for (auto [sl_, m] : P) {
            int isS = sl_ >= dd, i = isS ? sl_ - dd : sl_;
            int j = refl ? (isS ? ((2 * dd - i - 1) % dd) : ((dd - i) % dd)) : i;
            j = (j + r) % dd; Q.push_back({isS ? dd + j : j, m});
        }
        sort(Q.begin(), Q.end());
        if (seen.insert(Q).second) V.push_back(Q);
    }
}

static void buildSchedules() {
    auto pit = PIDX.find(d);
    CUR_PIDX = (pit != PIDX.end()) ? &(pit->second) : nullptr;
    for (int i = 0; i <= d; i++) {
        RES_X[i].clear();
        RES_EX6[i].clear();
        RES_RTAB[i].clear();
        RES_L3Q[i].clear();
        MPATS_FULL[i].clear();
        FPATS_STEP[i].clear();
    }
    for (int j = 0; j < d; j++) {
        int rx = max({j, ws_step(j - 2), ws_step(j - 1), ws_step(j), ws_step(j + 1), ws_step(j + 2), ss_step(j - 1), ss_step(j)});
        RES_X[rx].push_back(j);

        int rex6 = max({j, ws_step(j - 2), ws_step(j - 1), ws_step(j), ws_step(j + 1), ws_step(j + 2), ss_step(j - 2), ss_step(j - 1), ss_step(j), ss_step(j + 1)});
        RES_EX6[rex6].push_back(j);

        int rrtab = max({j, ws_step(j - 1), ws_step(j), ws_step(j + 1), ws_step(j + 2), ss_step(j - 1), ss_step(j), ss_step(j + 1)});
        RES_RTAB[rrtab].push_back(j);

        int rl3 = max(j, d - 2);
        RES_L3Q[rl3].push_back(j);
    }

    auto it = FULL.find(d);
    if (it != FULL.end()) {
        for (const auto &Q : it->second) {
            int r = 0;
            int mw[32], ms[32];
            for (int j = 0; j < d; j++) { mw[j] = 31; ms[j] = 31; }
            for (auto [sl_, m] : Q) {
                int stp = (sl_ < d) ? ws_step(sl_) : ss_step(sl_ - d);
                if (stp > r) r = stp;
                if (sl_ < d) mw[sl_] &= m;
                else ms[sl_ - d] &= m;
            }
            bool possible = true;
            for (int j = 0; j < d; j++) if (mw[j] == 0 || ms[j] == 0) { possible = false; break; }
            if (!possible) continue;
            if (d <= 12) {
                uint64_t bw = 0, bs = 0;
                for (int j = 0; j < d; j++) {
                    if (mw[j] != 31) bw |= (uint64_t((~mw[j]) & 31) << (5 * j));
                    if (ms[j] != 31) bs |= (uint64_t((~ms[j]) & 31) << (5 * j));
                }
                MPATS_FULL[r].push_back({bw, bs});
            } else {
                FPATS_STEP[r].push_back(Q);
            }
        }
    }
}

struct Res { double w; string link, s; vector<int> v; };
static map<vector<int>, Res> found;
static set<pair<double, vector<int>>> found_by_w;
static mutex found_mtx;
static bool ARRKEY = false;
static double RBEST[125][25];
static vector<double> EX6;
static bool HASEX6 = false;
static double RREL[125][25];
static vector<double> REX;
static bool HASR = false;
static bool HASFB = false; static double FBREL[3][125][25]; static vector<double> FBX;
static bool HASL8 = false; static double L8REL[125][25]; static vector<double> L8X, L8P;
static bool HASL = false; static double L3REL[125][25]; static vector<double> L3QEX, L3PQ;
struct F2BRule { uint64_t forb_w, forb_s, kill_mask; };
static bool HASF2B = false;
static double H2_TAB[3][5][5][5][5][2][2][5];
static vector<uint8_t> PMASK8, L3_MK0, L8_MK0;
static vector<F2BRule> F2B_W6[3][25];
static vector<F2BRule> F2B_W7[2][2][25];
static atomic<long long> total_nodes{0};

static string canonWord(const string &w) {
    string best = w; int n = w.size();
    for (int refl = 0; refl < 2; refl++) {
        string s = w; if (refl) reverse(s.begin(), s.end());
        for (int k = 0; k < n; k++) { string t = s.substr(k) + s.substr(0, k); if (t < best) best = t; }
    }
    return best;
}

static atomic<double> CT{0.0};
static inline double curThr() { return CT.load(memory_order_relaxed); }
static void updThrLocked() {
    if ((int)found.size() < maxout) { CT.store(thr, memory_order_relaxed); return; }
    CT.store(max(thr, found_by_w.begin()->first), memory_order_relaxed);
}

static int omax = 0;
static long long nodelimit = 20000000;
static atomic<bool> aborted{false};

static bool fullForbidden() {
    auto it = FULL.find(d); if (it == FULL.end()) return false;
    return false;
}

struct Worker {
    int wl[32], sl[32], code[32], vars[32];
    int st_hist[32], c_hist[32];
    int tin[32], tout[32];
    int a0 = 0;
    int min_ws = 0;
    uint64_t cur_w = 0, cur_s = 0;
    const vector<vector<double>> *Bnd = nullptr;
    long long local_nodes = 0;

    inline double contrib(int j) {
        tin[j] = tout[j] = -1;
        int wj = wl[j]; if (wj < 2) return 0.0;
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; };
        auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
        int lj = wj - 2;
        int to1 = taucode(ui, lj, sidecode(W_(j - 1), W_(j - 2), S_(j - 1)), sidecode(W_(j + 1), W_(j + 2), S_(j)));
        int ti1 = taucode(lj, ui, sidecode(W_(j - 1), S_(j - 1), W_(j - 2)), sidecode(W_(j + 1), S_(j), W_(j + 2)));
        tout[j] = to1; tin[j] = ti1;
        return XV[ti1] - XV[to1];
    }

    inline int termj(int j, const int *x) const {
        auto X = [&](int k) { return x[((k % d) + d) % d]; };
        auto sw = [&](int k) { k = ((k % d) + d) % d; return wl[k] <= 1 && (X(k - 1) | X(k) | X(k + 1)); };
        auto ss = [&](int k) { k = ((k % d) + d) % d; return sl[k] <= 1 && (X(k) | X(k + 1)); };
        int t = 0;
        if (sw(j)) {
            t += wl[j] + 5 - 4; if (sw(j + 1)) t--; bool a = ss(j), b = ss(j - 1); if (a) t--; if (b) t--;
            if (wl[j] == 0 && a && b) t--;
        }
        if (ss(j)) t += sl[j] + 5 - 3;
        return t;
    }

    int minRing() const {
        int ns = 0; for (int j = 0; j < d; j++) ns += wl[j] == 0;
        if (ns < 2) return 1000;
        if (ns <= 12) {
            vector<int> pos; for (int j = 0; j < d; j++) if (wl[j] == 0) pos.push_back(j);
            int best = 1000, x[32];
            for (int m = 0; m < (1 << ns); m++) {
                if (__builtin_popcount(m) < 2) continue;
                for (int j = 0; j < d; j++) x[j] = 0;
                for (int k = 0; k < ns; k++) if (m >> k & 1) x[pos[k]] = 1;
                int r = d; for (int j = 0; j < d; j++) r += termj(j, x);
                best = min(best, r);
            }
            return best;
        }
        return 0;
    }

    int ringOf(const vector<int> &S) const {
        int x[32]; for (int j = 0; j < d; j++) x[j] = 0;
        for (int p : S) x[p] = 1;
        int r = d; for (int j = 0; j < d; j++) r += termj(j, x);
        return r;
    }

    bool oracleHit(int i) const {
        vector<int> P; for (int p = 0; p < i; p++) if (wl[p] == 0) P.push_back(p);
        for (size_t a = 0; a < P.size(); a++) {
            if (ringOf({P[a], i}) <= omax) return true;
            for (size_t b = a + 1; b < P.size(); b++) if (ringOf({P[a], P[b], i}) <= omax) return true;
        }
        return false;
    }

    inline bool forbidden(int i) const {
        if (!CUR_PIDX) return false;
        const auto &L = (*CUR_PIDX)[i * 625 + code[i]];
        for (const auto &im : L) {
            bool ok = true;
            for (auto [p, m] : im.rest) if (code[p] < 0 || !matches(m, code[p])) { ok = false; break; }
            if (ok) return true;
        }
        return false;
    }

    inline bool fullForbiddenStep(int i) const {
        if (d <= 12) {
            for (const auto &mp : MPATS_FULL[i]) {
                if (((cur_w & mp.bw) | (cur_s & mp.bs)) == 0) return true;
            }
            return false;
        }
        for (const auto &Q : FPATS_STEP[i]) {
            bool ok = true;
            for (auto [sl_, m] : Q) {
                int v = sl_ < d ? wl[sl_] : sl[sl_ - d];
                if (!((m >> v) & 1)) { ok = false; break; }
            }
            if (ok) return true;
        }
        return false;
    }

    inline double exact_ex6(int i) const {
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; };
        auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
        long idx = ((((((((long)ui * 5 + W_(i - 2)) * 5 + W_(i - 1)) * 5 + W_(i + 1)) * 5 + W_(i + 2)) * 5 + S_(i - 2)) * 5 + S_(i - 1)) * 5 + S_(i)) * 5 + S_(i + 1);
        return EX6[idx];
    }

    inline double exact_rtab(int i) const {
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; };
        auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
        long idx = ((((long)W_(i - 1) * 5 + W_(i)) * 5 + W_(i + 1)) * 5 + W_(i + 2)) * 25 + S_(i - 1) * 5 + S_(i + 1);
        return REX[idx];
    }

    inline double exact_fb(int i) const {
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; };
        auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
        long idx = ((((((((((long)ui * 5 + W_(i - 2)) * 5 + W_(i - 1)) * 5 + W_(i)) * 5 + W_(i + 1)) * 5 + W_(i + 2)) * 5 + S_(i - 2)) * 5 + S_(i - 1)) * 5 + S_(i)) * 5 + S_(i + 1));
        return FBX[idx];
    }

    inline double exact_l3q7(int i) const {
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; };
        auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
        double v = 0.0;
        for (int sg = 0; sg < 2; sg++) {
            int e = sg == 0 ? 1 : -1;
            int cc = W_(i + e), a = sg == 0 ? S_(i) : S_(i - 1), o = sg == 0 ? S_(i - 1) : S_(i);
            long q = (((((long)sg * 5 + cc) * 5 + a) * 5 + W_(i + 2 * e)) * 5 + W_(i + 3 * e)) * 5 + W_(i + 4 * e);
            v += L3QEX[q * 5 + o];
            v -= L3PQ[(W_(i + e) * 5 + W_(i + 2 * e)) * 5 + W_(i + 3 * e)];
        }
        return v;
    }

    inline double exact_l3q8_8(int i) const {
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; };
        auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
        double v = 0.0;
        for (int sg = 0; sg < 2; sg++) {
            int e = sg == 0 ? 1 : -1;
            int cc = W_(i + e), a = sg == 0 ? S_(i) : S_(i - 1), o = sg == 0 ? S_(i - 1) : S_(i);
            long q = (((((long)sg * 5 + cc) * 5 + a) * 5 + W_(i + 2 * e)) * 5 + W_(i + 3 * e)) * 5 + W_(i + 4 * e);
            v += L8X[q * 5 + o];
        }
        return v;
    }

    inline double exact_l3q8_7(int i) const {
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; };
        double v = 0.0;
        for (int sg = 0; sg < 2; sg++) {
            int e = sg == 0 ? 1 : -1;
            v -= L8P[(W_(i + e) * 5 + W_(i + 2 * e)) * 5 + W_(i + 3 * e)];
        }
        return v;
    }

    void leaf(double w) {
        if ((HASEX6 || HASR || HASL || HASL8 || HASFB) && w <= curThr()) return;
        if (HASF2B && d >= 7 && d <= 9) {
            auto W_ = [&](int k) { return wl[((k % d) + d) % d]; };
            auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
            for (int i = 0; i < d; i++) {
                if (wl[i] == 1) {
                    int sm1 = S_(i - 1), s0 = sl[i];
                    const auto &bkt = F2B_W6[ui][sm1 * 5 + s0];
                    if (!bkt.empty()) {
                        uint64_t rw = 0, rs = 0;
                        for (int off = 0; off < d; off++) {
                            int p = (i + off) % d;
                            rw |= (1ULL << (5 * off + wl[p]));
                            rs |= (1ULL << (5 * off + sl[p]));
                        }
                        uint8_t extra = 0;
                        for (const auto &r : bkt) {
                            if (((rw & r.forb_w) | (rs & r.forb_s)) == 0) extra |= (uint8_t)r.kill_mask;
                        }
                        if (extra) {
                            int wm2 = W_(i - 2), wm1 = W_(i - 1), wp1 = W_(i + 1), wp2 = W_(i + 2);
                            int sm2 = S_(i - 2), sp1 = S_(i + 1);
                            long idx8 = ((((((((long)ui * 5 + wm2) * 5 + wm1) * 5 + wp1) * 5 + wp2) * 5 + sm2) * 5 + sm1) * 5 + s0) * 5 + sp1;
                            uint8_t mk0 = PMASK8[idx8];
                            if (mk0 & extra) {
                                uint8_t mk = mk0 & ~extra;
                                int ap_m2 = wm2 >= 2 ? 1 : 0, ap_p2 = wp2 >= 2 ? 1 : 0;
                                const double *ht = H2_TAB[ui][wm1][sm1][s0][wp1][ap_m2][ap_p2];
                                double nv = 0.0;
                                for (int b = 0; b < 5; b++) if ((mk >> b) & 1) nv = max(nv, ht[b]);
                                w += nv - EX6[idx8];
                            }
                        }
                    }
                } else if (wl[i] == 2 && (d == 7 || d == 8)) {
                    int sm1 = S_(i - 1), s0 = sl[i];
                    int di = (d == 7) ? 0 : 1;
                    uint64_t rw = 0, rs = 0;
                    bool built_rot = false;
                    for (int sg = 0; sg < 2; sg++) {
                        int e = sg == 0 ? 1 : -1;
                        int cc = W_(i + e);
                        int a = sg == 0 ? s0 : sm1;
                        if (cc > 1 || a > 1) continue;
                        const auto &bkt = F2B_W7[di][sg][sm1 * 5 + s0];
                        if (bkt.empty()) continue;
                        if (!built_rot) {
                            for (int off = 0; off < d; off++) {
                                int p = (i + off) % d;
                                rw |= (1ULL << (5 * off + wl[p]));
                                rs |= (1ULL << (5 * off + sl[p]));
                            }
                            built_rot = true;
                        }
                        uint8_t extra = 0;
                        for (const auto &r : bkt) {
                            if (((rw & r.forb_w) | (rs & r.forb_s)) == 0) extra |= (uint8_t)r.kill_mask;
                        }
                        if (extra) {
                            int w2 = W_(i + 2 * e), w3 = W_(i + 3 * e), w4 = W_(i + 4 * e);
                            int o = sg == 0 ? sm1 : s0;
                            long qidx = ((((((long)sg * 5 + cc) * 5 + a) * 5 + w2) * 5 + w3) * 5 + w4) * 5 + o;
                            uint8_t mk0 = (d == 7) ? L3_MK0[qidx] : L8_MK0[qidx];
                            if (mk0 & extra) {
                                uint8_t mk = mk0 & ~extra;
                                const double *lp = (d == 7 ? L3PQ.data() : L8P.data()) + ((cc * 5 + a) * 5);
                                double nv = 0.0;
                                for (int b = 0; b < 5; b++) if ((mk >> b) & 1) nv = max(nv, lp[b]);
                                w += nv - (d == 7 ? L3QEX[qidx] : L8X[qidx]);
                            }
                        }
                    }
                }
            }
            if (w <= curThr()) return;
        }
        if (omax > 0 && minRing() <= omax) return;
        string link(d, '0'), s(d, '0');
        for (int i = 0; i < d; i++) { link[i] = '5' + wl[i]; s[i] = '5' + sl[i]; }
        if ((d == 7 || d == 8) && RBIG.count(canonWord(link))) return;
        vector<int> v; for (int i = 0; i < d; i++) if (vars[i] >= 0) v.push_back(vars[i]);
        if (RMODE && RMAXV > 0) for (int i = 0; i < d; i++) if (wl[i] == 1) {
            int st = wl[(i + d - 1) % d] * 25 + sl[(i + d - 1) % d] * 5 + wl[i], c = sl[i] * 5 + wl[(i + 1) % d];
            if (RA[st][c] >= 0) v.push_back(7000000 + RA[st][c]);
        }
        sort(v.begin(), v.end());
        if (HASX) {
            vector<int> tt; for (int i = 0; i < d; i++) if (wl[i] >= 2) { tt.push_back(1000000 + tin[i]); tt.push_back(2000000 + tout[i]); }
            sort(tt.begin(), tt.end()); v.push_back(-1); v.insert(v.end(), tt.begin(), tt.end());
        }
        if (ARRKEY) {
            vector<int> best_arr;
            for (int r = 0; r < d; r++) {
                vector<int> cur_arr(d);
                for (int i = 0; i < d; i++) {
                    int p = (r + i) % d;
                    cur_arr[i] = 9000000 + wl[p] * 5 + sl[p];
                }
                if (best_arr.empty() || cur_arr < best_arr) best_arr = cur_arr;
            }
            v.push_back(-2);
            v.insert(v.end(), best_arr.begin(), best_arr.end());
        }
        lock_guard<mutex> lk(found_mtx);
        if ((HASEX6 || HASR || HASL || HASL8 || HASFB) && w <= curThr()) return;
        auto it = found.find(v);
        if (it != found.end()) {
            if (w > it->second.w + 1e-12) {
                found_by_w.erase({it->second.w, v});
                it->second = Res{w, link, s, v};
                found_by_w.insert({w, v});
                updThrLocked();
            }
            return;
        }
        found[v] = Res{w, link, s, v};
        found_by_w.insert({w, v});
        if ((int)found.size() > maxout) {
            auto mi = found_by_w.begin();
            found.erase(mi->second);
            found_by_w.erase(mi);
        }
        updThrLocked();
    }

    void dfs(int i, int st, double w) {
        local_nodes++;
        if (nodelimit > 0 && (local_nodes & 4095) == 0) {
            long long tot = total_nodes.fetch_add(4096, memory_order_relaxed) + 4096;
            if (tot > nodelimit) {
                lock_guard<mutex> lk(found_mtx);
                if (!found.empty()) { aborted.store(true, memory_order_relaxed); return; }
            }
        }
        if (i == d) { if (st == a0) leaf(w); return; }
        int k = d - i;
        int wc = st % 5;
        st_hist[i] = st;
        const auto &Bnd_ref = *Bnd;

        for (int c = 0; c < 25; c++) {
            if (!AL[ui][st][c]) continue;
            int sc = c / 5, wn = c % 5;
            if (!NOSYM) {
                if (i == 0) {
                    if (sc != (min_ws % 5)) continue;
                } else {
                    if (wc * 5 + sc < min_ws) continue;
                }
            }
            int ns = wc * 25 + sc * 5 + wn;
            if (i == d - 1 && ns != a0) continue;
            if (i == d - 2 && wn != a0 / 25) continue;

            double nw = w + W[st][c];
            double b = (k - 1 == 0) ? (ns == a0 ? 0.0 : -1e18) : Bnd_ref[k - 1][ns * 125 + a0];
            if (nw + b <= curThr() + 1e-9) continue;

            c_hist[i] = c;
            sl[i] = sc;
            if (i + 1 < d) wl[i + 1] = wn;

            uint64_t old_w = cur_w, old_s = cur_s;
            if (d <= 12) {
                if (i < d - 1) cur_s |= (1ULL << (5 * i + sc));
                if (i + 1 < d - 1) cur_w |= (1ULL << (5 * (i + 1) + wn));
            }

            vars[i] = VA[ui][st][c];
            code[i] = (wc == 0) ? CO[ui][st][c] : -1;
            if (wc == 0 && forbidden(i)) { cur_w = old_w; cur_s = old_s; continue; }
            if (fullForbiddenStep(i)) { cur_w = old_w; cur_s = old_s; continue; }
            if (wc == 0 && omax > 0 && oracleHit(i)) { cur_w = old_w; cur_s = old_s; continue; }

            if (HASX) {
                for (int j : RES_X[i]) {
                    if (wl[j] >= 2) nw += contrib(j) - XREL[st_hist[j]][c_hist[j]];
                }
                if (nw + b <= curThr() + 1e-9) { cur_w = old_w; cur_s = old_s; continue; }
            }
            if (HASEX6 || HASFB) {
                for (int j : RES_EX6[i]) {
                    if (HASEX6 && wl[j] == 1) nw += exact_ex6(j) - RBEST[st_hist[j]][c_hist[j]];
                    if (HASFB) nw += exact_fb(j) - FBREL[ui][st_hist[j]][c_hist[j]];
                }
                if (nw + b <= curThr() + 1e-9) { cur_w = old_w; cur_s = old_s; continue; }
            }
            if (HASR) {
                for (int j : RES_RTAB[i]) {
                    if (sl[j] == 0) nw += exact_rtab(j) - RREL[st_hist[j]][c_hist[j]];
                }
                if (nw + b <= curThr() + 1e-9) { cur_w = old_w; cur_s = old_s; continue; }
            }
            if ((HASL && d == 7) || (HASL8 && (d == 7 || d == 8))) {
                for (int j : RES_L3Q[i]) {
                    if (HASL && d == 7 && wl[j] == 2) nw += exact_l3q7(j) - L3REL_TIGHT[st_hist[j]][c_hist[j]];
                    if (HASL8 && d == 7 && wl[j] == 3) nw += exact_l3q8_7(j) - L8REL7_TIGHT[st_hist[j]][c_hist[j]];
                    if (HASL8 && d == 8 && wl[j] == 2) nw += exact_l3q8_8(j) - L8REL8_TIGHT[st_hist[j]][c_hist[j]];
                }
                if (nw + b <= curThr() + 1e-9) { cur_w = old_w; cur_s = old_s; continue; }
            }

            dfs(i + 1, ns, nw);
            cur_w = old_w;
            cur_s = old_s;
            if (aborted.load(memory_order_relaxed)) return;
        }
    }
};

int main(int argc, char **argv) {
    initCode1Hot();
    NTHREADS = max(1u, thread::hardware_concurrency());
    if (const char *e = getenv("SEP_THREADS")) NTHREADS = max(1, atoi(e));
    if (const char *e = getenv("NOSYM")) NOSYM = atoi(e);
    if (const char *e = getenv("SEP_NODELIMIT")) nodelimit = atoll(e);
    if (const char *e = getenv("SEP_ARRKEY")) ARRKEY = atoi(e) != 0;
    if (const char *e = getenv("SEP_EXACT6")) {
        FILE *g = fopen(e, "rb"); if (!g) return 30; EX6.assign(3L * 390625, 0.0);
        if (fread(EX6.data(), sizeof(double), EX6.size(), g) != EX6.size()) return 31;
        fclose(g); HASEX6 = true;
        for (int u = 0; u < 3; u++) {
            for (int wm1 = 0; wm1 < 5; wm1++)
                for (int sm1 = 0; sm1 < 5; sm1++) {
                    int st = wm1 * 25 + sm1 * 5 + 1;
                    for (int s0 = 0; s0 < 5; s0++)
                        for (int wp1 = 0; wp1 < 5; wp1++) {
                            int c = s0 * 5 + wp1;
                            double mx = -1e18;
                            for (int wm2 = 0; wm2 < 5; wm2++)
                                for (int wp2 = 0; wp2 < 5; wp2++)
                                    for (int sm2 = 0; sm2 < 5; sm2++)
                                        for (int sp1 = 0; sp1 < 5; sp1++) {
                                            long idx = ((((((((long)u * 5 + wm2) * 5 + wm1) * 5 + wp1) * 5 + wp2) * 5 + sm2) * 5 + sm1) * 5 + s0) * 5 + sp1;
                                            if (EX6[idx] > mx) mx = EX6[idx];
                                        }
                            EX6REL[u][st][c] = mx;
                        }
                }
        }
        fprintf(stderr, "sep: exact six-window table loaded (%s)\n", e);
    }
    if (const char *e = getenv("SEP_FB6")) {
        FILE *g = fopen(e, "rb"); if (!g) return 41; FBX.assign(3L * 1953125, 0.0);
        if (fread(&FBREL[0][0][0], sizeof(double), 3 * 125 * 25, g) != 3 * 125 * 25) return 42;
        if (fread(FBX.data(), sizeof(double), FBX.size(), g) != FBX.size()) return 43;
        fclose(g); HASFB = true;
    }
    if (const char *e = getenv("SEP_L3Q")) {
        FILE *g = fopen(e, "rb"); if (!g) return 35; L3QEX.assign(31250, 0.0); L3PQ.assign(125, 0.0);
        if (fread(&L3REL[0][0], sizeof(double), 125 * 25, g) != 125 * 25) return 36;
        if (fread(L3QEX.data(), sizeof(double), 31250, g) != 31250) return 37;
        if (fread(L3PQ.data(), sizeof(double), 125, g) != 125) return 38;
        fclose(g); HASL = true;
        for (int wm1 = 0; wm1 < 5; wm1++)
            for (int sm1 = 0; sm1 < 5; sm1++) {
                int st = wm1 * 25 + sm1 * 5 + 2;
                for (int s0 = 0; s0 < 5; s0++)
                    for (int wp1 = 0; wp1 < 5; wp1++) {
                        int c = s0 * 5 + wp1;
                        double mx0 = -1e18, mx1 = -1e18;
                        for (int w2 = 0; w2 < 5; w2++)
                            for (int w3 = 0; w3 < 5; w3++) {
                                double pq0 = L3PQ[(wp1 * 5 + w2) * 5 + w3];
                                double pq1 = L3PQ[(wm1 * 5 + w2) * 5 + w3];
                                for (int w4 = 0; w4 < 5; w4++) {
                                    long q0 = (((((0L * 5 + wp1) * 5 + s0) * 5 + w2) * 5 + w3) * 5 + w4) * 5 + sm1;
                                    long q1 = (((((1L * 5 + wm1) * 5 + sm1) * 5 + w2) * 5 + w3) * 5 + w4) * 5 + s0;
                                    if (L3QEX[q0] - pq0 > mx0) mx0 = L3QEX[q0] - pq0;
                                    if (L3QEX[q1] - pq1 > mx1) mx1 = L3QEX[q1] - pq1;
                                }
                            }
                        L3REL_TIGHT[st][c] = mx0 + mx1;
                    }
            }
    }
    if (const char *e = getenv("SEP_L3Q8")) {
        FILE *g = fopen(e, "rb"); if (!g) return 45; L8X.assign(31250, 0.0); L8P.assign(125, 0.0);
        if (fread(&L8REL[0][0], sizeof(double), 125 * 25, g) != 125 * 25) return 46;
        if (fread(L8X.data(), sizeof(double), 31250, g) != 31250) return 47;
        if (fread(L8P.data(), sizeof(double), 125, g) != 125) return 48;
        fclose(g); HASL8 = true;
        for (int wm1 = 0; wm1 < 5; wm1++)
            for (int sm1 = 0; sm1 < 5; sm1++) {
                int st7 = wm1 * 25 + sm1 * 5 + 3;
                int st8 = wm1 * 25 + sm1 * 5 + 2;
                for (int s0 = 0; s0 < 5; s0++)
                    for (int wp1 = 0; wp1 < 5; wp1++) {
                        int c = s0 * 5 + wp1;
                        double mx7_0 = -1e18, mx7_1 = -1e18;
                        double mx8_0 = -1e18, mx8_1 = -1e18;
                        for (int w2 = 0; w2 < 5; w2++)
                            for (int w3 = 0; w3 < 5; w3++) {
                                double pq0 = -L8P[(wp1 * 5 + w2) * 5 + w3];
                                double pq1 = -L8P[(wm1 * 5 + w2) * 5 + w3];
                                if (pq0 > mx7_0) mx7_0 = pq0;
                                if (pq1 > mx7_1) mx7_1 = pq1;
                                for (int w4 = 0; w4 < 5; w4++) {
                                    long q0 = (((((0L * 5 + wp1) * 5 + s0) * 5 + w2) * 5 + w3) * 5 + w4) * 5 + sm1;
                                    long q1 = (((((1L * 5 + wm1) * 5 + sm1) * 5 + w2) * 5 + w3) * 5 + w4) * 5 + s0;
                                    if (L8X[q0] > mx8_0) mx8_0 = L8X[q0];
                                    if (L8X[q1] > mx8_1) mx8_1 = L8X[q1];
                                }
                            }
                        L8REL7_TIGHT[st7][c] = mx7_0 + mx7_1;
                        L8REL8_TIGHT[st8][c] = mx8_0 + mx8_1;
                    }
            }
    }
    if (const char *e = getenv("SEP_RTAB")) {
        FILE *g = fopen(e, "rb"); if (!g) return 32; REX.assign(15625, 0.0);
        if (fread(&RREL[0][0], sizeof(double), 125 * 25, g) != 125 * 25) return 33;
        if (fread(REX.data(), sizeof(double), REX.size(), g) != REX.size()) return 34;
        fclose(g); HASR = true;
        fprintf(stderr, "sep: hat-channel r table loaded (%s)\n", e);
    }
    if (const char *e = getenv("SEP_F2B")) {
        FILE *g = fopen(e, "rb"); if (!g) return 50;
        if (fread(&H2_TAB[0][0][0][0][0][0][0][0], sizeof(double), 37500, g) != 37500) return 51;
        PMASK8.assign(3L * 390625, 0); L3_MK0.assign(31250, 0); L8_MK0.assign(31250, 0);
        if (fread(PMASK8.data(), 1, PMASK8.size(), g) != PMASK8.size()) return 52;
        if (fread(L3_MK0.data(), 1, L3_MK0.size(), g) != L3_MK0.size()) return 53;
        if (fread(L8_MK0.data(), 1, L8_MK0.size(), g) != L8_MK0.size()) return 54;
        for (int u = 0; u < 3; u++) for (int b = 0; b < 25; b++) {
            uint32_t cnt = 0; if (fread(&cnt, sizeof(uint32_t), 1, g) != 1) return 55;
            F2B_W6[u][b].resize(cnt);
            if (cnt > 0 && fread(F2B_W6[u][b].data(), sizeof(F2BRule), cnt, g) != cnt) return 56;
        }
        for (int di = 0; di < 2; di++) for (int sg = 0; sg < 2; sg++) for (int b = 0; b < 25; b++) {
            uint32_t cnt = 0; if (fread(&cnt, sizeof(uint32_t), 1, g) != 1) return 57;
            F2B_W7[di][sg][b].resize(cnt);
            if (cnt > 0 && fread(F2B_W7[di][sg][b].data(), sizeof(F2BRule), cnt, g) != cnt) return 58;
        }
        fclose(g); HASF2B = true;
        fprintf(stderr, "sep: full2ball exact leaf table loaded (%s)\n", e);
    }
    FILE *f = fopen(argv[1], "r");
    if (fscanf(f, "%d", &NV) != 1) return 1;
    for (int u = 0; u < 3; u++) for (int a = 0; a < 125; a++) for (int c = 0; c < 25; c++)
        if (fscanf(f, "%d %d %d", &AL[u][a][c], &VA[u][a][c], &CO[u][a][c]) != 3) return 2;
    int nb; if (fscanf(f, "%d", &nb) != 1) return 3;
    char buf[64];
    for (int i = 0; i < nb; i++) { if (fscanf(f, "%63s", buf) != 1) return 4; RBIG.insert(canonWord(buf)); }
    int np; if (fscanf(f, "%d", &np) != 1) return 5;
    for (int i = 0; i < np; i++) {
        int dd, k; if (fscanf(f, "%d %d", &dd, &k) != 2) return 6;
        vector<pair<int,int>> P(k); for (auto &x : P) if (fscanf(f, "%d %d", &x.first, &x.second) != 2) return 7;
        addPattern(dd, P);
    }
    int nf = 0;
    if (fscanf(f, "%d", &nf) != 1) nf = 0;
    for (int i = 0; i < nf; i++) {
        int dd, k; if (fscanf(f, "%d %d", &dd, &k) != 2) return 13;
        vector<pair<int,int>> P(k); for (auto &x : P) if (fscanf(f, "%d %d", &x.first, &x.second) != 2) return 14;
        addFull(dd, P);
    }
    if (const char *e = getenv("SEP_FULLX")) {
        FILE *g = fopen(e, "r"); if (!g) return 39; int dd, k;
        while (fscanf(g, "%d %d", &dd, &k) == 2) {
            vector<pair<int,int>> P(k); for (auto &x : P) if (fscanf(g, "%d %d", &x.first, &x.second) != 2) return 40;
            addFull(dd, P); nf++;
        }
        fclose(g);
    }
    { char tb[4]; if (fscanf(f, "%3s", tb) == 1 && tb[0] == 'R') {
        RMODE = true;
        for (int u = 0; u < 3; u++) for (int a = 0; a < 125; a++) for (int c = 0; c < 25; c++)
            for (int q = 0; q < 5; q++) if (fscanf(f, "%d", &RV[u][a][c][q]) != 1) return 17;
    } }
    fclose(f);
    fprintf(stderr, "sep: 6-relay %s\n", RMODE ? "on" : "off");
    fprintf(stderr, "sep: NV=%d RBIG=%zu patterns=%d full=%d\n", NV, RBIG.size(), np, nf);
    char cmd[8];
    vector<double> y(NV);
    while (scanf("%7s", cmd) == 1) {
        if (cmd[0] == 'c') {
            char lb[40], sb[40];
            if (scanf("%d %39s %39s", &d, lb, sb) != 3) return 10;
            ui = d == 7 ? 0 : d == 8 ? 1 : 2; bool ok = true;
            auto pit = PIDX.find(d);
            CUR_PIDX = (pit != PIDX.end()) ? &(pit->second) : nullptr;
            Worker wchk;
            for (int i = 0; i < d; i++) { wchk.wl[i] = lb[i] - '5'; wchk.sl[i] = sb[i] - '5'; }
            if ((d == 7 || d == 8) && RBIG.count(canonWord(lb))) ok = false;
            for (int i = 0; i < d && ok; i++) {
                int st = wchk.wl[(i + d - 1) % d] * 25 + wchk.sl[(i + d - 1) % d] * 5 + wchk.wl[i], c = wchk.sl[i] * 5 + wchk.wl[(i + 1) % d];
                if (!AL[ui][st][c]) { ok = false; break; }
                wchk.code[i] = wchk.wl[i] == 0 ? CO[ui][st][c] : -1;
            }
            for (int i = 0; i < d && ok; i++) if (wchk.wl[i] == 0 && wchk.forbidden(i)) ok = false;
            if (ok) {
                auto fit = FULL.find(d);
                if (fit != FULL.end()) {
                    for (auto &Q : fit->second) {
                        bool fok = true;
                        for (auto [sl_, m] : Q) { int v = sl_ < d ? wchk.wl[sl_] : wchk.sl[sl_ - d]; if (!((m >> v) & 1)) { fok = false; break; } }
                        if (fok) { ok = false; break; }
                    }
                }
            }
            printf("%d\n", ok ? 1 : 0); fflush(stdout); continue;
        }
        if (scanf("%d %lf %d %d", &d, &thr, &maxout, &omax) != 4) return 8;
        for (auto &x : y) if (scanf("%lf", &x) != 1) return 9;
        ui = d == 7 ? 0 : d == 8 ? 1 : 2;
        { char xb[8]; int kx; if (scanf("%7s %d", xb, &kx) != 2 || xb[0] != 'X') return 11;
          fill(XV.begin(), XV.end(), 0.0); HASX = false;
          for (int q = 0; q < kx; q++) { int cd; double val; if (scanf("%d %lf", &cd, &val) != 2) return 12;
            if (cd >= 0 && cd < 140625 && val > 0) { XV[cd] = val; HASX = true; } } }
        if (RMODE) { char rb[8]; int k; if (scanf("%7s %d", rb, &k) != 2 || rb[0] != 'R') return 18;
            RY.assign(k, 0.0); for (auto &x : RY) if (scanf("%lf", &x) != 1) return 19; }

        buildSchedules();
        RMAXV = 0;
        for (int a = 0; a < 125; a++) {
            int wm1 = a / 25, sm1 = (a / 5) % 5, wc = a % 5;
            for (int c = 0; c < 25; c++) {
                int s0 = c / 5, wp1 = c % 5;
                W[a][c] = AL[ui][a][c] ? (VA[ui][a][c] >= 0 ? y[VA[ui][a][c]] : 0.0) : -1e18;
                RA[a][c] = -1; RBEST[a][c] = 0.0; XREL[a][c] = 0.0;
                if (!AL[ui][a][c]) continue;
                if (RMODE && wc == 1) {
                    double best = 0.0; int bv = -1;
                    for (int q = 0; q < 5; q++) { int vv = RV[ui][a][c][q]; if (vv >= 0 && RY[vv] > best + 1e-15) { best = RY[vv]; bv = vv; } }
                    RA[a][c] = bv; RMAXV = max(RMAXV, best);
                    if (HASEX6) best = EX6REL[ui][a][c];
                    W[a][c] += best; RBEST[a][c] = best;
                }
                if (HASX && wc >= 2) {
                    int lj = wc - 2;
                    double best_x = -1e18;
                    int ns_ac = wc * 25 + s0 * 5 + wp1;
                    for (int wm2 = 0; wm2 < 5; wm2++) {
                        bool ok_wm2 = false;
                        for (int sm2 = 0; sm2 < 5; sm2++) if (AL[ui][wm2 * 25 + sm2 * 5 + wm1][sm1 * 5 + wc]) { ok_wm2 = true; break; }
                        if (!ok_wm2) continue;
                        int sL_in = sidecode(wm1, sm1, wm2), sL_out = sidecode(wm1, wm2, sm1);
                        for (int wp2 = 0; wp2 < 5; wp2++) {
                            bool ok_wp2 = false;
                            for (int sp1 = 0; sp1 < 5; sp1++) if (AL[ui][ns_ac][sp1 * 5 + wp2]) { ok_wp2 = true; break; }
                            if (!ok_wp2) continue;
                            int sR_in = sidecode(wp1, s0, wp2), sR_out = sidecode(wp1, wp2, s0);
                            double vx = XV[taucode(lj, ui, sL_in, sR_in)] - XV[taucode(ui, lj, sL_out, sR_out)];
                            if (vx > best_x) best_x = vx;
                        }
                    }
                    if (best_x < -1e17) best_x = 0.0;
                    XREL[a][c] = best_x;
                    W[a][c] += best_x;
                }
                if (HASR && s0 == 0) W[a][c] += RREL[a][c];
                if (HASL && ui == 0 && d == 7 && wc == 2) W[a][c] += L3REL_TIGHT[a][c];
                if (HASL8 && ui == 0 && d == 7 && wc == 3) W[a][c] += L8REL7_TIGHT[a][c];
                if (HASL8 && ui == 1 && d == 8 && wc == 2) W[a][c] += L8REL8_TIGHT[a][c];
                if (HASFB) W[a][c] += FBREL[ui][a][c];
            }
        }

        found.clear(); found_by_w.clear(); total_nodes.store(0); CT.store(thr); aborted.store(false);
        bool anyStartR = HASX || RMAXV > 0 || HASR || (HASL && d == 7) || HASFB;

        int max_ws = NOSYM ? 1 : (anyStartR ? 25 : 5);
        vector<vector<vector<double>>> Bnd_ws(max_ws);
        struct Task { double neg_bnd; int ws_iter; int a; };
        vector<Task> tasks;

        for (int ws_iter = 0; ws_iter < max_ws; ws_iter++) {
            int min_ws = ws_iter;
            int w0_min = ws_iter / 5;
            int s0_min = ws_iter % 5;
            vector<double> M(125 * 125, -1e18);
            for (int a = 0; a < 125; a++) {
                if (!NOSYM) {
                    int wm1_ = a / 25, sm1_ = (a / 5) % 5, wc_ = a % 5;
                    if (wm1_ * 5 + sm1_ < min_ws || wc_ < w0_min) continue;
                }
                for (int c = 0; c < 25; c++) if (AL[ui][a][c]) {
                    if (!NOSYM) {
                        int sc_ = c / 5, wn_ = c % 5;
                        if ((a % 5) * 5 + sc_ < min_ws || wn_ < w0_min) continue;
                    }
                    int b = (a % 5) * 25 + (c / 5) * 5 + c % 5;
                    M[a * 125 + b] = max(M[a * 125 + b], W[a][c]);
                }
            }
            Bnd_ws[ws_iter].assign(d + 1, vector<double>());
            Bnd_ws[ws_iter][1] = M;
            for (int k = 2; k <= d; k++) {
                vector<double> P(125 * 125, -1e18);
                for (int a = 0; a < 125; a++) for (int m = 0; m < 125; m++) {
                    double x = Bnd_ws[ws_iter][k - 1][a * 125 + m]; if (x < -1e17) continue;
                    for (int b = 0; b < 125; b++) { double z = x + M[m * 125 + b]; if (z > P[a * 125 + b]) P[a * 125 + b] = z; }
                }
                Bnd_ws[ws_iter][k] = P;
            }

            for (int a = 0; a < 125; a++) {
                if (!NOSYM) {
                    if ((a % 5) != w0_min) continue;
                    if (((a / 25) * 5 + ((a / 5) % 5)) < min_ws) continue;
                } else {
                    if (!anyStartR && (a % 5) != 0) continue;
                }
                double best_start = -1e18;
                for (int wn = 0; wn < 5; wn++) {
                    int c0 = s0_min * 5 + wn;
                    if (!NOSYM) {
                        if (!AL[ui][a][c0] || wn < w0_min) continue;
                        int ns0 = w0_min * 25 + s0_min * 5 + wn;
                        double v = W[a][c0] + Bnd_ws[ws_iter][d - 1][ns0 * 125 + a];
                        if (v > best_start) best_start = v;
                    } else {
                        best_start = Bnd_ws[ws_iter][d][a * 125 + a];
                        break;
                    }
                }
                if (best_start > curThr() + 1e-9)
                    tasks.push_back({-best_start, ws_iter, a});
            }
        }
        sort(tasks.begin(), tasks.end(), [](const Task &x, const Task &y) {
            if (x.neg_bnd != y.neg_bnd) return x.neg_bnd < y.neg_bnd;
            if (x.ws_iter != y.ws_iter) return x.ws_iter < y.ws_iter;
            return x.a < y.a;
        });

        atomic<size_t> next_idx{0};
        int nt = min((int)tasks.size(), NTHREADS);
        if (nt <= 1) {
            Worker w;
            for (const auto &tk : tasks) {
                if (-tk.neg_bnd <= curThr() + 1e-9) break;
                w.min_ws = tk.ws_iter;
                w.Bnd = &Bnd_ws[tk.ws_iter];
                w.a0 = tk.a;
                w.wl[d - 1] = tk.a / 25;
                w.sl[d - 1] = (tk.a / 5) % 5;
                w.wl[0] = tk.a % 5;
                w.cur_w = (1ULL << (5 * 0 + w.wl[0])) | (1ULL << (5 * (d - 1) + w.wl[d - 1]));
                w.cur_s = (1ULL << (5 * (d - 1) + w.sl[d - 1]));
                w.dfs(0, tk.a, 0.0);
                if (aborted.load(memory_order_relaxed)) break;
            }
            total_nodes.fetch_add(w.local_nodes & 4095, memory_order_relaxed);
        } else {
            vector<thread> pool;
            pool.reserve(nt);
            for (int t = 0; t < nt; t++) {
                pool.emplace_back([&]() {
                    Worker w;
                    while (!aborted.load(memory_order_relaxed)) {
                        size_t idx = next_idx.fetch_add(1, memory_order_relaxed);
                        if (idx >= tasks.size()) break;
                        const auto &tk = tasks[idx];
                        if (-tk.neg_bnd <= curThr() + 1e-9) continue;
                        w.min_ws = tk.ws_iter;
                        w.Bnd = &Bnd_ws[tk.ws_iter];
                        w.a0 = tk.a;
                        w.wl[d - 1] = tk.a / 25;
                        w.sl[d - 1] = (tk.a / 5) % 5;
                        w.wl[0] = tk.a % 5;
                        w.cur_w = (1ULL << (5 * 0 + w.wl[0])) | (1ULL << (5 * (d - 1) + w.wl[d - 1]));
                        w.cur_s = (1ULL << (5 * (d - 1) + w.sl[d - 1]));
                        w.dfs(0, tk.a, 0.0);
                    }
                    total_nodes.fetch_add(w.local_nodes & 4095, memory_order_relaxed);
                });
            }
            for (auto &th : pool) th.join();
        }

        vector<Res> out; for (auto &kv : found) out.push_back(kv.second);
        sort(out.begin(), out.end(), [](const Res &a, const Res &b) { return a.w > b.w; });
        for (auto &r : out) {
            printf("A %.9f %s %s", r.w, r.link.c_str(), r.s.c_str());
            for (int v : r.v) printf(" %d", v);
            printf("\n");
        }
        printf("END %zu %lld %d\n", out.size(), total_nodes.load(), aborted.load() ? 1 : 0); fflush(stdout);
    }
}
