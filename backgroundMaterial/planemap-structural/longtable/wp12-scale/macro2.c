/* WP12-scale fast checker for the two-swap macro rank test at one degree-five root.
 *
 * Model (identical to longtable/mass_core.py and longtable/wp11_cert.py):
 *   states   = proper 4-colourings of T - r modulo global colour renaming, enumerated in the
 *              first-occurrence canonical form over vertex order V = (labels != r, ascending);
 *              enumeration order equals the order of mass_core.deletion_colourings.
 *   p        = max(0, #colours on B - 3), B = N(r); target iff p = 0.
 *   move     = swap the two colours on one whole active bichromatic component (component of the
 *              subgraph induced on the vertices coloured a or b, all 6 pairs, interior allowed).
 *   macro    = 1 or 2 moves, components recomputed after move 1; only the endpoint must be lower.
 *   rank     = (p, sum_i w_i f_i) lexicographic, f = the 8 wp11 features
 *              (q, lin, L, Lall, links, shortLinks, repMass, hubToggles).
 *   GOOD(w)  = every p = 1 state has a 1- or 2-move endpoint of strictly lower rank.
 *
 * Exact pruning: an endpoint with p = 0 is lower than any p = 1 start, so a p = 1 state with a
 * target endpoint within two moves can never be stuck under any weight vector. Only the remaining
 * "hard" states get full endpoint feature evaluation. Features are invariant under global colour
 * renaming, so endpoints are evaluated on raw (uncanonicalised) colourings.
 *
 * Input (stdin, repeated for a batch of instances until EOF):  n r nw / n lines "deg v1 .. vdeg" (rotation) / nw lines of 8 integer weights.
 * Output (stdout): one JSON object per line, per instance. argv[1] = number of threads (default 1).
 * Limits: n - 1 <= 63 vertices in T - r (bitmask representation).
 */
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;
#define MAXW 512
#define MAXC 400

static int n, root, m, NW, NT = 1;
static int lab[64];          /* V order: index -> label */
static u64 adj[64];          /* adjacency in T - r over V indices */
static u64 Bm;               /* mask of B */
static int Bv[5];            /* B indices in rotation order of r */
static long long W[MAXW][8];

typedef struct { u64 c[4]; } Col;
typedef struct { u64 K; int a, b; } Comp;
static const int PA[6] = {0, 0, 0, 1, 1, 2}, PB[6] = {1, 2, 3, 2, 3, 3};

/* ---------------------------------------------------------------- enumeration */
static u64 *keys = NULL;  /* 2 words per state: bits 2i..2i+1 of the 128-bit key hold colour of V[i] */
static size_t nstates = 0, capstates = 0;
static u64 earlier[64];

static void push_state(const unsigned char *cur) {
    if (nstates == capstates) {
        capstates = capstates ? capstates * 2 : 1 << 16;
        keys = realloc(keys, capstates * 2 * sizeof(u64));
        if (!keys) { fprintf(stderr, "out of memory\n"); exit(2); }
    }
    u64 lo = 0, hi = 0;
    for (int i = 0; i < m; i++) {
        if (i < 32) lo |= (u64)cur[i] << (2 * i);
        else hi |= (u64)cur[i] << (2 * (i - 32));
    }
    keys[2 * nstates] = lo;
    keys[2 * nstates + 1] = hi;
    nstates++;
}

static void enumerate(void) {
    unsigned char cur[64];
    int top[65], a[64];
    u64 cls[4] = {0, 0, 0, 0};
    int i = 0;
    top[0] = -1;
    a[0] = -1;
    /* iterative DFS identical in order to mass_core.deletion_colourings */
    while (i >= 0) {
        if (i == m) { push_state(cur); i--; if (i >= 0) cls[cur[i]] &= ~(1ULL << i); continue; }
        int lim = top[i] + 1 < 3 ? top[i] + 1 : 3;
        int x = a[i] + 1;
        while (x <= lim && (cls[x] & earlier[i])) x++;
        if (x > lim) {
            a[i] = -1;
            i--;
            if (i >= 0) cls[cur[i]] &= ~(1ULL << i);
            continue;
        }
        a[i] = x;
        cur[i] = (unsigned char)x;
        cls[x] |= 1ULL << i;
        top[i + 1] = top[i] > x ? top[i] : x;
        a[i + 1] = -1;
        i++;
    }
}

