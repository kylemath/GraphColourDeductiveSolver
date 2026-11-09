// sep3r_gk8 (W17 code_gk8, 9 Nov 2026): sep3r_gk.cpp of code_gk7 plus payer-8/9 GK keys, written from W6b's PAYER8SPEC.md (W5
// reading; no Opus code). Key payer mask: a nonempty subset of {5, 6, 7}, or exactly {8}, or exactly {9}; payer-8/9 keys may not
// use S.L+-3 (positions 2, 5). gkWinVal: the IN gate is widened to every payer letter (7, 8, 9 own privates wildcard) and, at
// U = 8, 9, the centre's OUT slots (centre pays w_j, SURE on the window: sg = +1 S.L+-1 = w_{j+-1}, S.L+-2 = w_{j+-2},
// S.A+1 = s_{j+1}, S.A-1 = s_{j-2}, R.L+2 = s_j, R.L-2 = s_{j-1}; sg = -1 mirrored) are subtracted, so GKW / GKREL may be < 0.
// gkCorr: d = 7 IN loop and d >= 8 loop run over every link position. Everything else as code_gk7.
// sep3r_gk7 (swarm W17 round 5, 6 Nov 2026): sep3r_gk.cpp (md5 10f952f6) plus one opt-in flag, SEP_F2B7=1 (needs SEP_Q7M), written
// from from_opus/f2b7/SPEC.md only: at the w10Corr leaf a q7m side whose common neighbour or apex is >= 7 gets 31 & ~f2bExtra
// (group d7/d8_w7 of that side) instead of 31; the window term QREL stays unmasked, so the leaf correction stays <= 0.
// sep3r_gk (swarm W17 round 4, 6 Nov 2026): sep3r_w17.cpp (md5 b3dd58f9) plus one opt-in table, SEP_GK: W6's generic 2-ball keys
// EDGE(U->V)[...] (payer letters in {5, 6, 7}, any payee set), written from W6's KEYSPEC.md and the gkwin paragraph of Opus's
// DUAL_EXPORT.md; no Opus code. File: int32 NK, then per key int32 U, int32 V (letter bits 0..4), double amount, int32 nc,
// nc x (int32 position, int32 mask); then GKREL[3][125][25] (Python's DP window bound). At load the separator computes its own
// gkwin table GKW[U = 7, 8, 9][5^9 windows (w_{j-2..j+2}, s_{j-2..j+1})] (IN credit of the link position j, amount-weighted,
// payer 6 private = pmask, neighbour 6 private = pmask OR-ed over its two letters outside the window, 7+ privates free), takes
// its max over (w_{j-2}, w_{j+2}, s_{j-2}, s_{j+1}) and refuses to run (exit 93) if that differs from Python's GKREL by > 1e-12.
// Window: + GKREL at every link position. Leaf (gkCorr): d = 7: the KEYSPEC section 5 picture (pmask & ~f2b extra6, l3q MASK &
// ~f2b extra7 when c, a <= 6), IN slots POSSIBLE minus OUT slots (centre 7 pays) SURE; d >= 8: GKW of each position (gkwin is the
// row there, as in Opus's python rows). Every per-position IN credit above GKREL is refused at run time (exit 92). Needs SEP_F2BS.
// SEP_GKPLANT=pay|half: planted C++ errors (payer sign flipped / d = 7 payee credit halved), controls only.
// sep3r_w17 (swarm W17, 5 Nov 2026): sep3r_w15.cpp v2 (md5 c44d0529) plus one opt-in table, SEP_KS (K* and the generic
// EDGE(7->P) family, W6 grammar positions S.L+-1..3, S.A+-1, R.L+-2), written from Team D's family statement and W6's grammar.py,
// no Opus code. File: int32 NK, int32 A10G, then per key int32 P (payee letter bits 0..4), double amount, int32 nc, nc x
// (int32 grammar position index, int32 letter mask); then KSREL[3][125][25] (the payee window bound at a link 7, per centre
// class ui, amount-weighted). Window: + KSREL at every link 7 (state a % 5 == 2). Leaf (ksCorr): every payee credit is
// re-read exactly (possible count: link, apexes, l3q table & ~f2b extra7 at d = 7, pmask & ~f2b extra6 at d <= 9, others free)
// and the d = 7 payer debit (sure count, exact letters) is subtracted. Both parts are <= 0 against the window; a payee credit
// above KSREL is refused at run time (exit 81). Needs SEP_F2BS (mask tables). SEP_KSPLANT=pay|half: planted C++ errors
// (payer sign flipped / payee credit halved), controls only.
// sep3r_w15 v2 (swarm W15, 5 Nov 2026; v2 adds the POSADM counters: positive-correction leaves that pass every admissibility
// filter and exceed the threshold, i.e. would be reported, and how many of them cross only by the correction): W12's sep3r_w12.cpp (md5 b8ef0d15; SEP_BUGFIX on by default) plus SEP_PART=k/n, which
// keeps only the start states with index % n == k in the sorted start list (a partition of the search, for splitting one
// degree over several runs).
// NOCLAMP mode (coordinator 5 Nov, after Opus jsepf_nc): SEP_SLACKD="7:x,8:y,9:z" adds slack(d) to every relaxed pruning test (the
// two in-step tests, the start-state filter and the start-loop break), so an arrangement cannot be pruned on account of a positive
// f2b leaf correction (Python passes slack(d) = d * max dM+ + 2d * max dQ+ over every (mask, sub-mask) pair). Leaf values stay
// exact and unclamped. The END line gains 'POS leaves viol cross': leaves reached with a positive f2b correction, how many of
// those are reported violators, and how many are violators only because of it (exact > thr >= exact - positive part).
// sep3r_w12 (swarm W12, 5 Nov 2026): copy of W10's sep3r_w10.cpp (md5 e5d865c0) with three search-only additions:
//   SEP_CANON=1   results keyed by the rotation-canonical arrangement (one entry per rotation class; SEP_CANONREFL=1 also merges
//                 reflections). With the pruned f2b rule file the rows are NOT reflection invariant, so reflections stay apart;
//   'M n m_0..m_{n-1}' slot masks (w_k at k, s_k at d + k, bits over letters 0..4; n = 0 clears), as W1/W7 sep_ms;
//   'r thr maxout'  re-run the search of the last query (same weights, same Bnd) with a new threshold / cap / masks.
//   'S thr K'       class sweep with an exact per-link relaxed bound (5-state cycle DP), top K per class.
//   SEP_NECK=1    prune a prefix whose link already has a strictly smaller rotation (every class keeps its least-rotation form).
// BOUND FIX (on by default, SEP_BUGFIX=0 restores the old line): the first pruning test of a transition counted the big
// positions resolved at this step as already in nw ((d - NRES[i + 1]) * XINMAX) although their transfer terms are added only
// after it, so a positive x term could be pruned away (found at d = 7: 5566997 / 5696767 lost in that rotation, kept in others).
// The inherited line is in sep3x.cpp, sep3r_ak.cpp, sep3r_f2bS.cpp and sep3r_w10.cpp. Row values and leaf corrections are unchanged.
// sep3r_w10 (swarm W10, 4 Nov 2026): copy of sep3r_f2bS.cpp (md5 8d6f0b53) with three more opt-in tables, written from
// RELAY_SPEC_s22 22.1 (z / zr), 15r (rr: no change here, the Python side folds r - rr into SEP_RTAB) and the s67 q7 line:
//   SEP_ZTAB  doubles ZREL[3][125][25] (relaxed z - zr at a link five: max over the two hat classes) + ZEX[3][5^6]
//             (exact, index ((((w_{i-2}*5+w_{i-1})*5+w_{i+1})*5+w_{i+2})*25 + s_{i-1}*5 + s_i); the leaf swaps ZREL for ZEX.
//   SEP_Q7    doubles QREL[3][125][25] (unmasked payee credit Q at a link 7, exact for d >= 9) + QPAIR[3][625][25]
//             (q of A's link (U, a, b, p1, p2, c, e), -1 = RBIG completion) + QPAY[5^7] (payer total of a raw d = 7 link).
//             Leaf: at d = 7, 8 with SEP_Q7M=1 the credit is re-read over p1 in m1, p2 in m2 (l3q table masks & ~f2b extra7,
//             a side masked only when its c and apex are in {5, 6}); at d = 7 the payer total is subtracted. Both deltas <= 0.
//   Command "e d link s": the exact row value of one arrangement under the last query's weights (self-test).
#include <cstdint>
#include <functional>
// sep3r_l3q: copy of sep3r_ak.cpp with one more opt-in table, SEP_L3Q (RELAY_SPEC section 21, l3q at d = 7): a relaxed
// window term at each link 7 (the max payee credit for the two (c, a) signatures it reads) and, at the leaf, the exact
// payee credit (mask table, Qeff) and payer debit -q. Without SEP_L3Q it behaves as sep3r_ak.
// SEP_L3Q8 (s47, l3qV = 7,8; opt-in): relaxed UB8 window term at a d = 8 link 7, exact Qeff8 payee credits at the d = 8 leaf, and
// the payer debit -q8 at a d = 7 link 8 at the leaf only. Without SEP_L3Q8 nothing changes.
// sep3r_ak: copy of sep3r.cpp (frozen for Job 31) with one opt-in change, SEP_ARRKEY=1: results keyed by arrangement.
// sep3r.cpp -- Job 31 (6-relay), built from sep3x.cpp (with the Job 30 whole-arrangement patterns).
//   A link 6 at w_i of a big receiver u passes y6b[q] to u, q = the six's wheel (u, w_{i+1}, s_i, p, s_{i-1}, w_{i-1})
//   rooted at u, with the six's private p outside u's arrangement: the inflow is the maximum of y6b over the non-R6
//   p (static candidate list per transition), a per-transition constant in the bound; the argmax var enters the row
//   signature (only when the inflow is positive, so that y6b = 0 reproduces sep3x exactly).
//   Static input: after the Job 30 section, "R" + 3*125*25 lines of 5 candidate var indices (-1 = none).
//   Query: after the X section, "R k" + k values (the y6b vector).
// Build: c++ -O2 -std=c++17 -o bin/sep3r sep3r.cpp
// sep3x.cpp -- Job 29 L2: sep3 + oriented big-big transfer terms (exact branch and bound).
//   Transfer type tau of the edge u -> v (v = w_j big): (from letter, to letter, two sides unordered), letters 7,8,9 -> 0..2,
//   side = (c, vertex at 'from' with c, vertex at 'to' with c) over letters 5..9 -> 0..4, code c*25 + a*5 + b.
//   From u's arrangement: side A = (w_{j-1}, w_{j-2}, s_{j-1}), side B = (w_{j+1}, w_{j+2}, s_j) for u -> v; for v -> u the
//   'from' and 'to' vertices swap: (w_{j-1}, s_{j-1}, w_{j-2}) and (w_{j+1}, s_j, w_{j+2}).
//   tau code = ((f*3 + t)*125 + lo)*125 + hi  (lo <= hi the two side codes).  A big position j adds X[in] - X[out].
//   Query: "q d thr maxout omax" + NV y weights + "X k" + k pairs "code value".  Bound: y bound + (positions not yet
//   resolved) * max_in, where max_in = max X over tau with to = this receiver's letter (admissible: X >= 0).
//   With any X > 0 every start letter is searched (an arrangement with no 5 can be overloaded by inflow).
// Build: c++ -O2 -std=c++17 -o bin/sep3x sep3x.cpp
// (sep3 header follows)
// sep3.cpp -- Job 28: sep.cpp with full-letter sender codes (0..624, letters 5..9 base 5, slot order
//   w_{i+1}, s_i, s_{i-1}, w_{i-1}) and pattern positions carrying a letter set per slot (20-bit mask, slot t
//   = bits 5t..5t+4, t = 0 most significant digit).  Pattern input lines: "d k pos mask pos mask ...".
// Build: c++ -O2 -std=c++17 -o bin/sep3 sep3.cpp
// (original header follows)
// sep.cpp -- receiver separation for wlp2.py (exploratory).  Finds the heaviest cyclic arrangements (w_i, s_i), i < d,
// around a receiver of exact degree d that avoid every forbidden receiver-centred pattern.
// Static input (file argv[1]):
//   NV
//   for U in 7, 8, 9: 125*25 lines "allowed var code"   (state a = (wp,sp,wc) base 5, choice c = (sc,wn) base 5;
//        var = rooted-word variable index or -1 (w_c not 5), code = abstract oriented root of w_c (0..80) or -1)
//   NB  then NB lines: forbidden whole link words (RBIG, D 7-/8-wheels), digits 5..9
//   NP  then NP lines: "d k pos code pos code ..."  (one image per pattern; this program adds all dihedral images)
// Commands on stdin: "q d thr maxout" followed by NV weights.  Output: lines "A weight link s var var ..." then "END n".
// Build: c++ -O2 -std=c++17 -o bin/sep sep.cpp
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <set>
#include <map>
#include <string>
#include <algorithm>
#include <unordered_set>
#include <cmath>
using namespace std;
static int NV;
static int AL[3][125][25], VA[3][125][25], CO[3][125][25];
static set<string> RBIG;
struct Img { vector<pair<int,int>> rest; };
static map<int, vector<vector<Img>>> PIDX;   // d -> [pos*625+code] -> images whose max position is pos (rest = (pos, mask))
static int revmask(int m) {   // reverse the 4 slots
    int r = 0; for (int t = 0; t < 4; t++) r |= ((m >> (5 * t)) & 31) << (5 * (3 - t)); return r;
}
static inline bool matches(int m, int c) {   // code c (4 base-5 digits, slot 0 most significant)
    for (int t = 0; t < 4; t++) { int dg = c / (t == 0 ? 125 : t == 1 ? 25 : t == 2 ? 5 : 1) % 5; if (!((m >> (5 * t + dg)) & 1)) return false; }
    return true;
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
static int d, ui; static double thr; static int maxout;
static vector<vector<double>> Bnd;   // Bnd[k][x*125+a0]
static int wl[32], sl[32], code[32], vars[32]; static int a0;
static vector<double> XV(140625, 0.0); static double XINMAX = 0.0; static bool HASX = false;
static int RV[3][125][25][5]; static bool RMODE = false; static vector<double> RY; static int RA[125][25]; static double RMAXV = 0;
static vector<int> RES[33]; static int NRES[34];   // positions resolved at step i; NRES[i+1] = number resolved after step i
static int tin[32], tout[32];                       // tau codes per resolved big position (-1 otherwise)
static inline int sidecode(int c, int a, int b) { return c * 25 + a * 5 + b; }
static inline int taucode(int f, int t, int s1, int s2) { int lo = min(s1, s2), hi = max(s1, s2); return ((f * 3 + t) * 125 + lo) * 125 + hi; }
static void buildRes() {
    for (int i = 0; i <= d; i++) RES[i].clear();
    auto ws = [&](int k) { k = ((k % d) + d) % d; return (k == 0 || k == d - 1) ? -1 : k - 1; };
    auto ss = [&](int k) { k = ((k % d) + d) % d; return (k == d - 1) ? -1 : k; };
    for (int j = 0; j < d; j++) {
        int r = max({ws(j - 2), ws(j - 1), ws(j), ws(j + 1), ws(j + 2), ss(j - 1), ss(j)});
        RES[max(r, 0)].push_back(j);
    }
    NRES[0] = 0; for (int i = 0; i < d; i++) NRES[i + 1] = NRES[i] + (int)RES[i].size();
}
static inline double contrib(int j) {
    tin[j] = tout[j] = -1;
    int wj = wl[j]; if (wj < 2) return 0.0;
    auto W_ = [&](int k) { return wl[((k % d) + d) % d]; }; auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
    int lj = wj - 2;
    int to1 = taucode(ui, lj, sidecode(W_(j - 1), W_(j - 2), S_(j - 1)), sidecode(W_(j + 1), W_(j + 2), S_(j)));
    int ti1 = taucode(lj, ui, sidecode(W_(j - 1), S_(j - 1), W_(j - 2)), sidecode(W_(j + 1), S_(j), W_(j + 2)));
    tout[j] = to1; tin[j] = ti1;
    return XV[ti1] - XV[to1];
}
struct Res { double w; string link, s; vector<int> v; };
static map<vector<int>, Res> found;
static bool ARRKEY = false;
static int PART_K = 0, PART_N = 1;   // W15
static double SLACKD[64] = {0}; static double SLACK = 0.0; static double F2POS = 0.0; static long long POSLEAF = 0, POSVIOL = 0, POSCROSS = 0, POSADM = 0, POSADMX = 0;   // W15 NOCLAMP (POSADM*: after the admissibility filters)
static bool CANONKEY = false; static bool CANONREFL = false; static bool BUGFIX = true; static bool NECK = false; static int DEC[64]; static bool HASM = false; static int MK[64]; static bool anyStartR = false;   // W12
static double RBEST[125][25];   // relaxed six value used in W at (state, c)
static vector<double> EX6;        // SEP_EXACT6: exact six-window values [ui][wm2][wm1][wp1][wp2][sm2][sm1][s0][sp1] (letters 0..4)
static bool HASEX6 = false;
static double RREL[125][25];   // SEP_RTAB (stage 18 hat channel): relaxed r term at an apex five s_i (max over w_{i+2}, s_{i+1})
static vector<double> REX;     // exact r term [w_{i-1}][w_i][w_{i+1}][w_{i+2}][s_{i-1}][s_{i+1}] (letters 0..4)
static bool HASR = false;
static bool HASFB = false; static double FBREL[3][125][25]; static vector<double> FBX;   // SEP_FB6 (RELAY_SPEC s44): relaxed fb window term [ui][state][c]; exact [ui][a][b][c][e][f][p][q][r][s]
static bool HASL8 = false; static double L8REL[125][25]; static vector<double> L8X, L8P;   // SEP_L3Q8 (s47, l3qV = 8): relaxed d = 8 term at a link 7 [state][c]; exact payee Qeff8 [sigma][c][a][w2][w3][w4][o]; payer q8[c][a][a2] (d = 7 at a link 8)
static bool HASL = false; static double L3REL[125][25]; static vector<double> L3QEX, L3PQ;   // SEP_L3Q: relaxed term [state][c]; exact payee [sigma][c][a][w2][w3][w4][o]; payer q[c][a][a2]   // sep3r_ak (s12r_check.py): key results by arrangement, not by row (env SEP_ARRKEY=1)
static long long nodes;
// f2b041 (Studio, 31 Oct): opt-in full-2-ball private-letter shrink (env SEP_F2BS, tables from st21_check_f2b.py). Leaf only,
// after every other exact term: at a link 6 (d <= 9) the M credit is re-read at pmask & ~extra, at a link 7 payee (d = 7: V7,
// d = 8: V8) the Qeff credit at mask & ~extra. Every delta is <= 0 (checked in Python: MT and QF monotone), so the relaxed
// pruning bound stays valid and the search stays exhaustive. Rule match: rotated word bits (5*off + letter), forbidden sets.
struct F2R { uint64_t fw, fs, m; };
static bool HASF2B = false;
static vector<double> F2MT, F2QF7, F2QF8;            // MT[ui][wp1][s0][sm1][wm1][apP][apM][32]; QF[c][a][32]
static vector<uint8_t> F2PM, F2MK7, F2MK8;           // pmask by EX6 index; l3q / V8 masks by L3QEX index
static vector<F2R> F2G[7][25];                       // groups w6 d7,d8,d9; w7 d7+,d7-,d8+,d8-; bucket sm1*5+s0
static uint8_t f2bExtra(int g, int i) {
    auto &B = F2G[g][sl[(i + d - 1) % d] * 5 + sl[i]]; if (B.empty()) return 0;
    uint64_t rw = 0, rs = 0;
    for (int o = 0; o < d; o++) { int p = (i + o) % d; rw |= 1ULL << (5 * o + wl[p]); rs |= 1ULL << (5 * o + sl[p]); }
    uint8_t e = 0; for (auto &r : B) if (!((rw & r.fw) | (rs & r.fs))) e |= (uint8_t)r.m;
    return e;
}
static double f2bDelta() {
    if (!HASF2B || d > 9) return 0.0;
    auto W_ = [&](int k) { return wl[((k % d) + d) % d]; }; auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
    double dw = 0.0;
    for (int i = 0; i < d; i++) {
        if (wl[i] == 1) {
            uint8_t ex = f2bExtra(d - 7, i); if (!ex) continue;
            long idx = ((((((((long)ui * 5 + W_(i - 2)) * 5 + W_(i - 1)) * 5 + W_(i + 1)) * 5 + W_(i + 2)) * 5 + S_(i - 2)) * 5 + S_(i - 1)) * 5 + S_(i)) * 5 + S_(i + 1);
            int m0 = F2PM[idx]; if (!(m0 & ex)) continue;
            long b = (((((((long)ui * 5 + W_(i + 1)) * 5 + S_(i)) * 5 + S_(i - 1)) * 5 + W_(i - 1)) * 2 + (W_(i + 2) >= 2)) * 2 + (W_(i - 2) >= 2)) * 32;
            { double dd_ = F2MT[b + (m0 & ~ex)] - F2MT[b + m0]; dw += dd_; if (dd_ > 0) F2POS += dd_; }   // W15: positive part tracked
        } else if (wl[i] == 2 && ((d == 7 && HASL) || (d == 8 && HASL8))) {
            for (int sg = 0; sg < 2; sg++) {
                int e = sg == 0 ? 1 : -1;
                int cc = W_(i + e), a = sg == 0 ? S_(i) : S_(i - 1), o = sg == 0 ? S_(i - 1) : S_(i);
                if (cc > 1 || a > 1) continue;
                uint8_t ex = f2bExtra(3 + (d - 7) * 2 + sg, i); if (!ex) continue;
                long q = ((((((long)sg * 5 + cc) * 5 + a) * 5 + W_(i + 2 * e)) * 5 + W_(i + 3 * e)) * 5 + W_(i + 4 * e)) * 5 + o;
                int m0 = (d == 7 ? F2MK7 : F2MK8)[q]; if (!(m0 & ex)) continue;
                const double *qf = (d == 7 ? F2QF7 : F2QF8).data() + (cc * 5 + a) * 32;
                { double dd_ = qf[m0 & ~ex] - qf[m0]; dw += dd_; if (dd_ > 0) F2POS += dd_; }   // W15: positive part tracked
            }
        }
    }
    return dw;
}
static bool HASZ = false; static double ZREL[3][125][25]; static vector<double> ZEX;   // W10 z / zr
static bool HASQ7 = false, Q7MASK = false, F2B7 = false; static double QREL[3][125][25]; static vector<double> QPAIR, QPAY; static double QMAXU[3] = {0, 0, 0};   // W10 q7
static double w10Corr() {   // W10 leaf corrections (each <= 0 against the window terms)
    if (!HASZ && !HASQ7) return 0.0;
    auto W_ = [&](int k) { return wl[((k % d) + d) % d]; }; auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
    double dw = 0.0;
    for (int i = 0; i < d; i++) {
        int st = W_(i - 1) * 25 + S_(i - 1) * 5 + wl[i], c = S_(i) * 5 + W_(i + 1);
        if (HASZ && wl[i] == 0) {
            long idx = (long)ui * 15625 + ((((long)W_(i - 2) * 5 + W_(i - 1)) * 5 + W_(i + 1)) * 5 + W_(i + 2)) * 25 + S_(i - 1) * 5 + S_(i);
            dw += ZEX[idx] - ZREL[ui][st][c];
        }
        if (HASQ7 && wl[i] == 2 && Q7MASK && (d == 7 || d == 8)) {
            int m[2];
            for (int sg = 0; sg < 2; sg++) {
                int e = sg == 0 ? 1 : -1;
                int cc = W_(i + e), a = sg == 0 ? S_(i) : S_(i - 1), o = sg == 0 ? S_(i - 1) : S_(i);
                if (cc > 1 || a > 1) { m[sg] = F2B7 ? (31 & ~f2bExtra(3 + (d - 7) * 2 + sg, i) & 31) : 31; continue; }   // W17 r5: f2b7 7-side
                long q = ((((((long)sg * 5 + cc) * 5 + a) * 5 + W_(i + 2 * e)) * 5 + W_(i + 3 * e)) * 5 + W_(i + 4 * e)) * 5 + o;
                m[sg] = (d == 7 ? F2MK7 : F2MK8)[q] & ~f2bExtra(3 + (d - 7) * 2 + sg, i) & 31;
            }
            long base = ((long)ui * 625 + ((W_(i + 1) * 5 + S_(i)) * 5 + S_(i - 1)) * 5 + W_(i - 1)) * 25;
            double qm = 0.0;
            for (int p1 = 0; p1 < 5; p1++) if ((m[0] >> p1) & 1) for (int p2 = 0; p2 < 5; p2++) if ((m[1] >> p2) & 1) {
                double v = QPAIR[base + p1 * 5 + p2]; if (v > qm) qm = v; }
            dw += qm - QREL[ui][st][c];
        }
    }
    if (HASQ7 && d == 7) { long idx = 0; for (int i = 0; i < 7; i++) idx = idx * 5 + wl[i]; dw -= QPAY[idx]; }
    return dw;
}

// ---- W17: K* / EDGE(7->P) (SEP_KS) ----
struct KSKey { int P; double a; int nc; int pos[16]; int msk[16]; };
static bool HASKS = false, KSA10G = false; static int KSPLANT = 0; static vector<KSKey> KSK;
static double KSREL[3][125][25]; static double KSMAXU[3] = {0, 0, 0};
static inline int ksW(int k) { return wl[((k % d) + d) % d]; }
static inline int ksS(int k) { return sl[((k % d) + d) % d]; }
static inline int ksAB(int a, int b) {   // apex between consecutive link positions a and b = a +- 1
    a = ((a % d) + d) % d; b = ((b % d) + d) % d; return (b == (a + 1) % d) ? sl[a] : sl[b];
}
static inline int ksPayerLetter(int pi, int j, int sg) {   // d = 7 payer centre, payee w_j, S.L+1 = w_{j+sg}
    switch (pi) {
        case 0: return ksW(j + sg);  case 1: return ksW(j + 2 * sg);  case 2: return ksW(j + 3 * sg);
        case 3: return ksW(j - sg);  case 4: return ksW(j - 2 * sg);  case 5: return ksW(j - 3 * sg);
        case 6: return ksAB(j + sg, j + 2 * sg);  case 7: return ksAB(j - sg, j - 2 * sg);
        case 8: return ksAB(j, j + sg);  case 10: return ksAB(j, j - sg);
    }
    fprintf(stderr, "sep: KS bad position %d\n", pi); exit(82);
}
static inline int ksPriv7(int j, int sg) {   // the payer 7's private next to ab(j, j+sg): l3q table & ~extra7 at d = 7 when c, a <= 6
    if (d != 7) return 31;
    int c = ksW(j + sg), a = ksAB(j, j + sg), o = ksAB(j, j - sg);
    if (c > 1 || a > 1) return 31;
    int si = sg == 1 ? 0 : 1, jj = ((j % d) + d) % d;
    long q = ((((((long)si * 5 + c) * 5 + a) * 5 + ksW(j + 2 * sg)) * 5 + ksW(j + 3 * sg)) * 5 + ksW(j + 4 * sg)) * 5 + o;
    return F2MK7[q] & ~f2bExtra(3 + si, jj) & 31;
}
static inline int ksPriv6(int k) {   // the private of the link 6 at k: pmask & ~extra6 (extra6 at d <= 9)
    if (KSA10G && d >= 10) return 31;
    long idx = ((((((((long)ui * 5 + ksW(k - 2)) * 5 + ksW(k - 1)) * 5 + ksW(k + 1)) * 5 + ksW(k + 2)) * 5 + ksS(k - 2)) * 5 + ksS(k - 1)) * 5 + ksS(k)) * 5 + ksS(k + 1);
    int m = F2PM[idx];
    if (d <= 9) m &= ~f2bExtra(d - 7, ((k % d) + d) % d);
    return m & 31;
}
static inline int ksFar(int j, int e) {   // w_k's link vertex next to ab(j, k), other than w_j (k = j + e)
    int k = j + e, wk = ksW(k);
    if (wk == 0) return 1 << ksAB(k, k + e);
    if (wk == 1) return ksPriv6(k);
    return 31;
}
static inline int ksPayeeSet(int pi, int j, int e) {   // payee centre, payer w_j = 7, S.L+1 = w_{j+e}
    switch (pi) {
        case 0: return 1 << ksW(j + e);  case 3: return 1 << ksW(j - e);
        case 1: return 1 << ksAB(j, j + e);  case 4: return 1 << ksAB(j, j - e);
        case 2: return ksPriv7(j, e);  case 5: return ksPriv7(j, -e);
        case 6: return ksFar(j, e);  case 7: return ksFar(j, -e);
        case 8: return 1 << ksW(j + 2 * e);  case 10: return 1 << ksW(j - 2 * e);
    }
    fprintf(stderr, "sep: KS bad position %d\n", pi); exit(82);
}
static double ksCorr() {   // leaf: exact payee credits minus the window bound, minus the d = 7 payer debits; <= 0
    if (!HASKS) return 0.0;
    double dw = 0.0; int U = ui + 2;   // centre letter index (7 -> 2, 8 -> 3, 9+ -> 4)
    for (int j = 0; j < d; j++) if (wl[j] == 2) {
        int st = ksW(j - 1) * 25 + ksS(j - 1) * 5 + 2, c = ksS(j) * 5 + ksW(j + 1);
        double ex = 0.0;
        for (auto &k : KSK) {
            if (!((k.P >> U) & 1)) continue;
            for (int e = 1; e >= -1; e -= 2) {
                bool ok = true;
                for (int t = 0; t < k.nc && ok; t++) ok = (ksPayeeSet(k.pos[t], j, e) & k.msk[t]) != 0;
                if (ok) ex += k.a;
            }
        }
        if (KSPLANT == 2) ex *= 0.5;   // planted control: payee credit halved
        if (ex > KSREL[ui][st][c] + 1e-12) {
            string lk(d, '0'), sw(d, '0'); for (int i = 0; i < d; i++) { lk[i] = '5' + wl[i]; sw[i] = '5' + sl[i]; }
            fprintf(stderr, "sep: KS BOUND VIOLATED d=%d %s %s j=%d exact %.15g > window %.15g\n", d, lk.c_str(), sw.c_str(), j, ex, KSREL[ui][st][c]);
            fflush(stderr); exit(81);
        }
        dw += ex - KSREL[ui][st][c];
    }
    if (d == 7) for (int j = 0; j < d; j++) for (auto &k : KSK) {
        if (!((k.P >> wl[j]) & 1)) continue;
        for (int sg = 1; sg >= -1; sg -= 2) {
            bool ok = true;
            for (int t = 0; t < k.nc && ok; t++) ok = (k.msk[t] >> ksPayerLetter(k.pos[t], j, sg)) & 1;
            if (ok) dw += KSPLANT == 1 ? k.a : -k.a;   // planted control 'pay': payer sign flipped
        }
    }
    return dw;
}

// ---- W17 round 4: generic 2-ball keys (SEP_GK) ----
struct GKKey { int U, V; double a; int nc; int pos[16]; int msk[16]; };
static bool HASGK = false; static int GKPLANT = 0; static vector<GKKey> GKK;
static double GKREL[3][125][25]; static double GKMAXU[3] = {0, 0, 0};
static vector<double> GKW; static const long GKN9 = 1953125;
static inline int gkPM(int u, int a, int b, int c, int e, int f, int g, int h, int k) {
    return F2PM[((((((((long)u * 5 + a) * 5 + b) * 5 + c) * 5 + e) * 5 + f) * 5 + g) * 5 + h) * 5 + k] & 31;
}
static double gkWinVal(int u, int wm2, int wm1, int w0, int wp1, int wp2, int sm2, int sm1, int s0, int sp1) {
    int U = u + 2, pvp, pvm, fp, fm;   // code_gk8: no payer gate (w0 = 8, 9 take the payer-7 branch: own privates wildcard)
    if (w0 == 0) { pvp = 1 << sm1; pvm = 1 << s0; }
    else if (w0 == 1) { pvp = pvm = gkPM(u, wm2, wm1, wp1, wp2, sm2, sm1, s0, sp1); }
    else { pvp = pvm = 31; }
    if (wp1 == 0) fp = 1 << sp1;
    else if (wp1 == 1) { fp = 0; for (int x = 0; x < 5; x++) for (int y = 0; y < 5; y++) fp |= gkPM(u, wm1, w0, wp2, x, sm1, s0, sp1, y); }
    else fp = 31;
    if (wm1 == 0) fm = 1 << sm2;
    else if (wm1 == 1) { fm = 0; for (int x = 0; x < 5; x++) for (int y = 0; y < 5; y++) fm |= gkPM(u, x, wm2, w0, wp1, y, sm2, sm1, s0); }
    else fm = 31;
    int vp[11] = {1 << wp1, 1 << s0, pvp, 1 << wm1, 1 << sm1, pvm, fp, fm, 1 << wp2, 0, 1 << wm2};
    int vm[11] = {1 << wm1, 1 << sm1, pvm, 1 << wp1, 1 << s0, pvp, fm, fp, 1 << wm2, 0, 1 << wp2};
    double v = 0.0;
    for (auto &k : GKK) {
        if (k.a == 0.0 || !((k.U >> w0) & 1) || !((k.V >> U) & 1)) continue;
        bool op = true, om = true;
        for (int t = 0; t < k.nc; t++) { op = op && (vp[k.pos[t]] & k.msk[t]); om = om && (vm[k.pos[t]] & k.msk[t]); }
        v += k.a * ((op ? 1 : 0) + (om ? 1 : 0));
    }
    if (u >= 1) {   // code_gk8 (PAYER8SPEC 3.1): OUT, the centre U (8 or 9) pays w_j; SURE match on the window; S.L+-3 wildcard
        int qp[11] = {1 << wp1, 1 << wp2, 31, 1 << wm1, 1 << wm2, 31, 1 << sp1, 1 << sm2, 1 << s0, 0, 1 << sm1};
        int qm[11] = {1 << wm1, 1 << wm2, 31, 1 << wp1, 1 << wp2, 31, 1 << sm2, 1 << sp1, 1 << sm1, 0, 1 << s0};
        for (auto &k : GKK) {
            if (k.a == 0.0 || ((1 << U) & ~k.U) || ((1 << w0) & ~k.V)) continue;
            bool op = true, om = true;
            for (int t = 0; t < k.nc; t++) { op = op && !(qp[k.pos[t]] & ~k.msk[t]); om = om && !(qm[k.pos[t]] & ~k.msk[t]); }
            v -= k.a * ((op ? 1 : 0) + (om ? 1 : 0));
        }
    }
    return v;
}
static inline long gkIdx(int j) {
    return ((((((((long)ksW(j - 2) * 5 + ksW(j - 1)) * 5 + ksW(j)) * 5 + ksW(j + 1)) * 5 + ksW(j + 2)) * 5 + ksS(j - 2)) * 5 + ksS(j - 1)) * 5 + ksS(j)) * 5 + ksS(j + 1);
}
static double gkCorr() {   // leaf: exact credit (d = 7 picture; gkwin at d >= 8) minus the window bound GKREL; <= 0
    if (!HASGK) return 0.0;
    double dw = 0.0;
    if (d == 7) {
        int p6c[8], p7c[8][2]; for (int i = 0; i < 8; i++) p6c[i] = p7c[i][0] = p7c[i][1] = -1;
        auto PV = [&](int k, int f) -> int {   // the private of w_k next to ab(k, k + f) in the KEYSPEC d = 7 picture
            k = ((k % d) + d) % d; int x = wl[k];
            if (x == 0) return 1 << ksAB(k, k - f);
            if (x == 1) { if (p6c[k] < 0) p6c[k] = ksPriv6(k); return p6c[k]; }
            if (x == 2) { int si = f == 1 ? 0 : 1; if (p7c[k][si] < 0) p7c[k][si] = ksPriv7(k, f); return p7c[k][si]; }
            return 31;
        };
        for (int j = 0; j < d; j++) {   // code_gk8: every link position (payers 8 / 9 too)
            int st = ksW(j - 1) * 25 + ksS(j - 1) * 5 + wl[j], c = ksS(j) * 5 + ksW(j + 1);
            double rel = GKREL[0][st][c], ex = 0.0;
            if (GKW[gkIdx(j)] > 0.0) {   // the d = 7 picture's sets lie inside the window's: a window count of 0 means no match
                for (int e = 1; e >= -1; e -= 2) {
                    int v[11] = {1 << ksW(j + e), 1 << ksAB(j, j + e), PV(j, e), 1 << ksW(j - e), 1 << ksAB(j, j - e), PV(j, -e),
                                 PV(j + e, -e), PV(j - e, e), 1 << ksW(j + 2 * e), 0, 1 << ksW(j - 2 * e)};
                    for (auto &k : GKK) {
                        if (k.a == 0.0 || !((k.U >> wl[j]) & 1) || !((k.V >> 2) & 1)) continue;
                        bool ok = true;
                        for (int t = 0; t < k.nc && ok; t++) ok = (v[k.pos[t]] & k.msk[t]) != 0;
                        if (ok) ex += k.a;
                    }
                }
            }
            if (GKPLANT == 2) ex *= 0.5;   // planted control: payee credit halved
            if (ex > rel + 1e-12) {
                string lk(d, '0'), sw(d, '0'); for (int i = 0; i < d; i++) { lk[i] = '5' + wl[i]; sw[i] = '5' + sl[i]; }
                fprintf(stderr, "sep: GK BOUND VIOLATED d=%d %s %s j=%d exact %.15g > window %.15g\n", d, lk.c_str(), sw.c_str(), j, ex, rel);
                fflush(stderr); exit(92);
            }
            dw += ex - rel;
        }
        for (int j = 0; j < d; j++) for (int sg = 1; sg >= -1; sg -= 2) {   // OUT: the centre 7 pays w_j, SURE on exact letters
            int v[11] = {1 << ksW(j + sg), 1 << ksW(j + 2 * sg), 1 << ksW(j + 3 * sg), 1 << ksW(j - sg), 1 << ksW(j - 2 * sg), 1 << ksW(j - 3 * sg),
                         1 << ksAB(j + sg, j + 2 * sg), 1 << ksAB(j - sg, j - 2 * sg), 1 << ksAB(j, j + sg), 0, 1 << ksAB(j, j - sg)};
            for (auto &k : GKK) {
                if (k.a == 0.0 || !((k.U >> 2) & 1) || !((k.V >> wl[j]) & 1)) continue;
                bool ok = true;
                for (int t = 0; t < k.nc && ok; t++) ok = (v[k.pos[t]] & ~k.msk[t]) == 0;
                if (ok) dw += GKPLANT == 1 ? k.a : -k.a;   // planted control 'pay': payer sign flipped
            }
        }
    } else {
        for (int j = 0; j < d; j++) {   // code_gk8: every link position (payer 8 / 9 IN, centre OUT)
            int st = ksW(j - 1) * 25 + ksS(j - 1) * 5 + wl[j], c = ksS(j) * 5 + ksW(j + 1);
            double v = GKW[(long)ui * GKN9 + gkIdx(j)], rel = GKREL[ui][st][c];
            if (v > rel + 1e-12) { fprintf(stderr, "sep: GK WINDOW ABOVE BOUND d=%d j=%d %.15g > %.15g\n", d, j, v, rel); fflush(stderr); exit(92); }
            dw += v - rel;
        }
    }
    return dw;
}
static string canonWord(const string &w) {
    string best = w; int n = w.size();
    for (int refl = 0; refl < 2; refl++) {
        string s = w; if (refl) reverse(s.begin(), s.end());
        for (int k = 0; k < n; k++) { string t = s.substr(k) + s.substr(0, k); if (t < best) best = t; }
    }
    return best;
}
static double CT;
static double curThr() { return CT; }
static void updThr() {
    if ((int)found.size() < maxout) { CT = thr; return; }
    double m = 1e18; for (auto &kv : found) m = min(m, kv.second.w); CT = max(thr, m);
}
static int omax = 0;
// min over sender subsets S (|S| >= 2) of the ring size of the configuration u + S + their links (B = 7,8,9 free),
// by Euler: r = d + sum_j term_j (simple ring assumed; checked against every built pairs/pairs2 configuration)
static inline int termj(int j, const int *x) {   // x indexed cyclically by position
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
static int minRing() {
    int ns = 0; for (int j = 0; j < d; j++) ns += wl[j] == 0;
    if (ns < 2) return 1000;
    if (ns <= 12) {   // brute force over subsets (exact)
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
    return 0;     // >12 senders: treat as forbidden (optimistic for the oracle)
}
static int ringOf(const vector<int> &S) {
    int x[32]; for (int j = 0; j < d; j++) x[j] = 0;
    for (int p : S) x[p] = 1;
    int r = d; for (int j = 0; j < d; j++) r += termj(j, x);
    return r;
}
// incremental oracle check at step i (sender i's root just completed; senders < i complete): pairs and triples with i
static bool oracleHit(int i) {
    vector<int> P; for (int p = 0; p < i; p++) if (wl[p] == 0) P.push_back(p);
    for (size_t a = 0; a < P.size(); a++) {
        if (ringOf({P[a], i}) <= omax) return true;
        for (size_t b = a + 1; b < P.size(); b++) if (ringOf({P[a], P[b], i}) <= omax) return true;
    }
    return false;
}
// Job 30: whole-arrangement patterns. A slot is w_i (index i) or s_i (index d + i); a 5-bit letter set (bit v-5) per
// constrained slot. All dihedral images are stored; an arrangement is forbidden when some image matches every slot.
// Checked at the leaf on the complete (w, s) word, so letters on slots that no 5-sender reads can be stated. Rows are
// still deduplicated by their variable (and transfer) signature, so a row survives iff some filling of it is free.
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
static bool fullForbidden() {
    auto it = FULL.find(d); if (it == FULL.end()) return false;
    for (auto &Q : it->second) {
        bool ok = true;
        for (auto [sl_, m] : Q) { int v = sl_ < d ? wl[sl_] : sl[sl_ - d]; if (!((m >> v) & 1)) { ok = false; break; } }
        if (ok) return true;
    }
    return false;
}
static double exactCorr() {   // W10 refactor: every leaf correction of sep3r_f2bS (unchanged) + w10Corr, as one delta
    double w = 0.0;
    if (HASEX6) {   // swap each link 6's relaxed value for the exact window value (st16 check); report only exact violators
        for (int i = 0; i < d; i++) if (wl[i] == 1) {
            auto W_ = [&](int k) { return wl[((k % d) + d) % d]; }; auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
            int st = W_(i - 1) * 25 + S_(i - 1) * 5 + 1, c = S_(i) * 5 + W_(i + 1);
            long idx = ((((((((long)ui * 5 + W_(i - 2)) * 5 + W_(i - 1)) * 5 + W_(i + 1)) * 5 + W_(i + 2)) * 5 + S_(i - 2)) * 5 + S_(i - 1)) * 5 + S_(i)) * 5 + S_(i + 1);
            w += EX6[idx] - RBEST[st][c];
        }
    }
    if (HASR) {     // stage 18: swap each apex five's relaxed r term for the exact one
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; }; auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
        for (int i = 0; i < d; i++) if (sl[i] == 0) {
            int st = W_(i - 1) * 25 + S_(i - 1) * 5 + W_(i), c = 0 * 5 + W_(i + 1);
            long idx = ((((long)W_(i - 1) * 5 + W_(i)) * 5 + W_(i + 1)) * 5 + W_(i + 2)) * 25 + S_(i - 1) * 5 + S_(i + 1);
            w += REX[idx] - RREL[st][c];
        }
    }
    if (HASL && d == 7) {   // section 21: swap each link 7's relaxed l3q term for the exact payee credits minus payer debits
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; }; auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
        for (int i = 0; i < d; i++) if (wl[i] == 2) {
            int st = W_(i - 1) * 25 + S_(i - 1) * 5 + 2, c = S_(i) * 5 + W_(i + 1);
            w -= L3REL[st][c];
            for (int sg = 0; sg < 2; sg++) {
                int e = sg == 0 ? 1 : -1;
                int cc = W_(i + e), a = sg == 0 ? S_(i) : S_(i - 1), o = sg == 0 ? S_(i - 1) : S_(i);
                long q = (((((long)sg * 5 + cc) * 5 + a) * 5 + W_(i + 2 * e)) * 5 + W_(i + 3 * e)) * 5 + W_(i + 4 * e);
                w += L3QEX[q * 5 + o];
                w -= L3PQ[(W_(i + e) * 5 + W_(i + 2 * e)) * 5 + W_(i + 3 * e)];
            }
        }
    }
    if (HASL8 && d == 8) {   // s47 (iii): swap each link 7's relaxed V = 8 term for the exact payee credits Qeff8 (indices mod 8)
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; }; auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
        for (int i = 0; i < d; i++) if (wl[i] == 2) {
            int st = W_(i - 1) * 25 + S_(i - 1) * 5 + 2, c = S_(i) * 5 + W_(i + 1);
            w -= L8REL[st][c];
            for (int sg = 0; sg < 2; sg++) {
                int e = sg == 0 ? 1 : -1;
                int cc = W_(i + e), a = sg == 0 ? S_(i) : S_(i - 1), o = sg == 0 ? S_(i - 1) : S_(i);
                long q = (((((long)sg * 5 + cc) * 5 + a) * 5 + W_(i + 2 * e)) * 5 + W_(i + 3 * e)) * 5 + W_(i + 4 * e);
                w += L8X[q * 5 + o];
            }
        }
    }
    if (HASL8 && d == 7) {   // s47 (iii): d = 7 payer debit at every link 8, leaf only (not in the window: it is <= 0)
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; };
        for (int i = 0; i < d; i++) if (wl[i] == 3)
            for (int sg = 0; sg < 2; sg++) { int e = sg == 0 ? 1 : -1; w -= L8P[(W_(i + e) * 5 + W_(i + 2 * e)) * 5 + W_(i + 3 * e)]; }
    }
    if (HASFB) {   // s44: swap each position's relaxed fb term for the exact window term
        auto W_ = [&](int k) { return wl[((k % d) + d) % d]; }; auto S_ = [&](int k) { return sl[((k % d) + d) % d]; };
        for (int i = 0; i < d; i++) {
            int st = W_(i - 1) * 25 + S_(i - 1) * 5 + W_(i), c = S_(i) * 5 + W_(i + 1);
            long idx = ((((((((((long)ui * 5 + W_(i - 2)) * 5 + W_(i - 1)) * 5 + W_(i)) * 5 + W_(i + 1)) * 5 + W_(i + 2)) * 5 + S_(i - 2)) * 5 + S_(i - 1)) * 5 + S_(i)) * 5 + S_(i + 1));
            w += FBX[idx] - FBREL[ui][st][c];
        }
    }
    w += f2bDelta();   // f2b041 (0 when SEP_F2BS is unset)
    w += w10Corr();    // W10 (0 when SEP_ZTAB / SEP_Q7 are unset)
    w += ksCorr();     // W17 (0 when SEP_KS is unset)
    w += gkCorr();     // W17 round 4 (0 when SEP_GK is unset)
    return w;
}
static void leaf(double w) {
    F2POS = 0.0;
    w += exactCorr();
    if (F2POS > 1e-15) { POSLEAF++; if (w > thr) { POSVIOL++; if (w - F2POS <= thr) POSCROSS++; } }   // W15 NOCLAMP counters
    if ((HASEX6 || HASR || HASL || HASL8 || HASFB || HASF2B || HASZ || HASQ7 || HASKS || HASGK) && w <= thr) return;
    if (omax > 0 && minRing() <= omax) return;
    if (fullForbidden()) return;
    string link(d, '0'), s(d, '0');
    for (int i = 0; i < d; i++) { link[i] = '5' + wl[i]; s[i] = '5' + sl[i]; }
    if ((d == 7 || d == 8) && RBIG.count(canonWord(link))) return;
    vector<int> v;
    if (CANONKEY) {   // W12: one entry per dihedral class
        int bw[64], bs[64]; bool have = false;
        for (int r = 0; r < d; r++) for (int f = 0; f < (CANONREFL ? 2 : 1); f++) {   // W12: rotations only by default (rows need not be reflection invariant)
            int cw[64], cs[64];
            for (int i = 0; i < d; i++) { cw[i] = f ? wl[((r - i) % d + d) % d] : wl[(i + r) % d]; cs[i] = f ? sl[((r - i - 1) % d + 2 * d) % d] : sl[(i + r) % d]; }
            bool lt = !have;
            if (have) { for (int i = 0; i < 2 * d; i++) { int a_ = i < d ? cw[i] : cs[i - d], b_ = i < d ? bw[i] : bs[i - d]; if (a_ != b_) { lt = a_ < b_; break; } } }
            if (lt) { have = true; for (int i = 0; i < d; i++) { bw[i] = cw[i]; bs[i] = cs[i]; } }
        }
        v.push_back(-3); for (int i = 0; i < d; i++) v.push_back(bw[i]); for (int i = 0; i < d; i++) v.push_back(bs[i]);
    } else {
    for (int i = 0; i < d; i++) if (vars[i] >= 0) v.push_back(vars[i]);
    if (RMODE && RMAXV > 0) for (int i = 0; i < d; i++) if (wl[i] == 1) {   // six inflow: the chosen y6b var
        int st = wl[(i + d - 1) % d] * 25 + sl[(i + d - 1) % d] * 5 + wl[i], c = sl[i] * 5 + wl[(i + 1) % d];
        if (RA[st][c] >= 0) v.push_back(7000000 + RA[st][c]);
    }
    sort(v.begin(), v.end());
    if (HASX) {   // rows differ by their transfer types too
        vector<int> tt; for (int i = 0; i < d; i++) if (wl[i] >= 2) { tt.push_back(1000000 + tin[i]); tt.push_back(2000000 + tout[i]); }
        sort(tt.begin(), tt.end()); v.push_back(-1); v.insert(v.end(), tt.begin(), tt.end());
    }
    if (ARRKEY) { v.push_back(-2); for (int i = 0; i < d; i++) v.push_back(9000000 + wl[i] * 5 + sl[i]); }   // s12r check: one entry per arrangement
    }
    if (F2POS > 1e-15) { POSADM++; if (w - F2POS <= thr) POSADMX++; }   // W15 v2: admissible leaf above the threshold that has a positive correction
    auto it = found.find(v);
    if (it != found.end()) return;
    found[v] = Res{w, link, s, v};
    if ((int)found.size() > maxout) {   // drop the lightest
        auto mi = found.begin();
        for (auto jt = found.begin(); jt != found.end(); ++jt) if (jt->second.w < mi->second.w) mi = jt;
        found.erase(mi);
    }
    updThr();
}
static bool forbidden(int i) {
    auto it = PIDX.find(d); if (it == PIDX.end()) return false;
    auto &L = it->second[i * 625 + code[i]];
    for (auto &im : L) {
        bool ok = true;
        for (auto [p, m] : im.rest) if (code[p] < 0 || !matches(m, code[p])) { ok = false; break; }
        if (ok) return true;
    }
    return false;
}
// state at step i: (w_{i-1}, s_{i-1}, w_i)
static long long nodelimit = 20000000; static bool aborted;
static void dfs(int i, int st, double w) {   // (sep3x: w includes resolved transfer terms)
    nodes++;
    if (nodelimit > 0 && nodes > nodelimit && !found.empty()) { aborted = true; return; }
    if (i == d) { if (st == a0) leaf(w); return; }
    int k = d - i;   // transitions left
    for (int c = 0; c < 25; c++) {
        if (!AL[ui][st][c]) continue;
        int sc = c / 5, wn = c % 5;
        if (HASM && (!((MK[d + i] >> sc) & 1) || (i + 1 < d && !((MK[i + 1] >> wn) & 1)))) continue;   // W12 slot masks
        int ns = (st % 5) * 25 + sc * 5 + wn;   // (wc, sc, wn)
        if (i == d - 1 && ns != a0) continue;
        if (i == d - 2 && wn != a0 / 25) continue;     // w_{d-1} is fixed by a0 (keeps wl[d-1] valid during the search)
        double nw = w + W[st][c];
        double b = (k - 1 == 0) ? (ns == a0 ? 0.0 : -1e18) : Bnd[k - 1][ns * 125 + a0];
        if (nw + b + (d - (BUGFIX ? NRES[i] : NRES[i + 1])) * XINMAX + SLACK <= curThr() + 1e-9) continue;   // W12 fix: the positions resolved at this step are not in nw yet
        sl[i] = sc; if (i + 1 < d) wl[i + 1] = wn;
        if (HASX) {
            for (int j : RES[i]) nw += contrib(j);
            if (nw + b + (d - NRES[i + 1]) * XINMAX + SLACK <= curThr() + 1e-9) continue;
        }
        int wc = st % 5;
        vars[i] = VA[ui][st][c]; code[i] = (wc == 0) ? CO[ui][st][c] : -1;
        if (wc == 0 && forbidden(i)) continue;
        if (wc == 0 && omax > 0 && oracleHit(i)) continue;
        int p_ = i + 1; bool nprune = false;   // W12 SEP_NECK: the link must be its own least rotation (strictly smaller rotation seen in the prefix -> prune)
        if (NECK && p_ < d) {
            for (int r = 1; r <= p_; r++) if (DEC[r] < 0) { int k_ = p_ - r;
                if (wl[p_] < wl[k_]) { nprune = true; break; } if (wl[p_] > wl[k_]) DEC[r] = p_; }
            if (nprune) { for (int r = 1; r <= p_; r++) if (DEC[r] == p_) DEC[r] = -1; continue; }
        }
        dfs(i + 1, ns, nw);
        if (NECK && p_ < d) for (int r = 1; r <= p_; r++) if (DEC[r] == p_) DEC[r] = -1;
        if (aborted) return;
    }
}
static void searchCore() {
    found.clear(); CT = thr; aborted = false;
    // start states: w_0 = 5 (every arrangement of positive weight has a 5; rotate it to position 0)
    vector<pair<double,int>> starts;
    for (int a = 0; a < 125; a++) if ((anyStartR || a % 5 == 0) && Bnd[d][a * 125 + a] + d * XINMAX + SLACK > thr + 1e-9 && !(HASM && (!((MK[d - 1] >> (a / 25)) & 1) || !((MK[2 * d - 1] >> (a / 5 % 5)) & 1) || !((MK[0] >> (a % 5)) & 1))))
        starts.push_back({-(Bnd[d][a * 125 + a] + d * XINMAX), a});
    sort(starts.begin(), starts.end());
    if (PART_N > 1) { vector<pair<double,int>> keep; for (size_t k = 0; k < starts.size(); k++) if ((int)(k % PART_N) == PART_K) keep.push_back(starts[k]); starts.swap(keep); }   // W15
    for (auto [nb_, a] : starts) {
        if (-nb_ + SLACK <= curThr() + 1e-9) break;
        a0 = a; wl[d - 1] = a / 25; sl[d - 1] = a / 5 % 5; wl[0] = a % 5;
        for (int r = 0; r < 64; r++) DEC[r] = -1;
        dfs(0, a, 0.0);
        if (aborted) break;
    }
}
static void runSearch() {
    nodes = 0; POSLEAF = POSVIOL = POSCROSS = POSADM = POSADMX = 0; searchCore();
    vector<Res> out; for (auto &kv : found) out.push_back(kv.second);
    sort(out.begin(), out.end(), [](const Res &a, const Res &b) { return a.w > b.w; });
    for (auto &r : out) {
        printf("A %.9f %s %s", r.w, r.link.c_str(), r.s.c_str());
        for (int v : r.v) printf(" %d", v);
        printf("\n");
    }
    printf("END %zu %lld %d POS %lld %lld %lld SLACK %.9g POSADM %lld %lld\n", out.size(), nodes, aborted ? 1 : 0, POSLEAF, POSVIOL, POSCROSS, SLACK, POSADM, POSADMX); fflush(stdout);
}

