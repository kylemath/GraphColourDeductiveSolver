// Exhaustive 4CT Full-Stack t=0 Unavoidability & Discharging Certificate Generator
//
// Proves c_final(u) <= 0 across all degrees d >= 5 under the 79-part local integer
// discharging rule set (71 RSST + 8 N2 unit parts) using ONLY [L]/[E2] reducible
// configurations, with strict global-chirality rotOK (RotOcc) verification.
//
// Outputs:
//   data/cert_karp_tail_d15.json  -- Exact 3,125-window c+ table & tail bound for d >= 15
//   data/certs/cert_d{5..17}.jsonl -- Explicit replayable DFS + rotOK witness certificates
//   data/certs/summary.json       -- Per-degree audit statistics & configuration usage

#include <algorithm>
#include <cassert>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>

struct Range {
    int lo, hi;
    bool is_full() const { return lo == 5 && hi == 9; }
    bool contains(int v) const { return lo <= v && v <= hi; }
};

struct Sub {
    Range sp;
    Range hat;
    std::vector<Range> fans;
};

struct Part {
    std::string tag;
    int n;
    std::vector<Sub> subs;
};

struct Slot {
    int kind; // 0 = 'I' (interior), 1 = 'R' (ring)
    int val;
};

struct Config {
    int id;
    std::string name;
    std::string source;
    std::string kind;
    std::string tier;
    int rim_pinned;
    int ring;
    int m;
    std::vector<int> deg;
    std::vector<std::vector<Slot>> rot;
    std::vector<std::vector<int>> int_adj;
    std::vector<std::set<int>> ring_set;
    std::vector<int> order;
    std::map<int, int> dm;
    int priority;
};

static int config_priority(const Config& c) {
    // Prefer Lean [L] RSST -> [E2] RSST -> 2.126 [L] -> P20 [L] -> L7 [L] -> [E2] D-subs -> [E2] rim-free windows
    if (c.source == "RSST_582") return (c.tier == "L") ? 0 : 1;
    if (c.source == "RSST_2o126_LEAN") return 2;
    if (c.source == "SUB_WINDOW" && c.tier == "L") return 3;
    if (c.source == "SUB_NL51") return (c.tier == "L") ? 4 : 5;
    if (c.source == "SUB_WINDOW" && c.rim_pinned == 0) return 6;
    return 7;
}

static void verify_config_self_rotok(const Config& c) {
    assert(c.m >= 1);
    for (int a = 0; a < c.m; ++a) {
        int g = (int)c.rot[a].size();
        assert(g == c.deg[a] && g >= 5);
        std::set<int> seen_i, seen_r;
        for (int k = 0; k < g; ++k) {
            const Slot& s = c.rot[a][k];
            if (s.kind == 0) {
                assert(0 <= s.val && s.val < c.m && s.val != a);
                seen_i.insert(s.val);
            } else {
                assert(0 <= s.val && s.val < c.ring);
                // Distinct ring slots around a single interior vertex
                assert(seen_r.find(s.val) == seen_r.end());
                seen_r.insert(s.val);
            }
        }
        assert((int)seen_i.size() == (int)c.int_adj[a].size());
        // slotTri (COccBridge.lean:52-54): a ring slot adjacent to an interior slot b in rot[a]
        // must be a listed ring neighbour of b as well.
        for (int k = 0; k < g; ++k) {
            const Slot& s0 = c.rot[a][k];
            const Slot& s1 = c.rot[a][(k + 1) % g];
            if (s1.kind == 0 && s0.kind == 1) {
                assert(c.ring_set[s1.val].count(s0.val) > 0);
            }
            if (s0.kind == 0 && s1.kind == 1) {
                assert(c.ring_set[s0.val].count(s1.val) > 0);
            }
        }
    }
}

static void compute_search_order(Config& c) {
    std::vector<bool> vis(c.m, false);
    c.order.clear();
    int best0 = 0;
    for (int u = 1; u < c.m; ++u) {
        if (std::make_pair(c.deg[u], (int)c.int_adj[u].size()) >
            std::make_pair(c.deg[best0], (int)c.int_adj[best0].size())) {
            best0 = u;
        }
    }
    c.order.push_back(best0);
    vis[best0] = true;
    while ((int)c.order.size() < c.m) {
        int best = -1;
        std::pair<int, int> best_sc(-1, -1);
        for (int u = 0; u < c.m; ++u) {
            if (vis[u]) continue;
            int conn = 0;
            for (int nb : c.int_adj[u]) if (vis[nb]) ++conn;
            std::pair<int, int> sc(conn, c.deg[u]);
            if (sc > best_sc) {
                best_sc = sc;
                best = u;
            }
        }
        c.order.push_back(best);
        vis[best] = true;
    }
}

// --- 2-Ball Window Representation ---
static inline int npriv(int L) {
    if (L == 5) return 0;
    if (L >= 9) return 3;
    return L - 5;
}

// Window vertex codes:
//   u        : 0
//   w_i      : 1 + i                (0 <= i < d)
//   s_i      : 1 + d + i            (0 <= i < d)
//   p_{i,j}  : 1 + 2*d + 3*i + j-1  (0 <= i < d, 1 <= j <= npriv(L_i))
//   open 'R' : -1
struct Window {
    int d;
    std::vector<int> link;
    std::vector<int> rot_u;
    std::vector<std::vector<int>> rot_w;
    std::vector<std::vector<int>> seg;
    std::unordered_map<int, int> r2prev, r2next;

    Window(int d_, const std::vector<int>& link_) : d(d_), link(link_), rot_w(d_), seg(d_) {
        for (int i = 0; i < d; ++i) rot_u.push_back(1 + i);
        std::vector<int> R2;
        for (int i = 0; i < d; ++i) {
            int k = npriv(link[i]);
            int s_prev = 1 + d + ((i + d - 1) % d);
            int s_cur = 1 + d + i;
            seg[i].push_back(s_prev);
            for (int j = 1; j <= k; ++j) {
                seg[i].push_back(1 + 2 * d + 3 * i + (j - 1));
            }
            seg[i].push_back(s_cur);

            rot_w[i].push_back(0);
            rot_w[i].push_back(1 + ((i + d - 1) % d));
            for (int v : seg[i]) rot_w[i].push_back(v);
            rot_w[i].push_back(1 + ((i + 1) % d));

            for (size_t t = 0; t + 1 < seg[i].size(); ++t) R2.push_back(seg[i][t]);
        }
        int n = (int)R2.size();
        for (int t = 0; t < n; ++t) {
            r2prev[R2[t]] = R2[(t + n - 1) % n];
            r2next[R2[t]] = R2[(t + 1) % n];
        }
    }

