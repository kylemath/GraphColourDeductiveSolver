// Fast Multi-Threaded 4CT Unavoidability Separator, Hypergraph Profiler & Certificate Emitter
//
// Supports:
//   - Arbitrary integer scale M (initial charge M * (6 - d))
//   - Arbitrary signed integer part weights w_p != 0 (push rules w_p > 0 and !open anti-rules w_p < 0)
//   - Exact Karp minimum-mean-cycle rational potential phi* on the 625-state 4-gram de Bruijn graph
//   - Zero-allocation in-place symbolic DFS across d = 5 .. max(17, d_tail)
//   - Exact per-config RotOcc hypergraph profiling (no cross-config subsumption masking!)
//   - Modes:
//       --mode sep      : Verify active set S; emit any violated max-depth leaves + all U killers
//       --mode profile  : Emit all max-depth positive leaves with |killers_in_S| <= K_thin (default 3)
//                         matched against ALL pool configs U, plus full 2-ball leaf state for rule synthesis
//       --mode degs D1,D2 : Fast check of specific degrees only (for millisecond rule side-effect screening)
//       --mode cert     : Emit full replayable certificates (cert_karp_tail.json + certs/cert_d*.jsonl)

#include <algorithm>
#include <atomic>
#include <cassert>
#include <chrono>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <mutex>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <thread>
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
    int weight; // > 0 push, < 0 anti-rule (retention)
    std::vector<Sub> subs;
};