// W12 class sweep ("S thr K"): every dihedral class of link words of degree d (least-rotation necklaces, reflection-filtered,
// RBIG links dropped at d = 7, 8). For a fixed link the relaxed row value (window weights W + transfer terms) is a cycle sum
// of terms in consecutive apex pairs (s_{i-1}, s_i), so a 5-state max-plus cycle DP gives its exact maximum over the apex
// letters; every leaf correction is <= 0 against it (the pruning bound of the search), so a class whose maximum is <= thr has
// no violator and is skipped. Every other class is searched exactly by the masked DFS (top K per class).
static vector<int> NW;   // current necklace
static long long SW_cls = 0, SW_dp = 0, SW_hit = 0; static vector<Res> SW_out;
static double classMax(const int *w) {
    double T_[64][5][5];
    if (HASX) for (int k = 0; k < d; k++) wl[k] = w[k];
    for (int i = 0; i < d; i++) for (int a = 0; a < 5; a++) for (int b = 0; b < 5; b++) {
        int st = w[(i + d - 1) % d] * 25 + a * 5 + w[i], c = b * 5 + w[(i + 1) % d];
        if (!AL[ui][st][c]) { T_[i][a][b] = -1e18; continue; }
        double v = W[st][c];
        if (HASX && w[i] >= 2) { sl[(i + d - 1) % d] = a; sl[i] = b; v += contrib(i); }
        T_[i][a][b] = v;
    }
    double best = -1e18;
    for (int s0 = 0; s0 < 5; s0++) {   // s_{d-1} = s0 closes the cycle: transition i uses (s_{i-1}, s_i), s_{-1} = s_{d-1}
        double D[5]; for (int b = 0; b < 5; b++) D[b] = T_[0][s0][b];
        for (int i = 1; i < d; i++) { double E[5]; for (int b = 0; b < 5; b++) { double m = -1e18; for (int a = 0; a < 5; a++) m = max(m, D[a] + T_[i][a][b]); E[b] = m; } for (int b = 0; b < 5; b++) D[b] = E[b]; }
        best = max(best, D[s0]);
    }
    return best;
}
static void sweepClass(int K) {
    SW_cls++;
    string lk(d, '0'); for (int i = 0; i < d; i++) lk[i] = '5' + NW[i];
    if ((d == 7 || d == 8) && RBIG.count(canonWord(lk))) return;
    // reflection filter: keep w only if w <= least rotation of reverse(w)
    if (CANONREFL) { vector<int> r(NW.rbegin(), NW.rend()); vector<int> best = r;
      for (int k = 1; k < d; k++) { vector<int> t(d); for (int i = 0; i < d; i++) t[i] = r[(i + k) % d]; if (t < best) best = t; }
      if (best < NW) return; }
    int w[64]; for (int i = 0; i < d; i++) w[i] = NW[i];
    double cm = classMax(w); SW_dp++;
    if (cm <= thr + 1e-9) return;
    HASM = true; for (int i = 0; i < d; i++) { MK[i] = 1 << NW[i]; MK[d + i] = 31; }
    int keepK = maxout; maxout = K; searchCore(); maxout = keepK; HASM = false;
    if (!found.empty()) SW_hit++;
    for (auto &kv : found) SW_out.push_back(kv.second);
}
static void runSweep(int K) {
    nodes = 0; SW_cls = SW_dp = SW_hit = 0; SW_out.clear(); NW.assign(d, 0);
    // FKM with a 1-based array a[0] = 0 sentinel: shift by one
    vector<int> A(d + 1, 0);
    std::function<void(int,int)> gen = [&](int t, int p) {
        if (t > d) { if (d % p == 0) { for (int i = 0; i < d; i++) NW[i] = A[i + 1]; sweepClass(K); } return; }
        A[t] = A[t - p]; gen(t + 1, p);
        for (int j = A[t - p] + 1; j < 5; j++) { A[t] = j; gen(t + 1, t); }
    };
    gen(1, 1);
    sort(SW_out.begin(), SW_out.end(), [](const Res &a, const Res &b) { return a.w > b.w; });
    for (auto &r : SW_out) printf("A %.9f %s %s\n", r.w, r.link.c_str(), r.s.c_str());
    printf("END %zu %lld 0 %lld %lld %lld\n", SW_out.size(), nodes, SW_cls, SW_dp, SW_hit); fflush(stdout);
}
int main(int argc, char **argv) {
    if (const char *e = getenv("SEP_NODELIMIT")) nodelimit = atoll(e);   // 0 = no abort (exhaustive)
    if (const char *e = getenv("SEP_ARRKEY")) ARRKEY = atoi(e) != 0;
    if (const char *e = getenv("SEP_CANON")) CANONKEY = atoi(e) != 0;   // W12
    if (const char *e = getenv("SEP_CANONREFL")) CANONREFL = atoi(e) != 0;   // W12: also identify reflections (only for reflection-invariant rows)
    if (const char *e = getenv("SEP_BUGFIX")) BUGFIX = atoi(e) != 0;
    if (const char *e = getenv("SEP_SLACKD")) { const char *p_ = e; int dd_; double v_; int n_;   // W15 NOCLAMP: "7:x,8:y,..."
        while (sscanf(p_, "%d:%lf%n", &dd_, &v_, &n_) == 2) { if (dd_ >= 0 && dd_ < 64 && v_ >= 0) SLACKD[dd_] = v_; p_ += n_; if (*p_ == ',') p_++; else break; }
        fprintf(stderr, "sep: NOCLAMP slack table loaded (%s)\n", e); }
    if (const char *e = getenv("SEP_PART")) { if (sscanf(e, "%d/%d", &PART_K, &PART_N) != 2 || PART_N < 1 || PART_K < 0 || PART_K >= PART_N) { fprintf(stderr, "bad SEP_PART\n"); return 90; } }   // W15   // W12: SEP_BUGFIX=0 restores the inherited pre-check (control only)
    if (const char *e = getenv("SEP_NECK")) NECK = atoi(e) != 0;   // W12: least-rotation pruning of the link (needs SEP_CANON for one entry per class)
    if (const char *e = getenv("SEP_EXACT6")) { FILE *g = fopen(e, "rb"); if (!g) return 30; EX6.assign(3L * 390625, 0.0);
        if (fread(EX6.data(), sizeof(double), EX6.size(), g) != EX6.size()) return 31; fclose(g); HASEX6 = true;
        fprintf(stderr, "sep: exact six-window table loaded (%s)\n", e); }
    if (const char *e = getenv("SEP_FB6")) { FILE *g = fopen(e, "rb"); if (!g) return 41; FBX.assign(3L * 1953125, 0.0);
        if (fread(&FBREL[0][0][0], sizeof(double), 3 * 125 * 25, g) != 3 * 125 * 25) return 42;
        if (fread(FBX.data(), sizeof(double), FBX.size(), g) != FBX.size()) return 43; fclose(g); HASFB = true; }
    if (const char *e = getenv("SEP_L3Q")) { FILE *g = fopen(e, "rb"); if (!g) return 35; L3QEX.assign(31250, 0.0); L3PQ.assign(125, 0.0);
        if (fread(&L3REL[0][0], sizeof(double), 125 * 25, g) != 125 * 25) return 36;
        if (fread(L3QEX.data(), sizeof(double), 31250, g) != 31250) return 37;
        if (fread(L3PQ.data(), sizeof(double), 125, g) != 125) return 38; fclose(g); HASL = true; }
    if (const char *e = getenv("SEP_L3Q8")) { FILE *g = fopen(e, "rb"); if (!g) return 45; L8X.assign(31250, 0.0); L8P.assign(125, 0.0);
        if (fread(&L8REL[0][0], sizeof(double), 125 * 25, g) != 125 * 25) return 46;
        if (fread(L8X.data(), sizeof(double), 31250, g) != 31250) return 47;
        if (fread(L8P.data(), sizeof(double), 125, g) != 125) return 48; fclose(g); HASL8 = true; }
    if (const char *e = getenv("SEP_RTAB")) { FILE *g = fopen(e, "rb"); if (!g) return 32; REX.assign(15625, 0.0);
        if (fread(&RREL[0][0], sizeof(double), 125 * 25, g) != 125 * 25) return 33;
        if (fread(REX.data(), sizeof(double), REX.size(), g) != REX.size()) return 34; fclose(g); HASR = true;
        fprintf(stderr, "sep: hat-channel r table loaded (%s)\n", e); }
    if (const char *e = getenv("SEP_F2BS")) { FILE *g = fopen(e, "rb"); if (!g) return 60;
        F2MT.assign(3L * 625 * 4 * 32, 0.0); F2QF7.assign(25 * 32, 0.0); F2QF8.assign(25 * 32, 0.0);
        F2PM.assign(3L * 390625, 0); F2MK7.assign(31250, 0); F2MK8.assign(31250, 0);
        if (fread(F2MT.data(), 8, F2MT.size(), g) != F2MT.size()) return 61;
        if (fread(F2QF7.data(), 8, 800, g) != 800 || fread(F2QF8.data(), 8, 800, g) != 800) return 62;
        if (fread(F2PM.data(), 1, F2PM.size(), g) != F2PM.size()) return 63;
        if (fread(F2MK7.data(), 1, 31250, g) != 31250 || fread(F2MK8.data(), 1, 31250, g) != 31250) return 64;
        long nr = 0;
        for (int gi = 0; gi < 7; gi++) { uint32_t n; if (fread(&n, 4, 1, g) != 1) return 65;
            int dd = gi < 3 ? 7 + gi : (gi < 5 ? 7 : 8);
            for (uint32_t k = 0; k < n; k++) { F2R r; if (fread(&r, sizeof(F2R), 1, g) != 1) return 66; nr++;
                for (int b = 0; b < 25; b++) {   // bucket by (s_{i-1}, s_i): keep the rule unless it forbids that pair
                    int sm1 = b / 5, s0 = b % 5;
                    if ((r.fs >> (5 * (dd - 1) + sm1) & 1) || (r.fs >> s0 & 1)) continue;
                    F2G[gi][b].push_back(r);
                } } }
        fclose(g); HASF2B = true; fprintf(stderr, "sep: f2b leaf tables loaded, %ld rules (%s)\n", nr, e); }
    if (const char *e = getenv("SEP_ZTAB")) { FILE *g = fopen(e, "rb"); if (!g) return 70; ZEX.assign(3L * 15625, 0.0);
        if (fread(&ZREL[0][0][0], sizeof(double), 3 * 125 * 25, g) != 3 * 125 * 25) return 71;
        if (fread(ZEX.data(), sizeof(double), ZEX.size(), g) != ZEX.size()) return 72; fclose(g); HASZ = true;
        fprintf(stderr, "sep: W10 z table loaded (%s)\n", e); }
    if (const char *e = getenv("SEP_KS")) { FILE *g = fopen(e, "rb"); if (!g) return 84; int32_t nk, a10;   // W17
        if (fread(&nk, 4, 1, g) != 1 || fread(&a10, 4, 1, g) != 1 || nk < 0 || nk > 64) return 85; KSA10G = a10 != 0;
        for (int q = 0; q < nk; q++) { KSKey k; int32_t P, nc; double a;
            if (fread(&P, 4, 1, g) != 1 || fread(&a, 8, 1, g) != 1 || fread(&nc, 4, 1, g) != 1 || nc < 0 || nc > 16) return 86;
            if (!(a >= 0.0) || P <= 0 || (P & 3)) { fprintf(stderr, "sep: KS key %d refused (amount %g, payee mask %d)\n", q, a, P); return 87; }
            k.P = P; k.a = a; k.nc = nc;
            for (int t = 0; t < nc; t++) { int32_t pp, mm; if (fread(&pp, 4, 1, g) != 1 || fread(&mm, 4, 1, g) != 1) return 86;
                if (pp < 0 || pp > 10 || pp == 9 || mm <= 0 || mm > 31) { fprintf(stderr, "sep: KS position %d / mask %d refused\n", pp, mm); return 88; }
                k.pos[t] = pp; k.msk[t] = mm; }
            KSK.push_back(k); }
        if (fread(&KSREL[0][0][0], sizeof(double), 3 * 125 * 25, g) != 3 * 125 * 25) return 89; fclose(g); HASKS = true;
        for (int u = 0; u < 3; u++) for (int a = 0; a < 125; a++) for (int c = 0; c < 25; c++) { if (KSREL[u][a][c] < 0) return 89; KSMAXU[u] = max(KSMAXU[u], KSREL[u][a][c]); }
        if (const char *m = getenv("SEP_KSPLANT")) KSPLANT = string(m) == "pay" ? 1 : string(m) == "half" ? 2 : 0;
        if (!getenv("SEP_F2BS")) { fprintf(stderr, "sep: SEP_KS needs SEP_F2BS (mask tables)\n"); return 83; }
        fprintf(stderr, "sep: W17 KS table loaded (%s): %d keys, window max %.6g / %.6g / %.6g, a10 %s, plant %d\n", e, nk, KSMAXU[0], KSMAXU[1], KSMAXU[2], KSA10G ? "grammar" : "amask", KSPLANT); }
    if (const char *e = getenv("SEP_GK")) { FILE *g = fopen(e, "rb"); if (!g) return 94; int32_t nk;   // W17 round 4
        if (!getenv("SEP_F2BS") || F2PM.empty()) { fprintf(stderr, "sep: SEP_GK needs SEP_F2BS (pmask / MASK tables)\n"); return 95; }
        if (fread(&nk, 4, 1, g) != 1 || nk < 0 || nk > 4096) return 96;
        for (int q = 0; q < nk; q++) { GKKey k; int32_t U, V, nc; double a;
            if (fread(&U, 4, 1, g) != 1 || fread(&V, 4, 1, g) != 1 || fread(&a, 8, 1, g) != 1 || fread(&nc, 4, 1, g) != 1 || nc < 0 || nc > 16) return 97;
            if (!(a >= 0.0) || U <= 0 || ((U & ~7) && U != 8 && U != 16) || V <= 0 || V > 31) { fprintf(stderr, "sep: GK key %d refused (amount %g, payer %d, payee %d)\n", q, a, U, V); return 98; }
            k.U = U; k.V = V; k.a = a; k.nc = nc;
            for (int t = 0; t < nc; t++) { int32_t pp, mm; if (fread(&pp, 4, 1, g) != 1 || fread(&mm, 4, 1, g) != 1) return 97;
                if (pp < 0 || pp > 10 || pp == 9 || mm <= 0 || mm > 31 || (U >= 8 && (pp == 2 || pp == 5))) { fprintf(stderr, "sep: GK position %d / mask %d refused\n", pp, mm); return 99; }
                k.pos[t] = pp; k.msk[t] = mm; }
            GKK.push_back(k); }
        if (fread(&GKREL[0][0][0], sizeof(double), 3 * 125 * 25, g) != 3 * 125 * 25) return 100; fclose(g);
        GKW.assign(3 * GKN9, 0.0); double own[3][125][25]; for (int u = 0; u < 3; u++) for (int a = 0; a < 125; a++) for (int c = 0; c < 25; c++) own[u][a][c] = -1e300;   // code_gk8: cells may be < 0
        for (int u = 0; u < 3; u++) for (long ix = 0; ix < GKN9; ix++) {
            int x[9]; long r = ix; for (int t = 8; t >= 0; t--) { x[t] = r % 5; r /= 5; }   // wm2 wm1 w0 wp1 wp2 sm2 sm1 s0 sp1
            double v = gkWinVal(u, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]); GKW[u * GKN9 + ix] = v;
            int st = x[1] * 25 + x[6] * 5 + x[2], c = x[7] * 5 + x[3]; if (v > own[u][st][c]) own[u][st][c] = v;
        }
        double mdiff = 0.0; long nd = 0;
        for (int u = 0; u < 3; u++) for (int a = 0; a < 125; a++) for (int c = 0; c < 25; c++) {
            double df = fabs(own[u][a][c] - GKREL[u][a][c]); if (df > mdiff) mdiff = df; if (df > 1e-12) nd++;
            GKMAXU[u] = max(GKMAXU[u], GKREL[u][a][c]); if (!(GKREL[u][a][c] > -1e9 && GKREL[u][a][c] < 1e9)) return 100; }   // code_gk8: negative cells allowed (payer-8/9 OUT)
        if (const char *m = getenv("SEP_GKPLANT")) GKPLANT = string(m) == "pay" ? 1 : string(m) == "half" ? 2 : 0;
        fprintf(stderr, "sep: W17 GK table loaded (%s): %d keys, window max %.6g / %.6g / %.6g; own window table vs Python's: %ld cells differ, max |diff| %.3g; plant %d\n",
                e, nk, GKMAXU[0], GKMAXU[1], GKMAXU[2], nd, mdiff, GKPLANT);
        if (nd) { fprintf(stderr, "sep: GK window tables differ between C++ and Python: refused\n"); return 93; }
        HASGK = true; }
    if (const char *e = getenv("SEP_Q7")) { FILE *g = fopen(e, "rb"); if (!g) return 73; QPAIR.assign(3L * 625 * 25, 0.0); QPAY.assign(78125, 0.0);
        if (fread(&QREL[0][0][0], sizeof(double), 3 * 125 * 25, g) != 3 * 125 * 25) return 74;
        if (fread(QPAIR.data(), sizeof(double), QPAIR.size(), g) != QPAIR.size()) return 75;
        if (fread(QPAY.data(), sizeof(double), QPAY.size(), g) != QPAY.size()) return 76; fclose(g); HASQ7 = true;
        for (int u = 0; u < 3; u++) for (int a = 0; a < 125; a++) for (int c = 0; c < 25; c++) QMAXU[u] = max(QMAXU[u], QREL[u][a][c]);
        if (const char *m = getenv("SEP_Q7M")) Q7MASK = atoi(m) != 0;
        if (Q7MASK && !HASF2B) { fprintf(stderr, "sep: SEP_Q7M needs SEP_F2BS (mask tables)\n"); return 77; }
        if (const char *m = getenv("SEP_F2B7")) F2B7 = atoi(m) != 0;   // W17 round 5 (SPEC f2b7)
        if (F2B7 && !Q7MASK) { fprintf(stderr, "sep: SEP_F2B7 needs SEP_Q7M and SEP_F2BS\n"); return 78; }
        if (F2B7) fprintf(stderr, "sep: W17 f2b7 on: q7m 7-sides (c or apex >= 7) masked 31 & ~f2b extra7 at the leaf; window unmasked\n");
        fprintf(stderr, "sep: W10 q7 table loaded (%s), masks %d\n", e, (int)Q7MASK); }
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
    int nf = 0;   // Job 30: optional section "NF" + NF lines "d k slot mask ..." (absent in older inputs)
    if (fscanf(f, "%d", &nf) != 1) nf = 0;
    for (int i = 0; i < nf; i++) {
        int dd, k; if (fscanf(f, "%d %d", &dd, &k) != 2) return 13;
        vector<pair<int,int>> P(k); for (auto &x : P) if (fscanf(f, "%d %d", &x.first, &x.second) != 2) return 14;
        addFull(dd, P);
    }
    if (const char *e = getenv("SEP_FULLX")) {   // RELAY_SPEC_s39o rpatN: extra whole-window patterns "d k slot mask ..." per line
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
        if (cmd[0] == 'f') {   // f2b041 self-test: "f d link s" -> the leaf delta of this arrangement
            char lb[40], sb[40];
            if (scanf("%d %39s %39s", &d, lb, sb) != 3) return 10;
            ui = d == 7 ? 0 : d == 8 ? 1 : 2;
            for (int i = 0; i < d; i++) { wl[i] = lb[i] - '5'; sl[i] = sb[i] - '5'; }
            printf("%.15f\n", f2bDelta()); fflush(stdout); continue;
        }
        if (cmd[0] == 'e') {   // W10 self-test: "e d link s" -> exact row value under the last query's weights (same d), no filters
            char lb[40], sb[40]; int dd;
            if (scanf("%d %39s %39s", &dd, lb, sb) != 3) return 10;
            if (dd != d) { printf("nan\n"); fflush(stdout); continue; }
            for (int i = 0; i < d; i++) { wl[i] = lb[i] - '5'; sl[i] = sb[i] - '5'; }
            double w = 0.0; bool ok = true;
            for (int i = 0; i < d; i++) {
                int st = wl[(i + d - 1) % d] * 25 + sl[(i + d - 1) % d] * 5 + wl[i], c = sl[i] * 5 + wl[(i + 1) % d];
                if (!AL[ui][st][c]) ok = false; else w += W[st][c];
            }
            if (HASX) for (int j = 0; j < d; j++) w += contrib(j);
            w += exactCorr();
            if (ok) printf("%.15f\n", w); else printf("inadm\n");
            fflush(stdout); continue;
        }
        if (cmd[0] == 'M') {   // W12: "M n m_0 .. m_{n-1}" slot masks for the next searches (n = 0 clears)
            int n; if (scanf("%d", &n) != 1) return 80; HASM = n > 0;
            for (int k = 0; k < n; k++) if (scanf("%d", &MK[k]) != 1) return 81;
            continue;
        }
        if (cmd[0] == 'S') {   // W12: "S thr K": class sweep under the last query's weights (see runSweep)
            int K; if (scanf("%lf %d", &thr, &K) != 2) return 83;
            runSweep(K); continue;
        }
        if (cmd[0] == 'r') {   // W12: "r thr maxout": search again under the last query's weights
            if (scanf("%lf %d", &thr, &maxout) != 2) return 82;
            runSearch(); continue;
        }
        if (cmd[0] == 'c') {   // "c d link s": is this arrangement free of forbidden patterns (and not an RBIG wheel)?
            char lb[40], sb[40];
            if (scanf("%d %39s %39s", &d, lb, sb) != 3) return 10;
            ui = d == 7 ? 0 : d == 8 ? 1 : 2; bool ok = true;
            for (int i = 0; i < d; i++) { wl[i] = lb[i] - '5'; sl[i] = sb[i] - '5'; }
            if ((d == 7 || d == 8) && RBIG.count(canonWord(lb))) ok = false;
            for (int i = 0; i < d && ok; i++) {
                int st = wl[(i + d - 1) % d] * 25 + sl[(i + d - 1) % d] * 5 + wl[i], c = sl[i] * 5 + wl[(i + 1) % d];
                if (!AL[ui][st][c]) { ok = false; break; }
                code[i] = wl[i] == 0 ? CO[ui][st][c] : -1;
            }
            // pattern check needs all codes: test every position as the 'last' one in index order
            for (int i = 0; i < d && ok; i++) if (wl[i] == 0 && forbidden(i)) ok = false;
            if (ok && fullForbidden()) ok = false;
            printf("%d\n", ok ? 1 : 0); fflush(stdout); continue;
        }
        if (scanf("%d %lf %d %d", &d, &thr, &maxout, &omax) != 4) return 8;
        SLACK = (d >= 0 && d < 64) ? SLACKD[d] : 0.0;   // W15 NOCLAMP
        for (auto &x : y) if (scanf("%lf", &x) != 1) return 9;
        ui = d == 7 ? 0 : d == 8 ? 1 : 2;
        { char xb[8]; int kx; if (scanf("%7s %d", xb, &kx) != 2 || xb[0] != 'X') return 11;
          fill(XV.begin(), XV.end(), 0.0); HASX = false; XINMAX = 0.0;
          for (int q = 0; q < kx; q++) { int cd; double val; if (scanf("%d %lf", &cd, &val) != 2) return 12;
            if (cd >= 0 && cd < 140625 && val > 0) { XV[cd] = val; HASX = true;
              int t_ = (cd / 15625) % 3; if (t_ == ui) XINMAX = max(XINMAX, val); } } }
        if (RMODE) { char rb[8]; int k; if (scanf("%7s %d", rb, &k) != 2 || rb[0] != 'R') return 18;
            RY.assign(k, 0.0); for (auto &x : RY) if (scanf("%lf", &x) != 1) return 19; }
        buildRes(); RMAXV = 0;
        for (int a = 0; a < 125; a++) for (int c = 0; c < 25; c++) {
            W[a][c] = AL[ui][a][c] ? (VA[ui][a][c] >= 0 ? y[VA[ui][a][c]] : 0.0) : -1e18;
            RA[a][c] = -1; RBEST[a][c] = 0.0;
            if (RMODE && AL[ui][a][c] && a % 5 == 1) {   // a link 6 at w_i: + max over p of y6b
                double best = 0.0; int bv = -1;
                for (int q = 0; q < 5; q++) { int vv = RV[ui][a][c][q]; if (vv >= 0 && RY[vv] > best + 1e-15) { best = RY[vv]; bv = vv; } }
                W[a][c] += best; RA[a][c] = bv; RMAXV = max(RMAXV, best); RBEST[a][c] = best;
            }
            if (HASR && AL[ui][a][c] && c / 5 == 0) W[a][c] += RREL[a][c];   // apex five s_i: + relaxed r
            if (HASL && ui == 0 && d == 7 && AL[ui][a][c] && a % 5 == 2) W[a][c] += L3REL[a][c];   // link 7 at d = 7: + relaxed l3q
            if (HASL8 && ui == 1 && d == 8 && AL[ui][a][c] && a % 5 == 2) W[a][c] += L8REL[a][c];   // s47 (ii): link 7 at d = 8: + UB8(e, r) + UB8(b, q)
            if (HASFB && AL[ui][a][c]) W[a][c] += FBREL[ui][a][c];   // s44: + relaxed fb window term
            if (HASZ && AL[ui][a][c] && a % 5 == 0) W[a][c] += ZREL[ui][a][c];    // W10: link five, relaxed z - zr
            if (HASQ7 && AL[ui][a][c] && a % 5 == 2) W[a][c] += QREL[ui][a][c];   // W10: link 7, unmasked payee credit Q
            if (HASKS && AL[ui][a][c] && a % 5 == 2) W[a][c] += KSREL[ui][a][c];  // W17: link 7, K* / EDGE payee window bound
            if (HASGK && AL[ui][a][c]) W[a][c] += GKREL[ui][a][c];   // W17 round 4: generic keys, window bound at every link position
        }
        // M[a][b] (max-plus one step), Bnd[k] = M^k
        vector<double> M(125 * 125, -1e18);
        for (int a = 0; a < 125; a++) for (int c = 0; c < 25; c++) if (AL[ui][a][c]) {
            int b = (a % 5) * 25 + (c / 5) * 5 + c % 5; M[a * 125 + b] = max(M[a * 125 + b], W[a][c]);
        }
        Bnd.assign(d + 1, vector<double>());
        Bnd[1] = M;
        for (int k = 2; k <= d; k++) {
            vector<double> P(125 * 125, -1e18);
            for (int a = 0; a < 125; a++) for (int m = 0; m < 125; m++) {
                double x = Bnd[k - 1][a * 125 + m]; if (x < -1e17) continue;
                for (int b = 0; b < 125; b++) { double z = x + M[m * 125 + b]; if (z > P[a * 125 + b]) P[a * 125 + b] = z; }
            }
            Bnd[k] = P;
        }
        anyStartR = HASX || RMAXV > 0 || HASR || (HASL && d == 7) || HASFB || (HASQ7 && QMAXU[ui] > 0) || (HASKS && KSMAXU[ui] > 0) || (HASGK && GKMAXU[ui] > 0);   // W10: Q can load a row with no five
        runSearch();
    }
}