    // Returns: kind 0 = dec(val), kind 1 = var(var_code), kind 2 = open
    std::pair<int, int> deg_info(int v) const {
        if (v == -1) return {2, 0};
        if (v == 0) return {0, std::min(d, 9)};
        if (v >= 1 && v <= d) return {0, link[v - 1]};
        if (v >= 1 + d && v <= 2 * d) return {1, 100 + (v - 1 - d)};
        int q = v - 1 - 2 * d;
        int i = q / 3, j = (q % 3) + 1;
        assert(!(link[i] >= 9 && j == 2)); // 9+ middle private is never read!
        return {1, 200 + 3 * i + (j - 1)};
    }

    int succ(int x, int y) const {
        if (x == -1) return -1;
        if (x == 0) {
            for (int k = 0; k < d; ++k) if (rot_u[k] == y) return rot_u[(k + 1) % d];
            assert(false);
        }
        if (x >= 1 && x <= d) {
            const auto& L = rot_w[x - 1];
            int sz = (int)L.size();
            for (int k = 0; k < sz; ++k) if (L[k] == y) return L[(k + 1) % sz];
            assert(false);
        }
        int prev = r2prev.at(x), nxt = r2next.at(x);
        if (x >= 1 + d && x <= 2 * d) {
            int i = x - 1 - d;
            int w1 = 1 + ((i + 1) % d), w0 = 1 + i;
            if (y == w1) return w0;
            if (y == w0) return prev;
            if (y == prev) return -1;
            if (y == nxt) return w1;
            return -1;
        }
        int q = x - 1 - 2 * d;
        int wi = 1 + (q / 3);
        if (y == wi) return prev;
        if (y == prev) return -1;
        if (y == nxt) return wi;
        return -1;
    }
};

struct Cond {
    int var_code;
    int lo, hi;
    bool operator<(const Cond& o) const {
        return std::tie(var_code, lo, hi) < std::tie(o.var_code, o.lo, o.hi);
    }
    bool operator==(const Cond& o) const {
        return std::tie(var_code, lo, hi) == std::tie(o.var_code, o.lo, o.hi);
    }
};

struct Inst {
    std::vector<Cond> conds;
    bool open;
    int hub_w; // -1 for u, 0..d-1 for w_i
};

static bool test_vertex(const Window& W, int v, const Range& r, std::vector<Cond>& conds, bool& open_flag) {
    if (r.is_full()) return true;
    auto [kind, val] = W.deg_info(v);
    if (kind == 0) {
        return r.contains(val);
    } else if (kind == 2) {
        open_flag = true;
        return true;
    } else {
        conds.push_back({val, r.lo, r.hi});
        return true;
    }
}

static bool fit_part(const Window& W, int h, const Part& part, int a, Inst& out_inst) {
    const std::vector<int>& S = (h == 0) ? W.rot_u : W.rot_w[h - 1];
    int n = part.n;
    if ((int)S.size() != n) return false;
    std::vector<Cond> conds;
    bool open_flag = false;
    for (int j = 0; j < n; ++j) {
        const Sub& sb = part.subs[j];
        int x = S[(a + j) % n];
        int xp = S[(a + j + n - 1) % n];
        int xn = S[(a + j + 1) % n];
        if (!test_vertex(W, x, sb.sp, conds, open_flag)) return false;
        if (!sb.hat.is_full()) {
            if (!test_vertex(W, W.succ(x, xp), sb.hat, conds, open_flag)) return false;
        }
        bool any_fan = false;
        for (const auto& f : sb.fans) if (!f.is_full()) any_fan = true;
        if (any_fan) {
            if (x == 0 || (x >= 1 && x <= W.d)) {
                int hv = W.succ(x, xp);
                int hn = W.succ(xn, x);
                const std::vector<int>& Rr = (x == 0) ? W.rot_u : W.rot_w[x - 1];
                int rsz = (int)Rr.size();
                int idx_hv = -1;
                for (int k = 0; k < rsz; ++k) if (Rr[k] == hv) { idx_hv = k; break; }
                assert(idx_hv != -1);
                int t = (idx_hv + 1) % rsz;
                std::vector<int> F;
                int guard = 0;
                while (Rr[t] != hn) {
                    F.push_back(Rr[t]);
                    t = (t + 1) % rsz;
                    if (++guard > rsz) return false;
                }
                if (F.size() != sb.fans.size()) return false;
                for (size_t fi = 0; fi < F.size(); ++fi) {
                    if (!test_vertex(W, F[fi], sb.fans[fi], conds, open_flag)) return false;
                }
            } else {
                open_flag = true;
            }
        }
    }
    out_inst.conds = std::move(conds);
    out_inst.open = open_flag;
    out_inst.hub_w = (h == 0) ? -1 : (h - 1);
    return true;
}

static void build_instances(const Window& W, const std::vector<Part>& parts,
                            std::vector<Inst>& ins, std::vector<Inst>& outs) {
    ins.clear();
    outs.clear();
    if (5 <= W.d && W.d <= 8) {
        for (const auto& p : parts) {
            if (p.n != W.d) continue;
            for (int a = 0; a < W.d; ++a) {
                Inst inst;
                if (fit_part(W, 0, p, a, inst)) outs.push_back(std::move(inst));
            }
        }
    }
    for (int i = 0; i < W.d; ++i) {
        int L = W.link[i];
        if (L > 8) continue;
        for (const auto& p : parts) {
            if (p.n != L) continue;
            int a = L - 2;
            assert(W.rot_w[i][(a + 2) % L] == 0);
            Inst inst;
            if (fit_part(W, 1 + i, p, a, inst)) ins.push_back(std::move(inst));
        }
    }
}