struct Slot {
    int kind; // 0 = 'I', 1 = 'R'
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
    if (c.source == "RSST_582") return (c.tier == "L") ? 0 : 1;
    if (c.source == "RSST_2o126_LEAN") return 2;
    if (c.source == "RSST_CMERGE") return 3;
    if (c.source == "SUPER_PATS44") return 4;
    if (c.source == "SUPER_NL51") return 5;
    return 6;
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
                assert(seen_r.find(s.val) == seen_r.end());
                seen_r.insert(s.val);
            }
        }
        assert((int)seen_i.size() == (int)c.int_adj[a].size());
        for (int k = 0; k < g; ++k) {
            const Slot& s0 = c.rot[a][k];
            const Slot& s1 = c.rot[a][(k + 1) % g];
            if (s1.kind == 0 && s0.kind == 1) assert(c.ring_set[s1.val].count(s0.val) > 0);
            if (s0.kind == 0 && s1.kind == 1) assert(c.ring_set[s0.val].count(s1.val) > 0);
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

static inline int npriv(int L) {
    if (L == 5) return 0;
    if (L >= 9) return 3;
    return L - 5;
}

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
            for (int j = 1; j <= k; ++j) seg[i].push_back(1 + 2 * d + 3 * i + (j - 1));
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

    std::pair<int, int> deg_info(int v) const {
        if (v == -1) return {2, 0};
        if (v == 0) return {0, std::min(d, 9)};
        if (v >= 1 && v <= d) return {0, link[v - 1]};
        if (v >= 1 + d && v <= 2 * d) return {1, 100 + (v - 1 - d)};
        int q = v - 1 - 2 * d;
        int i = q / 3, j = (q % 3) + 1;
        assert(!(link[i] >= 9 && j == 2));
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
    int weight; // signed part weight
};

static bool test_vertex(const Window& W, int v, const Range& r, std::vector<Cond>& conds, bool& open_flag) {
    if (r.is_full()) return true;
    auto [kind, val] = W.deg_info(v);
    if (kind == 0) return r.contains(val);
    if (kind == 2) { open_flag = true; return true; }
    conds.push_back({val, r.lo, r.hi});
    return true;
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
    // Deduplicate identical conditions on the same instance so rem_conds counts unique conditions!
    std::sort(conds.begin(), conds.end());
    conds.erase(std::unique(conds.begin(), conds.end()), conds.end());
    // Check self-contradictory conditions on the same variable within one instance
    for (size_t i = 0; i + 1 < conds.size(); ++i) {
        if (conds[i].var_code == conds[i + 1].var_code) {
            int lo = std::max(conds[i].lo, conds[i + 1].lo);
            int hi = std::min(conds[i].hi, conds[i + 1].hi);
            if (lo > hi) return false;
            conds[i + 1] = {conds[i].var_code, lo, hi};
            conds.erase(conds.begin() + i);
            --i;
        }
    }
    out_inst.conds = std::move(conds);
    out_inst.open = open_flag;
    out_inst.hub_w = (h == 0) ? -1 : (h - 1);
    out_inst.weight = part.weight;
    return true;
}

// Normalize signed-weight instances into unified upper-bound terms!
// In Window2Ball upper bound ub(u) = base + sum_{plus} w_plus * 1_alive - sum_{minus} w_minus * 1_sure:
//   - An incoming part with weight > 0 adds +w whenever ALIVE (may fire).
//   - An outgoing part with weight < 0 adds +|w| whenever ALIVE (may fire).
//   - An outgoing part with weight > 0 subtracts w ONLY when SURE (!open && conds_rem == 0).
//   - An incoming part with weight < 0 subtracts |w| ONLY when SURE (!open && conds_rem == 0).
//     (Note: if open == true on an incoming part with weight < 0, it can NEVER become sure, so omit it from minus!)
static void build_ub_terms(const Window& W, const std::vector<Part>& parts,
                           std::vector<Inst>& plus_terms, std::vector<Inst>& minus_terms) {
    plus_terms.clear();
    minus_terms.clear();
    if (5 <= W.d && W.d <= 8) {
        for (const auto& p : parts) {
            if (p.n != W.d || p.weight == 0) continue;
            for (int a = 0; a < W.d; ++a) {
                Inst inst;
                if (fit_part(W, 0, p, a, inst)) {
                    assert(!inst.open);
                    if (p.weight > 0) {
                        inst.weight = p.weight;
                        minus_terms.push_back(std::move(inst));
                    } else {
                        inst.weight = -p.weight;
                        plus_terms.push_back(std::move(inst));
                    }
                }
            }
        }
    }
    for (int i = 0; i < W.d; ++i) {
        int L = W.link[i];
        if (L > 8) continue;
        for (const auto& p : parts) {
            if (p.n != L || p.weight == 0) continue;
            int a = L - 2;
            Inst inst;
            if (fit_part(W, 1 + i, p, a, inst)) {
                if (p.weight > 0) {
                    inst.weight = p.weight;
                    plus_terms.push_back(std::move(inst));
                } else if (!inst.open) {
                    inst.weight = -p.weight;
                    minus_terms.push_back(std::move(inst));
                }
            }
        }
    }
}

// --- Strict Global-Chirality rotOK (RotOcc) ---
static bool check_rot_ok(int d, const std::vector<int>& link, const Config& cfg,
                         const std::vector<int>& phi, int& out_sigma, std::vector<int>& out_shifts) {
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
                        if (phi_set.count(fv)) { ok = false; break; }
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
    std::vector<std::pair<int, int>> req;
    int cfg_id;
    int priority;
    std::vector<int> phi;
    int sigma;
    std::vector<int> shifts;
};

// When cross_prune == false (used in sep/profile modes), every config keeps its own minimal reqs
// without masking other configs! When cross_prune == true (cert mode), keeps one witness per req.
static std::vector<EmbWitness> find_link_embeddings(
    const Window& W, const std::vector<Config>& cfgs, const std::set<int>& rel_vars, bool cross_prune) {
    std::vector<int> hosts;
    std::unordered_map<int, std::set<int>> host_degs;
    std::unordered_map<int, int> host_var;

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
    for (auto& [h, st] : adj_set) adj_vec[h] = std::vector<int>(st.begin(), st.end());

    std::map<int, int> hc;
    for (auto& [h, st] : host_degs) for (int x : st) hc[x]++;

    if (cross_prune) {
        std::map<std::vector<std::pair<int, int>>, EmbWitness> best_by_req;
        for (const auto& cfg : cfgs) {
            if (cfg.m > (int)hosts.size()) continue;
            bool deg_ok = true;
            for (auto [dg, cnt] : cfg.dm) if (hc[dg] < cnt) { deg_ok = false; break; }
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
                        std::make_pair(cfg.priority, cfg.id)) return;
                    int sg = 0;
                    std::vector<int> shifts;
                    if (check_rot_ok(W.d, W.link, cfg, phi, sg, shifts)) {
                        best_by_req[req] = EmbWitness{req, cfg.id, cfg.priority, phi, sg, std::move(shifts)};
                    }
                    return;
                }
                int x = cfg.order[k];
                int anchor_nb = -1;
                for (int prev_idx = 0; prev_idx < k; ++prev_idx) {
                    int y = cfg.order[prev_idx];
                    if (std::binary_search(cfg.int_adj[x].begin(), cfg.int_adj[x].end(), y)) {
                        anchor_nb = y;
                        break;
                    }
                }
                const std::vector<int>& cands = (anchor_nb == -1) ? hosts : adj_vec[phi[anchor_nb]];
                for (int t : cands) {
                    if (used_h.count(t) || !host_degs[t].count(cfg.deg[x])) continue;
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
        std::vector<EmbWitness> raw, keep;
        for (auto& [rq, ew] : best_by_req) raw.push_back(std::move(ew));
        std::sort(raw.begin(), raw.end(), [](const EmbWitness& a, const EmbWitness& b) {
            if (a.req.size() != b.req.size()) return a.req.size() < b.req.size();
            if (a.priority != b.priority) return a.priority < b.priority;
            return a.cfg_id < b.cfg_id;
        });
        for (auto& ew : raw) {
            bool sub = false;
            for (const auto& kw : keep) {
                if (std::includes(ew.req.begin(), ew.req.end(), kw.req.begin(), kw.req.end())) {
                    sub = true; break;
                }
            }
            if (!sub) keep.push_back(std::move(ew));
        }
        return keep;
    }

    // Per-config minimal reqs (NO cross-config pruning!)
    std::vector<EmbWitness> all_out;
    for (const auto& cfg : cfgs) {
        if (cfg.m > (int)hosts.size()) continue;
        bool deg_ok = true;
        for (auto [dg, cnt] : cfg.dm) if (hc[dg] < cnt) { deg_ok = false; break; }
        if (!deg_ok) continue;

        std::map<std::vector<std::pair<int, int>>, EmbWitness> cfg_reqs;
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
                if (cfg_reqs.count(req)) return;
                int sg = 0;
                std::vector<int> shifts;
                if (check_rot_ok(W.d, W.link, cfg, phi, sg, shifts)) {
                    cfg_reqs[req] = EmbWitness{req, cfg.id, cfg.priority, phi, sg, std::move(shifts)};
                }
                return;
            }
            int x = cfg.order[k];
            int anchor_nb = -1;
            for (int prev_idx = 0; prev_idx < k; ++prev_idx) {
                int y = cfg.order[prev_idx];
                if (std::binary_search(cfg.int_adj[x].begin(), cfg.int_adj[x].end(), y)) {
                    anchor_nb = y;
                    break;
                }
            }
            const std::vector<int>& cands = (anchor_nb == -1) ? hosts : adj_vec[phi[anchor_nb]];
            for (int t : cands) {
                if (used_h.count(t) || !host_degs[t].count(cfg.deg[x])) continue;
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

        std::vector<EmbWitness> craw;
        for (auto& [rq, ew] : cfg_reqs) craw.push_back(std::move(ew));
        std::sort(craw.begin(), craw.end(), [](const EmbWitness& a, const EmbWitness& b) {
            return a.req.size() < b.req.size();
        });
        std::vector<EmbWitness> ckeep;
        for (auto& ew : craw) {
            bool sub = false;
            for (const auto& kw : ckeep) {
                if (std::includes(ew.req.begin(), ew.req.end(), kw.req.begin(), kw.req.end())) {
                    sub = true; break;
                }
            }
            if (!sub) ckeep.push_back(std::move(ew));
        }
        for (auto& ew : ckeep) all_out.push_back(std::move(ew));
    }
    return all_out;
}

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
    for (int x : {5, 6, 7, 8, 9}) if (pat(x) == p9) c9.push_back(x);
    out.push_back(c9);
    for (int x : {5, 6, 7, 8}) if (pat(x) != p9) out.push_back({x});
    return out;
}

