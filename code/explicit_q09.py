"""Explicit full-bunkbed counterexample below q=1: doubled-triangle fan core
(ABC)^2, L=21, q=9/10, x=1 (p=1/2).  Exact N(y) and minimal pendant count."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json,time,sys
from fractions import Fraction as Fr
from bb_tools import *
q,x=Fr(9,10),Fr(1); D=q*q+3*q*x+3*x*x; r=x**3/D
wd=[0,1,2]*2; t=3; L=int(sys.argv[1]) if len(sys.argv)>1 else 21
t1=time.time(); Ny=full_core_poly_int(wd,L,q,x); dt=time.time()-t1
NT=core_numerator(wd,L,q,x)
_require_v03((len(Ny)==t+1 and Ny[-1]==NT and NT<0), 'Validation failed in explicit_q09.py: 10')
k=0; yk=(1+x)-1
while not peval(Ny,yk)<0:
    k+=1; yk=(1+x)*(1+r)**k-1
n=t+6*L+1; e=6*(2*L+1)
rec={'q':str(q),'p':'1/2','word':wd,'L':L,'core_vertices':n,'core_edges':e,'N_y_coefficients':[str(c) for c in Ny],
     'coefficient_signs':[int(c>0)-int(c<0) for c in Ny],'a_t_equals_NT':True,'min_pendants_per_post':k,
     'base_vertices':n+3*k,'base_edges':e+3*k,'full_vertices':2*(n+3*k),'full_edges':2*(e+3*k)+(n+3*k),'N_y_seconds':round(dt,1)}
json.dump(rec,open('/home/claude/bunkbed/v02/data/explicit_q09_L%d.json'%L,'w'),indent=1)
print(json.dumps({k_:v for k_,v in rec.items() if k_!='N_y_coefficients'},indent=1))
