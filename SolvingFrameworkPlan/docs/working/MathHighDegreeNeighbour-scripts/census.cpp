// MathRadiusCensus / census.cpp  [exploratory tooling]
// For every degree-5 vertex v ("hole") of each triangulation in the input file:
//   enumerate all proper 4-colourings of T-v up to colour renaming (canonical = colours numbered by first appearance in vertex order),
//   classify filled (link uses <=3 colours) / unfilled-not-DL / doubly locked (DL, Step 1 of MathConfinementAttack),
//   build the Kempe graph (all whole-component two-colour swaps, all six pairs), multi-source BFS from filled states,
//   report counts, the histogram of the radius over all states and over DL states, unreached states, max DL radius + a witness.
// Usage: census FILE [--range A B] [--cap STATES]  (a hole with more canonical colourings than the cap is written as {capped:true}: inconclusive)  (graph index = 0-based line index among lines starting with 'G')
// Input line: G n hex nf a b c a b c ...  (oriented or unoriented triangular faces; only the faces are used)
// Output (stdout): one JSON object per line per (graph,hole). Exit 0 only if everything ran.
// Compile-time mutations for the mutation tests: -DMUT=k  (see MUT blocks).
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <sstream>
#include <fstream>
#include <iostream>
using std::vector; using std::string;
#ifndef MUT
#define MUT 0
#endif
typedef uint64_t u64;

struct Census {
  int m;                       // vertices of T-v
  vector<vector<int>> nb;      // adjacency of T-v (BFS order labels)
  int link[5];                 // link vertices in cyclic order (labels in T-v)
  vector<u64> states;          // packed 2 bits / vertex
  std::unordered_map<u64,int> idx;
  int col[32];
  size_t cap=2000000; bool capped=false;
  void enumerate(int i, int maxc){
    if(capped) return;
    if(states.size()>cap){ capped=true; return; }
    if(i==m){ u64 p=0; for(int k=0;k<m;k++) p|=(u64)col[k]<<(2*k); idx[p]=states.size(); states.push_back(p); return; }
    int lim = (MUT==4)? 4 : maxc+1; if(lim>4) lim=4;
    for(int c=0;c<lim;c++){
      bool ok=true; for(int w: nb[i]) if(w<i && col[w]==c){ ok=false; break; }
      if(!ok) continue; col[i]=c; enumerate(i+1, std::max(maxc,c+1));
    }
  }
  u64 canon(const int*c) const {
    int mp[4]={-1,-1,-1,-1}; int k=0; u64 p=0;
    for(int i=0;i<m;i++){ int x=c[i]; if(mp[x]<0) mp[x]=k++; p|=(u64)mp[x]<<(2*i); }
    return p;
  }
};
static inline int getc_(u64 p,int i){ return (p>>(2*i))&3; }

// component of colour-pair (a,b) containing vertex s, as bitmask
static u64 comp(const Census&C, const int*c, int a, int b, int s){
  u64 seen=1ull<<s; int st[32],sp=0; st[sp++]=s;
  while(sp){ int u=st[--sp]; for(int w: C.nb[u]) if(!((seen>>w)&1) && (c[w]==a||c[w]==b)){ seen|=1ull<<w; st[sp++]=w; } }
  return seen;
}