static void decode(size_t s, Col *c, unsigned char *out) {
    memset(c, 0, sizeof *c);
    u64 lo = keys[2 * s], hi = keys[2 * s + 1];
    for (int i = 0; i < m; i++) {
        int x = i < 32 ? (int)((lo >> (2 * i)) & 3) : (int)((hi >> (2 * (i - 32))) & 3);
        c->c[x] |= 1ULL << i;
        if (out) out[i] = (unsigned char)x;
    }
}

/* ---------------------------------------------------------------- components and features */
static inline u64 flood(u64 seed, u64 S) {
    u64 comp = seed, fr = seed;
    while (fr) {
        u64 nb = 0;
        while (fr) { int v = __builtin_ctzll(fr); fr &= fr - 1; nb |= adj[v]; }
        nb &= S & ~comp;
        comp |= nb;
        fr = nb;
    }
    return comp;
}

static int components(const Col *c, Comp *out) {
    int k = 0;
    for (int pr = 0; pr < 6; pr++) {
        int a = PA[pr], b = PB[pr];
        u64 S = c->c[a] | c->c[b];
        while (S) {
            u64 K = flood(S & -S, S);
            S &= ~K;
            out[k].K = K; out[k].a = a; out[k].b = b; k++;
        }
    }
    return k;
}

static inline int pval(const Col *c) {
    int k = 0;
    for (int x = 0; x < 4; x++) k += (c->c[x] & Bm) != 0;
    return k > 3 ? k - 3 : 0;
}

static inline int colour_of(const Col *c, int v) {
    u64 bit = 1ULL << v;
    for (int x = 0; x < 4; x++) if (c->c[x] & bit) return x;
    return -1;
}

/* p and the 8 features, exactly as wp11_cert.features (targets: all zero except hubToggles). */
static int features(const Col *c, const Comp *cs, int nc, long long f[8]) {
    int p = pval(c);
    long long hub = 0;
    for (int i = 0; i < nc; i++)
        if (__builtin_popcountll(cs[i].K) == 2 && (cs[i].K & ~Bm)) hub++;
    memset(f, 0, 8 * sizeof(long long));
    f[7] = hub;
    if (p == 0) return 0;
    int cnt[4];
    for (int x = 0; x < 4; x++) cnt[x] = __builtin_popcountll(c->c[x] & Bm);
    int rho = -1;
    for (int x = 0; x < 4; x++) if (cnt[x] == 2) rho = x;
    for (int i = 0; i < nc; i++) {
        u64 K = cs[i].K, KB = K & Bm;
        if (!KB) continue;
        long long out = __builtin_popcountll(K & ~Bm);
        f[0] += out * out;
        f[1] += out;
        if (__builtin_popcountll(KB) >= 2) { f[4]++; if (!(K & ~Bm)) f[5]++; }
        if (cs[i].a == rho || cs[i].b == rho) f[6] += out * out;
    }
    for (int j = 0; j < 5; j++) {
        int v = Bv[j], cv = colour_of(c, v);
        int single = cnt[cv] == 1;
        for (int x = 0; x < 4; x++) {
            if (x == cv) continue;
            u64 K = flood(1ULL << v, c->c[cv] | c->c[x]);
            int linked = ((K & Bm) & ~(1ULL << v)) != 0;
            f[3] += linked;
            if (single) f[2] += linked;
        }
    }
    return p;
}

static inline void swapc(const Col *c, const Comp *k, Col *o) {
    *o = *c;
    u64 A = c->c[k->a] & k->K, Bb = c->c[k->b] & k->K;
    o->c[k->a] = (c->c[k->a] & ~k->K) | Bb;
    o->c[k->b] = (c->c[k->b] & ~k->K) | A;
}

static inline long long dot(const long long *w, const long long *f) {
    long long s = 0;
    for (int i = 0; i < 8; i++) s += w[i] * f[i];
    return s;
}

