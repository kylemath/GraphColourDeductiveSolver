// MathRadiusCensus / gen_tri.cpp  [exploratory tooling]
// Generator of plane triangulations with minimum degree >= 5, WITHOUT plantri.
// Usage: gen_tri N [--part I K] [--depth D] [--all] > out.txt
//   Output: one line per isomorphism class (within this process):  G <n> <canon-hex> <nf> a b c a b c ...
//   --all : also output triangulations having a separating triangle (default: 4-connected only)
//   --part I K (default depth 20 faces; deeper = better balance, more prefix overhead): only expand nodes with (counter at depth D faces) % K == I, so K shards are disjoint and complete
//                together; shard outputs must be merged with merge_dedup.py (isomorph classes can recur across shards).
// Method: advancing front. Start at a degree-5 vertex v0 with its 5-link as boundary cycle. Boundary = stack of simple cycles.
//   Step: take top cycle, pivot u = boundary vertex of largest current degree, front edge (u,next(u)); add the triangle
//   (u,next(u),z) with z = a new vertex or any admissible vertex of the same cycle (this may split the cycle in two).
//   Pivot rule depends only on the partial structure, so every triangulation with a degree-5 vertex is reached
//   (every min-degree-5 triangulation has one). Pruning: closed vertex needs degree >= 5; degree <= n-7 (from sum(6-d)=12).
//   Dedup by canonical form (min over all darts x 2 orientations of a BFS code).
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <map>
#include <array>
#include <unordered_set>
#include <algorithm>
using std::string; using std::vector; using std::map; using std::pair; using std::array; using std::unordered_set; using std::swap; using std::min; using std::max;
static const int MAXN = 28;
int n;
struct S {
  uint32_t adj[MAXN]; uint8_t deg[MAXN], occ[MAXN];
  uint8_t buf[200]; uint8_t len[60]; int nseg, bufend, nv, nf;
  uint8_t fa[2*MAXN*3];
};
bool allflag = false; int partI = 0, partK = 1, depthD = 0; long long depthCounter = 0;
long long nodes = 0, emitted = 0, raw = 0;
unordered_set<string> seen;
inline bool isadj(const S&s, int a, int b){ return (s.adj[a]>>b)&1; }
inline void addedge(S&s, int a, int b){ s.adj[a]|=1u<<b; s.adj[b]|=1u<<a; s.deg[a]++; s.deg[b]++; }
inline void addface(S&s, int a, int b, int c){ s.fa[3*s.nf]=a; s.fa[3*s.nf+1]=b; s.fa[3*s.nf+2]=c; s.nf++; }

string canon(const S&s){
  // orient faces by propagation
  int F = s.nf; vector<array<int,3>> f(F); for(int i=0;i<F;i++) f[i]={s.fa[3*i],s.fa[3*i+1],s.fa[3*i+2]};
  map<pair<int,int>,int> dart; // directed edge -> face index (as oriented)
  vector<char> done(F,0); vector<int> st; done[0]=1; st.push_back(0);
  for(int k=0;k<3;k++) dart[{f[0][k],f[0][(k+1)%3]}]=0;
  // edge->faces
  map<pair<int,int>,vector<int>> ef;
  for(int i=0;i<F;i++) for(int k=0;k<3;k++){ int a=f[i][k],b=f[i][(k+1)%3]; ef[{min(a,b),max(a,b)}].push_back(i);}
  while(!st.empty()){ int i=st.back(); st.pop_back();
    for(int k=0;k<3;k++){ int a=f[i][k],b=f[i][(k+1)%3]; auto&v=ef[{min(a,b),max(a,b)}];
      for(int j: v) if(j!=i && !done[j]){ // need b->a in j
        int pos=-1; for(int t=0;t<3;t++) if((f[j][t]==a&&f[j][(t+1)%3]==b)||(f[j][t]==b&&f[j][(t+1)%3]==a)) pos=t;
        if(f[j][pos]==a){ swap(f[j][1],f[j][2]); } // make it traverse b->a
        done[j]=1; st.push_back(j);} } }
  // rotation: for each vertex, neighbours in ccw order: face (a,b,c) oriented: at a, after b comes c  => next[a][b]=c
  vector<vector<int>> nxt(n, vector<int>(n,-1));
  for(int i=0;i<F;i++) for(int k=0;k<3;k++){ int a=f[i][k],b=f[i][(k+1)%3],c=f[i][(k+2)%3]; nxt[a][b]=c; }
  // prv[a][c]=b
  vector<vector<int>> prv(n, vector<int>(n,-1));
  for(int a=0;a<n;a++) for(int b=0;b<n;b++) if(nxt[a][b]>=0) prv[a][nxt[a][b]]=b;
  string best; bool have=false;
  for(int mir=0;mir<2;mir++){ auto &nx = mir? prv: nxt;
    for(int x=0;x<n;x++) for(int y=0;y<n;y++) if(nx[x][y]>=0){
      vector<int> lab(n,-1), order; lab[x]=0; order.push_back(x); string code; 
      // ref neighbour for root = y
      vector<int> ref(n,-1); ref[x]=y;
      for(size_t qi=0; qi<order.size(); qi++){ int w=order[qi]; int r=ref[w]; int cur=r; 
        do{ if(lab[cur]<0){ lab[cur]=order.size(); order.push_back(cur); ref[cur]=w; }
            code.push_back((char)(lab[cur]+1)); cur=nx[w][cur]; } while(cur!=r);
        code.push_back((char)0); }
      if(!have || code<best){ best=code; have=true; }
    } }
  return best;
}
string tohex(const string&c){ static const char*H="0123456789abcdef"; string o; for(unsigned char ch: c){ o+=H[ch>>4]; o+=H[ch&15]; } return o; }

