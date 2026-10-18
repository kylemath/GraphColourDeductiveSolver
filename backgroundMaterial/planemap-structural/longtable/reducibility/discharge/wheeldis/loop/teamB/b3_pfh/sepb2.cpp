// Team B round B3: receiver separation for the PFH LP, with receiver patterns (own code), version 2.
// Same model and stdin protocol as sepb.cpp. Difference: the search assigns one slot at a time and its bound is a
// backward DP whose state is the last KS assigned letters, so every pattern whose free slots fall inside a window of
// KS+1 consecutive steps (plus the fixed outer triple) is excluded inside the bound itself, not only at the leaf.
// Patterns that do not fit the window are checked in the search when their last slot is assigned.
// Step order (fixed per outer triple: w_{d-1}, s_{d-1}, w_0):  step 2k+1 = s_k (k = 0..d-2), step 2k = w_k (k = 1..d-2).
// Position i contributes W_U[w_{i-1}, s_{i-1}, w_i, s_i, w_{i+1}]; d = 7 leaves pay H_OUT and skip RBIG7 words.
// Protocol (stdin): "T U" + 3125 doubles | "H" + 78125 doubles | "Q d thr many limit" -> "R val wword sword" lines,
// then "END nodes FULL|TRUNC".
#include <bits/stdc++.h>
using namespace std;
static const double NEG = -1e300;
static const int KS = 6, NS = 15625;       // state = last KS letters (base 5)
double W[10][3125];
double HOUT[78125];
bool RB7[78125];
int d_, U_; double thr_; size_t many_;
long long nodes, limit_; bool trunc_;
priority_queue<double, vector<double>, greater<double>> heap;
vector<tuple<double,string,string>> found;

struct Grp { vector<int> sl; vector<unsigned long long> codes; int ord; bool local; };
vector<Grp> grps[40];
vector<int> nonlocal_at[40][80];
// forb[d][triple][step] : bitset over state*5 + letter (letter = the one assigned at this step)
vector<vector<vector<vector<uint64_t>>>> forb(40);

inline int slot_order(int d, int sl) {
  if (sl < d) { int i = sl; if (i == 0 || i == d - 1) return 0; return 2 * i; }
  int i = sl - d; if (i == d - 1) return 0; return 2 * i + 1;
}
inline int step_slot(int d, int j) { return (j & 1) ? d + (j - 1) / 2 : j / 2; }   // step -> slot
inline int triple_of(int a, int b, int c) { return (a * 5 + b) * 5 + c; }

int Lt[80];          // letters by step (1..N); Lt[0] unused
int Fw1, Fs1, Fw0;   // fixed triple
inline int letter_at_slot(int d, int sl) {
  if (sl == d - 1) return Fw1;
  if (sl == 0) return Fw0;
  if (sl == 2 * d - 1) return Fs1;
  return Lt[slot_order(d, sl)];
}
inline int wc(int a, int b, int c, int e, int f) { return (((a*5+b)*5+c)*5+e)*5+f; }
double bar() { return (heap.size() >= many_) ? max(thr_, heap.top()) : thr_; }

// contribution completing at step j, given the letter at each step <= j (via get) and the fixed triple
template <class F> inline double contrib(int d, int j, F get) {
  int N = 2 * d - 3;
  double c = 0;
  if (j == 2) { double x = W[U_][wc(Fw1, Fs1, Fw0, get(1), get(2))]; if (x <= NEG/2) return NEG; c += x; }
  if (j >= 4 && !(j & 1) && j <= 2 * d - 4) {
    int i = (j - 2) / 2;
    int wim1 = (i >= 2) ? get(2*i - 2) : Fw0;
    double x = W[U_][wc(wim1, get(2*i - 1), get(2*i), get(2*i + 1), get(2*i + 2))];
    if (x <= NEG/2) return NEG; c += x;
  }
  if (j == N) {
    int wd3 = (d - 3 >= 1) ? get(2*d - 6) : Fw0;
    double x = W[U_][wc(wd3, get(2*d - 5), get(2*d - 4), get(2*d - 3), Fw1)];
    if (x <= NEG/2) return NEG; c += x;
    double y = W[U_][wc(get(2*d - 4), get(2*d - 3), Fw1, Fs1, Fw0)];
    if (y <= NEG/2) return NEG; c += y;
  }
  return c;
}

