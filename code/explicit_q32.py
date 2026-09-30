"""Exact N(y) for the smallest negative core (ell=4, L=19) at q=3/2, x=1, and
the minimal number of pendant vertices per post that makes the full bunkbed
numerator negative.  Also repeats for L=20 (the v0.1 core) for comparison."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json,time,sys
from fractions import Fraction as Fr
from bb_tools import *
import math
def sf(x):
    x=Fr(x)
    if x==0: return 0.0
    sgn=-1 if x<0 else 1; x=abs(x)
    e=len(str(x.numerator))-len(str(x.denominator))
    return sgn*float(Fr(x.numerator,x.denominator)/Fr(10)**e)*10.0**e if abs(e)<300 else sgn*float('inf')

q,x=Fr(3,2),Fr(1); D=q*q+3*q*x+3*x*x; r=x**3/D
out={}
for L in ([int(a) for a in sys.argv[1:]] or (19,20)):
    wd=[0,1,2]*4; t=3
    t1=time.time(); Ny=full_core_poly_int(wd,L,q,x); dt=time.time()-t1
    NT=core_numerator(wd,L,q,x)
    _require_v03((len(Ny)==t+1 and Ny[-1]==NT), "leading coefficient must equal the conditioned numerator")
    # largest real root of the cubic N(y) (a_3<0): N(y)<0 for y beyond it
    negs,roots=negative_intervals([Fr(c) for c in Ny],Fr(0),Fr(10**12),eps=Fr(1,10**12))
    ystar=max(hi for lo,hi in roots) if roots else Fr(0)
    # minimal k with y_k=(1+x)(1+r)^k-1 > ystar and N(y_k)<0 (check exactly)
    k=0; yk=(1+x)-1
    while not (yk>ystar and peval(Ny,yk)<0):
        k+=1; yk=(1+x)*(1+r)**k-1
    _require_v03((peval(Ny,yk)<0 and (k==0 or not peval(Ny,(1+x)*(1+r)**(k-1)-1)<0)), 'Validation failed in explicit_q32.py: 29')
    n=t+12*L+1; e=12*(2*L+1)
    rec={'L':L,'core_vertices':n,'core_edges':e,'N_y_coefficients':[str(c) for c in Ny],
         'a_t_equals_NT':True,'largest_root_y_upper':str(ystar),'largest_root_y_float':sf(ystar),
         'min_pendants_per_post':k,'y_k':str(yk),'base_vertices':n+3*k,'base_edges':e+3*k,
         'full_vertices':2*(n+3*k),'full_edges':2*(e+3*k)+(n+3*k),'N_y_seconds':round(dt,1)}
    out[f'L{L}']=rec
    print(json.dumps({k_:v for k_,v in rec.items() if k_!='N_y_coefficients'},indent=1),flush=True)
    print("  coefficient signs:",[int(c>0)-int(c<0) for c in Ny], " log10|c|:",[ (len(str(abs(c.numerator)))-len(str(c.denominator))) for c in Ny])
json.dump(out,open('/home/claude/bunkbed/v02/data/explicit_q32_L%s.json'%('_'.join(sys.argv[1:]) or 'all'),'w'),indent=1)