// --- Strict Global-Chirality rotOK (RotOcc) Verification ---
static bool check_rot_ok(int d, const std::vector<int>& link, const Config& cfg,
                         const std::vector<int>& phi, int& out_sigma, std::vector<int>& out_shifts) {
    // Build exact R2 boundary cycle Z (splitting 9+ middle into two distinct non-hosts q_{i,L} != q_{i,R})
    std::vector<int> Z;
    std::unordered_map<int, int> pos_in_Z;
    for (int i = 0; i < d; ++i) {
        int L = link[i];
        if (L == 9) {
            int p1 = 1 + 2 * d + 3 * i + 0;
            int qL = 1000 + 2 * i + 0;
            int qR = 1000 + 2 * i + 1;
            int p3 = 1 + 2 * d + 3 * i + 2;
            int si = 1 + d + i;
            for (int v : {p1, qL, qR, p3, si}) {
                pos_in_Z[v] = (int)Z.size();
                Z.push_back(v);
            }
        } else {
            for (int j = 1; j <= L - 5; ++j) {
                int pj = 1 + 2 * d + 3 * i + (j - 1);
                pos_in_Z[pj] = (int)Z.size();
                Z.push_back(pj);
            }
            int si = 1 + d + i;
            pos_in_Z[si] = (int)Z.size();
            Z.push_back(si);
        }
    }
    int M = (int)Z.size();
    std::vector<int> uf(M);
    std::iota(uf.begin(), uf.end(), 0);
    auto uf_find = [&](auto& self, int x) -> int {
        return uf[x] == x ? x : uf[x] = self(self, uf[x]);
    };
    auto uf_union = [&](int a, int b) {
        a = uf_find(uf_find, a);
        b = uf_find(uf_find, b);
        if (a != b) uf[b] = a;
    };

    // Only an apex s_i mapped to an interior vertex of exact degree 5 merges its two outside triangles
    for (int a = 0; a < cfg.m; ++a) {
        int h = phi[a];
        if (1 + d <= h && h < 1 + 2 * d && cfg.deg[a] == 5) {
            int t = pos_in_Z.at(h);
            uf_union((t + M - 1) % M, t);
        }
    }

    int next_fresh = 3000;
    std::vector<std::vector<int>> rf(cfg.m);
    std::set<int> phi_set(phi.begin(), phi.end());
    if ((int)phi_set.size() != cfg.m) return false;

    for (int a = 0; a < cfg.m; ++a) {
        int h = phi[a];
        int g = cfg.deg[a];
        auto& r = rf[a];
        if (h == 0) {
            if (d != g) return false;
            for (int i = 0; i < d; ++i) r.push_back(1 + i);
        } else if (1 <= h && h <= d) {
            int i = h - 1;
            if (link[i] > 8 || link[i] != g) return false;
            r.push_back(0);
            r.push_back(1 + ((i + d - 1) % d));
            r.push_back(1 + d + ((i + d - 1) % d));
            for (int j = 1; j <= link[i] - 5; ++j) r.push_back(1 + 2 * d + 3 * i + (j - 1));
            r.push_back(1 + d + i);
            r.push_back(1 + ((i + 1) % d));
        } else if (1 + d <= h && h < 1 + 2 * d) {
            if (g < 5 || g > 8) return false;
            int i = h - 1 - d;
            int t = pos_in_Z.at(h);
            int prev = Z[(t + M - 1) % M];
            int nxt = Z[(t + 1) % M];
            r.push_back(nxt);
            r.push_back(1 + ((i + 1) % d));
            r.push_back(1 + i);
            r.push_back(prev);
            if (g == 5) {
                r.push_back(2000 + uf_find(uf_find, (t + M - 1) % M));
            } else {
                r.push_back(2000 + uf_find(uf_find, (t + M - 1) % M));
                for (int k = 0; k < g - 6; ++k) r.push_back(next_fresh++);
                r.push_back(2000 + uf_find(uf_find, t));
            }
        } else {
            if (g < 5 || g > 8) return false;
            int q = h - 1 - 2 * d;
            int i = q / 3;
            int j = (q % 3) + 1;
            if (link[i] >= 9 && j == 2) return false;
            int t = pos_in_Z.at(h);
            int prev = Z[(t + M - 1) % M];
            int nxt = Z[(t + 1) % M];
            r.push_back(nxt);
            r.push_back(1 + i);
            r.push_back(prev);
            r.push_back(2000 + uf_find(uf_find, (t + M - 1) % M));
            for (int k = 0; k < g - 5; ++k) r.push_back(next_fresh++);
            r.push_back(2000 + uf_find(uf_find, t));
        }
        if ((int)r.size() != g) return false;
        std::set<int> uniq(r.begin(), r.end());
        if ((int)uniq.size() != g) return false;
    }

    for (int sg : {1, -1}) {
        std::vector<int> shifts(cfg.m, -1);
        std::vector<int> rho(cfg.ring, -1);

        auto dfs_rot = [&](auto& self, int step) -> bool {
            if (step == cfg.m) return true;
            int a = cfg.order[step];
            int g = cfg.deg[a];
            const auto& rc = cfg.rot[a];
            const auto& rfa = rf[a];

            // Narrow candidate shifts if a has an interior neighbour
            std::vector<int> cand_shifts;
            int first_i_pos = -1, first_i_nb = -1;
            for (int k = 0; k < g; ++k) {
                if (rc[k].kind == 0) {
                    first_i_pos = k;
                    first_i_nb = rc[k].val;
                    break;
                }
            }
            if (first_i_pos != -1) {
                int target = phi[first_i_nb];
                for (int idx = 0; idx < g; ++idx) {
                    if (rfa[idx] == target) {
                        int sh = ((idx - sg * first_i_pos) % g + g) % g;
                        cand_shifts.push_back(sh);
                    }
                }
            } else {
                for (int sh = 0; sh < g; ++sh) cand_shifts.push_back(sh);
            }

            for (int sh : cand_shifts) {
                bool ok = true;
                std::vector<std::pair<int, int>> added_rho;
                for (int k = 0; k < g; ++k) {
                    int fv = rfa[((sh + sg * k) % g + g) % g];
                    if (rc[k].kind == 0) {
                        if (fv != phi[rc[k].val]) { ok = false; break; }
                    } else {
                        if (phi_set.count(fv)) { ok = false; break; } // RotOcc.disj
                        int r_idx = rc[k].val;
                        if (rho[r_idx] == -1) {
                            rho[r_idx] = fv;
                            added_rho.push_back({r_idx, -1});
                        } else if (rho[r_idx] != fv) {
                            ok = false;
                            break;
                        }
                    }
                }
                if (ok) {
                    shifts[a] = sh;
                    if (self(self, step + 1)) return true;
                }
                for (auto [ri, oldv] : added_rho) rho[ri] = oldv;
            }
            return false;
        };

        if (dfs_rot(dfs_rot, 0)) {
            out_sigma = sg;
            out_shifts = std::move(shifts);
            return true;
        }
    }
    return false;
}

struct EmbWitness {
    std::vector<std::pair<int, int>> req; // sorted (var_code, deg)
    int cfg_id;
    int priority;
    std::vector<int> phi;
    int sigma;
    std::vector<int> shifts;
};

