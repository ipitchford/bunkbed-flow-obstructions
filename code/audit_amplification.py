"""Independent checks of Lemma 4.1 (exact post amplification):
 (a) own full-bunkbed DP N(y) vs brute force on a tiny core, at several y;
 (b) leading coefficient a_t equals the conditioned-post numerator N^T;
 (c) pendant series-parallel reduction: factor D=q^2+3qx+3x^2 and effective
     activity y=(1+x)(1+r)-1, r=x^3/D, checked by brute force."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json,time
from fractions import Fraction as Fr
from bb_tools import *
t0=time.time(); rep={}
# (a),(b) tiny core: word [0,1], L=1 -> base: posts 0,1 ; path 2,3,4
for (wd,L,q,x) in [([0,1],1,Fr(3,2),Fr(1)),([0,1],1,Fr(21,10),Fr(1,2)),([0,1],1,Fr(7,10),Fr(2))]:
    n,E,u,v=fan_chain_edges(wd,L); t=max(wd)+1
    Ny=full_core_poly(wd,L,q,x)
    for y in (Fr(0),Fr(1),Fr(3),Fr(7,2)):
        acts={('v',s):y for s in range(t)}
        bf=full_bunkbed_bruteforce(n,E,u,v,q,x,acts)
        _require_v03((peval(Ny,y)==bf), (wd,y,peval(Ny,y),bf))
    NT=core_numerator(wd,L,q,x)
    lead=Ny[-1] if len(Ny)==t+1 else Fr(0)
    _require_v03((len(ptrim(Ny))<=t+1), 'Validation failed in audit_amplification.py: 20')
    print("word",wd,"L",L,"q",q,"x",x,": N(y) =",[str(c) for c in Ny]," a_t =",lead," N^T =",NT," equal:",lead==NT)
    _require_v03((lead==NT), 'Validation failed in audit_amplification.py: 22')
rep['tiny_core_checks']='N(y) DP == brute force at 4 values of y; a_t == N^T (3 instances)'
# (c) pendant reduction on a small base graph: triangle a=0,b=1,c=2 plus pendant p=3 at a; u=b, v=c
q,x=Fr(3,2),Fr(1)
D=q*q+3*q*x+3*x*x; r=x**3/D; y1=(1+x)*(1+r)-1
E_with=[(0,1),(1,2),(0,2),(0,3)]; E_without=[(0,1),(1,2),(0,2)]
with_p=full_bunkbed_bruteforce(4,E_with,1,2,q,x)
without=full_bunkbed_bruteforce(3,E_without,1,2,q,x,{('v',0):y1})
print("pendant reduction: N(with pendant) =",with_p,"; D * N(y1) =",D*without,"; equal:",with_p==D*without)
_require_v03((with_p==D*without), 'Validation failed in audit_amplification.py: 31')
# two pendants at a
E2=[(0,1),(1,2),(0,2),(0,3),(0,4)]; y2=(1+x)*(1+r)**2-1
w2=full_bunkbed_bruteforce(5,E2,1,2,q,x); wo2=full_bunkbed_bruteforce(3,E_without,1,2,q,x,{('v',0):y2})
_require_v03((w2==D*D*wo2), 'Validation failed in audit_amplification.py: 35'); print("two pendants:", w2==D*D*wo2)
rep['pendant_reduction_bruteforce']=True
rep['elapsed']=time.time()-t0
json.dump(rep,open('/home/claude/bunkbed/v02/data/amplification_audit.json','w'),indent=1)
print("elapsed",time.time()-t0)