/* ---------------------------------------------------------------- per-thread work */
typedef struct {
    int tid;
    size_t nontarget, hard, onestep_target, endpoints_eval;
    size_t stuck2[MAXW], stuck1[MAXW];
    size_t first2[MAXW];
} Work;

static void *run(void *arg) {
    Work *wk = arg;
    Comp *c0s = malloc(MAXC * sizeof(Comp)), *c1s = malloc(MAXC * sizeof(Comp)), *c2s = malloc(MAXC * sizeof(Comp));
    long long s0[MAXW];
    unsigned char lower1[MAXW], lower[MAXW];
    for (int w = 0; w < NW; w++) wk->first2[w] = (size_t)-1;
    for (size_t s = wk->tid; s < nstates; s += NT) {
        Col c, c1, c2;
        decode(s, &c, NULL);
        if (pval(&c) == 0) continue;
        wk->nontarget++;
        int n0 = components(&c, c0s);
        long long f0[8];
        features(&c, c0s, n0, f0);
        for (int w = 0; w < NW; w++) { s0[w] = dot(W[w], f0); lower1[w] = 0; }
        int target1 = 0;
        /* 1-move endpoints: needed for the one-swap counts and as macro endpoints */
        for (int i = 0; i < n0; i++) {
            swapc(&c, &c0s[i], &c1);
            int n1 = components(&c1, c1s);
            long long f1[8];
            int p1 = features(&c1, c1s, n1, f1);
            if (p1 == 0) { target1 = 1; for (int w = 0; w < NW; w++) lower1[w] = 1; break; }
            for (int w = 0; w < NW; w++) if (!lower1[w] && dot(W[w], f1) < s0[w]) lower1[w] = 1;
        }
        for (int w = 0; w < NW; w++) if (!lower1[w]) wk->stuck1[w]++;
        if (target1) { wk->onestep_target++; continue; }
        /* 2-move target search (weight independent) */
        int target2 = 0;
        for (int i = 0; i < n0 && !target2; i++) {
            swapc(&c, &c0s[i], &c1);
            int n1 = components(&c1, c1s);
            for (int j = 0; j < n1; j++) {
                swapc(&c1, &c1s[j], &c2);
                if (pval(&c2) == 0) { target2 = 1; break; }
            }
        }
        if (target2) continue;
        /* hard state: full rank comparison over the complete endpoint list */
        wk->hard++;
        int remaining = 0;
        for (int w = 0; w < NW; w++) { lower[w] = lower1[w]; remaining += !lower[w]; }
        for (int i = 0; i < n0 && remaining; i++) {
            swapc(&c, &c0s[i], &c1);
            int n1 = components(&c1, c1s);
            for (int j = 0; j < n1 && remaining; j++) {
                swapc(&c1, &c1s[j], &c2);
                int n2 = components(&c2, c2s);
                long long f2[8];
                features(&c2, c2s, n2, f2);  /* p2 = 1 here (hard) */
                wk->endpoints_eval++;
                for (int w = 0; w < NW; w++)
                    if (!lower[w] && dot(W[w], f2) < s0[w]) { lower[w] = 1; remaining--; }
            }
        }
        for (int w = 0; w < NW; w++)
            if (!lower[w]) { wk->stuck2[w]++; if (s < wk->first2[w]) wk->first2[w] = s; }
    }
    free(c0s); free(c1s); free(c2s);
    return NULL;
}

static double now(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + 1e-9 * t.tv_nsec;
}

