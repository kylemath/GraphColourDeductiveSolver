#!/usr/bin/env python3
"""[exploratory] NightP1: build picyc.p1 = ../27-studio-positive-config/picyc.cpp + a --p1 block (copied to ./picyc_p1.cpp; the original is untouched).
--p1 (implies --sigc, so every link pattern): every degree-5 hole with a positive pi-cycle. Output "p1": {
  "grp": {cycle: group root} for every cycle in a sigma-group (sigma = {alpha,mu}-swap at m from every DD-step endpoint) that contains a positive cycle,
  "cyc": {cycle: [Lambda = 5w, L, all-DL?, excursions [[u, f], ...] in pi order starting at an unfilled state after a filled one (all-DL: [[L, 0]])]} for the same cycles,
  "links": {Z: [[i, T, R-type, sigma-image kind (0 filled, 1 unfilled non-DL, 2 DL), l1, l2, f (lockless image: filled states after it, else -1), excursion index of the image in T], ...]}
           for every positive Z, over its DD-step endpoints (position i on Z),
  "edges": [[a, b], ...] all sigma-links between distinct cycles of those groups (from every DD-step endpoint),
  "tedges": {Z: [[T, Lambda(T), #lock-breaking swaps, T in a positive cycle's sigma-group?], ...]} transport-T edges: link-free swaps from DL states of Z to nonpositive T != Z }.
Exits in the Job S sense are the links with R-type 3, kind 1, l1 = l2 = 0, T != Z."""
import os, subprocess
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, '..', '27-studio-positive-config', 'picyc.cpp')).read()
block = r'''
        if (P1 && !pos.empty()) {
            std::vector<int> up(cycles.size()); for (size_t i = 0; i < up.size(); i++) up[i] = i;
            std::function<int(int)> fr = [&](int x) { while (up[x] != x) { up[x] = up[up[x]]; x = up[x]; } return x; };
            auto isDDend = [&](long long k) { return kind[k] == 2 && (kind[pi[k]] == 2 || kind[pinv[k]] == 2); };
            for (long long k = 0; k < S; k++) { if (!isDDend(k)) continue; int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd);
                int a = fr(cyc[k]), b = fr(cyc[sg]); if (a != b) up[a] = b; }
            std::set<int> G; for (int ci : pos) G.insert(fr(ci));
            std::vector<int> excidx(S, -1);
            std::string pp = ", \"p1\": {\"grp\": {"; bool f1 = true; std::string cs = "}, \"cyc\": {"; bool f2 = true;
            for (size_t ci = 0; ci < cycles.size(); ci++) { if (!G.count(fr(ci))) continue; char b[96];
                snprintf(b, sizeof b, "%s\"%zu\": %d", f1 ? "" : ", ", ci, fr(ci)); pp += b; f1 = false;
                const auto &z = cycles[ci]; size_t Lz = z.size(); long long st = -1; bool alldl = true; for (int32_t x : z) if (kind[x] != 2) alldl = false;
                for (size_t i = 0; i < Lz; i++) if (kind[z[i]] != 0 && kind[z[(i + Lz - 1) % Lz]] == 0) { st = i; break; }
                snprintf(b, sizeof b, "%s\"%zu\": [%lld, %zu, %d, [", f2 ? "" : ", ", ci, 5 * wind[ci], Lz, alldl ? 1 : 0); cs += b; f2 = false;
                if (st < 0) { snprintf(b, sizeof b, "[%zu, 0]", kind[z[0]] != 0 ? Lz : (size_t)0); cs += b; for (int32_t x : z) excidx[x] = 0; }
                else { size_t i = st, done = 0; int e = 0; bool fe = true;
                    while (done < Lz) { long long u = 0, f = 0;
                        while (done < Lz && kind[z[i]] != 0) { excidx[z[i]] = e; u++; i = (i + 1) % Lz; done++; }
                        while (done < Lz && kind[z[i]] == 0) { excidx[z[i]] = e; f++; i = (i + 1) % Lz; done++; }
                        snprintf(b, sizeof b, "%s[%lld, %lld]", fe ? "" : ", ", u, f); cs += b; fe = false; e++; } }
                cs += "]]"; }
            pp += cs; pp += "}, \"links\": {"; bool f3 = true;
            for (int ci : pos) { char b[160]; snprintf(b, sizeof b, "%s\"%d\": [", f3 ? "" : ", ", ci); pp += b; f3 = false; bool f4 = true; const auto &z = cycles[ci];
                for (size_t i = 0; i < z.size(); i++) { long long x = z[i]; if (!isDDend(x)) continue; int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd);
                    long long f = -1; if (kd == 1 && !l1 && !l2) { long long y = pi[sg]; f = 0; while (kind[y] == 0) { f++; y = pi[y]; } }
                    snprintf(b, sizeof b, "%s[%zu, %d, %d, %d, %d, %d, %lld, %d]", f4 ? "" : ", ", i, cyc[sg], ty, kd, l1, l2, f, excidx[sg]); pp += b; f4 = false; }
                pp += "]"; }
            pp += "}, \"edges\": ["; std::set<std::pair<int,int>> E;
            for (long long k = 0; k < S; k++) { if (!isDDend(k) || !G.count(fr(cyc[k]))) continue; int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd);
                if (cyc[sg] != cyc[k]) E.insert({std::min(cyc[k], cyc[sg]), std::max(cyc[k], cyc[sg])}); }
            bool f5 = true; for (auto &e : E) { char b[48]; snprintf(b, sizeof b, "%s[%d, %d]", f5 ? "" : ", ", e.first, e.second); pp += b; f5 = false; }
            pp += "], \"tedges\": {"; bool f6 = true;
            for (int ci : pos) { char b[64]; snprintf(b, sizeof b, "%s\"%d\": [", f6 ? "" : ", ", ci); pp += b; f6 = false; bool f7 = true;
                for (auto &kv : exits[ci]) { const Exit &e = kv.second; if (!e.dl || wind[kv.first] > 0) continue;
                    snprintf(b, sizeof b, "%s[%d, %lld, %lld, %d]", f7 ? "" : ", ", kv.first, 5 * wind[kv.first], (long long)e.lb, G.count(fr(kv.first)) ? 1 : 0); pp += b; f7 = false; }
                pp += "]"; }
            pp += "}}"; jobe += pp; }
'''
anchor = '        if (JOBG) {   // Job G (NightC1Gamma'
assert src.count(anchor) == 1
src = src.replace(anchor, block + anchor)
src = src.replace('static bool FULL = false,', 'static bool P1 = false; static bool FULL = false,', 1)
src = src.replace('else if (a == "--jobk")', 'else if (a == "--p1") { P1 = true; SIGC = true; } else if (a == "--jobk")', 1)
assert 'P1 = false' in src and '"--p1"' in src
open(os.path.join(here, 'picyc_p1.cpp'), 'w').write(src)
subprocess.check_call(['clang++', '-O2', '-std=c++17', '-o', os.path.join(here, 'picyc.p1'), os.path.join(here, 'picyc_p1.cpp')])
print('built picyc.p1')