static std::vector<EmbWitness> find_link_embeddings(
    const Window& W, const std::vector<Config>& active_cfgs, const std::set<int>& rel_vars) {
    // Build host graph on relevant/fixed exact-degree hosts
    std::vector<int> hosts;
    std::unordered_map<int, std::set<int>> host_degs;
    std::unordered_map<int, int> host_var; // only for variable hosts

    hosts.push_back(0);
    host_degs[0] = {W.d};
    for (int i = 0; i < W.d; ++i) {
        if (W.link[i] <= 8) {
            hosts.push_back(1 + i);
            host_degs[1 + i] = {W.link[i]};
        }
        int sv = 1 + W.d + i;
        int sc = 100 + i;
        if (rel_vars.count(sc)) {
            hosts.push_back(sv);
            host_degs[sv] = {5, 6, 7, 8};
            host_var[sv] = sc;
        }
        int k = npriv(W.link[i]);
        for (int j = 1; j <= k; ++j) {
            if (W.link[i] >= 9 && j == 2) continue;
            int pv = 1 + 2 * W.d + 3 * i + (j - 1);
            int pc = 200 + 3 * i + (j - 1);
            if (rel_vars.count(pc)) {
                hosts.push_back(pv);
                host_degs[pv] = {5, 6, 7, 8};
                host_var[pv] = pc;
            }
        }
    }

    std::unordered_map<int, std::set<int>> adj_set;
    for (int h : hosts) adj_set[h] = {};
    auto add_e = [&](int a, int b) {
        if (a != b && host_degs.count(a) && host_degs.count(b)) {
            adj_set[a].insert(b);
            adj_set[b].insert(a);
        }
    };
    for (int i = 0; i < W.d; ++i) {
        add_e(0, 1 + i);
        add_e(1 + i, 1 + ((i + 1) % W.d));
        add_e(1 + W.d + i, 1 + ((i + 1) % W.d));
        const auto& sg = W.seg[i];
        for (size_t t = 0; t < sg.size(); ++t) {
            add_e(1 + i, sg[t]);
            if (t + 1 < sg.size()) add_e(sg[t], sg[t + 1]);
        }
    }
    std::unordered_map<int, std::vector<int>> adj_vec;
    for (auto& [h, st] : adj_set) {
        adj_vec[h] = std::vector<int>(st.begin(), st.end());
    }

    std::map<int, int> hc;
    for (auto& [h, st] : host_degs) {
        for (int x : st) hc[x]++;
    }

    // Best rotOK witness per distinct requirement vector across ALL active configs
    std::map<std::vector<std::pair<int, int>>, EmbWitness> best_by_req;

    for (const auto& cfg : active_cfgs) {
        if (cfg.m > (int)hosts.size()) continue;
        bool deg_ok = true;
        for (auto [dg, cnt] : cfg.dm) {
            if (hc[dg] < cnt) { deg_ok = false; break; }
        }
        if (!deg_ok) continue;

        std::vector<int> phi(cfg.m, -1);
        std::set<int> used_h;

        auto rec = [&](auto& self, int k) -> void {
            if (k == cfg.m) {
                std::vector<std::pair<int, int>> req;
                for (int u = 0; u < cfg.m; ++u) {
                    auto it = host_var.find(phi[u]);
                    if (it != host_var.end()) req.push_back({it->second, cfg.deg[u]});
                }
                std::sort(req.begin(), req.end());
                auto it_b = best_by_req.find(req);
                if (it_b != best_by_req.end() &&
                    std::make_pair(it_b->second.priority, it_b->second.cfg_id) <=
                    std::make_pair(cfg.priority, cfg.id)) {
                    return; // Already have an equal-or-higher-priority rotOK witness for this exact req!
                }
                int sg = 0;
                std::vector<int> shifts;
                if (check_rot_ok(W.d, W.link, cfg, phi, sg, shifts)) {
                    best_by_req[req] = EmbWitness{req, cfg.id, cfg.priority, phi, sg, std::move(shifts)};
                }
                return;
            }
            int x = cfg.order[k];
            std::vector<int> placed_int_nbs;
            for (int prev_idx = 0; prev_idx < k; ++prev_idx) {
                int y = cfg.order[prev_idx];
                if (std::binary_search(cfg.int_adj[x].begin(), cfg.int_adj[x].end(), y)) {
                    placed_int_nbs.push_back(y);
                }
            }
            const std::vector<int>& cands = placed_int_nbs.empty() ? hosts : adj_vec[phi[placed_int_nbs[0]]];
            for (int t : cands) {
                if (used_h.count(t)) continue;
                if (!host_degs[t].count(cfg.deg[x])) continue;
                bool ind_ok = true;
                for (int prev_idx = 0; prev_idx < k; ++prev_idx) {
                    int y = cfg.order[prev_idx];
                    bool in_E = std::binary_search(cfg.int_adj[x].begin(), cfg.int_adj[x].end(), y);
                    bool in_H = adj_set[t].count(phi[y]) > 0;
                    if (in_E != in_H) { ind_ok = false; break; }
                }
                if (!ind_ok) continue;
                phi[x] = t;
                used_h.insert(t);
                self(self, k + 1);
                used_h.erase(t);
                phi[x] = -1;
            }
        };
        rec(rec, 0);
    }

    // Prune non-minimal requirements (keep smaller reqs first, then priority)
    std::vector<EmbWitness> raw;
    raw.reserve(best_by_req.size());
    for (auto& [rq, ew] : best_by_req) raw.push_back(std::move(ew));
    std::sort(raw.begin(), raw.end(), [](const EmbWitness& a, const EmbWitness& b) {
        if (a.req.size() != b.req.size()) return a.req.size() < b.req.size();
        if (a.priority != b.priority) return a.priority < b.priority;
        return a.cfg_id < b.cfg_id;
    });

    std::vector<EmbWitness> keep;
    for (auto& ew : raw) {
        bool subsumed = false;
        for (const auto& kw : keep) {
            if (std::includes(ew.req.begin(), ew.req.end(), kw.req.begin(), kw.req.end())) {
                subsumed = true;
                break;
            }
        }
        if (!subsumed) keep.push_back(std::move(ew));
    }
    return keep;
}

// --- Deterministic Symbolic DFS (matches RSSTCheckCore / verify_4ct_t0.py) ---
static std::tuple<int, int, int> site_key(int c) {
    if (c < 200) return {c - 100, 0, 0};
    return {(c - 200) / 3, 1, (c - 200) % 3};
}

