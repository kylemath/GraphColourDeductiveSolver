// Folding-degree parity vs Kempe classes. Usage: degree_parity triN.txt [more files]
// Labelled colourings (all 4-colourings), Kempe classes by union-find, parity of folding degree.
// Also tests candidate descriptions of the parity.
#include <vector>
#include <array>
#include <map>
#include <set>
#include <string>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <numeric>
#include <functional>
#include <cstdio>
using namespace std;
typedef unsigned long long u64;
struct G{int n; vector<array<int,3>> F; vector<vector<int>> adj;};
static void orient(vector<array<int,3>>&F){
  map<pair<int,int>,vector<int>> E; int m=F.size();
  for(int i=0;i<m;i++)for(int k=0;k<3;k++){int a=F[i][k],b=F[i][(k+1)%3];E[{min(a,b),max(a,b)}].push_back(i);}
  vector<char> done(m,0); vector<int> st={0}; done[0]=1;
  while(!st.empty()){int i=st.back();st.pop_back();
    for(int k=0;k<3;k++){int a=F[i][k],b=F[i][(k+1)%3];
      for(int j:E[{min(a,b),max(a,b)}]){ if(done[j])continue; auto&g=F[j];
        for(int q=0;q<3;q++) if(g[q]==a&&g[(q+1)%3]==b){ swap(g[1],g[2]); break;}
        done[j]=1; st.push_back(j);}}}
}
int main(int argc,char**argv){
  for(int ai=1;ai<argc;ai++){
    ifstream in(argv[ai]); string line;
    long graphs=0,classes=0,mixed=0,multi=0,multiboth=0,depmis=0;
    // candidate tests: count colourings (classes) where candidate parity != deg parity
    long cand_fail[8]={0}; long ncol_tot=0; long maxcol=0;
    string firstcex="";
    while(getline(in,line)){
      if(line.empty()||line[0]!='G')continue;
      istringstream ss(line); string g,adjs; int n,m; ss>>g>>n>>adjs>>m;
      G T; T.n=n; T.F.resize(m); for(int i=0;i<m;i++)ss>>T.F[i][0]>>T.F[i][1]>>T.F[i][2];
      T.adj.assign(n,{}); { vector<set<int>> A(n); for(auto&f:T.F)for(int k=0;k<3;k++){int a=f[k],b=f[(k+1)%3];A[a].insert(b);A[b].insert(a);} for(int v=0;v<n;v++)T.adj[v].assign(A[v].begin(),A[v].end()); }
      orient(T.F);
      // BFS order from max degree vertex
      vector<int> order; { int s=0; for(int v=0;v<n;v++) if(T.adj[v].size()>T.adj[s].size()) s=v;
        vector<char> seen(n,0); order.push_back(s); seen[s]=1;
        for(size_t h=0;h<order.size();h++) for(int w:T.adj[order[h]]) if(!seen[w]){seen[w]=1;order.push_back(w);} }
      vector<int> col(n,-1); vector<u64> cols;
      function<void(int)> bt=[&](int i){ if(i==n){u64 k=0;for(int v=0;v<n;v++)k|=(u64)col[v]<<(2*v);cols.push_back(k);return;}
        int v=order[i]; int used=0; for(int w:T.adj[v]) if(col[w]>=0) used|=1<<col[w];
        for(int c=0;c<4;c++) if(!(used>>c&1)){col[v]=c;bt(i+1);col[v]=-1;} };
      bt(0); sort(cols.begin(),cols.end());
      int N=cols.size(); ncol_tot+=N; maxcol=max<long>(maxcol,N);
      vector<int> par(N); iota(par.begin(),par.end(),0);
      function<int(int)> find=[&](int x){while(par[x]!=x){par[x]=par[par[x]];x=par[x];}return x;};
      auto idx=[&](u64 k){return int(lower_bound(cols.begin(),cols.end(),k)-cols.begin());};
      vector<int> cv(n), stk; vector<char> seen(n);
      for(int ci=0;ci<N;ci++){ u64 k=cols[ci]; for(int v=0;v<n;v++)cv[v]=(k>>(2*v))&3;
        for(int a=0;a<4;a++)for(int b=a+1;b<4;b++){ fill(seen.begin(),seen.end(),0);
          for(int v=0;v<n;v++) if((cv[v]==a||cv[v]==b)&&!seen[v]){
            u64 nk=k; stk={v}; seen[v]=1;
            while(!stk.empty()){int u=stk.back();stk.pop_back(); int nc=cv[u]==a?b:a; nk=(nk&~(3ULL<<(2*u)))|((u64)nc<<(2*u));
              for(int w:T.adj[u]) if((cv[w]==a||cv[w]==b)&&!seen[w]){seen[w]=1;stk.push_back(w);} }
            int x=find(ci),y=find(idx(nk)); if(x!=y)par[x]=y; } } }
      // degree & candidates
      map<int,int> cls_par; // root -> bitmask of parities seen
      for(int ci=0;ci<N;ci++){ u64 k=cols[ci]; for(int v=0;v<n;v++)cv[v]=(k>>(2*v))&3;
        int dg[4]; int Favoid[4]={0,0,0,0};
        for(int mm=0;mm<4;mm++){ int rest[3],r=0; for(int x=0;x<4;x++) if(x!=mm) rest[r++]=x; int s=0,cnt=0;
          for(auto&f:T.F){ int t[3]={cv[f[0]],cv[f[1]],cv[f[2]]}; if(t[0]==mm||t[1]==mm||t[2]==mm)continue; cnt++;
            bool pos=false; for(int q=0;q<3;q++) if(t[0]==rest[q]&&t[1]==rest[(q+1)%3]&&t[2]==rest[(q+2)%3]) pos=true;
            s+=pos?1:-1; }
          dg[mm]=s; Favoid[mm]=cnt; }
        bool same=true; for(int mm=1;mm<4;mm++) if(dg[mm]!=dg[0]&&dg[mm]!=-dg[0]) same=false;
        if(!same) depmis++;
        int P=((dg[0]%2)+2)%2;
        // candidates, each computed for colour 0 (and checked all colours for 0,1)
        int nodd[4]={0},nv[4]={0}; for(int v=0;v<n;v++){nv[cv[v]]++; if(T.adj[v].size()%2) nodd[cv[v]]++;}
        bool c0=true,c1=true,c2=true,c3=true,c4=true;
        for(int mm=0;mm<4;mm++){ if((Favoid[mm]&1)!=P) c0=false; if((nodd[mm]&1)!=P) c1=false; if((nv[mm]&1)!=P) c2=false; }
        if(((nv[0]+nv[1]+nv[2]+nv[3])&1)!=P) c3=false; // n parity
        if(((n)&1)!=P) c4=false;
        if(!c0)cand_fail[0]++; if(!c1)cand_fail[1]++; if(!c2)cand_fail[2]++; if(!c3)cand_fail[3]++; if(!c4)cand_fail[4]++;
        cls_par[find(ci)] |= 1<<P;
      }
      int k=cls_par.size(); graphs++; classes+=k; int mix=0,both=0; int seenP=0;
      for(auto&kv:cls_par){ if(kv.second==3) mix++; else seenP|=kv.second; }
      if(mix){ mixed+=mix; if(firstcex.empty()) firstcex=line.substr(0,60); }
      if(k>1){ multi++; if(seenP==3) multiboth++; }
    }
    printf("order-file %s graphs=%ld classes=%ld mixed_classes=%ld multi_class_graphs=%ld multi_both_parities=%ld colourings=%ld (max/graph %ld) face_dep_artefact=%ld | cand_fail: Favoid=%ld oddDegVertsOfColour=%ld nvColour=%ld nParity=%ld n=%ld %s\n",
      argv[ai],graphs,classes,mixed,multi,multiboth,ncol_tot,maxcol,depmis,cand_fail[0],cand_fail[1],cand_fail[2],cand_fail[3],cand_fail[4],firstcex.c_str());
    fflush(stdout);
  }
}
