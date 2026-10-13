/* genus.c -- exhaustive embedding genus with a prescribed rotation at one vertex (Long Table, r0surfaces).

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
            -sepT / -sepP  count all torus / projective-plane embeddings with the rotation at v, and how many of
                   them make the Hamiltonian cycle H = edges 0..n-1 (normal form) SEPARATING (2 face classes)
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
static int a0[4 * MAXE], a1[4 * MAXE], vis[4 * MAXE], fid[4 * MAXE];
static int sep_mode = 0, nH = 0, list_mode = 0;  /* -sepP / -sepT: H = edges 0..nH-1 */

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
        do { vis[y] = 1; fid[y] = F; int z = a0[y]; vis[z] = 1; fid[z] = F; y = a1[z]; } while (y != x);
        F++;
    }
    return F;
}

static int uf[4 * MAXE];
static int ufind(int x) { while (uf[x] != x) { uf[x] = uf[uf[x]]; x = uf[x]; } return x; }
/* is the cycle H = edges 0..nH-1 separating in the current embedding (F faces, fid filled)? */
static int h_separating(int F) {
    for (int f = 0; f < F; f++) uf[f] = f;
    int cls = F;
    for (int e = nH; e < m; e++) {
        int a = ufind(fid[4 * e]), b = ufind(fid[4 * e + 1]);
        if (a != b) { uf[a] = b; cls--; }
    }
    if (cls != 2) return 0;
    for (int e = 0; e < nH; e++) if (ufind(fid[4 * e]) == ufind(fid[4 * e + 1])) return 0;
    return 1;
}

