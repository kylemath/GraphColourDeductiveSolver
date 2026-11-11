// Automated Surgical 2-Ball Cochain Synthesizer (Scale M=20 Half-Quantum Push + !open Anti-Rules)
//
// Starts from RSST_633 (active_cfgs) and RSST's 71 base parts scaled to M=20 (weight=2 each).
// Precomputes all RotOcc embeddings of RSST_633 across canonical words once at startup (~20s on 3 threads),
// then iteratively eliminates configurations 1-for-0 by synthesizing mirror-closed local 2-ball parts:
//   - Family A (5 <= d <= 8): Half-quantum (w=+1) / full-quantum (w=+2..) single-spoke & 2-spoke split push parts
//   - Family B (6 <= d <= 14): Half-quantum (w=-1) / full-quantum (w=-2..) single-spoke & 2-spoke split !open anti-parts
// Every candidate rule batch is verified against:
//   1. Exact Karp minimum-mean-cycle potential phi* on G_4 (tail_d0 <= 18)
//   2. 0 unkilled positive leaves on ALL words where cid previously embedded
//   3. 0 unkilled positive leaves on ALL words across d = 5 .. max(17, tail_d0) where any new part
//      can contribute to plus_terms (incoming w > 0 or outgoing w < 0), including any newly c+-positive d >= 9 words!
// Finally runs a complete full-world verification sweep from scratch and exports:
//   - synth_rules.txt / synth_rules.json
//   - synth_active.txt (surviving configuration IDs)

#include <algorithm>
#include <atomic>
#include <cassert>
#include <chrono>
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
    bool operator==(const Range& o) const { return lo == o.lo && hi == o.hi; }
    bool operator!=(const Range& o) const { return !(*this == o); }
};

struct Sub {
    Range sp;
    Range hat;
    std::vector<Range> fans;
    bool operator==(const Sub& o) const { return sp == o.sp && hat == o.hat && fans == o.fans; }
};

struct Part {
    std::string tag;
    int n;
    int weight;
    std::vector<Sub> subs;
};

static bool same_subs(const Part& a, const Part& b) {
    return a.n == b.n && a.subs == b.subs;
}

static Part make_mirror_part(const Part& p, const std::string& mtag) {
    Part mp;
    mp.tag = mtag;
    mp.n = p.n;
    mp.weight = p.weight;
    mp.subs.resize(p.n);
    for (int k = 0; k < p.n; ++k) {
        const Sub& s4 = p.subs[((4 - k) % p.n + p.n) % p.n];
        const Sub& s5 = p.subs[((5 - k) % p.n + p.n) % p.n];
        mp.subs[k].sp = s4.sp;
        mp.subs[k].hat = s5.hat;
        mp.subs[k].fans.assign(s4.fans.rbegin(), s4.fans.rend());
    }
    return mp;
}

static void verify_part_valid(const Part& p) {
    assert(5 <= p.n && p.n <= 8);
    assert(p.weight != 0 && (int)p.subs.size() == p.n);
    for (int j = 0; j < p.n; ++j) {
        const Sub& sb = p.subs[j];
        assert(5 <= sb.sp.lo && sb.sp.lo <= sb.sp.hi && sb.sp.hi <= 9);
        assert(5 <= sb.hat.lo && sb.hat.lo <= sb.hat.hi && sb.hat.hi <= 9);
        if (!sb.fans.empty()) {
            assert(sb.sp.lo == sb.sp.hi && 6 <= sb.sp.lo && sb.sp.lo <= 8);
            assert((int)sb.fans.size() == sb.sp.lo - 5);
            for (const auto& fr : sb.fans) {
                assert(5 <= fr.lo && fr.lo <= fr.hi && fr.hi <= 9);
            }
        }
    }
    Part mp = make_mirror_part(p, p.tag + "m");
    Part mmp = make_mirror_part(mp, p.tag);
    assert(same_subs(p, mmp));
}

struct Slot { int kind, val; };

struct Config {
    int id;
    std::string name, source, kind, tier;
    int rim_pinned, ring, m;
    std::vector<int> deg;
    std::vector<std::vector<Slot>> rot;
    std::vector<std::vector<int>> int_adj;
    std::vector<std::set<int>> ring_set;
    std::vector<int> order;
    std::map<int, int> dm;
};

static void compute_search_order(Config& c) {
    std::vector<bool> vis(c.m, false);
    c.order.clear();
    int best0 = 0;
    for (int u = 1; u < c.m; ++u) {
        if (std::make_pair(c.deg[u], (int)c.int_adj[u].size()) >
            std::make_pair(c.deg[best0], (int)c.int_adj[best0].size())) best0 = u;
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
            if (sc > best_sc) { best_sc = sc; best = u; }
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

    bool is_forbidden_9mid(int v) const {
        if (v < 1 + 2 * d) return false;
        int q = v - 1 - 2 * d;
        int i = q / 3, j = (q % 3) + 1;
        return (link[i] >= 9 && j == 2);
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

    std::set<int> all_valid_var_codes() const {
        std::set<int> out;
        for (int i = 0; i < d; ++i) {
            out.insert(100 + i);
            int k = npriv(link[i]);
            for (int j = 1; j <= k; ++j) {
                if (link[i] >= 9 && j == 2) continue;
                out.insert(200 + 3 * i + (j - 1));
            }
        }
        return out;
    }
};

struct Cond {
    int var_code, lo, hi;
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
    int hub_w;
    int weight;
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
    std::sort(conds.begin(), conds.end());
    conds.erase(std::unique(conds.begin(), conds.end()), conds.end());
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

static bool any_plus_term_fits(const Window& W, const std::vector<Part>& new_parts) {
    if (5 <= W.d && W.d <= 8) {
        for (const auto& p : new_parts) {
            if (p.n == W.d && p.weight < 0) {
                for (int a = 0; a < W.d; ++a) {
                    Inst inst;
                    if (fit_part(W, 0, p, a, inst)) return true;
                }
            }
        }
    }
    int dec_u = std::min(W.d, 9);
    bool any_pos_for_u = false;
    for (const auto& p : new_parts) {
        if (p.weight > 0 && p.subs[2].sp.lo <= dec_u && dec_u <= p.subs[2].sp.hi) {
            any_pos_for_u = true;
            break;
        }
    }
    if (!any_pos_for_u) return false;

    for (int i = 0; i < W.d; ++i) {
        int L = W.link[i];
        if (L > 8) continue;
        for (const auto& p : new_parts) {
            if (p.n == L && p.weight > 0 && p.subs[2].sp.lo <= dec_u && dec_u <= p.subs[2].sp.hi) {
                Inst inst;
                if (fit_part(W, 1 + i, p, L - 2, inst)) return true;
            }
        }
    }
    return false;
}

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
                    if (p.weight > 0) { inst.weight = p.weight; minus_terms.push_back(std::move(inst)); }
                    else { inst.weight = -p.weight; plus_terms.push_back(std::move(inst)); }
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
                if (p.weight > 0) { inst.weight = p.weight; plus_terms.push_back(std::move(inst)); }
                else if (!inst.open) { inst.weight = -p.weight; minus_terms.push_back(std::move(inst)); }
            }
        }
    }
}

