"""Scan thickened-triangle fan cores at q=3/2, x=1 (p=1/2) for the smallest
core with a negative conditioned-post numerator."""
import json,time
from fractions import Fraction as Fr
from bb_tools import *
q,x=Fr(3,2),Fr(1); rows=[]
t0=time.time()
for ell in (4,6,8):
    wd=[0,1,2]*ell; m=len(wd)
    lim=q**5*peval(flow_poly_from_word(wd),q)/(q-1)
    for L in range(6,26):
        n=3+m*L+1
        t1=time.time(); N=core_numerator(wd,L,q,x); dt=time.time()-t1
        rows.append({'ell':ell,'L':L,'core_vertices':n,'core_edges':m*(2*L+1),'sign':int(N>0)-int(N<0),'value':str(N),'secs':round(dt,1)})
        print("ell=%d L=%2d n=%4d sign=%+d  N=%.6g (%.1fs)"%(ell,L,n,rows[-1]['sign'],float(N),dt),flush=True)
        if N<0 and L>=8: break
json.dump(rows,open('/home/claude/bunkbed/v02/data/scan_q32_cores.json','w'),indent=1)
neg=[r for r in rows if r['sign']<0]
best=min(neg,key=lambda r:r['core_vertices']) if neg else None
print("smallest negative core:",best)
print("elapsed",time.time()-t0)