// --- Signed-weight 5-gram maxsat & Exact Karp Minimum-Mean-Cycle Potential ---
static int maxsat_signed(const std::vector<Inst>& plus_w2, const std::vector<Inst>& minus_w2) {
    std::set<int> vset;
    for (const auto& I : plus_w2) for (const auto& c : I.conds) vset.insert(c.var_code);
    for (const auto& I : minus_w2) for (const auto& c : I.conds) vset.insert(c.var_code);
    std::vector<int> names(vset.begin(), vset.end());
    int nv = (int)names.size();
    std::unordered_map<int, int> pos;
    for (int k = 0; k < nv; ++k) pos[names[k]] = k;

    std::vector<std::vector<std::tuple<int, int, int>>> by_p(nv), by_m(nv);
    int init_p = 0;
    for (int t = 0; t < (int)plus_w2.size(); ++t) {
        init_p += plus_w2[t].weight;
        for (const auto& c : plus_w2[t].conds) by_p[pos[c.var_code]].push_back({t, c.lo, c.hi});
    }
    for (int t = 0; t < (int)minus_w2.size(); ++t) {
        for (const auto& c : minus_w2[t].conds) by_m[pos[c.var_code]].push_back({t, c.lo, c.hi});
    }

    std::vector<int> dead_p(plus_w2.size(), 0);
    std::vector<int> dead_m(minus_w2.size(), 0);
    std::vector<int> rem_m(minus_w2.size(), 0);
    int init_sure_m = 0;
    for (int t = 0; t < (int)minus_w2.size(); ++t) {
        rem_m[t] = (int)minus_w2[t].conds.size();
        if (rem_m[t] == 0) init_sure_m += minus_w2[t].weight;
    }

    int best = -1000000000;
    auto rec = [&](auto& self, int k, int cur_p, int cur_sure_m) -> void {
        if (cur_p - cur_sure_m <= best) return;
        if (k == nv) {
            best = cur_p - cur_sure_m;
            return;
        }
        for (int val : {5, 6, 7, 8, 9}) {
            int np = cur_p, nm = cur_sure_m;
            for (auto [t, lo, hi] : by_p[k]) {
                if (!(lo <= val && val <= hi)) {
                    if (dead_p[t] == 0) np -= plus_w2[t].weight;
                    dead_p[t]++;
                }
            }
            for (auto [t, lo, hi] : by_m[k]) {
                if (lo <= val && val <= hi) {
                    rem_m[t]--;
                    if (rem_m[t] == 0 && dead_m[t] == 0) nm += minus_w2[t].weight;
                } else {
                    dead_m[t]++;
                }
            }
            self(self, k + 1, np, nm);
            for (auto [t, lo, hi] : by_p[k]) {
                if (!(lo <= val && val <= hi)) dead_p[t]--;
            }
            for (auto [t, lo, hi] : by_m[k]) {
                if (lo <= val && val <= hi) rem_m[t]++;
                else dead_m[t]--;
            }
        }
    };
    rec(rec, 0, init_p, init_sure_m);
    return (best == -1000000000) ? 0 : best;
}

struct KarpResult {
    int CP[5][5][5][5][5];
    int max_cp;
    long long P_num; // reduced numerator of lambda*
    long long Q_den; // reduced denominator of lambda*
    long long Phi[625]; // integer potential so Q*CP + Phi[y] - Phi[x] <= P
    long long E_shift[5][5][5][5][5]; // Q*CP + Phi[y] - Phi[x] <= P
    long long emax_center[10];
    long long emax_all;
    int tail_d0; // smallest d >= 9 such that scale_M*(6 - d)*Q + P*d <= 0 for all d >= tail_d0
};

