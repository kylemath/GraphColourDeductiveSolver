// defectb9.cpp -- EXPLORE round 18 (exploratory): defectc9.cpp with letters 5..9 allowed on rings < K (MAXL = 9: an
// exact degree-9 vertex; its own wheel has no table, so it never counts as reducible) and defectb7's optional 9th
// argument LINK:RING2 (and a 10th, FREEMAX: letters 5..FREEMAX on free slots of rings 2..K-1), which fixes the ring-1 word (exact) and the ring-2 letters at the given positions ('.' = free).
// Build: g++ -O2 -std=c++17 -o defectb9 defectb9.cpp
// defectc9.cpp -- G9 probe 2 (exploratory): defectc8 with a centre of degree C0 in 5..12. Letter 9 = degree >= 9
// (only the centre); tables over {5..9} from defect_tables9.py (base 5). The centre's own wheel for C0 >= 9 has no
// table: counted NOT reducible. For C0 >= 9 and K = 2, ring-1 words with charge < CMIN are skipped before the
// canonical test (no effect on leaves; C0 <= 8 runs are unchanged).  Usage: ./defectc9 TABLES9 C0 K CMIN MAXL [...]
// (base) defectc8.cpp -- G9 (exploratory): defectc.cpp (README §7, test G) with the alphabet {5,6,7,8} on rings < K.
// Disc around a centre (degree C0 in 5..8); ring k vertices get degrees in {5..MAXL} for k < K (MAXL = 7 reproduces
// defectc, MAXL = 8 allows degree 8), ring K and later all 6.  A vertex is rejected as soon as its link is complete
// and its wheel is reducible per loop/g9/defect_tables8.txt (bad5, bad6, d7, t7, d8, t8 over {5,6,7,8}, base-4 index);
// untested words are not reducible.  Look-ahead: feas[d][pattern base 5: 0..3 = 5..8, 4 = unknown] = some completion
// over {5..MAXL} is not bad (pruning only).
// Output: one line per leaf with charge >= CMIN: "c=<c> sig=<ring0>|<ring1>|...|<ringK> n8=<number of 8s in rings<K>".
// Build: g++ -O2 -o defectc8 defectc8.cpp
// Usage: ./defectc8 TABLES8 C0 K CMIN MAXL [MAXLEAVES] [MAXRING] [START]
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;
static vector<char> TB[9];      // TB[d] = reducible d-wheels (d = 5..8), base-4 index
static vector<char> feas[9];
static long npruned = 0;
static int FREEMAX = 9;   // b9: letters of free (unfixed) slots on rings 2..K-1 are 5..FREEMAX
static string FIX1, FIX2;   // b7/b9: fixed ring-1 word and ring-2 letters ('.' = free)
static int C0, K, CMIN, MAXL = 8, NL = 4; static long MAXLEAVES = 1000000000L, leaves = 0, leaves8 = 0, nodes = 0;
static int MAXRING = 60;
struct Ring { int a; vector<int> deg; vector<vector<int>> inb, outb; };
static vector<Ring> R;
static inline int LT(int d) { return d > 9 ? 9 : d; }
static int encode(const vector<int>& w) { int x = 0; for (int d : w) x = x * 5 + (d - 5); return x; }
static void build_feas() {
    for (int d = 5; d <= 8; d++) {
        int n = 1; for (int i = 0; i < d; i++) n *= 6;
        vector<int> pw(d); { int p = 1; for (int i = d - 1; i >= 0; i--) { pw[i] = p; p *= 6; } }
        feas[d].assign(n, 0);
        for (int x = 0; x < n; x++) {
            int dig[8], y = x; for (int i = d - 1; i >= 0; i--) { dig[i] = y % 6; y /= 6; }
            int u = -1; for (int i = 0; i < d; i++) if (dig[i] == 5) { u = i; break; }
            if (u < 0) { int code = 0; for (int i = 0; i < d; i++) code = code * 5 + dig[i]; feas[d][x] = !TB[d][code]; continue; }
            bool ok = false;
            for (int c = 0; c < NL && !ok; c++) if (feas[d][x - (5 - c) * pw[u]]) ok = true;
            feas[d][x] = ok;
        }
    }
}
// letters 5..8 known, 0 = unknown
static bool feasible(int deg, const vector<int>& w) {
    if (deg > 8) return true;
    if (deg < 5) return false;
    if ((int)w.size() != deg) { fprintf(stderr, "feasible: size mismatch\n"); exit(2); }
    int x = 0; for (int d : w) x = x * 6 + (d == 0 ? 5 : d - 5);
    return feas[deg][x];
}
static void linkword(int k, int j, vector<int>& w) {
    w.clear();
    if (k == 0) { for (int i = 0; i < R[1].a; i++) w.push_back(R[1].deg[i]); return; }
    Ring& r = R[k]; int a = r.a;
    w.push_back(r.deg[(j - 1 + a) % a]);
    if (k == 1) w.push_back(LT(C0)); else for (int p : r.inb[j]) w.push_back(R[k - 1].deg[p]);
    w.push_back(r.deg[(j + 1) % a]);
    const vector<int>& ob = r.outb[j];
    for (int i = (int)ob.size() - 1; i >= 0; i--) w.push_back(R[k + 1].deg[ob[i]]);
}
static bool badw(int deg, const vector<int>& w) {
    if (deg > 8) return false;   // centre of degree >= 9: no table, not reducible
    for (int d : w) if (d < 5 || d > 9) return true;
    if ((int)w.size() != deg) return true;
    if (deg < 5) return true;
    return TB[deg][encode(w)];
}
static bool grow(int k) {
    Ring& r = R[k]; int a = r.a; vector<int> out(a); int b = 0;
    for (int j = 0; j < a; j++) {
        int in = (k == 0) ? 0 : (k == 1 ? 1 : (int)r.inb[j].size());
        out[j] = r.deg[j] - in - 2; if (out[j] < 1) return false; b += out[j] - 1;
    }
    if (k == 0) { return true; }
    if (b < 3 || b > MAXRING) return false;
    if ((int)R.size() <= k + 1) R.resize(k + 2);
    Ring& z = R[k + 1]; z.a = b; z.deg.assign(b, 0); z.inb.assign(b, {}); z.outb.assign(b, {});
    r.outb.assign(a, {}); int t = 0;
    for (int j = 0; j < a; j++) {
        for (int i = 0; i < out[j]; i++) { int q = (t + i) % b; r.outb[j].push_back(q); z.inb[q].push_back(j); }
        t += out[j] - 1;
    }
    vector<int>& i0 = z.inb[0];
    if (find(i0.begin(), i0.end(), a - 1) != i0.end() && i0.size() > 1) {
        vector<int> o; o.push_back(a - 1); for (int x : i0) if (x != a - 1) o.push_back(x); i0 = o;
    }
    return true;
}
static void emit() {
    int c = 0, n8 = 0; for (int k = 0; k < K; k++) for (int d : R[k].deg) { c += 6 - d; if (d == 8) n8++; }
    if (c < CMIN) return;
    leaves++; if (n8) leaves8++;
    printf("c=%d sig=", c);
    for (int k = 0; k <= K; k++) { if (k) putchar('|'); if (k == 0) printf("%d", C0); else for (int d : R[k].deg) putchar('0' + d); }
    printf(" n8=%d\n", n8); fflush(stdout);
}
static void ring_dfs(int k);
static void finish(int k) {
    if (k < K) { if (!grow(k)) return; ring_dfs(k + 1); return; }
    if (!grow(K)) return;
    for (int i = 0; i < R[K + 1].a; i++) R[K + 1].deg[i] = 6;
    vector<int> w;
    for (int j = 0; j < R[K].a; j++) { linkword(K, j, w); if (badw(6, w)) return; }
    for (int e = K + 1; e < K + 4; e++) {
        if (!grow(e)) return;
        for (int i = 0; i < R[e + 1].a; i++) R[e + 1].deg[i] = 6;
    }
    emit();
}
static void ring_dfs(int k) {
    if (leaves >= MAXLEAVES) return;
    Ring& r = R[k]; int a = r.a; Ring& p = R[k - 1];
    vector<vector<int>> done_at(a);
    if (k >= 2) for (int j = 0; j < p.a; j++) {
        const vector<int>& ob = p.outb[j]; int last;
        if (ob.size() > 1 && ob.back() == 0 && ob.front() != 0) last = a - 1;
        else last = *max_element(ob.begin(), ob.end());
        done_at[last].push_back(j);
    }
    vector<vector<int>> ch(a);
    for (int j = 0; j < a; j++) {
        int in = (k == 1) ? 1 : (int)r.inb[j].size(); int lo = in + 3;
        bool fx = (k == 2 && !FIX2.empty() && FIX2[j] != '.');
        if (k < K) { for (int d = 5; d <= (fx || k < 2 ? MAXL : FREEMAX); d++) if (d >= lo) ch[j].push_back(d); }
        else if (6 >= lo) ch[j].push_back(6);
        if (fx) {
            vector<int> f; for (int d : ch[j]) if (d == FIX2[j] - '0') f.push_back(d); ch[j] = f;
        }
    }
    vector<int> w;
    int cfix = 0; for (int kk = 0; kk < k && kk < K; kk++) for (int d : R[kk].deg) cfix += 6 - d;
    auto partial_k = [&](int j, vector<int>& pw) {
        pw.clear(); pw.push_back(r.deg[(j - 1 + a) % a]);
        if (k == 1) pw.push_back(LT(C0)); else for (int q : r.inb[j]) pw.push_back(p.deg[q]);
        pw.push_back(r.deg[(j + 1) % a]);
        int in = (k == 1) ? 1 : (int)r.inb[j].size(); int out = r.deg[j] - in - 2;
        for (int i = 0; i < out; i++) pw.push_back(k + 1 >= K ? 6 : 0);
    };
    auto partial_p = [&](int j, vector<int>& pw) {
        int pa = p.a; pw.clear(); pw.push_back(p.deg[(j - 1 + pa) % pa]);
        if (k - 1 == 1) pw.push_back(LT(C0)); else for (int q : p.inb[j]) pw.push_back(R[k - 2].deg[q]);
        pw.push_back(p.deg[(j + 1) % pa]);
        const vector<int>& ob = p.outb[j];
        for (int i = (int)ob.size() - 1; i >= 0; i--) pw.push_back(r.deg[ob[i]]);
    };
    vector<vector<int>> sees(a);
    if (k >= 2) for (int j = 0; j < p.a; j++) for (int q : p.outb[j]) sees[q].push_back(j);
    vector<int> idx(a + 1, -1); int t = 0;
    while (t >= 0) {
        if (leaves >= MAXLEAVES) return;
        if (t == a) { nodes++; finish(k); t--; continue; }
        idx[t]++;
        if (idx[t] >= (int)ch[t].size()) { idx[t] = -1; r.deg[t] = 0; t--; continue; }
        r.deg[t] = ch[t][idx[t]]; nodes++;
        bool ok = true;
        for (int j : done_at[t]) { linkword(k - 1, j, w); if (badw(p.deg[j], w)) { ok = false; break; } }
        if (ok) for (int j : sees[t]) { partial_p(j, w); if (!feasible(p.deg[j], w)) { ok = false; break; } }
        if (ok) { partial_k(t, w); if (!feasible(r.deg[t], w)) ok = false; }
        if (ok && t > 0) { partial_k(t - 1, w); if (!feasible(r.deg[t - 1], w)) ok = false; }
        if (ok && t == a - 1) { partial_k(0, w); if (!feasible(r.deg[0], w)) ok = false; }
        if (ok && k == K - 1) {
            int cp = cfix; for (int i = 0; i <= t; i++) cp += 6 - r.deg[i];
            if (cp + (a - 1 - t) < CMIN) ok = false;
        }
        if (!ok) npruned++;
        if (ok) { t++; if (t < a) idx[t] = -1; }
    }
}
int main(int argc, char** argv) {
    if (argc < 6) { fprintf(stderr, "usage: defectb9 TABLES9 C0 K CMIN MAXL [MAXLEAVES] [MAXRING] [START] [LINK:RING2] [FREEMAX]\n"); return 1; }
    if (argc > 9) { string a = argv[9]; size_t c = a.find(':'); FIX1 = a.substr(0, c); FIX2 = a.substr(c + 1); }
    FILE* f = fopen(argv[1], "r"); C0 = atoi(argv[2]); K = atoi(argv[3]); CMIN = atoi(argv[4]); MAXL = atoi(argv[5]);
    NL = MAXL - 4;
    FREEMAX = argc > 10 ? atoi(argv[10]) : MAXL;
    if (argc > 6) MAXLEAVES = atol(argv[6]); if (argc > 7) MAXRING = atoi(argv[7]);
    string START = argc > 8 ? argv[8] : "";
    int lens[6] = {5, 6, 7, 7, 8, 8}; int dst[6] = {5, 6, 7, -1, 8, -1};
    for (int i = 0; i < 6; i++) {
        int n = 1; for (int j = 0; j < lens[i]; j++) n *= 5;
        vector<char> tmp(n);
        for (int j = 0; j < n; j++) { int x; if (fscanf(f, "%d", &x) != 1) { fprintf(stderr, "bad tables\n"); return 1; } tmp[j] = x; }
        if (dst[i] > 0) TB[dst[i]] = tmp;
    }
    build_feas();
    R.resize(K + 6);
    R[0].a = 1; R[0].deg = {C0};
    R[1].a = C0; R[1].deg.assign(C0, 0); R[1].inb.assign(C0, {}); R[1].outb.assign(C0, {});
    vector<int> w(C0); long ncanon = 0;
    int base = (K > 1 ? NL : 1);
    long tot = 1; for (int i = 0; i < C0; i++) tot *= base;
    for (long code = 0; code < tot; code++) {
        long x = code; for (int i = C0 - 1; i >= 0; i--) { w[i] = (K > 1 ? 5 + (int)(x % NL) : 6); if (K > 1) x /= NL; }
        if (C0 >= 9) {   // cheap filters for big centres: w[0] minimal letter; K = 2 charge bound
            bool mn = true; for (int i = 1; i < C0; i++) if (w[i] < w[0]) { mn = false; break; }
            if (!mn) continue;
            if (K == 2) { int c = 6 - C0; for (int i = 0; i < C0; i++) c += 6 - w[i]; if (c < CMIN) continue; }
        }
        bool canon = true;
        for (int s = 0; s < 2 && canon; s++) for (int rot = 0; rot < C0; rot++) {
            vector<int> v(C0); for (int i = 0; i < C0; i++) v[i] = s ? w[(rot - i + 2 * C0) % C0] : w[(rot + i) % C0];
            if (v < w) { canon = false; break; }
        }
        string w0; for (int d : w) w0 += char('0' + d);
        if (!FIX1.empty()) { if (w0 != FIX1) continue; }
        else if (!canon) continue;
        if (badw(C0, w)) continue;
        ncanon++;
        string ws; for (int d : w) ws += char('0' + d);
        if (ws < START) continue;
        fprintf(stderr, "ring1 %s start leaves %ld leaves8 %ld nodes %ld\n", ws.c_str(), leaves, leaves8, nodes); fflush(stderr);
        R[1].deg = w;
        if (!grow(1)) continue;
        ring_dfs(2);
        if (leaves >= MAXLEAVES) break;
    }
    fprintf(stderr, "ring1 words tried %ld\n", ncanon);
    fprintf(stderr, "centre %d K %d MAXL %d nodes %ld pruned %ld leaves %ld leaves_with_8 %ld\n", C0, K, MAXL, nodes, npruned, leaves, leaves8);
}