/* is the primal (dual of the embedded G, plus a vertex x in the pentagon at v) a simple triangulation? */
static int pairseen[4 * MAXE][4 * MAXE / 2];
static int primal_simple(int F) {
    static int stamp = 0; stamp++;
    for (int e = 0; e < m; e++) {
        int a = fid[4 * e], b = fid[4 * e + 1];
        if (a == b) return 0;
        if (a > b) { int t = a; a = b; b = t; }
        if (pairseen[a][b] == stamp) return 0;
        pairseen[a][b] = stamp;
    }
    int fs[5];
    for (int i = 0; i < 5; i++) {
        int c = ord[vsp][0][i];           /* edge-end code at v, rotation f0..f4 */
        fs[i] = fid[2 * c + 1];
        for (int j = 0; j < i; j++) if (fs[j] == fs[i]) return 0;
    }
    return 1;
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

/* returns og, eg, ng (ng = 999 if none found) */
static void solve(int vfixed, int cap, int *og, int *eg, int *ng, int *capped) {
    int V = n, E = m;
    /* orientable */
    for (int u = 0; u < n; u++) gen_orders(u, 0, vfixed && u == vsp);
    if (!vfixed && vsp >= 0) { /* free v: fix first edge, all (d-1)! (mirror handled by others) */ }
    int idx[MAXV]; memset(idx, 0, sizeof idx);
    int bestF = -1;
    set_twist(0ULL);
    for (int u = 0; u < n; u++) set_rot(u, ord[u][0]);
    /* choose a vertex whose orders we do NOT vary over mirror... simply enumerate all */
    while (1) {
        int F = count_faces(); if (F > bestF) bestF = F;
        int u = 0;
        while (u < n) {
            idx[u]++;
            if (idx[u] < nord[u]) { set_rot(u, ord[u][idx[u]]); break; }
            idx[u] = 0; set_rot(u, ord[u][0]); u++;
        }
        if (u == n) break;
    }
    *og = (2 - V + E - bestF) / 2;
    if (orient_only) { *eg = -1; *ng = -1; *capped = 0; return; }
    /* general */
    for (int u = 0; u < n; u++) gen_orders(u, 1, vfixed && u == vsp);
    memset(idx, 0, sizeof idx);
    for (int u = 0; u < n; u++) set_rot(u, ord[u][0]);
    int bestAll = -1, bestNon = -1; *capped = 0;
    int target = (cap >= 0) ? (2 - V + E - cap) : 1 << 30;   /* F >= target  <=> eg <= cap */
    while (1) {
        for (unsigned long long tw = 0; tw < (1ULL << E); tw++) {
            set_twist(tw);
            int F = count_faces();
            if (F > bestAll) bestAll = F;
            if (F > bestNon && !is_orientable(tw)) bestNon = F;
            if (bestNon >= target) { *capped = 1; goto done; }
        }
        int u = 0;
        while (u < n) {
            idx[u]++;
            if (idx[u] < nord[u]) { set_rot(u, ord[u][idx[u]]); break; }
            idx[u] = 0; set_rot(u, ord[u][0]); u++;
        }
        if (u == n) break;
    }
done:
    *eg = 2 - V + E - bestAll;
    *ng = bestNon < 0 ? 999 : 2 - V + E - bestNon;
}

/* -sepT: all orientable genus-1 embeddings (v fixed); -sepP: all Euler-genus-1 embeddings (v fixed, canonical
   rotations + twists).  Prints: #embeddings, #with H separating, #with simple primal triangulation, #both. */
static void sep_run(void) {
    int V = n, E = m, idx[MAXV]; long nemb = 0, nsep = 0, nsimp = 0, nsimpsep = 0;
    memset(idx, 0, sizeof idx);
    int target_eg = (sep_mode == 3) ? 0 : 2;
    if (sep_mode == 1 || sep_mode == 3) {           /* torus (or sphere with -sepS) */
        for (int u = 0; u < n; u++) { gen_orders(u, 0, u == vsp); set_rot(u, ord[u][0]); }
        set_twist(0ULL);
        while (1) {
            int F = count_faces();
            if (2 - V + E - F == target_eg) { int hs = h_separating(F), ps = primal_simple(F); nemb++; nsep += hs; nsimp += ps; nsimpsep += hs && ps;
                if (list_mode && nemb <= 400) { unsigned long long b = 0; for (int w = 0; w < n; w++) if (idx[w]) b |= 1ULL << w; printf("%llx ", b); } }
            int u = 0;
            while (u < n) { idx[u]++; if (idx[u] < nord[u]) { set_rot(u, ord[u][idx[u]]); break; } idx[u] = 0; set_rot(u, ord[u][0]); u++; }
            if (u == n) break;
        }
    } else {                       /* projective plane */
        for (int u = 0; u < n; u++) { gen_orders(u, 1, u == vsp); set_rot(u, ord[u][0]); }
        for (unsigned long long tw = 0; tw < (1ULL << E); tw++) {
            set_twist(tw); int F = count_faces();
            if ((sep_mode == 2 && 2 - V + E - F == 1) || (sep_mode == 4 && 2 - V + E - F == 2 && !is_orientable(tw))) { int hs = h_separating(F), ps = primal_simple(F); nemb++; nsep += hs; nsimp += ps; nsimpsep += hs && ps;
                if (list_mode && nemb <= 400) printf("%llx ", tw); }
        }
    }
    if (list_mode) printf("| ");
    printf("%ld %ld %ld %ld\n", nemb, nsep, nsimp, nsimpsep); fflush(stdout);
}

int main(int argc, char **argv) {
    int dofree = 0, cap = -1; orient_only = 0;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-free")) dofree = 1;
        else if (!strcmp(argv[i], "-cap")) cap = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-o")) orient_only = 1;
        else if (!strcmp(argv[i], "-sepT")) sep_mode = 1;
        else if (!strcmp(argv[i], "-sepP")) sep_mode = 2;
        else if (!strcmp(argv[i], "-sepS")) sep_mode = 3;   /* sphere embeddings (control) */
        else if (!strcmp(argv[i], "-sepK")) sep_mode = 4;   /* Klein-bottle embeddings */
        else if (!strcmp(argv[i], "-list")) list_mode = 1;   /* with -sepT/-sepP: print the first 400 embeddings
                   (torus: hex bitmask of cubic vertices using the reversed order; RP2: hex twist vector) */
    }
    char buf[1 << 16];
    while (fgets(buf, sizeof buf, stdin)) {
        char *p = buf; int off;
        if (sscanf(p, "%d %d%n", &n, &m, &off) != 2) continue; p += off;
        memset(deg, 0, sizeof deg);
        for (int e = 0; e < m; e++) {
            sscanf(p, "%d %d%n", &ea[e], &eb[e], &off); p += off;
            inc[ea[e]][deg[ea[e]]++] = 2 * e + 0;
            inc[eb[e]][deg[eb[e]]++] = 2 * e + 1;
        }
        vsp = -1;
        if (sscanf(p, "%d %d %d %d %d", &fv[0], &fv[1], &fv[2], &fv[3], &fv[4]) == 5) {
            int a = ea[fv[0]], b = eb[fv[0]];
            vsp = (a == ea[fv[1]] || a == eb[fv[1]]) ? a : b;
        }
        int og, eg, ng, capped;
        if (sep_mode) { nH = n; sep_run(); continue; }
        if (vsp >= 0) {
            solve(1, cap, &og, &eg, &ng, &capped);
            printf("%d %d%s %d%s", og, eg, capped ? "*" : "", ng, capped ? "*" : "");
        } else printf("- - -");
        if (dofree) {
            solve(0, cap, &og, &eg, &ng, &capped);
            printf(" %d %d%s %d%s", og, eg, capped ? "*" : "", ng, capped ? "*" : "");
        }
        printf("\n"); fflush(stdout);
    }
    return 0;
}
