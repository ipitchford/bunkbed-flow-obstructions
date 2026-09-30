"""Exact multivariate hypergraph identity checks using only the standard library."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

from collections import Counter
from fractions import Fraction as F
import json,time

def merge(p,vs):
    labels={p[i] for i in vs};a=min(labels)
    return tuple(a if x in labels else x for x in p)

def check(word):
    letters=sorted(set(word));t=len(letters);m=len(word)
    hyper=[(t+l*(m+1)+i,t+l*(m+1)+i+1,letters.index(c)) for l in range(2) for i,c in enumerate(word)]
    n=t+2*(m+1);u=t;v=t+m;vp=t+2*m+1;C=Counter()
    def rec(i,p,mask):
        if i==2*m:
            sign=int(p[u]==p[v])-int(p[u]==p[vp])
            if sign:C[len(set(p)),mask]+=sign
            return
        rec(i+1,p,mask)
        rec(i+1,merge(p,hyper[i]),mask+(1<<(2*(i%m))))
    rec(0,tuple(range(n)),0)
    C={k:v for k,v in C.items() if v}
    desired=sum(1<<(2*i) for i in range(m));_require_v03((all(mask==desired for k,mask in C)), 'Validation failed in verify_words.py: 23')
    E=[(letters.index(word[i]),letters.index(word[(i+1)%m])) for i in range(m)]
    flow=Counter()
    for mask in range(1<<m):
        p=tuple(range(t));a=mask.bit_count()
        for i,e in enumerate(E):
            if mask>>i&1:p=merge(p,e)
        flow[a-t+len(set(p))]+=(-1)**(m-a)
    co=[flow[i] for i in range(max(flow)+1)]
    while co and co[-1]==0:co.pop()
    quot=[0]*(len(co)-1);quot[-1]=co[-1]
    for k in range(len(quot)-2,-1,-1):quot[k]=co[k+1]+quot[k+1]
    _require_v03((co[0]==-quot[0]), 'Validation failed in verify_words.py: 35')
    actual={k:c for (k,mask),c in C.items()}
    expected={k+t+2:c for k,c in enumerate(quot) if c}
    _require_v03((actual==expected), 'Validation failed in verify_words.py: 38')
    return {'word':word,'configurations':4**m,'status':'PASS',
            'flow_coefficients_ascending':co,'numerator_coefficients':actual}

if __name__=='__main__':
    start=time.time();checks=[check(w) for w in ['A','AA','AB','ABA','ABC','ABAC','ABCACB','ABCABC','AABCCB','ABACBDCD']]
    choices=[]
    for q in [F(6,5),F(3,2),F(9,5),F(199,100)]:
        z=q-1;ell=2
        while not 4*z**ell<1-z:ell+=2
        phi=(z**(3*ell-1)+3*z**ell+z-1)/q**2
        _require_v03((phi<0), 'Validation failed in verify_words.py: 49')
        choices.append({'q':str(q),'even_multiplicity':ell,'negative':True})
    print(json.dumps({'status':'PASS','word_checks':checks,'triangle_choices':choices,'elapsed_seconds':time.time()-start},indent=2))
