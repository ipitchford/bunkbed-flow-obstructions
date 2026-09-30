"""Exact conditioned-post fan-chain verification by two independent methods.

Method A: random-cluster connectivity frontier dynamic programming (integers).
Method B: finite post-colour partition/Potts transfer (rational matrices).
No numerical floating-point computations enter these checks.
"""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

from fractions import Fraction as F
from collections import defaultdict
from itertools import product
from math import comb
import json, sys, time
sys.set_int_max_str_digits(1000000)

def canonical(p):
    d={}
    return tuple(d.setdefault(a,len(d)) for a in p)

def merge(p,a,b):
    x,y=p[a],p[b]
    if x==y:return p
    return canonical(tuple(x if z==y else z for z in p))

def neighbours(word,L,j):
    """Posts adjacent to rim vertex j (there are len(word)*L+1)."""
    m=len(word)
    if j==0:return [word[0]]
    if j==m*L:return [word[-1]]
    i,r=divmod(j,L)
    return sorted(set([word[i-1],word[i]])) if r==0 else [word[i]]

def core_dp(q,x,L,word):
    q,x=F(q),F(x);t=max(word)+1;N=len(word)*L
    # slots: t permanent posts, permanent u_0, moving top, moving bottom.
    state=tuple(range(t+1))+(t,t+1)
    states={state:1};den=1;max_states=1
    def edge(a,b):
        nonlocal states,den,max_states
        out=defaultdict(int)
        for p,c in states.items():
            out[p]+=c*x.denominator
            out[merge(p,a,b)]+=c*x.numerator
        states=dict(out);den*=x.denominator
        max_states=max(max_states,len(states))
    for a in neighbours(word,L,0):
        edge(a,t+1);edge(a,t+2)
    for j in range(1,N+1):
        states={p+(max(p)+1,max(p)+2):c for p,c in states.items()}
        edge(t+1,t+3);edge(t+2,t+4)
        for a in neighbours(word,L,j):
            edge(a,t+3);edge(a,t+4)
        keep=list(range(t+1))+[t+3,t+4]
        out=defaultdict(int)
        for p,c in states.items():
            pp=tuple(p[k] for k in keep)
            lost=len(set(p)-set(pp))
            out[canonical(pp)]+=c*q.numerator**lost*q.denominator**(2-lost)
        states=dict(out);den*=q.denominator**2
    total=0;s=t+3
    for p,c in states.items():
        sign=int(p[t]==p[t+1])-int(p[t]==p[t+2])
        k=len(set(p))
        total+=sign*c*q.numerator**k*q.denominator**(s-k)
    den*=q.denominator**s
    return F(total,den),max_states

def partitions(n):
    def rec(a,r):
        if len(a)==n:
            yield tuple(a);return
        for s in range(r+1):yield from rec(a+[s],max(r,s+1))
    yield from rec([0],1)

def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def mm(A,B):
    n=len(A);return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def power(A,L):
    out=eye(len(A))
    while L:
        if L&1:out=mm(out,A)
        L//=2
        if L:A=mm(A,A)
    return out

def core_potts(q,x,L,word):
    q,x=F(q),F(x);f=1+x;t=max(word)+1;m=len(word);ans=F(0)
    for pi in partitions(t):
        r=max(pi)+1;n=r+1;w=[F(1)]*r+[q-r]
        R=[[w[j]+x*(i==j) for j in range(n)] for i in range(n)]
        mats=[]
        for s in range(r):
            D=eye(n);D[s][s]=f
            mats.append(mm(D,power(mm(R,D),L)))
        K=eye(n)
        for c in word:K=mm(K,mats[pi[c]])
        K2=mm(K,K)
        z=sum(w[i]*K[i][j] for i in range(n) for j in range(n))
        val=z*(sum(K[i][i] for i in range(n))+(q-r-1)*x**(L*m))
        val-=sum(w[i]*K2[i][j] for i in range(n) for j in range(n))
        falling=F(1)
        for j in range(r):falling*=q-j
        ans+=falling*val
    return q/(q-1)*ans

