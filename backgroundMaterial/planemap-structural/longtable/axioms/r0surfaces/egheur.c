/* egheur.c (generated from genus.c helpers) -- HEURISTIC upper bounds on Euler genus
   by simulated annealing over twist vectors (canonical rotations, v fixed); usage: egheur ITERS RESTARTS CAP SEED < lines
   Output per line: best_eg best_nonorientable_eg best_orientable_genus(rotation-only annealing) twist-vector(hex, of the best non-orientable one; bit e = edge e twisted, rotations canonical = input incidence order, v = f0..f4).
   Original header of genus.c follows:
   genus.c -- exhaustive embedding genus with a prescribed rotation at one vertex (Long Table, r0surfaces).

   Input (stdin), one graph per line, TrackU line format:
       n m a_0 b_0 a_1 b_1 ... a_{m-1} b_{m-1} f_0 f_1 f_2 f_3 f_4
   (f_s = edge ids at the special vertex v, in rotation order).  Graph must be connected, loopless.

   Output per line:  og eg ng   [og_free eg_free ng_free with -free]
     og = min orientable genus with rotation at v equal to (f_0..f_4) (mirror included automatically)
     eg = min Euler genus over all cellular embeddings (orientable or not) with local rotation at v
          equal to (f_0..f_4) up to reversal
     ng = min Euler genus over NON-orientable embeddings with that local rotation (= non-orientable genus)
     *_free: same with the rotation at v unconstrained.
   Options: -o     orientable genus only (eg, ng printed as -1)
            -free  also compute the unconstrained values.
            -cap K stop the non-orientable search as soon as an embedding of Euler genus <= K is found
                   (then eg/ng are reported as "<=K" upper bounds, marked with a trailing '*').

   Method: generalized maps.  Flags (e, end j, side s), id 4e+2j+s.  alpha2 flips s; alpha0 crosses the edge,
   (e,j,s) -> (e,1-j,1-s) if untwisted, (e,1-j,s) if twisted; alpha1 pairs (c_i, side 1) with (c_{i+1}, side 0)
   for consecutive edge-ends in the rotation at a vertex.  Faces = orbits of <alpha0, alpha1>.
   Euler genus = 2 - V + E - F.  Orientable embeddings: all edges untwisted, rotations enumerated over all
   (d-1)! cyclic orders (v fixed).  General embeddings: by vertex switches every embedding is equivalent to
   one whose rotations are taken from a fixed set of representatives of cyclic orders up to reversal
   ((d-1)!/2 for d >= 3), with an arbitrary twist vector in {0,1}^E; the switch at v reverses v's rotation,
   so fixing v's rotation (up to reversal) is exactly "local rotation at v prescribed".
   Orientability of (rho, lambda): lambda is a coboundary (checked by BFS parity). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXV 64
#define MAXE 128
#define MAXD 8

static int orient_only;
static int n, m, ea[MAXE], eb[MAXE], fv[5], vsp;
static int deg[MAXV], inc[MAXV][MAXD];          /* edge-end codes 2e+j */
static int a0[4 * MAXE], a1[4 * MAXE], vis[4 * MAXE];

/* permutations: list of cyclic orders for each vertex */
static int nord[MAXV];
static int ord[MAXV][800][MAXD];

static void gen_orders(int u, int upto_rev, int fixed) {
    int d = deg[u];
    nord[u] = 0;
    if (fixed) {   /* rotation f_0..f_4 at v */
        for (int s = 0; s < d; s++) {
            int e = fv[s]; int j = (ea[e] == u) ? 0 : 1;
            ord[u][0][s] = 2 * e + j;
        }
        nord[u] = 1; return;
    }
    if (d <= 2) {
        for (int i = 0; i < d; i++) ord[u][0][i] = inc[u][i];
        nord[u] = 1; return;
    }
    /* permutations of inc[u][1..d-1] with inc[u][0] first */
    int p[MAXD]; for (int i = 0; i < d - 1; i++) p[i] = i + 1;
    /* Heap-free: iterate lexicographic permutations */
    int k = d - 1;
    while (1) {
        int keep = 1;
        if (upto_rev && p[0] > p[k - 1]) keep = 0;    /* reversal rep: second elt < last elt */
        if (keep) {
            ord[u][nord[u]][0] = inc[u][0];
            for (int i = 0; i < k; i++) ord[u][nord[u]][i + 1] = inc[u][p[i]];
            nord[u]++;
        }
        /* next permutation */
        int i = k - 2; while (i >= 0 && p[i] > p[i + 1]) i--;
        if (i < 0) break;
        int j = k - 1; while (p[j] < p[i]) j--;
        int t = p[i]; p[i] = p[j]; p[j] = t;
        for (int a = i + 1, b = k - 1; a < b; a++, b--) { t = p[a]; p[a] = p[b]; p[b] = t; }
    }
}

static void set_rot(int u, int *r) {
    int d = deg[u];
    for (int i = 0; i < d; i++) {
        int c = r[i], cn = r[(i + 1) % d];
        int x = 2 * c + 1, y = 2 * cn + 0;   /* flag id = 4e+2j+s = 2*(2e+j)+s */
        a1[x] = y; a1[y] = x;
    }
}

