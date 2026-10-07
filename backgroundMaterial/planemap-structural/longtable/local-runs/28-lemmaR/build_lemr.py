#!/usr/bin/env python3
"""[exploratory] NightLemmaR: build picyc.lemr = ../27-studio-positive-config/picyc.cpp + a --lemr block (copied to ./picyc_lemr.cpp; the original is untouched).
--lemr: every degree-5 hole with a positive pi-cycle (all link patterns). For every cycle T hit by a sigma-image of a DL state of a positive cycle
whose image is lockless (u = 1), print T's excursions in pi order as [u, f, hits], hits = list of codes 8*type + 4*ddend + 2*same + 1
(type = R-type of the source frame 0..3 (3 = R3), ddend = source is a DD-step endpoint, same = source cycle == T).
A Gamma or all-filled cycle prints its length as u (resp. f) with no excursion structure."""
import os, re, subprocess
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, '..', '27-studio-positive-config', 'picyc.cpp')).read()
block = r'''
        if (LEMR) {
            std::map<int, std::map<long long, std::vector<int>>> rh;   // target cycle -> hit unfilled state -> codes
            for (int ci : pos) for (int32_t x : cycles[ci]) { if (kind[x] != 2) continue; int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd);
                if (!(kd == 1 && !l1 && !l2)) continue; int dd = (kind[pi[x]] == 2 || kind[pinv[x]] == 2) ? 1 : 0;
                rh[cyc[sg]][sg].push_back(8 * ty + 4 * dd + 2 * (cyc[sg] == ci ? 1 : 0) + 1); }
            std::string rr = ", \"lemr\": ["; bool fr = true;
            for (auto &kv : rh) { int T = kv.first; const auto &z = cycles[T]; size_t Lz = z.size(); long long st = -1;
                for (size_t i = 0; i < Lz; i++) if (kind[z[i]] != 0 && kind[z[(i + Lz - 1) % Lz]] == 0) { st = i; break; }
                char b[128]; snprintf(b, sizeof b, "%s{\"w\": %lld, \"L\": %zu, \"exc\": [", fr ? "" : ", ", wind[T], Lz); rr += b; fr = false;
                if (st >= 0) { size_t i = st, done = 0; bool fe = true;
                    while (done < Lz) { long long u = 0, f = 0, h = -1; std::vector<int> codes;
                        while (done < Lz && kind[z[i]] != 0) { if (kv.second.count(z[i])) codes = kv.second.at(z[i]); u++; i = (i + 1) % Lz; done++; }
                        while (done < Lz && kind[z[i]] == 0) { f++; i = (i + 1) % Lz; done++; }
                        rr += fe ? "[" : ", ["; fe = false; snprintf(b, sizeof b, "%lld, %lld, [", u, f); rr += b;
                        for (size_t q = 0; q < codes.size(); q++) { snprintf(b, sizeof b, "%s%d", q ? ", " : "", codes[q]); rr += b; } rr += "]]"; } }
                rr += "]}"; }
            rr += "]"; jobe += rr; }
'''
anchor = '        if (JOBG) {   // Job G (NightC1Gamma'
assert src.count(anchor) == 1
src = src.replace(anchor, block + anchor)
src = src.replace('JOBS = false;', 'JOBS = false, LEMR = false;', 1)
src = src.replace('else if (a == "--jobk")', 'else if (a == "--lemr") { LEMR = true; SIGC = true; } else if (a == "--jobk")', 1)
assert 'LEMR = false' in src and '"--lemr"' in src
open(os.path.join(here, 'picyc_lemr.cpp'), 'w').write(src)
subprocess.check_call(['clang++', '-O2', '-std=c++17', '-o', os.path.join(here, 'picyc.lemr'), os.path.join(here, 'picyc_lemr.cpp')])
print('built picyc.lemr')