static std::vector<std::vector<int>> classes_of(int v, const std::vector<Inst>& allc) {
    std::vector<std::pair<int, int>> ts;
    for (const auto& inst : allc) {
        for (const auto& cd : inst.conds) {
            if (cd.var_code == v) ts.push_back({cd.lo, cd.hi});
        }
    }
    auto pat = [&](int x) {
        std::vector<bool> p;
        p.reserve(ts.size());
        for (auto [lo, hi] : ts) p.push_back(lo <= x && x <= hi);
        return p;
    };
    auto p9 = pat(9);
    std::vector<int> c9;
    std::vector<std::vector<int>> out;
    for (int x : {5, 6, 7, 8, 9}) {
        if (pat(x) == p9) c9.push_back(x);
    }
    out.push_back(c9);
    for (int x : {5, 6, 7, 8}) {
        if (pat(x) != p9) out.push_back({x});
    }
    return out;
}

static bool simp1(int v, const std::vector<int>& S, const Inst& inst, Inst& out) {
    for (const auto& cd : inst.conds) {
        if (cd.var_code == v) {
            bool any_true = false;
            for (int l : S) if (cd.lo <= l && l <= cd.hi) { any_true = true; break; }
            if (!any_true) return false;
        }
    }
    out.open = inst.open;
    out.hub_w = inst.hub_w;
    out.conds.clear();
    for (const auto& cd : inst.conds) {
        if (cd.var_code == v) {
            bool all_true = true;
            for (int l : S) if (!(cd.lo <= l && l <= cd.hi)) { all_true = false; break; }
            if (all_true) continue;
        }
        out.conds.push_back(cd);
    }
    return true;
}

struct ActiveReq {
    std::vector<std::pair<int, int>> req;
    int idx;
};

static bool simpR1(int v, const std::vector<int>& S, const ActiveReq& r, ActiveReq& out) {
    for (auto [c, l] : r.req) {
        if (c == v) {
            if (S.size() != 1 || S[0] != l) return false;
        }
    }
    out.idx = r.idx;
    out.req.clear();
    for (auto [c, l] : r.req) {
        if (c != v) out.req.push_back({c, l});
    }
    return true;
}

struct DfsStats {
    long long nodes = 0;
    long long ub_leaves = 0;
    long long kill_leaves = 0;
};

static bool run_dfs(int base, int depth, const std::vector<std::pair<int, std::vector<std::vector<int>>>>& vs,
                    const std::vector<Inst>& ins, const std::vector<Inst>& outs,
                    const std::vector<ActiveReq>& reqs, std::set<int>& used_embs, DfsStats& st) {
    st.nodes++;
    int sure_outs = 0;
    for (const auto& o : outs) {
        if (o.conds.empty() && !o.open) sure_outs++;
    }
    int ub = base + (int)ins.size() - sure_outs;
    if (ub <= 0) {
        st.ub_leaves++;
        return true;
    }
    int pick = -1;
    for (const auto& r : reqs) {
        if (r.req.empty()) {
            if (used_embs.count(r.idx)) { pick = r.idx; break; }
            if (pick == -1) pick = r.idx;
        }
    }
    if (pick != -1) {
        used_embs.insert(pick);
        st.kill_leaves++;
        return true;
    }
    if (depth == (int)vs.size()) return false;

    int v = vs[depth].first;
    const auto& cls = vs[depth].second;
    for (const auto& S : cls) {
        std::vector<Inst> i2, o2;
        std::vector<ActiveReq> r2;
        i2.reserve(ins.size());
        o2.reserve(outs.size());
        r2.reserve(reqs.size());
        for (const auto& x : ins) {
            Inst y;
            if (simp1(v, S, x, y)) i2.push_back(std::move(y));
        }
        for (const auto& x : outs) {
            Inst y;
            if (simp1(v, S, x, y)) o2.push_back(std::move(y));
        }
        for (const auto& x : reqs) {
            ActiveReq y;
            if (simpR1(v, S, x, y)) r2.push_back(std::move(y));
        }
        if (!run_dfs(base, depth + 1, vs, i2, o2, r2, used_embs, st)) return false;
    }
    return true;
}

// --- Exact 3,125-Window c+ Table & Canonical Link Word Enumeration ---
static int maxsat(const std::vector<Inst>& insts) {
    std::set<int> vset;
    for (const auto& I : insts) for (const auto& c : I.conds) vset.insert(c.var_code);
    std::vector<int> names(vset.begin(), vset.end());
    int nv = (int)names.size();
    std::unordered_map<int, int> pos;
    for (int k = 0; k < nv; ++k) pos[names[k]] = k;
    std::vector<std::vector<std::tuple<int, int, int>>> by(nv);
    for (int t = 0; t < (int)insts.size(); ++t) {
        for (const auto& c : insts[t].conds) {
            by[pos[c.var_code]].push_back({t, c.lo, c.hi});
        }
    }
    std::vector<int> dead_cnt(insts.size(), 0);
    int best = 0;
    auto rec = [&](auto& self, int k, int ub) -> void {
        if (ub <= best) return;
        if (k == nv) { best = ub; return; }
        for (int val : {5, 6, 7, 8, 9}) {
            int nub = ub;
            for (auto [t, lo, hi] : by[k]) {
                if (!(lo <= val && val <= hi)) {
                    if (dead_cnt[t] == 0) nub--;
                    dead_cnt[t]++;
                }
            }
            self(self, k + 1, nub);
            for (auto [t, lo, hi] : by[k]) {
                if (!(lo <= val && val <= hi)) dead_cnt[t]--;
            }
        }
    };
    rec(rec, 0, (int)insts.size());
    return best;
}

static bool is_dihedral_canon(const std::vector<int>& w) {
    int d = (int)w.size();
    for (int r = 0; r < d; ++r) {
        std::vector<int> rot(d), rev(d);
        for (int i = 0; i < d; ++i) {
            rot[i] = w[(i + r) % d];
            rev[i] = w[(r - i % d + d) % d];
        }
        if (rot < w || rev < w) return false;
    }
    return true;
}

static std::vector<std::vector<int>> gen_canon_links_small(int d) {
    std::vector<std::vector<int>> out;
    std::vector<int> cur(d, 5);
    auto rec = [&](auto& self, int k) -> void {
        if (k == d) {
            if (is_dihedral_canon(cur)) out.push_back(cur);
            return;
        }
        for (int v = 5; v <= 9; ++v) {
            if (k > 0 && v < cur[0]) continue;
            cur[k] = v;
            self(self, k + 1);
        }
    };
    rec(rec, 0);
    return out;
}