static int count_faces(void) {
    int F = 0, N = 4 * m;
    memset(vis, 0, sizeof(int) * N);
    for (int x = 0; x < N; x++) {
        if (vis[x]) continue;
        int y = x;
        do { vis[y] = 1; int z = a0[y]; vis[z] = 1; y = a1[z]; } while (y != x);
        F++;
    }
    return F;
}

static void set_twist(unsigned long long tw) {
    for (int e = 0; e < m; e++) {
        int t = (tw >> e) & 1;
        for (int s = 0; s < 2; s++) {
            int x = 4 * e + 0 + s, y = 4 * e + 2 + (t ? s : 1 - s);
            a0[x] = y; a0[y] = x;
        }
    }
}

static int is_orientable(unsigned long long tw) {
    int col[MAXV], q[MAXV], h = 0, tl = 0;
    for (int i = 0; i < n; i++) col[i] = -1;
    col[0] = 0; q[tl++] = 0;
    while (h < tl) {
        int u = q[h++];
        for (int i = 0; i < deg[u]; i++) {
            int c = inc[u][i], e = c >> 1, w = (c & 1) ? ea[e] : eb[e];
            int want = col[u] ^ (int)((tw >> e) & 1);
            if (col[w] < 0) { col[w] = want; q[tl++] = w; }
            else if (col[w] != want) return 0;
        }
    }
    return 1;
}


static unsigned long long rng = 88172645463325252ULL;
static unsigned long long xr(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static double ur(void) { return (xr() >> 11) * (1.0 / 9007199254740992.0); }
#include <math.h>
int main(int argc, char **argv) {
    long iters = atol(argv[1]); int restarts = atoi(argv[2]); int cap = atoi(argv[3]); rng ^= (unsigned long long)atol(argv[4]) * 2654435761ULL;
    char buf[1 << 16];
    while (fgets(buf, sizeof buf, stdin)) {
        char *p = buf; int off;
        if (sscanf(p, "%d %d%n", &n, &m, &off) != 2) continue; p += off;
        memset(deg, 0, sizeof deg);
        for (int e = 0; e < m; e++) {
            sscanf(p, "%d %d%n", &ea[e], &eb[e], &off); p += off;
            inc[ea[e]][deg[ea[e]]++] = 2 * e + 0; inc[eb[e]][deg[eb[e]]++] = 2 * e + 1;
        }
        sscanf(p, "%d %d %d %d %d", &fv[0], &fv[1], &fv[2], &fv[3], &fv[4]);
        { int a = ea[fv[0]], b = eb[fv[0]]; vsp = (a == ea[fv[1]] || a == eb[fv[1]]) ? a : b; }
        int V = n, E = m, bestAll = -1, bestNon = -1, bestOr = -1; unsigned long long bestTw = 0;
        /* nonorientable / general: anneal over twists, canonical rotations */
        for (int u = 0; u < n; u++) { gen_orders(u, 1, u == vsp); set_rot(u, ord[u][0]); }
        int target = 2 - V + E - cap;
        for (int r = 0; r < restarts && bestNon < target; r++) {
            unsigned long long tw = 0; for (int e = 0; e < E; e++) if (xr() & 1) tw |= 1ULL << e;
            set_twist(tw); int F = count_faces();
            for (long it = 0; it < iters; it++) {
                double T = 2.0 * (1.0 - (double)it / iters) + 0.05;
                int e = xr() % E; unsigned long long t2 = tw ^ (1ULL << e);
                set_twist(t2); int F2 = count_faces();
                if (F2 >= F || ur() < exp((F2 - F) / T)) { tw = t2; F = F2; }
                if (F > bestAll) bestAll = F;
                if (F > bestNon && !is_orientable(tw)) { bestNon = F; bestTw = tw; if (bestNon >= target) break; }
            }
        }
        /* orientable: anneal over rotations (cubic vertices: 2 orders), no twists */
        for (int u = 0; u < n; u++) { gen_orders(u, 0, u == vsp); set_rot(u, ord[u][0]); }
        set_twist(0ULL);
        int idx[MAXV];
        for (int r = 0; r < restarts; r++) {
            for (int u = 0; u < n; u++) { idx[u] = xr() % nord[u]; set_rot(u, ord[u][idx[u]]); }
            int F = count_faces();
            for (long it = 0; it < iters; it++) {
                double T = 2.0 * (1.0 - (double)it / iters) + 0.05;
                int u = xr() % n; if (nord[u] < 2) continue;
                int old = idx[u], nw = xr() % nord[u]; if (nw == old) continue;
                set_rot(u, ord[u][nw]); int F2 = count_faces();
                if (F2 >= F || ur() < exp((F2 - F) / T)) { idx[u] = nw; F = F2; }
                else set_rot(u, ord[u][old]);
                if (F > bestOr) bestOr = F;
            }
        }
        printf("%d %d %d %llx\n", 2 - V + E - bestAll, bestNon < 0 ? 999 : 2 - V + E - bestNon, (2 - V + E - bestOr) / 2, bestTw);
        fflush(stdout);
    }
    return 0;
}