void build_tables(int d) {
  int N = 2 * d - 3;
  forb[d].assign(125, vector<vector<uint64_t>>(N + 1, vector<uint64_t>((NS * 5 + 63) / 64, 0)));
  long long marks = 0;
  for (auto &g : grps[d]) {
    if (!g.local) continue;
    int j = g.ord;
    // slot -> role
    for (auto code : g.codes) {
      // decode letters (slots stored ascending; code is base-5 in that order)
      int n = g.sl.size(); vector<int> let(n);
      unsigned long long c = code;
      for (int k = n - 1; k >= 0; k--) { let[k] = c % 5; c /= 5; }
      int fw1 = -1, fs1 = -1, fw0 = -1, cur = -1;
      int stfix[KS]; for (int k = 0; k < KS; k++) stfix[k] = -1;     // stfix[k] = letter at step j-KS+k
      for (int k = 0; k < n; k++) {
        int sl = g.sl[k], o = slot_order(d, sl);
        if (o == 0) { if (sl == d - 1) fw1 = let[k]; else if (sl == 0) fw0 = let[k]; else fs1 = let[k]; }
        else if (o == j) cur = let[k];
        else stfix[o - (j - KS)] = let[k];
      }
      // enumerate free state digits; digits at steps < 1 are always 0
      vector<int> freek;
      for (int k = 0; k < KS; k++) { int st = j - KS + k; if (st < 1) stfix[k] = 0; else if (stfix[k] < 0) freek.push_back(k); }
      int nf = freek.size(); int tot = 1; for (int k = 0; k < nf; k++) tot *= 5;
      for (int a = 0; a < 5; a++) { if (fw1 >= 0 && a != fw1) continue;
      for (int b = 0; b < 5; b++) { if (fs1 >= 0 && b != fs1) continue;
      for (int e = 0; e < 5; e++) { if (fw0 >= 0 && e != fw0) continue;
        auto &tb = forb[d][triple_of(a, b, e)][j];
        for (int m = 0; m < tot; m++) {
          int dig[KS]; for (int k = 0; k < KS; k++) dig[k] = stfix[k];
          int mm = m; for (int k = 0; k < nf; k++) { dig[freek[k]] = mm % 5; mm /= 5; }
          int st = 0; for (int k = 0; k < KS; k++) st = st * 5 + dig[k];
          int idx = st * 5 + cur;
          tb[idx >> 6] |= 1ULL << (idx & 63); marks++;
        }
      }}}
    }
  }
  fprintf(stderr, "sepb2: d=%d tables built (%lld marks)\n", d, marks);
}
bool built[40];

double G[82][NS];
int N_;
inline bool isforb(int tr, int j, int st, int l) { int idx = st * 5 + l; return (forb[d_][tr][j][idx >> 6] >> (idx & 63)) & 1; }
inline bool nonlocal_hit(int j) {
  for (int gi : nonlocal_at[d_][j]) {
    auto &g = grps[d_][gi];
    unsigned long long c = 0;
    for (int sl : g.sl) c = c * 5 + letter_at_slot(d_, sl);
    if (binary_search(g.codes.begin(), g.codes.end(), c)) return true;
  }
  return false;
}
int TR;
void dfs(int j, int st, double acc) {
  // steps 1..j-1 assigned; st = letters at steps j-KS..j-1
  nodes++;
  if (limit_ && nodes > limit_) { trunc_ = true; return; }
  int d = d_, N = N_;
  for (int l = 0; l < 5; l++) {
    if (isforb(TR, j, st, l)) continue;
    Lt[j] = l;
    if (nonlocal_hit(j)) continue;
    double c = contrib(d, j, [&](int o) { return Lt[o]; });
    if (c <= NEG/2) continue;
    int nst = (st * 5 + l) % NS;
    double a2 = acc + c;
    if (j == N) {
      double tot = a2;
      if (d == 7) {
        int code = 0; for (int k = 0; k < 7; k++) code = code * 5 + letter_at_slot(d, k);
        if (RB7[code]) continue;
        tot -= HOUT[code];
      }
      if (tot <= bar()) continue;
      string ws, ss;
      for (int k = 0; k < d; k++) { ws += char('5' + letter_at_slot(d, k)); ss += char('5' + letter_at_slot(d, d + k)); }
      found.emplace_back(tot, ws, ss);
      heap.push(tot); while (heap.size() > many_) heap.pop();
      continue;
    }
    if (a2 + G[j + 1][nst] <= bar()) continue;
    dfs(j + 1, nst, a2);
    if (trunc_) return;
  }
}