static std::vector<std::vector<int>> gen_cplus_words(int d, const int CP[5][5][5][5][5], const int cmax[10]) {
    std::vector<std::vector<int>> out;
    int base = 10 * (6 - d);
    std::vector<int> L(d, 0);
    auto partial_bound = [&](int k) {
        int s = base;
        for (int i = 0; i < d; ++i) {
            if (i - 2 >= 0 && i + 2 <= k - 1) {
                s += CP[L[i - 2] - 5][L[i - 1] - 5][L[i] - 5][L[i + 1] - 5][L[i + 2] - 5];
            } else if (i <= k - 1) {
                s += cmax[L[i]];
            } else {
                s += 6;
            }
        }
        return s;
    };
    auto rec = [&](auto& self, int k) -> void {
        if (k == d) {
            if (!is_dihedral_canon(L)) return;
            int cyc = base;
            for (int i = 0; i < d; ++i) {
                cyc += CP[L[(i + d - 2) % d] - 5][L[(i + d - 1) % d] - 5][L[i] - 5]
                         [L[(i + 1) % d] - 5][L[(i + 2) % d] - 5];
            }
            if (cyc > 0) out.push_back(L);
            return;
        }
        for (int v = 5; v <= 9; ++v) {
            if (k > 0 && v < L[0]) continue;
            L[k] = v;
            if (partial_bound(k + 1) > 0) self(self, k + 1);
        }
        L[k] = 0;
    };
    rec(rec, 0);
    return out;
}

static std::string link_str(const std::vector<int>& link) {
    std::string s;
    s.reserve(link.size());
    for (int x : link) s.push_back(char('0' + x));
    return s;
}

