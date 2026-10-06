// MathNDiscSearch / disc_gen.cpp   [exploratory, undeclared, post hoc]
// Direct construction of acyclic 4-coloured triangulated discs T-x with ring word D a D b g
// (colours 0=D,1=a,2=b,3=g on ring u0..u4), all six pair subgraphs forests, component vector
// (Da,Db,Dg,ab,ag,bg) = (1,2,2,1,1,1), class sizes fixed by a target (nD,na,nb,ng), class degree
// excess exactly n-4-3n_i (a: n-3-3n_a) (Prop 3 of d1-hand-attack.md). No triangulation enumeration:
// the disc is grown inward from the ring by an advancing front (a stack of simple cycles).
// Usage: disc_gen N [maxout] [tlimit_sec]   (N = order of T; disc has N-1 vertices)
// Output: one line per disc: "SIZES nD na nb ng" headers and "DISC col(V) ; edges u-v ..."
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <ctime>
#include <vector>
#include <set>
using namespace std;
using namespace std;
static int V, N;
static int target[4], excT[4];
static const int PI[4][4] = {{-1,0,1,2},{0,-1,3,4},{1,3,-1,5},{2,4,5,-1}};
static const int PT[6] = {1,2,2,1,1,1};   // target comps per pair (Da,Db,Dg,ab,ag,bg)
struct St {
  int8_t col[24]; int8_t deg[24]; int8_t occ[24]; int cnt; int8_t ccount[4];
  uint32_t adj[24];
  int8_t lab[6][24];
  vector<vector<int8_t>> cyc;
};
static long long nodes=0, found=0, maxout=1000000; static double tlimit=1e18; static clock_t t0;
static bool timeout_hit=false;
static inline bool isring(int v){return v<5;}
static bool addEdge(St&s,int u,int v){
  if(s.adj[u]>>v&1) return false;
  if(isring(u)&&isring(v)) return false;           // ring chord (or duplicate ring edge) forbidden
  int a=s.col[u],b=s.col[v]; if(a==b) return false;
  int p=PI[a][b];
  if(s.lab[p][u]==s.lab[p][v]) return false;      // would close a cycle in a pair subgraph
  int from=s.lab[p][v],to=s.lab[p][u];
  for(int i=0;i<V;i++) if(s.lab[p][i]==from) s.lab[p][i]=to;
  s.adj[u]|=1u<<v; s.adj[v]|=1u<<u; s.deg[u]++; s.deg[v]++;
  return true;
}
static bool feasible(const St&s){
  // class excess lower bound
  int ex[4]={0,0,0,0};
  for(int v=0;v<s.cnt;v++){ int td=s.deg[v]+(isring(v)?1:0); if(td>5) ex[(int)s.col[v]]+=td-5; }
  for(int k=0;k<4;k++) if(ex[k]>excT[k]) return false;
  // closed vertices need final degree
  for(int v=0;v<s.cnt;v++) if(s.occ[v]==0){ int td=s.deg[v]+(isring(v)?1:0); if(td<5) return false; }
  // pair components: closed comps cannot merge
  for(int a=0;a<4;a++) for(int b=a+1;b<4;b++){
    int p=PI[a][b]; int closedc=0,openc=0; bool seen[24]={0}; // by label
    // label -> closed?
    int8_t st[24]; for(int i=0;i<24;i++) st[i]=-1; // -1 none, 0 closed, 1 open
    for(int v=0;v<s.cnt;v++) if(s.col[v]==a||s.col[v]==b){
      int l=s.lab[p][v]; int o=s.occ[v]>0;
      if(st[l]==-1) st[l]=o?1:0; else if(o) st[l]=1;
    }
    (void)seen;
    for(int i=0;i<24;i++){ if(st[i]==0) closedc++; else if(st[i]==1) openc++; }
    if(closedc+(openc>0?1:0)>PT[p]) return false;
  }
  return true;
}
static void output(const St&s){
  found++;
  printf("DISC %d %d %d %d ;", target[0],target[1],target[2],target[3]);
  for(int v=0;v<V;v++) printf(" %d",s.col[v]);
  printf(" ;");
  for(int u=0;u<V;u++) for(int v=u+1;v<V;v++) if(s.adj[u]>>v&1) printf(" %d-%d",u,v);
  printf("\n"); fflush(stdout);
}
static void finalcheck(const St&s){
  if(s.cnt!=V) return;
  for(int a=0;a<4;a++) for(int b=a+1;b<4;b++){
    int p=PI[a][b]; set<int> L; for(int v=0;v<V;v++) if(s.col[v]==a||s.col[v]==b) L.insert(s.lab[p][v]);
    if((int)L.size()!=PT[p]) return;
  }
  for(int v=0;v<V;v++){ int td=s.deg[v]+(isring(v)?1:0); if(td<5) return; }
  output(s);
}
static void rec(St s){
  if(found>=maxout||timeout_hit) return;
  nodes++;
  if((nodes&0xFFFF)==0 && (double)(clock()-t0)/CLOCKS_PER_SEC>tlimit){timeout_hit=true;return;}
  // drop finished cycles
  if(s.cyc.empty()){ finalcheck(s); return; }
  vector<int8_t> c=s.cyc.back(); s.cyc.pop_back();
  int L=c.size();
  // choose the vertex of max degree, edge (c[i],c[i+1])
  int bi=0; for(int i=1;i<L;i++) if(s.deg[(int)c[i]]>s.deg[(int)c[bi]]) bi=i;
  int i=bi, a=c[i], b=c[(i+1)%L];
  // 1. new vertex
  if(s.cnt<V){
    for(int k=0;k<4;k++){
      if(k==s.col[a]||k==s.col[b]||s.ccount[k]>=target[k]) continue;
      St t=s; int w=t.cnt++; t.col[w]=k; t.ccount[k]++; t.deg[w]=0; t.occ[w]=1; t.adj[w]=0;
      if(!addEdge(t,a,w)||!addEdge(t,b,w)) continue;
      vector<int8_t> nc; for(int j=0;j<L;j++){ nc.push_back(c[j]); if(j==i) nc.push_back(w); }
      t.cyc.push_back(nc);
      if(feasible(t)) rec(t);
    }
  }
  // 2. existing vertex of the same cycle
  if(L==3){
    St t=s; int w=c[(i+2)%3];
    for(int j=0;j<3;j++) t.occ[(int)c[j]]--;
    (void)w;
    if(feasible(t)) rec(t);
  } else {
    for(int d=2; d<=L-1; d++){
      int j=(i+d)%L, w=c[j];
      St t=s; bool ok=true;
      if(d==2){ // w = next(b): edge bw exists; new edge a-w; remove b
        ok=addEdge(t,a,w); if(!ok) continue;
        t.occ[b]--; vector<int8_t> nc; for(int q=0;q<L;q++) if(q!=(i+1)%L) nc.push_back(c[q]);
        t.cyc.push_back(nc);
      } else if(d==L-1){ // w = prev(a): new edge b-w; remove a
        ok=addEdge(t,b,w); if(!ok) continue;
        t.occ[a]--; vector<int8_t> nc; for(int q=0;q<L;q++) if(q!=i) nc.push_back(c[q]);
        t.cyc.push_back(nc);
      } else {
        if(!addEdge(t,a,w)||!addEdge(t,b,w)) continue;
        vector<int8_t> c1,c2; // c1 = b..w ; c2 = w..a
        for(int q=(i+1)%L;;q=(q+1)%L){ c1.push_back(c[q]); if(q==j) break; }
        for(int q=j;;q=(q+1)%L){ c2.push_back(c[q]); if(q==i) break; }
        t.occ[w]++;
        t.cyc.push_back(c1); t.cyc.push_back(c2);
      }
      if(feasible(t)) rec(t);
    }
  }
}
int main(int argc,char**argv){
  N=atoi(argv[1]); V=N-1; if(argc>2) maxout=atoll(argv[2]); if(argc>3) tlimit=atof(argv[3]);
  t0=clock();
  // enumerate size targets: nD>=2, others>=1; exc_i>=0
  for(int nD=2;nD<=V;nD++) for(int na=1;na<=V;na++) for(int nb=1;nb<=V;nb++){
    int ng=V-nD-na-nb; if(ng<1) continue;
    int ex[4]={N-4-3*nD, N-3-3*na, N-4-3*nb, N-4-3*ng};
    if(ex[0]<0||ex[1]<0||ex[2]<0||ex[3]<0) continue;
    target[0]=nD;target[1]=na;target[2]=nb;target[3]=ng; for(int k=0;k<4;k++) excT[k]=ex[k];
    St s; memset(&s,0,sizeof s);
    s.cnt=5; int rc[5]={0,1,0,2,3};
    for(int v=0;v<5;v++){ s.col[v]=rc[v]; s.occ[v]=1; s.ccount[rc[v]]++; }
    for(int p=0;p<6;p++) for(int v=0;v<24;v++) s.lab[p][v]=v;
    bool ok=true; for(int v=0;v<5;v++) ok&=addEdge(s,v,(v+1)%5);
    // addEdge forbids ring-ring edges; ring edges are added by hand instead
    (void)ok;
    memset(s.adj,0,sizeof s.adj); memset(s.deg,0,sizeof s.deg);
    for(int p=0;p<6;p++) for(int v=0;v<24;v++) s.lab[p][v]=v;
    for(int v=0;v<5;v++){ int u=(v+1)%5; int p=PI[s.col[v]][s.col[u]];
      int from=s.lab[p][u],to=s.lab[p][v]; for(int i=0;i<24;i++) if(s.lab[p][i]==from) s.lab[p][i]=to;
      s.adj[v]|=1u<<u; s.adj[u]|=1u<<v; s.deg[v]++; s.deg[u]++; }
    if(s.ccount[0]>nD||s.ccount[1]>na||s.ccount[2]>nb||s.ccount[3]>ng) continue;
    vector<int8_t> c={0,1,2,3,4}; s.cyc.push_back(c);
    long long f0=found,n0=nodes; rec(s);
    fprintf(stderr,"sizes (%d,%d,%d,%d) exc (%d,%d,%d,%d): found %lld nodes %lld%s\n",nD,na,nb,ng,ex[0],ex[1],ex[2],ex[3],found-f0,nodes-n0,timeout_hit?" TIMEOUT":"");
    if(timeout_hit||found>=maxout) break;
  }
  fprintf(stderr,"N=%d total found %lld nodes %lld cpu %.1fs%s\n",N,found,nodes,(double)(clock()-t0)/CLOCKS_PER_SEC,timeout_hit?" (INCOMPLETE: time limit)":"");
}