static KarpResult solve_karp_potential(int scale_M, const std::vector<Part>& parts) {
    KarpResult kr{};
    kr.max_cp = -1000000;
    for (int a = 5; a <= 9; ++a)
    for (int b = 5; b <= 9; ++b)
    for (int c = 5; c <= 9; ++c)
    for (int d = 5; d <= 9; ++d)
    for (int e = 5; e <= 9; ++e) {
        int val = 0;
        if (c <= 8) {
            Window W(10, {a, b, c, d, e, 5, 5, 5, 5, 5});
            std::vector<Inst> plus_t, minus_t, pw2, mw2;
            build_ub_terms(W, parts, plus_t, minus_t);
            for (auto& I : plus_t) if (I.hub_w == 2) pw2.push_back(std::move(I));
            for (auto& I : minus_t) if (I.hub_w == 2) mw2.push_back(std::move(I));
            val = maxsat_signed(pw2, mw2);
        }
        kr.CP[a - 5][b - 5][c - 5][d - 5][e - 5] = val;
        kr.max_cp = std::max(kr.max_cp, val);
    }

    // Karp's exact max-mean-cycle DP on 625-vertex 4-gram de Bruijn graph
    const int N = 625;
    const long long NEG_INF = -1000000000000000LL;
    std::vector<std::vector<long long>> dp(N + 1, std::vector<long long>(N, NEG_INF));
    for (int v = 0; v < N; ++v) dp[0][v] = 0;
    for (int k = 1; k <= N; ++k) {
        for (int x = 0; x < N; ++x) {
            if (dp[k - 1][x] == NEG_INF) continue;
            int a = (x / 125) % 5, b = (x / 25) % 5, c = (x / 5) % 5, d = x % 5;
            for (int e = 0; e < 5; ++e) {
                int y = b * 125 + c * 25 + d * 5 + e;
                long long w = kr.CP[a][b][c][d][e];
                if (dp[k - 1][x] + w > dp[k][y]) dp[k][y] = dp[k - 1][x] + w;
            }
        }
    }

    long long best_P = 0, best_Q = 1;
    bool has_v = false;
    for (int v = 0; v < N; ++v) {
        if (dp[N][v] == NEG_INF) continue;
        // Compute min_{0 <= k < N} (dp[N][v] - dp[k][v]) / (N - k)
        long long min_p = 0, min_q = 1;
        bool has_k = false;
        for (int k = 0; k < N; ++k) {
            if (dp[k][v] == NEG_INF) continue;
            long long p = dp[N][v] - dp[k][v];
            long long q = N - k;
            if (!has_k || p * min_q < min_p * q) {
                min_p = p;
                min_q = q;
                has_k = true;
            }
        }
        if (has_k && (!has_v || min_p * best_Q > best_P * min_q)) {
            best_P = min_p;
            best_Q = min_q;
            has_v = true;
        }
    }
    long long g = std::gcd(std::abs(best_P), best_Q);
    kr.P_num = best_P / g;
    kr.Q_den = best_Q / g;

    // Bellman-Ford for exact integer potential Phi: dist[y] = max(dist[y], dist[x] + Q*W - P)
    std::vector<long long> dist(N, 0);
    for (int iter = 0; iter <= N; ++iter) {
        bool changed = false;
        for (int x = 0; x < N; ++x) {
            int a = (x / 125) % 5, b = (x / 25) % 5, c = (x / 5) % 5, d = x % 5;
            for (int e = 0; e < 5; ++e) {
                int y = b * 125 + c * 25 + d * 5 + e;
                long long wp = kr.Q_den * (long long)kr.CP[a][b][c][d][e] - kr.P_num;
                if (dist[x] + wp > dist[y]) {
                    assert(iter < N && "Positive cycle in Bellman-Ford despite Karp optimum!");
                    dist[y] = dist[x] + wp;
                    changed = true;
                }
            }
        }
        if (!changed) break;
    }
    for (int v = 0; v < N; ++v) kr.Phi[v] = -dist[v];

    kr.emax_all = NEG_INF;
    for (int c = 5; c <= 9; ++c) kr.emax_center[c] = NEG_INF;
    for (int a = 0; a < 5; ++a)
    for (int b = 0; b < 5; ++b)
    for (int c = 0; c < 5; ++c)
    for (int d = 0; d < 5; ++d)
    for (int e = 0; e < 5; ++e) {
        int x = a * 125 + b * 25 + c * 5 + d;
        int y = b * 125 + c * 25 + d * 5 + e;
        long long es = kr.Q_den * (long long)kr.CP[a][b][c][d][e] + kr.Phi[y] - kr.Phi[x];
        assert(es <= kr.P_num);
        kr.E_shift[a][b][c][d][e] = es;
        kr.emax_center[c + 5] = std::max(kr.emax_center[c + 5], es);
        kr.emax_all = std::max(kr.emax_all, es);
    }

    // Compute tail_d0: need scale_M * (6 - d) * Q + P * d <= 0 <=> (scale_M * Q - P) * d >= 6 * scale_M * Q
    long long denom = (long long)scale_M * kr.Q_den - kr.P_num;
    if (denom <= 0) {
        kr.tail_d0 = 999999; // Tail does NOT close!
    } else {
        long long numer = 6LL * scale_M * kr.Q_den;
        kr.tail_d0 = (int)((numer + denom - 1) / denom);
        if (kr.tail_d0 < 9) kr.tail_d0 = 9;
    }
    return kr;
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

static std::vector<std::vector<int>> gen_cplus_words_karp(int d, int scale_M, const KarpResult& kr) {
    std::vector<std::vector<int>> out;
    long long base_Q = (long long)scale_M * (6 - d) * kr.Q_den;
    std::vector<int> L(d, 0);
    auto partial_bound = [&](int k) {
        long long s = base_Q;
        for (int i = 0; i < d; ++i) {
            if (i - 2 >= 0 && i + 2 <= k - 1) {
                s += kr.E_shift[L[i - 2] - 5][L[i - 1] - 5][L[i] - 5][L[i + 1] - 5][L[i + 2] - 5];
            } else if (i <= k - 1) {
                s += kr.emax_center[L[i]];
            } else {
                s += kr.emax_all;
            }
        }
        return s;
    };
    auto rec = [&](auto& self, int k) -> void {
        if (k == d) {
            if (!is_dihedral_canon(L)) return;
            long long cyc = (long long)scale_M * (6 - d);
            for (int i = 0; i < d; ++i) {
                cyc += kr.CP[L[(i + d - 2) % d] - 5][L[(i + d - 1) % d] - 5][L[i] - 5]
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

// --- Zero-Allocation In-Place Symbolic DFS ---
struct PreparedDFS {
    int base;
    int nv;
    std::vector<int> vars;
    std::vector<int> w_plus, w_minus;
    int init_plus_sum = 0;
    int init_sure_minus_sum = 0;
    std::vector<int> init_rem_minus;
    std::vector<std::vector<std::tuple<int, int, int>>> p_conds, m_conds;

    PreparedDFS(int base_, const std::vector<Inst>& plus_t, const std::vector<Inst>& minus_t) : base(base_) {
        std::vector<Inst> allc = plus_t;
        allc.insert(allc.end(), minus_t.begin(), minus_t.end());
        std::set<int> rel_set;
        for (const auto& I : allc) for (const auto& cd : I.conds) rel_set.insert(cd.var_code);
        vars.assign(rel_set.begin(), rel_set.end());
        std::sort(vars.begin(), vars.end(), [](int a, int b) { return site_key(a) < site_key(b); });
        nv = (int)vars.size();
        std::unordered_map<int, int> vpos;
        for (int k = 0; k < nv; ++k) vpos[vars[k]] = k;

        p_conds.resize(nv);
        m_conds.resize(nv);

        w_plus.resize(plus_t.size());
        for (size_t t = 0; t < plus_t.size(); ++t) {
            w_plus[t] = plus_t[t].weight;
            init_plus_sum += w_plus[t];
            for (const auto& cd : plus_t[t].conds) {
                p_conds[vpos.at(cd.var_code)].push_back({(int)t, cd.lo, cd.hi});
            }
        }

        w_minus.resize(minus_t.size());
        init_rem_minus.resize(minus_t.size());
        for (size_t t = 0; t < minus_t.size(); ++t) {
            w_minus[t] = minus_t[t].weight;
            init_rem_minus[t] = (int)minus_t[t].conds.size();
            if (init_rem_minus[t] == 0) init_sure_minus_sum += w_minus[t];
            for (const auto& cd : minus_t[t].conds) {
                m_conds[vpos.at(cd.var_code)].push_back({(int)t, cd.lo, cd.hi});
            }
        }
    }
};

struct PreparedReqs {
    int nr;
    std::vector<int> cfg_of;
    std::vector<int> init_rem;
    std::vector<std::vector<std::pair<int, int>>> r_conds;

    PreparedReqs(const PreparedDFS& pd, const std::vector<EmbWitness>& cands) {
        nr = (int)cands.size();
        cfg_of.resize(nr);
        init_rem.resize(nr);
        std::unordered_map<int, int> vpos;
        for (int k = 0; k < pd.nv; ++k) vpos[pd.vars[k]] = k;

        r_conds.resize(pd.nv);
        for (int r = 0; r < nr; ++r) {
            cfg_of[r] = cands[r].cfg_id;
            init_rem[r] = (int)cands[r].req.size();
            for (auto [vc, deg_req] : cands[r].req) {
                r_conds[vpos.at(vc)].push_back({r, deg_req});
            }
        }
    }
};

struct LeafRecord {
    int d;
    std::string link;
    int ub;
    std::vector<std::pair<int, std::vector<int>>> var_classes; // (var_code, class_vec)
    std::vector<int> killers_S;
    std::vector<int> killers_U;
};

int main(int argc, char** argv) {
    std::string pool_path = "/Users/kylemathewson/GraphColouringNov/beat_633/data/pool_input.txt";
    std::string rules_path;
    std::string active_path;
    std::string mode = "sep";
    std::string out_path = "/Users/kylemathewson/GraphColouringNov/beat_633/data/sep_out.jsonl";
    std::string cert_data_dir = "/Users/kylemathewson/GraphColouringNov/beat_633/data";
    std::string degs_arg;
    int k_thin = 1;
    int cap_per_cfg = 400;
    int n_threads = 3;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--pool" && i + 1 < argc) pool_path = argv[++i];
        else if (arg == "--rules" && i + 1 < argc) rules_path = argv[++i];
        else if (arg == "--active" && i + 1 < argc) active_path = argv[++i];
        else if (arg == "--mode" && i + 1 < argc) mode = argv[++i];
        else if (arg == "--out" && i + 1 < argc) out_path = argv[++i];
        else if (arg == "--cert-dir" && i + 1 < argc) cert_data_dir = argv[++i];
        else if (arg == "--degs" && i + 1 < argc) degs_arg = argv[++i];
        else if (arg == "--k-thin" && i + 1 < argc) k_thin = std::stoi(argv[++i]);
        else if (arg == "--cap-per-cfg" && i + 1 < argc) cap_per_cfg = std::stoi(argv[++i]);
        else if (arg == "--threads" && i + 1 < argc) n_threads = std::max(1, std::stoi(argv[++i]));
    }

    auto t_start = std::chrono::steady_clock::now();
    std::ifstream fpool(pool_path);
    assert(fpool && "Cannot open pool_path");

    std::string hdr;
    int scale_M = 10;
    fpool >> hdr >> scale_M;
    assert(hdr == "SCALE" && scale_M > 0);
    int nparts = 0;
    fpool >> hdr >> nparts;
    assert(hdr == "PARTS");
    std::vector<Part> parts(nparts);
    for (int i = 0; i < nparts; ++i) {
        fpool >> parts[i].tag >> parts[i].n >> parts[i].weight;
        parts[i].subs.resize(parts[i].n);
        for (int j = 0; j < parts[i].n; ++j) {
            int nf = 0;
            fpool >> parts[i].subs[j].sp.lo >> parts[i].subs[j].sp.hi
                  >> parts[i].subs[j].hat.lo >> parts[i].subs[j].hat.hi >> nf;
            parts[i].subs[j].fans.resize(nf);
            for (int f = 0; f < nf; ++f) {
                fpool >> parts[i].subs[j].fans[f].lo >> parts[i].subs[j].fans[f].hi;
            }
        }
    }

    int ncfgs = 0;
    fpool >> hdr >> ncfgs;
    assert(hdr == "CONFIGS" && ncfgs > 0);
    std::vector<Config> all_cfgs(ncfgs);
    for (int i = 0; i < ncfgs; ++i) {
        Config& c = all_cfgs[i];
        fpool >> c.id >> c.name >> c.source >> c.kind >> c.tier >> c.rim_pinned >> c.ring >> c.m;
        assert(c.id == i);
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
        verify_config_self_rotok(c);
        compute_search_order(c);
        c.priority = config_priority(c);
    }

    // Override rules if --rules specified
    if (!rules_path.empty()) {
        std::ifstream fr(rules_path);
        assert(fr && "Cannot open rules_path");
        fr >> hdr >> scale_M;
        assert(hdr == "SCALE" && scale_M > 0);
        fr >> hdr >> nparts;
        assert(hdr == "PARTS");
        parts.assign(nparts, Part{});
        for (int i = 0; i < nparts; ++i) {
            fr >> parts[i].tag >> parts[i].n >> parts[i].weight;
            parts[i].subs.resize(parts[i].n);
            for (int j = 0; j < parts[i].n; ++j) {
                int nf = 0;
                fr >> parts[i].subs[j].sp.lo >> parts[i].subs[j].sp.hi
                   >> parts[i].subs[j].hat.lo >> parts[i].subs[j].hat.hi >> nf;
                parts[i].subs[j].fans.resize(nf);
                for (int f = 0; f < nf; ++f) {
                    fr >> parts[i].subs[j].fans[f].lo >> parts[i].subs[j].fans[f].hi;
                }
            }
        }
    }

    std::set<int> active_set;
    if (!active_path.empty()) {
        std::ifstream fa(active_path);
        assert(fa && "Cannot open active_path");
        int cid;
        while (fa >> cid) {
            assert(0 <= cid && cid < ncfgs);
            active_set.insert(cid);
        }
    } else {
        for (int i = 0; i < std::min(633, ncfgs); ++i) active_set.insert(i);
    }

    std::vector<Config> active_cfgs, ext_cfgs;
    for (int i = 0; i < ncfgs; ++i) {
        if (active_set.count(i)) active_cfgs.push_back(all_cfgs[i]);
        else ext_cfgs.push_back(all_cfgs[i]);
    }

    KarpResult kr = solve_karp_potential(scale_M, parts);
    std::cout << "[KARP] scale_M=" << scale_M << " parts=" << parts.size()
              << " active_cfgs=" << active_cfgs.size() << " max_cp=" << kr.max_cp
              << " lambda*=" << kr.P_num << "/" << kr.Q_den
              << " tail_d0=" << kr.tail_d0 << "\n";
    if (kr.tail_d0 > 30) {
        std::cerr << "FAIL: Karp tail_d0=" << kr.tail_d0 << " (> 30)!\n";
        return 3;
    }

    int d_max = std::max(17, kr.tail_d0);
    std::set<int> filter_degs;
    if (!degs_arg.empty()) {
        std::stringstream ss(degs_arg);
        std::string tok;
        while (std::getline(ss, tok, ',')) if (!tok.empty()) filter_degs.insert(std::stoi(tok));
    }

    if (mode == "cert") {
        // Emit cert_karp_tail.json + certs/cert_d*.jsonl + certs/summary.json
        {
            std::ofstream fcp(cert_data_dir + "/cert_karp_tail.json");
            fcp << "{\n  \"scale_M\": " << scale_M << ",\n"
                << "  \"max_cplus\": " << kr.max_cp << ",\n"
                << "  \"karp_lambda_star_num\": " << kr.P_num << ",\n"
                << "  \"karp_lambda_star_den\": " << kr.Q_den << ",\n"
                << "  \"tail_degree_d0\": " << kr.tail_d0 << ",\n"
                << "  \"max_checked_degree\": " << d_max << ",\n"
                << "  \"phi_625\": [";
            for (int v = 0; v < 625; ++v) {
                if (v) fcp << ",";
                fcp << kr.Phi[v];
            }
            fcp << "],\n  \"cplus_3125\": {\n";
            bool first = true;
            for (int a = 5; a <= 9; ++a)
            for (int b = 5; b <= 9; ++b)
            for (int c = 5; ++c <= 10; --c) break; // dummy no-op
            for (int a = 5; a <= 9; ++a)
            for (int b = 5; b <= 9; ++b)
            for (int c = 5; c <= 9; ++c)
            for (int d = 5; d <= 9; ++d)
            for (int e = 5; e <= 9; ++e) {
                if (!first) fcp << ",\n";
                first = false;
                fcp << "    \"" << a << b << c << d << e << "\": " << kr.CP[a - 5][b - 5][c - 5][d - 5][e - 5];
            }
            fcp << "\n  }\n}\n";
        }

        std::string cert_dir = cert_data_dir + "/certs";
        std::map<int, long long> global_cfg_uses;
        std::ostringstream summ_deg_json;
        summ_deg_json << "[\n";

        for (int d = 5; d <= d_max; ++d) {
            auto td0 = std::chrono::steady_clock::now();
            auto words = (d <= 8) ? gen_canon_links_small(d) : gen_cplus_words_karp(d, scale_M, kr);
            int nw = (int)words.size();
            std::vector<std::string> lines(nw);
            std::vector<long long> w_nodes(nw, 0), w_ub(nw, 0), w_kill(nw, 0), w_embs(nw, 0);
            std::vector<int> w_is_ub0(nw, 0);
            std::vector<std::vector<int>> w_used_cfgs(nw);
            std::atomic<int> next_idx{0};
            std::atomic<bool> any_fail{false};

            auto worker = [&]() {
                while (!any_fail.load()) {
                    int idx = next_idx.fetch_add(1);
                    if (idx >= nw) break;
                    const auto& link = words[idx];
                    Window W(d, link);
                    std::vector<Inst> plus_t, minus_t;
                    build_ub_terms(W, parts, plus_t, minus_t);
                    int base = scale_M * (6 - d);
                    int init_p = 0, init_m = 0;
                    for (const auto& x : plus_t) init_p += x.weight;
                    for (const auto& x : minus_t) if (x.conds.empty()) init_m += x.weight;
                    int ub0 = base + init_p - init_m;
                    if (ub0 <= 0) {
                        w_is_ub0[idx] = 1;
                        w_nodes[idx] = 1;
                        lines[idx] = "{\"link\":\"" + link_str(link) + "\",\"ub0\":" + std::to_string(ub0) + "}\n";
                        continue;
                    }
                    PreparedDFS pd(base, plus_t, minus_t);
                    std::set<int> rel_set(pd.vars.begin(), pd.vars.end());
                    auto cands = find_link_embeddings(W, active_cfgs, rel_set, true);
                    PreparedReqs pr(pd, cands);

                    std::vector<int> dead_p(plus_t.size(), 0), dead_m(minus_t.size(), 0);
                    std::vector<int> rem_m = pd.init_rem_minus;
                    std::vector<int> dead_r(pr.nr, 0), rem_r = pr.init_rem;
                    std::set<int> used_embs;
                    long long nodes = 0, ub_l = 0, kill_l = 0;

                    auto dfs = [&](auto& self, int depth, int cur_p, int cur_m) -> bool {
                        nodes++;
                        if (base + cur_p - cur_m <= 0) { ub_l++; return true; }
                        int pick = -1;
                        for (int r = 0; r < pr.nr; ++r) {
                            if (dead_r[r] == 0 && rem_r[r] == 0) {
                                if (used_embs.count(r)) { pick = r; break; }
                                if (pick == -1) pick = r;
                            }
                        }
                        if (pick != -1) { used_embs.insert(pick); kill_l++; return true; }
                        if (depth == pd.nv) return false;

                        bool same9[9] = {false, false, false, false, false, true, true, true, true};
                        for (auto [t, lo, hi] : pd.p_conds[depth]) {
                            if (dead_p[t] == 0) {
                                bool in9 = (lo <= 9 && 9 <= hi);
                                for (int x = 5; x <= 8; ++x) if ((lo <= x && x <= hi) != in9) same9[x] = false;
                            }
                        }
                        for (auto [t, lo, hi] : pd.m_conds[depth]) {
                            if (dead_m[t] == 0) {
                                bool in9 = (lo <= 9 && 9 <= hi);
                                for (int x = 5; x <= 8; ++x) if ((lo <= x && x <= hi) != in9) same9[x] = false;
                            }
                        }
                        int reps[5];
                        int n_reps = 0;
                        reps[n_reps++] = 9;
                        for (int x = 5; x <= 8; ++x) if (!same9[x]) reps[n_reps++] = x;

                        for (int bi = 0; bi < n_reps; ++bi) {
                            int rep = reps[bi];
                            int np = cur_p, nm = cur_m;
                            for (auto [t, lo, hi] : pd.p_conds[depth]) {
                                if (!(lo <= rep && rep <= hi)) {
                                    if (dead_p[t] == 0) np -= pd.w_plus[t];
                                    dead_p[t]++;
                                }
                            }
                            for (auto [t, lo, hi] : pd.m_conds[depth]) {
                                if (lo <= rep && rep <= hi) {
                                    rem_m[t]--;
                                    if (rem_m[t] == 0 && dead_m[t] == 0) nm += pd.w_minus[t];
                                } else {
                                    dead_m[t]++;
                                }
                            }
                            for (auto [r, deg_req] : pr.r_conds[depth]) {
                                if (rep == deg_req) rem_r[r]--;
                                else dead_r[r]++;
                            }

                            bool ok = self(self, depth + 1, np, nm);

                            for (auto [t, lo, hi] : pd.p_conds[depth]) {
                                if (!(lo <= rep && rep <= hi)) dead_p[t]--;
                            }
                            for (auto [t, lo, hi] : pd.m_conds[depth]) {
                                if (lo <= rep && rep <= hi) rem_m[t]++;
                                else dead_m[t]--;
                            }
                            for (auto [r, deg_req] : pr.r_conds[depth]) {
                                if (rep == deg_req) rem_r[r]++;
                                else dead_r[r]--;
                            }
                            if (!ok) return false;
                        }
                        return true;
                    };

                    if (!dfs(dfs, 0, pd.init_plus_sum, pd.init_sure_minus_sum)) {
                        std::cerr << "FATAL CERT FAIL at d=" << d << " link=" << link_str(link) << "\n";
                        any_fail.store(true);
                        return;
                    }
                    w_nodes[idx] = nodes;
                    w_ub[idx] = ub_l;
                    w_kill[idx] = kill_l;
                    w_embs[idx] = (long long)used_embs.size();

                    std::ostringstream oss;
                    oss << "{\"link\":\"" << link_str(link) << "\",\"vars\":[";
                    for (int k = 0; k < pd.nv; ++k) { if (k) oss << ","; oss << pd.vars[k]; }
                    oss << "],\"ub_leaves\":" << ub_l << ",\"kill_leaves\":" << kill_l << ",\"embs\":[";
                    bool fe = true;
                    for (int r : used_embs) {
                        if (!fe) oss << ",";
                        fe = false;
                        const auto& ew = cands[r];
                        w_used_cfgs[idx].push_back(ew.cfg_id);
                        oss << "[" << ew.cfg_id << ",[";
                        for (size_t k = 0; k < ew.phi.size(); ++k) { if (k) oss << ","; oss << ew.phi[k]; }
                        oss << "]," << ew.sigma << ",[";
                        for (size_t k = 0; k < ew.shifts.size(); ++k) { if (k) oss << ","; oss << ew.shifts[k]; }
                        oss << "]]";
                    }
                    oss << "]}\n";
                    lines[idx] = oss.str();
                }
            };

            std::vector<std::thread> ths;
            for (int t = 0; t < n_threads; ++t) ths.emplace_back(worker);
            for (auto& th : ths) th.join();
            if (any_fail.load()) return 2;

            std::ofstream fcert(cert_dir + "/cert_d" + std::to_string(d) + ".jsonl");
            long long n_ub0 = 0, n_dfs = 0, tot_nodes = 0, tot_ub = 0, tot_kill = 0, tot_embs = 0;
            for (int idx = 0; idx < nw; ++idx) {
                fcert << lines[idx];
                if (w_is_ub0[idx]) n_ub0++; else n_dfs++;
                tot_nodes += w_nodes[idx];
                tot_ub += w_ub[idx];
                tot_kill += w_kill[idx];
                tot_embs += w_embs[idx];
                for (int cid : w_used_cfgs[idx]) global_cfg_uses[cid]++;
            }
            double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - td0).count();
            std::cout << "  d=" << std::setw(2) << d << ": PASS | words=" << std::setw(6) << nw
                      << " | dfs=" << std::setw(5) << n_dfs << " | nodes=" << std::setw(8) << tot_nodes
                      << " | embs=" << std::setw(6) << tot_embs << " | " << std::fixed << std::setprecision(2) << secs << "s\n";
            if (d > 5) summ_deg_json << ",\n";
            summ_deg_json << "    {\"d\": " << d << ", \"canon_words\": " << nw
                          << ", \"ub0_le0\": " << n_ub0 << ", \"dfs_words\": " << n_dfs
                          << ", \"dfs_nodes\": " << tot_nodes << ", \"ub_leaves\": " << tot_ub
                          << ", \"kill_leaves\": " << tot_kill << ", \"embs\": " << tot_embs
                          << ", \"secs\": " << std::fixed << std::setprecision(3) << secs << "}";
        }
        summ_deg_json << "\n  ]";
        double total_secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t_start).count();
        std::cout << "CERT COMPLETE: " << global_cfg_uses.size() << " distinct configs used in "
                  << std::fixed << std::setprecision(2) << total_secs << "s!\n";
        std::ofstream fsumm(cert_dir + "/summary.json");
        fsumm << "{\n  \"total_secs\": " << std::fixed << std::setprecision(3) << total_secs << ",\n"
              << "  \"scale_M\": " << scale_M << ",\n"
              << "  \"num_parts\": " << parts.size() << ",\n"
              << "  \"distinct_configs_used\": " << global_cfg_uses.size() << ",\n"
              << "  \"used_cfg_ids\": [";
        bool fu = true;
        for (auto [cid, cnt] : global_cfg_uses) { if (!fu) fsumm << ","; fu = false; fsumm << cid; }
        fsumm << "],\n  \"degrees\": " << summ_deg_json.str() << "\n}\n";
        return 0;
    }

    // Modes: "sep", "profile", "degs"
    bool is_profile = (mode == "profile");
    int cut_cap_S = is_profile ? k_thin : 0;
    std::vector<std::atomic<int>> cfg_leaf_cnt(ncfgs);
    for (int i = 0; i < ncfgs; ++i) cfg_leaf_cnt[i].store(0);

    std::vector<LeafRecord> collected;
    std::mutex col_mtx;
    long long grand_violated = 0;
    long long grand_thin = 0;

    for (int d = 5; d <= d_max; ++d) {
        if (!filter_degs.empty() && !filter_degs.count(d)) continue;
        auto td0 = std::chrono::steady_clock::now();
        auto words = (d <= 8) ? gen_canon_links_small(d) : gen_cplus_words_karp(d, scale_M, kr);
        int nw = (int)words.size();
        std::atomic<int> next_idx{0};
        std::atomic<long long> deg_viol{0}, deg_thin{0};

        auto worker = [&]() {
            std::vector<LeafRecord> local_recs;
            while (true) {
                int idx = next_idx.fetch_add(1);
                if (idx >= nw) break;
                const auto& link = words[idx];
                Window W(d, link);
                std::vector<Inst> plus_t, minus_t;
                build_ub_terms(W, parts, plus_t, minus_t);
                int base = scale_M * (6 - d);
                int init_p = 0, init_m = 0;
                for (const auto& x : plus_t) init_p += x.weight;
                for (const auto& x : minus_t) if (x.conds.empty()) init_m += x.weight;
                if (base + init_p - init_m <= 0) continue;

                PreparedDFS pd(base, plus_t, minus_t);
                std::set<int> rel_set(pd.vars.begin(), pd.vars.end());
                auto cands_S = find_link_embeddings(W, active_cfgs, rel_set, false);
                PreparedReqs pr_S(pd, cands_S);

                std::vector<int> dead_p(plus_t.size(), 0), dead_m(minus_t.size(), 0);
                std::vector<int> rem_m = pd.init_rem_minus;
                std::vector<int> dead_r(pr_S.nr, 0), rem_r = pr_S.init_rem;
                std::vector<int> branch_rep(pd.nv, 9);
                std::vector<int> branch_mask(pd.nv, 0x1F);

                // Collect thin/violated leaves on this word first; only run ext_cfgs if at least one leaf found!
                struct RawLeaf {
                    int ub;
                    std::vector<int> brep;
                    std::vector<int> bmask;
                    std::vector<int> kS;
                };
                std::vector<RawLeaf> raw_leaves;

                auto dfs = [&](auto& self, int depth, int cur_p, int cur_m) -> void {
                    int ub = base + cur_p - cur_m;
                    if (ub <= 0) return;

                    // Count distinct satisfied configs in S at this node
                    int sat_cnt = 0;
                    int last_cid = -1;
                    int first_cid = -1;
                    for (int r = 0; r < pr_S.nr; ++r) {
                        if (dead_r[r] == 0 && rem_r[r] == 0) {
                            int cid = pr_S.cfg_of[r];
                            if (cid != last_cid) {
                                last_cid = cid;
                                if (sat_cnt == 0) first_cid = cid;
                                sat_cnt++;
                                if (sat_cnt > cut_cap_S) return;
                            }
                        }
                    }
                    if (is_profile && sat_cnt == 1 && cap_per_cfg > 0 &&
                        cfg_leaf_cnt[first_cid].load(std::memory_order_relaxed) >= cap_per_cfg) {
                        return;
                    }
                    if (mode == "sep" && (int)raw_leaves.size() >= 32) {
                        return;
                    }

                    if (depth == pd.nv) {
                        std::vector<int> kS;
                        int prev_c = -1;
                        for (int r = 0; r < pr_S.nr; ++r) {
                            if (dead_r[r] == 0 && rem_r[r] == 0 && pr_S.cfg_of[r] != prev_c) {
                                prev_c = pr_S.cfg_of[r];
                                kS.push_back(prev_c);
                            }
                        }
                        if (is_profile && kS.size() == 1) {
                            int cur_c = cfg_leaf_cnt[kS[0]].fetch_add(1, std::memory_order_relaxed);
                            if (cap_per_cfg > 0 && cur_c >= cap_per_cfg) return;
                        }
                        raw_leaves.push_back({ub, branch_rep, branch_mask, std::move(kS)});
                        return;
                    }

                    bool same9[9] = {false, false, false, false, false, true, true, true, true};
                    for (auto [t, lo, hi] : pd.p_conds[depth]) {
                        if (dead_p[t] == 0) {
                            bool in9 = (lo <= 9 && 9 <= hi);
                            for (int x = 5; x <= 8; ++x) if ((lo <= x && x <= hi) != in9) same9[x] = false;
                        }
                    }
                    for (auto [t, lo, hi] : pd.m_conds[depth]) {
                        if (dead_m[t] == 0) {
                            bool in9 = (lo <= 9 && 9 <= hi);
                            for (int x = 5; x <= 8; ++x) if ((lo <= x && x <= hi) != in9) same9[x] = false;
                        }
                    }
                    int c9_mask = (1 << 4);
                    for (int x = 5; x <= 8; ++x) if (same9[x]) c9_mask |= (1 << (x - 5));
                    int reps[5];
                    int n_reps = 0;
                    reps[n_reps++] = 9;
                    for (int x = 5; x <= 8; ++x) if (!same9[x]) reps[n_reps++] = x;

                    for (int bi = 0; bi < n_reps; ++bi) {
                        int rep = reps[bi];
                        branch_rep[depth] = rep;
                        branch_mask[depth] = (rep == 9) ? c9_mask : (1 << (rep - 5));
                        int np = cur_p, nm = cur_m;
                        for (auto [t, lo, hi] : pd.p_conds[depth]) {
                            if (!(lo <= rep && rep <= hi)) {
                                if (dead_p[t] == 0) np -= pd.w_plus[t];
                                dead_p[t]++;
                            }
                        }
                        for (auto [t, lo, hi] : pd.m_conds[depth]) {
                            if (lo <= rep && rep <= hi) {
                                rem_m[t]--;
                                if (rem_m[t] == 0 && dead_m[t] == 0) nm += pd.w_minus[t];
                            } else {
                                dead_m[t]++;
                            }
                        }
                        for (auto [r, deg_req] : pr_S.r_conds[depth]) {
                            if (rep == deg_req) rem_r[r]--;
                            else dead_r[r]++;
                        }

                        self(self, depth + 1, np, nm);

                        for (auto [t, lo, hi] : pd.p_conds[depth]) {
                            if (!(lo <= rep && rep <= hi)) dead_p[t]--;
                        }
                        for (auto [t, lo, hi] : pd.m_conds[depth]) {
                            if (lo <= rep && rep <= hi) rem_m[t]++;
                            else dead_m[t]--;
                        }
                        for (auto [r, deg_req] : pr_S.r_conds[depth]) {
                            if (rep == deg_req) rem_r[r]++;
                            else dead_r[r]--;
                        }

                        // In fast "degs" screening mode, 1 violation on this word is enough to abort the word!
                        if (mode == "degs" && !raw_leaves.empty()) return;
                    }
                };

                dfs(dfs, 0, pd.init_plus_sum, pd.init_sure_minus_sum);
                if (raw_leaves.empty()) continue;

                // Match external pool configs U \ S ONLY on words that actually have raw_leaves (and not in "degs" mode)
                std::vector<EmbWitness> cands_ext;
                if (mode != "degs" && !ext_cfgs.empty()) {
                    cands_ext = find_link_embeddings(W, ext_cfgs, rel_set, false);
                }

                // Evaluate cands_ext on each raw_leaf
                std::unordered_map<int, int> vpos;
                for (int k = 0; k < pd.nv; ++k) vpos[pd.vars[k]] = k;

                std::string lstr = link_str(link);
                for (auto& rl : raw_leaves) {
                    if (rl.kS.empty()) deg_viol++; else deg_thin++;
                    std::vector<int> kU = rl.kS;
                    int prev_e = -1;
                    for (int r = 0; r < (int)cands_ext.size(); ++r) {
                        if (cands_ext[r].cfg_id == prev_e) continue;
                        bool sat = true;
                        for (auto [vc, deg_req] : cands_ext[r].req) {
                            int k = vpos.at(vc);
                            if (rl.brep[k] != deg_req) { sat = false; break; }
                        }
                        if (sat) {
                            prev_e = cands_ext[r].cfg_id;
                            kU.push_back(prev_e);
                        }
                    }
                    std::sort(kU.begin(), kU.end());
                    LeafRecord rec;
                    rec.d = d;
                    rec.link = lstr;
                    rec.ub = rl.ub;
                    for (int k = 0; k < pd.nv; ++k) {
                        std::vector<int> scls;
                        for (int x = 5; x <= 9; ++x) if (rl.bmask[k] & (1 << (x - 5))) scls.push_back(x);
                        rec.var_classes.push_back({pd.vars[k], std::move(scls)});
                    }
                    rec.killers_S = std::move(rl.kS);
                    rec.killers_U = std::move(kU);
                    local_recs.push_back(std::move(rec));
                }
            }
            if (!local_recs.empty()) {
                std::lock_guard<std::mutex> lk(col_mtx);
                for (auto& r : local_recs) collected.push_back(std::move(r));
            }
        };

        std::vector<std::thread> ths;
        for (int t = 0; t < n_threads; ++t) ths.emplace_back(worker);
        for (auto& th : ths) th.join();

        grand_violated += deg_viol.load();
        grand_thin += deg_thin.load();
        double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - td0).count();
        std::cout << "  d=" << std::setw(2) << d << " | words=" << std::setw(6) << nw
                  << " | violated=" << std::setw(6) << deg_viol.load()
                  << " | thin=" << std::setw(7) << deg_thin.load()
                  << " | " << std::fixed << std::setprecision(2) << secs << "s\n";
        if (mode == "degs" && grand_violated > 0) break;
    }

    if (mode != "degs") {
        std::ofstream fout(out_path);
        for (const auto& rec : collected) {
            fout << "{\"d\":" << rec.d << ",\"link\":\"" << rec.link << "\",\"ub\":" << rec.ub << ",\"vars\":[";
            for (size_t i = 0; i < rec.var_classes.size(); ++i) {
                if (i) fout << ",";
                fout << "[" << rec.var_classes[i].first << ",[";
                for (size_t j = 0; j < rec.var_classes[i].second.size(); ++j) {
                    if (j) fout << ",";
                    fout << rec.var_classes[i].second[j];
                }
                fout << "]]";
            }
            fout << "],\"kS\":[";
            for (size_t i = 0; i < rec.killers_S.size(); ++i) { if (i) fout << ","; fout << rec.killers_S[i]; }
            fout << "],\"kU\":[";
            for (size_t i = 0; i < rec.killers_U.size(); ++i) { if (i) fout << ","; fout << rec.killers_U[i]; }
            fout << "]}\n";
        }
    }

    double tot_s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t_start).count();
    std::cout << "[DONE] mode=" << mode << " violated=" << grand_violated
              << " thin=" << grand_thin << " total_secs=" << std::fixed << std::setprecision(2) << tot_s << "s\n";
    return (grand_violated == 0) ? 0 : 1;
}
