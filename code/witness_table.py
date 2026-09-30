"""Certified table of Eulerian witnesses above q=2 (K_{4,b} and circulants).
Exact flow polynomial (frontier DP), exact real-root isolation (sympy over QQ),
and a certified negative sub-interval with short rational endpoints:
P(a)<0, P(b)<0 and count_roots(a,b)=0, where P=F/(q-1)."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json,time,sys,math
from fractions import Fraction as Fr
import sympy
from bb_tools import *
qs=sympy.symbols('q')
def circulant(n,S):
    E=set()
    for i in range(n):
        for s in S:
            j=(i+s)%n
            if j!=i: E.add((min(i,j),max(i,j)))
    return n,sorted(E)
def K4b(b): return 4+b,[(i,4+j) for j in range(b) for i in range(4)]
def certify(P):
    Pq=sympy.Poly(sum(sympy.Integer(c)*qs**i for i,c in enumerate(P)),qs,domain='QQ')
    ivs=Pq.intervals(inf=2,sup=60,eps=sympy.Rational(1,10**8))
    roots=[(Fr(int(a.p),int(a.q)),Fr(int(b.p),int(b.q))) for (a,b),_ in ivs]
    _require_v03((len(roots)==2), ("expected exactly two roots above 2", roots))
    (l1,l2),(u1,u2)=roots
    # short rational endpoints: a = ceil(l2 * 10^7)/10^7 ; b = floor(u1*10^4)/10^4
    a=Fr(math.ceil(l2*10**7),10**7); b=Fr(math.floor(u1*10**4),10**4)
    ok=peval(P,a)<0 and peval(P,b)<0 and Pq.count_roots(sympy.Rational(a.numerator,a.denominator),sympy.Rational(b.numerator,b.denominator))==0
    _require_v03((ok), 'Validation failed in witness_table.py: 27')
    # also: no other real roots above 2 => P>0 elsewhere on (2,60]; check P(2)>0 and P(60)>0
    _require_v03((peval(P,Fr(2))>0 and peval(P,Fr(60))>0), 'Validation failed in witness_table.py: 29')
    return {'roots_isolating':[[str(l1),str(l2)],[str(u1),str(u2)]],'roots_float':[float((l1+l2)/2),float((u1+u2)/2)],'certified_negative':[str(a),str(b)],'certified_negative_float':[float(a),float(b)]}
jobs=[('K4,6',K4b(6)),('K4,8',K4b(8)),('K4,12',K4b(12)),('K4,16',K4b(16)),
      ('C10(1,4)',circulant(10,(1,4))),('C10(1,3)',circulant(10,(1,3))),('C12(2,3)',circulant(12,(2,3))),('C14(1,3)',circulant(14,(1,3))),
      ('C16(2,3)',circulant(16,(2,3))),('C18(1,5)',circulant(18,(1,5))),('C20(2,3)',circulant(20,(2,3))),('C20(3,4)',circulant(20,(3,4))),
      ('C24(3,4)',circulant(24,(3,4))),('C24(2,5)',circulant(24,(2,5))),('C28(1,5)',circulant(28,(1,5)))]
if '--with-C32' in sys.argv: jobs.append(('C32(1,5)',circulant(32,(1,5))))
rows=[]
if __name__!='__main__': jobs=[]
for name,(n,E) in jobs:
    t1=time.time(); F=flow_poly(n,E); P,r=pdivmod(F,[-1,1]); _require_v03((not r), 'Validation failed in witness_table.py: 39'); P=[int(c) for c in P]
    c=certify(P)
    rows.append({'name':name,'n':n,'m':len(E),'edges':E,'flow_coefficients_ascending':F,'P_coefficients_ascending':P,**c,'seconds':round(time.time()-t1,1)})
    print("%-9s n=%2d m=%3d roots %.7f %.7f  certified [%s, %s] (%.1fs)"%(name,n,len(E),c['roots_float'][0],c['roots_float'][1],c['certified_negative'][0],c['certified_negative'][1],time.time()-t1),flush=True)
if __name__=='__main__': json.dump(rows,open('/home/claude/bunkbed/v02/data/witnesses_above2.json','w'),indent=1)