int main(int argc, char** argv) {
  ifstream pf(argv[1]); int d, n, npat = 0;
  static map<vector<int>, int> gidx[40];
  while (pf >> d >> n) {
    vector<pair<int,int>> sm(n);
    for (auto &q : sm) pf >> q.first >> q.second;
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
      imgs.insert(vector<pair<int,int>>(m.begin(), m.end()));
    }
    for (auto &v : imgs) {
      vector<int> sl; for (auto &q : v) sl.push_back(q.first);
      auto it = gidx[d].find(sl);
      int gi;
      if (it == gidx[d].end()) {
        gi = grps[d].size(); gidx[d][sl] = gi;
        int mx = 0, mn = 1 << 30;
        for (int x : sl) { int o = slot_order(d, x); mx = max(mx, o); if (o > 0) mn = min(mn, o); }
        bool local = (mx == 0) ? false : (mn >= mx - KS);
        grps[d].push_back({sl, {}, mx, local});
        if (!local) nonlocal_at[d][mx].push_back(gi);
      } else gi = it->second;
      vector<unsigned long long> cur{0};
      for (auto &q : v) {
        vector<unsigned long long> nx;
        for (auto c : cur) for (int l = 0; l < 5; l++) if ((q.second >> l) & 1) nx.push_back(c * 5 + l);
        cur.swap(nx);
      }
      auto &cv = grps[d][gi].codes; cv.insert(cv.end(), cur.begin(), cur.end());
    }
    npat++;
  }
  size_t ncode = 0;
  for (int dd = 0; dd < 40; dd++) for (auto &g : grps[dd]) {
    sort(g.codes.begin(), g.codes.end()); g.codes.erase(unique(g.codes.begin(), g.codes.end()), g.codes.end()); ncode += g.codes.size();
  }
  // a group made only of fixed-triple slots (ord 0) is checked once per triple
  ifstream rf(argv[2]); string ww;
  while (rf >> ww) { int code = 0; for (char c : ww) code = code*5 + (c - '5'); RB7[code] = true; }
  fprintf(stderr, "sepb2: %d patterns loaded, %zu forbidden codes\n", npat, ncode);
  for (int u = 0; u < 10; u++) for (int k = 0; k < 3125; k++) W[u][k] = NEG;
  string cmd;
  while (cin >> cmd) {
    if (cmd == "T") { int u; cin >> u; for (int k = 0; k < 3125; k++) { double x; cin >> x; W[u][k] = (x < -1e200) ? NEG : x; } }
    else if (cmd == "H") { for (int k = 0; k < 78125; k++) cin >> HOUT[k]; }
    else if (cmd == "Q") {
      cin >> d_ >> thr_ >> many_ >> limit_; trunc_ = false;
      U_ = min(d_, 9);
      if (!built[d_]) { build_tables(d_); built[d_] = true; }
      nodes = 0; found.clear(); heap = decltype(heap)();
      int dd = d_, N = 2 * dd - 3; N_ = N;
      for (Fw1 = 0; Fw1 < 5 && !trunc_; Fw1++) for (Fs1 = 0; Fs1 < 5 && !trunc_; Fs1++) for (Fw0 = 0; Fw0 < 5 && !trunc_; Fw0++) {
        TR = triple_of(Fw1, Fs1, Fw0);
        // groups made only of the fixed slots
        bool dead = false;
        for (int gi : nonlocal_at[dd][0]) {
          auto &g = grps[dd][gi]; unsigned long long c = 0;
          for (int sl : g.sl) c = c * 5 + letter_at_slot(dd, sl);
          if (binary_search(g.codes.begin(), g.codes.end(), c)) { dead = true; break; }
        }
        if (dead) continue;
        // backward DP: G[j][st] = max total contribution of steps j..N given letters at steps j-KS..j-1 = st
        for (int st = 0; st < NS; st++) G[N + 1][st] = 0;
        int lo[82];
        for (int j = N; j >= 1; j--) {
          for (int st = 0; st < NS; st++) {
            // reject states with nonzero digits at steps < 1
            bool okst = true;
            for (int k = 0; k < KS; k++) { int sp = j - KS + k; if (sp < 1) { int dg = (st / (int)pow(5, KS - 1 - k)) % 5; if (dg) { okst = false; break; } } }
            if (!okst) { G[j][st] = NEG; continue; }
            int dig[KS]; { int x = st; for (int k = KS - 1; k >= 0; k--) { dig[k] = x % 5; x /= 5; } }
            double best = NEG;
            for (int l = 0; l < 5; l++) {
              if (isforb(TR, j, st, l)) continue;
              int nst = (st * 5 + l) % NS;
              double g = G[j + 1][nst];
              if (g <= NEG/2) continue;
              double c = contrib(dd, j, [&](int o) { return o == j ? l : dig[o - (j - KS)]; });
              if (c <= NEG/2) continue;
              best = max(best, c + g);
            }
            G[j][st] = best;
          }
        }
        (void)lo;
        if (G[1][0] <= bar()) continue;
        dfs(1, 0, 0.0);
      }
      sort(found.begin(), found.end(), [](auto &x, auto &y){ return get<0>(x) > get<0>(y); });
      size_t k = 0;
      for (auto &f : found) { if (k++ >= many_) break; printf("R %.12f %s %s\n", get<0>(f), get<1>(f).c_str(), get<2>(f).c_str()); }
      printf("END %lld %s\n", nodes, trunc_ ? "TRUNC" : "FULL"); fflush(stdout);
    }
  }
}
