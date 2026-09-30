"""Large circulants: exact flow polynomial by frontier DP, exact real-root
isolation with sympy, certified negative interval above 2."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json, time, sys
from fractions import Fraction as Fr
import sympy
from bb_tools import *
q=sympy.symbols('q')
def circulant(n,S):
    E=set()
    for i in range(n):
        for s in S:
            j=(i+s)%n
            if j!=i: E.add((min(i,j),max(i,j)))
    return n,sorted(E)
def certified_neg(P):
    """P: int coeff list ascending. Returns list of (a,b) rational with P<0 on [a,b], no roots inside, a,b near the roots."""
    Pq=sympy.Poly(sum(sympy.Integer(c)*q**i for i,c in enumerate(P)),q,domain='QQ')
    ivs=Pq.intervals(inf=2,sup=50,eps=sympy.Rational(1,10**9))
    roots=[(Fr(int(a.p),int(a.q)),Fr(int(b.p),int(b.q))) for (a,b),mult in ivs]
    pts=[Fr(2)]+[x for r in roots for x in r]+[Fr(50)]
    out=[]
    for i in range(0,len(pts),2):
        a,b=pts[i],pts[i+1]
        if b<=a: continue
        if peval(P,a)<0 and peval(P,b)<0 and Pq.count_roots(sympy.Rational(a.numerator,a.denominator),sympy.Rational(b.numerator,b.denominator))==0:
            out.append((a,b))
    return out,roots
jobs=[]
for S in [(1,5),(3,4),(2,5),(3,5),(1,6),(2,7),(1,4),(1,3)]:
    for n in [int(x) for x in sys.argv[1].split(',')]:
        jobs.append((n,S))
rows=[]
for n,S in jobs:
    t1=time.time(); nn,E=circulant(n,S)
    F=flow_poly(nn,E); P,r=pdivmod(F,[-1,1]); _require_v03((not r), 'Validation failed in families4.py: 35'); P=[int(c) for c in P]
    negs,roots=certified_neg(P)
    rows.append({'family':f'C{n}{S}','n':n,'m':len(E),'certified_neg':[[str(a),str(b)] for a,b in negs],'neg_float':[[float(a),float(b)] for a,b in negs],'roots_float':[float((a+b)/2) for a,b in roots]})
    print("C%d%s m=%d neg>2: %s  (%.1fs)"%(n,S,len(E),[(round(float(a),6),round(float(b),6)) for a,b in negs],time.time()-t1),flush=True)
    json.dump(rows,open(f'/home/claude/bunkbed/v02/data/families4_{sys.argv[1].replace(",","_")}.json','w'),indent=1)