/* one instance; returns 0 on success, 1 at end of input, 2 on malformed input */
static int solve_one(void) {
    if (scanf("%d %d %d", &n, &root, &NW) != 3) return 1;
    if (n - 1 > 63 || NW > MAXW) { fprintf(stderr, "limits exceeded\n"); return 2; }
    memset(adj, 0, sizeof adj);
    nstates = 0;
    static int rot[65][64], deg[65];
    for (int v = 0; v < n; v++) {
        if (scanf("%d", &deg[v]) != 1 || deg[v] > 63) return 2;
        for (int k = 0; k < deg[v]; k++) if (scanf("%d", &rot[v][k]) != 1) return 2;
    }
    for (int w = 0; w < NW; w++) for (int k = 0; k < 8; k++) if (scanf("%lld", &W[w][k]) != 1) return 2;
    if (deg[root] != 5) { fprintf(stderr, "root not degree five\n"); return 2; }
    int pos[65];
    m = 0;
    for (int v = 0; v < n; v++) { if (v == root) { pos[v] = -1; continue; } pos[v] = m; lab[m++] = v; }
    for (int v = 0; v < n; v++) {
        if (v == root) continue;
        for (int k = 0; k < deg[v]; k++) if (rot[v][k] != root) adj[pos[v]] |= 1ULL << pos[rot[v][k]];
    }
    for (int i = 0; i < m; i++) earlier[i] = adj[i] & ((1ULL << i) - 1);
    Bm = 0;
    for (int j = 0; j < 5; j++) { Bv[j] = pos[rot[root][j]]; Bm |= 1ULL << Bv[j]; }

    double t0 = now();
    enumerate();
    double t1 = now();
    Work *wk = calloc(NT, sizeof(Work));
    pthread_t *th = malloc(NT * sizeof(pthread_t));
    for (int t = 0; t < NT; t++) { wk[t].tid = t; pthread_create(&th[t], NULL, run, &wk[t]); }
    for (int t = 0; t < NT; t++) pthread_join(th[t], NULL);
    double t2 = now();

    size_t nontarget = 0, hard = 0, one_t = 0, evals = 0;
    for (int t = 0; t < NT; t++) {
        nontarget += wk[t].nontarget; hard += wk[t].hard; one_t += wk[t].onestep_target; evals += wk[t].endpoints_eval;
    }
    printf("{\"n\":%d,\"root\":%d,\"vertex_order\":[", n, root);
    for (int i = 0; i < m; i++) printf("%s%d", i ? "," : "", lab[i]);
    printf("],\"boundary_cyclic_order\":[");
    for (int j = 0; j < 5; j++) printf("%s%d", j ? "," : "", rot[root][j]);
    printf("],\"coloring_orbits\":%zu,\"non_target\":%zu,\"one_move_target\":%zu,\"hard\":%zu,"
           "\"hard_endpoint_evaluations\":%zu,\"threads\":%d,\"seconds_enumerate\":%.3f,\"seconds_check\":%.3f,\"results\":[",
           nstates, nontarget, one_t, hard, evals, NT, t1 - t0, t2 - t1);
    for (int w = 0; w < NW; w++) {
        size_t s2 = 0, s1 = 0, first = (size_t)-1;
        for (int t = 0; t < NT; t++) {
            s2 += wk[t].stuck2[w]; s1 += wk[t].stuck1[w];
            if (wk[t].first2[w] < first) first = wk[t].first2[w];
        }
        printf("%s{\"weights\":[", w ? "," : "");
        for (int k = 0; k < 8; k++) printf("%s%lld", k ? "," : "", W[w][k]);
        printf("],\"good\":%s,\"two_swap_stuck\":%zu,\"one_swap_stuck\":%zu,\"first_stuck\":", s2 ? "false" : "true", s2, s1);
        if (first == (size_t)-1) printf("null");
        else {
            Col c; unsigned char col[64];
            decode(first, &c, col);
            Comp cs[MAXC];
            long long f[8];
            int nc = components(&c, cs);
            features(&c, cs, nc, f);
            printf("{\"state_index\":%zu,\"coloring\":[", first);
            for (int i = 0; i < m; i++) printf("%s%d", i ? "," : "", col[i]);
            printf("],\"features\":[");
            for (int k = 0; k < 8; k++) printf("%s%lld", k ? "," : "", f[k]);
            printf("]}");
        }
        printf("}");
    }
    printf("]}\n");
    fflush(stdout);
    free(wk);
    free(th);
    return 0;
}

int main(int argc, char **argv) {
    if (argc > 1) NT = atoi(argv[1]);
    if (NT < 1) NT = 1;
    int rc, k = 0;
    while ((rc = solve_one()) == 0) k++;
    return (rc == 1 && k > 0) ? 0 : 1;
}
