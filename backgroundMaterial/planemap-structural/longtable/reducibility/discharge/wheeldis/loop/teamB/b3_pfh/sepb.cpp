// Team B round B3: receiver separation for the PFH LP, with receiver patterns (own code).
// Arrangement around a receiver u of exact degree d: link w_0..w_{d-1}, s_i between w_i and w_{i+1}; letters 5..9
// coded 0..4. Position i contributes W_U[w_{i-1}, s_{i-1}, w_i, s_i, w_{i+1}] (already maximised over w_i's privates
// by the caller; -inf = forbidden window). For d = 7 the leaf also pays H_OUT(word) (u's hand-offs; >= 0, so the
// bound stays an upper bound) and words in RBIG7 are skipped. A pattern = slot masks over w (slot i) and s (slot
// d + i); all 2d dihedral images are stored; an arrangement matching any image at every slot is forbidden.
// Protocol (stdin): "T U" + 3125 doubles | "H" + 78125 doubles | "Q d thr many" -> lines "R val wword sword", "END n".
#include <bits/stdc++.h>
using namespace std;
static const double NEG = -1e300;
double W[10][3125];
double HOUT[78125];
bool RB7[78125];
struct Pat { int d; vector<pair<int,int>> sm; };
vector<Pat> pats[40];
int d_, U_; double thr_; size_t many_;
int w[40], s[40];
long long nodes;
double G[41][125];
priority_queue<double, vector<double>, greater<double>> heap;
vector<tuple<double,string,string>> found;
inline int wc(int a, int b, int c, int e, int f) { return (((a*5+b)*5+c)*5+e)*5+f; }
double bar() { return (heap.size() >= many_) ? max(thr_, heap.top()) : thr_; }
bool forbidden() {
  for (auto &p : pats[d_]) {
    bool all = true;
    for (auto &q : p.sm) {
      int sl = q.first, m = q.second;
      int letter = sl < d_ ? w[sl] : s[sl - d_];
      if (!((m >> letter) & 1)) { all = false; break; }
    }
    if (all) return true;
  }
  return false;
}
int a0w1, a0s1, a0w0;   // fixed w_{d-1}, s_{d-1}, w_0
// DFS: positions assigned in order s_0, w_1, s_1, w_2, ... ; contribution of position i added once w_{i+1} known.
void dfs(int i, double acc) {
  // here w_0..w_i and s_0..s_{i-1} assigned (plus w_{d-1}, s_{d-1}); next choose s_i then w_{i+1}
  nodes++;
  int d = d_;
  if (i == d - 1) {
    // s_{d-1}, w_{d-1} fixed; add contribution of position d-1 (w_{d-2}, s_{d-2}, w_{d-1}, s_{d-1}, w_0) and 0
    double c1 = W[U_][wc(w[d-2], s[d-2], w[d-1], s[d-1], w[0])];
    double c0 = W[U_][wc(w[d-1], s[d-1], w[0], s[0], w[1])];
    if (c1 <= NEG/2 || c0 <= NEG/2) return;
    double tot = acc + c1 + c0;
    if (d == 7) {
      int code = 0; for (int k = 0; k < 7; k++) code = code*5 + w[k];
      if (RB7[code]) return;
      tot -= HOUT[code];
    }
    if (tot <= bar()) return;
    if (forbidden()) return;
    string ws, ss;
    for (int k = 0; k < d; k++) { ws += char('5'+w[k]); ss += char('5'+s[k]); }
    found.emplace_back(tot, ws, ss);
    heap.push(tot); while (heap.size() > many_) heap.pop();
    return;
  }
  for (int sc = 0; sc < 5; sc++) {
    if (i == 0) {} // s_0 free
    s[i] = sc;
    int wnmax = (i + 1 == d - 1) ? 1 : 5;
    for (int wn = 0; wn < wnmax; wn++) {
      int wnext = (i + 1 == d - 1) ? a0w1 : wn;
      w[i+1] = wnext;
      double acc2 = acc;
      if (i >= 1) {
        double c = W[U_][wc(w[i-1], s[i-1], w[i], s[i], w[i+1])];
        if (c <= NEG/2) continue;
        acc2 += c;
      }
      // bound: positions i+1 .. d-2 from state (w_i, s_i, w_{i+1}) at step i+1, plus closing upper bound in G
      double b = acc2 + G[i+1][(w[i]*5 + s[i])*5 + w[i+1]];
      if (i == 0) b = acc2 + G[1][(w[0]*5 + s[0])*5 + w[1]];
      if (b <= bar()) continue;
      dfs(i + 1, acc2);
    }
  }
}
int main(int argc, char** argv) {
  // argv[1] = pattern file, argv[2] = RBIG7 file (raw 7-letter words, letters 5..9)
  ifstream pf(argv[1]); int d, n;
  int npat = 0;
  while (pf >> d >> n) {
    vector<pair<int,int>> sm(n);
    for (auto &q : sm) pf >> q.first >> q.second;
    // dihedral images
    set<vector<pair<int,int>>> imgs;
    for (int refl = 0; refl < 2; refl++) for (int r = 0; r < d; r++) {
      map<int,int> m; bool ok = true;
      for (auto &q : sm) {
        int sl = q.first, nsl;
        if (sl < d) { int i = sl; int j = refl ? ((-i % d) + d) % d : i; nsl = (j + r) % d; }
        else { int i = sl - d; int j = refl ? (((-i - 1) % d) + d) % d : i; nsl = d + (j + r) % d; }
        if (m.count(nsl)) { m[nsl] &= q.second; if (!m[nsl]) ok = false; } else m[nsl] = q.second;
      }
      if (!ok) continue;
      vector<pair<int,int>> v(m.begin(), m.end());
      imgs.insert(v);
    }
    for (auto &v : imgs) { pats[d].push_back({d, v}); }
    npat++;
  }
  ifstream rf(argv[2]); string ww;
  while (rf >> ww) { int code = 0; for (char c : ww) code = code*5 + (c - '5'); RB7[code] = true; }
  fprintf(stderr, "sepb: %d patterns loaded\n", npat);
  for (int u = 0; u < 10; u++) for (int k = 0; k < 3125; k++) W[u][k] = NEG;
  string cmd;
  while (cin >> cmd) {
    if (cmd == "T") { int u; cin >> u; for (int k = 0; k < 3125; k++) { double x; cin >> x; W[u][k] = (x < -1e200) ? NEG : x; } }
    else if (cmd == "H") { for (int k = 0; k < 78125; k++) cin >> HOUT[k]; }
    else if (cmd == "Q") {
      cin >> d_ >> thr_ >> many_;
      U_ = min(d_, 9) - 5 + 5;  // letter value 7..9 used as index
      U_ = min(d_, 9);
      nodes = 0; found.clear(); heap = decltype(heap)();
      for (a0w1 = 0; a0w1 < 5; a0w1++) for (int a0s = 0; a0s < 5; a0s++) for (a0w0 = 0; a0w0 < 5; a0w0++) {
        int dd = d_;
        w[dd-1] = a0w1; s[dd-1] = a0s; w[0] = a0w0;
        // backward DP G[k][(w_{k-1}, s_{k-1}, w_k)] = max over completion of contributions of positions k..d-2,
        // plus positions d-1 and 0 (which need s_0, w_1: maximised over them consistently with the path)
        // Simplification: G[k][state] covers positions k..d-2 exactly, plus an upper bound for positions d-1 and 0.
        double close[125];   // close[(w_{d-2}, s_{d-2}, w_{d-1})] upper bound on c_{d-1} + c_0 given fixed s_{d-1}, w_0
        for (int a = 0; a < 5; a++) for (int b = 0; b < 5; b++) for (int c = 0; c < 5; c++) {
          int st = (a*5+b)*5+c; close[st] = NEG;
          if (c != a0w1) continue;
          double c1 = W[U_][wc(a, b, c, a0s, a0w0)];
          if (c1 <= NEG/2) continue;
          double best0 = NEG;
          for (int s0 = 0; s0 < 5; s0++) for (int w1 = 0; w1 < 5; w1++) best0 = max(best0, W[U_][wc(c, a0s, a0w0, s0, w1)]);
          if (best0 <= NEG/2) continue;
          close[st] = c1 + best0;
        }
        for (int st = 0; st < 125; st++) G[dd-1][st] = close[st];
        for (int k = dd - 2; k >= 1; k--) {
          for (int st = 0; st < 125; st++) {
            int a = st / 25, b = (st / 5) % 5, c = st % 5;   // (w_{k-1}, s_{k-1}, w_k)
            double best = NEG;
            for (int sc = 0; sc < 5; sc++) for (int wn = 0; wn < 5; wn++) {
              double cw = W[U_][wc(a, b, c, sc, wn)];
              if (cw <= NEG/2) continue;
              double g = G[k+1][(c*5+sc)*5+wn];
              if (g <= NEG/2) continue;
              best = max(best, cw + g);
            }
            G[k][st] = best;
          }
        }
        // G[1][(w_0, s_0, w_1)] : positions 1..d-2 + close. Start DFS at i = 0 (choose s_0, w_1).
        double ub = NEG;
        for (int st = 0; st < 125; st++) if (st / 25 == a0w0) ub = max(ub, G[1][st]);
        if (ub <= bar()) continue;
        dfs(0, 0.0);
      }
      sort(found.begin(), found.end(), [](auto &x, auto &y){ return get<0>(x) > get<0>(y); });
      size_t k = 0;
      for (auto &f : found) { if (k++ >= many_) break; printf("R %.12f %s %s\n", get<0>(f), get<1>(f).c_str(), get<2>(f).c_str()); }
      printf("END %lld\n", nodes); fflush(stdout);
    }
  }
}