int main(int argc, char** argv) {
    std::string data_dir = "/Users/kylemathewson/GraphColouringNov/fullstack_t0/data";
    bool allow_rimpin = false;
    std::string pool_path;
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--allow-rimpin") allow_rimpin = true;
        else if (arg == "--discover-pool" && i + 1 < argc) pool_path = argv[++i];
        else data_dir = arg;
    }

    auto t_start = std::chrono::steady_clock::now();
    std::ifstream fin(data_dir + "/engine_input.txt");
    if (!fin) {
        std::cerr << "Cannot open " << data_dir << "/engine_input.txt\n";
        return 1;
    }

    std::string hdr;
    int nparts = 0;
    fin >> hdr >> nparts;
    assert(hdr == "PARTS" && nparts == 79);
    std::vector<Part> parts(nparts);
    for (int i = 0; i < nparts; ++i) {
        fin >> parts[i].tag >> parts[i].n;
        parts[i].subs.resize(parts[i].n);
        for (int j = 0; j < parts[i].n; ++j) {
            int nf = 0;
            fin >> parts[i].subs[j].sp.lo >> parts[i].subs[j].sp.hi
                >> parts[i].subs[j].hat.lo >> parts[i].subs[j].hat.hi >> nf;
            parts[i].subs[j].fans.resize(nf);
            for (int f = 0; f < nf; ++f) {
                fin >> parts[i].subs[j].fans[f].lo >> parts[i].subs[j].fans[f].hi;
            }
        }
    }

    int ncfgs = 0;
    fin >> hdr >> ncfgs;
    assert(hdr == "CONFIGS" && ncfgs > 0);
    std::vector<Config> all_cfgs(ncfgs), active_cfgs;
    for (int i = 0; i < ncfgs; ++i) {
        Config& c = all_cfgs[i];
        fin >> c.id >> c.name >> c.source >> c.kind >> c.tier >> c.rim_pinned >> c.ring >> c.m;
        assert(c.id == i);
        assert(c.tier == "L" || c.tier == "E2");
        c.deg.resize(c.m);
        c.rot.resize(c.m);
        c.int_adj.resize(c.m);
        c.ring_set.resize(c.m);
        for (int u = 0; u < c.m; ++u) {
            int g = 0;
            fin >> g;
            c.deg[u] = g;
            c.dm[g]++;
            c.rot[u].resize(g);
            for (int k = 0; k < g; ++k) {
                fin >> c.rot[u][k].kind >> c.rot[u][k].val;
                if (c.rot[u][k].kind == 0) c.int_adj[u].push_back(c.rot[u][k].val);
                else c.ring_set[u].insert(c.rot[u][k].val);
            }
            std::sort(c.int_adj[u].begin(), c.int_adj[u].end());
        }
        verify_config_self_rotok(c);
        compute_search_order(c);
        c.priority = config_priority(c);
        if (!allow_rimpin && c.source == "SUB_WINDOW" && c.rim_pinned && c.tier != "L") continue;
        active_cfgs.push_back(c);
    }
    std::cout << "Loaded " << nparts << " parts and " << ncfgs << " verified configs ("
              << active_cfgs.size() << " active; allow_rimpin=" << allow_rimpin << ").\n";

    std::vector<Config> pool_cfgs;
    std::set<std::string> known_names;
    for (const auto& c : all_cfgs) known_names.insert(c.name);
    if (!pool_path.empty()) {
        std::ifstream fpool(pool_path);
        assert(fpool && "Cannot open pool_path");
        std::string phdr;
        int npool = 0;
        fpool >> phdr >> npool;
        assert(phdr == "POOL");
        for (int i = 0; i < npool; ++i) {
            Config c;
            int dummy_id = 0;
            fpool >> dummy_id >> c.name >> c.source >> c.kind >> c.tier >> c.rim_pinned >> c.ring >> c.m;
            c.deg.resize(c.m);
            c.rot.resize(c.m);
            c.int_adj.resize(c.m);
            c.ring_set.resize(c.m);
            for (int u = 0; u < c.m; ++u) {
                int g = 0;
                fpool >> g;
                c.deg[u] = g;
                c.dm[g]++;
                c.rot[u].resize(g);
                for (int k = 0; k < g; ++k) {
                    fpool >> c.rot[u][k].kind >> c.rot[u][k].val;
                    if (c.rot[u][k].kind == 0) c.int_adj[u].push_back(c.rot[u][k].val);
                    else c.ring_set[u].insert(c.rot[u][k].val);
                }
                std::sort(c.int_adj[u].begin(), c.int_adj[u].end());
            }
            if (known_names.count(c.name)) continue;
            c.id = 100000 + (int)pool_cfgs.size();
            verify_config_self_rotok(c);
            compute_search_order(c);
            c.priority = (c.source == "SUB_NL51") ? 10 : 11;
            pool_cfgs.push_back(std::move(c));
        }
        std::cout << "Loaded " << pool_cfgs.size() << " candidate pool configs from " << pool_path << ".\n";
    }
    std::vector<std::string> discovered_names;

    // Step 1: Compute exact 3,125-window c+ table and tail certificate
    int CP[5][5][5][5][5] = {};
    int cmax[10] = {};
    int max_cp_overall = 0;
    for (int a = 5; a <= 9; ++a)
    for (int b = 5; b <= 9; ++b)
    for (int c = 5; c <= 9; ++c)
    for (int d = 5; d <= 9; ++d)
    for (int e = 5; e <= 9; ++e) {
        int val = 0;
        if (c <= 8) {
            Window W(10, {a, b, c, d, e, 5, 5, 5, 5, 5});
            std::vector<Inst> ins, outs;
            build_instances(W, parts, ins, outs);
            std::vector<Inst> w2_ins;
            for (auto& I : ins) if (I.hub_w == 2) w2_ins.push_back(std::move(I));
            val = maxsat(w2_ins);
        }
        CP[a - 5][b - 5][c - 5][d - 5][e - 5] = val;
        cmax[c] = std::max(cmax[c], val);
        max_cp_overall = std::max(max_cp_overall, val);
    }
    std::cout << "Computed exact 3,125-window c+ table: cmax={5:" << cmax[5] << ", 6:" << cmax[6]
              << ", 7:" << cmax[7] << ", 8:" << cmax[8] << ", 9:" << cmax[9]
              << "}, max_cp=" << max_cp_overall << ".\n";
    assert(max_cp_overall == 6);

    {
        std::ofstream fcp(data_dir + "/cert_karp_tail_d15.json");
        fcp << "{\n  \"max_cplus\": " << max_cp_overall << ",\n"
            << "  \"cmax_by_center\": {\"5\": " << cmax[5] << ", \"6\": " << cmax[6]
            << ", \"7\": " << cmax[7] << ", \"8\": " << cmax[8] << ", \"9\": " << cmax[9] << "},\n"
            << "  \"tail_degree_d0\": 15,\n"
            << "  \"tail_formula\": \"10*(6 - d) + 6*d = 60 - 4*d <= 0 for all d >= 15\",\n"
            << "  \"karp_lambda_star_num\": 6,\n"
            << "  \"karp_lambda_star_den\": 1,\n"
            << "  \"cplus_3125\": {\n";
        bool first = true;
        for (int a = 5; a <= 9; ++a)
        for (int b = 5; b <= 9; ++b)
        for (int c = 5; c <= 9; ++c)
        for (int d = 5; d <= 9; ++d)
        for (int e = 5; e <= 9; ++e) {
            if (!first) fcp << ",\n";
            first = false;
            fcp << "    \"" << a << b << c << d << e << "\": " << CP[a - 5][b - 5][c - 5][d - 5][e - 5];
        }
        fcp << "\n  }\n}\n";
    }

    // Step 2: Exhaustive certificate generation across d = 5 .. 17
    std::string cert_dir = data_dir + "/certs";
    std::map<int, long long> global_cfg_uses;
    std::ostringstream summ_deg_json;
    summ_deg_json << "[\n";

    for (int d = 5; d <= 17; ++d) {
        auto td0 = std::chrono::steady_clock::now();
        std::vector<std::vector<int>> words =
            (d <= 8) ? gen_canon_links_small(d) : gen_cplus_words(d, CP, cmax);

        std::ofstream fcert(cert_dir + "/cert_d" + std::to_string(d) + ".jsonl");
        long long n_ub0 = 0, n_dfs = 0, total_nodes = 0, total_ub_leaves = 0, total_kill_leaves = 0, total_embs = 0;

        for (const auto& link : words) {
            Window W(d, link);
            std::vector<Inst> ins, outs;
            build_instances(W, parts, ins, outs);
            int base = 10 * (6 - d);
            int sure_outs0 = 0;
            for (const auto& o : outs) if (o.conds.empty() && !o.open) sure_outs0++;
            int ub0 = base + (int)ins.size() - sure_outs0;

            if (ub0 <= 0) {
                n_ub0++;
                total_nodes++;
                fcert << "{\"link\":\"" << link_str(link) << "\",\"ub0\":" << ub0 << "}\n";
                continue;
            }

            std::vector<Inst> allc = ins;
            allc.insert(allc.end(), outs.begin(), outs.end());
            std::set<int> rel_set;
            for (const auto& I : allc) for (const auto& cd : I.conds) rel_set.insert(cd.var_code);
            std::vector<int> rel(rel_set.begin(), rel_set.end());
            std::sort(rel.begin(), rel.end(), [](int a, int b) { return site_key(a) < site_key(b); });

            std::vector<std::pair<int, std::vector<std::vector<int>>>> vs;
            vs.reserve(rel.size());
            for (int v : rel) vs.push_back({v, classes_of(v, allc)});

            auto cands = find_link_embeddings(W, active_cfgs, rel_set);
            std::vector<ActiveReq> reqs;
            reqs.reserve(cands.size());
            for (int idx = 0; idx < (int)cands.size(); ++idx) {
                reqs.push_back({cands[idx].req, idx});
            }

            std::set<int> used_embs;
            DfsStats st;
            bool ok = run_dfs(base, 0, vs, ins, outs, reqs, used_embs, st);
            if (!ok && !pool_cfgs.empty()) {
                auto pool_cands = find_link_embeddings(W, pool_cfgs, rel_set);
                std::vector<EmbWitness> merged = cands;
                for (auto& pw : pool_cands) merged.push_back(std::move(pw));
                std::vector<ActiveReq> mreqs;
                for (int idx = 0; idx < (int)merged.size(); ++idx) {
                    mreqs.push_back({merged[idx].req, idx});
                }
                std::set<int> mused;
                DfsStats mst;
                if (run_dfs(base, 0, vs, ins, outs, mreqs, mused, mst)) {
                    // Promote newly used pool configs into all_cfgs + active_cfgs so later words reuse them first!
                    for (int idx : mused) {
                        int cid = merged[idx].cfg_id;
                        if (cid >= 100000) {
                            Config pc = pool_cfgs[cid - 100000];
                            if (!known_names.count(pc.name)) {
                                known_names.insert(pc.name);
                                pc.id = (int)all_cfgs.size();
                                pc.priority = 5;
                                discovered_names.push_back(pc.name);
                                std::cout << "    [DISCOVERED] d=" << d << " link=" << link_str(link)
                                          << " -> " << pc.name << " (r=" << pc.ring << ", m=" << pc.m << ")\n";
                                all_cfgs.push_back(pc);
                                active_cfgs.push_back(pc);
                            }
                            for (auto& xw : merged) {
                                if (xw.cfg_id == cid) {
                                    // Map to newly assigned id in all_cfgs
                                    for (const auto& ac : all_cfgs) {
                                        if (ac.name == pc.name) { xw.cfg_id = ac.id; break; }
                                    }
                                }
                            }
                        }
                    }
                    cands = std::move(merged);
                    used_embs = std::move(mused);
                    st = mst;
                    ok = true;
                }
            }
            if (!ok) {
                std::cerr << "FATAL: Unkilled positive leaf at d=" << d << " link=" << link_str(link) << "!\n";
                return 2;
            }

            n_dfs++;
            total_nodes += st.nodes;
            total_ub_leaves += st.ub_leaves;
            total_kill_leaves += st.kill_leaves;
            total_embs += (long long)used_embs.size();

            fcert << "{\"link\":\"" << link_str(link) << "\",\"vars\":[";
            for (size_t k = 0; k < rel.size(); ++k) {
                if (k) fcert << ",";
                fcert << rel[k];
            }
            fcert << "],\"ub_leaves\":" << st.ub_leaves << ",\"kill_leaves\":" << st.kill_leaves << ",\"embs\":[";
            bool first_e = true;
            for (int idx : used_embs) {
                if (!first_e) fcert << ",";
                first_e = false;
                const auto& ew = cands[idx];
                global_cfg_uses[ew.cfg_id]++;
                fcert << "[" << ew.cfg_id << ",[";
                for (size_t k = 0; k < ew.phi.size(); ++k) {
                    if (k) fcert << ",";
                    fcert << ew.phi[k];
                }
                fcert << "]," << ew.sigma << ",[";
                for (size_t k = 0; k < ew.shifts.size(); ++k) {
                    if (k) fcert << ",";
                    fcert << ew.shifts[k];
                }
                fcert << "]]";
            }
            fcert << "]}\n";
        }

        double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - td0).count();
        std::cout << "  d=" << std::setw(2) << d << ": PASS | canon_words=" << std::setw(6) << words.size()
                  << " | ub0_le0=" << std::setw(6) << n_ub0 << " | dfs_words=" << std::setw(6) << n_dfs
                  << " | dfs_nodes=" << std::setw(8) << total_nodes << " | embs=" << std::setw(6) << total_embs
                  << " | " << std::fixed << std::setprecision(2) << secs << "s\n";

        if (d > 5) summ_deg_json << ",\n";
        summ_deg_json << "    {\"d\": " << d << ", \"canon_words\": " << words.size()
                      << ", \"ub0_le0\": " << n_ub0 << ", \"dfs_words\": " << n_dfs
                      << ", \"dfs_nodes\": " << total_nodes << ", \"ub_leaves\": " << total_ub_leaves
                      << ", \"kill_leaves\": " << total_kill_leaves << ", \"embs\": " << total_embs
                      << ", \"secs\": " << std::fixed << std::setprecision(3) << secs << "}";
    }
    summ_deg_json << "\n  ]";

    // Summarize distinct configurations actually used across the entire proof
    std::map<std::string, int> used_by_source, used_by_tier, used_by_kind;
    int used_rim_pinned_total = 0;
    int used_rim_pinned_rsst582 = 0;
    int used_rim_pinned_2o126 = 0;
    int used_rim_pinned_sub_window_lean = 0;
    int used_rim_pinned_sub_window_non_lean = 0;
    for (auto [cid, cnt] : global_cfg_uses) {
        const auto& c = all_cfgs[cid];
        used_by_source[c.source]++;
        used_by_tier[c.tier]++;
        used_by_kind[c.kind]++;
        if (c.rim_pinned) {
            used_rim_pinned_total++;
            if (c.source == "RSST_582") used_rim_pinned_rsst582++;
            else if (c.source == "RSST_2o126_LEAN") used_rim_pinned_2o126++;
            else if (c.source == "SUB_WINDOW" && c.tier == "L") used_rim_pinned_sub_window_lean++;
            else used_rim_pinned_sub_window_non_lean++;
        }
    }

    double total_secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t_start).count();
    std::cout << "\nALL DEGREES d=5..17 + KARP TAIL d>=15 PASSED 100% ("
              << global_cfg_uses.size() << " distinct configs used; rim-pinned total="
              << used_rim_pinned_total << " [RSST_582=" << used_rim_pinned_rsst582
              << ", 2.126=" << used_rim_pinned_2o126
              << ", SUB_WINDOW_L=" << used_rim_pinned_sub_window_lean
              << ", SUB_WINDOW_nonL=" << used_rim_pinned_sub_window_non_lean
              << "]; total " << std::fixed << std::setprecision(2)
              << total_secs << "s)!\n";

    std::ofstream fsumm(cert_dir + "/summary.json");
    fsumm << "{\n  \"total_secs\": " << std::fixed << std::setprecision(3) << total_secs << ",\n"
          << "  \"allow_rimpin\": " << (allow_rimpin ? "true" : "false") << ",\n"
          << "  \"distinct_configs_used\": " << global_cfg_uses.size() << ",\n"
          << "  \"used_rim_pinned_total\": " << used_rim_pinned_total << ",\n"
          << "  \"used_rim_pinned_rsst582_foldsafe\": " << used_rim_pinned_rsst582 << ",\n"
          << "  \"used_rim_pinned_2o126_lean\": " << used_rim_pinned_2o126 << ",\n"
          << "  \"used_rim_pinned_sub_window_lean\": " << used_rim_pinned_sub_window_lean << ",\n"
          << "  \"used_rim_pinned_sub_window_non_lean\": " << used_rim_pinned_sub_window_non_lean << ",\n"
          << "  \"used_by_tier\": {\"L\": " << used_by_tier["L"] << ", \"E2\": " << used_by_tier["E2"] << "},\n"
          << "  \"used_by_source\": {\"RSST_582\": " << used_by_source["RSST_582"]
          << ", \"RSST_2o126_LEAN\": " << used_by_source["RSST_2o126_LEAN"]
          << ", \"SUB_NL51\": " << used_by_source["SUB_NL51"]
          << ", \"SUB_WINDOW\": " << used_by_source["SUB_WINDOW"] << "},\n"
          << "  \"degrees\": " << summ_deg_json.str() << "\n}\n";

    if (!discovered_names.empty()) {
        std::ofstream fdisc(data_dir + "/discovered_whitney_subs.txt");
        for (const auto& nm : discovered_names) fdisc << nm << "\n";
        std::cout << "Wrote " << discovered_names.size() << " discovered Whitney-masked D-substitutes to "
                  << data_dir << "/discovered_whitney_subs.txt\n";
    }

    return 0;
}