// --- RotOcc ---
static bool check_rot_ok(int d, const std::vector<int>& link, const Config& cfg,
                         const std::vector<int>& phi) {
    std::vector<int> Z;
    std::unordered_map<int, int> pos_in_Z;
    for (int i = 0; i < d; ++i) {
        int L = link[i];
        if (L == 9) {
            int p1 = 1 + 2 * d + 3 * i + 0, qL = 1000 + 2 * i, qR = 1000 + 2 * i + 1;
            int p3 = 1 + 2 * d + 3 * i + 2, si = 1 + d + i;
            for (int v : {p1, qL, qR, p3, si}) { pos_in_Z[v] = (int)Z.size(); Z.push_back(v); }
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
    auto uf_find = [&](auto& self, int x) -> int { return uf[x] == x ? x : uf[x] = self(self, uf[x]); };
    auto uf_union = [&](int a, int b) {
        a = uf_find(uf_find, a); b = uf_find(uf_find, b);
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
        int h = phi[a], g = cfg.deg[a];
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
            int i = h - 1 - d, t = pos_in_Z.at(h);
            r.push_back(Z[(t + 1) % M]);
            r.push_back(1 + ((i + 1) % d));
            r.push_back(1 + i);
            r.push_back(Z[(t + M - 1) % M]);
            if (g == 5) r.push_back(2000 + uf_find(uf_find, (t + M - 1) % M));
            else {
                r.push_back(2000 + uf_find(uf_find, (t + M - 1) % M));
                for (int k = 0; k < g - 6; ++k) r.push_back(next_fresh++);
                r.push_back(2000 + uf_find(uf_find, t));
            }
        } else {
            if (g < 5 || g > 8) return false;
            int q = h - 1 - 2 * d, i = q / 3, j = (q % 3) + 1;
            if (link[i] >= 9 && j == 2) return false;
            int t = pos_in_Z.at(h);
            r.push_back(Z[(t + 1) % M]);
            r.push_back(1 + i);
            r.push_back(Z[(t + M - 1) % M]);
            r.push_back(2000 + uf_find(uf_find, (t + M - 1) % M));
            for (int k = 0; k < g - 5; ++k) r.push_back(next_fresh++);
            r.push_back(2000 + uf_find(uf_find, t));
        }
        if ((int)r.size() != g) return false;
        std::set<int> uniq(r.begin(), r.end());
        if ((int)uniq.size() != g) return false;
    }
    for (int sg : {1, -1}) {
        std::vector<int> rho(cfg.ring, -1);
        auto dfs_rot = [&](auto& self, int step) -> bool {
            if (step == cfg.m) return true;
            int a = cfg.order[step], g = cfg.deg[a];
            const auto& rc = cfg.rot[a];
            const auto& rfa = rf[a];
            std::vector<int> cand_shifts;
            int first_i_pos = -1, first_i_nb = -1;
            for (int k = 0; k < g; ++k) if (rc[k].kind == 0) { first_i_pos = k; first_i_nb = rc[k].val; break; }
            if (first_i_pos != -1) {
                int target = phi[first_i_nb];
                for (int idx = 0; idx < g; ++idx)
                    if (rfa[idx] == target) cand_shifts.push_back(((idx - sg * first_i_pos) % g + g) % g);
            } else {
                for (int sh = 0; sh < g; ++sh) cand_shifts.push_back(sh);
            }
            for (int sh : cand_shifts) {
                bool ok = true;
                std::vector<std::pair<int, int>> added;
                for (int k = 0; k < g; ++k) {
                    int fv = rfa[((sh + sg * k) % g + g) % g];
                    if (rc[k].kind == 0) {
                        if (fv != phi[rc[k].val]) { ok = false; break; }
                    } else {
                        if (phi_set.count(fv)) { ok = false; break; }
                        int ri = rc[k].val;
                        if (rho[ri] == -1) { rho[ri] = fv; added.push_back({ri, -1}); }
                        else if (rho[ri] != fv) { ok = false; break; }
                    }
                }
                if (ok && self(self, step + 1)) return true;
                for (auto [ri, oldv] : added) rho[ri] = oldv;
            }
            return false;
        };
        if (dfs_rot(dfs_rot, 0)) return true;
    }
    return false;
}

struct CompactEmb {
    int cfg_id;
    std::vector<std::pair<int, int>> req;
};

static std::vector<CompactEmb> compute_word_embs_all_vars(const Window& W, const std::vector<Config>& cfgs) {
    std::set<int> all_vars = W.all_valid_var_codes();
    std::vector<int> hosts = {0};
    std::unordered_map<int, std::set<int>> host_degs;
    std::unordered_map<int, int> host_var;
    host_degs[0] = {W.d};
    for (int i = 0; i < W.d; ++i) {
        if (W.link[i] <= 8) { hosts.push_back(1 + i); host_degs[1 + i] = {W.link[i]}; }
        int sv = 1 + W.d + i, sc = 100 + i;
        hosts.push_back(sv); host_degs[sv] = {5, 6, 7, 8}; host_var[sv] = sc;
        int k = npriv(W.link[i]);
        for (int j = 1; j <= k; ++j) {
            if (W.link[i] >= 9 && j == 2) continue;
            int pv = 1 + 2 * W.d + 3 * i + (j - 1), pc = 200 + 3 * i + (j - 1);
            hosts.push_back(pv); host_degs[pv] = {5, 6, 7, 8}; host_var[pv] = pc;
        }
    }
    std::unordered_map<int, std::set<int>> adj_set;
    for (int h : hosts) adj_set[h] = {};
    auto add_e = [&](int a, int b) {
        if (a != b && host_degs.count(a) && host_degs.count(b)) {
            adj_set[a].insert(b); adj_set[b].insert(a);
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

    std::vector<CompactEmb> out;
    for (const auto& cfg : cfgs) {
        if (cfg.m > (int)hosts.size()) continue;
        bool deg_ok = true;
        for (auto [dg, cnt] : cfg.dm) if (hc[dg] < cnt) { deg_ok = false; break; }
        if (!deg_ok) continue;

        std::set<std::vector<std::pair<int, int>>> cfg_reqs;
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
                if (check_rot_ok(W.d, W.link, cfg, phi)) cfg_reqs.insert(std::move(req));
                return;
            }
            int x = cfg.order[k], anchor_nb = -1;
            for (int prev_idx = 0; prev_idx < k; ++prev_idx) {
                int y = cfg.order[prev_idx];
                if (std::binary_search(cfg.int_adj[x].begin(), cfg.int_adj[x].end(), y)) { anchor_nb = y; break; }
            }
            const std::vector<int>& cands = (anchor_nb == -1) ? hosts : adj_vec[phi[anchor_nb]];
            for (int t : cands) {
                if (used_h.count(t) || !host_degs[t].count(cfg.deg[x])) continue;
                bool ind_ok = true;
                for (int prev_idx = 0; prev_idx < k; ++prev_idx) {
                    int y = cfg.order[prev_idx];
                    if (std::binary_search(cfg.int_adj[x].begin(), cfg.int_adj[x].end(), y) !=
                        (adj_set[t].count(phi[y]) > 0)) { ind_ok = false; break; }
                }
                if (!ind_ok) continue;
                phi[x] = t; used_h.insert(t);
                self(self, k + 1);
                used_h.erase(t); phi[x] = -1;
            }
        };
        rec(rec, 0);

        std::vector<std::vector<std::pair<int, int>>> craw(cfg_reqs.begin(), cfg_reqs.end());
        std::sort(craw.begin(), craw.end(), [](const auto& a, const auto& b) { return a.size() < b.size(); });
        std::vector<std::vector<std::pair<int, int>>> ckeep;
        for (auto& rq : craw) {
            bool sub = false;
            for (const auto& kr : ckeep) {
                if (std::includes(rq.begin(), rq.end(), kr.begin(), kr.end())) { sub = true; break; }
            }
            if (!sub) {
                ckeep.push_back(rq);
                out.push_back({cfg.id, std::move(rq)});
            }
        }
    }
    return out;
}

static std::tuple<int, int, int> site_key(int c) {
    if (c < 200) return {c - 100, 0, 0};
    return {(c - 200) / 3, 1, (c - 200) % 3};
}

static std::vector<std::vector<int>> classes_of(int v, const std::vector<Inst>& allc) {
    std::vector<std::pair<int, int>> ts;
    for (const auto& inst : allc) for (const auto& cd : inst.conds) if (cd.var_code == v) ts.push_back({cd.lo, cd.hi});
    auto pat = [&](int x) {
        std::vector<bool> p;
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
    std::vector<int> dead_p(plus_w2.size(), 0), dead_m(minus_w2.size(), 0), rem_m(minus_w2.size(), 0);
    int init_sure_m = 0;
    for (int t = 0; t < (int)minus_w2.size(); ++t) {
        rem_m[t] = (int)minus_w2[t].conds.size();
        if (rem_m[t] == 0) init_sure_m += minus_w2[t].weight;
    }
    int best = -1000000000;
    auto rec = [&](auto& self, int k, int cur_p, int cur_sure_m) -> void {
        if (cur_p - cur_sure_m <= best) return;
        if (k == nv) { best = cur_p - cur_sure_m; return; }
        for (int val : {5, 6, 7, 8, 9}) {
            int np = cur_p, nm = cur_sure_m;
            for (auto [t, lo, hi] : by_p[k]) {
                if (!(lo <= val && val <= hi)) { if (dead_p[t] == 0) np -= plus_w2[t].weight; dead_p[t]++; }
            }
            for (auto [t, lo, hi] : by_m[k]) {
                if (lo <= val && val <= hi) { rem_m[t]--; if (rem_m[t] == 0 && dead_m[t] == 0) nm += minus_w2[t].weight; }
                else dead_m[t]++;
            }
            self(self, k + 1, np, nm);
            for (auto [t, lo, hi] : by_p[k]) if (!(lo <= val && val <= hi)) dead_p[t]--;
            for (auto [t, lo, hi] : by_m[k]) { if (lo <= val && val <= hi) rem_m[t]++; else dead_m[t]--; }
        }
    };
    rec(rec, 0, init_p, init_sure_m);
    return (best == -1000000000) ? 0 : best;
}

struct KarpResult {
    int CP[5][5][5][5][5];
    int max_cp;
    long long P_num, Q_den;
    long long Phi[625];
    long long E_shift[5][5][5][5][5];
    long long emax_center[10], emax_all;
    int tail_d0;
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
        long long min_p = 0, min_q = 1;
        bool has_k = false;
        for (int k = 0; k < N; ++k) {
            if (dp[k][v] == NEG_INF) continue;
            long long p = dp[N][v] - dp[k][v], q = N - k;
            if (!has_k || p * min_q < min_p * q) { min_p = p; min_q = q; has_k = true; }
        }
        if (has_k && (!has_v || min_p * best_Q > best_P * min_q)) { best_P = min_p; best_Q = min_q; has_v = true; }
    }
    long long g = std::gcd(std::abs(best_P), best_Q);
    kr.P_num = best_P / g;
    kr.Q_den = best_Q / g;

    std::vector<long long> dist(N, 0);
    for (int iter = 0; iter <= N; ++iter) {
        bool changed = false;
        for (int x = 0; x < N; ++x) {
            int a = (x / 125) % 5, b = (x / 25) % 5, c = (x / 5) % 5, d = x % 5;
            for (int e = 0; e < 5; ++e) {
                int y = b * 125 + c * 25 + d * 5 + e;
                long long wp = kr.Q_den * (long long)kr.CP[a][b][c][d][e] - kr.P_num;
                if (dist[x] + wp > dist[y]) {
                    assert(iter < N);
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
        int x = a * 125 + b * 25 + c * 5 + d, y = b * 125 + c * 25 + d * 5 + e;
        long long es = kr.Q_den * (long long)kr.CP[a][b][c][d][e] + kr.Phi[y] - kr.Phi[x];
        assert(es <= kr.P_num);
        kr.E_shift[a][b][c][d][e] = es;
        kr.emax_center[c + 5] = std::max(kr.emax_center[c + 5], es);
        kr.emax_all = std::max(kr.emax_all, es);
    }
    long long denom = (long long)scale_M * kr.Q_den - kr.P_num;
    if (denom <= 0) kr.tail_d0 = 999999;
    else {
        kr.tail_d0 = (int)((6LL * scale_M * kr.Q_den + denom - 1) / denom);
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
        if (k == d) { if (is_dihedral_canon(cur)) out.push_back(cur); return; }
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
            if (i - 2 >= 0 && i + 2 <= k - 1) s += kr.E_shift[L[i - 2] - 5][L[i - 1] - 5][L[i] - 5][L[i + 1] - 5][L[i + 2] - 5];
            else if (i <= k - 1) s += kr.emax_center[L[i]];
            else s += kr.emax_all;
        }
        return s;
    };
    auto rec = [&](auto& self, int k) -> void {
        if (k == d) {
            if (!is_dihedral_canon(L)) return;
            long long cyc = (long long)scale_M * (6 - d);
            for (int i = 0; i < d; ++i)
                cyc += kr.CP[L[(i + d - 2) % d] - 5][L[(i + d - 1) % d] - 5][L[i] - 5][L[(i + 1) % d] - 5][L[(i + 2) % d] - 5];
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
    for (int x : link) s.push_back(char('0' + x));
    return s;
}

// Fast DFS word evaluator using cached CompactEmb
struct ForcedLeaf {
    int d;
    std::vector<int> link;
    int ub;
    std::map<int, std::vector<int>> vcls; // var_code -> class vec
};

static bool check_word_dfs(
    const Window& W, int scale_M, const std::vector<Part>& parts,
    const std::vector<CompactEmb>& word_embs, const std::vector<bool>& active_mask,
    bool collect_leaves, int cap_leaves, std::vector<ForcedLeaf>* out_leaves) {

    std::vector<Inst> plus_t, minus_t;
    build_ub_terms(W, parts, plus_t, minus_t);
    int base = scale_M * (6 - W.d);
    int init_p = 0, init_m = 0;
    for (const auto& x : plus_t) init_p += x.weight;
    for (const auto& x : minus_t) if (x.conds.empty()) init_m += x.weight;
    if (base + init_p - init_m <= 0) return true;

    std::vector<Inst> allc = plus_t;
    allc.insert(allc.end(), minus_t.begin(), minus_t.end());
    std::set<int> rel_set;
    for (const auto& I : allc) for (const auto& cd : I.conds) rel_set.insert(cd.var_code);
    std::vector<int> vars(rel_set.begin(), rel_set.end());
    std::sort(vars.begin(), vars.end(), [](int a, int b) { return site_key(a) < site_key(b); });
    int nv = (int)vars.size();
    std::unordered_map<int, int> vpos;
    for (int k = 0; k < nv; ++k) vpos[vars[k]] = k;

    std::vector<std::vector<std::vector<int>>> classes(nv);
    std::vector<std::vector<std::vector<int>>> killed_p(nv), sat_m(nv), killed_m(nv);
    for (int k = 0; k < nv; ++k) {
        classes[k] = classes_of(vars[k], allc);
        int nb = (int)classes[k].size();
        killed_p[k].resize(nb); sat_m[k].resize(nb); killed_m[k].resize(nb);
    }

    for (size_t t = 0; t < plus_t.size(); ++t) {
        for (const auto& cd : plus_t[t].conds) {
            int k = vpos.at(cd.var_code);
            for (int b = 0; b < (int)classes[k].size(); ++b) {
                int rep = classes[k][b][0];
                if (!(cd.lo <= rep && rep <= cd.hi)) killed_p[k][b].push_back((int)t);
            }
        }
    }
    std::vector<int> init_rem_m(minus_t.size());
    for (size_t t = 0; t < minus_t.size(); ++t) {
        init_rem_m[t] = (int)minus_t[t].conds.size();
        for (const auto& cd : minus_t[t].conds) {
            int k = vpos.at(cd.var_code);
            for (int b = 0; b < (int)classes[k].size(); ++b) {
                int rep = classes[k][b][0];
                if (cd.lo <= rep && rep <= cd.hi) sat_m[k][b].push_back((int)t);
                else killed_m[k][b].push_back((int)t);
            }
        }
    }

    // Filter word_embs: active_mask[cfg_id] == true AND every req variable is in vpos!
    // (Any req variable NOT in vpos has class {5,6,7,8,9} implicitly so it can never be singleton <= 8!)
    std::vector<const CompactEmb*> valid_embs;
    for (const auto& ce : word_embs) {
        if (!active_mask[ce.cfg_id]) continue;
        bool ok_v = true;
        for (auto [vc, dg] : ce.req) if (!vpos.count(vc)) { ok_v = false; break; }
        if (ok_v) valid_embs.push_back(&ce);
    }
    int nr = (int)valid_embs.size();
    std::vector<int> init_rem_r(nr);
    std::vector<std::vector<std::vector<int>>> sat_r(nv), killed_r(nv);
    for (int k = 0; k < nv; ++k) {
        sat_r[k].resize(classes[k].size());
        killed_r[k].resize(classes[k].size());
    }
    for (int r = 0; r < nr; ++r) {
        init_rem_r[r] = (int)valid_embs[r]->req.size();
        // Immediate root kill check!
        if (init_rem_r[r] == 0) return true;
        for (auto [vc, dg] : valid_embs[r]->req) {
            int k = vpos.at(vc);
            for (int b = 0; b < (int)classes[k].size(); ++b) {
                const auto& S = classes[k][b];
                if (S.size() == 1 && S[0] == dg) sat_r[k][b].push_back(r);
                else killed_r[k][b].push_back(r);
            }
        }
    }

    std::vector<int> dead_p(plus_t.size(), 0), dead_m(minus_t.size(), 0), rem_m = init_rem_m;
    std::vector<int> dead_r(nr, 0), rem_r = init_rem_r;
    std::vector<int> bhist(nv, 0);
    bool all_ok = true;

    auto dfs = [&](auto& self, int depth, int cur_p, int cur_m) -> void {
        if (!collect_leaves && !all_ok) return;
        if (collect_leaves && out_leaves && (int)out_leaves->size() > cap_leaves) return;

        int ub = base + cur_p - cur_m;
        if (ub <= 0) return;
        for (int r = 0; r < nr; ++r) {
            if (dead_r[r] == 0 && rem_r[r] == 0) return;
        }
        if (depth == nv) {
            all_ok = false;
            if (collect_leaves && out_leaves) {
                ForcedLeaf fl;
                fl.d = W.d;
                fl.link = W.link;
                fl.ub = ub;
                for (int k = 0; k < nv; ++k) fl.vcls[vars[k]] = classes[k][bhist[k]];
                out_leaves->push_back(std::move(fl));
            }
            return;
        }
        int nb = (int)classes[depth].size();
        for (int b = 0; b < nb; ++b) {
            bhist[depth] = b;
            int np = cur_p, nm = cur_m;
            for (int t : killed_p[depth][b]) { if (dead_p[t] == 0) np -= plus_t[t].weight; dead_p[t]++; }
            for (int t : sat_m[depth][b]) { rem_m[t]--; if (rem_m[t] == 0 && dead_m[t] == 0) nm += minus_t[t].weight; }
            for (int t : killed_m[depth][b]) dead_m[t]++;
            for (int r : sat_r[depth][b]) rem_r[r]--;
            for (int r : killed_r[depth][b]) dead_r[r]++;

            self(self, depth + 1, np, nm);

            for (int t : killed_p[depth][b]) dead_p[t]--;
            for (int t : sat_m[depth][b]) rem_m[t]++;
            for (int t : killed_m[depth][b]) dead_m[t]--;
            for (int r : sat_r[depth][b]) rem_r[r]++;
            for (int r : killed_r[depth][b]) dead_r[r]--;
            if (!collect_leaves && !all_ok) return;
            if (collect_leaves && out_leaves && (int)out_leaves->size() > cap_leaves) return;
        }
    };
    dfs(dfs, 0, init_p, init_m);
    return all_ok;
}

// --- Synthesize Candidate Mirror-Closed Part Batches on a Same-(d, link) Group of Leaves ---
static Range hull_var_range(const std::vector<ForcedLeaf>& grp, int vc) {
    int lo = 9, hi = 5;
    for (const auto& fl : grp) {
        auto it = fl.vcls.find(vc);
        if (it == fl.vcls.end()) return {5, 9};
        for (int x : it->second) { lo = std::min(lo, x); hi = std::max(hi, x); }
    }
    return {lo, hi};
}

static bool inst_sure_on_leaf(const Inst& inst, const ForcedLeaf& fl) {
    if (inst.open) return false;
    for (const auto& cd : inst.conds) {
        auto it = fl.vcls.find(cd.var_code);
        if (it == fl.vcls.end()) return false;
        for (int x : it->second) if (!(cd.lo <= x && x <= cd.hi)) return false;
    }
    return true;
}

static bool inst_alive_on_leaf(const Inst& inst, const ForcedLeaf& fl) {
    for (const auto& cd : inst.conds) {
        auto it = fl.vcls.find(cd.var_code);
        if (it == fl.vcls.end()) continue; // unconstrained {5..9} always intersects [lo, hi]
        bool any_sat = false;
        for (int x : it->second) {
            if (cd.lo <= x && x <= cd.hi) { any_sat = true; break; }
        }
        if (!any_sat) return false;
    }
    return true;
}

static std::vector<Part> close_mirror_batch(const std::vector<Part>& raw_parts) {
    std::vector<Part> out;
    for (const auto& p : raw_parts) {
        verify_part_valid(p);
        Part mp = make_mirror_part(p, p.tag + "m");
        verify_part_valid(mp);
        out.push_back(p);
        if (!same_subs(p, mp)) out.push_back(mp);
    }
    return out;
}

static Part build_push_part_hull(const Window& W, const std::vector<ForcedLeaf>& grp,
                                 int t_idx, int weight, const std::string& tag) {
    int d = W.d;
    int a = (t_idx - 2 + d) % d;
    Part P;
    P.tag = tag;
    P.n = d;
    P.weight = weight;
    P.subs.resize(d);
    for (int j = 0; j < d; ++j) {
        int i = (a + j) % d;
        int Li = W.link[i];
        P.subs[j].sp = {Li, Li};
        P.subs[j].hat = hull_var_range(grp, 100 + ((i + d - 1) % d));
        if (6 <= Li && Li <= 8) {
            P.subs[j].fans.resize(Li - 5);
            for (int f = 0; f < Li - 5; ++f) {
                P.subs[j].fans[f] = hull_var_range(grp, 200 + 3 * i + f);
            }
        }
    }
    return P;
}

static Part build_anti_part_hull(const Window& W, const std::vector<ForcedLeaf>& grp,
                                 int sp_i, int neg_weight, const std::string& tag) {
    int L = W.link[sp_i];
    assert(5 <= L && L <= 8 && neg_weight < 0);
    int a = L - 2;
    const auto& S = W.rot_w[sp_i];
    Part P;
    P.tag = tag;
    P.n = L;
    P.weight = neg_weight;
    P.subs.resize(L);

    auto range_of_v = [&](int v) -> Range {
        if (v == -1 || W.is_forbidden_9mid(v)) return {5, 9};
        auto [kind, val] = W.deg_info(v);
        if (kind == 0) return {val, val};
        if (kind == 1) return hull_var_range(grp, val);
        return {5, 9};
    };

    for (int j = 0; j < L; ++j) {
        int x = S[(a + j) % L];
        int xp = S[(a + j + L - 1) % L];
        int xn = S[(a + j + 1) % L];
        P.subs[j].sp = range_of_v(x);
        P.subs[j].hat = range_of_v(W.succ(x, xp));
        if (P.subs[j].sp.lo == P.subs[j].sp.hi && 6 <= P.subs[j].sp.lo && P.subs[j].sp.lo <= 8 &&
            (x == 0 || (1 <= x && x <= W.d))) {
            int hv = W.succ(x, xp), hn = W.succ(xn, x);
            const std::vector<int>& Rr = (x == 0) ? W.rot_u : W.rot_w[x - 1];
            int rsz = (int)Rr.size(), idx_hv = -1;
            for (int k = 0; k < rsz; ++k) if (Rr[k] == hv) { idx_hv = k; break; }
            if (idx_hv != -1) {
                int t = (idx_hv + 1) % rsz, guard = 0;
                std::vector<int> F;
                while (Rr[t] != hn && ++guard <= rsz) { F.push_back(Rr[t]); t = (t + 1) % rsz; }
                if ((int)F.size() == P.subs[j].sp.lo - 5) {
                    bool all_visible = true;
                    for (int fv : F) if (fv == -1 || W.is_forbidden_9mid(fv)) all_visible = false;
                    if (all_visible) {
                        P.subs[j].fans.resize(F.size());
                        for (size_t fi = 0; fi < F.size(); ++fi) P.subs[j].fans[fi] = range_of_v(F[fi]);
                    }
                }
            }
        }
    }
    Inst chk;
    bool ok = fit_part(W, 1 + sp_i, P, a, chk);
    assert(ok && !chk.open);
    return P;
}

static bool batch_discharges_group(const Window& W, const std::vector<ForcedLeaf>& grp,
                                   const std::vector<Part>& batch) {
    std::vector<Inst> plus_b, minus_b;
    build_ub_terms(W, batch, plus_b, minus_b);
    for (const auto& fl : grp) {
        int net_red = 0;
        for (const auto& m_inst : minus_b) {
            if (inst_sure_on_leaf(m_inst, fl)) net_red += m_inst.weight;
        }
        for (const auto& p_inst : plus_b) {
            if (inst_alive_on_leaf(p_inst, fl)) net_red -= p_inst.weight;
        }
        if (net_red < fl.ub) return false;
    }
    return true;
}

static std::vector<std::vector<Part>> generate_candidates_for_group(
    const Window& W, const std::vector<ForcedLeaf>& grp, int& uid_counter) {
    std::vector<std::vector<Part>> out;
    int d = W.d;
    int max_ub = 0;
    for (const auto& fl : grp) max_ub = std::max(max_ub, fl.ub);
    if (max_ub <= 0) return out;

    std::vector<int> try_weights = {1};
    int half_w = (max_ub + 1) / 2;
    if (half_w > 1) try_weights.push_back(half_w);
    if (max_ub > half_w) try_weights.push_back(max_ub);

    // 1. Outgoing Push Candidates (5 <= d <= 8)
    if (5 <= d && d <= 8) {
        std::vector<int> order_t(d);
        std::iota(order_t.begin(), order_t.end(), 0);
        std::sort(order_t.begin(), order_t.end(), [&](int a, int b) { return W.link[a] > W.link[b]; });

        // 1a. Two-spoke split first when max_ub >= 2 (gentlest on receivers: w1 + w2 = max_ub)
        if (max_ub >= 2) {
            int w1 = max_ub / 2;
            int w2 = max_ub - w1;
            for (int ii = 0; ii < d; ++ii) {
                int t1 = order_t[ii];
                if (W.link[t1] < 6) continue;
                for (int jj = ii + 1; jj < d; ++jj) {
                    int t2 = order_t[jj];
                    if (W.link[t2] < 6) continue;
                    Part p1 = build_push_part_hull(W, grp, t1, w2, "SP_" + std::to_string(++uid_counter));
                    Part p2 = build_push_part_hull(W, grp, t2, w1, "SP_" + std::to_string(++uid_counter));
                    auto batch = close_mirror_batch({p1, p2});
                    if (batch_discharges_group(W, grp, batch)) out.push_back(std::move(batch));
                }
            }
        }

        // 1b. Single-spoke push (try smallest sufficient weight first!)
        for (int t_idx : order_t) {
            if (W.link[t_idx] < 6) continue;
            for (int w_try : try_weights) {
                Part p = build_push_part_hull(W, grp, t_idx, w_try, "SP_" + std::to_string(++uid_counter));
                auto batch = close_mirror_batch({p});
                if (batch_discharges_group(W, grp, batch)) {
                    out.push_back(std::move(batch));
                    break;
                }
            }
        }
    }

    // 2. Incoming !open Anti-Rule Candidates (d >= 7, including d = 9, 10, 11, 12!)
    if (d >= 7) {
        std::vector<int> senders;
        for (int i = 0; i < d; ++i) if (W.link[i] <= 8) senders.push_back(i);
        // Try higher-degree senders (8, 7) first (they have negative curvature slack -40, -20!), then 6, 5!
        std::sort(senders.begin(), senders.end(), [&](int a, int b) { return W.link[a] > W.link[b]; });

        // 2a. Two-sender anti-rule split when max_ub >= 2
        if (max_ub >= 2 && senders.size() >= 2) {
            int w1 = max_ub / 2;
            int w2 = max_ub - w1;
            for (size_t ii = 0; ii < senders.size() && ii < 7; ++ii) {
                for (size_t jj = ii + 1; jj < senders.size() && jj < 8; ++jj) {
                    Part p1 = build_anti_part_hull(W, grp, senders[ii], -w2, "SA_" + std::to_string(++uid_counter));
                    Part p2 = build_anti_part_hull(W, grp, senders[jj], -w1, "SA_" + std::to_string(++uid_counter));
                    auto batch = close_mirror_batch({p1, p2});
                    if (batch_discharges_group(W, grp, batch)) out.push_back(std::move(batch));
                }
            }
        }

        // 2b. Single-sender anti-rule (try smallest sufficient |w| first!)
        for (int sp_i : senders) {
            for (int w_abs : try_weights) {
                Part p = build_anti_part_hull(W, grp, sp_i, -w_abs, "SA_" + std::to_string(++uid_counter));
                auto batch = close_mirror_batch({p});
                if (batch_discharges_group(W, grp, batch)) {
                    out.push_back(std::move(batch));
                    break;
                }
            }
        }
    }

    // 3. Mixed Push + Anti-Rule Split on d = 7, 8 when max_ub >= 2 (splits load across 1 receiver + 1 sender!)
    if ((d == 7 || d == 8) && max_ub >= 2) {
        int w_push = max_ub - (max_ub / 2);
        int w_anti = max_ub / 2;
        std::vector<int> recvs, sends;
        for (int i = 0; i < d; ++i) {
            if (W.link[i] >= 7) recvs.push_back(i);
            if (W.link[i] <= 8) sends.push_back(i);
        }
        std::sort(recvs.begin(), recvs.end(), [&](int a, int b) { return W.link[a] > W.link[b]; });
        std::sort(sends.begin(), sends.end(), [&](int a, int b) { return W.link[a] > W.link[b]; });
        for (size_t ii = 0; ii < recvs.size() && ii < 3; ++ii) {
            for (size_t jj = 0; jj < sends.size() && jj < 3; ++jj) {
                if (recvs[ii] == sends[jj]) continue;
                Part p1 = build_push_part_hull(W, grp, recvs[ii], w_push, "SP_" + std::to_string(++uid_counter));
                Part p2 = build_anti_part_hull(W, grp, sends[jj], -w_anti, "SA_" + std::to_string(++uid_counter));
                auto batch = close_mirror_batch({p1, p2});
                if (batch_discharges_group(W, grp, batch)) out.push_back(std::move(batch));
            }
        }
    }
    return out;
}

int main(int argc, char** argv) {
    std::string pool_path = "/Users/kylemathewson/GraphColouringNov/beat_633/data/pool_input.txt";
    std::string out_rules_txt = "/Users/kylemathewson/GraphColouringNov/beat_633/data/synth_rules.txt";
    std::string out_active_txt = "/Users/kylemathewson/GraphColouringNov/beat_633/data/synth_active.txt";
    int n_threads = 3;
    int max_leaf_cap = 350;
    int max_passes = 3;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--pool" && i + 1 < argc) pool_path = argv[++i];
        else if (arg == "--out-rules" && i + 1 < argc) out_rules_txt = argv[++i];
        else if (arg == "--out-active" && i + 1 < argc) out_active_txt = argv[++i];
        else if (arg == "--threads" && i + 1 < argc) n_threads = std::max(1, std::stoi(argv[++i]));
        else if (arg == "--max-leaves" && i + 1 < argc) max_leaf_cap = std::stoi(argv[++i]);
        else if (arg == "--passes" && i + 1 < argc) max_passes = std::stoi(argv[++i]);
    }

    auto t0_all = std::chrono::steady_clock::now();
    std::ifstream fpool(pool_path);
    assert(fpool && "Cannot open pool_path");
    std::string hdr;
    int orig_M = 10, nparts = 0;
    fpool >> hdr >> orig_M >> hdr >> nparts;
    assert(orig_M == 10);

    // Scale to M = 20 (each base RSST part gets weight 2) to unlock half-quantum (±1 = ±0.05) transfers!
    int scale_M = 20;
    std::vector<Part> parts(nparts);
    for (int i = 0; i < nparts; ++i) {
        int w_in = 1;
        fpool >> parts[i].tag >> parts[i].n >> w_in;
        parts[i].weight = w_in * 2;
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
        verify_part_valid(parts[i]);
    }

    int ncfgs_all = 0;
    fpool >> hdr >> ncfgs_all;
    std::vector<Config> rsst_cfgs(633);
    for (int i = 0; i < ncfgs_all; ++i) {
        Config c;
        fpool >> c.id >> c.name >> c.source >> c.kind >> c.tier >> c.rim_pinned >> c.ring >> c.m;
        c.deg.resize(c.m); c.rot.resize(c.m); c.int_adj.resize(c.m); c.ring_set.resize(c.m);
        for (int u = 0; u < c.m; ++u) {
            int g = 0; fpool >> g; c.deg[u] = g; c.dm[g]++; c.rot[u].resize(g);
            for (int k = 0; k < g; ++k) {
                fpool >> c.rot[u][k].kind >> c.rot[u][k].val;
                if (c.rot[u][k].kind == 0) c.int_adj[u].push_back(c.rot[u][k].val);
                else c.ring_set[u].insert(c.rot[u][k].val);
            }
            std::sort(c.int_adj[u].begin(), c.int_adj[u].end());
        }
        compute_search_order(c);
        if (i < 633) rsst_cfgs[i] = std::move(c);
    }

    KarpResult kr_cur = solve_karp_potential(scale_M, parts);
    std::cout << "[INIT] scale_M=" << scale_M << " base_parts=" << parts.size()
              << " lambda*=" << kr_cur.P_num << "/" << kr_cur.Q_den << " tail_d0=" << kr_cur.tail_d0 << "\n";

    // Precompute canonical words for d = 5..8, and dynamic cache for d >= 9 words -> RotOcc embeddings of RSST_633!
    struct WordEntry {
        int d;
        std::vector<int> link;
        Window W;
        std::vector<CompactEmb> embs;
        WordEntry(int d_, const std::vector<int>& l_) : d(d_), link(l_), W(d_, l_) {}
    };

    std::unordered_map<std::string, int> word_idx_by_key;
    std::vector<WordEntry> word_cache;
    std::vector<std::vector<int>> cfg_word_indices(633);

    auto ensure_words_cached = [&](const std::vector<std::pair<int, std::vector<int>>>& req_words) {
        std::vector<int> to_compute;
        for (const auto& [d, lk] : req_words) {
            std::string key = std::to_string(d) + ":" + link_str(lk);
            if (!word_idx_by_key.count(key)) {
                int widx = (int)word_cache.size();
                word_idx_by_key[key] = widx;
                word_cache.emplace_back(d, lk);
                to_compute.push_back(widx);
            }
        }
        if (to_compute.empty()) return;
        std::atomic<size_t> next_i{0};
        auto worker = [&]() {
            while (true) {
                size_t ii = next_i.fetch_add(1);
                if (ii >= to_compute.size()) break;
                int widx = to_compute[ii];
                word_cache[widx].embs = compute_word_embs_all_vars(word_cache[widx].W, rsst_cfgs);
            }
        };
        std::vector<std::thread> ths;
        for (int t = 0; t < n_threads; ++t) ths.emplace_back(worker);
        for (auto& th : ths) th.join();

        for (int widx : to_compute) {
            int prev_c = -1;
            for (const auto& ce : word_cache[widx].embs) {
                if (ce.cfg_id != prev_c) {
                    prev_c = ce.cfg_id;
                    cfg_word_indices[prev_c].push_back(widx);
                }
            }
        }
    };

    // Seed cache with all d = 5..8 canonical words + initial d = 9..17 c+-positive words
    // (Load from / save to binary disk cache so subsequent runs start in < 1s!)
    std::string bin_cache_path = "/Users/kylemathewson/GraphColouringNov/beat_633/data/word_embs_cache_v1.bin";
    {
        auto tp0 = std::chrono::steady_clock::now();
        std::ifstream fbin(bin_cache_path, std::ios::binary);
        bool loaded_ok = false;
        if (fbin) {
            uint32_t magic = 0, n_entries = 0;
            fbin.read(reinterpret_cast<char*>(&magic), sizeof(magic));
            fbin.read(reinterpret_cast<char*>(&n_entries), sizeof(n_entries));
            if (magic == 0x524F5431U && n_entries > 0) {
                word_cache.reserve(n_entries);
                for (uint32_t wi = 0; wi < n_entries; ++wi) {
                    int32_t d_in = 0;
                    fbin.read(reinterpret_cast<char*>(&d_in), sizeof(d_in));
                    std::vector<int> lk(d_in);
                    for (int k = 0; k < d_in; ++k) {
                        int32_t lv = 0;
                        fbin.read(reinterpret_cast<char*>(&lv), sizeof(lv));
                        lk[k] = lv;
                    }
                    int widx = (int)word_cache.size();
                    std::string key = std::to_string(d_in) + ":" + link_str(lk);
                    word_idx_by_key[key] = widx;
                    word_cache.emplace_back(d_in, lk);
                    uint32_t n_embs = 0;
                    fbin.read(reinterpret_cast<char*>(&n_embs), sizeof(n_embs));
                    word_cache[widx].embs.resize(n_embs);
                    int prev_c = -1;
                    for (uint32_t ei = 0; ei < n_embs; ++ei) {
                        int32_t cid_in = 0;
                        uint16_t n_req = 0;
                        fbin.read(reinterpret_cast<char*>(&cid_in), sizeof(cid_in));
                        fbin.read(reinterpret_cast<char*>(&n_req), sizeof(n_req));
                        auto& ce = word_cache[widx].embs[ei];
                        ce.cfg_id = cid_in;
                        ce.req.resize(n_req);
                        for (uint16_t ri = 0; ri < n_req; ++ri) {
                            int16_t vc_in = 0, dg_in = 0;
                            fbin.read(reinterpret_cast<char*>(&vc_in), sizeof(vc_in));
                            fbin.read(reinterpret_cast<char*>(&dg_in), sizeof(dg_in));
                            ce.req[ri] = {vc_in, dg_in};
                        }
                        if (ce.cfg_id != prev_c) {
                            prev_c = ce.cfg_id;
                            cfg_word_indices[prev_c].push_back(widx);
                        }
                    }
                }
                if (fbin) loaded_ok = true;
            }
        }
        std::vector<std::pair<int, std::vector<int>>> init_words;
        for (int d = 5; d <= 17; ++d) {
            auto ws = (d <= 8) ? gen_canon_links_small(d) : gen_cplus_words_karp(d, scale_M, kr_cur);
            for (auto& lk : ws) init_words.push_back({d, std::move(lk)});
        }
        size_t bef_sz = word_cache.size();
        ensure_words_cached(init_words);
        double sp = std::chrono::duration<double>(std::chrono::steady_clock::now() - tp0).count();
        std::cout << "[CACHE] " << (loaded_ok ? "Loaded + verified" : "Precomputed")
                  << " RotOcc embeddings on " << word_cache.size()
                  << " canonical words in " << std::fixed << std::setprecision(2) << sp << "s." << std::endl;
        if (!loaded_ok || word_cache.size() > bef_sz) {
            std::ofstream fout_bin(bin_cache_path, std::ios::binary);
            uint32_t magic = 0x524F5431U, n_entries = (uint32_t)word_cache.size();
            fout_bin.write(reinterpret_cast<const char*>(&magic), sizeof(magic));
            fout_bin.write(reinterpret_cast<const char*>(&n_entries), sizeof(n_entries));
            for (const auto& we : word_cache) {
                int32_t d_out = we.d;
                fout_bin.write(reinterpret_cast<const char*>(&d_out), sizeof(d_out));
                for (int lv : we.link) {
                    int32_t lv_out = lv;
                    fout_bin.write(reinterpret_cast<const char*>(&lv_out), sizeof(lv_out));
                }
                uint32_t n_embs = (uint32_t)we.embs.size();
                fout_bin.write(reinterpret_cast<const char*>(&n_embs), sizeof(n_embs));
                for (const auto& ce : we.embs) {
                    int32_t cid_out = ce.cfg_id;
                    uint16_t n_req = (uint16_t)ce.req.size();
                    fout_bin.write(reinterpret_cast<const char*>(&cid_out), sizeof(cid_out));
                    fout_bin.write(reinterpret_cast<const char*>(&n_req), sizeof(n_req));
                    for (auto [vc, dg] : ce.req) {
                        int16_t vc_out = (int16_t)vc, dg_out = (int16_t)dg;
                        fout_bin.write(reinterpret_cast<const char*>(&vc_out), sizeof(vc_out));
                        fout_bin.write(reinterpret_cast<const char*>(&dg_out), sizeof(dg_out));
                    }
                }
            }
        }
    }

    std::vector<bool> active_mask(633, true);
    int active_count = 633;
    int uid_counter = 0;

    auto write_checkpoint = [&]() {
        {
            std::ofstream fr(out_rules_txt);
            fr << "SCALE " << scale_M << "\n";
            fr << "PARTS " << parts.size() << "\n";
            for (const auto& p : parts) {
                fr << p.tag << " " << p.n << " " << p.weight;
                for (const auto& sb : p.subs) {
                    fr << " " << sb.sp.lo << " " << sb.sp.hi << " " << sb.hat.lo << " " << sb.hat.hi << " " << sb.fans.size();
                    for (const auto& fn : sb.fans) fr << " " << fn.lo << " " << fn.hi;
                }
                fr << "\n";
            }
        }
        {
            std::ofstream fa(out_active_txt);
            for (int i = 0; i < 633; ++i) if (active_mask[i]) fa << i << "\n";
        }
    };

    // Verify candidate addition `new_batch` while dropping `drop_cid`:
    // Returns true iff Karp tail <= 18 AND 0 violated leaves exist across:
    //   (a) all words in cfg_word_indices[drop_cid] (if drop_cid >= 0), AND
    //   (b) all canonical words across d = 5 .. max(17, kr_cand.tail_d0) where new_batch fits as a plus_term
    //       OR any newly c+-positive d >= 9 word not previously cached!
    auto verify_batch_and_drop = [&](int drop_cid, const std::vector<Part>& new_batch, KarpResult& out_kr) -> bool {
        std::vector<Part> cand_parts = parts;
        cand_parts.insert(cand_parts.end(), new_batch.begin(), new_batch.end());

        out_kr = solve_karp_potential(scale_M, cand_parts);
        if (out_kr.tail_d0 > 18) return false;

        int d_max = std::max(17, out_kr.tail_d0);
        std::vector<std::pair<int, std::vector<int>>> new_d9_words;
        std::vector<std::vector<std::vector<int>>> d9_lists(d_max + 1);
        for (int d = 9; d <= d_max; ++d) {
            d9_lists[d] = gen_cplus_words_karp(d, scale_M, out_kr);
            for (const auto& lk : d9_lists[d]) {
                std::string key = std::to_string(d) + ":" + link_str(lk);
                if (!word_idx_by_key.count(key)) new_d9_words.push_back({d, lk});
            }
        }
        if (!new_d9_words.empty()) ensure_words_cached(new_d9_words);

        std::vector<bool> mask_test = active_mask;
        if (drop_cid >= 0) mask_test[drop_cid] = false;

        std::set<int> words_to_check;
        if (drop_cid >= 0) {
            for (int widx : cfg_word_indices[drop_cid]) words_to_check.insert(widx);
        }
        for (int widx = 0; widx < (int)word_cache.size(); ++widx) {
            if (word_cache[widx].d <= 8) {
                if (any_plus_term_fits(word_cache[widx].W, new_batch)) words_to_check.insert(widx);
            }
        }
        for (int d = 9; d <= d_max; ++d) {
            for (const auto& lk : d9_lists[d]) {
                int widx = word_idx_by_key.at(std::to_string(d) + ":" + link_str(lk));
                if (any_plus_term_fits(word_cache[widx].W, new_batch)) words_to_check.insert(widx);
            }
        }

        std::vector<int> check_vec(words_to_check.begin(), words_to_check.end());
        std::atomic<size_t> nxt{0};
        std::atomic<bool> ok{true};
        auto wfn = [&]() {
            while (ok.load(std::memory_order_relaxed)) {
                size_t ii = nxt.fetch_add(1);
                if (ii >= check_vec.size()) break;
                int widx = check_vec[ii];
                if (!check_word_dfs(word_cache[widx].W, scale_M, cand_parts,
                                    word_cache[widx].embs, mask_test, false, 0, nullptr)) {
                    ok.store(false, std::memory_order_relaxed);
                    break;
                }
            }
        };
        if (check_vec.size() < 24) {
            wfn();
        } else {
            std::vector<std::thread> ths;
            for (int t = 0; t < n_threads; ++t) ths.emplace_back(wfn);
            for (auto& th : ths) th.join();
        }
        return ok.load();
    };

    // Helper: check whether adding `delta_b` on top of `base_b` keeps Karp tail <= 18
    // AND produces 0 receiver violations under `mask_without` (skipping uncovered sender words in `skip_words`)!
    auto check_receiver_safe = [&](const std::vector<Part>& base_b,
                                   const std::vector<Part>& delta_b,
                                   const std::vector<bool>& mask_without,
                                   const std::set<int>& skip_words,
                                   int must_clear_widx,
                                   std::vector<Part>& out_cand_parts) -> bool {
        out_cand_parts = parts;
        out_cand_parts.insert(out_cand_parts.end(), base_b.begin(), base_b.end());
        out_cand_parts.insert(out_cand_parts.end(), delta_b.begin(), delta_b.end());

        // 1. Fast check on must_clear_widx first (~0.05 ms)
        if (must_clear_widx >= 0) {
            if (!check_word_dfs(word_cache[must_clear_widx].W, scale_M, out_cand_parts,
                                word_cache[must_clear_widx].embs, mask_without, false, 0, nullptr)) {
                return false;
            }
        }

        // 2. Fast check across all already-cached receiver words (both d <= 8 and cached d >= 9), early-aborting!
        int cur_cache_sz = (int)word_cache.size();
        for (int rw = 0; rw < cur_cache_sz; ++rw) {
            if (skip_words.count(rw)) continue;
            if (any_plus_term_fits(word_cache[rw].W, delta_b)) {
                if (!check_word_dfs(word_cache[rw].W, scale_M, out_cand_parts,
                                    word_cache[rw].embs, mask_without, false, 0, nullptr)) {
                    return false;
                }
            }
        }

        // 3. Only if ALL cached receiver words passed AND (base_b U delta_b) pushes positive weight to a 9+ target,
        //    recompute Karp potential & check any newly unlocked d >= 9 c+-positive words!
        bool pushes_to_9 = false;
        for (const auto& p : base_b) {
            if (p.weight > 0 && p.subs[2].sp.lo <= 9 && 9 <= p.subs[2].sp.hi) { pushes_to_9 = true; break; }
        }
        if (!pushes_to_9) {
            for (const auto& p : delta_b) {
                if (p.weight > 0 && p.subs[2].sp.lo <= 9 && 9 <= p.subs[2].sp.hi) { pushes_to_9 = true; break; }
            }
        }
        if (!pushes_to_9) return true;

        KarpResult tmp_kr = solve_karp_potential(scale_M, out_cand_parts);
        if (tmp_kr.tail_d0 > 18) return false;

        int d_max = std::max(17, tmp_kr.tail_d0);
        std::vector<std::pair<int, std::vector<int>>> new_d9;
        for (int d = 9; d <= d_max; ++d) {
            auto d9_lks = gen_cplus_words_karp(d, scale_M, tmp_kr);
            for (const auto& lk : d9_lks) {
                std::string key = std::to_string(d) + ":" + link_str(lk);
                if (!word_idx_by_key.count(key)) new_d9.push_back({d, lk});
            }
        }
        if (!new_d9.empty()) {
            int old_sz = (int)word_cache.size();
            ensure_words_cached(new_d9);
            for (int rw = old_sz; rw < (int)word_cache.size(); ++rw) {
                if (skip_words.count(rw)) continue;
                if (!check_word_dfs(word_cache[rw].W, scale_M, out_cand_parts,
                                    word_cache[rw].embs, mask_without, false, 0, nullptr)) {
                    return false;
                }
            }
        }
        return true;
    };

    for (int pass = 1; pass <= max_passes; ++pass) {
        std::cout << "\n=== SYNTHESIS PASS " << pass << " (starting active_cfgs = " << active_count
                  << ", parts = " << parts.size() << ") ===" << std::endl;

        struct CfgCand {
            int cid;
            int n_leaves;
            int n_words;
        };
        // Parallel forced-leaf count scan over snapshot of active_mask
        const std::vector<bool> snap_mask = active_mask;
        std::vector<int> scan_leaves(633, -1), scan_words(633, 0);
        {
            std::atomic<int> next_cid{0};
            auto scan_worker = [&]() {
                while (true) {
                    int cid = next_cid.fetch_add(1);
                    if (cid >= 633) break;
                    if (!snap_mask[cid]) continue;
                    std::vector<bool> mask_wo = snap_mask;
                    mask_wo[cid] = false;
                    std::vector<ForcedLeaf> leaves;
                    int n_w = 0;
                    for (int widx : cfg_word_indices[cid]) {
                        size_t bef = leaves.size();
                        check_word_dfs(word_cache[widx].W, scale_M, parts,
                                       word_cache[widx].embs, mask_wo, true, max_leaf_cap, &leaves);
                        if (leaves.size() > bef) n_w++;
                        if ((int)leaves.size() > max_leaf_cap) break;
                    }
                    scan_leaves[cid] = (int)leaves.size();
                    scan_words[cid] = n_w;
                }
            };
            std::vector<std::thread> ths;
            for (int t = 0; t < n_threads; ++t) ths.emplace_back(scan_worker);
            for (auto& th : ths) th.join();
        }

        std::vector<CfgCand> order_cids;
        int deleted_in_pass = 0;
        for (int cid = 0; cid < 633; ++cid) {
            if (!active_mask[cid] || scan_leaves[cid] < 0) continue;
            if (scan_leaves[cid] == 0) {
                // Sequential verification before free deletion so mutually-redundant pairs never both drop!
                std::vector<bool> mask_wo = active_mask;
                mask_wo[cid] = false;
                bool still_zero = true;
                for (int widx : cfg_word_indices[cid]) {
                    if (!check_word_dfs(word_cache[widx].W, scale_M, parts,
                                        word_cache[widx].embs, mask_wo, false, 0, nullptr)) {
                        still_zero = false;
                        break;
                    }
                }
                if (still_zero) {
                    active_mask[cid] = false;
                    active_count--;
                    deleted_in_pass++;
                    std::cout << "  [FREE DELETE] id=" << cid << " " << rsst_cfgs[cid].name
                              << " (0 live forced leaves!) -> active=" << active_count << std::endl;
                    continue;
                }
            }
            if (scan_leaves[cid] <= max_leaf_cap) {
                order_cids.push_back({cid, scan_leaves[cid], scan_words[cid]});
            }
        }

        std::sort(order_cids.begin(), order_cids.end(), [](const CfgCand& a, const CfgCand& b) {
            return std::tie(a.n_leaves, a.n_words, a.cid) < std::tie(b.n_leaves, b.n_words, b.cid);
        });
        std::cout << "  Found " << order_cids.size() << " active configs with <= " << max_leaf_cap
                  << " live forced leaves." << std::endl;

        for (const auto& cc : order_cids) {
            int cid = cc.cid;
            if (!active_mask[cid]) continue;

            std::vector<bool> mask_without = active_mask;
            mask_without[cid] = false;
            std::vector<ForcedLeaf> leaves;
            std::map<int, std::vector<ForcedLeaf>> by_widx;
            bool over_cap = false;
            for (int widx : cfg_word_indices[cid]) {
                std::vector<ForcedLeaf> wleaves;
                check_word_dfs(word_cache[widx].W, scale_M, parts,
                               word_cache[widx].embs, mask_without, true, max_leaf_cap, &wleaves);
                if (!wleaves.empty()) {
                    for (const auto& fl : wleaves) leaves.push_back(fl);
                    by_widx[widx] = std::move(wleaves);
                }
                if ((int)leaves.size() > max_leaf_cap) { over_cap = true; break; }
            }
            if (over_cap) continue;
            if (leaves.empty()) {
                active_mask[cid] = false;
                active_count--;
                deleted_in_pass++;
                std::cout << "  [FREE DELETE] id=" << cid << " " << rsst_cfgs[cid].name
                          << " -> active=" << active_count << std::endl;
                continue;
            }

            std::set<int> all_sender_words;
            for (auto& kv : by_widx) all_sender_words.insert(kv.first);

            std::vector<Part> combined_batch;
            bool all_words_covered = true;

            for (auto& [widx, wleaves] : by_widx) {
                const Window& W = word_cache[widx].W;
                std::set<int> skip_other = all_sender_words;
                skip_other.erase(widx);

                // Attempt 1: Single hull batch covering ALL wleaves on W at once!
                bool word_ok = false;
                auto hull_cands = generate_candidates_for_group(W, wleaves, uid_counter);
                for (auto& cand_b : hull_cands) {
                    std::vector<Part> cand_parts;
                    if (check_receiver_safe(combined_batch, cand_b, mask_without, skip_other, widx, cand_parts)) {
                        combined_batch.insert(combined_batch.end(), cand_b.begin(), cand_b.end());
                        word_ok = true;
                        break;
                    }
                }

                // Attempt 1.5: Balanced 2-way split along widest variable when single hull collided on receivers!
                if (!word_ok && wleaves.size() >= 2 && wleaves.size() <= 300) {
                    // Find variable vc whose midpoint splits wleaves into two non-empty halves most balancedly
                    int best_vc = -1, best_thr = -1;
                    size_t best_bal = wleaves.size();
                    std::set<int> all_vcs;
                    for (const auto& fl : wleaves) for (const auto& kv : fl.vcls) all_vcs.insert(kv.first);
                    for (int vc : all_vcs) {
                        for (int thr = 5; thr <= 8; ++thr) {
                            size_t cnt_lo = 0;
                            for (const auto& fl : wleaves) {
                                auto it = fl.vcls.find(vc);
                                int hi_v = (it == fl.vcls.end()) ? 9 : it->second.back();
                                if (hi_v <= thr) cnt_lo++;
                            }
                            if (cnt_lo > 0 && cnt_lo < wleaves.size()) {
                                size_t imb = (cnt_lo > wleaves.size() - cnt_lo)
                                           ? (cnt_lo - (wleaves.size() - cnt_lo))
                                           : ((wleaves.size() - cnt_lo) - cnt_lo);
                                if (imb < best_bal) {
                                    best_bal = imb;
                                    best_vc = vc;
                                    best_thr = thr;
                                }
                            }
                        }
                    }
                    if (best_vc != -1) {
                        std::vector<ForcedLeaf> grpA, grpB;
                        for (const auto& fl : wleaves) {
                            auto it = fl.vcls.find(best_vc);
                            int hi_v = (it == fl.vcls.end()) ? 9 : it->second.back();
                            if (hi_v <= best_thr) grpA.push_back(fl);
                            else grpB.push_back(fl);
                        }
                        auto candsA = generate_candidates_for_group(W, grpA, uid_counter);
                        std::vector<Part> chosenA;
                        bool okA = false;
                        for (auto& ca : candsA) {
                            std::vector<Part> cp;
                            if (check_receiver_safe(combined_batch, ca, mask_without, all_sender_words, -1, cp)) {
                                chosenA = std::move(ca);
                                okA = true;
                                break;
                            }
                        }
                        if (okA) {
                            std::vector<Part> baseAB = combined_batch;
                            baseAB.insert(baseAB.end(), chosenA.begin(), chosenA.end());
                            auto candsB = generate_candidates_for_group(W, grpB, uid_counter);
                            for (auto& cb : candsB) {
                                std::vector<Part> cp;
                                if (check_receiver_safe(baseAB, cb, mask_without, skip_other, widx, cp)) {
                                    baseAB.insert(baseAB.end(), cb.begin(), cb.end());
                                    combined_batch = std::move(baseAB);
                                    word_ok = true;
                                    break;
                                }
                            }
                        }
                    }
                }

                // Attempt 2: Greedy cluster / leaf-by-leaf cover (up to 16 batches when wleaves.size() <= 100)!
                if (!word_ok && wleaves.size() > 1 && wleaves.size() <= 100) {
                    std::vector<Part> sub_batch = combined_batch;
                    std::vector<ForcedLeaf> rem = wleaves;
                    bool sub_ok = true;
                    int guard_steps = 0;
                    while (!rem.empty() && ++guard_steps <= 16) {
                        // Try a tight cluster around rem[0] (at most 1 differing variable range) first, then {rem[0]}!
                        std::vector<std::vector<ForcedLeaf>> seed_groups;
                        if (rem.size() > 1) {
                            std::vector<ForcedLeaf> near_grp;
                            for (const auto& fl : rem) {
                                int diff = 0;
                                for (const auto& [vc, vec0] : rem[0].vcls) {
                                    auto it = fl.vcls.find(vc);
                                    if (it == fl.vcls.end() || it->second != vec0) {
                                        if (++diff > 1) break;
                                    }
                                }
                                if (diff <= 1) near_grp.push_back(fl);
                            }
                            if (near_grp.size() > 1) seed_groups.push_back(std::move(near_grp));
                        }
                        seed_groups.push_back({rem[0]});

                        bool step_found = false;
                        for (const auto& sgrp : seed_groups) {
                            auto single_cands = generate_candidates_for_group(W, sgrp, uid_counter);
                            for (auto& sc : single_cands) {
                                std::vector<Part> cand_parts;
                                if (check_receiver_safe(sub_batch, sc, mask_without, all_sender_words, -1, cand_parts)) {
                                    sub_batch.insert(sub_batch.end(), sc.begin(), sc.end());
                                    rem.clear();
                                    check_word_dfs(word_cache[widx].W, scale_M, cand_parts,
                                                   word_cache[widx].embs, mask_without, true, 120, &rem);
                                    step_found = true;
                                    break;
                                }
                            }
                            if (step_found) break;
                        }
                        if (!step_found) { sub_ok = false; break; }
                    }
                    if (sub_ok && rem.empty()) {
                        // Also check widx itself is not violated by self-plus terms!
                        std::vector<Part> cp = parts;
                        cp.insert(cp.end(), sub_batch.begin(), sub_batch.end());
                        if (check_word_dfs(word_cache[widx].W, scale_M, cp,
                                           word_cache[widx].embs, mask_without, false, 0, nullptr)) {
                            combined_batch = std::move(sub_batch);
                            word_ok = true;
                        }
                    }
                }

                if (!word_ok) { all_words_covered = false; break; }
            }

            if (!all_words_covered) continue;

            // Final airtight joint check of combined_batch + dropping cid across ALL affected + cid words!
            KarpResult next_kr;
            if (verify_batch_and_drop(cid, combined_batch, next_kr)) {
                parts.insert(parts.end(), combined_batch.begin(), combined_batch.end());
                kr_cur = next_kr;
                active_mask[cid] = false;
                active_count--;
                deleted_in_pass++;
                std::cout << "  [DELETED] id=" << std::setw(3) << cid << " " << std::setw(16) << rsst_cfgs[cid].name
                          << " (" << std::setw(7) << rsst_cfgs[cid].kind << " r=" << std::setw(2) << rsst_cfgs[cid].ring
                          << ") | leaves=" << std::setw(3) << leaves.size() << " words=" << std::setw(2) << by_widx.size()
                          << " +parts=" << std::setw(2) << combined_batch.size()
                          << " -> ACTIVE=" << active_count << " (tot_parts=" << parts.size()
                          << ", lambda*=" << kr_cur.P_num << "/" << kr_cur.Q_den << " d0=" << kr_cur.tail_d0 << ")" << std::endl;
                if (deleted_in_pass % 20 == 0) write_checkpoint();
            }
        }
        write_checkpoint();
        std::cout << "=== PASS " << pass << " SUMMARY: deleted " << deleted_in_pass
                  << " configs -> ACTIVE = " << active_count << " ===" << std::endl;
        if (deleted_in_pass == 0) break;
    }

    write_checkpoint();
    double tot_s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0_all).count();
    std::cout << "\n[SYNTHESIS COMPLETE] Surviving RSST configs = " << active_count
              << " / 633 (eliminated " << (633 - active_count) << " configs!), total_parts = "
              << parts.size() << ", elapsed = " << std::fixed << std::setprecision(2) << tot_s << "s." << std::endl;
    return 0;
}