def core_edges(word,L):
    t=max(word)+1;m=len(word);edges=[]
    for j in range(m*L):edges.append((t+j,t+j+1))
    for j in range(m*L+1):
        for a in neighbours(word,L,j):edges.append((a,t+j))
    _require_v03((len(edges)==m*(2*L+1)), 'Validation failed in verify_core.py: 109')
    _require_v03((len(set(tuple(sorted(e)) for e in edges))==len(edges)), 'Validation failed in verify_core.py: 110')
    return t+m*L+1,edges,list(range(t)),t,t+m*L

def direct(q,x,L,word):
    n,E,T,u,v=core_edges(word,L);t=len(T)
    # Build the contracted-post two-layer graph; no vertical edges elsewhere.
    def vertex(a,layer):return a if a<t else t+2*(a-t)+layer
    edges=[(vertex(a,k),vertex(b,k)) for a,b in E for k in (0,1)]
    nv=2*n-t;out=F(0)
    for bits in product((0,1),repeat=len(edges)):
        p=tuple(range(nv));a=0
        for bit,(s,z) in zip(bits,edges):
            if bit:p=merge(p,s,z);a+=1
        sign=int(p[vertex(u,0)]==p[vertex(v,0)])-int(p[vertex(u,0)]==p[vertex(v,1)])
        out+=sign*F(q)**len(set(p))*F(x)**a
    return out

def amplify(q,x,n,e,t,delta):
    """A conservative exact post-amplification certificate."""
    q,x,delta=F(q),F(x),F(delta)
    _require_v03((q>0 and x>0 and delta>0), 'Validation failed in verify_core.py: 130')
    B=max(F(1),q)**(2*n)*(1+x)**(2*e+n-t)
    r=x**3/(q*q+3*q*x+3*x*x)
    h=(r.denominator+r.numerator-1)//r.numerator
    target=max(F(2),2**(t+1)*B/delta)
    s=max(1,target.numerator.bit_length()-target.denominator.bit_length()+1)
    while 2**s<=target:s+=1
    while s>1 and 2**(s-1)>target:s-=1
    k=h*s
    _require_v03((h*r>=1 and 2**s>target), 'Validation failed in verify_core.py: 139')
    return {'h':h,'s':s,'k_per_post':k,'base_vertices':n+t*k,
            'base_edges':e+t*k,'full_vertices':2*(n+t*k),
            'full_edges':2*(e+t*k)+(n+t*k)}

if __name__=='__main__':
    start=time.time();checks=[]
    for q,x,L,word in [(F(3,2),F(1),1,[0,1]),(F(21,10),F(2,3),1,[0,1]),
                       (F(1,2),F(3,2),1,[0,1]),(F(3),F(1),1,[0,1])]:
        a,ms=core_dp(q,x,L,word);b=core_potts(q,x,L,word);c=direct(q,x,L,word)
        _require_v03((a==b==c), 'Validation failed in verify_core.py: 149')
        checks.append({'q':str(q),'x':str(x),'L':L,'word':word,'numerator':str(a),'three_methods_agree':True})
    word=[0,1,2]*4;q=F(3,2);x=F(1);L=20
    a,ms=core_dp(q,x,L,word);b=core_potts(q,x,L,word)
    _require_v03((a==b and a<0), 'Validation failed in verify_core.py: 153')
    n,E,T,u,v=core_edges(word,L)
    receipt={'status':'PASS','q':str(q),'p':'1/2','x':str(x),'word':word,'L':L,
             'core_vertices':n,'core_edges':len(E),'frontier_max_states':ms,
             'core_numerator':str(a),'independent_methods_agree':True,
             'amplification':amplify(q,x,n,len(E),len(T),-a),
             'small_checks':checks,'elapsed_seconds':time.time()-start}
    print(json.dumps(receipt,indent=2))
