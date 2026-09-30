"""Independent checks of (i) the exact word identity at random rational
(q, lambda) using a brute-force hypergraph enumerator and the frontier-DP flow
polynomial; (ii) own conditioned-post DP vs brute force and vs the v0.1 stored
value; (iii) convergence of N^T/a_L^m to q^{t+2}F/(q-1)."""

# v0.3: proof-critical checks remain active under python -O and -OO.
def _require_v03(condition, message="Verification failed"):
    if not condition:
        raise ValueError(message)

import json, time, random, sys
from fractions import Fraction as Fr
from bb_tools import *
random.seed(20260930)
t0=time.time(); rep={}

# (i) word identity
words=[[0],[0,0],[0,1],[0,1,0],[0,1,2],[0,1,0,2],[0,1,2,0,2,1],[0,1,2,0,1,2],[0,0,1,2,2,1],[0,1,0,2,1,3,2,3],[0,1,2,3,1,3,0,2]]
res=[]
for wd in words:
    m=len(wd); t=max(wd)+1
    for trial in range(2):
        q=Fr(random.randint(2,9),random.randint(1,5))
        if q==1: q+=Fr(1,7)
        lam=[Fr(random.randint(1,9),random.randint(1,4)) for _ in range(m)]
        lhs=hyper_numerator(wd,q,lam)
        Fw=flow_poly_from_word(wd)
        prod=Fr(1)
        for l in lam: prod*=l
        rhs=q**(t+2)*prod*peval(Fw,q)/(q-1)
        _require_v03((lhs==rhs), (wd,q,lam,lhs,rhs))
        res.append({'word':wd,'q':str(q),'lambda':[str(l) for l in lam],'N':str(lhs)})
print("word identity: %d random-point checks passed (%d words, incl. loops/repeats)"%(len(res),len(words)))
rep['word_identity_checks']=res

# (ii) own core DP vs brute force (tiny) and vs v0.1 stored value
for (wd,L,q,x) in [([0,1],1,Fr(3,2),Fr(1)),([0,1],1,Fr(21,10),Fr(2,3)),([0,1],1,Fr(1,2),Fr(3,2)),([0,1,2],1,Fr(3),Fr(1)),([0,1,0],1,Fr(5,4),Fr(2))]:
    a=core_numerator(wd,L,q,x); b=core_numerator_bruteforce(wd,L,q,x)
    _require_v03((a==b), (wd,L,q,x,a,b))
print("own core DP == brute force on 5 tiny instances")
v01=json.load(open('/home/claude/bunkbed/v01/evidence_press_bunkbed_v0_1/certificates/q_3_2_core.json'))
t1=time.time()
a=core_numerator([0,1,2]*4,20,Fr(3,2),Fr(1))
print("own DP (ABC)^4, L=20, q=3/2, x=1: sign", "negative" if a<0 else "nonneg", "; equals v0.1 stored value:", str(a)==v01['core_numerator'], "(%.1fs)"%(time.time()-t1))
rep['core_3_2_L20_matches_v01']= (str(a)==v01['core_numerator'])
rep['core_3_2_L20_value_float']=float(a)

# (iii) convergence of the normalised numerator to the limit
def limit(wd,q):
    t=max(wd)+1; return q**(t+2)*peval(flow_poly_from_word(wd),q)/(q-1)
def aL(q,x,L):
    f=1+x; d=f*x*(q+x); return f*d**L/(q-1)
conv=[]
for (wd,q,x,Ls) in [([0,1,2]*2,Fr(3,2),Fr(1),[1,2,4,8,12,16,20]),([0,1,2]*4,Fr(3,2),Fr(1),[1,2,4,8,12,16,20,24]),
                    ([0,1,2]*2,Fr(21,10),Fr(1),[1,2,4,8,12,16]),([0,1,2]*2,Fr(3,2),Fr(1,3),[1,2,4,8,12]),
                    ([0,1,0,2,1,3,2,3],Fr(3,2),Fr(1),[1,2,4,6,8])]:
    m=len(wd); lim=limit(wd,q); rows=[]
    for L in Ls:
        t1=time.time(); N=core_numerator(wd,L,q,x); ratio=N/aL(q,x,L)**m
        rows.append({'L':L,'ratio':float(ratio),'sign':int(N>0)-int(N<0),'secs':round(time.time()-t1,2)})
    print("word",wd,"q",q,"x",x,"limit",float(lim))
    for r in rows: print("   L=%3d  N^T/a_L^m = %.9f  sign %+d  (%.1fs)"%(r['L'],r['ratio'],r['sign'],r['secs']))
    conv.append({'word':wd,'q':str(q),'x':str(x),'limit':float(lim),'rows':rows})
rep['convergence']=conv
rep['elapsed']=time.time()-t0
json.dump(rep,open('/home/claude/bunkbed/v02/data/word_core_audit.json','w'),indent=1)
print("elapsed",time.time()-t0)
