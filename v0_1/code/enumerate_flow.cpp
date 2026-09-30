// Independent exact combinatorial enumerations. No external libraries.
// Usage: enumerate_flow subsets|partitions < graph.txt
// graph.txt: n m, followed by m unordered endpoint pairs (zero based).
#include <iostream>
#include <vector>
#include <string>
#include <functional>
#include <stdexcept>
#include <cstdint>
#include <set>
using namespace std;
int main(int argc,char**argv){
 try{
  if(argc!=2)throw runtime_error("usage: enumerate_flow subsets|partitions");
  int n,m;if(!(cin>>n>>m)||n<1||n>12||m<0||m>24)throw runtime_error("invalid graph size");
  vector<pair<int,int>> E(m);vector<uint64_t> prior(n,0);set<pair<int,int>> seen;
  for(auto &e:E){cin>>e.first>>e.second;if(e.first<0||e.second<0||e.first>=n||e.second>=n||e.first==e.second)throw runtime_error("invalid edge");
   int a=min(e.first,e.second),b=max(e.first,e.second);if(!seen.insert({a,b}).second)throw runtime_error("simple graphs only");prior[b]|=uint64_t(1)<<a;}
  string mode(argv[1]);
  if(mode=="subsets"){
   vector<int> p(n);for(int i=0;i<n;i++)p[i]=i;
   vector<int64_t> co(m+1,0);
   auto find=[&](int a){while(p[a]!=a)a=p[a];return a;};
   function<void(int,int,int)> rec=[&](int i,int a,int k){
    if(i==m){int nullity=a-n+k;if(nullity<0)throw runtime_error("negative nullity");co[nullity]+=((m-a)%2?-1:1);return;}
    rec(i+1,a,k);
    int u=find(E[i].first),v=find(E[i].second);
    if(u==v)rec(i+1,a+1,k);else{p[u]=v;rec(i+1,a+1,k-1);p[u]=u;}
   };
   rec(0,0,n);for(int i=0;i<=m;i++)if(co[i])cout<<i<<" "<<co[i]<<"\n";
  }else if(mode=="partitions"){
   // Named colour classes as vertex bitsets; no connectivity algorithm here.
   vector<uint64_t> blocks(n,0);vector<vector<int64_t>> hist(n+1,vector<int64_t>(m+1));
   function<void(int,int,int)> rec=[&](int i,int r,int h){
    if(i==n){hist[r][h]++;return;}
    for(int b=0;b<r;b++){
     int add=__builtin_popcountll(prior[i]&blocks[b]);blocks[b]|=uint64_t(1)<<i;
     rec(i+1,r,h+add);blocks[b]^=uint64_t(1)<<i;
    }
    blocks[r]=uint64_t(1)<<i;rec(i+1,r+1,h);blocks[r]=0;
   };
   rec(0,0,0);for(int r=0;r<=n;r++)for(int h=0;h<=m;h++)if(hist[r][h])cout<<r<<" "<<h<<" "<<hist[r][h]<<"\n";
  }else throw runtime_error("unknown mode");
 }catch(const exception&e){cerr<<e.what()<<"\n";return 1;}
}
