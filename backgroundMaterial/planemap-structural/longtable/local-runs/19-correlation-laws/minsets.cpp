// [exploratory] Item 19: enumerate minimal subsets S of {0..nf-1} with  sum_{i in S} F_i >= U  for every constraint (U, F_0..F_{nf-1}).
// stdin: nf ncons kmax, then ncons lines "U F_0 ... F_{nf-1}". stdout: one line per minimal valid S (bitmask), then "ALL <0/1>" (is S = everything valid).
#include <cstdio>
#include <vector>
#include <algorithm>
#include <cstdint>
int nf, nc, kmax; std::vector<int> U; std::vector<int> F; std::vector<uint32_t> found;
static bool ok(uint32_t S, int *order) {
    int idx[32], k = 0; for (int i = 0; i < nf; i++) if (S >> i & 1) idx[k++] = i;
    for (int c = 0; c < nc; c++) { int s = 0; const int *f = &F[(size_t)order[c] * nf]; for (int j = 0; j < k; j++) s += f[idx[j]]; if (s < U[order[c]]) {
        // move-to-front heuristic: swap with the front region
        if (c > 8) std::swap(order[c], order[c / 2]); return false; } }
    return true;
}
int main() {
    if (scanf("%d %d %d", &nf, &nc, &kmax) != 3) return 2;
    U.resize(nc); F.resize((size_t)nc * nf);
    for (int c = 0; c < nc; c++) { scanf("%d", &U[c]); for (int i = 0; i < nf; i++) scanf("%d", &F[(size_t)c * nf + i]); }
    std::vector<int> order(nc); for (int c = 0; c < nc; c++) order[c] = c;
    std::sort(order.begin(), order.end(), [&](int a, int b) { long sa = -U[a], sb = -U[b]; for (int i = 0; i < nf; i++) { sa += F[(size_t)a * nf + i]; sb += F[(size_t)b * nf + i]; } return sa < sb; });
    for (int k = 1; k <= kmax && k <= nf; k++) {
        uint32_t S = (1u << k) - 1;
        while (S < (1u << nf)) {
            bool sup = false; for (uint32_t m : found) if ((m & S) == m) { sup = true; break; }
            if (!sup && ok(S, order.data())) { found.push_back(S); printf("%u\n", S); fflush(stdout); }
            uint32_t c = S & -S, r = S + c; S = (((r ^ S) >> 2) / c) | r;
        }
    }
    printf("ALL %d\n", ok((1u << nf) - 1, order.data()) ? 1 : 0);
}