int main(int argc,char**argv){
  if(argc<2){ fprintf(stderr,"usage: census FILE [--range A B] [--cap STATES]  (a hole with more canonical colourings than the cap is written as {capped:true}: inconclusive)\n"); return 2; }
  long ra=0, rb=1L<<60; size_t cap=2000000; for(int i=2;i<argc;i++){ string a=argv[i]; if(a=="--range"){ ra=atol(argv[++i]); rb=atol(argv[++i]); } else if(a=="--cap") cap=atol(argv[++i]); }
  std::ifstream in(argv[1]); string line; long gi=0;
  while(std::getline(in,line)){
    if(line.empty()||line[0]!='G') continue;
    long myidx=gi++; if(myidx<ra||myidx>=rb) continue;
    std::istringstream ss(line); string tag,hex; int n,nf; ss>>tag>>n>>hex>>nf;
    vector<vector<int>> faces(nf, vector<int>(3)); for(auto&f:faces) ss>>f[0]>>f[1]>>f[2];
    vector<vector<char>> adj(n, vector<char>(n,0)); for(auto&f:faces) for(int k=0;k<3;k++){ adj[f[k]][f[(k+1)%3]]=adj[f[(k+1)%3]][f[k]]=1; }
    vector<int> deg(n,0); for(int a=0;a<n;a++) for(int b=0;b<n;b++) deg[a]+=adj[a][b];
    int ntri=0; for(int a=0;a<n;a++) for(int b=a+1;b<n;b++) if(adj[a][b]) for(int c2=b+1;c2<n;c2++) if(adj[a][c2]&&adj[b][c2]) ntri++;
    int sep=(ntri!=2*n-4);   // 1 = has a separating triangle (not 4-connected)
    for(int v=0; v<n; v++){
      if(deg[v]!=5) continue;
      // link cycle of v from faces containing v
      vector<std::pair<int,int>> ed; for(auto&f:faces) for(int k=0;k<3;k++) if(f[k]==v) ed.push_back({f[(k+1)%3],f[(k+2)%3]});
      if(ed.size()!=5){ fprintf(stderr,"bad link graph %ld v %d\n",myidx,v); return 3; }
      int lk[5]; lk[0]=ed[0].first; lk[1]=ed[0].second; 
      for(int i=2;i<5;i++){ int cur=lk[i-1]; int nx=-1; for(auto&e:ed){ if(e.first==cur && e.second!=lk[i-2]) nx=e.second; else if(e.second==cur && e.first!=lk[i-2]) nx=e.first; } lk[i]=nx; }
      // relabel T-v in BFS order from lk[0]
      vector<int> order, lab(n,-1); order.push_back(lk[0]); lab[lk[0]]=0;
      for(size_t q=0;q<order.size();q++){ int u=order[q]; for(int w=0;w<n;w++) if(w!=v&&adj[u][w]&&lab[w]<0){ lab[w]=order.size(); order.push_back(w);} }
      Census C; C.m=n-1; C.nb.assign(C.m,{});
      for(int a=0;a<n;a++) for(int b=0;b<n;b++) if(a!=v&&b!=v&&adj[a][b]) C.nb[lab[a]].push_back(lab[b]);
      for(int i=0;i<5;i++) C.link[i]=lab[lk[i]];
      C.states.reserve(1<<14); C.idx.reserve(1<<14);
      C.cap=cap; C.col[0]=0; C.enumerate(1,1);
      if(C.capped){ printf("{\"g\":%ld,\"n\":%d,\"sep\":%d,\"hex\":\"%s\",\"v\":%d,\"capped\":true}\n",myidx,n,sep,hex.c_str(),v); continue; }
      int S=C.states.size();
      vector<vector<int>> nbr(S);   // Kempe neighbours
      vector<char> filled(S), dl(S);
      for(int s=0;s<S;s++){
        int c[32]; for(int i=0;i<C.m;i++) c[i]=getc_(C.states[s],i);
        // classify
        int cnt[4]={0,0,0,0}; for(int i=0;i<5;i++) cnt[c[C.link[i]]]++;
        int used=0; for(int k=0;k<4;k++) used+=cnt[k]>0;
        filled[s]=(used<=3); dl[s]=0;
        if(!filled[s]){
          // exactly one repeated colour on non-adjacent link vertices x_j, x_{j+2}
          int j=-1; for(int t=0;t<5;t++) if(c[C.link[t]]==c[C.link[(t+2)%5]]) j=t;
          int x1=C.link[(j+1)%5], x3=C.link[(j+3)%5], x4=C.link[(j+4)%5];
          int be=c[x1], ga=c[x3], de=c[x4];
          bool l1 = (comp(C,c,be,ga,x1)>>x3)&1;   // beta-gamma path x1 ~ x3
          bool l2 = (comp(C,c,be,de,x1)>>x4)&1;   // beta-delta path x1 ~ x4
#if MUT==1
          dl[s]=l1;
#elif MUT==2
          dl[s]=l1||l2;
#else
          dl[s]=l1&&l2;
#endif
        }
        // Kempe moves
        for(int a=0;a<4;a++) for(int b=a+1;b<4;b++){
#if MUT==3
          if(a==0&&b==1) continue;
#endif
          u64 done=0;
          for(int s0=0;s0<C.m;s0++){
            if(!(c[s0]==a||c[s0]==b) || ((done>>s0)&1)) continue;
            u64 K=comp(C,c,a,b,s0); done|=K;
            int d[32]; memcpy(d,c,sizeof(int)*C.m);
            for(int i=0;i<C.m;i++) if((K>>i)&1) d[i]= (c[i]==a)? b : a;
            u64 p=C.canon(d); auto it=C.idx.find(p);
            if(it==C.idx.end()){ fprintf(stderr,"swap left state space\n"); return 4; }
            if(it->second!=s) nbr[s].push_back(it->second);
          }
        }
      }
      // multi-source BFS from filled
      vector<int> dist(S,-1); vector<int> q;
      for(int s=0;s<S;s++){
#if MUT==5
        if(filled[s]||!dl[s]){ dist[s]=0; q.push_back(s);} 
#else
        if(filled[s]){ dist[s]=0; q.push_back(s);} 
#endif
      }
      for(size_t h=0;h<q.size();h++){ int s=q[h]; for(int t: nbr[s]) if(dist[t]<0){ dist[t]=dist[s]+1; q.push_back(t);} }
      int nfilled=0,ndl=0,unr=0,unrdl=0; vector<long> hall(40,0), hdl(40,0); int maxdl=-1, wit=-1;
      for(int s=0;s<S;s++){
        nfilled+=filled[s]; ndl+=dl[s];
        if(dist[s]<0){ unr++; unrdl+=dl[s]; continue; }
        hall[std::min(dist[s],39)]++; if(dl[s]){ hdl[std::min(dist[s],39)]++; if(dist[s]>maxdl){ maxdl=dist[s]; wit=s; } }
      }
      auto hs=[&](vector<long>&h){ int top=39; while(top>0&&h[top]==0) top--; string o="["; for(int i=0;i<=top;i++){ if(i) o+=","; o+=std::to_string(h[i]); } return o+"]"; };
      printf("{\"g\":%ld,\"n\":%d,\"sep\":%d,\"hex\":\"%s\",\"v\":%d,\"ncol\":%d,\"nfilled\":%d,\"ndl\":%d,\"hist_all\":%s,\"hist_dl\":%s,\"unreached\":%d,\"unreached_dl\":%d,\"maxdl\":%d",
             myidx,n,sep,hex.c_str(),v,S,nfilled,ndl,hs(hall).c_str(),hs(hdl).c_str(),unr,unrdl,maxdl);
      if(wit>=0){ printf(",\"wit\":["); for(int i=0;i<n;i++){ if(i) printf(","); if(i==v) printf("-1"); else printf("%d",getc_(C.states[wit],lab[i])); } printf("]"); }
      printf("}\n");
    }
  }
  return 0;
}