void emit(const S&s){
  raw++;
  // triangle count == 2n-4 ?  (4-connected iff every triangle is a face)
  if(!allflag){
    int tri=0; for(int a=0;a<n;a++) for(int b=a+1;b<n;b++) if(isadj(s,a,b)) tri+=__builtin_popcount(s.adj[a]&s.adj[b]&~((2u<<b)-1));
    if(tri!=2*n-4) return;
  }
  string c=canon(s); string h=tohex(c);
  if(seen.insert(h).second){ emitted++;
    printf("G %d %s %d", n, h.c_str(), s.nf); for(int i=0;i<s.nf;i++) printf(" %d %d %d", s.fa[3*i],s.fa[3*i+1],s.fa[3*i+2]); printf("\n"); }
}

// decrement occurrence; return false if the vertex is closed with too small degree
inline bool leave(S&s,int v){ if(--s.occ[v]==0) return s.deg[v]>=5; return true; }

void rec(S&s);
void push(S&s,const vector<int>&c){ for(int v: c) s.buf[s.bufend++]=v; s.len[s.nseg++]=c.size(); }

void rec(S&s){
  nodes++;
  { int ex=0; for(int v=0;v<s.nv;v++) if(s.deg[v]>5) ex+=s.deg[v]-5; if(ex>n-12) return; }  // sum(deg-5)=n-12 exactly
  if(s.nseg==0){ if(s.nv==n && s.nf==2*n-4) emit(s); return; }
  if(depthD && s.nf==depthD){ long long k=depthCounter++; if(k%partK!=partI) return; }
  int L=s.len[s.nseg-1]; int base=s.bufend-L;
  int c[64]; for(int i=0;i<L;i++) c[i]=s.buf[base+i];
  int p=0; for(int i=1;i<L;i++) if(s.deg[c[i]]>s.deg[c[p]]) p=i;
  if(p){ int t[64]; for(int i=0;i<L;i++) t[i]=c[(i+p)%L]; memcpy(c,t,sizeof(int)*L); }
  int x=c[0], y=c[1];
  int dmax=n-7;
  // (a) new vertex
  if(s.nv<n && s.deg[x]+1<=dmax && s.deg[y]+1<=dmax){
    S t=s; t.bufend-=L; t.nseg--; int z=t.nv++; addedge(t,x,z); addedge(t,y,z); t.occ[z]=1; addface(t,x,y,z);
    vector<int> nc; nc.push_back(x); nc.push_back(z); for(int i=1;i<L;i++) nc.push_back(c[i]);
    push(t,nc); rec(t);
  }
  if(L==3){
    int z=c[2]; S t=s; t.bufend-=L; t.nseg--; addface(t,x,y,z);
    bool ok=leave(t,x)&&leave(t,y)&&leave(t,z); if(ok) rec(t); return;
  }
  for(int j=2;j<L;j++){
    int z=c[j];
    if(j==L-1){ // z = prev(x); edge x-z is a cycle edge
      if(isadj(s,y,z)) continue; if(s.deg[y]+1>dmax||s.deg[z]+1>dmax) continue;
      S t=s; t.bufend-=L; t.nseg--; addedge(t,y,z); addface(t,x,y,z);
      vector<int> nc(c+1,c+L); push(t,nc); if(leave(t,x)) rec(t);
    } else if(j==2){ // z = next(y); edge y-z is a cycle edge
      if(isadj(s,x,z)) continue; if(s.deg[x]+1>dmax||s.deg[z]+1>dmax) continue;
      S t=s; t.bufend-=L; t.nseg--; addedge(t,x,z); addface(t,x,y,z);
      vector<int> nc; nc.push_back(x); for(int i=2;i<L;i++) nc.push_back(c[i]); push(t,nc); if(leave(t,y)) rec(t);
    } else {
      if(isadj(s,x,z)||isadj(s,y,z)) continue;
      if(s.deg[x]+1>dmax||s.deg[y]+1>dmax||s.deg[z]+2>dmax) continue;
      S t=s; t.bufend-=L; t.nseg--; addedge(t,x,z); addedge(t,y,z); addface(t,x,y,z); t.occ[z]++;
      vector<int> A(c+1,c+j+1); vector<int> B; for(int i=j;i<L;i++) B.push_back(c[i]); B.push_back(c[0]);
      push(t,A); push(t,B); rec(t);   // top = B
    }
  }
}

int main(int argc,char**argv){
  if(argc<2){ fprintf(stderr,"usage\n"); return 2; }
  n=atoi(argv[1]); if(n>MAXN){ fprintf(stderr,"n too big\n"); return 2; }
  for(int i=2;i<argc;i++){ string a=argv[i];
    if(a=="--all") allflag=true; else if(a=="--part"){ partI=atoi(argv[++i]); partK=atoi(argv[++i]); }
    else if(a=="--depth") depthD=atoi(argv[++i]); }
  if(partK>1 && !depthD) depthD=20;
  S s; memset(&s,0,sizeof s);
  // v0 = 0, link 1..5
  for(int i=1;i<=5;i++){ addedge(s,0,i); }
  for(int i=1;i<=5;i++){ int j=i%5+1; addedge(s,i,j); addface(s,0,i,j); }
  s.nv=6; for(int i=1;i<=5;i++) s.occ[i]=1;
  vector<int> cyc={1,2,3,4,5}; push(s,cyc);
  rec(s);
  fprintf(stderr,"n=%d nodes=%lld raw=%lld classes=%lld\n",n,nodes,raw,emitted);
  return 0;
}
