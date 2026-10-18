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
static long long nodes;
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
static void leaf(double w) {
    if (omax > 0 && minRing() <= omax) return;
    if (fullForbidden()) return;
    string link(d, '0'), s(d, '0');
    for (int i = 0; i < d; i++) { link[i] = '5' + wl[i]; s[i] = '5' + sl[i]; }
    if ((d == 7 || d == 8) && RBIG.count(canonWord(link))) return;
    vector<int> v; for (int i = 0; i < d; i++) if (vars[i] >= 0) v.push_back(vars[i]);
    if (RMODE && RMAXV > 0) for (int i = 0; i < d; i++) if (wl[i] == 1) {   // six inflow: the chosen y6b var
        int st = wl[(i + d - 1) % d] * 25 + sl[(i + d - 1) % d] * 5 + wl[i], c = sl[i] * 5 + wl[(i + 1) % d];
        if (RA[st][c] >= 0) v.push_back(7000000 + RA[st][c]);
    }
    sort(v.begin(), v.end());
    if (HASX) {   // rows differ by their transfer types too
        vector<int> tt; for (int i = 0; i < d; i++) if (wl[i] >= 2) { tt.push_back(1000000 + tin[i]); tt.push_back(2000000 + tout[i]); }
        sort(tt.begin(), tt.end()); v.push_back(-1); v.insert(v.end(), tt.begin(), tt.end());
    }
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
        int ns = (st % 5) * 25 + sc * 5 + wn;   // (wc, sc, wn)
        if (i == d - 1 && ns != a0) continue;
        if (i == d - 2 && wn != a0 / 25) continue;     // w_{d-1} is fixed by a0 (keeps wl[d-1] valid during the search)
        double nw = w + W[st][c];
        double b = (k - 1 == 0) ? (ns == a0 ? 0.0 : -1e18) : Bnd[k - 1][ns * 125 + a0];
        if (nw + b + (d - NRES[i + 1]) * XINMAX <= curThr() + 1e-9) continue;
        sl[i] = sc; if (i + 1 < d) wl[i + 1] = wn;
        if (HASX) {
            for (int j : RES[i]) nw += contrib(j);
            if (nw + b + (d - NRES[i + 1]) * XINMAX <= curThr() + 1e-9) continue;
        }
        int wc = st % 5;
        vars[i] = VA[ui][st][c]; code[i] = (wc == 0) ? CO[ui][st][c] : -1;
        if (wc == 0 && forbidden(i)) continue;
        if (wc == 0 && omax > 0 && oracleHit(i)) continue;
        dfs(i + 1, ns, nw);
        if (aborted) return;
    }
}
int main(int argc, char **argv) {
    if (const char *e = getenv("SEP_NODELIMIT")) nodelimit = atoll(e);   // 0 = no abort (exhaustive)
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
            RA[a][c] = -1;
            if (RMODE && AL[ui][a][c] && a % 5 == 1) {   // a link 6 at w_i: + max over p of y6b
                double best = 0.0; int bv = -1;
                for (int q = 0; q < 5; q++) { int vv = RV[ui][a][c][q]; if (vv >= 0 && RY[vv] > best + 1e-15) { best = RY[vv]; bv = vv; } }
                W[a][c] += best; RA[a][c] = bv; RMAXV = max(RMAXV, best);
            }
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
        found.clear(); nodes = 0; CT = thr; aborted = false;
        // start states: w_0 = 5 (every arrangement of positive weight has a 5; rotate it to position 0)
        vector<pair<double,int>> starts;
        bool anyStartR = HASX || RMAXV > 0;
        for (int a = 0; a < 125; a++) if ((anyStartR || a % 5 == 0) && Bnd[d][a * 125 + a] + d * XINMAX > thr + 1e-9)
            starts.push_back({-(Bnd[d][a * 125 + a] + d * XINMAX), a});
        sort(starts.begin(), starts.end());
        for (auto [nb_, a] : starts) {
            if (-nb_ <= curThr() + 1e-9) break;
            a0 = a; wl[d - 1] = a / 25; sl[d - 1] = a / 5 % 5; wl[0] = a % 5;
            dfs(0, a, 0.0);
            if (aborted) break;
        }
        vector<Res> out; for (auto &kv : found) out.push_back(kv.second);
        sort(out.begin(), out.end(), [](const Res &a, const Res &b) { return a.w > b.w; });
        for (auto &r : out) {
            printf("A %.9f %s %s", r.w, r.link.c_str(), r.s.c_str());
            for (int v : r.v) printf(" %d", v);
            printf("\n");
        }
        printf("END %zu %lld %d\n", out.size(), nodes, aborted ? 1 : 0); fflush(stdout);
    }
}
